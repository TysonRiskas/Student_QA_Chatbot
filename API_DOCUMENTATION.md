# API Documentation
## Student Q&A Chatbot RESTful API v1.0

**Base URL:** `http://localhost:5000/api/v1`  
**Version:** 1.0  
**Authentication:** Session-based (login via web interface first)

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Response Format](#response-format)
4. [Endpoints](#endpoints)
5. [Error Codes](#error-codes)
6. [Examples](#examples)
7. [Canvas Integration](#canvas-integration)

---

## Overview

The Student Q&A Chatbot API provides programmatic access to chatbot data and functionality. It follows RESTful principles and returns JSON responses.

**Key Features:**
- Get conversation history
- Submit questions to AI chatbot
- View user statistics
- Admin access to all users (admin only)
- Pagination support
- Proper HTTP status codes

---

## Authentication

### Session-Based Authentication

The API uses session-based authentication. Users must login via the web interface before making API calls.

**Login Process:**
1. Navigate to `http://localhost:5000/login`
2. Login with credentials
3. Session cookie is set
4. API calls now authenticated

**For Students:**
```
POST /login
email: student@uvu.edu
password: student_password
```

**For Admins:**
```
POST /admin/login
email: admin@uvu.edu
password: admin_password
```

**Note:** API calls use the same session as web interface.

---

## Response Format

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2025-11-18T21:00:00.000Z"
}
```

### Error Response

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "status": 400
}
```

### Paginated Response

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
  },
  "timestamp": "2025-11-18T21:00:00.000Z"
}
```

---

## Endpoints

### 1. API Information

**Endpoint:** `GET /api/v1/`  
**Description:** Get API information and available endpoints  
**Authentication:** Not required

**Response:**
```json
{
  "name": "Student Q&A Chatbot API",
  "version": "1.0",
  "description": "RESTful API for accessing chatbot data",
  "base_url": "/api/v1",
  "endpoints": { ... }
}
```

---

### 2. Get All Conversations (User)

**Endpoint:** `GET /api/v1/conversations`  
**Description:** Get all conversations for the authenticated user  
**Authentication:** Required (Student)

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20, max: 100)

**Request:**
```
GET /api/v1/conversations?page=1&per_page=20
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "question": "What is INFO 6200?",
      "answer": "INFO 6200 is a course on...",
      "session_id": "abc-123-def-456",
      "timestamp": "2025-11-18T10:30:00.000Z",
      "saved_at": "2025-11-18T10:30:00.000Z",
      "is_guest": false,
      "user_info": {
        "firstName": "John",
        "lastName": "Doe",
        "studentId": "12345",
        "email": "john@uvu.edu",
        "courseSection": "001",
        "semester": "Fall 2025",
        "is_registered": true
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 5,
    "total_pages": 1,
    "has_next": false,
    "has_prev": false
  },
  "timestamp": "2025-11-18T21:00:00.000Z"
}
```

---

### 3. Get Single Conversation

**Endpoint:** `GET /api/v1/conversations/<id>`  
**Description:** Get a specific conversation by ID  
**Authentication:** Required (Student - own data only)

**Request:**
```
GET /api/v1/conversations/1
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "question": "What is INFO 6200?",
    "answer": "INFO 6200 is a course on...",
    "session_id": "abc-123-def-456",
    "timestamp": "2025-11-18T10:30:00.000Z",
    "saved_at": "2025-11-18T10:30:00.000Z",
    "is_guest": false,
    "user_info": {
      "firstName": "John",
      "lastName": "Doe",
      "studentId": "12345",
      "email": "john@uvu.edu",
      "courseSection": "001",
      "semester": "Fall 2025",
      "is_registered": true
    }
  },
  "timestamp": "2025-11-18T21:00:00.000Z"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Not found",
  "message": "Conversation 999 not found or access denied",
  "status": 404
}
```

---

### 4. Ask a Question

**Endpoint:** `POST /api/v1/ask`  
**Description:** Submit a question to the AI chatbot  
**Authentication:** Required (Student)

**Request Body:**
```json
{
  "question": "What are the course requirements?"
}
```

**Request:**
```bash
curl -X POST http://localhost:5000/api/v1/ask \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"question": "What are the course requirements?"}'
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "conversation_id": 15,
    "question": "What are the course requirements?",
    "answer": "The course requirements for INFO 6200 include...",
    "timestamp": "2025-11-18T21:05:00.000Z"
  },
  "timestamp": "2025-11-18T21:05:00.000Z"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Bad request",
  "message": "Question field is required",
  "status": 400
}
```

---

### 5. Get User Statistics

**Endpoint:** `GET /api/v1/stats`  
**Description:** Get statistics for the authenticated user  
**Authentication:** Required (Student)

**Request:**
```
GET /api/v1/stats
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "john@uvu.edu",
      "first_name": "John",
      "last_name": "Doe",
      "student_id": "12345"
    },
    "statistics": {
      "total_conversations": 15,
      "conversations_last_7_days": 5,
      "member_since": "2025-09-01T08:00:00.000Z",
      "last_activity": "2025-11-18T10:30:00.000Z"
    }
  },
  "timestamp": "2025-11-18T21:00:00.000Z"
}
```

---

### 6. Get All Users (Admin Only)

**Endpoint:** `GET /api/v1/users`  
**Description:** Get all registered users  
**Authentication:** Required (Admin)

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20, max: 100)
- `search` (optional): Search term for email, name, or student ID

**Request:**
```
GET /api/v1/users?search=john&page=1
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "email": "john@uvu.edu",
      "firstName": "John",
      "lastName": "Doe",
      "studentId": "12345",
      "courseSection": "001",
      "semester": "Fall 2025",
      "isActive": true,
      "createdAt": "2025-09-01T08:00:00.000Z",
      "conversationCount": 15
    }
  ],
  "pagination": { ... },
  "search": "john",
  "timestamp": "2025-11-18T21:00:00.000Z"
}
```

**Response (403 Forbidden):**
```json
{
  "error": "Admin authentication required",
  "message": "Admin access only",
  "status": 403
}
```

---

### 7. Get Single User (Admin Only)

**Endpoint:** `GET /api/v1/users/<id>`  
**Description:** Get a specific user by ID  
**Authentication:** Required (Admin)

**Request:**
```
GET /api/v1/users/1
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "john@uvu.edu",
    "firstName": "John",
    "lastName": "Doe",
    "studentId": "12345",
    "courseSection": "001",
    "semester": "Fall 2025",
    "isActive": true,
    "createdAt": "2025-09-01T08:00:00.000Z",
    "conversationCount": 15
  },
  "timestamp": "2025-11-18T21:00:00.000Z"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Not found",
  "message": "User 999 not found",
  "status": 404
}
```

---

## Error Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 405 | Method Not Allowed | HTTP method not allowed |
| 500 | Internal Server Error | Server error occurred |

---

## Examples

### Example 1: Get Conversation History (Python)

```python
import requests

# Login first
session = requests.Session()
session.post('http://localhost:5000/login', data={
    'email': 'student@uvu.edu',
    'password': 'password123'
})

# Get conversations
response = session.get('http://localhost:5000/api/v1/conversations')
data = response.json()

for conversation in data['data']:
    print(f"Q: {conversation['question']}")
    print(f"A: {conversation['answer']}\n")
```

### Example 2: Ask a Question (Python)

```python
import requests

session = requests.Session()
session.post('http://localhost:5000/login', data={
    'email': 'student@uvu.edu',
    'password': 'password123'
})

# Ask question
response = session.post('http://localhost:5000/api/v1/ask', json={
    'question': 'What is the midterm date?'
})

result = response.json()
print(f"Answer: {result['data']['answer']}")
```

### Example 3: Get Statistics (JavaScript/Fetch)

```javascript
// Assuming already logged in via web interface

fetch('http://localhost:5000/api/v1/stats')
  .then(response => response.json())
  .then(data => {
    console.log('Total Conversations:', data.data.statistics.total_conversations);
    console.log('Last 7 Days:', data.data.statistics.conversations_last_7_days);
  });
```

### Example 4: Admin Get All Users (cURL)

```bash
# Login as admin first
curl -c cookies.txt -X POST http://localhost:5000/admin/login \
  -d "email=admin@uvu.edu" \
  -d "password=admin123"

# Get users
curl -b cookies.txt http://localhost:5000/api/v1/users?per_page=10
```

---

## Canvas Integration

### Embedding API in Canvas

The API is designed to be integrated with Canvas LMS. Here's how:

#### Option 1: External Tool (LTI)

Create a Canvas External Tool that communicates with the API:

1. **Canvas → Settings → Apps → Add App**
2. Configure tool URL: `https://your-app.herokuapp.com`
3. Use API endpoints to fetch/display data

#### Option 2: JavaScript Widget

Embed in Canvas page using JavaScript:

```html
<!-- In Canvas HTML Editor -->
<div id="chatbot-widget"></div>

<script>
// Fetch user's conversation history
fetch('https://your-app.herokuapp.com/api/v1/conversations')
  .then(response => response.json())
  .then(data => {
    const widget = document.getElementById('chatbot-widget');
    data.data.forEach(conv => {
      widget.innerHTML += `
        <div class="conversation">
          <strong>Q:</strong> ${conv.question}<br>
          <strong>A:</strong> ${conv.answer}
        </div>
      `;
    });
  });
</script>
```

#### Option 3: Canvas API Integration

Use Canvas API + Chatbot API together:

```python
# Get Canvas user info
canvas_user = canvas_api.get_user(user_id)

# Login to chatbot
session.post(f'{CHATBOT_URL}/login', data={
    'email': canvas_user['email'],
    'password': 'synced_password'
})

# Get chatbot stats
stats = session.get(f'{CHATBOT_URL}/api/v1/stats').json()

# Display in Canvas
canvas_api.create_content_item({
    'title': 'Your Q&A History',
    'content': render_stats(stats)
})
```

### Authentication Flow for Canvas

1. Student logs into Canvas
2. Canvas redirects to chatbot with OAuth/LTI
3. Chatbot creates session
4. Student uses embedded widget
5. Widget makes API calls with session

### CORS Configuration (if needed)

For cross-origin requests from Canvas:

```python
# Add to web_app_sql.py
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://uvu.instructure.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## Rate Limiting (Recommended)

For production, add rate limiting:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: session.get('user_id', 'anonymous')
)

@api_bp.route('/conversations')
@limiter.limit("60 per minute")
def get_conversations():
    # ...
```

---

## Best Practices

1. **Always check authentication** before making API calls
2. **Use pagination** for large datasets
3. **Handle errors gracefully** with try-catch
4. **Cache responses** when appropriate
5. **Use HTTPS** in production
6. **Validate input** on client side before submitting
7. **Store session cookies** securely
8. **Monitor API usage** with logging

---

## Testing the API

### Using cURL

```bash
# Login
curl -c cookies.txt -X POST http://localhost:5000/login \
  -d "email=student@uvu.edu" -d "password=password123"

# Get conversations
curl -b cookies.txt http://localhost:5000/api/v1/conversations

# Ask question
curl -b cookies.txt -X POST http://localhost:5000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the syllabus?"}'

# Get stats
curl -b cookies.txt http://localhost:5000/api/v1/stats
```

### Using Postman

1. Create a POST request to `/login`
2. Set body to form-data with email/password
3. Send request (captures session cookie)
4. Create GET request to `/api/v1/conversations`
5. Cookies automatically included
6. View JSON response

---

## Support & Resources

- **API Base URL:** `/api/v1/`
- **Documentation:** This file
- **Source Code:** `api.py`
- **Issues:** Contact system administrator

---

**API Version:** 1.0  
**Last Updated:** November 18, 2025  
**Status:** Production Ready
