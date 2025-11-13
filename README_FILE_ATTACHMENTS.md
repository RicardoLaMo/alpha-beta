# Canvas Quiz with File Attachments - Quick Start

## 🎯 What's New?

Now you can **attach Excel files (or any files) to Canvas quizzes**! Students can:
1. Download data files (Excel, PDF, etc.)
2. Work on the data/analyze it
3. Submit answers to quiz questions based on their work

Perfect for:
- **Excel assignments** with real data
- **Data analysis** midterms/finals
- **Statistics** practice quizzes
- Any course requiring file-based work

## 🚀 Quick Start (5 Minutes)

### Step 1: Create Sample Excel Files

```bash
python create_sample_excel.py
```

This creates 3 sample Excel files:
- `temperature_data.xlsx` - 30 days of temperature data
- `sales_data.xlsx` - Product sales data
- `statistics_data.xlsx` - Test scores data

### Step 2: Set Your API Key

```bash
export CANVAS_API_KEY="your_canvas_token"
```

### Step 3: Run Example Quiz

```bash
# Simple Excel quiz (all students see same questions)
export QUIZ_JSON_PATH="example_quiz_with_excel_file.json"
python canvas_quiz_with_attachments.py
```

**OR**

```bash
# Midterm with randomized questions + multiple Excel files
export QUIZ_JSON_PATH="example_midterm_with_excel_banks.json"
python canvas_quiz_with_attachments.py
```

### Step 4: Preview in Canvas

The script outputs a URL. Open it in Canvas to see your quiz!

## 📁 File Structure

```
canvas_quiz_with_attachments.py          # Main script (with file upload)
canvas_quiz_with_item_banks.py           # Original script (no files)

create_sample_excel.py                   # Generate sample Excel files
temperature_data.xlsx                    # Sample data (generated)
sales_data.xlsx                         # Sample data (generated)
statistics_data.xlsx                    # Sample data (generated)

example_quiz_with_excel_file.json       # Simple Excel quiz
example_midterm_with_excel_banks.json   # Randomized + multiple files

FILE_ATTACHMENTS_GUIDE.md               # Comprehensive file attachment guide
CANVAS_QUIZ_DOCUMENTATION.md            # Full quiz documentation
README_CANVAS_QUIZ.md                   # Original quick start
```

## 📊 Example 1: Simple Excel Quiz

**File:** `example_quiz_with_excel_file.json`

All students:
- Download `temperature_data.xlsx`
- Complete temperature conversions (F → C → K)
- Answer 5 questions (3 numeric, 1 MC, 1 essay)

**JSON Configuration:**
```json
{
  "quiz": {
    "title": "Temperature Data Analysis",
    "attached_files": ["temp_data"]
  },
  "files": {
    "temp_data": "temperature_data.xlsx"
  },
  "questions": [
    {
      "type": "numeric",
      "title": "Average Temperature",
      "body": "<p>Calculate the average temperature in Celsius...</p>",
      "correct_value": "25.3",
      "margin": "0.5",
      "points": 5
    }
  ]
}
```

## 🎓 Example 2: Midterm with Randomization

**File:** `example_midterm_with_excel_banks.json`

Each student:
- Downloads 3 Excel files (temp, sales, stats)
- Gets 2 random questions from each file's question bank (6 total)
- Answers 1 common essay question

**Benefits:**
- 4³ = 64 possible question combinations
- Reduces cheating
- Fair assessment (all questions from same difficulty pools)

**Configuration:**
```json
{
  "files": {
    "temp_data": "temperature_data.xlsx",
    "sales_data": "sales_data.xlsx",
    "stats_data": "statistics_data.xlsx"
  },
  "item_banks": [
    {
      "name": "Temperature Analysis Questions",
      "questions": [ /* 4 questions */ ]
    },
    {
      "name": "Sales Analysis Questions",
      "questions": [ /* 3 questions */ ]
    },
    {
      "name": "Statistics Analysis Questions",
      "questions": [ /* 3 questions */ ]
    }
  ],
  "quiz_structure": [
    {"type": "item_bank_group", "bank_name": "Temperature Analysis Questions", "pick_count": 2},
    {"type": "item_bank_group", "bank_name": "Sales Analysis Questions", "pick_count": 2},
    {"type": "item_bank_group", "bank_name": "Statistics Analysis Questions", "pick_count": 2}
  ]
}
```

## 💡 How It Works

### 1. Define Files
```json
{
  "files": {
    "my_data": "path/to/myfile.xlsx"
  }
}
```

### 2. Attach to Quiz Instructions
```json
{
  "quiz": {
    "attached_files": ["my_data"]  // Shows download button in instructions
  }
}
```

### 3. Or Attach to Specific Questions
```json
{
  "questions": [{
    "attached_file": "my_data",  // Shows download button above question
    "body": "<p>Analyze the data...</p>"
  }]
}
```

### 4. Script Handles Everything
- ✅ Uploads file to Canvas
- ✅ Creates download buttons
- ✅ Embeds in quiz/questions
- ✅ Students can download and work

## 🎯 Comparison: With vs Without Files

### Before (No Files):
```json
{
  "questions": [{
    "body": "<p>Calculate the average of: 23, 45, 67, 89...</p>"
  }]
}
```
**Limitation:** Data must be in question text (messy for large datasets)

### After (With Files):
```json
{
  "files": {"data": "mydata.xlsx"},
  "questions": [{
    "attached_file": "data",
    "body": "<p>Calculate the average from column A</p>"
  }]
}
```
**Benefits:**
- ✅ Clean question text
- ✅ Real datasets (100s of rows)
- ✅ Students use Excel skills
- ✅ More realistic assessment

## 🔧 Common Workflows

### Workflow 1: Excel Assignment
1. Create Excel file with data
2. Students download and complete calculations
3. Answer numeric questions with their results

**Use:** `example_quiz_with_excel_file.json`

### Workflow 2: Randomized Midterm
1. Create multiple Excel files
2. Create question banks for each file
3. Each student gets random selection

**Use:** `example_midterm_with_excel_banks.json`

### Workflow 3: Mixed Assessment
1. Some questions use shared Excel file
2. Some questions don't need files
3. Combine direct questions + item banks

**Create your own JSON** based on examples

## ✅ Features Comparison

| Feature | `canvas_quiz_with_item_banks.py` | `canvas_quiz_with_attachments.py` |
|---------|----------------------------------|-----------------------------------|
| Item Banks (Randomization) | ✅ | ✅ |
| Multiple Question Types | ✅ | ✅ |
| Shuffle Questions/Answers | ✅ | ✅ |
| **File Attachments** | ❌ | ✅ |
| **Excel/PDF Support** | ❌ | ✅ |
| **Upload to Canvas** | ❌ | ✅ |

**Recommendation:** Use `canvas_quiz_with_attachments.py` for everything. It has all features from the original plus file support.

## 📚 Documentation

| File | Description |
|------|-------------|
| **FILE_ATTACHMENTS_GUIDE.md** | Complete guide to file attachments |
| **CANVAS_QUIZ_DOCUMENTATION.md** | Full quiz system documentation |
| **README_CANVAS_QUIZ.md** | Original quick start (no files) |

## 🎓 Teaching Tips

### For Excel Courses:
- Use `temperature_data.xlsx` for formula practice
- Students practice: AVERAGE, MAX, MIN, STDEV, IF, VLOOKUP
- Questions test both Excel skills and understanding

### For Data Analysis:
- Use `sales_data.xlsx` for pivot tables
- `statistics_data.xlsx` for statistical analysis
- Combine with essay questions for interpretation

### For Midterm/Final Exams:
- Create large item banks (10+ questions per topic)
- Select 2-3 questions per bank
- Attach relevant data files
- Enable shuffle + time limit
- Each student gets unique exam

### For Practice Quizzes:
- Allow multiple attempts
- No time limit
- Provide immediate feedback
- Attach formula reference sheets

## 🐛 Troubleshooting

**Problem:** File upload fails
```bash
# Check file exists
ls -l temperature_data.xlsx

# Use absolute path if needed
{
  "files": {
    "my_data": "/full/path/to/file.xlsx"
  }
}
```

**Problem:** File doesn't show in quiz
```json
// Add to quiz instructions:
{
  "quiz": {
    "attached_files": ["my_data"]  // ← Add this
  }
}

// OR add to individual question:
{
  "questions": [{
    "attached_file": "my_data"  // ← Add this
  }]
}
```

**Problem:** Answers marked wrong
```json
// Increase margin:
{
  "correct_value": "25.5",
  "margin": "1.0",  // ← Increase this
  "margin_type": "absolute"
}
```

## 🚀 Next Steps

1. **Try the examples:**
   ```bash
   python create_sample_excel.py
   export QUIZ_JSON_PATH="example_quiz_with_excel_file.json"
   python canvas_quiz_with_attachments.py
   ```

2. **Create your own:**
   - Modify example JSON files
   - Add your own Excel files
   - Customize questions

3. **Read full docs:**
   - `FILE_ATTACHMENTS_GUIDE.md` - File attachment details
   - `CANVAS_QUIZ_DOCUMENTATION.md` - Complete quiz reference

4. **Deploy for real:**
   - Set `"publish": false"` first
   - Test thoroughly
   - Set `"publish": true"` when ready

## 📝 Quick Reference

### Create Quiz with Excel File
```json
{
  "quiz": {
    "title": "My Quiz",
    "attached_files": ["data"]
  },
  "files": {
    "data": "myfile.xlsx"
  },
  "questions": [ /* ... */ ]
}
```

### Run Script
```bash
export CANVAS_API_KEY="token"
export QUIZ_JSON_PATH="myquiz.json"
python canvas_quiz_with_attachments.py
```

### Generate Sample Data
```bash
python create_sample_excel.py
```

---

**Ready to create file-based quizzes!** 📊🎓

For questions or issues, see the full documentation files.
