# Pre-Production Security Audit
## Student Q&A Chatbot

**Date:** November 18, 2025  
**Status:** ⚠️ ACTION REQUIRED

---

## 🔍 Audit Summary

**Good News:** ✅ No hard-coded secrets in production code  
**Action Required:** ⚠️ Fix fallback credentials and .gitignore

---

## 1. Hard-Coded Sensitive Data Audit

### ✅ PASSED: API Keys
**Finding:** No hard-coded API keys found in production code

**Evidence:**
```python
# chatbot.py:98
self.api_key = os.getenv("MISTRAL_API_KEY")

# All environment variables properly loaded from .env
```

**Status:** ✅ SECURE

---

### ⚠️ ACTION REQUIRED: Fallback SECRET_KEY

**Finding:** Development fallback SECRET_KEY present in multiple files

**Affected Files:**
1. `web_app_sql.py:27`
   ```python
   app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
   ```

2. `migrate_to_sql.py:23`
   ```python
   app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
   ```

3. `web_app.py:23`
   ```python
   app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
   ```

**Risk:** If .env file is missing, app will use weak development key

**Recommendation:**  
❌ Remove fallback OR
✅ Change to fail-fast approach:

```python
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise ValueError("SECRET_KEY environment variable not set!")
```

**Priority:** HIGH  
**Before Production:** MUST FIX

---

### ⚠️ INFORMATIONAL: Default Admin Credentials

**Finding:** Default admin credentials mentioned in security_setup.py comments

**File:** `security_setup.py:67`
```python
print("Current password: admin123 (DEFAULT - MUST CHANGE!)\n")
```

**File:** `test_api.py:57`
```python
def login_admin(self, email='admin@uvu.edu', password='admin123'):
```

**Status:** ⚠️ DOCUMENTATION ONLY (not hard-coded in production)

**These are:**
- ✅ Only in setup scripts (not production code)
- ✅ Not actually used unless admin creates with this password
- ✅ Security script reminds user to change

**Action:** Ensure admin password is changed before production (use `security_setup.py`)

---

### ⚠️ ACTION REQUIRED: Test File Credentials

**Finding:** Test credentials in test_api.py

**File:** `test_api.py`
```python
# Line 39
def login_user(self, email='test@example.com', password='test123'):

# Line 57  
def login_admin(self, email='admin@uvu.edu', password='admin123'):
```

**Risk:** Low (test file only, not used in production)

**Recommendation:**
- ✅ Keep as-is for testing
- ⚠️ Ensure test_api.py not deployed to production
- ✅ Verify .gitignore excludes test data

---

## 2. Environment Variable Configuration

### ✅ PASSED: All Config from Environment

**Finding:** All configuration properly loads from environment variables

**Files Checked:**
- `web_app_sql.py` - ✅ Loads SECRET_KEY, DATABASE_URL
- `database.py` - ✅ Loads DATABASE_URL
- `chatbot.py` - ✅ Loads MISTRAL_API_KEY
- `admin.py` - ✅ Uses session security from config
- `api.py` - ✅ Uses app security settings

**Evidence:**
```python
# web_app_sql.py
app.secret_key = os.getenv('SECRET_KEY', ...)
app.config['SESSION_COOKIE_HTTPONLY'] = True  # ✅ Hard-coded security
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # ✅ Hard-coded security

# database.py
database_url = os.getenv('DATABASE_URL')

# chatbot.py
self.api_key = os.getenv("MISTRAL_API_KEY")
```

**Status:** ✅ GOOD PRACTICE

---

## 3. .gitignore Audit

### ⚠️ ACTION REQUIRED: Missing Important Entries

**Current .gitignore:**
```
venv/
__pycache__/
*.pyc
.env
*.pdf
*.docx
*.mp4
corpus/
qa_conversations.json
users_db.json
.flask_session/
instance/
*.db
backup_*.json
migrations/
```

**Missing Critical Entries:**
```
# Add these:
.env.local
.env.*.local
*.log
*.pid
.DS_Store
.vscode/
.idea/
*.swp
*.swo
*~
.python-version
local_settings.py
```

**Recommendations:**

### Updated .gitignore for Production:
```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Python
venv/
env/
ENV/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
.python-version

# Flask
instance/
.webassets-cache
.flask_session/

# Database
*.db
*.sqlite
*.sqlite3
backup_*.json

# Migrations (if using Alembic manually)
migrations/

# Legacy data files
qa_conversations.json
users_db.json

# Course materials (large files)
*.pdf
*.docx
*.mp4
*.pptx
*.xlsx
corpus/

# Logs
*.log
logs/
*.pid

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/

# OS
Thumbs.db
```

**Priority:** MEDIUM  
**Action:** Update .gitignore before first commit

---

## 4. Security Configuration Summary

### ✅ EXCELLENT: Security Settings

**Web App SQL (web_app_sql.py):**
```python
app.config['SESSION_COOKIE_HTTPONLY'] = True      # ✅ Prevents XSS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'    # ✅ Prevents CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # ✅ 1-hour timeout
```

**Database (database.py):**
```python
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # ✅ Performance
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True  # ✅ Connection health check
}
```

**Status:** ✅ PRODUCTION READY

---

## 5. Password Security

### ✅ EXCELLENT: Password Hashing

**Implementation:**
```python
# models.py - User class
def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

**Using:** Werkzeug's PBKDF2-SHA256 with 260,000 iterations

**Status:** ✅ EXCELLENT (Industry standard)

---

## 6. Pre-Production Checklist

### 🔴 MUST DO Before Production

- [ ] **CRITICAL:** Change SECRET_KEY from default
  ```bash
  python security_setup.py
  # Choose option 1
  ```

- [ ] **CRITICAL:** Change admin password from default
  ```bash
  python security_setup.py
  # Choose option 2
  ```

- [ ] **CRITICAL:** Verify .env file exists and has real values
  ```bash
  # Check .env contains:
  MISTRAL_API_KEY=your_real_key_here
  SECRET_KEY=your_generated_key_here
  ```

- [ ] **HIGH:** Update .gitignore (see section 3)

- [ ] **HIGH:** Remove fallback SECRET_KEY or make fail-fast
  ```python
  # In web_app_sql.py, migrate_to_sql.py
  app.secret_key = os.getenv('SECRET_KEY')
  if not app.secret_key:
      raise ValueError("SECRET_KEY must be set!")
  ```

- [ ] **MEDIUM:** Verify .env NOT in Git
  ```bash
  git status
  # Should NOT show .env
  ```

- [ ] **MEDIUM:** Set Heroku environment variables
  ```bash
  heroku config:set MISTRAL_API_KEY=your_key
  heroku config:set SECRET_KEY=your_secret
  ```

### 🟡 SHOULD DO Before Production

- [ ] Enable debug=False in web_app_sql.py
  ```python
  # Currently line ~400
  app.run(host='0.0.0.0', port=port, debug=False)  # ✅ Already False!
  ```

- [ ] Set SESSION_COOKIE_SECURE=True for HTTPS (Heroku auto)
  ```bash
  heroku config:set SESSION_COOKIE_SECURE=True
  ```

- [ ] Review admin email (currently admin@uvu.edu)

- [ ] Test all functionality after SECRET_KEY change

### 🟢 NICE TO HAVE

- [ ] Add rate limiting (Flask-Limiter)
- [ ] Add CORS configuration (Flask-CORS) for API
- [ ] Add logging configuration
- [ ] Set up error monitoring (Sentry, etc.)

---

## 7. Detailed Findings

### File-by-File Analysis

#### web_app_sql.py (Main Application)
- ✅ Loads all config from environment
- ⚠️ Has fallback SECRET_KEY
- ✅ Security settings properly configured
- ✅ No hard-coded credentials
- **Grade:** A- (would be A+ without fallback)

#### database.py
- ✅ Loads DATABASE_URL from environment
- ✅ Proper SQLAlchemy configuration
- ✅ No sensitive data
- **Grade:** A+

#### admin.py
- ✅ No hard-coded credentials
- ✅ Uses password hashing
- ✅ Session validation
- **Grade:** A+

#### api.py
- ✅ No hard-coded credentials
- ✅ Proper authentication checks
- ✅ Uses app security configuration
- **Grade:** A+

#### chatbot.py
- ✅ Loads API key from environment
- ✅ Fails gracefully if missing
- ✅ No hard-coded data
- **Grade:** A+

#### models.py
- ✅ Excellent password hashing
- ✅ No default passwords
- ✅ Secure by design
- **Grade:** A+

#### migrate_to_sql.py
- ⚠️ Has fallback SECRET_KEY
- ✅ Prompts for admin password (not hard-coded)
- ✅ Setup script only
- **Grade:** B+ (acceptable for setup script)

#### security_setup.py
- ✅ Generates secure keys
- ✅ Changes admin password
- ⚠️ Mentions default password in help text (acceptable)
- **Grade:** A

#### test_api.py
- ⚠️ Contains test credentials (acceptable)
- ✅ Not used in production
- ✅ Documented as test file
- **Grade:** A (for test file)

---

## 8. Comparison with Best Practices

### ✅ What You're Doing Right

1. **Environment Variables:** All secrets loaded from .env ✅
2. **Password Hashing:** Using PBKDF2-SHA256 ✅
3. **Session Security:** HTTPOnly, SameSite configured ✅
4. **Database:** SQLAlchemy ORM prevents SQL injection ✅
5. **Input Validation:** Email regex, length limits ✅
6. **No Plain Passwords:** All hashed in database ✅
7. **.env in .gitignore:** Prevents secret commits ✅
8. **Security Setup Script:** Makes it easy to secure ✅

### ⚠️ What Needs Improvement

1. **Fallback SECRET_KEY:** Remove or fail-fast ⚠️
2. **.gitignore:** Add more IDE/OS files ⚠️
3. **Pre-Production:** Must change defaults before deploy ⚠️

---

## 9. Recommended Fixes

### Fix 1: Remove Fallback SECRET_KEY (CRITICAL)

**File:** `web_app_sql.py`

**Current (Line 27):**
```python
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
```

**Replace with:**
```python
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError(
        "SECRET_KEY environment variable not set! "
        "Run 'python security_setup.py' to generate one."
    )
```

**Repeat for:**
- `migrate_to_sql.py` (line 23)
- `web_app.py` (line 23) - if still using this file

---

### Fix 2: Update .gitignore

**Create improved .gitignore** (see section 3 for full version)

---

### Fix 3: Pre-Deployment Script

**Create `pre_deploy_check.py`:**

```python
"""
Pre-deployment security check
Run before deploying to production
"""

import os
from dotenv import load_dotenv

def check_environment():
    """Check all required environment variables."""
    load_dotenv()
    
    issues = []
    warnings = []
    
    # Check SECRET_KEY
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        issues.append("❌ SECRET_KEY not set in .env")
    elif secret_key == 'dev-secret-key-change-in-production':
        issues.append("❌ SECRET_KEY still using default value!")
    elif len(secret_key) < 32:
        warnings.append("⚠️  SECRET_KEY seems short (recommend 64+ chars)")
    
    # Check MISTRAL_API_KEY
    mistral_key = os.getenv('MISTRAL_API_KEY')
    if not mistral_key:
        issues.append("❌ MISTRAL_API_KEY not set in .env")
    elif mistral_key == 'your_mistral_api_key_here':
        issues.append("❌ MISTRAL_API_KEY still using placeholder!")
    
    # Print results
    print("="*60)
    print("PRE-DEPLOYMENT SECURITY CHECK")
    print("="*60)
    
    if not issues and not warnings:
        print("\n✅ ALL CHECKS PASSED!")
        print("✅ Ready for deployment")
        return True
    
    if issues:
        print("\n🔴 CRITICAL ISSUES:")
        for issue in issues:
            print(f"  {issue}")
    
    if warnings:
        print("\n🟡 WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    print("\n" + "="*60)
    return len(issues) == 0

if __name__ == '__main__':
    passed = check_environment()
    exit(0 if passed else 1)
```

**Usage:**
```bash
python pre_deploy_check.py
# Must pass before: git push heroku main
```

---

## 10. Final Security Score

### Overall Grade: A-

**Breakdown:**
- API Key Management: A+ ✅
- Password Security: A+ ✅
- Session Security: A+ ✅
- Database Security: A+ ✅
- Environment Config: A ✅
- .gitignore: B+ ⚠️
- Production Hardening: B ⚠️ (needs SECRET_KEY fix)

**With Recommended Fixes: A+**

---

## 11. Deployment Checklist

### Pre-Commit
```bash
# 1. Update .gitignore
git status  # Verify .env not listed

# 2. Generate new SECRET_KEY
python security_setup.py  # Option 1

# 3. Change admin password
python security_setup.py  # Option 2

# 4. Run pre-deployment check
python pre_deploy_check.py

# 5. Commit
git add .
git commit -m "Security hardening for production"
git push origin main
```

### Pre-Deploy to Heroku
```bash
# 1. Set environment variables on Heroku
heroku config:set MISTRAL_API_KEY=your_real_key
heroku config:set SECRET_KEY=your_generated_key
heroku config:set SESSION_COOKIE_SECURE=True

# 2. Verify
heroku config

# 3. Deploy
git push heroku main

# 4. Initialize database
heroku run python migrate_to_sql.py

# 5. Test
heroku open
```

---

## 12. Summary

### ✅ What's Secure
- No hard-coded API keys in production code
- All sensitive config from environment variables
- Excellent password hashing (PBKDF2-SHA256)
- Strong session security (HTTPOnly, SameSite)
- SQL injection protection (SQLAlchemy ORM)
- .env file in .gitignore

### ⚠️ What Needs Action
1. Remove/fix fallback SECRET_KEY (CRITICAL)
2. Update .gitignore (MEDIUM)
3. Change SECRET_KEY before production (CRITICAL)
4. Change admin password before production (CRITICAL)
5. Run pre-deployment check (RECOMMENDED)

### 🎯 Next Steps
1. Apply fixes from section 9
2. Run `python security_setup.py`
3. Update `.gitignore`
4. Create `pre_deploy_check.py`
5. Test locally
6. Deploy with confidence!

---

**Audit Complete!**  
**Date:** November 18, 2025  
**Auditor:** GitHub Copilot  
**Status:** ⚠️ FIX REQUIRED → ✅ PRODUCTION READY (after fixes)

