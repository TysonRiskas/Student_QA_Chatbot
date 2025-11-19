"""
Database Migration Script
Migrates data from JSON files to SQL database
Run this once to migrate existing data
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask
from dotenv import load_dotenv
from database import init_db, migrate_json_to_db, create_admin_user, get_database_stats

# Load environment variables
load_dotenv()

# Create Flask app for database context
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

def main():
    """Main migration function."""
    print("=" * 70)
    print("Student Q&A Chatbot - Database Migration Tool")
    print("=" * 70)
    print()
    
    # Initialize database
    print("Initializing database...")
    init_db(app)
    
    with app.app_context():
        # Ask user what to do
        print("\nOptions:")
        print("1. Migrate JSON data to SQL database")
        print("2. Create admin user")
        print("3. View database statistics")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            confirm = input("\nThis will migrate all JSON data to SQL. Continue? (yes/no): ")
            if confirm.lower() == 'yes':
                migrate_json_to_db()
                print("\n✓ Migration complete!")
                print("\nDatabase statistics:")
                stats = get_database_stats()
                for key, value in stats.items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            else:
                print("Migration cancelled.")
        
        elif choice == '2':
            print("\nCreate Admin User")
            print("-" * 40)
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            is_super = input("Super Admin? (yes/no): ").strip().lower() == 'yes'
            
            try:
                admin = create_admin_user(email, password, first_name, last_name, is_super)
                print(f"\n✓ Admin user created: {admin.email}")
            except Exception as e:
                print(f"\n✗ Error creating admin: {e}")
        
        elif choice == '3':
            print("\nDatabase Statistics:")
            print("-" * 40)
            stats = get_database_stats()
            for key, value in stats.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        elif choice == '4':
            print("\nGoodbye!")
        
        else:
            print("\nInvalid choice.")


if __name__ == '__main__':
    main()
