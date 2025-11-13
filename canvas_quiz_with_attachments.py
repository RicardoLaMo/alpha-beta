"""
Canvas New Quiz Creator with Item Bank and File Attachment Support
====================================================================
This script creates Canvas New Quizzes with support for:
- Direct questions (all students get the same questions)
- Item banks (question pools for randomization)
- Item bank groups (randomly select N questions from a bank for each student)
- File attachments (Excel files, PDFs, etc.) for students to download and use

This allows students to download data files, work on them, and submit answers.
"""

import json
import os
import uuid
from pathlib import Path
import requests
from typing import Dict, List, Any, Optional
import mimetypes

# ============================================================================
# Configuration
# ============================================================================

BASE = os.environ.get('CANVAS_API_URL', 'https://instructure.charlotte.edu')
COURSE_ID = 89667
JSON_PATH = os.environ.get('QUIZ_JSON_PATH', 'quiz_with_attachments.json')

# ============================================================================
# API Setup
# ============================================================================

if 'rq' not in globals():
    TOKEN = os.environ.get('CANVAS_API_KEY') or globals().get('API_KEY')
    if not TOKEN:
        raise RuntimeError('Set CANVAS_API_KEY or define API_KEY before running this cell.')

    S = requests.Session()
    S.headers.update({"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})

    def rq(method, path, **kw):
        """Make an API request and handle errors."""
        resp = S.request(method, BASE + path, **kw)
        if resp.status_code >= 400:
            raise RuntimeError(f"{resp.status_code} {resp.text[:500]}")
        return resp.json()

# ============================================================================
# File Upload Functions
# ============================================================================

def upload_file_to_canvas(course_id: int, file_path: str, folder: str = "quiz_files") -> Dict[str, Any]:
    """
    Upload a file to Canvas course files.

    Args:
        course_id: Canvas course ID
        file_path: Local path to the file
        folder: Folder name in Canvas (default: "quiz_files")

    Returns:
        Uploaded file data including URL
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    file_name = file_path.name
    file_size = file_path.stat().st_size
    content_type = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

    print(f"Uploading {file_name} ({file_size} bytes)...")

    # Step 1: Tell Canvas we want to upload a file
    upload_params = {
        'name': file_name,
        'size': file_size,
        'content_type': content_type,
        'parent_folder_path': folder
    }

    upload_url = f"/api/v1/courses/{course_id}/files"
    response = rq('POST', upload_url, json=upload_params)

    # Step 2: Upload the file to the provided URL
    upload_url = response['upload_url']
    upload_params = response['upload_params']

    with open(file_path, 'rb') as f:
        files = {'file': (file_name, f, content_type)}
        upload_response = requests.post(upload_url, data=upload_params, files=files)

        if upload_response.status_code >= 400:
            raise RuntimeError(f"File upload failed: {upload_response.text[:500]}")

    # Step 3: Get the file information
    if upload_response.status_code == 301:
        # Follow redirect to get file info
        location = upload_response.headers.get('Location')
        file_info = requests.get(location, headers=S.headers).json()
    else:
        file_info = upload_response.json()

    print(f"  ✓ Uploaded: {file_info['url']}")
    return file_info


def create_file_download_html(file_info: Dict[str, Any], description: str = None) -> str:
    """
    Create HTML for a file download link.

    Args:
        file_info: File information from Canvas
        description: Optional description text

    Returns:
        HTML string for embedding in quiz/questions
    """
    file_name = file_info['display_name']
    file_url = file_info['url']
    file_id = file_info['id']

    desc_text = description or f"Download {file_name}"

    html = f'''<div class="file-download" style="padding: 10px; background-color: #f0f0f0; border-left: 4px solid #0374B5; margin: 10px 0;">
    <p><strong>📎 Required File:</strong></p>
    <p><a href="/courses/{COURSE_ID}/files/{file_id}/download?download_frd=1" class="btn btn-primary" target="_blank">
        <i class="icon-download"></i> {desc_text}
    </a></p>
    <p><em>Click the button above to download the data file. You will need to work with this file to answer the questions.</em></p>
</div>'''

    return html


# ============================================================================
# Item Bank Functions
# ============================================================================

def create_item_bank(course_id: int, bank_name: str, description: str = "") -> Dict[str, Any]:
    """
    Create an item bank (question pool).

    Args:
        course_id: Canvas course ID
        bank_name: Name of the item bank
        description: Optional description

    Returns:
        Created item bank data
    """
    payload = {
        'item_bank': {
            'title': bank_name,
            'description': description
        }
    }
    bank = rq('POST', f"/api/quiz/v1/courses/{course_id}/item_banks", json=payload)
    print(f"Created item bank {bank['id']}: {bank['title']}")
    return bank


def add_question_to_bank(course_id: int, bank_id: str, question: Dict[str, Any],
                        idx: int = 1, uploaded_files: Dict[str, Dict] = None) -> Dict[str, Any]:
    """
    Add a question to an item bank.

    Args:
        course_id: Canvas course ID
        bank_id: Item bank ID
        question: Question configuration
        idx: Question index for display
        uploaded_files: Dictionary of uploaded file info (for embedding in questions)

    Returns:
        Created item data
    """
    q_type = question.get('type', 'numeric')

    # Build the item payload based on question type
    if q_type == 'numeric':
        item_payload = build_numeric_item(question, idx, uploaded_files)
    elif q_type == 'multiple_choice':
        item_payload = build_multiple_choice_item(question, idx, uploaded_files)
    elif q_type == 'true_false':
        item_payload = build_true_false_item(question, idx, uploaded_files)
    elif q_type == 'essay':
        item_payload = build_essay_item(question, idx, uploaded_files)
    else:
        raise ValueError(f"Unsupported question type: {q_type}")

    item = rq('POST', f"/api/quiz/v1/courses/{course_id}/item_banks/{bank_id}/items", json=item_payload)
    print(f"  Added item {item['id']} to bank ({item['entry']['title']})")
    return item


def build_numeric_item(q: Dict[str, Any], idx: int, uploaded_files: Dict = None) -> Dict[str, Any]:
    """Build a numeric question item payload."""
    scoring_type = q.get('scoring_type', 'marginOfError')
    scoring_value = {
        'id': str(uuid.uuid4()),
        'type': scoring_type,
        'value': str(q['correct_value'])
    }

    if scoring_type == 'marginOfError':
        scoring_value['margin'] = str(q.get('margin', '0.5'))
        scoring_value['margin_type'] = q.get('margin_type', 'absolute')

    # Embed file link if specified
    body = q['body']
    if 'attached_file' in q and uploaded_files:
        file_key = q['attached_file']
        if file_key in uploaded_files:
            file_html = create_file_download_html(uploaded_files[file_key])
            body = file_html + '<br>' + body

    return {
        'item': {
            'entry_type': 'Item',
            'points_possible': q.get('points', 1),
            'entry': {
                'title': q.get('title', f'Question {idx}'),
                'item_body': body,
                'calculator_type': q.get('calculator_type', 'none'),
                'interaction_type_slug': 'numeric',
                'interaction_data': {},
                'scoring_algorithm': 'Numeric',
                'scoring_data': {'value': [scoring_value]}
            }
        }
    }


def build_multiple_choice_item(q: Dict[str, Any], idx: int, uploaded_files: Dict = None) -> Dict[str, Any]:
    """Build a multiple choice question item payload."""
    answers = q.get('answers', [])
    if not answers:
        raise ValueError(f"Multiple choice question {idx} must have answers")

    # Build interaction data with answer options
    interaction_data = {
        'shuffle': q.get('shuffle_answers', False),
        'choices': []
    }

    scoring_data = {'value': []}

    for answer in answers:
        choice_id = str(uuid.uuid4())
        interaction_data['choices'].append({
            'id': choice_id,
            'item_body': answer['text']
        })

        if answer.get('correct', False):
            scoring_data['value'].append({
                'id': str(uuid.uuid4()),
                'value': choice_id
            })

    # Embed file link if specified
    body = q['body']
    if 'attached_file' in q and uploaded_files:
        file_key = q['attached_file']
        if file_key in uploaded_files:
            file_html = create_file_download_html(uploaded_files[file_key])
            body = file_html + '<br>' + body

    return {
        'item': {
            'entry_type': 'Item',
            'points_possible': q.get('points', 1),
            'entry': {
                'title': q.get('title', f'Question {idx}'),
                'item_body': body,
                'interaction_type_slug': 'choice',
                'interaction_data': interaction_data,
                'scoring_algorithm': 'Equivalence',
                'scoring_data': scoring_data
            }
        }
    }


def build_true_false_item(q: Dict[str, Any], idx: int, uploaded_files: Dict = None) -> Dict[str, Any]:
    """Build a true/false question item payload."""
    correct_answer = q.get('correct_answer', True)

    true_id = str(uuid.uuid4())
    false_id = str(uuid.uuid4())

    interaction_data = {
        'shuffle': False,
        'choices': [
            {'id': true_id, 'item_body': 'True'},
            {'id': false_id, 'item_body': 'False'}
        ]
    }

    correct_id = true_id if correct_answer else false_id

    # Embed file link if specified
    body = q['body']
    if 'attached_file' in q and uploaded_files:
        file_key = q['attached_file']
        if file_key in uploaded_files:
            file_html = create_file_download_html(uploaded_files[file_key])
            body = file_html + '<br>' + body

    return {
        'item': {
            'entry_type': 'Item',
            'points_possible': q.get('points', 1),
            'entry': {
                'title': q.get('title', f'Question {idx}'),
                'item_body': body,
                'interaction_type_slug': 'choice',
                'interaction_data': interaction_data,
                'scoring_algorithm': 'Equivalence',
                'scoring_data': {'value': [{'id': str(uuid.uuid4()), 'value': correct_id}]}
            }
        }
    }


def build_essay_item(q: Dict[str, Any], idx: int, uploaded_files: Dict = None) -> Dict[str, Any]:
    """Build an essay question item payload."""
    # Embed file link if specified
    body = q['body']
    if 'attached_file' in q and uploaded_files:
        file_key = q['attached_file']
        if file_key in uploaded_files:
            file_html = create_file_download_html(uploaded_files[file_key])
            body = file_html + '<br>' + body

    return {
        'item': {
            'entry_type': 'Item',
            'points_possible': q.get('points', 1),
            'entry': {
                'title': q.get('title', f'Question {idx}'),
                'item_body': body,
                'interaction_type_slug': 'essay',
                'interaction_data': {},
                'scoring_algorithm': 'None',
                'scoring_data': {}
            }
        }
    }


def add_item_bank_group_to_quiz(course_id: int, quiz_id: str, bank_id: str,
                                 group_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add an item bank group to a quiz.

    An item bank group randomly selects N questions from the bank for each student.

    Args:
        course_id: Canvas course ID
        quiz_id: Quiz ID
        bank_id: Item bank ID
        group_config: Configuration with 'pick_count' and optional 'points_per_item'

    Returns:
        Created group data
    """
    pick_count = group_config.get('pick_count', 1)
    points_per_item = group_config.get('points_per_item', 1)

    payload = {
        'item': {
            'entry_type': 'ItemBank',
            'item_bank_id': bank_id,
            'assessment_item_bank_count': pick_count,
            'points_possible': points_per_item
        }
    }

    group = rq('POST', f"/api/quiz/v1/courses/{course_id}/quizzes/{quiz_id}/items", json=payload)
    print(f"  Added item bank group: will pick {pick_count} question(s) from bank {bank_id}")
    return group


def add_direct_question_to_quiz(course_id: int, quiz_id: str, question: Dict[str, Any],
                                idx: int, uploaded_files: Dict = None) -> Dict[str, Any]:
    """
    Add a question directly to a quiz (not from a bank).
    All students will see this question.

    Args:
        course_id: Canvas course ID
        quiz_id: Quiz ID
        question: Question configuration
        idx: Question index
        uploaded_files: Dictionary of uploaded file info

    Returns:
        Created item data
    """
    q_type = question.get('type', 'numeric')

    if q_type == 'numeric':
        item_payload = build_numeric_item(question, idx, uploaded_files)
    elif q_type == 'multiple_choice':
        item_payload = build_multiple_choice_item(question, idx, uploaded_files)
    elif q_type == 'true_false':
        item_payload = build_true_false_item(question, idx, uploaded_files)
    elif q_type == 'essay':
        item_payload = build_essay_item(question, idx, uploaded_files)
    else:
        raise ValueError(f"Unsupported question type: {q_type}")

    item = rq('POST', f"/api/quiz/v1/courses/{course_id}/quizzes/{quiz_id}/items", json=item_payload)
    print(f"  Added direct item {item['id']} ({item['entry']['title']})")
    return item


# ============================================================================
# Main Quiz Creation Function
# ============================================================================

def create_quiz_from_json(json_path: str, course_id: int) -> Dict[str, Any]:
    """
    Create a Canvas New Quiz from a JSON configuration file.

    Supports:
    - Direct questions (all students see these)
    - Item banks with randomized question selection
    - File attachments (Excel, PDF, etc.)

    Args:
        json_path: Path to JSON configuration file
        course_id: Canvas course ID

    Returns:
        Created quiz data
    """
    cfg = json.loads(Path(json_path).read_text())
    quiz_cfg = cfg['quiz']

    # ========================================================================
    # Step 1: Upload Files (if any)
    # ========================================================================
    uploaded_files = {}
    if 'files' in cfg:
        print("\n=== Uploading Files ===")
        for file_key, file_path in cfg['files'].items():
            try:
                file_info = upload_file_to_canvas(course_id, file_path)
                uploaded_files[file_key] = file_info
            except Exception as e:
                print(f"  ✗ Failed to upload {file_path}: {e}")
                raise

    # ========================================================================
    # Step 2: Create Item Banks (if any)
    # ========================================================================
    item_banks = {}
    if 'item_banks' in cfg:
        print("\n=== Creating Item Banks ===")
        for bank_cfg in cfg['item_banks']:
            bank_name = bank_cfg['name']
            bank_desc = bank_cfg.get('description', '')
            bank = create_item_bank(course_id, bank_name, bank_desc)
            item_banks[bank_name] = bank['id']

            # Add questions to this bank
            questions = bank_cfg.get('questions', [])
            for idx, question in enumerate(questions, 1):
                add_question_to_bank(course_id, bank['id'], question, idx, uploaded_files)

    # ========================================================================
    # Step 3: Create the Quiz
    # ========================================================================
    print("\n=== Creating Quiz ===")
    instructions_html = quiz_cfg.get('instructions') or quiz_cfg.get('description', '')

    # Add file download links to instructions if specified
    if 'attached_files' in quiz_cfg and uploaded_files:
        file_links_html = '<div style="margin-bottom: 20px;">'
        for file_key in quiz_cfg['attached_files']:
            if file_key in uploaded_files:
                file_links_html += create_file_download_html(uploaded_files[file_key])
        file_links_html += '</div>'
        instructions_html = file_links_html + instructions_html

    default_settings = {
        'allow_backtracking': True,
        'shuffle_questions': False,
        'shuffle_answers': False,
        'has_time_limit': False
    }
    quiz_settings = default_settings | quiz_cfg.get('quiz_settings', {})

    # Calculate total points
    total_points = 0

    # Points from direct questions
    direct_questions = cfg.get('questions', [])
    total_points += sum(q.get('points', 1) for q in direct_questions)

    # Points from item bank groups
    if 'quiz_structure' in cfg:
        for item in cfg['quiz_structure']:
            if item['type'] == 'item_bank_group':
                pick_count = item.get('pick_count', 1)
                points_per_item = item.get('points_per_item', 1)
                total_points += pick_count * points_per_item
            elif item['type'] == 'direct_question':
                total_points += item['question'].get('points', 1)

    quiz_payload = {
        'quiz': {
            'title': quiz_cfg['title'],
            'instructions': instructions_html,
            'points_possible': total_points,
            'published': False,
            'quiz_settings': quiz_settings
        }
    }

    new_quiz = rq('POST', f"/api/quiz/v1/courses/{course_id}/quizzes", json=quiz_payload)
    quiz_id = new_quiz['id']
    print(f"Created quiz {quiz_id}: {new_quiz['title']}")

    # ========================================================================
    # Step 4: Add Content to Quiz
    # ========================================================================
    print("\n=== Adding Content to Quiz ===")

    # If quiz_structure is defined, use it (allows mixing direct questions and banks)
    if 'quiz_structure' in cfg:
        question_counter = 1
        for item in cfg['quiz_structure']:
            if item['type'] == 'direct_question':
                question = item['question']
                add_direct_question_to_quiz(course_id, quiz_id, question, question_counter, uploaded_files)
                question_counter += 1
            elif item['type'] == 'item_bank_group':
                bank_name = item['bank_name']
                if bank_name not in item_banks:
                    raise ValueError(f"Unknown item bank: {bank_name}")
                add_item_bank_group_to_quiz(course_id, quiz_id, item_banks[bank_name], item)
    else:
        # Legacy support: add direct questions if no structure defined
        for idx, question in enumerate(direct_questions, 1):
            add_direct_question_to_quiz(course_id, quiz_id, question, idx, uploaded_files)

    # ========================================================================
    # Step 5: Publish if Requested
    # ========================================================================
    if quiz_cfg.get('publish'):
        print("\n=== Publishing Quiz ===")
        publish_payload = {'assignment': {'published': True}}
        assignment = rq('PUT', f"/api/v1/courses/{course_id}/assignments/{quiz_id}", json=publish_payload)
        print(f"Assignment published? {assignment['published']}")
    else:
        print('\nQuiz left unpublished (publish flag false).')

    print(f"\n✅ Quiz created successfully!")
    print(f"Review: {BASE}/courses/{course_id}/assignments/{quiz_id}?display=full_width_with_nav")

    return new_quiz


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == '__main__':
    create_quiz_from_json(JSON_PATH, COURSE_ID)
