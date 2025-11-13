# Canvas Quiz File Attachments Guide

## Overview

This guide explains how to attach files (Excel, PDF, images, etc.) to Canvas New Quizzes, allowing students to download data files, work with them, and submit their answers.

## 🎯 Use Cases

### Perfect for:
- **Excel assignments** - Students download data, perform calculations, answer questions
- **Data analysis** - Provide datasets for statistical analysis
- **Document review** - Attach PDFs, images, or other materials for questions
- **Coding exercises** - Provide starter code files or data
- **Case studies** - Attach background materials

### Example Workflow:
1. **Instructor** creates quiz with Excel file attachment
2. **Student** downloads the Excel file
3. **Student** performs calculations/analysis in Excel
4. **Student** answers quiz questions based on their work
5. **(Optional)** Student uploads completed Excel file separately

## 📁 Supported File Types

- **Excel**: `.xlsx`, `.xls`
- **CSV**: `.csv`
- **PDF**: `.pdf`
- **Word**: `.docx`, `.doc`
- **Images**: `.png`, `.jpg`, `.gif`
- **Text**: `.txt`
- **Code**: `.py`, `.java`, `.cpp`, etc.
- **Any other file type** Canvas supports

## 🚀 Quick Start

### Step 1: Create Your Data Files

```bash
# Generate sample Excel files
python create_sample_excel.py
```

This creates:
- `temperature_data.xlsx` - Temperature conversion data
- `sales_data.xlsx` - Sales analysis data
- `statistics_data.xlsx` - Statistical analysis data

### Step 2: Create Quiz JSON with File Attachments

```json
{
  "quiz": {
    "title": "Excel Data Analysis Quiz",
    "instructions": "<p>Download the file and complete the analysis.</p>",
    "attached_files": ["my_data"],
    "publish": false
  },
  "files": {
    "my_data": "temperature_data.xlsx"
  },
  "questions": [
    {
      "type": "numeric",
      "title": "Calculate Average",
      "body": "<p>What is the average temperature?</p>",
      "correct_value": "25.5",
      "margin": "0.5",
      "margin_type": "absolute",
      "points": 5
    }
  ]
}
```

### Step 3: Run the Script

```bash
export CANVAS_API_KEY="your_token"
export QUIZ_JSON_PATH="example_quiz_with_excel_file.json"
python canvas_quiz_with_attachments.py
```

## 📋 Configuration Reference

### Files Section

Define files to upload:

```json
{
  "files": {
    "file_key1": "path/to/file1.xlsx",
    "file_key2": "path/to/file2.pdf",
    "file_key3": "data/dataset.csv"
  }
}
```

**Notes:**
- `file_key` - Unique identifier (you reference this in questions)
- `path` - Relative or absolute path to the file

### Attach Files to Quiz Instructions

All students will see these files in the quiz instructions:

```json
{
  "quiz": {
    "title": "My Quiz",
    "instructions": "<p>Instructions here...</p>",
    "attached_files": ["file_key1", "file_key2"]
  }
}
```

This adds download buttons to the quiz instructions.

### Attach Files to Individual Questions

Attach specific files to specific questions:

```json
{
  "questions": [
    {
      "type": "numeric",
      "title": "Question 1",
      "body": "<p>Analyze the data...</p>",
      "attached_file": "file_key1",
      "correct_value": "42",
      "points": 5
    }
  ]
}
```

The download button appears above the question text.

### Use with Item Banks

Attach files to questions in item banks:

```json
{
  "item_banks": [
    {
      "name": "Analysis Questions",
      "questions": [
        {
          "type": "numeric",
          "title": "Calculate Mean",
          "body": "<p>Find the mean...</p>",
          "attached_file": "file_key1",
          "correct_value": "25",
          "points": 5
        }
      ]
    }
  ]
}
```

## 📊 Complete Examples

### Example 1: Simple Excel Quiz

All students download the same file and answer the same questions.

**File:** `example_quiz_with_excel_file.json`

**Features:**
- Single Excel file attached to quiz instructions
- 5 questions requiring Excel analysis
- Mix of numeric, multiple choice, and essay questions

**Use this when:**
- You want a straightforward Excel assignment
- All students work with the same data
- No randomization needed

### Example 2: Midterm with Multiple Files and Item Banks

Students get randomized questions from pools, all referencing data files.

**File:** `example_midterm_with_excel_banks.json`

**Features:**
- 3 Excel files (temperature, sales, statistics data)
- 3 item banks with questions for each file
- Students get 2 random questions from each bank
- 1 common essay question for all students

**Use this when:**
- You want to reduce cheating with randomization
- Multiple datasets to analyze
- High-stakes exam (midterm/final)

## 🎓 Best Practices

### 1. Clear File References

Always mention the file name in the question:

```json
{
  "body": "<p>Using the <strong>temperature_data.xlsx</strong> file, calculate...</p>"
}
```

### 2. Include Instructions in Files

Add an "Instructions" sheet in Excel files:

```python
instructions = pd.DataFrame({
    'Instructions': [
        '1. Download this file',
        '2. Complete the calculations',
        '3. Answer the quiz questions',
        '4. Formula: C = (F - 32) × 5/9'
    ]
})
instructions.to_excel(writer, sheet_name='Instructions', index=False)
```

### 3. Use Appropriate Margins

For calculated values, allow reasonable margins:

```json
{
  "correct_value": "25.5",
  "margin": "0.5",        // ±0.5
  "margin_type": "absolute"
}
```

**For percentage margins:**
```json
{
  "correct_value": "100",
  "margin": "5",          // ±5%
  "margin_type": "percentage"
}
```

### 4. Enable Calculator Type

```json
{
  "calculator_type": "basic"       // or "scientific"
}
```

Options:
- `"none"` - No calculator
- `"basic"` - Basic arithmetic
- `"scientific"` - Advanced functions

### 5. Test First!

Always set `"publish": false` and test:

1. Create the quiz
2. Preview in Canvas
3. Download the files as a student would
4. Verify calculations
5. Check that margins are appropriate
6. Then set `"publish": true`

## 🔧 Advanced Techniques

### Multiple Files per Question

You can attach files at multiple levels:

```json
{
  "quiz": {
    "attached_files": ["reference_sheet"]  // Available quiz-wide
  },
  "questions": [
    {
      "attached_file": "dataset1",         // Specific to this question
      "body": "<p>Use dataset1.xlsx...</p>"
    }
  ]
}
```

### File Organization

Organize files in the JSON:

```json
{
  "files": {
    // Temperature files
    "temp_jan": "data/temperature_january.xlsx",
    "temp_feb": "data/temperature_february.xlsx",

    // Sales files
    "sales_q1": "data/sales_q1.xlsx",
    "sales_q2": "data/sales_q2.xlsx",

    // Reference materials
    "formula_sheet": "references/formulas.pdf"
  }
}
```

### Conditional File Attachments

Attach different files to different question banks:

```json
{
  "item_banks": [
    {
      "name": "Temperature Questions",
      "questions": [
        {
          "attached_file": "temp_data",
          "body": "<p>Analyze temperature_data.xlsx...</p>"
        }
      ]
    },
    {
      "name": "Sales Questions",
      "questions": [
        {
          "attached_file": "sales_data",
          "body": "<p>Analyze sales_data.xlsx...</p>"
        }
      ]
    }
  ]
}
```

Each bank's questions reference their specific file.

## 🎯 Real-World Example: Midterm Exam

### Scenario:
You're teaching a data analysis course. For the midterm:
- 60 students
- Need to reduce cheating
- Students analyze real datasets
- Time limit: 60 minutes

### Solution:

**Step 1: Create 3 datasets**
```bash
python create_sample_excel.py
# Creates: temperature_data.xlsx, sales_data.xlsx, statistics_data.xlsx
```

**Step 2: Create question banks**
- 4 questions per dataset (12 total)
- Students get 2 questions from each dataset (6 total)
- 1 common essay question

**Step 3: Configuration**
```json
{
  "quiz": {
    "attached_files": ["temp_data", "sales_data", "stats_data"],
    "quiz_settings": {
      "shuffle_questions": true,
      "has_time_limit": true,
      "time_limit": 60
    }
  },
  "files": {
    "temp_data": "temperature_data.xlsx",
    "sales_data": "sales_data.xlsx",
    "stats_data": "statistics_data.xlsx"
  },
  "item_banks": [
    // 3 banks with 4 questions each
  ],
  "quiz_structure": [
    {"type": "item_bank_group", "bank_name": "Temperature", "pick_count": 2},
    {"type": "item_bank_group", "bank_name": "Sales", "pick_count": 2},
    {"type": "item_bank_group", "bank_name": "Statistics", "pick_count": 2},
    {"type": "direct_question", "question": { /* essay */ }}
  ]
}
```

**Result:**
- Each student: 6 randomized questions + 1 essay
- With 4³ = 64 possible combinations, very low chance of identical exams
- All students work with same data files but different questions

## 📈 Grading Considerations

### Auto-Graded Questions (Numeric, MC, T/F)
Canvas grades these automatically using your specified correct values and margins.

### Essay Questions
You may want to ask students to:
1. Upload their completed Excel file separately (Canvas assignment)
2. Show work in essay response
3. Include key formulas used

**Example essay question:**
```json
{
  "type": "essay",
  "title": "Show Your Work",
  "body": "<p>Paste your Excel formulas and explain your calculation process.</p>",
  "points": 10
}
```

## 🐛 Troubleshooting

### Problem: File upload fails

**Error:** `File not found`

**Solution:** Check the file path is correct:
```json
{
  "files": {
    "my_data": "temperature_data.xlsx"  // Must exist in current directory
  }
}
```

Use absolute paths if needed:
```json
{
  "files": {
    "my_data": "/home/user/data/temperature_data.xlsx"
  }
}
```

### Problem: File doesn't appear in quiz

**Issue:** Forgot to reference the file

**Solution:** Add to `attached_files`:
```json
{
  "quiz": {
    "attached_files": ["my_data"]  // Add this!
  }
}
```

Or add to individual question:
```json
{
  "questions": [{
    "attached_file": "my_data"     // Add this!
  }]
}
```

### Problem: Students can't download file

**Issue:** File permissions or course access

**Solution:**
1. Check file uploaded successfully (script shows confirmation)
2. Verify course ID is correct
3. Ensure students are enrolled in the course
4. Check file isn't marked as "hidden" in Canvas

### Problem: Margins too strict/loose

**Issue:** All students getting wrong answer

**Solution:** Adjust margin:
```json
{
  "correct_value": "25.5",
  "margin": "1.0",           // Increase from 0.5 to 1.0
  "margin_type": "absolute"
}
```

Or use percentage:
```json
{
  "margin": "5",             // ±5%
  "margin_type": "percentage"
}
```

## 📚 Additional Resources

### Creating Excel Files Programmatically

See `create_sample_excel.py` for examples of:
- Creating DataFrames with pandas
- Adding multiple sheets
- Including instructions
- Formatting cells

### File Upload API

The script uses Canvas Files API:
1. Request upload URL
2. Upload file to provided URL
3. Get file ID and URL
4. Embed in quiz/questions

### HTML Customization

Customize the download button appearance by editing `create_file_download_html()` in the script:

```python
html = f'''<div style="padding: 10px; background-color: #f0f0f0;">
    <a href="/courses/{COURSE_ID}/files/{file_id}/download" class="btn btn-primary">
        📎 Download {file_name}
    </a>
</div>'''
```

## ✅ Checklist for Excel Quiz Creation

- [ ] Create Excel file with data
- [ ] Add "Instructions" sheet to Excel file
- [ ] Test Excel calculations manually
- [ ] Create quiz JSON with file references
- [ ] Set appropriate answer margins
- [ ] Enable calculator if needed
- [ ] Set `"publish": false` for testing
- [ ] Run the script to create quiz
- [ ] Preview quiz in Canvas
- [ ] Download file as student would
- [ ] Verify questions display correctly
- [ ] Test answer submission
- [ ] Adjust margins if needed
- [ ] Set `"publish": true` when ready

---

**Happy Quiz Creating with File Attachments!** 📊✨
