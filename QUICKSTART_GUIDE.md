# Quick Start Guide
## Student Q&A Chatbot - Get Started in 10 Minutes

**This guide will get your chatbot running locally in 10 minutes!**

---

## 📋 Prerequisites

Before you start, make sure you have:
- ✅ Python 3.8 or higher
- ✅ Git (optional, for version control)
- ✅ Text editor (VS Code, PyCharm, etc.)
- ✅ Mistral AI API key ([get one free](https://console.mistral.ai/))

---

## 🚀 Quick Setup (10 Minutes)

### Step 1: Get the Project (1 minute)

**Option A: Download ZIP**
1. Download project ZIP file
2. Extract to your desired location
3. Open terminal in the extracted folder

**Option B: Clone from GitHub**
```bash
git clone https://github.com/yourusername/Student_QA_Chatbot.git
cd Student_QA_Chatbot
```

### Step 2: Create Virtual Environment (2 minutes)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

**This installs:**
- Flask (web framework)
- SQLAlchemy (database)
- Mistral AI (chatbot)
- And other dependencies

### Step 4: Configure Environment (2 minutes)

Create a file named `.env` in the project root:

```bash
# Windows
notepad .env

# Mac/Linux
nano .env
```

Add these lines (replace with your actual API key):

```env
MISTRAL_API_KEY=your_mistral_api_key_here
SECRET_KEY=your_secret_key_here
```

**Get your Mistral API key:**
1. Go to https://console.mistral.ai/
2. Sign up (free tier available)
3. Create API key
4. Copy and paste into `.env`

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste as SECRET_KEY in `.env`

### Step 5: Initialize Database (1 minute)

```bash
python migrate_to_sql.py
```

**Choose option 2** to create admin user when prompted.

**Set admin password:**
- Email: `admin@uvu.edu` (default)
- Password: Create a strong password (min 12 characters)

### Step 6: Run the Application (1 minute)

```bash
python web_app_sql.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 7: Access the Chatbot (1 minute)

Open your browser and go to:
```
http://localhost:5000
```

**You should see the chatbot interface!** 🎉

---

## 🎯 First Steps

### Test as Guest

1. Click "Continue as Guest" on homepage
2. Ask a question: "What is INFO 6200?"
3. Get AI-powered answer!

### Register an Account

1. Click "Register" in top navigation
2. Fill in:
   - Email: your@email.com
   - Password: (min 6 characters)
   - First Name, Last Name
   - Student ID
   - Course Section
   - Semester
3. Click "Register"
4. You're now logged in!

### Ask Questions

1. Type your question in the text box
2. Click "Ask" or press Enter
3. Get instant AI answer
4. View in conversation history

### Access Admin Portal

1. Go to `http://localhost:5000/admin`
2. Login with admin credentials
3. Explore admin features:
   - View all users
   - View all conversations
   - Edit/delete data
   - Export data

---

## 🔍 Verify Everything Works

### ✅ Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] `.env` file created with API keys
- [ ] Database initialized
- [ ] App running on http://localhost:5000
- [ ] Can access chatbot interface
- [ ] Can ask questions as guest
- [ ] Can register new account
- [ ] Can login with account
- [ ] Can access admin portal

---

## 🛠️ Troubleshooting

### "ModuleNotFoundError"

**Problem:** Missing dependencies  
**Fix:**
```bash
pip install -r requirements.txt
```

### "Mistral API error"

**Problem:** Invalid or missing API key  
**Fix:**
1. Check `.env` file exists
2. Verify MISTRAL_API_KEY is correct
3. Try generating new key at https://console.mistral.ai/

### "Database not found"

**Problem:** Database not initialized  
**Fix:**
```bash
python migrate_to_sql.py
```
Choose option 2 to create fresh database

### "Port already in use"

**Problem:** Another app using port 5000  
**Fix:**
```bash
# Kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in web_app_sql.py
app.run(port=5001)
```

### "Admin login not working"

**Problem:** Wrong credentials or admin not created  
**Fix:**
```bash
python migrate_to_sql.py
```
Choose option 2, re-create admin user

---

## 📁 Project Structure

```
Student_QA_Chatbot/
├── web_app_sql.py          # Main application (run this)
├── models.py               # Database models
├── admin.py                # Admin portal
├── api.py                  # RESTful API
├── chatbot.py              # AI chatbot logic
├── migrate_to_sql.py       # Database setup
├── security_setup.py       # Security configuration
├── test_api.py             # API testing
├── .env                    # Environment variables (YOU CREATE THIS)
├── requirements.txt        # Dependencies
├── templates/              # HTML templates
├── static/                 # CSS, JavaScript
├── corpus/                 # Course materials
└── instance/               # Database files (auto-created)
```

---

## 🎓 Next Steps

### Option 1: Use Locally
- Start chatbot: `python web_app_sql.py`
- Use for course questions
- Build conversation history
- Export data as needed

### Option 2: Deploy to Production
- See `DEPLOYMENT_GUIDE.md` for:
  - GitHub setup
  - Heroku deployment
  - PostgreSQL configuration
  - HTTPS setup

### Option 3: Integrate with Canvas
- See `CANVAS_INTEGRATION.md` for:
  - iFrame embedding
  - JavaScript widgets
  - LTI integration

---

## 🔒 Security Recommendations

**Before sharing or deploying:**

1. **Change SECRET_KEY** (if using default)
   ```bash
   python security_setup.py
   ```

2. **Change admin password**
   ```bash
   python security_setup.py
   ```

3. **Never commit `.env` to Git**
   - Already in `.gitignore`
   - Keep API keys secret

4. **Review security settings**
   - See `SECURITY_QUICK_REFERENCE.md`

---

## 📖 Learn More

### Essential Documentation
- **README.md** - Full project overview
- **PROJECT_SUMMARY.md** - Complete feature list
- **DEPLOYMENT_GUIDE.md** - Deploy to Heroku
- **API_DOCUMENTATION.md** - API reference

### Quick References
- **API_QUICK_REFERENCE.md** - API cheat sheet
- **SECURITY_QUICK_REFERENCE.md** - Security tips
- **ADMIN_CRUD_REFERENCE.md** - Admin operations

### Integration Guides
- **CANVAS_INTEGRATION.md** - Canvas LMS setup
- **SECURITY_CONFIGURATION.md** - Advanced security

---

## 🆘 Getting Help

### Common Questions

**Q: How do I stop the server?**  
A: Press `CTRL+C` in the terminal

**Q: How do I restart the server?**  
A: Press `CTRL+C`, then run `python web_app_sql.py` again

**Q: Can I change the admin email?**  
A: Yes, edit in `migrate_to_sql.py` or database directly

**Q: Where is my data stored?**  
A: In `instance/chatbot.db` (SQLite file)

**Q: How do I reset everything?**  
A: Delete `instance/chatbot.db` and run `python migrate_to_sql.py`

**Q: Can I add more course materials?**  
A: Yes, add PDFs/DOCX to `corpus/` folder

### Support Resources
- Project documentation in `/docs`
- Check `TROUBLESHOOTING.md`
- Review error messages
- Check Python version (3.8+)

---

## ✅ You're All Set!

Your chatbot is now running! Here's what you can do:

✅ **Ask Questions** - Get AI-powered answers  
✅ **Register Account** - Save conversation history  
✅ **Admin Portal** - Manage users and data  
✅ **API Access** - Programmatic access  
✅ **Export Data** - Download conversations  

---

## 🎉 Success!

If you've made it here, your Student Q&A Chatbot is **up and running**!

**Next Steps:**
1. Try asking some questions
2. Explore the admin portal
3. Check out the API at `http://localhost:5000/api/v1/`
4. When ready, see `DEPLOYMENT_GUIDE.md` to deploy to production

**Enjoy your AI-powered chatbot!** 🚀

---

**Quick Start Version:** 1.0  
**Estimated Setup Time:** 10 minutes  
**Difficulty:** ⭐ Easy  
**Status:** Production Ready ✅
