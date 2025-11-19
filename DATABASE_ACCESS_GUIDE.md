# How to Access the Database

You have **3 different ways** to access your database:

## Method 1: Admin Web Panel (Easiest) ✅

**Best for:** Browsing, viewing, exporting data

### Steps:
1. Visit http://localhost:5000
2. Click "🔐 Admin Login" (top-right)
3. Login with:
   - Email: admin@uvu.edu
   - Password: admin123

### What You Can Do:
- **Dashboard** - View statistics and recent activity
- **Users** - Browse all registered students, search, view profiles
- **Conversations** - Browse all Q&A pairs, filter, search
- **Analytics** - Usage patterns, top users, charts
- **Export Users** - Download all users as CSV (Excel)
- **Export Conversations** - Download all Q&A pairs as CSV
- **Backup** - Create JSON backup files

**This is the easiest way!** No command line needed.

---

## Method 2: Python Interactive Shell

**Best for:** Querying data, making changes, scripting

### Open Python Shell:
```bash
cd "C:\Users\10295495\OneDrive - Utah Valley University\Cursor\Student_QA_Chatbot"
venv\Scripts\activate
python
```

### View All Users:
```python
from web_app_sql import app, db, User, Conversation
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"{user.email} - {user.first_name} {user.last_name}")
```

### View All Conversations:
```python
from web_app_sql import app, db, User, Conversation
with app.app_context():
    convs = Conversation.query.all()
    for conv in convs:
        print(f"Q: {conv.question[:50]}...")
        print(f"A: {conv.answer[:50]}...\n")
```

### Count Users:
```python
from web_app_sql import app, db, User
with app.app_context():
    total = User.query.count()
    print(f"Total users: {total}")
```

### Find Specific User:
```python
from web_app_sql import app, db, User
with app.app_context():
    user = User.query.filter_by(email='student@example.com').first()
    if user:
        print(f"Found: {user.first_name} {user.last_name}")
        print(f"Conversations: {user.conversations.count()}")
```

### View User's Conversations:
```python
from web_app_sql import app, db, User
with app.app_context():
    user = User.query.filter_by(email='student@example.com').first()
    for conv in user.conversations:
        print(f"Q: {conv.question}")
        print(f"A: {conv.answer}\n")
```

### Database Statistics:
```python
from web_app_sql import app
from database import get_database_stats
with app.app_context():
    stats = get_database_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
```

---

## Method 3: SQLite Database Browser (GUI Tool)

**Best for:** Visual exploration, SQL queries, schema viewing

### Download DB Browser for SQLite:
https://sqlitebrowser.org/dl/

### Open Your Database:
1. Install DB Browser for SQLite
2. Open the program
3. Click "Open Database"
4. Navigate to: `C:\Users\10295495\OneDrive - Utah Valley University\Cursor\Student_QA_Chatbot\chatbot.db`
5. Browse tables visually

### What You Can Do:
- View tables: users, conversations, admin_users
- Run SQL queries
- Export to CSV, JSON, SQL
- See database schema
- Edit data directly (be careful!)

### Example SQL Queries in DB Browser:

**View all users:**
```sql
SELECT * FROM users;
```

**Count conversations:**
```sql
SELECT COUNT(*) FROM conversations;
```

**Find conversations by user:**
```sql
SELECT u.first_name, u.last_name, c.question, c.timestamp
FROM conversations c
JOIN users u ON c.user_id = u.id
WHERE u.email = 'student@example.com'
ORDER BY c.timestamp DESC;
```

**Top 10 most active users:**
```sql
SELECT u.first_name, u.last_name, u.email, COUNT(c.id) as conversation_count
FROM users u
LEFT JOIN conversations c ON u.id = c.user_id
GROUP BY u.id
ORDER BY conversation_count DESC
LIMIT 10;
```

---

## Method 4: Migration Script

**Best for:** Quick stats, creating backups

### Run the Script:
```bash
cd "C:\Users\10295495\OneDrive - Utah Valley University\Cursor\Student_QA_Chatbot"
venv\Scripts\activate
python migrate_to_sql.py
```

### Menu Options:
1. Migrate JSON data to SQL (already done)
2. Create admin user (already done)
3. **View database statistics** ← Use this!
4. Exit

---

## Quick Reference: Common Tasks

### Task: View all users
**Method:** Admin Panel → Users page

### Task: Export data to Excel
**Method:** Admin Panel → Export Users/Conversations → Download CSV

### Task: See how many conversations today
**Method:** Admin Panel → Dashboard (shows recent conversations)

### Task: Find a specific student's chats
**Method:** Admin Panel → Users → Search for student → View their conversations

### Task: Backup everything
**Method:** Admin Panel → Dashboard → Click "Create Backup" button

### Task: Run custom SQL query
**Method:** DB Browser for SQLite → Execute SQL tab

### Task: Check database statistics
**Method:** 
- Admin Panel → Dashboard (visual stats)
- OR: `python migrate_to_sql.py` → Option 3

---

## Database File Location

Your database file is located at:
```
C:\Users\10295495\OneDrive - Utah Valley University\Cursor\Student_QA_Chatbot\chatbot.db
```

- **SQLite database** (for local development)
- Can copy this file for backup
- Open with DB Browser for SQLite
- On Heroku, it will use PostgreSQL instead

---

## Recommended Workflow

**For Regular Use:**
1. Use **Admin Web Panel** (easiest, no technical knowledge needed)
2. Export to CSV when you need data in Excel

**For Advanced Queries:**
1. Use **DB Browser for SQLite** (visual, powerful)
2. Run SQL queries for custom reports

**For Automation/Scripts:**
1. Use **Python shell** to query programmatically
2. Create scripts to generate reports

---

## Example: Complete Data Export

**Via Admin Panel (Easiest):**
1. Login to admin panel
2. Click "Export Users" → Get users.csv
3. Click "Export Conversations" → Get conversations.csv
4. Click "Create Backup" → Get JSON files
5. Open CSV files in Excel

**Via Python:**
```python
from web_app_sql import app, db, User, Conversation
import csv

with app.app_context():
    # Export users
    users = User.query.all()
    with open('my_users.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Email', 'Name', 'Student ID', 'Conversations'])
        for user in users:
            writer.writerow([
                user.email,
                f"{user.first_name} {user.last_name}",
                user.student_id,
                user.conversations.count()
            ])
    
    print("Exported to my_users.csv")
```

---

## Security Notes

⚠️ **Keep your database secure:**
- Don't share chatbot.db file (contains passwords)
- Don't commit chatbot.db to git (already in .gitignore)
- Change admin password from default
- Backup regularly

✅ **Safe to share:**
- CSV exports (no passwords)
- JSON backups from admin panel (no passwords)
- Statistics and reports

---

## Need Help?

**Can't see data?**
- Make sure you've created some users/conversations first
- Try admin panel Dashboard to see if anything exists

**Database file missing?**
- It's created automatically when you run web_app_sql.py
- Look for chatbot.db in project folder

**Admin panel not loading?**
- Make sure web_app_sql.py is running
- Check http://localhost:5000/admin/login
- Verify admin account exists (email: admin@uvu.edu)

---

**Start with the Admin Web Panel - it's the easiest way to browse your data!**

Visit: http://localhost:5000 → Click "🔐 Admin Login"
