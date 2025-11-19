"""
Data Extraction Script for Student Q&A Chatbot
This script helps you view and export conversation data with user information.
"""

import json
from pathlib import Path
from datetime import datetime
import csv


def load_conversations(filepath="qa_conversations.json"):
    """Load conversations from JSON file."""
    file_path = Path(filepath)
    if not file_path.exists():
        print(f"Error: {filepath} not found!")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def display_summary(conversations):
    """Display summary statistics."""
    print("\n" + "=" * 70)
    print("CONVERSATION DATA SUMMARY")
    print("=" * 70)
    print(f"Total Conversations: {len(conversations)}")
    
    # Count unique users
    unique_students = set()
    for conv in conversations:
        user_info = conv.get('user_info', {})
        student_id = user_info.get('studentId', 'N/A')
        if student_id != 'N/A':
            unique_students.add(student_id)
    
    print(f"Unique Students: {len(unique_students)}")
    print(f"Anonymous Conversations: {len([c for c in conversations if not c.get('user_info', {}).get('studentId')])}")
    print("=" * 70 + "\n")


def display_by_student(conversations):
    """Display conversations grouped by student."""
    # Group by student
    student_data = {}
    for conv in conversations:
        user_info = conv.get('user_info', {})
        student_id = user_info.get('studentId', 'Anonymous')
        
        if student_id not in student_data:
            student_data[student_id] = {
                'user_info': user_info,
                'conversations': []
            }
        
        student_data[student_id]['conversations'].append({
            'id': conv.get('id'),
            'question': conv.get('question'),
            'answer': conv.get('answer'),
            'timestamp': conv.get('timestamp')
        })
    
    # Display
    for student_id, data in student_data.items():
        print("\n" + "-" * 70)
        if student_id != 'Anonymous':
            user_info = data['user_info']
            print(f"Student: {user_info.get('firstName', 'N/A')} {user_info.get('lastName', 'N/A')}")
            print(f"ID: {student_id}")
            print(f"Email: {user_info.get('email', 'N/A')}")
            print(f"Section: {user_info.get('courseSection', 'N/A')}")
            print(f"Semester: {user_info.get('semester', 'N/A')}")
        else:
            print("Anonymous User (No student info)")
        
        print(f"Total Questions: {len(data['conversations'])}")
        print("\nRecent Questions:")
        for i, conv in enumerate(data['conversations'][-5:], 1):
            print(f"  {i}. {conv['question'][:80]}{'...' if len(conv['question']) > 80 else ''}")
        print("-" * 70)


def export_to_csv(conversations, output_file="conversations_export.csv"):
    """Export conversations to CSV file."""
    if not conversations:
        print("No conversations to export!")
        return
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'conversation_id', 'student_id', 'first_name', 'last_name', 
            'email', 'course_section', 'semester', 'question', 'answer', 
            'timestamp', 'session_id'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for conv in conversations:
            user_info = conv.get('user_info', {})
            writer.writerow({
                'conversation_id': conv.get('id', ''),
                'student_id': user_info.get('studentId', ''),
                'first_name': user_info.get('firstName', ''),
                'last_name': user_info.get('lastName', ''),
                'email': user_info.get('email', ''),
                'course_section': user_info.get('courseSection', ''),
                'semester': user_info.get('semester', ''),
                'question': conv.get('question', ''),
                'answer': conv.get('answer', ''),
                'timestamp': conv.get('timestamp', ''),
                'session_id': conv.get('session_id', '')
            })
    
    print(f"\n✓ Data exported to {output_file}")


def search_by_student_id(conversations, student_id):
    """Search conversations by student ID."""
    results = [c for c in conversations if c.get('user_info', {}).get('studentId') == student_id]
    
    if not results:
        print(f"\nNo conversations found for Student ID: {student_id}")
        return
    
    print(f"\nFound {len(results)} conversation(s) for Student ID: {student_id}")
    print("-" * 70)
    
    for i, conv in enumerate(results, 1):
        print(f"\nConversation #{i} (ID: {conv.get('id')})")
        print(f"Timestamp: {conv.get('timestamp', 'N/A')}")
        print(f"Q: {conv.get('question', 'N/A')}")
        print(f"A: {conv.get('answer', 'N/A')[:200]}{'...' if len(conv.get('answer', '')) > 200 else ''}")
        print("-" * 70)


def main():
    """Main menu for data extraction."""
    print("\n" + "=" * 70)
    print("STUDENT Q&A CHATBOT - DATA EXTRACTION TOOL")
    print("=" * 70)
    
    conversations = load_conversations()
    if not conversations:
        return
    
    while True:
        print("\nOptions:")
        print("1. View summary statistics")
        print("2. View conversations by student")
        print("3. Search by Student ID")
        print("4. Export to CSV")
        print("5. Export to JSON (formatted)")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            display_summary(conversations)
        
        elif choice == '2':
            display_by_student(conversations)
        
        elif choice == '3':
            student_id = input("Enter Student ID: ").strip()
            search_by_student_id(conversations, student_id)
        
        elif choice == '4':
            filename = input("Enter CSV filename (default: conversations_export.csv): ").strip()
            if not filename:
                filename = "conversations_export.csv"
            export_to_csv(conversations, filename)
        
        elif choice == '5':
            filename = input("Enter JSON filename (default: conversations_formatted.json): ").strip()
            if not filename:
                filename = "conversations_formatted.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'export_timestamp': datetime.now().isoformat(),
                    'total_conversations': len(conversations),
                    'conversations': conversations
                }, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Data exported to {filename}")
        
        elif choice == '6':
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
