from web_app_sql import app, db, AdminUser

with app.app_context():
    # Check if admin already exists
    admin = AdminUser.query.filter_by(email='tyson.riskas@uvu.edu').first()
    
    if admin:
        # If admin exists, just reset the password
        admin.set_password('10342243Xnt5!')
        print("Password updated for tyson.riskas@uvu.edu")
    else:
        # If admin doesn't exist, create new
        admin = AdminUser(
            email='tyson.riskas@uvu.edu',
            first_name='Admin',
            last_name='User',
            is_active=True,
            is_super_admin=True
        )
        admin.set_password('10342243Xnt5!')
        db.session.add(admin)
        print("Admin user created: tyson.riskas@uvu.edu")
    
    # Save changes
    db.session.commit()
    print("✅ Admin setup complete!")
    print("Email: tyson.riskas@uvu.edu")
    print("Password: 10342243Xnt5!")
