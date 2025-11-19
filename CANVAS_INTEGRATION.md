# Canvas LMS Integration Guide
## Deploying Student Q&A Chatbot to Canvas

This guide shows you how to integrate the Student Q&A Chatbot API into your Canvas course shell.

---

## Table of Contents

1. [Overview](#overview)
2. [Integration Methods](#integration-methods)
3. [Method 1: Embedded iFrame](#method-1-embedded-iframe)
4. [Method 2: JavaScript Widget](#method-2-javascript-widget)
5. [Method 3: External Tool (LTI)](#method-3-external-tool-lti)
6. [Authentication & Session Management](#authentication--session-management)
7. [Example Implementations](#example-implementations)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The Student Q&A Chatbot can be integrated into Canvas in several ways:

**Benefits:**
- Students access chatbot directly in Canvas
- No separate login required (uses Canvas authentication)
- Course-specific deployment
- Consistent student experience

**Requirements:**
- Deployed chatbot application (Heroku/AWS)
- HTTPS enabled
- Canvas admin or instructor permissions

---

## Integration Methods

### Comparison

| Method | Difficulty | Features | Best For |
|--------|-----------|----------|----------|
| iFrame | Easy | Full interface | Quick deployment |
| JavaScript Widget | Medium | Custom UI | Embedded experience |
| LTI External Tool | Hard | SSO, deep integration | Production use |

---

## Method 1: Embedded iFrame

**Difficulty:** ⭐ Easy  
**Time:** 5 minutes  
**Best for:** Quick deployment and testing

### Step 1: Deploy Your Application

First, deploy to Heroku or another platform with HTTPS.

```bash
# Deploy to Heroku
heroku create uvu-chatbot
git push heroku main
heroku open
```

Your app URL: `https://uvu-chatbot.herokuapp.com`

### Step 2: Create Canvas Page

1. Go to your Canvas course
2. Click **Pages** → **+ Page**
3. Enter page title: "INFO 6200 AI Chatbot"
4. Switch to **HTML Editor** (click `<>` icon)

### Step 3: Add iFrame Code

```html
<h2>INFO 6200 Student Q&A Chatbot</h2>
<p>Ask questions about the course and get instant AI-powered answers!</p>

<iframe 
  src="https://uvu-chatbot.herokuapp.com" 
  width="100%" 
  height="800px" 
  frameborder="0"
  allow="clipboard-write"
  title="Student Q&A Chatbot">
</iframe>

<p><small>Tip: Login with your UVU email to save your conversation history.</small></p>
```

### Step 4: Publish

1. Click **Save**
2. Click **Publish**
3. Add to course navigation if desired

**Result:** Students can now access the full chatbot interface within Canvas!

---

## Method 2: JavaScript Widget

**Difficulty:** ⭐⭐ Medium  
**Time:** 30 minutes  
**Best for:** Custom integration with Canvas UI

### Implementation

Create a custom widget that shows conversation history:

```html
<!-- Canvas Page HTML Editor -->
<div id="chatbot-container">
  <h2>My Q&A History</h2>
  <div id="loading">Loading your conversations...</div>
  <div id="conversations"></div>
  <div id="ask-section" style="display:none;">
    <h3>Ask a Question</h3>
    <textarea id="question" rows="3" style="width:100%;"></textarea>
    <button onclick="askQuestion()">Submit Question</button>
  </div>
</div>

<style>
  #chatbot-container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background: #f9f9f9;
    border-radius: 8px;
  }
  .conversation {
    background: white;
    padding: 15px;
    margin: 10px 0;
    border-left: 4px solid #2196F3;
    border-radius: 4px;
  }
  .question {
    font-weight: bold;
    color: #1976D2;
    margin-bottom: 8px;
  }
  .answer {
    color: #333;
  }
  .timestamp {
    font-size: 12px;
    color: #999;
    margin-top: 8px;
  }
</style>

<script>
  const API_BASE = 'https://uvu-chatbot.herokuapp.com/api/v1';
  
  // Load conversations when page loads
  window.addEventListener('load', loadConversations);
  
  async function loadConversations() {
    try {
      // Fetch conversations from API
      const response = await fetch(`${API_BASE}/conversations`, {
        credentials: 'include'  // Include session cookies
      });
      
      const loading = document.getElementById('loading');
      const container = document.getElementById('conversations');
      
      if (!response.ok) {
        loading.textContent = 'Please login to the chatbot first to view your history.';
        loading.innerHTML += '<br><a href="https://uvu-chatbot.herokuapp.com/login" target="_blank">Click here to login</a>';
        return;
      }
      
      const data = await response.json();
      loading.style.display = 'none';
      
      if (data.data.length === 0) {
        container.innerHTML = '<p>No conversations yet. Ask your first question below!</p>';
      } else {
        container.innerHTML = data.data.map(conv => `
          <div class="conversation">
            <div class="question">Q: ${conv.question}</div>
            <div class="answer">A: ${conv.answer}</div>
            <div class="timestamp">${new Date(conv.timestamp).toLocaleString()}</div>
          </div>
        `).join('');
      }
      
      // Show ask section
      document.getElementById('ask-section').style.display = 'block';
      
    } catch (error) {
      document.getElementById('loading').textContent = 'Error loading conversations: ' + error.message;
    }
  }
  
  async function askQuestion() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();
    
    if (!question) {
      alert('Please enter a question');
      return;
    }
    
    try {
      const response = await fetch(`${API_BASE}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ question })
      });
      
      if (!response.ok) {
        alert('Error submitting question. Please login first.');
        return;
      }
      
      const data = await response.json();
      
      // Add new conversation to display
      const container = document.getElementById('conversations');
      const newConv = document.createElement('div');
      newConv.className = 'conversation';
      newConv.innerHTML = `
        <div class="question">Q: ${data.data.question}</div>
        <div class="answer">A: ${data.data.answer}</div>
        <div class="timestamp">${new Date(data.data.timestamp).toLocaleString()}</div>
      `;
      container.insertBefore(newConv, container.firstChild);
      
      // Clear input
      questionInput.value = '';
      
      alert('Question submitted successfully!');
      
    } catch (error) {
      alert('Error: ' + error.message);
    }
  }
</script>
```

### Step-by-Step Setup

1. **Create Canvas Page**
   - Pages → + Page
   - Title: "Q&A with AI"

2. **Add HTML Code**
   - Switch to HTML Editor
   - Paste the code above
   - Update API_BASE URL to your deployed app

3. **Configure CORS** (in your Flask app)
   ```python
   from flask_cors import CORS
   
   CORS(app, resources={
       r"/api/*": {
           "origins": ["https://uvu.instructure.com"],
           "supports_credentials": True
       }
   })
   ```

4. **Test**
   - Publish the page
   - Have students login to chatbot first
   - Then visit Canvas page

---

## Method 3: External Tool (LTI)

**Difficulty:** ⭐⭐⭐ Advanced  
**Time:** 2-4 hours  
**Best for:** Production deployment with SSO

### Overview

LTI (Learning Tools Interoperability) enables:
- Single Sign-On (SSO)
- Automatic user creation
- Grade passback (if needed)
- Deep Canvas integration

### Requirements

- Flask-LTI library
- Consumer key and secret
- SSL certificate (HTTPS)

### Installation

```bash
pip install PyLTI Flask-LTI
```

### Implementation

```python
# lti_config.py
from pylti.flask import lti
from flask import Flask, session

app.config.update({
    'SECRET_KEY': os.getenv('SECRET_KEY'),
    'PYLTI_CONFIG': {
        'consumers': {
            os.getenv('LTI_CONSUMER_KEY'): {
                'secret': os.getenv('LTI_CONSUMER_SECRET')
            }
        },
        'roles': {
            'admin': ['Administrator', 'Instructor'],
            'student': ['Student', 'Learner']
        }
    }
})

@app.route('/lti/launch', methods=['POST'])
@lti(request='initial', app=app)
def lti_launch(lti=lti):
    """Handle LTI launch from Canvas."""
    
    # Get user info from LTI params
    user_id = lti.user_id
    email = lti.lis_person_contact_email_primary
    name = lti.lis_person_name_full
    
    # Create or update user in database
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            email=email,
            first_name=name.split()[0],
            last_name=' '.join(name.split()[1:]),
            student_id=user_id
        )
        user.set_password(os.urandom(24).hex())  # Random password
        db.session.add(user)
        db.session.commit()
    
    # Log user in
    session['user_id'] = user.id
    session['user_info'] = user.to_dict()
    
    # Redirect to chatbot
    return redirect(url_for('index'))
```

### Canvas Configuration

1. **Settings → Apps → View App Configurations**
2. **+ App**
3. **Configuration Type:** By URL or Manual
4. Fill in:
   - **Name:** INFO 6200 Chatbot
   - **Consumer Key:** `your_key`
   - **Shared Secret:** `your_secret`
   - **Launch URL:** `https://your-app.com/lti/launch`
   - **Privacy:** Public

5. **Submit**

---

## Authentication & Session Management

### Option 1: Manual Login

Students login separately:

1. Visit chatbot URL
2. Register/login
3. Return to Canvas
4. Canvas iFrame shows logged-in state

**Pros:** Simple, no configuration  
**Cons:** Requires separate login

### Option 2: Session Sharing

Use same domain for both:

1. Deploy chatbot to: `chatbot.uvu.edu`
2. Canvas at: `canvas.uvu.edu`
3. Share session cookies across subdomains

**Pros:** Seamless experience  
**Cons:** Requires domain control

### Option 3: LTI SSO

Canvas passes authentication:

1. Student clicks link in Canvas
2. LTI launches chatbot with user info
3. Chatbot creates session automatically
4. No separate login needed

**Pros:** Best user experience  
**Cons:** Complex setup

---

## Example Implementations

### Example 1: Simple History Display

```html
<!-- Show last 5 conversations -->
<div id="recent-chats"></div>

<script>
fetch('https://your-app.com/api/v1/conversations?per_page=5')
  .then(r => r.json())
  .then(data => {
    const html = data.data.map(c => 
      `<p><strong>${c.question}</strong><br>${c.answer}</p>`
    ).join('<hr>');
    document.getElementById('recent-chats').innerHTML = html;
  });
</script>
```

### Example 2: Interactive Chat Interface

```html
<div id="chat-box">
  <div id="messages"></div>
  <input type="text" id="user-input" placeholder="Ask a question...">
  <button onclick="sendMessage()">Send</button>
</div>

<script>
async function sendMessage() {
  const input = document.getElementById('user-input');
  const question = input.value;
  
  const response = await fetch('https://your-app.com/api/v1/ask', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    credentials: 'include',
    body: JSON.stringify({question})
  });
  
  const data = await response.json();
  
  document.getElementById('messages').innerHTML += `
    <div><strong>You:</strong> ${question}</div>
    <div><strong>AI:</strong> ${data.data.answer}</div>
  `;
  
  input.value = '';
}
</script>
```

---

## Troubleshooting

### "No conversations found"
**Cause:** Student not logged in  
**Fix:** Add login link to Canvas page

### CORS Error
**Cause:** Cross-origin requests blocked  
**Fix:** Install Flask-CORS and configure

### Session not persisting
**Cause:** Cookies blocked by browser  
**Fix:** Use LTI or same-origin deployment

### iFrame not loading
**Cause:** X-Frame-Options header  
**Fix:** Configure Flask to allow framing from Canvas

```python
@app.after_request
def after_request(response):
    response.headers['X-Frame-Options'] = 'ALLOW-FROM https://uvu.instructure.com'
    return response
```

---

## Production Checklist

Before deploying to Canvas:

- [ ] App deployed with HTTPS
- [ ] CORS configured for Canvas domain
- [ ] Error handling in place
- [ ] Session management tested
- [ ] Mobile responsive
- [ ] Tested with student accounts
- [ ] Documented for students
- [ ] Support plan in place

---

## Support

**Canvas Integration Issues:**
- Check Canvas developer docs
- Contact Canvas support
- Review LTI specifications

**API Issues:**
- See API_DOCUMENTATION.md
- Check application logs
- Review SECURITY_AUDIT.md

---

**Integration Guide Version:** 1.0  
**Last Updated:** November 18, 2025  
**Status:** Ready for Canvas Deployment
