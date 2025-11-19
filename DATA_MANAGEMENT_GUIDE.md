# Data Management Guide

## Overview
This guide explains how to access and manage student conversation data collected through the Q&A Chatbot.

## User Data Collection Flow

1. **Student visits the website** → First sees the user information form
2. **Student submits their info** → Data includes:
   - First Name
   - Last Name
   - Student ID
   - Email Address
   - Course Section (optional)
   - Semester (optional)
3. **Student starts chatting** → All conversations tagged with their information
4. **Data is saved** → Each Q&A automatically saved to `qa_conversations.json`

## Data Structure

Each conversation entry contains:
```json
{
  "id": 1,
  "question": "Student's question",
  "answer": "AI's response",
  "timestamp": "2025-11-13T22:30:00.000000",
  "saved_at": "2025-11-13T22:30:00.000000",
  "session_id": "unique-session-identifier",
  "user_info": {
    "firstName": "John",
    "lastName": "Doe",
    "studentId": "12345678",
    "email": "john.doe@example.com",
    "courseSection": "Section 001",
    "semester": "Fall 2025",
    "submission_timestamp": "2025-11-13T22:00:00.000000"
  }
}
```

## Accessing the Data

### Method 1: Using the Data Extraction Tool (Recommended)

Run the interactive tool:
```bash
python extract_data.py
```

**Options Available:**

1. **View Summary Statistics**
   - Total conversations
   - Number of unique students
   - Anonymous conversations (without user info)

2. **View Conversations by Student**
   - Grouped by student ID
   - Shows student details
   - Lists all their questions

3. **Search by Student ID**
   - Enter a specific student ID
   - View all their conversations
   - See timestamps and questions/answers

4. **Export to CSV**
   - Creates a spreadsheet-friendly file
   - One row per conversation
   - Includes all user data and Q&A content
   - Default filename: `conversations_export.csv`

5. **Export to JSON**
   - Formatted JSON with metadata
   - Includes export timestamp
   - Total conversation count
   - Default filename: `conversations_formatted.json`

### Method 2: Direct API Access

While the web app is running, access:

**Export all data:**
```
GET http://localhost:5000/export_data
```

Returns JSON with:
- Total conversation count
- All conversation data
- Export timestamp

**Example using curl:**
```bash
curl http://localhost:5000/export_data > data_export.json
```

### Method 3: Direct File Access

The raw data is stored in:
```
qa_conversations.json
```

You can open this file directly with:
- Any text editor (VS Code, Notepad++, etc.)
- Python scripts
- JSON viewers
- Excel (import as JSON)

## Common Use Cases

### Finding a specific student's conversations
```bash
python extract_data.py
# Choose option 3
# Enter the student ID
```

### Exporting data for analysis in Excel
```bash
python extract_data.py
# Choose option 4
# Enter filename or press Enter for default
# Open the CSV file in Excel
```

### Getting a snapshot of all data
```bash
python extract_data.py
# Choose option 1 for summary
# Choose option 2 to browse by student
```

### Creating a backup
```bash
python extract_data.py
# Choose option 5
# Enter a filename like "backup_2025_11_13.json"
```

## Data Privacy & Security

**Important Notes:**
- User data is stored locally in `qa_conversations.json`
- Sessions use secure Flask session management
- Session IDs are unique UUID values
- No data is sent to external services (except Mistral AI for responses)

**Best Practices:**
- Regularly backup `qa_conversations.json`
- Keep the `.env` file secure (contains SECRET_KEY)
- Don't commit `qa_conversations.json` to version control (already in .gitignore)
- Export data periodically for analysis

## Analyzing Student Engagement

You can use the exported data to:
- Track which students are using the chatbot
- Identify common questions
- Measure engagement by course section
- Track usage patterns over time
- Identify topics that need more clarification

## Troubleshooting

**Problem:** No data when running extract_data.py
- **Solution:** Make sure students have used the web interface and `qa_conversations.json` exists

**Problem:** Missing user info in conversations
- **Solution:** These are from before Chunk 4 implementation or if students bypassed the form

**Problem:** Can't export to CSV
- **Solution:** Make sure you have write permissions in the directory

**Problem:** Session expires and asks for info again
- **Solution:** Sessions timeout after inactivity. Increase session timeout in `web_app.py` if needed

## Example Workflow

1. **End of Week Review:**
   ```bash
   python extract_data.py
   # View summary statistics
   # Export to CSV for detailed analysis
   ```

2. **Student Support:**
   ```bash
   python extract_data.py
   # Search by student ID
   # Review their conversation history
   # Identify areas where they need help
   ```

3. **Course Improvement:**
   ```bash
   python extract_data.py
   # Export all data
   # Analyze common questions
   # Update course materials accordingly
   ```

## Future Enhancements

Planned features for future chunks:
- Admin dashboard for visualizing data
- Advanced filtering and search
- Usage analytics and charts
- Email notifications for instructors
- Integration with LMS platforms
