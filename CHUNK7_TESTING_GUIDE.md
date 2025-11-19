# Quick Testing Guide - Chunk 7 CRUD Features

## Starting the Application

```bash
cd "C:\Users\10295495\OneDrive - Utah Valley University\Cursor\Student_QA_Chatbot"
venv\Scripts\activate
python web_app_sql.py
```

Then open your browser to: **http://localhost:5000**

## Testing Checklist

### ✅ Step 1: Login to Admin Panel
1. Navigate to http://localhost:5000/admin/login
2. Login with:
   - Email: `admin@uvu.edu`
   - Password: `admin123`
3. You should see the admin dashboard

### ✅ Step 2: Test User Edit Functionality
1. Go to "Users" from the top navigation
2. Click the ✏️ icon next to any user (or open a user and click "Edit User")
3. Try changing:
   - First or last name
   - Email address
   - Student ID
   - Course section
4. Click "Save Changes"
5. Verify the changes appear on the user detail page
6. Try checking/unchecking the "Active Account" checkbox
7. Optionally test password reset (leave blank to skip)

### ✅ Step 3: Test Conversation Edit Functionality
1. Go to "Conversations" from the top navigation
2. Click the ✏️ icon on any conversation
3. Try modifying:
   - The question text
   - The answer text
   - Guest user information (if it's a guest conversation)
4. Click "Save Changes"
5. Verify changes appear in the conversation list

### ✅ Step 4: Test Delete User
1. Go to "Users"
2. Open a test user's profile
3. Click "🗑️ Delete User" button
4. You should see a confirmation dialog
5. Confirm the deletion
6. Verify:
   - User is removed from the users list
   - User's conversations are also deleted (cascade)
   - Flash message confirms deletion

**Note:** Only delete test accounts, not real student data!

### ✅ Step 5: Test Delete Conversation
1. Go to "Conversations"
2. Click the 🗑️ icon on any conversation
3. Confirm the deletion in the dialog
4. Verify:
   - Conversation is removed from the list
   - Flash message confirms deletion

### ✅ Step 6: Test Merge Accounts
1. First, create two test users:
   - Register at http://localhost:5000/register
   - Create User 1: john.doe@test.com
   - Create User 2: john.doe2@test.com
   - Have each ask at least one question
2. Login to admin panel
3. Go to "Users" → Click "🔀 Merge Accounts"
4. Select User 2 as "Source User" (will be deleted)
5. Select User 1 as "Target User" (will keep)
6. Review the preview boxes
7. Click "Merge Accounts"
8. Confirm the merge
9. Verify:
   - User 2 is deleted
   - User 1 has all conversations from both accounts
   - Flash message shows how many conversations were transferred

### ✅ Step 7: Test Validation & Edge Cases

**Test Invalid Merge:**
1. Try selecting the same user for both source and target
2. Should prevent merge with error message

**Test Empty Edit:**
1. Try submitting edit form with required fields empty
2. Should show validation error

**Test Password Length:**
1. Edit a user
2. Try setting password shorter than 6 characters
3. Should show error

**Test Non-existent Records:**
1. Try accessing `/admin/users/9999/edit` (non-existent ID)
2. Should show 404 error

## Expected Results

All operations should:
- Show confirmation dialogs for destructive actions
- Display flash messages after completion
- Redirect to appropriate pages
- Handle errors gracefully
- Work without JavaScript errors in browser console

## Common Issues & Solutions

### Issue: "Admin login required" after clicking buttons
**Solution:** Session expired, login again

### Issue: Changes don't save
**Solution:** Check browser console for errors, verify form is submitting

### Issue: Delete button doesn't show confirmation
**Solution:** Ensure JavaScript is enabled in browser

### Issue: Merge shows wrong conversation count
**Solution:** Refresh the page, counts are calculated in real-time

## Quick Commands

### View all users (Python shell):
```python
from web_app_sql import app, db, User
with app.app_context():
    users = User.query.all()
    for u in users:
        print(f"{u.email} - Conversations: {u.conversations.count()}")
```

### View all conversations (Python shell):
```python
from web_app_sql import app, db, Conversation
with app.app_context():
    convs = Conversation.query.all()
    print(f"Total conversations: {len(convs)}")
```

### Create test admin (if needed):
```bash
python migrate_to_sql.py
# Choose option 2
```

## Testing Complete? ✅

If all tests pass:
- ✅ Edit user works
- ✅ Edit conversation works
- ✅ Delete user works (with cascade)
- ✅ Delete conversation works
- ✅ Merge accounts works
- ✅ Validations prevent errors
- ✅ Confirmations show before destructive actions
- ✅ Flash messages provide feedback

**Your CRUD implementation is complete and working!**

## Next Steps

After testing, you can:
1. Create a backup: Admin Panel → Dashboard → "Create Backup"
2. Export data: Use "Export Users" or "Export Conversations"
3. Document any issues found
4. Use the system with real student data

---

**Remember:** Always backup data before performing bulk operations or testing destructive actions!
