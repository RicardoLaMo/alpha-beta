# Canvas New Quiz Creator with Item Banks

## Overview

This enhanced Canvas quiz creation system allows you to create quizzes where **each student receives different questions** from question pools (item banks). This is ideal for:

- **Midterm exams** - Reduce cheating by giving each student a unique set of questions
- **Practice quizzes** - Provide varied practice opportunities
- **Assessment banks** - Maintain large pools of questions and randomly select from them

## Key Features

### 1. **Item Banks (Question Pools)**
- Create pools of questions organized by topic or difficulty
- Questions are stored in the bank and can be reused across multiple quizzes

### 2. **Item Bank Groups**
- Randomly select N questions from a bank for each student
- Each student gets a different combination of questions

### 3. **Multiple Question Types**
- Numeric (with margin of error)
- Multiple Choice
- True/False
- Essay

### 4. **Flexible Quiz Structure**
- All randomized questions from item banks
- All direct questions (everyone sees the same)
- Mixed: Some direct questions + some randomized from banks

## How It Works

### For a Midterm with Randomized Questions

If you have:
- **5 questions** in an item bank
- Set to **pick 3 questions** per student

Then:
- Student A might get questions 1, 3, 5
- Student B might get questions 2, 3, 4
- Student C might get questions 1, 2, 5

**Each student has a different exam!**

## Installation & Setup

### 1. Set Environment Variables

```bash
export CANVAS_API_KEY="your_canvas_api_token_here"
export CANVAS_API_URL="https://instructure.charlotte.edu"
export QUIZ_JSON_PATH="example_midterm_with_item_banks.json"
```

### 2. Run the Script

```bash
python canvas_quiz_with_item_banks.py
```

Or import it in a Jupyter notebook:

```python
from canvas_quiz_with_item_banks import create_quiz_from_json

create_quiz_from_json('example_midterm_with_item_banks.json', course_id=89667)
```

## JSON Configuration Guide

### Basic Structure

```json
{
  "quiz": { ... },           // Quiz settings
  "item_banks": [ ... ],     // Optional: Question pools
  "questions": [ ... ],      // Optional: Direct questions (legacy support)
  "quiz_structure": [ ... ]  // Optional: Define order of content
}
```

### Quiz Settings

```json
{
  "quiz": {
    "title": "My Quiz Title",
    "instructions": "<p>Quiz instructions in HTML</p>",
    "publish": false,
    "quiz_settings": {
      "allow_backtracking": true,
      "shuffle_questions": true,
      "shuffle_answers": true,
      "has_time_limit": true,
      "time_limit": 60
    }
  }
}
```

### Defining Item Banks

```json
{
  "item_banks": [
    {
      "name": "Numeric Temperature Questions",
      "description": "Pool of temperature conversion problems",
      "questions": [
        {
          "type": "numeric",
          "title": "Freezing point",
          "body": "<p>What is the freezing point of water in Celsius?</p>",
          "correct_value": "0",
          "margin": "0.2",
          "margin_type": "absolute",
          "points": 2
        },
        {
          "type": "multiple_choice",
          "title": "Temperature scale",
          "body": "<p>Which scale starts at absolute zero?</p>",
          "shuffle_answers": true,
          "points": 3,
          "answers": [
            {"text": "Kelvin", "correct": true},
            {"text": "Celsius", "correct": false},
            {"text": "Fahrenheit", "correct": false}
          ]
        }
      ]
    }
  ]
}
```

### Using Item Banks in Quiz

```json
{
  "quiz_structure": [
    {
      "type": "item_bank_group",
      "bank_name": "Numeric Temperature Questions",
      "pick_count": 3,
      "points_per_item": 2
    }
  ]
}
```

This will:
- Randomly select **3 questions** from the "Numeric Temperature Questions" bank
- Each question is worth **2 points**
- Each student gets a **different set of 3 questions**

## Question Types

### 1. Numeric Questions

```json
{
  "type": "numeric",
  "title": "Question title",
  "body": "<p>Question text in HTML</p>",
  "correct_value": "42",
  "margin": "0.5",
  "margin_type": "absolute",
  "points": 2,
  "calculator_type": "basic"
}
```

**Margin types:**
- `"absolute"` - Accept answers within ±0.5 of correct value
- `"percentage"` - Accept answers within ±5% of correct value

**Calculator types:**
- `"none"` - No calculator
- `"basic"` - Basic calculator
- `"scientific"` - Scientific calculator

### 2. Multiple Choice Questions

```json
{
  "type": "multiple_choice",
  "title": "Question title",
  "body": "<p>Question text</p>",
  "shuffle_answers": true,
  "points": 3,
  "answers": [
    {"text": "Correct answer", "correct": true},
    {"text": "Wrong answer 1", "correct": false},
    {"text": "Wrong answer 2", "correct": false},
    {"text": "Also correct", "correct": true}
  ]
}
```

**Note:** You can have multiple correct answers for "select all that apply" questions.

### 3. True/False Questions

```json
{
  "type": "true_false",
  "title": "Question title",
  "body": "<p>True or False: The sky is blue.</p>",
  "correct_answer": true,
  "points": 2
}
```

### 4. Essay Questions

```json
{
  "type": "essay",
  "title": "Question title",
  "body": "<p>Explain your reasoning...</p>",
  "points": 10
}
```

**Note:** Essay questions require manual grading.

## Common Use Cases

### Use Case 1: Midterm with All Randomized Questions

Create multiple item banks (one per topic) and use item bank groups to select questions from each.

**See:** `example_midterm_with_item_banks.json`

**Benefits:**
- Each student gets a unique exam
- Reduces cheating
- Maintains fairness (all questions from same difficulty pool)

### Use Case 2: Mixed Direct and Randomized Questions

Some questions everyone must answer (e.g., essay questions), while calculation problems are randomized.

**See:** `example_mixed_quiz.json`

**Structure:**
1. Direct question (everyone sees this)
2. Item bank group (randomized)
3. Another direct question (everyone sees this)

### Use Case 3: Legacy Format (No Item Banks)

Continue using the original format for simple quizzes where everyone gets the same questions.

**See:** `example_original_format.json`

## Tips for Creating Effective Item Banks

### 1. **Equivalent Difficulty**
All questions in a bank should be approximately the same difficulty level, since students will be randomly assigned questions.

### 2. **Sufficient Pool Size**
Create more questions than you'll use:
- If picking 3 questions, create at least 5-10 in the bank
- Provides better randomization
- Allows for question reuse across multiple quiz attempts

### 3. **Organize by Topic**
Create separate banks for different topics:
```json
{
  "item_banks": [
    {"name": "Temperature Conversions", "questions": [...]},
    {"name": "Pressure Calculations", "questions": [...]},
    {"name": "Volume Problems", "questions": [...]}
  ]
}
```

### 4. **Balance Points**
When using `points_per_item`, ensure all questions in that bank are worth the same or adjust individually.

## Advanced Configuration

### Shuffle Settings

```json
{
  "quiz_settings": {
    "shuffle_questions": true,   // Randomize question order
    "shuffle_answers": true      // Randomize answer order (MC questions)
  }
}
```

**Recommendation for Midterms:**
- `shuffle_questions: true` - Different question order for each student
- `shuffle_answers: true` - Prevents "the answer is B" sharing

### Time Limits

```json
{
  "quiz_settings": {
    "has_time_limit": true,
    "time_limit": 60          // 60 minutes
  }
}
```

### Backtracking

```json
{
  "quiz_settings": {
    "allow_backtracking": false   // Prevent going back to previous questions
  }
}
```

**Use for high-stakes exams** to prevent students from changing answers after seeing later questions.

## Workflow Example: Creating a Midterm Exam

### Step 1: Create Your Question Banks

Create 3 banks with 5 questions each:
- Bank A: Numeric calculations (5 questions)
- Bank B: Multiple choice concepts (5 questions)
- Bank C: True/False facts (5 questions)

### Step 2: Configure Quiz to Pick from Banks

- Pick 3 from Bank A
- Pick 2 from Bank B
- Pick 2 from Bank C

**Total:** 7 questions per student, but with 5×5×5 = 125 possible combinations!

### Step 3: Test the Quiz

1. Set `"publish": false`
2. Run the script
3. Preview the quiz in Canvas
4. Take the quiz as a test student
5. Verify randomization is working

### Step 4: Publish

Change `"publish": true` and run the script again.

## Troubleshooting

### Error: "Unknown item bank"

**Cause:** The `bank_name` in `quiz_structure` doesn't match any bank in `item_banks`.

**Solution:** Check spelling and capitalization of bank names.

### Error: "Must have answers"

**Cause:** Multiple choice question is missing the `answers` array.

**Solution:** Add at least 2 answers to each multiple choice question.

### Questions Aren't Randomizing

**Cause:** Using `"questions"` array instead of `item_banks`.

**Solution:** Move questions into `item_banks` and use `quiz_structure` with item bank groups.

### All Students Getting Same Questions

**Cause:** Using direct questions instead of item bank groups.

**Solution:** Use `"type": "item_bank_group"` in `quiz_structure`.

## Backward Compatibility

The system is **fully backward compatible** with the original format:

```json
{
  "quiz": { ... },
  "questions": [ ... ]
}
```

If you don't use `item_banks` or `quiz_structure`, all questions are added directly to the quiz (everyone sees the same questions).

## Security Best Practices

### For High-Stakes Exams

1. **Enable shuffle:** `"shuffle_questions": true` and `"shuffle_answers": true`
2. **Disable backtracking:** `"allow_backtracking": false`
3. **Set time limit:** `"has_time_limit": true`
4. **Use large item banks:** Create 2-3× more questions than you select
5. **Review student IPs:** Check for multiple students from same location

### For Practice Quizzes

1. **Allow backtracking:** `"allow_backtracking": true`
2. **No time limit:** `"has_time_limit": false`
3. **Allow multiple attempts:** Configure in Canvas quiz settings after creation

## Support and Further Reading

- **Canvas New Quizzes API:** [Canvas LMS REST API Documentation](https://canvas.instructure.com/doc/api/)
- **Item Banks Guide:** [Canvas Item Banks Documentation](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-use-Item-Banks-in-New-Quizzes/ta-p/587)

## License

This code is provided as-is for educational purposes.

---

## Quick Reference

| Feature | JSON Key | Description |
|---------|----------|-------------|
| Item Bank | `item_banks` | Create question pools |
| Bank Group | `quiz_structure` → `item_bank_group` | Select N questions from bank |
| Direct Question | `questions` OR `quiz_structure` → `direct_question` | Everyone sees this |
| Shuffle Questions | `quiz_settings` → `shuffle_questions` | Randomize order |
| Time Limit | `quiz_settings` → `time_limit` | Minutes allowed |
| Backtracking | `quiz_settings` → `allow_backtracking` | Allow going back |

---

**Version:** 1.0
**Last Updated:** November 2024
