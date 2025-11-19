# Chunk 7: CRUD Operations - Complete Guide

## Overview
This update adds full CRUD (Create, Read, Update, Delete) functionality to the admin panel, allowing administrators to manage users and conversations through the web interface.

## New Features

### 1. Update (Edit) Functionality

#### Edit User Information
- **Route:** `/admin/users/<user_id>/edit`
- **Access:** Admin panel → Users → Select user → "✏️ Edit User"
- **Capabilities:**
  - Modify first name, last name
  - Update email address
  - Change student ID
  - Edit course section and semester
  - Toggle account active/inactive status
  - Reset user password (optional)

#### Edit Conversations
- **Route:** `/admin/conversations/<conv_id>/edit`
- **Access:** Admin panel → Conversations → Click ✏️ icon on any conversation
- **Capabilities:**
  - Modify question text
  - Edit answer text
  - Update guest user information (for guest conversations)
  - Update name, email, student ID, section, semester for guest entries

### 2. Delete Functionality

#### Delete Users
- **Route:** `/admin/users/<user_id>/delete` (POST)
- **Access:** Admin panel → Users → Select user → "🗑️ Delete User"
- **Behavior:**
  - Permanently deletes user account
  - Automatically deletes all associated conversations (cascade delete)
  - Shows confirmation dialog before deletion
  - Cannot be undone

#### Delete Conversations
- **Route:** `/admin/conversations/<conv_id>/delete` (POST)
- **Access:** Admin panel → Conversations → Click 🗑️ icon on any conversation
- **Behavior:**
  - Permanently deletes the conversation
  - Shows confirmation dialog
  - Cannot be undone

### 3. Merge Accounts Feature

#### Merge Duplicate Users
- **Route:** `/admin/users/merge`
- **Access:** Admin panel → Users → "🔀 Merge Accounts" button
- **Purpose:** Combine duplicate accounts or correct data entry errors
- **Process:**
  1. Select **Source User** (account to be deleted)
  2. Select **Target User** (account to keep)
  3. Preview both accounts with full details
  4. Confirm merge operation
  5. All conversations transferred from source to target
  6. Source user account deleted
  7. Target user retains all data plus merged conversations

- **Safety Features:**
  - Visual preview of both accounts before merging
  - Shows conversation counts
  - Prevents merging a user with themselves
  - Double confirmation dialog
  - Clear warning about irreversible action

## User Interface Updates

### Users List Page (`/admin/users`)
- Added "🔀 Merge Accounts" button at top
- Added "Actions" column to table
- Each user row shows:
  - ✏️ (Edit) - Quick link to edit form
  - 👁️ (View) - Link to user detail page

### User Detail Page (`/admin/users/<id>`)
- Added action buttons at top:
  - "✏️ Edit User" - Opens edit form
  - "🗑️ Delete User" - Deletes user with confirmation

### Conversations List Page (`/admin/conversations`)
- Each conversation card shows:
  - ✏️ (Edit) - Opens conversation edit form
  - 🗑️ (Delete) - Deletes conversation with confirmation

## New Templates

### 1. `templates/admin/edit_user.html`
Form to edit user details with:
- All user fields (name, email, student ID, etc.)
- Active/inactive checkbox
- Optional password reset field
- Warning box about changes taking effect immediately
- Save and Cancel buttons

### 2. `templates/admin/edit_conversation.html`
Form to edit conversation details with:
- Question textarea (expandable)
- Answer textarea (expandable)
- Conversation metadata (ID, timestamp, type)
- Guest user information section (if applicable)
- Save and Cancel buttons

### 3. `templates/admin/merge_users.html`
Interactive merge interface with:
- Side-by-side user selection dropdowns
- Real-time preview of selected users
- Visual arrow showing merge direction
- Detailed user information display
- JavaScript validation
- Double confirmation system
- Warning about irreversible action

## Updated Routes

### Admin Blueprint Routes (`admin.py`)

```python
# EDIT ROUTES
GET/POST /admin/users/<user_id>/edit          - Edit user form
GET/POST /admin/conversations/<conv_id>/edit  - Edit conversation form
GET/POST /admin/users/merge                    - Merge accounts interface

# DELETE ROUTES
POST /admin/users/<user_id>/delete             - Delete user
POST /admin/conversations/<conv_id>/delete     - Delete conversation
```

## Database Operations

### Update Operations
- User updates use SQLAlchemy's commit system
- Password changes use `set_password()` method with hashing
- Conversations can be updated including guest info
- All updates are transactional with rollback on error

### Delete Operations
- User deletion uses cascade to remove conversations
- Direct deletion via `db.session.delete()`
- Conversation deletion is independent
- All deletes are transactional

### Merge Operations
- Transfers all conversations via foreign key update
- Uses transaction for atomicity
- Deletes source user after transfer
- Counts transferred conversations for confirmation

## Security Features

1. **Admin Authentication Required**
   - All routes protected by `@admin_required` decorator
   - Session-based authentication
   - Redirects to login if not authenticated

2. **Confirmation Dialogs**
   - JavaScript confirm() for all destructive operations
   - Clear warning messages
   - Details shown in confirmation text

3. **Data Validation**
   - Form field validation
   - Password length requirements (6+ characters)
   - Email format validation
   - Prevents self-merge

4. **Error Handling**
   - Try-catch blocks around database operations
   - Flash messages for success/error feedback
   - Database rollback on errors
   - 404 errors for non-existent records

## Usage Examples

### Example 1: Fix Student Information
**Scenario:** Student entered wrong email during registration

1. Go to Admin Panel → Users
2. Search for student by name or ID
3. Click ✏️ edit icon or open profile and click "Edit User"
4. Update email address
5. Click "Save Changes"
6. Student can now login with corrected email

### Example 2: Remove Inappropriate Content
**Scenario:** Student asked inappropriate question

1. Go to Admin Panel → Conversations
2. Find the conversation (use search if needed)
3. Click 🗑️ delete icon
4. Confirm deletion
5. Conversation permanently removed

### Example 3: Merge Duplicate Accounts
**Scenario:** Student accidentally created two accounts

1. Go to Admin Panel → Users
2. Click "🔀 Merge Accounts"
3. Select duplicate account as "Source User"
4. Select main account as "Target User"
5. Review preview showing both accounts
6. Click "Merge Accounts"
7. Confirm the merge
8. All conversations moved to main account, duplicate deleted

### Example 4: Edit Guest User Data
**Scenario:** Guest user data has typo

1. Go to Admin Panel → Conversations
2. Find conversation from guest user
3. Click ✏️ edit icon
4. Scroll to "Guest User Information" section
5. Update name, email, or other fields
6. Click "Save Changes"

## Flash Message System

The admin panel uses Flask's flash message system:

```python
# Success messages (green)
flash('User updated successfully!', 'success')

# Error messages (red)
flash('Error updating user: ...', 'error')
```

Messages appear at top of page after redirects.

## Best Practices

### When to Edit vs Delete

**Edit When:**
- Correcting typos or data entry errors
- Updating contact information
- Fixing misspelled names
- Adjusting course sections

**Delete When:**
- Removing test data
- Removing duplicate entries (after merging)
- Removing inappropriate content
- Cleaning up old/unused accounts

**Merge When:**
- Student has duplicate accounts
- Consolidating accounts with different emails
- Combining accounts from different registration methods

### Safety Tips

1. **Always verify before deleting**
   - Check conversation count
   - Review user information
   - Consider editing instead of deleting

2. **Use merge for duplicates**
   - Don't delete both accounts
   - Merge preserves all data
   - Choose primary account carefully

3. **Backup before bulk operations**
   - Use "Create Backup" before major changes
   - Export data regularly
   - Keep records of changes

4. **Test on non-critical data first**
   - Try editing test accounts
   - Practice merge operations
   - Understand confirmation dialogs

## Technical Details

### Form Handling
- GET requests display forms with current data
- POST requests process updates
- Validation on server side
- Flash messages for feedback
- Redirects after successful operations

### Database Transactions
```python
try:
    db.session.commit()
    flash('Success!', 'success')
except Exception as e:
    db.session.rollback()
    flash(f'Error: {str(e)}', 'error')
```

### Cascade Deletes
Configured in `models.py`:
```python
conversations = db.relationship('Conversation', 
                               cascade='all, delete-orphan')
```

## Troubleshooting

### "User updated successfully" but changes don't appear
- Clear browser cache
- Refresh the page
- Check you edited the correct user

### Delete button doesn't work
- Check JavaScript is enabled
- Look for console errors
- Ensure admin session is active

### Merge doesn't transfer all conversations
- Check source user had conversations
- Verify database constraints
- Look at flash error message

### Edit form shows old data after save
- This is normal - form prepopulates with current data
- Changes are saved to database
- Navigate away and back to verify

## Future Enhancements (Potential)

- Bulk delete operations
- Bulk edit capabilities
- Undo/restore deleted items
- Audit log of all changes
- Email notifications for changes
- Advanced merge with field selection
- Conversation reassignment to different users
- Export filtered data

## Files Modified/Created

### New Files:
- `templates/admin/edit_user.html`
- `templates/admin/edit_conversation.html`
- `templates/admin/merge_users.html`
- `CHUNK7_CRUD_GUIDE.md` (this file)

### Modified Files:
- `admin.py` - Added 6 new routes
- `templates/admin/users.html` - Added merge button and action icons
- `templates/admin/user_detail.html` - Added edit/delete buttons
- `templates/admin/conversations.html` - Added edit/delete icons

## Summary

Chunk 7 completes the CRUD functionality for the Student Q&A Chatbot admin panel:

✅ **Create** - Already existed (user registration, conversations via chat)
✅ **Read** - Already existed (view users, conversations, analytics)
✅ **Update** - NEW: Edit users and conversations
✅ **Delete** - NEW: Remove users and conversations
✅ **Merge** - BONUS: Combine duplicate accounts

All operations are available through the admin web interface with proper authentication, validation, and user-friendly confirmations.
