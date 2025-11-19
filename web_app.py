"""
Student Q&A Chatbot - Flask Web Application
A web-based chatbot that answers student questions using course materials and AI assistance.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json
import uuid
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from mistralai import Mistral
import PyPDF2
import docx
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'

class ChatbotCorpus:
    """Manages the corpus of course materials (PDFs, DOCX, MP4)."""
    
    def __init__(self, corpus_dir="corpus"):
        self.corpus_dir = Path(corpus_dir)
        self.corpus_text = ""
        
    def load_corpus(self):
        """Load all documents from the corpus directory."""
        if not self.corpus_dir.exists():
            print(f"Creating corpus directory: {self.corpus_dir}")
            self.corpus_dir.mkdir(parents=True, exist_ok=True)
            return
        
        corpus_parts = []
        
        # Load PDFs
        for pdf_file in self.corpus_dir.glob("*.pdf"):
            print(f"Loading PDF: {pdf_file.name}")
            corpus_parts.append(self._read_pdf(pdf_file))
        
        # Load DOCX files
        for docx_file in self.corpus_dir.glob("*.docx"):
            print(f"Loading DOCX: {docx_file.name}")
            corpus_parts.append(self._read_docx(docx_file))
        
        # Load MP4 files (extract metadata/info)
        for mp4_file in self.corpus_dir.glob("*.mp4"):
            print(f"Loading MP4 metadata: {mp4_file.name}")
            corpus_parts.append(self._read_mp4_info(mp4_file))
        
        self.corpus_text = "\n\n".join(corpus_parts)
        
        if self.corpus_text.strip():
            print(f"Corpus loaded successfully! ({len(corpus_parts)} files)")
        else:
            print("No corpus files found.")
    
    def _read_pdf(self, filepath):
        """Extract text from PDF file."""
        try:
            text_parts = []
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text_parts.append(page.extract_text())
            return f"[PDF: {filepath.name}]\n" + "\n".join(text_parts)
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")
            return ""
    
    def _read_docx(self, filepath):
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(filepath)
            text = "\n".join([para.text for para in doc.paragraphs])
            return f"[DOCX: {filepath.name}]\n" + text
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")
            return ""
    
    def _read_mp4_info(self, filepath):
        """Extract basic info from MP4 file."""
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(str(filepath))
            duration = clip.duration
            clip.close()
            return f"[VIDEO: {filepath.name}]\nDuration: {duration:.2f} seconds\nNote: This is a video lecture file."
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")
            return f"[VIDEO: {filepath.name}]\nNote: Video file present but metadata unavailable."


class ChatbotManager:
    """Manages chatbot conversations and AI interactions."""
    
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key or self.api_key == "your_mistral_api_key_here":
            print("ERROR: MISTRAL_API_KEY not found in .env file")
            sys.exit(1)
        
        self.client = Mistral(api_key=self.api_key)
        self.model = "mistral-small-latest"
        self.corpus = ChatbotCorpus()
        self.storage_file = Path("qa_conversations.json")
        self.corpus.load_corpus()
    
    def get_ai_response(self, question):
        """Get response from Mistral AI."""
        try:
            system_message = (
                "You are a helpful teaching assistant for INFO 6200, a Python coding course. "
                "Answer student questions clearly and concisely based on the course materials provided. "
                "If the answer isn't in the course materials, provide general Python guidance but mention "
                "that students should verify with their professor."
            )
            
            if self.corpus.corpus_text:
                system_message += f"\n\nCourse Materials:\n{self.corpus.corpus_text[:8000]}"
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": question}
            ]
            
            response = self.client.chat.complete(
                model=self.model,
                messages=messages
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}\nPlease try again."
    
    def save_conversation(self, question, answer, user_info=None, session_id=None):
        """Save a Q&A pair to persistent storage with user metadata."""
        try:
            # Load existing conversations
            conversations = []
            if self.storage_file.exists():
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)
            
            # Add new conversation with user info
            qa_pair = {
                "id": len(conversations) + 1,
                "question": question,
                "answer": answer,
                "timestamp": datetime.now().isoformat(),
                "saved_at": datetime.now().isoformat(),
                "session_id": session_id or str(uuid.uuid4()),
                "user_info": user_info or {}
            }
            conversations.append(qa_pair)
            
            # Save to file
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False


# Initialize chatbot
chatbot = ChatbotManager()

# User database file
USERS_DB_FILE = Path("users_db.json")

def load_users():
    """Load users from JSON file."""
    if USERS_DB_FILE.exists():
        with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file."""
    with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


@app.route('/')
def index():
    """Main route - redirects to login if no session, otherwise shows chat."""
    if 'user_info' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user_info=session.get('user_info'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        users = load_users()
        
        if email in users:
            user = users[email]
            if check_password_hash(user['password_hash'], password):
                # Successful login
                session['user_info'] = {
                    'firstName': user['firstName'],
                    'lastName': user['lastName'],
                    'studentId': user['studentId'],
                    'email': user['email'],
                    'courseSection': user.get('courseSection', ''),
                    'semester': user.get('semester', ''),
                    'is_registered': True
                }
                session['session_id'] = str(uuid.uuid4())
                session['session_start'] = datetime.now().isoformat()
                session['user_email'] = email
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Invalid email or password')
        else:
            return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route."""
    if request.method == 'POST':
        firstName = request.form.get('firstName', '').strip()
        lastName = request.form.get('lastName', '').strip()
        studentId = request.form.get('studentId', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirmPassword = request.form.get('confirmPassword', '')
        courseSection = request.form.get('courseSection', '').strip()
        semester = request.form.get('semester', '').strip()
        
        # Validation
        if not all([firstName, lastName, studentId, email, password]):
            return render_template('register.html', error='All required fields must be filled')
        
        if password != confirmPassword:
            return render_template('register.html', error='Passwords do not match')
        
        if len(password) < 6:
            return render_template('register.html', error='Password must be at least 6 characters')
        
        users = load_users()
        
        if email in users:
            return render_template('register.html', error='Email already registered')
        
        # Create new user
        users[email] = {
            'firstName': firstName,
            'lastName': lastName,
            'studentId': studentId,
            'email': email,
            'password_hash': generate_password_hash(password),
            'courseSection': courseSection,
            'semester': semester,
            'created_at': datetime.now().isoformat()
        }
        
        save_users(users)
        
        # Auto-login after registration
        session['user_info'] = {
            'firstName': firstName,
            'lastName': lastName,
            'studentId': studentId,
            'email': email,
            'courseSection': courseSection,
            'semester': semester,
            'is_registered': True
        }
        session['session_id'] = str(uuid.uuid4())
        session['session_start'] = datetime.now().isoformat()
        session['user_email'] = email
        
        return redirect(url_for('index'))
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """Logout route."""
    session.clear()
    return redirect(url_for('login'))


@app.route('/user_form')
def user_form():
    """Display the user information form for guest users."""
    return render_template('user_form.html')


@app.route('/submit_user_info', methods=['POST'])
def submit_user_info():
    """Process user information form for guest session."""
    user_info = {
        'firstName': request.form.get('firstName', '').strip(),
        'lastName': request.form.get('lastName', '').strip(),
        'studentId': request.form.get('studentId', '').strip(),
        'email': request.form.get('email', '').strip(),
        'courseSection': request.form.get('courseSection', '').strip(),
        'semester': request.form.get('semester', '').strip(),
        'submission_timestamp': datetime.now().isoformat(),
        'is_registered': False
    }
    
    # Validate required fields
    if not all([user_info['firstName'], user_info['lastName'], 
                user_info['studentId'], user_info['email']]):
        return "Missing required fields", 400
    
    # Store user info in session
    session['user_info'] = user_info
    session['session_id'] = str(uuid.uuid4())
    session['session_start'] = datetime.now().isoformat()
    
    return redirect(url_for('index'))


@app.route('/ask', methods=['POST'])
def ask():
    """API endpoint to handle chat questions."""
    # Check if user has submitted their info
    if 'user_info' not in session:
        return jsonify({'error': 'Please submit your information first'}), 403
    
    data = request.get_json()
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({'error': 'Question cannot be empty'}), 400
    
    # Get AI response
    answer = chatbot.get_ai_response(question)
    
    # Save conversation with user info
    chatbot.save_conversation(
        question, 
        answer, 
        user_info=session.get('user_info'),
        session_id=session.get('session_id')
    )
    
    return jsonify({
        'question': question,
        'answer': answer,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/history', methods=['GET'])
def get_history():
    """API endpoint to retrieve conversation history (only for registered users)."""
    try:
        # Only allow registered users to view history
        if 'user_info' not in session or not session.get('user_info', {}).get('is_registered'):
            return jsonify({'error': 'History is only available for registered users'}), 403
        
        user_email = session.get('user_email')
        conversations = []
        
        if chatbot.storage_file.exists():
            with open(chatbot.storage_file, 'r', encoding='utf-8') as f:
                all_conversations = json.load(f)
                
            # Filter conversations for this user only
            conversations = [
                c for c in all_conversations 
                if c.get('user_info', {}).get('email', '').lower() == user_email
            ]
        
        return jsonify({
            'conversations': conversations,
            'count': len(conversations)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/export_data', methods=['GET'])
def export_data():
    """Export all conversation data (admin/backend route)."""
    try:
        conversations = []
        if chatbot.storage_file.exists():
            with open(chatbot.storage_file, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
        
        # Return as downloadable JSON
        return jsonify({
            'total_conversations': len(conversations),
            'data': conversations,
            'export_timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/clear_session', methods=['POST'])
def clear_session():
    """Clear current user session (logout)."""
    session.clear()
    return jsonify({'success': True, 'message': 'Session cleared'})


if __name__ == '__main__':
    print("=" * 60)
    print("Starting INFO 6200 Student Q&A Chatbot Web Application")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
