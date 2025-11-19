# Quick Test & Demo Guide

## Testing Chunk 4 Implementation

### 1. Start the Web Application

```bash
python web_app.py
```

The server should start on http://localhost:5000

### 2. Test User Form Flow

1. **Open browser to:** http://localhost:5000
2. **You should see:** User Information Form (not the chat directly)
3. **Fill in the form:**
   - First Name: Test
   - Last Name: Student
   - Student ID: 12345678
   - Email: test@example.com
   - Course Section: Section 001
   - Semester: Fall 2025
4. **Click:** "Start Chat Session"
5. **You should be redirected to:** Chat interface

### 3. Test Chat with User Tracking

1. Ask a question (e.g., "What is a Python list?")
2. Wait for response
3. Ask another question
4. Close browser

### 4. Verify Data Storage

Open `qa_conversations.json` and verify:
- Latest conversations have `user_info` object
- Contains firstName, lastName, studentId, email, etc.
- Has a unique `session_id`
- Timestamp is present

### 5. Test Data Extraction Tool

```bash
python extract_data.py
```

**Try these options:**

**Option 1 - Summary:**
- Should show total conversations
- Should show unique students count
- Should differentiate old (without user info) vs new conversations

**Option 2 - By Student:**
- Should list "Test Student" (or whatever name you used)
- Should show their student ID and email
- Should list their questions

**Option 3 - Search:**
- Enter student ID: 12345678
- Should find and display their conversations

**Option 4 - CSV Export:**
- Accept default filename or enter custom
- Check that CSV file is created
- Open in Excel/LibreOffice to verify data

### 6. Test Session Management

1. Close browser completely
2. Reopen http://localhost:5000
3. Should see form again (session cleared)
4. Fill in with DIFFERENT student info
5. Chat again
6. Check `qa_conversations.json` - should have conversations from BOTH students

### 7. Test API Endpoint

With web app running:

```bash
# Windows PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/export_data" -OutFile "api_export.json"

# Or using curl if available
curl http://localhost:5000/export_data > api_export.json
```

Check the exported file has all data.

## Expected Results

✅ User must fill form before chatting
✅ Conversations saved with complete user metadata
✅ Each session gets unique session_id
✅ Data extraction tool shows all information
✅ CSV export works correctly
✅ Different users can use the system
✅ Old conversations (pre-Chunk 4) still accessible

## Common Issues & Solutions

**Issue:** Form keeps reappearing
- **Cause:** SECRET_KEY not set or sessions not working
- **Fix:** Check .env file has SECRET_KEY set

**Issue:** No user_info in saved conversations
- **Cause:** Accessed chat directly without going through form
- **Fix:** Always start from http://localhost:5000 (not /index)

**Issue:** extract_data.py shows no students
- **Cause:** Only old conversations exist (before Chunk 4)
- **Fix:** Submit form and chat to create new conversations with user data

**Issue:** Can't export CSV
- **Cause:** Permission error or file in use
- **Fix:** Close any open CSV files, check directory permissions

## Demo Scenario

**For presenting Chunk 4 completion:**

1. **Show the form:**
   - Navigate to http://localhost:5000
   - Explain: "Students first enter their information"
   - Fill in sample data
   - Submit

2. **Show the chat:**
   - Ask: "How do I create a list in Python?"
   - Show response
   - Explain: "This conversation is now tagged with the student's info"

3. **Show data capture:**
   - Open qa_conversations.json
   - Point out the user_info object
   - Show session_id and timestamps

4. **Show extraction tool:**
   - Run `python extract_data.py`
   - Show option 1 (summary)
   - Show option 2 (by student)
   - Export to CSV

5. **Show the CSV:**
   - Open in Excel
   - Show how data is structured
   - Explain how instructors can analyze this

## Success Criteria

All three tasks completed:

✅ **Task 1:** Created user_form.html template
- Professional looking form
- All required fields
- Good UX with validation

✅ **Task 2:** Connected form to conversation storage
- User info stored in session
- Session ID generated
- All conversations tagged with metadata

✅ **Task 3:** Backend data extraction
- extract_data.py tool created
- Multiple export formats (CSV, JSON)
- Search and filter capabilities
- Dictionary structure maintained

## Next Steps After Testing

Once testing is complete:
1. Commit changes to version control
2. Update .env with production-ready SECRET_KEY
3. Consider backing up qa_conversations.json regularly
4. Plan for future analytics dashboard (next chunk)
