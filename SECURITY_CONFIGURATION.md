# Security Configuration Guide
## Student Q&A Chatbot - Production Security Setup

This guide provides step-by-step instructions for configuring security settings before deploying to production.

---

## 1. Environment Variables Configuration

### 1.1 Generate Secure SECRET_KEY

**Never use the default SECRET_KEY in production!**

```python
# Run this in Python to generate a secure key:
import secrets
print(secrets.token_hex(32))
```

Example output: `3c5d8f2a1b9e4d6c7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f`

### 1.2 Update .env File

```env
# .env file (NEVER commit this file!)
MISTRAL_API_KEY=your_actual_mistral_api_key_here
SECRET_KEY=3c5d8f2a1b9e4d6c7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f
```

### 1.3 Verify .gitignore

Ensure `.gitignore` contains:
```
.env
*.db
instance/
__pycache__/
venv/
```

---

## 2. Admin Password Security

### 2.1 Change Default Admin Password

**Default credentials (MUST CHANGE):**
- Email: admin@uvu.edu
- Password: admin123

**To change:**

```python
# Run in Python shell:
from web_app_sql import app, db, AdminUser
with app.app_context():
    admin = AdminUser.query.filter_by(email='admin@uvu.edu').first()
    if admin:
        admin.set_password('YourNewSecurePassword123!')
        db.session.commit()
        print("Admin password updated successfully!")
```

**Password requirements:**
- Minimum 12 characters
- Mix of uppercase and lowercase
- Include numbers
- Include special characters
- Don't use common words or patterns

---

## 3. Session Security Configuration

### 3.1 Current Security Settings

Already configured in `web_app_sql.py`:

```python
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevents JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour timeout
```

### 3.2 Additional Production Settings

For HTTPS environments (Heroku, AWS, etc.), add:

```python
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only (production)
```

**Note:** Only enable `SESSION_COOKIE_SECURE` when using HTTPS!

---

## 4. Database Security

### 4.1 File Permissions (Linux/Mac)

```bash
chmod 600 chatbot.db  # Read/write for owner only
chmod 700 instance/    # Directory access for owner only
```

### 4.2 Backup Strategy

**Automated backups:**
```bash
# Create backup script: backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp chatbot.db backups/chatbot_${DATE}.db
# Keep only last 7 days of backups
find backups/ -name "chatbot_*.db" -mtime +7 -delete
```

**Schedule with cron (Linux/Mac):**
```bash
# Daily at 2 AM
0 2 * * * /path/to/backup.sh
```

### 4.3 PostgreSQL (Production)

For Heroku or AWS deployment:

```bash
# Set DATABASE_URL environment variable
heroku config:set DATABASE_URL=postgres://user:pass@host:port/dbname
```

The app automatically uses PostgreSQL when DATABASE_URL is set.

---

## 5. HTTPS Configuration

### 5.1 Heroku Deployment

Heroku provides automatic HTTPS. No additional configuration needed!

```bash
# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

### 5.2 Custom Server (Flask-Talisman)

Install Flask-Talisman:
```bash
pip install flask-talisman
```

Add to `web_app_sql.py`:
```python
from flask_talisman import Talisman

# After app = Flask(__name__)
Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    session_cookie_secure=True
)
```

---

## 6. Input Validation Enhancements

### 6.1 Current Protections

✅ Already implemented:
- Email format validation
- Password length requirement (6+ chars)
- Question length limit (1000 chars)
- Input sanitization (strip whitespace)
- SQL injection protection (SQLAlchemy ORM)
- XSS protection (Jinja2 auto-escaping)

### 6.2 Optional: Add Password Complexity

Add to `web_app_sql.py` registration validation:

```python
import re

def validate_password_strength(password):
    """Validate password meets complexity requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain a number"
    return True, "Password is strong"

# Use in registration:
is_valid, message = validate_password_strength(password)
if not is_valid:
    return render_template('register.html', error=message)
```

---

## 7. Rate Limiting (Optional but Recommended)

### 7.1 Install Flask-Limiter

```bash
pip install flask-limiter
```

### 7.2 Configure Rate Limiting

Add to `web_app_sql.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Apply to login route
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    # ... existing code ...
```

**Recommended limits:**
- Login: 5 attempts per minute
- Registration: 3 per hour
- API calls: 60 per minute

---

## 8. Error Handling & Logging

### 8.1 Production Error Handler

Add to `web_app_sql.py`:

```python
import logging

# Configure logging
if not app.debug:
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server Error: {error}')
    return render_template('error.html', 
                         message="An internal error occurred"), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                         message="Page not found"), 404
```

### 8.2 Security Event Logging

Add security event logging:

```python
def log_security_event(event_type, details):
    """Log security-relevant events."""
    app.logger.warning(f'SECURITY: {event_type} - {details}')

# Use in login failures:
if not user or not user.check_password(password):
    log_security_event('LOGIN_FAILED', f'Email: {email}')
```

---

## 9. Production Deployment Checklist

### Pre-Deployment

- [ ] Change SECRET_KEY from default
- [ ] Change admin password
- [ ] Update .env with production keys
- [ ] Review .gitignore (no sensitive files)
- [ ] Test all routes
- [ ] Run security audit
- [ ] Configure backups
- [ ] Set up monitoring

### During Deployment

- [ ] Set environment variables
- [ ] Enable HTTPS
- [ ] Configure database
- [ ] Set SESSION_COOKIE_SECURE=True
- [ ] Disable debug mode
- [ ] Configure logging
- [ ] Test authentication
- [ ] Verify session management

### Post-Deployment

- [ ] Verify HTTPS working
- [ ] Test login/logout
- [ ] Test admin panel
- [ ] Check error handling
- [ ] Monitor logs
- [ ] Test backups
- [ ] Document production URLs
- [ ] Update admin credentials document

---

## 10. Security Monitoring

### 10.1 What to Monitor

**Login Activity:**
- Failed login attempts (potential brute force)
- Multiple sessions from different IPs
- Unusual login times

**Database Activity:**
- Mass data exports
- Bulk deletions
- Schema changes

**API Activity:**
- Unusual traffic patterns
- Repeated 403/401 errors
- High request rates

### 10.2 Alert Thresholds

**Critical (immediate action):**
- 10+ failed logins in 5 minutes
- Database connection failures
- Unhandled exceptions

**Warning (review within 24 hours):**
- 5+ failed logins in 1 hour
- Unusual geographic access patterns
- High API usage

---

## 11. Maintenance Schedule

### Daily
- Review error logs
- Check backup success
- Monitor disk space

### Weekly
- Review security logs
- Check for failed logins
- Test backup restoration

### Monthly
- Update dependencies (`pip install --upgrade`)
- Review access permissions
- Test disaster recovery
- Rotate admin passwords (recommended)

### Quarterly
- Security audit
- Penetration testing
- Update documentation
- Review and update this guide

---

## 12. Security Incident Response

### If Breach Suspected

1. **Immediate Actions:**
   - Take affected system offline if needed
   - Change all passwords immediately
   - Revoke all active sessions
   - Enable maintenance mode

2. **Investigation:**
   - Review access logs
   - Check database for unauthorized changes
   - Identify entry point
   - Document timeline

3. **Remediation:**
   - Patch vulnerability
   - Restore from clean backup if needed
   - Update security measures
   - Deploy fixes

4. **Notification:**
   - Notify affected users (if data compromised)
   - Document incident
   - Report to appropriate authorities if required

### Emergency Contacts

- **Technical Lead:** [Name, Email, Phone]
- **Security Team:** [Contact Info]
- **Database Admin:** [Contact Info]

---

## 13. Quick Reference: Security Commands

### Generate Secret Key
```python
import secrets; print(secrets.token_hex(32))
```

### Change Admin Password
```bash
python -c "from web_app_sql import app, db, AdminUser; app.app_context().push(); admin = AdminUser.query.first(); admin.set_password('NewPassword'); db.session.commit()"
```

### Create Database Backup
```bash
cp chatbot.db chatbot_backup_$(date +%Y%m%d).db
```

### Check for Weak Passwords (admin shell)
```python
from web_app_sql import app, db, User
with app.app_context():
    users = User.query.all()
    # Manual review - check password policies
```

### Clear All Sessions
```bash
rm -rf flask_session/*
```

---

## 14. Additional Resources

**Documentation:**
- SECURITY_AUDIT.md - Comprehensive security audit
- CHUNK8_SECURITY_GUIDE.md - This document
- DATABASE_ACCESS_GUIDE.md - Database security

**External Resources:**
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [SQLAlchemy Security](https://docs.sqlalchemy.org/en/20/faq/security.html)

---

**Remember:** Security is an ongoing process, not a one-time setup!

Regularly review and update your security measures as threats evolve.
