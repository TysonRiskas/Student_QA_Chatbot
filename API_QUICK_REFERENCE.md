# API Quick Reference Card
## Student Q&A Chatbot API v1.0

**Print this for quick API reference!**

---

## 🔗 Base URL

```
Development: http://localhost:5000/api/v1
Production:  https://your-app.herokuapp.com/api/v1
```

---

## 🔐 Authentication

**Method:** Session-based (login via web interface first)

**Login:**
```bash
POST /login
  email: student@uvu.edu
  password: your_password
```

**Session:** Cookie automatically included in subsequent requests

---

## 📡 Endpoints

### 1. API Info
```
GET /api/v1/
Auth: None
Returns: API information and endpoint list
```

### 2. Get Conversations
```
GET /api/v1/conversations?page=1&per_page=20
Auth: User
Returns: List of user's conversations with pagination
```

### 3. Get Single Conversation
```
GET /api/v1/conversations/<id>
Auth: User (own data only)
Returns: Specific conversation details
```

### 4. Ask Question
```
POST /api/v1/ask
Auth: User
Body: {"question": "Your question here"}
Returns: AI answer and conversation ID
```

### 5. Get Statistics
```
GET /api/v1/stats
Auth: User
Returns: User statistics (total conversations, recent activity)
```

### 6. Get Users (Admin)
```
GET /api/v1/users?search=john&page=1
Auth: Admin
Returns: List of all users with search/pagination
```

### 7. Get User (Admin)
```
GET /api/v1/users/<id>
Auth: Admin
Returns: Specific user details
```

---

## 📊 Response Format

### Success (200/201)
```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2025-11-18T21:00:00.000Z"
}
```

### Error (400/401/403/404/500)
```json
{
  "error": "Error type",
  "message": "Detailed description",
  "status": 404
}
```

### Paginated
```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 45,
    "total_pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## 🔢 HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Not logged in |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Internal error |

---

## 💻 Quick Examples

### Python

```python
import requests

# Login
session = requests.Session()
session.post('http://localhost:5000/login', data={
    'email': 'student@uvu.edu',
    'password': 'password'
})

# Get conversations
resp = session.get('http://localhost:5000/api/v1/conversations')
print(resp.json())

# Ask question
resp = session.post('http://localhost:5000/api/v1/ask', 
    json={'question': 'What is the syllabus?'})
print(resp.json()['data']['answer'])
```

### JavaScript

```javascript
// Get stats (after login)
fetch('http://localhost:5000/api/v1/stats')
  .then(r => r.json())
  .then(data => console.log(data));

// Ask question
fetch('http://localhost:5000/api/v1/ask', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({question: 'When is the exam?'})
})
  .then(r => r.json())
  .then(data => console.log(data.data.answer));
```

### cURL

```bash
# Login
curl -c cookies.txt -X POST http://localhost:5000/login \
  -d "email=student@uvu.edu" -d "password=pass"

# Get conversations
curl -b cookies.txt http://localhost:5000/api/v1/conversations

# Ask question
curl -b cookies.txt -X POST http://localhost:5000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the midterm date?"}'
```

---

## 🎓 Canvas Integration

### iFrame (Easiest)
```html
<iframe src="https://your-app.herokuapp.com" 
        width="100%" height="800px"></iframe>
```

### JavaScript Widget
```javascript
fetch('https://your-app.herokuapp.com/api/v1/conversations')
  .then(r => r.json())
  .then(data => {
    // Display conversations
    data.data.forEach(conv => {
      console.log(conv.question, conv.answer);
    });
  });
```

---

## 🧪 Testing

### Run Test Suite
```bash
python test_api.py
```

### Manual Test
```bash
# Start app
python web_app_sql.py

# In another terminal
curl http://localhost:5000/api/v1/
```

---

## 🔒 Security

**All endpoints protected except:**
- `GET /api/v1/` (API info)

**User endpoints:**
- Require user login
- Return only user's own data

**Admin endpoints:**
- Require admin login
- Return all data

**Data isolation:**
- Users cannot access other users' data
- Database queries filtered by user_id

---

## ⚠️ Common Issues

### "Authentication required"
**Fix:** Login first via `/login`

### "Not found"
**Fix:** Check ID exists and user has access

### CORS error
**Fix:** Configure Flask-CORS for your domain

### Empty data array
**Fix:** User has no conversations yet

---

## 📋 Pagination Parameters

```
?page=1           # Page number (default: 1)
?per_page=20      # Items per page (default: 20, max: 100)
?search=term      # Search term (users endpoint only)
```

---

## 🎯 Best Practices

1. **Always check status code** before processing data
2. **Handle errors gracefully** with try-catch
3. **Use pagination** for large datasets (per_page=20-50)
4. **Cache responses** when appropriate
5. **Validate input** before sending to API
6. **Use HTTPS** in production
7. **Log API calls** for debugging

---

## 📞 Quick Help

**Documentation:**
- API_DOCUMENTATION.md - Full reference
- CANVAS_INTEGRATION.md - Canvas guide
- test_api.py - Example code

**Support:**
- Check response error message
- Review status code
- Check authentication
- Verify endpoint URL

---

## 🔗 Useful URLs

**Development:**
- API: http://localhost:5000/api/v1
- Login: http://localhost:5000/login
- Admin: http://localhost:5000/admin/login

**Testing:**
- Info: http://localhost:5000/api/v1/
- Conversations: http://localhost:5000/api/v1/conversations
- Stats: http://localhost:5000/api/v1/stats

---

## 📊 Feature Summary

| Feature | Status |
|---------|--------|
| RESTful Design | ✅ |
| JSON Responses | ✅ |
| Authentication | ✅ |
| Pagination | ✅ |
| Error Handling | ✅ |
| Data Isolation | ✅ |
| Admin Access | ✅ |
| HTTPS Ready | ✅ |
| Canvas Ready | ✅ |
| Documented | ✅ |

---

**API Version:** 1.0  
**Base Path:** `/api/v1`  
**Format:** JSON  
**Auth:** Session  
**Status:** Production Ready ✅

---

**Keep this card handy for quick API reference!**
