"""
Database Models for Student Q&A Chatbot
SQLAlchemy models for PostgreSQL (Heroku-ready, AWS-compatible)
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """User model for registered students."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    course_section = db.Column(db.String(50))
    semester = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = db.relationship('Conversation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'studentId': self.student_id,
            'courseSection': self.course_section,
            'semester': self.semester,
            'isActive': self.is_active,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'conversationCount': self.conversations.count()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'


class Conversation(db.Model):
    """Conversation model for Q&A pairs."""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    
    # Guest user information (for non-registered users)
    guest_first_name = db.Column(db.String(100))
    guest_last_name = db.Column(db.String(100))
    guest_student_id = db.Column(db.String(50))
    guest_email = db.Column(db.String(120))
    guest_course_section = db.Column(db.String(50))
    guest_semester = db.Column(db.String(50))
    
    is_guest = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert conversation to dictionary."""
        result = {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'session_id': self.session_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'saved_at': self.timestamp.isoformat() if self.timestamp else None,
            'is_guest': self.is_guest
        }
        
        if self.is_guest:
            result['user_info'] = {
                'firstName': self.guest_first_name,
                'lastName': self.guest_last_name,
                'studentId': self.guest_student_id,
                'email': self.guest_email,
                'courseSection': self.guest_course_section,
                'semester': self.guest_semester,
                'is_registered': False
            }
        else:
            if self.user:
                result['user_info'] = {
                    'firstName': self.user.first_name,
                    'lastName': self.user.last_name,
                    'studentId': self.user.student_id,
                    'email': self.user.email,
                    'courseSection': self.user.course_section,
                    'semester': self.user.semester,
                    'is_registered': True
                }
        
        return result
    
    def __repr__(self):
        return f'<Conversation {self.id}>'


class AdminUser(db.Model):
    """Admin user model for instructor access."""
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hash and set admin password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert admin to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'isSuperAdmin': self.is_super_admin,
            'isActive': self.is_active,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'lastLogin': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<AdminUser {self.email}>'
