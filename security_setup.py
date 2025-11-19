"""
Security Setup Script
Use this script to generate a secure SECRET_KEY and change admin password
Run this BEFORE deploying to production!
"""

import secrets
import os
from pathlib import Path

def generate_secret_key():
    """Generate a cryptographically secure secret key."""
    print("\n" + "="*60)
    print("GENERATING SECRET KEY")
    print("="*60)
    
    secret_key = secrets.token_hex(32)
    print(f"\nYour new SECRET_KEY:\n{secret_key}\n")
    
    # Update .env file
    env_path = Path('.env')
    
    if env_path.exists():
        print("✅ Found existing .env file")
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Update SECRET_KEY line
        updated = False
        new_lines = []
        for line in lines:
            if line.startswith('SECRET_KEY='):
                new_lines.append(f'SECRET_KEY={secret_key}\n')
                updated = True
            else:
                new_lines.append(line)
        
        # If SECRET_KEY wasn't found, add it
        if not updated:
            new_lines.append(f'SECRET_KEY={secret_key}\n')
        
        with open(env_path, 'w') as f:
            f.writelines(new_lines)
        
        print("✅ Updated SECRET_KEY in .env file")
    else:
        print("⚠️  No .env file found, creating one...")
        with open(env_path, 'w') as f:
            f.write(f'MISTRAL_API_KEY=your_mistral_api_key_here\n')
            f.write(f'SECRET_KEY={secret_key}\n')
        print("✅ Created .env file with new SECRET_KEY")
    
    print("\n⚠️  IMPORTANT: Never commit the .env file to git!")
    print("✅ SECRET_KEY has been updated\n")


def change_admin_password():
    """Change the admin password."""
    print("\n" + "="*60)
    print("CHANGING ADMIN PASSWORD")
    print("="*60)
    
    try:
        from web_app_sql import app, db, AdminUser
        
        print("\nCurrent admin email: admin@uvu.edu")
        print("Current password: admin123 (DEFAULT - MUST CHANGE!)\n")
        
        new_password = input("Enter new admin password (min 12 characters): ").strip()
        
        if len(new_password) < 12:
            print("❌ Password too short! Must be at least 12 characters.")
            return
        
        confirm_password = input("Confirm new password: ").strip()
        
        if new_password != confirm_password:
            print("❌ Passwords don't match!")
            return
        
        with app.app_context():
            admin = AdminUser.query.filter_by(email='admin@uvu.edu').first()
            
            if admin:
                admin.set_password(new_password)
                db.session.commit()
                print("\n✅ Admin password updated successfully!")
                print("✅ New password is secure and hashed in database")
                print("\n⚠️  REMEMBER YOUR NEW PASSWORD - It cannot be recovered!")
            else:
                print("❌ Admin user not found. Run migrate_to_sql.py first.")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure you:")
        print("1. Have activated your virtual environment")
        print("2. Have run migrate_to_sql.py to create admin user")
        print("3. Are in the correct directory")


def main():
    """Main menu for security setup."""
    print("\n" + "="*60)
    print("SECURITY SETUP SCRIPT")
    print("Student Q&A Chatbot")
    print("="*60)
    
    print("\nThis script will help you:")
    print("1. Generate a secure SECRET_KEY")
    print("2. Change the default admin password")
    print("\nBoth are REQUIRED before production deployment!\n")
    
    while True:
        print("\nOptions:")
        print("1. Generate new SECRET_KEY")
        print("2. Change admin password")
        print("3. Do both (recommended)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            generate_secret_key()
        elif choice == '2':
            change_admin_password()
        elif choice == '3':
            generate_secret_key()
            change_admin_password()
        elif choice == '4':
            print("\n✅ Security setup complete!")
            print("Don't forget to:")
            print("- Test login with new password")
            print("- Never share or commit .env file")
            print("- Enable HTTPS in production")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")


if __name__ == '__main__':
    main()
