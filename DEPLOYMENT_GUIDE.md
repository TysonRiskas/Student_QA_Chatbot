# Deployment Guide
## GitHub & Heroku Deployment for Student Q&A Chatbot

**Complete guide to deploying your chatbot to production**

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [GitHub Setup](#github-setup)
3. [Heroku Deployment](#heroku-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup (PostgreSQL)](#database-setup-postgresql)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

### ✅ Before You Deploy

**Complete these tasks first:**

- [ ] Test application locally (runs without errors)
- [ ] Change SECRET_KEY from default
- [ ] Change admin password from default
- [ ] Review and update `.gitignore`
- [ ] Remove any sensitive data from code
- [ ] Test all major features work
- [ ] Review security settings
- [ ] Prepare environment variables

### 🔒 Security Tasks

**Run the security setup:**

```bash
python security_setup.py
```

Choose option 3 ("Do both"):
- Generates new SECRET_KEY
- Changes admin password

**Verify `.gitignore` includes:**
```
.env
*.db
instance/
__pycache__/
venv/
.DS_Store
flask_session/
```

### 📝 Document Your Credentials

**Save these securely (NOT in Git):**
- SECRET_KEY (from `.env`)
- MISTRAL_API_KEY (from `.env`)
- Admin email and password
- Heroku app name
- Database connection string

---

## GitHub Setup

### Step 1: Create GitHub Repository

1. **Go to GitHub.com**
2. **Click "New Repository"**
3. **Fill in details:**
   - Name: `Student_QA_Chatbot`
   - Description: "AI-powered chatbot for INFO 6200 students"
   - Visibility: **Private** (recommended) or Public
   - **DO NOT** initialize with README (you have one)
4. **Click "Create Repository"**

### Step 2: Initialize Git Locally

**If not already initialized:**

```bash
cd "C:\Users\10295495\OneDrive - Utah Valley University\Cursor\Student_QA_Chatbot"
git init
```

**Verify `.gitignore` exists and contains:**

```bash
cat .gitignore
```

Should include:
```
.env
*.db
instance/
__pycache__/
venv/
```

### Step 3: Add Files to Git

```bash
# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status

# VERIFY .env is NOT listed!
```

**⚠️ CRITICAL:** If you see `.env` in the list:
```bash
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
```

### Step 4: Create First Commit

```bash
git commit -m "Initial commit: Student Q&A Chatbot v1.0"
```

### Step 5: Connect to GitHub

**Replace `yourusername` with your GitHub username:**

```bash
git remote add origin https://github.com/yourusername/Student_QA_Chatbot.git
git branch -M main
git push -u origin main
```

**If prompted for credentials:**
- Username: your GitHub username
- Password: your GitHub Personal Access Token (not your password!)

**Create Personal Access Token:**
1. GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Generate new token (classic)
3. Select: `repo` scope
4. Copy token and save securely

### Step 6: Verify on GitHub

1. Go to https://github.com/yourusername/Student_QA_Chatbot
2. You should see all your files
3. **Verify `.env` is NOT there!**
4. Check README displays correctly

---

## Heroku Deployment

### Step 1: Install Heroku CLI

**Download and install:**
- https://devcenter.heroku.com/articles/heroku-cli

**Verify installation:**
```bash
heroku --version
```

### Step 2: Login to Heroku

```bash
heroku login
```

**This will:**
- Open browser
- Login to Heroku account
- Authenticate CLI

### Step 3: Create Heroku App

```bash
heroku create uvu-student-chatbot
```

**Or let Heroku generate name:**
```bash
heroku create
```

**Note the app URL:**
```
https://uvu-student-chatbot.herokuapp.com
```

### Step 4: Add PostgreSQL Database

**Heroku doesn't support SQLite, use PostgreSQL:**

```bash
heroku addons:create heroku-postgresql:essential-0
```

**Free tier available (up to 10,000 rows)**

**Verify database added:**
```bash
heroku config
```

You should see `DATABASE_URL` with PostgreSQL connection string.

### Step 5: Configure Environment Variables

**Set your environment variables on Heroku:**

```bash
# Set Mistral API Key
heroku config:set MISTRAL_API_KEY=your_mistral_api_key_here

# Set Secret Key
heroku config:set SECRET_KEY=your_generated_secret_key_here

# Verify
heroku config
```

**⚠️ DO NOT commit these to Git!**

### Step 6: Update Code for PostgreSQL

**Heroku automatically sets `DATABASE_URL`. Update `database.py`:**

Already configured! Check line 14:
```python
database_url = os.getenv('DATABASE_URL', 'sqlite:///chatbot.db')
```

Heroku will use PostgreSQL automatically.

### Step 7: Create Procfile

**Already exists in your project!** Verify it contains:

```
web: python web_app_sql.py
```

**If missing, create it:**
```bash
echo "web: python web_app_sql.py" > Procfile
```

### Step 8: Update `web_app_sql.py` for Production

**Make sure these lines exist (they should):**

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

**Set `debug=False` for production!**

### Step 9: Commit Changes (if any)

```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push origin main
```

### Step 10: Deploy to Heroku

```bash
git push heroku main
```

**This will:**
- Upload code to Heroku
- Install dependencies
- Build application
- Start web dyno

**Watch the build output!** Look for:
```
remote: -----> Launching...
remote:        Released v3
remote:        https://uvu-student-chatbot.herokuapp.com/ deployed to Heroku
```

### Step 11: Scale Web Dyno

```bash
heroku ps:scale web=1
```

### Step 12: Initialize Database

**Run migration on Heroku:**

```bash
heroku run python migrate_to_sql.py
```

**Choose option 2** to create admin user.

**Or use Heroku console:**
```bash
heroku run bash
python migrate_to_sql.py
exit
```

### Step 13: Open Your App!

```bash
heroku open
```

**Or visit:**
```
https://uvu-student-chatbot.herokuapp.com
```

**🎉 Your chatbot is now live!**

---

## Environment Configuration

### Required Environment Variables

**On Heroku:**

```bash
# Already set by Heroku
DATABASE_URL=postgres://...

# You need to set these
MISTRAL_API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

**Set additional variables:**

```bash
# Session security (production)
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set SESSION_COOKIE_HTTPONLY=True
heroku config:set SESSION_COOKIE_SAMESITE=Lax

# Flask environment
heroku config:set FLASK_ENV=production
```

**View all config:**
```bash
heroku config
```

---

## Database Setup (PostgreSQL)

### PostgreSQL vs SQLite

**Differences:**
- **SQLite:** File-based, local only
- **PostgreSQL:** Server-based, production-ready

**Your app supports both!** It automatically detects the environment.

### Verify Database Connection

```bash
# Check database URL
heroku config:get DATABASE_URL

# Access database console
heroku pg:psql

# In psql:
\dt  # List tables
SELECT COUNT(*) FROM "user";  # Count users
\q   # Quit
```

### Backup Database

```bash
# Create backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download

# List backups
heroku pg:backups
```

### Reset Database (if needed)

```bash
heroku pg:reset DATABASE_URL
heroku run python migrate_to_sql.py
```

---

## Post-Deployment Verification

### ✅ Checklist

**Test these features:**

- [ ] Homepage loads
- [ ] Can ask questions as guest
- [ ] Can register new account
- [ ] Can login with account
- [ ] Can view conversation history
- [ ] Admin login works
- [ ] Admin can view users
- [ ] Admin can edit data
- [ ] API endpoints work (`/api/v1/`)
- [ ] HTTPS enabled (automatic on Heroku)

### Test Admin Portal

1. Go to `https://your-app.herokuapp.com/admin`
2. Login with admin credentials
3. Verify you can:
   - View users
   - View conversations
   - Edit data
   - Export data

### Test API

```bash
# Get API info
curl https://your-app.herokuapp.com/api/v1/

# Or in browser
https://your-app.herokuapp.com/api/v1/
```

---

## Monitoring & Logs

### View Logs

```bash
# View recent logs
heroku logs --tail

# View last 200 lines
heroku logs -n 200

# Filter for errors
heroku logs --tail | grep ERROR
```

### Monitor Application

```bash
# Check dyno status
heroku ps

# View app info
heroku info

# Open dashboard
heroku dashboard
```

### Performance

**Heroku metrics (paid plans):**
```bash
heroku logs --ps web
```

**Or view in Heroku Dashboard:**
- https://dashboard.heroku.com/apps/uvu-student-chatbot

---

## Updating Your App

### Deploy Changes

**Workflow:**

1. **Make changes locally**
2. **Test thoroughly**
3. **Commit to Git:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
4. **Deploy to Heroku:**
   ```bash
   git push heroku main
   ```

**Heroku automatically:**
- Rebuilds app
- Restarts dynos
- Updates live site

### Rollback if Needed

```bash
# View releases
heroku releases

# Rollback to previous version
heroku rollback

# Or specific version
heroku rollback v15
```

---

## Troubleshooting

### App Crashes on Heroku

**Check logs:**
```bash
heroku logs --tail
```

**Common issues:**
- Missing environment variables
- Import errors
- Database connection issues
- Port configuration

**Fix:**
```bash
# Restart dynos
heroku restart

# Check buildpack
heroku buildpacks

# Should be: heroku/python
```

### Database Connection Errors

**Check:**
```bash
heroku config:get DATABASE_URL
```

**Fix database issues:**
```bash
# Restart database
heroku pg:restart

# Reset database
heroku pg:reset DATABASE_URL
heroku run python migrate_to_sql.py
```

### Static Files Not Loading

**Heroku serves static files differently.**

**Solution:** Add whitenoise:

```bash
# Add to requirements.txt
echo "whitenoise" >> requirements.txt

# In web_app_sql.py, after app creation:
from whitenoise import WhiteNoise
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')

# Commit and deploy
git add .
git commit -m "Add whitenoise for static files"
git push heroku main
```

### Slow Performance

**Upgrade dyno (paid):**
```bash
heroku ps:resize web=hobby
```

**Or optimize code:**
- Add caching
- Reduce API calls
- Optimize database queries

### "Application Error"

**Check logs immediately:**
```bash
heroku logs --tail
```

**Common causes:**
- Missing dependencies in `requirements.txt`
- Syntax errors
- Missing environment variables
- Database not initialized

---

## Security in Production

### ✅ Production Security Checklist

- [ ] SECRET_KEY changed from default
- [ ] Admin password changed from default
- [ ] Debug mode OFF (`debug=False`)
- [ ] HTTPS enabled (automatic on Heroku)
- [ ] SESSION_COOKIE_SECURE=True
- [ ] Environment variables not in code
- [ ] `.env` not in Git repository
- [ ] Database backups configured
- [ ] Monitoring enabled

### Update Environment Variables

```bash
# Update any variable
heroku config:set VARIABLE_NAME=new_value

# Remove variable
heroku config:unset VARIABLE_NAME
```

---

## Cost & Scaling

### Free Tier

**Heroku Free Tier includes:**
- 550-1000 dyno hours/month
- Essential-0 PostgreSQL (10,000 rows)
- HTTPS automatic
- Custom domain support

**Limitations:**
- Sleeps after 30 min inactivity
- Wakes on first request (slow)
- 512 MB RAM

### Upgrade Options

**Hobby Dyno ($7/month):**
```bash
heroku ps:resize web=hobby
```

**Hobby PostgreSQL ($5/month):**
- 10 million rows
- Better performance

**Professional tiers available for high traffic**

---

## Custom Domain (Optional)

### Add Custom Domain

1. **Get domain** (GoDaddy, Namecheap, etc.)

2. **Add to Heroku:**
   ```bash
   heroku domains:add chatbot.yourdomain.com
   ```

3. **Configure DNS:**
   - Add CNAME record
   - Point to Heroku DNS target

4. **Enable SSL:**
   ```bash
   heroku certs:auto:enable
   ```

**Heroku automatically provides SSL certificate!**

---

## 🎉 Deployment Complete!

### You've Successfully Deployed Your Chatbot!

**Your app is now:**
- ✅ Live on the internet
- ✅ Accessible 24/7
- ✅ Using PostgreSQL database
- ✅ HTTPS secured
- ✅ Version controlled with Git
- ✅ Easy to update

### Next Steps

1. **Share the URL** with students
2. **Monitor logs** regularly
3. **Setup backups** (automated)
4. **Integrate with Canvas** (see CANVAS_INTEGRATION.md)
5. **Monitor usage** and costs
6. **Update** as needed

### URLs to Save

- **App URL:** https://uvu-student-chatbot.herokuapp.com
- **Admin Portal:** https://uvu-student-chatbot.herokuapp.com/admin
- **API:** https://uvu-student-chatbot.herokuapp.com/api/v1
- **GitHub Repo:** https://github.com/yourusername/Student_QA_Chatbot
- **Heroku Dashboard:** https://dashboard.heroku.com/apps/uvu-student-chatbot

---

## Quick Reference

### Common Commands

```bash
# Deploy updates
git push heroku main

# View logs
heroku logs --tail

# Restart app
heroku restart

# Access console
heroku run python

# Database backup
heroku pg:backups:capture

# Check status
heroku ps

# View config
heroku config
```

---

**Deployment Guide Version:** 1.0  
**Platform:** Heroku  
**Database:** PostgreSQL  
**Status:** Production Ready ✅

**Congratulations on deploying your chatbot!** 🚀
