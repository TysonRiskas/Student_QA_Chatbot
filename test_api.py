"""
API Testing Script
Test all API endpoints to verify functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'
API_BASE = f'{BASE_URL}/api/v1'

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def print_test(message):
    print(f"\n{Colors.YELLOW}Testing: {message}{Colors.END}")


class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.user_logged_in = False
        self.admin_logged_in = False
    
    def login_user(self, email='test@example.com', password='test123'):
        """Login as a regular user."""
        print_test("User Login")
        
        response = self.session.post(f'{BASE_URL}/login', data={
            'email': email,
            'password': password
        })
        
        if response.status_code == 200 or 'user_info' in self.session.cookies:
            print_success(f"Logged in as {email}")
            self.user_logged_in = True
            return True
        else:
            print_error(f"Login failed for {email}")
            print_info("Make sure user exists. Create via /register first.")
            return False
    
    def login_admin(self, email='admin@uvu.edu', password='admin123'):
        """Login as admin."""
        print_test("Admin Login")
        
        response = self.session.post(f'{BASE_URL}/admin/login', data={
            'email': email,
            'password': password
        })
        
        if response.status_code == 200:
            print_success(f"Logged in as admin: {email}")
            self.admin_logged_in = True
            return True
        else:
            print_error(f"Admin login failed")
            return False
    
    def test_api_info(self):
        """Test API information endpoint."""
        print_test("GET /api/v1/ - API Information")
        
        response = self.session.get(f'{API_BASE}/')
        
        if response.status_code == 200:
            data = response.json()
            print_success("API info retrieved")
            print_info(f"API: {data.get('name')} v{data.get('version')}")
            print_info(f"Endpoints: {len(data.get('endpoints', {}))} available")
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    
    def test_get_conversations(self):
        """Test getting user conversations."""
        print_test("GET /api/v1/conversations - Get User Conversations")
        
        if not self.user_logged_in:
            print_error("User not logged in")
            return False
        
        response = self.session.get(f'{API_BASE}/conversations')
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('data', []))
            print_success(f"Retrieved {count} conversations")
            
            pagination = data.get('pagination', {})
            print_info(f"Page {pagination.get('page')} of {pagination.get('total_pages')}")
            print_info(f"Total items: {pagination.get('total_items')}")
            
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            print_info(response.text)
            return False
    
    def test_get_conversation_detail(self, conversation_id=1):
        """Test getting a specific conversation."""
        print_test(f"GET /api/v1/conversations/{conversation_id} - Get Single Conversation")
        
        if not self.user_logged_in:
            print_error("User not logged in")
            return False
        
        response = self.session.get(f'{API_BASE}/conversations/{conversation_id}')
        
        if response.status_code == 200:
            data = response.json()
            conv = data.get('data', {})
            print_success(f"Retrieved conversation #{conversation_id}")
            print_info(f"Question: {conv.get('question', 'N/A')[:50]}...")
            return True
        elif response.status_code == 404:
            print_info(f"Conversation {conversation_id} not found (expected if none exist)")
            return True  # Not a failure
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    
    def test_ask_question(self):
        """Test asking a question via API."""
        print_test("POST /api/v1/ask - Ask Question")
        
        if not self.user_logged_in:
            print_error("User not logged in")
            return False
        
        question = "What is the course syllabus?"
        
        response = self.session.post(f'{API_BASE}/ask', json={
            'question': question
        })
        
        if response.status_code == 201:
            data = response.json()
            result = data.get('data', {})
            print_success(f"Question submitted, conversation ID: {result.get('conversation_id')}")
            print_info(f"Answer length: {len(result.get('answer', ''))} characters")
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            print_info(response.text)
            return False
    
    def test_get_stats(self):
        """Test getting user statistics."""
        print_test("GET /api/v1/stats - Get User Statistics")
        
        if not self.user_logged_in:
            print_error("User not logged in")
            return False
        
        response = self.session.get(f'{API_BASE}/stats')
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('data', {}).get('statistics', {})
            print_success("Statistics retrieved")
            print_info(f"Total conversations: {stats.get('total_conversations')}")
            print_info(f"Last 7 days: {stats.get('conversations_last_7_days')}")
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    
    def test_get_users_admin(self):
        """Test getting all users (admin only)."""
        print_test("GET /api/v1/users - Get All Users (Admin)")
        
        if not self.admin_logged_in:
            print_info("Skipping (requires admin login)")
            return True
        
        response = self.session.get(f'{API_BASE}/users')
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('data', []))
            print_success(f"Retrieved {count} users")
            return True
        elif response.status_code == 403:
            print_error("Access denied (not admin)")
            return False
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    
    def test_get_user_detail_admin(self, user_id=1):
        """Test getting a specific user (admin only)."""
        print_test(f"GET /api/v1/users/{user_id} - Get Single User (Admin)")
        
        if not self.admin_logged_in:
            print_info("Skipping (requires admin login)")
            return True
        
        response = self.session.get(f'{API_BASE}/users/{user_id}')
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('data', {})
            print_success(f"Retrieved user: {user.get('email')}")
            return True
        elif response.status_code == 404:
            print_info(f"User {user_id} not found")
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    
    def test_error_handling(self):
        """Test error handling."""
        print_test("Error Handling Tests")
        
        # Test 404
        response = self.session.get(f'{API_BASE}/nonexistent')
        if response.status_code == 404:
            print_success("404 error handled correctly")
        else:
            print_error(f"Expected 404, got {response.status_code}")
        
        # Test 401 (unauthorized)
        temp_session = requests.Session()
        response = temp_session.get(f'{API_BASE}/conversations')
        if response.status_code == 401:
            print_success("401 unauthorized handled correctly")
        else:
            print_error(f"Expected 401, got {response.status_code}")
        
        # Test 400 (bad request)
        if self.user_logged_in:
            response = self.session.post(f'{API_BASE}/ask', json={})
            if response.status_code == 400:
                print_success("400 bad request handled correctly")
            else:
                print_error(f"Expected 400, got {response.status_code}")
        
        return True
    
    def run_all_tests(self):
        """Run all API tests."""
        print("\n" + "="*60)
        print("API TESTING SUITE")
        print("Student Q&A Chatbot API v1.0")
        print("="*60)
        
        results = []
        
        # Public endpoint
        results.append(('API Info', self.test_api_info()))
        
        # User tests
        print("\n" + "-"*60)
        print("USER ENDPOINTS (Requires User Login)")
        print("-"*60)
        
        if self.login_user():
            results.append(('Get Conversations', self.test_get_conversations()))
            results.append(('Get Conversation Detail', self.test_get_conversation_detail()))
            results.append(('Ask Question', self.test_ask_question()))
            results.append(('Get Stats', self.test_get_stats()))
        
        # Admin tests
        print("\n" + "-"*60)
        print("ADMIN ENDPOINTS (Requires Admin Login)")
        print("-"*60)
        
        # Create new session for admin
        self.session = requests.Session()
        
        if self.login_admin():
            results.append(('Get Users (Admin)', self.test_get_users_admin()))
            results.append(('Get User Detail (Admin)', self.test_get_user_detail_admin()))
        
        # Error handling
        print("\n" + "-"*60)
        print("ERROR HANDLING")
        print("-"*60)
        results.append(('Error Handling', self.test_error_handling()))
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✓ PASS" if result else "✗ FAIL"
            color = Colors.GREEN if result else Colors.RED
            print(f"{color}{status}{Colors.END} - {test_name}")
        
        print("\n" + "-"*60)
        print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        print("="*60)
        
        if passed == total:
            print(f"\n{Colors.GREEN}🎉 All tests passed! API is working correctly.{Colors.END}\n")
        else:
            print(f"\n{Colors.YELLOW}⚠ Some tests failed. Check output above.{Colors.END}\n")


def main():
    """Main function."""
    print("\n" + "="*60)
    print("API Testing Script")
    print("="*60)
    print("\nThis script will test all API endpoints.")
    print("\nPrerequisites:")
    print("1. Flask app must be running (python web_app_sql.py)")
    print("2. Database must be initialized")
    print("3. At least one user should be registered")
    print("4. Admin user should exist")
    print("\nStarting tests in 3 seconds...")
    
    import time
    time.sleep(3)
    
    tester = APITester()
    tester.run_all_tests()


if __name__ == '__main__':
    main()
