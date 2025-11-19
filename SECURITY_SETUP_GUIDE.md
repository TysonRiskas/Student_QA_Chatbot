# Security Setup - Quick Start Guide

## Easy Way: Run the Security Setup Script

I've created a simple script that does everything for you!

### Steps:

1. **Open your terminal/command prompt**

2. **Navigate to your project directory:**
   ```bash
   cd "C:\Users\10295495\OneDrive - Utah Valley University\Cursor\Student_QA_Chatbot"
   ```

3. **Activate your virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

4. **Run the security setup script:**
   ```bash
   python security_setup.py
   ```

5. **Follow the prompts:**
   - Choose option 3 ("Do both - recommended")
   - Enter a new admin password when prompted (min 12 characters)
   - Confirm your password
   - Done! ✅

### What the Script Does:

✅ **Generates a secure SECRET_KEY**
- Creates a cryptographically secure 64-character key
- Automatically updates (or creates) your .env file
- Warns you not to commit .env to git

✅ **Changes Admin Password**
- Prompts you for a new password (min 12 chars)
- Hashes it securely with PBKDF2-SHA256
- Updates the database
- Confirms success

### Example Session:

```
$ python security_setup.py

============================================================
SECURITY SETUP SCRIPT
Student Q&A Chatbot
============================================================

Options:
1. Generate new SECRET_KEY
2. Change admin password
3. Do both (recommended)
4. Exit

Enter your choice (1-4): 3

============================================================
GENERATING SECRET_KEY
============================================================

Your new SECRET_KEY:
a1b2c3d4e5f6...

✅ Updated SECRET_KEY in .env file

============================================================
CHANGING ADMIN PASSWORD
============================================================

Current admin email: admin@uvu.edu
Current password: admin123 (DEFAULT - MUST CHANGE!)

Enter new admin password (min 12 characters): YourSecurePassword123!
Confirm new password: YourSecurePassword123!

✅ Admin password updated successfully!
✅ New password is secure and hashed in database

⚠️  REMEMBER YOUR NEW PASSWORD - It cannot be recovered!
```

---

## Manual Way (If You Prefer)

### 1. Generate SECRET_KEY Manually

**Option A: In Python Shell**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and manually add to `.env` file:
```env
SECRET_KEY=paste_your_generated_key_here
```

**Option B: In Interactive Python**
```bash
python
>>> import secrets
>>> secrets.token_hex(32)
'your_key_will_appear_here'
>>> exit()
```

### 2. Change Admin Password Manually

**Open Python shell:**
```bash
python
```

**Run these commands:**
```python
from web_app_sql import app, db, AdminUser

with app.app_context():
    admin = AdminUser.query.filter_by(email='admin@uvu.edu').first()
    admin.set_password('YourNewSecurePassword123!')
    db.session.commit()
    print("Password changed!")
```

**Exit:**
```python
exit()
```

---

## Verification

### Test Your New Password:

1. Start the app:
   ```bash
   python web_app_sql.py
   ```

2. Navigate to: http://localhost:5000/admin/login

3. Login with:
   - Email: `admin@uvu.edu`
   - Password: `your_new_password`

4. If successful, you're all set! ✅

---

## Troubleshooting

### "ModuleNotFoundError"
**Problem:** Virtual environment not activated
**Solution:**
```bash
venv\Scripts\activate
```

### "Admin user not found"
**Problem:** Admin not created yet
**Solution:**
```bash
python migrate_to_sql.py
# Choose option 2
```

### "Password too short"
**Problem:** Password less than 12 characters
**Solution:** Use a longer, stronger password

### Forgot Your New Password?
**Solution:** Run `security_setup.py` again and choose option 2

---

## Security Best Practices

✅ **Use a strong password:**
- At least 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- Don't use common words or patterns

✅ **Never share your password:**
- Don't email it
- Don't write it in code
- Don't commit .env to git

✅ **Store it securely:**
- Use a password manager
- Write it down and keep in safe place
- Don't store in cloud storage

---

## Next Steps After Setup

1. ✅ SECRET_KEY generated
2. ✅ Admin password changed
3. ⬜ Test login with new credentials
4. ⬜ Deploy to production with HTTPS
5. ⬜ Monitor security logs

---

**Questions?** See SECURITY_CONFIGURATION.md for detailed information.

**Ready for production!** 🚀
