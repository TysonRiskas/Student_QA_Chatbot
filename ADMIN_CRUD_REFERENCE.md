# Admin Panel CRUD Operations - Quick Reference

## 🎯 Quick Access Map

### User Management

```
Admin Panel → Users
├── 🔀 Merge Accounts (top button)
│   └── Select 2 users → Merge → Confirm
│
└── User List (table)
    ├── ✏️ Edit User → Edit Form → Save
    ├── 👁️ View User → User Detail Page
    │   ├── ✏️ Edit User → Edit Form → Save
    │   └── 🗑️ Delete User → Confirm → Delete
    └── (Each row has edit/view icons)
```

### Conversation Management

```
Admin Panel → Conversations
└── Conversation List (cards)
    ├── ✏️ Edit → Edit Form → Save
    └── 🗑️ Delete → Confirm → Delete
```

## 🔗 Direct URLs

### Edit Operations
- Edit User: `http://localhost:5000/admin/users/<id>/edit`
- Edit Conversation: `http://localhost:5000/admin/conversations/<id>/edit`
- Merge Accounts: `http://localhost:5000/admin/users/merge`

### View Operations
- User List: `http://localhost:5000/admin/users`
- User Detail: `http://localhost:5000/admin/users/<id>`
- Conversations: `http://localhost:5000/admin/conversations`
- Dashboard: `http://localhost:5000/admin/dashboard`

### Delete Operations
- Delete User: POST to `/admin/users/<id>/delete`
- Delete Conversation: POST to `/admin/conversations/<id>/delete`

## 📋 Field Reference

### User Edit Form Fields
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| First Name | Text | Yes | Student's first name |
| Last Name | Text | Yes | Student's last name |
| Email | Email | Yes | Must be valid email format |
| Student ID | Text | Yes | University student ID |
| Course Section | Text | No | Section number |
| Semester | Text | No | e.g., "Fall 2024" |
| Active Account | Checkbox | No | Uncheck to disable login |
| New Password | Password | No | Min 6 chars, leave blank to keep current |

### Conversation Edit Form Fields
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Question | Textarea | Yes | Student's question |
| Answer | Textarea | Yes | AI's answer |

### Guest Conversation Additional Fields
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Guest First Name | Text | No | For guest users only |
| Guest Last Name | Text | No | For guest users only |
| Guest Student ID | Text | No | For guest users only |
| Guest Email | Email | No | For guest users only |
| Guest Course Section | Text | No | For guest users only |
| Guest Semester | Text | No | For guest users only |

### Merge Accounts Fields
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Source User | Dropdown | Yes | Account to delete |
| Target User | Dropdown | Yes | Account to keep |

## 🎨 Icon Legend

| Icon | Meaning | Action |
|------|---------|--------|
| ✏️ | Edit | Open edit form |
| 🗑️ | Delete | Delete with confirmation |
| 👁️ | View | View details |
| 🔀 | Merge | Merge two accounts |
| 💾 | Save | Save changes |
| ❌ | Cancel | Cancel operation |

## ⚡ Keyboard Shortcuts

While no keyboard shortcuts are built-in, you can:
- **Tab** - Navigate between form fields
- **Enter** - Submit form (when focused on text input)
- **Esc** - Close browser confirmation dialogs

## 🔔 Flash Message Types

| Type | Color | Meaning |
|------|-------|---------|
| Success | Green | Operation completed successfully |
| Error | Red | Operation failed, see message |

## 📊 Common Workflows

### Workflow 1: Fix Wrong Email
```
1. Users → Search for student
2. Click ✏️ edit icon
3. Update email field
4. Click "Save Changes"
5. ✓ Done
```

### Workflow 2: Remove Test Data
```
1. Conversations → Find test conversation
2. Click 🗑️ delete icon
3. Confirm deletion
4. ✓ Done
```

### Workflow 3: Merge Duplicate Accounts
```
1. Users → Click "Merge Accounts"
2. Select duplicate as Source
3. Select main account as Target
4. Review previews
5. Click "Merge Accounts"
6. Confirm merge
7. ✓ Done - All conversations transferred
```

### Workflow 4: Deactivate Student
```
1. Users → Find student → Click 👁️
2. Click "Edit User"
3. Uncheck "Active Account"
4. Click "Save Changes"
5. ✓ Done - Student cannot login
```

### Workflow 5: Batch Clean Users
```
1. Users → Identify test users
2. For each test user:
   a. Open profile
   b. Click "Delete User"
   c. Confirm
3. ✓ Done - All users and their conversations removed
```

## 🛡️ Safety Checklist

Before deleting or merging:
- [ ] Verify you have the correct user/conversation
- [ ] Check conversation count (shows impact)
- [ ] Consider editing instead of deleting
- [ ] Create backup if making bulk changes
- [ ] Read confirmation dialog carefully
- [ ] Understand that deletions cannot be undone

## 📞 Quick Help

**Can't find a user?**
→ Use the search bar on Users page

**Want to undo a delete?**
→ Deletions are permanent, restore from backup

**Merge the wrong accounts?**
→ Cannot undo, you'll need to manually recreate

**Edit not saving?**
→ Check for error flash message at top of page

**Delete button not working?**
→ Ensure JavaScript is enabled

**Need to bulk edit?**
→ Currently one-by-one only, use CSV export for analysis

## 🔄 Update Frequency

**When to Edit:**
- Student reports incorrect information
- Email address changed
- Course section changed
- Name spelling correction

**When to Delete:**
- Removing test data
- Cleaning up old accounts (after backup)
- Removing inappropriate content
- After successful merge (automated)

**When to Merge:**
- Student has duplicate accounts
- Same student with different emails
- Consolidating test accounts

## 📈 Admin Panel Navigation

```
┌─────────────────────────────────────────┐
│  🤖 Student Q&A Chatbot - Admin Panel  │
├─────────────────────────────────────────┤
│  Dashboard | Users | Conversations |    │
│  Analytics | Export Users | Export Convs│
│  Student Site | Logout                  │
└─────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│         Current Page Content             │
│  [CRUD operations available here]        │
│  • Edit buttons (✏️)                     │
│  • Delete buttons (🗑️)                   │
│  • View buttons (👁️)                     │
│  • Special features (🔀)                 │
└──────────────────────────────────────────┘
```

## 💾 Backup Reminder

**Before major operations:**
```
Dashboard → "Create Backup" button → JSON files saved
```

Files created:
- `users_backup_YYYYMMDD_HHMMSS.json`
- `conversations_backup_YYYYMMDD_HHMMSS.json`

---

**Print this page for quick reference while working in the admin panel!**
