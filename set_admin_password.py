import getpass
from web_app_sql import app, db, AdminUser

def set_new_password():
    """Securely prompts user to set a new admin password."""
    password = getpass.getpass("Enter the new admin password: ")
    password_confirm = getpass.getpass("Confirm the new admin password: ")

    if password != password_confirm:
        print("Passwords do not match. Please try again.")
        return

    if not password:
        print("Password cannot be empty. Please try again.")
        return

    with app.app_context():
        admin = AdminUser.query.filter_by(email='admin@uvu.edu').first()
        if admin:
            admin.set_password(password)
            db.session.commit()
            print("Admin password updated successfully!")
        else:
            print("Admin user 'admin@uvu.edu' not found.")

if __name__ == "__main__":
    set_new_password()
