"""
Database Configuration and Utilities
Handles database initialization, migration, and helper functions
"""

import os
from models import db, User, Conversation, AdminUser
from datetime import datetime


def get_database_url():
    """
    Get database URL based on environment.
    Supports both local development (SQLite) and production (PostgreSQL on Heroku/AWS).
    """
    # Check for Heroku PostgreSQL
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Heroku uses postgres:// but SQLAlchemy needs postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    
    # Local development - use SQLite
    return 'sqlite:///chatbot.db'


def init_db(app):
    """Initialize database with Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print(f"Database initialized: {app.config['SQLALCHEMY_DATABASE_URI']}")


def create_admin_user(email, password, first_name, last_name, is_super_admin=False):
    """Create an admin user."""
    admin = AdminUser(
        email=email.lower(),
        first_name=first_name,
        last_name=last_name,
        is_super_admin=is_super_admin
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    
    return admin


def migrate_json_to_db():
    """
    Migrate existing JSON data to SQL database.
    This is a one-time migration function.
    """
    import json
    from pathlib import Path
    
    print("Starting data migration from JSON to SQL...")
    
    # Migrate users from users_db.json
    users_file = Path('users_db.json')
    user_map = {}  # Map email to User object
    
    if users_file.exists():
        print("Migrating users...")
        with open(users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        for email, user_data in users_data.items():
            # Check if user already exists
            existing_user = User.query.filter_by(email=email.lower()).first()
            if existing_user:
                user_map[email.lower()] = existing_user
                continue
            
            user = User(
                email=email.lower(),
                password_hash=user_data.get('password_hash'),
                first_name=user_data.get('firstName', ''),
                last_name=user_data.get('lastName', ''),
                student_id=user_data.get('studentId', ''),
                course_section=user_data.get('courseSection', ''),
                semester=user_data.get('semester', '')
            )
            
            # Parse created_at if exists
            if 'created_at' in user_data:
                try:
                    user.created_at = datetime.fromisoformat(user_data['created_at'])
                except:
                    pass
            
            db.session.add(user)
            user_map[email.lower()] = user
        
        db.session.commit()
        print(f"Migrated {len(user_map)} users")
    
    # Migrate conversations from qa_conversations.json
    conversations_file = Path('qa_conversations.json')
    
    if conversations_file.exists():
        print("Migrating conversations...")
        with open(conversations_file, 'r', encoding='utf-8') as f:
            conversations_data = json.load(f)
        
        migrated_count = 0
        for conv_data in conversations_data:
            user_info = conv_data.get('user_info', {})
            is_registered = user_info.get('is_registered', False)
            
            conversation = Conversation(
                question=conv_data.get('question', ''),
                answer=conv_data.get('answer', ''),
                session_id=conv_data.get('session_id', ''),
                is_guest=not is_registered
            )
            
            # Parse timestamp
            if 'timestamp' in conv_data:
                try:
                    conversation.timestamp = datetime.fromisoformat(conv_data['timestamp'])
                except:
                    pass
            
            if is_registered:
                # Link to registered user
                email = user_info.get('email', '').lower()
                if email in user_map:
                    conversation.user_id = user_map[email].id
            else:
                # Store guest user info
                conversation.guest_first_name = user_info.get('firstName', '')
                conversation.guest_last_name = user_info.get('lastName', '')
                conversation.guest_student_id = user_info.get('studentId', '')
                conversation.guest_email = user_info.get('email', '')
                conversation.guest_course_section = user_info.get('courseSection', '')
                conversation.guest_semester = user_info.get('semester', '')
            
            db.session.add(conversation)
            migrated_count += 1
        
        db.session.commit()
        print(f"Migrated {migrated_count} conversations")
    
    print("Migration complete!")


def get_database_stats():
    """Get statistics about the database."""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    total_conversations = Conversation.query.count()
    registered_conversations = Conversation.query.filter_by(is_guest=False).count()
    guest_conversations = Conversation.query.filter_by(is_guest=True).count()
    total_admins = AdminUser.query.count()
    
    return {
        'total_users': total_users,
        'active_users': active_users,
        'total_conversations': total_conversations,
        'registered_conversations': registered_conversations,
        'guest_conversations': guest_conversations,
        'total_admins': total_admins
    }


def backup_database_to_json():
    """Backup database to JSON files (for safety)."""
    import json
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Backup users
    users = User.query.all()
    users_data = {user.email: user.to_dict() for user in users}
    
    with open(f'backup_users_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=2, ensure_ascii=False)
    
    # Backup conversations
    conversations = Conversation.query.all()
    conversations_data = [conv.to_dict() for conv in conversations]
    
    with open(f'backup_conversations_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(conversations_data, f, indent=2, ensure_ascii=False)
    
    print(f"Backup created: backup_users_{timestamp}.json, backup_conversations_{timestamp}.json")
