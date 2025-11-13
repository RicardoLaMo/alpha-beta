"""
Canvas New Quiz Creator with Item Bank Support
===============================================
This script creates Canvas New Quizzes with support for:
- Direct questions (all students get the same questions)
- Item banks (question pools for randomization)
- Item bank groups (randomly select N questions from a bank for each student)

This allows each student to receive different questions from the pool.
"""

import json
import os
import uuid
from pathlib import Path
import requests
from typing import Dict, List, Any, Optional

# ============================================================================
# Configuration
# ============================================================================

BASE = os.environ.get('CANVAS_API_URL', 'https://instructure.charlotte.edu')
COURSE_ID = 89667
JSON_PATH = os.environ.get('QUIZ_JSON_PATH', 'quiz_with_item_banks.json')

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
# Helper Functions
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


def add_question_to_bank(course_id: int, bank_id: str, question: Dict[str, Any], idx: int = 1) -> Dict[str, Any]:
    """
    Add a question to an item bank.

    Args:
        course_id: Canvas course ID
        bank_id: Item bank ID
        question: Question configuration
        idx: Question index for display

    Returns:
        Created item data
    """
    q_type = question.get('type', 'numeric')

    # Build the item payload based on question type
    if q_type == 'numeric':
        item_payload = build_numeric_item(question, idx)
    elif q_type == 'multiple_choice':
        item_payload = build_multiple_choice_item(question, idx)
    elif q_type == 'true_false':
        item_payload = build_true_false_item(question, idx)
    elif q_type == 'essay':
        item_payload = build_essay_item(question, idx)
    else:
        raise ValueError(f"Unsupported question type: {q_type}")

    item = rq('POST', f"/api/quiz/v1/courses/{course_id}/item_banks/{bank_id}/items", json=item_payload)
    print(f"  Added item {item['id']} to bank ({item['entry']['title']})")
    return item


def build_numeric_item(q: Dict[str, Any], idx: int) -> Dict[str, Any]:
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

    return {
        'item': {
            'entry_type': 'Item',
            'points_possible': q.get('points', 1),
            'entry': {
                'title': q.get('title', f'Question {idx}'),
                'item_body': q['body'],
                'calculator_type': q.get('calculator_type', 'none'),
                'interaction_type_slug': 'numeric',
                'interaction_data': {},
                'scoring_algorithm': 'Numeric',
                'scoring_data': {'value': [scoring_value]}
            }
        }
    }


def build_multiple_choice_item(q: Dict[str, Any], idx: int) -> Dict[str, Any]:
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

    return {
        'item': {
            'entry_type': 'Item',
            'points_possible': q.get('points', 1),
            'entry': {
                'title': q.get('title', f'Question {idx}'),
                'item_body': q['body'],
                'interaction_type_slug': 'choice',
                'interaction_data': interaction_data,
                'scoring_algorithm': 'Equivalence',
                'scoring_data': scoring_data
            }
        }
    }


def build_true_false_item(q: Dict[str, Any], idx: int) -> Dict[str, Any]:
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

    return {
        'item': {
            'entry_type': 'Item',
            'points_possible': q.get('points', 1),
            'entry': {
                'title': q.get('title', f'Question {idx}'),
                'item_body': q['body'],
                'interaction_type_slug': 'choice',
                'interaction_data': interaction_data,
                'scoring_algorithm': 'Equivalence',
                'scoring_data': {'value': [{'id': str(uuid.uuid4()), 'value': correct_id}]}
            }
        }
    }


def build_essay_item(q: Dict[str, Any], idx: int) -> Dict[str, Any]:
    """Build an essay question item payload."""
    return {
        'item': {
            'entry_type': 'Item',
            'points_possible': q.get('points', 1),
            'entry': {
                'title': q.get('title', f'Question {idx}'),
                'item_body': q['body'],
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


def add_direct_question_to_quiz(course_id: int, quiz_id: str, question: Dict[str, Any], idx: int) -> Dict[str, Any]:
    """
    Add a question directly to a quiz (not from a bank).
    All students will see this question.

    Args:
        course_id: Canvas course ID
        quiz_id: Quiz ID
        question: Question configuration
        idx: Question index

    Returns:
        Created item data
    """
    q_type = question.get('type', 'numeric')

    if q_type == 'numeric':
        item_payload = build_numeric_item(question, idx)
    elif q_type == 'multiple_choice':
        item_payload = build_multiple_choice_item(question, idx)
    elif q_type == 'true_false':
        item_payload = build_true_false_item(question, idx)
    elif q_type == 'essay':
        item_payload = build_essay_item(question, idx)
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

    Args:
        json_path: Path to JSON configuration file
        course_id: Canvas course ID

    Returns:
        Created quiz data
    """
    cfg = json.loads(Path(json_path).read_text())
    quiz_cfg = cfg['quiz']

    # ========================================================================
    # Step 1: Create Item Banks (if any)
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
                add_question_to_bank(course_id, bank['id'], question, idx)

    # ========================================================================
    # Step 2: Create the Quiz
    # ========================================================================
    print("\n=== Creating Quiz ===")
    instructions_html = quiz_cfg.get('instructions') or quiz_cfg.get('description', '')

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
    # Step 3: Add Content to Quiz
    # ========================================================================
    print("\n=== Adding Content to Quiz ===")

    # If quiz_structure is defined, use it (allows mixing direct questions and banks)
    if 'quiz_structure' in cfg:
        question_counter = 1
        for item in cfg['quiz_structure']:
            if item['type'] == 'direct_question':
                question = item['question']
                add_direct_question_to_quiz(course_id, quiz_id, question, question_counter)
                question_counter += 1
            elif item['type'] == 'item_bank_group':
                bank_name = item['bank_name']
                if bank_name not in item_banks:
                    raise ValueError(f"Unknown item bank: {bank_name}")
                add_item_bank_group_to_quiz(course_id, quiz_id, item_banks[bank_name], item)
    else:
        # Legacy support: add direct questions if no structure defined
        for idx, question in enumerate(direct_questions, 1):
            add_direct_question_to_quiz(course_id, quiz_id, question, idx)

    # ========================================================================
    # Step 4: Publish if Requested
    # ========================================================================
    if quiz_cfg.get('publish'):
        print("\n=== Publishing Quiz ===")
        publish_payload = {'assignment': {'published': True}}
        assignment = rq('PUT', f"/api/v1/courses/{course_id}/assignments/{quiz_id}", json=publish_payload)
        print(f"Assignment published? {assignment['published']}")
    else:
        print('\nQuiz left unpublished (publish flag false).')

    print(f"\nReview: {BASE}/courses/{course_id}/assignments/{quiz_id}?display=full_width_with_nav")

    return new_quiz


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == '__main__':
    create_quiz_from_json(JSON_PATH, COURSE_ID)
