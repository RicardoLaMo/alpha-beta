# Canvas Quiz Creator - Quick Start Guide

## What's New?

This enhanced version supports **Item Banks** - allowing each student to receive **different questions** from question pools at midterm or any exam!

## Key Benefits

✅ **Reduce Cheating** - Each student gets a unique set of questions
✅ **Fair Assessment** - All questions from the same difficulty pool
✅ **Reusable Content** - Build question banks you can use across multiple quizzes
✅ **Flexible** - Mix direct questions (everyone sees) with randomized questions

## Quick Start

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Set Your Canvas API Key

```bash
export CANVAS_API_KEY="your_api_token_here"
```

### 3. Choose an Example

We provide three ready-to-use examples:

#### Option A: Original Format (No Randomization)
All students see the same questions.

```bash
export QUIZ_JSON_PATH="example_original_format.json"
python canvas_quiz_with_item_banks.py
```

#### Option B: Midterm with Item Banks (Recommended)
Each student gets different questions from pools.

```bash
export QUIZ_JSON_PATH="example_midterm_with_item_banks.json"
python canvas_quiz_with_item_banks.py
```

This example creates:
- 5 numeric questions (students get 3 random ones)
- 3 multiple choice questions (students get 2 random ones)
- 3 true/false questions (students get 2 random ones)

**Total:** Each student answers 7 questions, but from a pool of 11!

#### Option C: Mixed Quiz
Some questions everyone sees, some are randomized.

```bash
export QUIZ_JSON_PATH="example_mixed_quiz.json"
python canvas_quiz_with_item_banks.py
```

## How Item Banks Work

### Traditional Quiz (Old Way)
```
Question 1 → All students see this
Question 2 → All students see this
Question 3 → All students see this
```

**Problem:** Students can share answers easily.

### Item Bank Quiz (New Way)
```
Item Bank A: [Q1, Q2, Q3, Q4, Q5] → Pick 3

Student A gets: Q1, Q3, Q5
Student B gets: Q2, Q4, Q5
Student C gets: Q1, Q2, Q4
```

**Solution:** Each student has a different exam!

## Creating Your First Item Bank Quiz

### Step 1: Create a JSON File

```json
{
  "quiz": {
    "title": "My Midterm Exam",
    "instructions": "<p>Complete all questions.</p>",
    "publish": false,
    "quiz_settings": {
      "shuffle_questions": true,
      "has_time_limit": true,
      "time_limit": 60
    }
  },
  "item_banks": [
    {
      "name": "My Question Pool",
      "description": "Pool of similar difficulty questions",
      "questions": [
        {
          "type": "numeric",
          "title": "Question 1",
          "body": "<p>What is 2 + 2?</p>",
          "correct_value": "4",
          "margin": "0.1",
          "margin_type": "absolute",
          "points": 2
        },
        {
          "type": "numeric",
          "title": "Question 2",
          "body": "<p>What is 3 + 3?</p>",
          "correct_value": "6",
          "margin": "0.1",
          "margin_type": "absolute",
          "points": 2
        }
      ]
    }
  ],
  "quiz_structure": [
    {
      "type": "item_bank_group",
      "bank_name": "My Question Pool",
      "pick_count": 1,
      "points_per_item": 2
    }
  ]
}
```

### Step 2: Run the Script

```bash
export QUIZ_JSON_PATH="my_quiz.json"
python canvas_quiz_with_item_banks.py
```

### Step 3: Review in Canvas

The script outputs a link to review your quiz in Canvas.

## Supported Question Types

| Type | JSON `type` | Description |
|------|-------------|-------------|
| Numeric | `numeric` | Number with margin of error |
| Multiple Choice | `multiple_choice` | Choose one or more answers |
| True/False | `true_false` | Boolean question |
| Essay | `essay` | Free text response |

## File Structure

```
canvas_quiz_with_item_banks.py          # Main script
CANVAS_QUIZ_DOCUMENTATION.md            # Full documentation
example_original_format.json            # Legacy format example
example_midterm_with_item_banks.json    # Item banks example
example_mixed_quiz.json                 # Mixed format example
```

## Common Questions

### Q: Will students know they have different questions?
**A:** They will see different questions but won't know which other students have which questions. All questions should be similar difficulty.

### Q: Can I reuse the same item bank in multiple quizzes?
**A:** Yes! Once created, item banks can be used across multiple quizzes in the same course.

### Q: How many questions should I put in an item bank?
**A:** Recommendation: Create 2-3× more questions than you'll select. If picking 3, create 6-9 questions.

### Q: Can I mix randomized and non-randomized questions?
**A:** Yes! Use `quiz_structure` to define some direct questions and some item bank groups. See `example_mixed_quiz.json`.

### Q: Is this backward compatible with my old quizzes?
**A:** Yes! The old format still works. Just use the `questions` array without `item_banks`.

## Tips for Midterm Exams

1. **Create large item banks** - More questions = better randomization
2. **Enable shuffle** - Randomize both question and answer order
3. **Set a time limit** - Prevent extended collaboration
4. **Test first** - Set `"publish": false` and preview the quiz
5. **Keep questions equivalent** - All questions in a bank should be similar difficulty

## Need Help?

📖 **Full Documentation:** See `CANVAS_QUIZ_DOCUMENTATION.md`
🔧 **Modify the Script:** Edit `canvas_quiz_with_item_banks.py`
📝 **Example Configs:** Check the `example_*.json` files

## Next Steps

1. ✅ Review the examples
2. ✅ Read the full documentation
3. ✅ Create your own JSON configuration
4. ✅ Test with `"publish": false`
5. ✅ Publish when ready!

---

**Happy Quiz Creating!** 🎓
