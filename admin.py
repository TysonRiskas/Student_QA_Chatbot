"""
Admin Dashboard for Student Q&A Chatbot
Provides administrator-friendly database access and management
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models import db, User, Conversation, AdminUser
from database import get_database_stats, backup_database_to_json
from datetime import datetime, timedelta
from functools import wraps
import csv
import io

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        admin = AdminUser.query.filter_by(email=email).first()
        
        if admin and admin.is_active and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_email'] = admin.email
            session['admin_name'] = admin.first_name
            session['is_super_admin'] = admin.is_super_admin
            
            # Update last login
            admin.last_login = datetime.utcnow()
            db.session.commit()
            
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin/login.html')


@admin_bp.route('/logout')
def admin_logout():
    """Admin logout."""
    session.clear()
    return redirect(url_for('admin.admin_login'))


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Main admin dashboard."""
    stats = get_database_stats()
    
    # Get recent activity
    recent_conversations = Conversation.query.order_by(
        Conversation.timestamp.desc()
    ).limit(10).all()
    
    recent_users = User.query.order_by(
        User.created_at.desc()
    ).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_conversations=recent_conversations,
                         recent_users=recent_users)


@admin_bp.route('/users')
@admin_required
def list_users():
    """List all users."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    search = request.args.get('search', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            db.or_(
                User.email.ilike(f'%{search}%'),
                User.first_name.ilike(f'%{search}%'),
                User.last_name.ilike(f'%{search}%'),
                User.student_id.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/users.html',
                         users=pagination.items,
                         pagination=pagination,
                         search=search)


@admin_bp.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    """View user details and their conversations."""
    user = User.query.get_or_404(user_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    pagination = user.conversations.order_by(
        Conversation.timestamp.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/user_detail.html',
                         user=user,
                         conversations=pagination.items,
                         pagination=pagination)


@admin_bp.route('/conversations')
@admin_required
def list_conversations():
    """List all conversations."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    search = request.args.get('search', '')
    filter_type = request.args.get('filter', 'all')
    
    query = Conversation.query
    
    # Apply filters
    if filter_type == 'registered':
        query = query.filter_by(is_guest=False)
    elif filter_type == 'guest':
        query = query.filter_by(is_guest=True)
    
    if search:
        query = query.filter(
            db.or_(
                Conversation.question.ilike(f'%{search}%'),
                Conversation.answer.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(Conversation.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/conversations.html',
                         conversations=pagination.items,
                         pagination=pagination,
                         search=search,
                         filter_type=filter_type)


@admin_bp.route('/analytics')
@admin_required
def analytics():
    """Analytics dashboard."""
    # Get date range
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Conversations over time
    conversations_by_date = db.session.query(
        db.func.date(Conversation.timestamp).label('date'),
        db.func.count(Conversation.id).label('count')
    ).filter(
        Conversation.timestamp >= start_date
    ).group_by(
        db.func.date(Conversation.timestamp)
    ).all()
    
    # Top users by conversation count
    top_users = db.session.query(
        User,
        db.func.count(Conversation.id).label('conversation_count')
    ).join(
        Conversation
    ).group_by(
        User.id
    ).order_by(
        db.desc('conversation_count')
    ).limit(10).all()
    
    # Most common questions (simplified - just counts)
    total_conversations = Conversation.query.filter(
        Conversation.timestamp >= start_date
    ).count()
    
    registered_count = Conversation.query.filter(
        Conversation.timestamp >= start_date,
        Conversation.is_guest == False
    ).count()
    
    guest_count = Conversation.query.filter(
        Conversation.timestamp >= start_date,
        Conversation.is_guest == True
    ).count()
    
    return render_template('admin/analytics.html',
                         conversations_by_date=conversations_by_date,
                         top_users=top_users,
                         total_conversations=total_conversations,
                         registered_count=registered_count,
                         guest_count=guest_count,
                         days=days)


@admin_bp.route('/export/users')
@admin_required
def export_users():
    """Export users to CSV."""
    users = User.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['ID', 'Email', 'First Name', 'Last Name', 'Student ID', 
                    'Course Section', 'Semester', 'Created At', 'Conversation Count'])
    
    # Data
    for user in users:
        writer.writerow([
            user.id,
            user.email,
            user.first_name,
            user.last_name,
            user.student_id,
            user.course_section or '',
            user.semester or '',
            user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '',
            user.conversations.count()
        ])
    
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': f'attachment; filename=users_{datetime.now().strftime("%Y%m%d")}.csv'
    }


@admin_bp.route('/export/conversations')
@admin_required
def export_conversations():
    """Export conversations to CSV."""
    conversations = Conversation.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['ID', 'User Email', 'Student ID', 'Question', 'Answer', 
                    'Timestamp', 'Is Guest', 'Session ID'])
    
    # Data
    for conv in conversations:
        if conv.is_guest:
            user_email = conv.guest_email or 'Guest'
            student_id = conv.guest_student_id or 'N/A'
        else:
            user_email = conv.user.email if conv.user else 'N/A'
            student_id = conv.user.student_id if conv.user else 'N/A'
        
        writer.writerow([
            conv.id,
            user_email,
            student_id,
            conv.question,
            conv.answer,
            conv.timestamp.strftime('%Y-%m-%d %H:%M:%S') if conv.timestamp else '',
            'Yes' if conv.is_guest else 'No',
            conv.session_id
        ])
    
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': f'attachment; filename=conversations_{datetime.now().strftime("%Y%m%d")}.csv'
    }


@admin_bp.route('/backup')
@admin_required
def create_backup():
    """Create database backup."""
    try:
        backup_database_to_json()
        flash('Backup created successfully!', 'success')
    except Exception as e:
        flash(f'Backup failed: {str(e)}', 'error')
    
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/api/stats')
@admin_required
def api_stats():
    """API endpoint for dashboard stats."""
    stats = get_database_stats()
    return jsonify(stats)


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit user details."""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name', '').strip()
        user.last_name = request.form.get('last_name', '').strip()
        user.email = request.form.get('email', '').strip().lower()
        user.student_id = request.form.get('student_id', '').strip()
        user.course_section = request.form.get('course_section', '').strip()
        user.semester = request.form.get('semester', '').strip()
        user.is_active = request.form.get('is_active') == 'on'
        
        # Optional password change
        new_password = request.form.get('new_password', '').strip()
        if new_password:
            if len(new_password) < 6:
                flash('Password must be at least 6 characters', 'error')
                return render_template('admin/edit_user.html', user=user)
            user.set_password(new_password)
        
        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.user_detail', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
    
    return render_template('admin/edit_user.html', user=user)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    
    try:
        # Conversations will be deleted automatically due to cascade
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.email} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('admin.list_users'))


@admin_bp.route('/conversations/<int:conv_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_conversation(conv_id):
    """Edit a conversation."""
    conversation = Conversation.query.get_or_404(conv_id)
    
    if request.method == 'POST':
        conversation.question = request.form.get('question', '').strip()
        conversation.answer = request.form.get('answer', '').strip()
        
        # Update guest info if it's a guest conversation
        if conversation.is_guest:
            conversation.guest_first_name = request.form.get('guest_first_name', '').strip()
            conversation.guest_last_name = request.form.get('guest_last_name', '').strip()
            conversation.guest_student_id = request.form.get('guest_student_id', '').strip()
            conversation.guest_email = request.form.get('guest_email', '').strip()
            conversation.guest_course_section = request.form.get('guest_course_section', '').strip()
            conversation.guest_semester = request.form.get('guest_semester', '').strip()
        
        try:
            db.session.commit()
            flash('Conversation updated successfully!', 'success')
            return redirect(url_for('admin.list_conversations'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating conversation: {str(e)}', 'error')
    
    return render_template('admin/edit_conversation.html', conversation=conversation)


@admin_bp.route('/conversations/<int:conv_id>/delete', methods=['POST'])
@admin_required
def delete_conversation(conv_id):
    """Delete a conversation."""
    conversation = Conversation.query.get_or_404(conv_id)
    
    try:
        db.session.delete(conversation)
        db.session.commit()
        flash('Conversation deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting conversation: {str(e)}', 'error')
    
    return redirect(url_for('admin.list_conversations'))


@admin_bp.route('/users/merge', methods=['GET', 'POST'])
@admin_required
def merge_users():
    """Merge two user accounts."""
    if request.method == 'POST':
        source_id = request.form.get('source_user_id', type=int)
        target_id = request.form.get('target_user_id', type=int)
        
        if not source_id or not target_id:
            flash('Please select both users to merge', 'error')
            return redirect(url_for('admin.merge_users'))
        
        if source_id == target_id:
            flash('Cannot merge a user with themselves', 'error')
            return redirect(url_for('admin.merge_users'))
        
        source_user = User.query.get_or_404(source_id)
        target_user = User.query.get_or_404(target_id)
        
        try:
            # Move all conversations from source to target
            conversations = Conversation.query.filter_by(user_id=source_id).all()
            for conv in conversations:
                conv.user_id = target_id
            
            # Delete source user
            db.session.delete(source_user)
            db.session.commit()
            
            flash(f'Successfully merged {source_user.email} into {target_user.email}. '
                  f'{len(conversations)} conversations transferred.', 'success')
            return redirect(url_for('admin.user_detail', user_id=target_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error merging users: {str(e)}', 'error')
    
    # Get all users for the merge form
    users = User.query.order_by(User.email).all()
    return render_template('admin/merge_users.html', users=users)
