"""
RESTful API for Student Q&A Chatbot
Provides programmatic access to chatbot data for external applications
Version 1.0 - /api/v1/
"""

from flask import Blueprint, request, jsonify, session
from functools import wraps
from datetime import datetime
from models import db, User, Conversation, AdminUser

# Create API Blueprint with version prefix
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


# ============================================================================
# AUTHENTICATION DECORATORS
# ============================================================================

def api_key_required(f):
    """Decorator to require API key authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for API key in header
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'error': 'API key required',
                'message': 'Please provide X-API-Key header',
                'status': 401
            }), 401
        
        # Verify API key (check if it matches admin or user session)
        # For now, we'll use session-based auth as fallback
        # In production, implement proper API key validation
        
        if 'user_id' not in session and 'admin_id' not in session:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Invalid or expired API key',
                'status': 401
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function


def user_api_auth(f):
    """Decorator for user-authenticated API endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check session authentication
        if 'user_id' not in session:
            return jsonify({
                'error': 'Authentication required',
                'message': 'User must be logged in',
                'status': 401
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function


def admin_api_auth(f):
    """Decorator for admin-authenticated API endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return jsonify({
                'error': 'Admin authentication required',
                'message': 'Admin access only',
                'status': 403
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# API INFO & DOCUMENTATION
# ============================================================================

@api_bp.route('/', methods=['GET'])
def api_info():
    """API information and available endpoints."""
    return jsonify({
        'name': 'Student Q&A Chatbot API',
        'version': '1.0',
        'description': 'RESTful API for accessing chatbot data',
        'base_url': '/api/v1',
        'endpoints': {
            'info': {
                'path': '/api/v1/',
                'method': 'GET',
                'description': 'API information',
                'auth_required': False
            },
            'conversations_list': {
                'path': '/api/v1/conversations',
                'method': 'GET',
                'description': 'Get all conversations for authenticated user',
                'auth_required': True,
                'parameters': {
                    'page': 'Page number (optional, default: 1)',
                    'per_page': 'Items per page (optional, default: 20, max: 100)'
                }
            },
            'conversation_detail': {
                'path': '/api/v1/conversations/<id>',
                'method': 'GET',
                'description': 'Get a specific conversation by ID',
                'auth_required': True
            },
            'users_list': {
                'path': '/api/v1/users',
                'method': 'GET',
                'description': 'Get all users (admin only)',
                'auth_required': True,
                'admin_only': True
            },
            'user_detail': {
                'path': '/api/v1/users/<id>',
                'method': 'GET',
                'description': 'Get a specific user by ID (admin only)',
                'auth_required': True,
                'admin_only': True
            },
            'ask_question': {
                'path': '/api/v1/ask',
                'method': 'POST',
                'description': 'Submit a question to the chatbot',
                'auth_required': True,
                'body': {
                    'question': 'The question to ask (required)'
                }
            },
            'stats': {
                'path': '/api/v1/stats',
                'method': 'GET',
                'description': 'Get user statistics',
                'auth_required': True
            }
        },
        'authentication': {
            'type': 'Session-based',
            'note': 'Login via web interface before using API'
        },
        'response_format': 'JSON',
        'timestamp': datetime.utcnow().isoformat()
    })


# ============================================================================
# CONVERSATION ENDPOINTS
# ============================================================================

@api_bp.route('/conversations', methods=['GET'])
@user_api_auth
def get_conversations():
    """
    Get all conversations for the authenticated user.
    Supports pagination.
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Limit per_page to prevent abuse
        if per_page > 100:
            per_page = 100
        
        user_id = session.get('user_id')
        
        # Query conversations for this user with pagination
        pagination = Conversation.query.filter_by(
            user_id=user_id
        ).order_by(
            Conversation.timestamp.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        conversations = pagination.items
        
        return jsonify({
            'success': True,
            'data': [conv.to_dict() for conv in conversations],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_items': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500


@api_bp.route('/conversations/<int:conversation_id>', methods=['GET'])
@user_api_auth
def get_conversation(conversation_id):
    """
    Get a specific conversation by ID.
    User can only access their own conversations.
    """
    try:
        user_id = session.get('user_id')
        
        # Query conversation
        conversation = Conversation.query.filter_by(
            id=conversation_id,
            user_id=user_id
        ).first()
        
        if not conversation:
            return jsonify({
                'error': 'Not found',
                'message': f'Conversation {conversation_id} not found or access denied',
                'status': 404
            }), 404
        
        return jsonify({
            'success': True,
            'data': conversation.to_dict(),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500


# ============================================================================
# USER ENDPOINTS (Admin Only)
# ============================================================================

@api_bp.route('/users', methods=['GET'])
@admin_api_auth
def get_users():
    """
    Get all users (admin only).
    Supports pagination and search.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str)
        
        if per_page > 100:
            per_page = 100
        
        # Build query
        query = User.query
        
        # Apply search filter if provided
        if search:
            query = query.filter(
                db.or_(
                    User.email.ilike(f'%{search}%'),
                    User.first_name.ilike(f'%{search}%'),
                    User.last_name.ilike(f'%{search}%'),
                    User.student_id.ilike(f'%{search}%')
                )
            )
        
        # Paginate
        pagination = query.order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        users = pagination.items
        
        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in users],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_items': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'search': search if search else None,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500


@api_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_api_auth
def get_user(user_id):
    """
    Get a specific user by ID (admin only).
    """
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'error': 'Not found',
                'message': f'User {user_id} not found',
                'status': 404
            }), 404
        
        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500


# ============================================================================
# CHATBOT INTERACTION ENDPOINT
# ============================================================================

@api_bp.route('/ask', methods=['POST'])
@user_api_auth
def ask_question():
    """
    Submit a question to the chatbot and get an AI response.
    Saves the conversation to the database.
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'error': 'Bad request',
                'message': 'Question field is required',
                'status': 400
            }), 400
        
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'error': 'Bad request',
                'message': 'Question cannot be empty',
                'status': 400
            }), 400
        
        if len(question) > 1000:
            return jsonify({
                'error': 'Bad request',
                'message': 'Question too long (max 1000 characters)',
                'status': 400
            }), 400
        
        # Import chatbot (lazy load to avoid circular imports)
        from web_app_sql import chatbot
        
        # Get AI response
        answer = chatbot.get_ai_response(question)
        
        # Save conversation
        user_id = session.get('user_id')
        session_id = session.get('session_id')
        
        conversation = Conversation(
            user_id=user_id,
            session_id=session_id,
            question=question,
            answer=answer,
            is_guest=False
        )
        
        db.session.add(conversation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'conversation_id': conversation.id,
                'question': question,
                'answer': answer,
                'timestamp': conversation.timestamp.isoformat()
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500


# ============================================================================
# STATISTICS ENDPOINT
# ============================================================================

@api_bp.route('/stats', methods=['GET'])
@user_api_auth
def get_user_stats():
    """
    Get statistics for the authenticated user.
    """
    try:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'error': 'Not found',
                'message': 'User not found',
                'status': 404
            }), 404
        
        # Get conversation statistics
        total_conversations = user.conversations.count()
        
        # Get recent conversations (last 7 days)
        from datetime import timedelta
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_conversations = user.conversations.filter(
            Conversation.timestamp >= seven_days_ago
        ).count()
        
        # Get latest conversation
        latest_conversation = user.conversations.order_by(
            Conversation.timestamp.desc()
        ).first()
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'student_id': user.student_id
                },
                'statistics': {
                    'total_conversations': total_conversations,
                    'conversations_last_7_days': recent_conversations,
                    'member_since': user.created_at.isoformat() if user.created_at else None,
                    'last_activity': latest_conversation.timestamp.isoformat() if latest_conversation else None
                }
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@api_bp.errorhandler(404)
def api_not_found(error):
    """Handle 404 errors in API."""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found',
        'status': 404
    }), 404


@api_bp.errorhandler(405)
def api_method_not_allowed(error):
    """Handle 405 errors in API."""
    return jsonify({
        'error': 'Method not allowed',
        'message': 'The method is not allowed for the requested URL',
        'status': 405
    }), 405


@api_bp.errorhandler(500)
def api_internal_error(error):
    """Handle 500 errors in API."""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred',
        'status': 500
    }), 500
