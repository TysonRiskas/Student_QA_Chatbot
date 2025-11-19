"""
Pre-deployment Security Check
Run before deploying to production

Usage: python pre_deploy_check.py
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check all required environment variables."""
    load_dotenv()
    
    issues = []
    warnings = []
    
    print("="*70)
    print("PRE-DEPLOYMENT SECURITY CHECK")
    print("Student Q&A Chatbot")
    print("="*70)
    print()
    
    # Check SECRET_KEY
    print("Checking SECRET_KEY...")
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        issues.append("❌ SECRET_KEY not set in .env file")
    elif secret_key == 'dev-secret-key-change-in-production':
        issues.append("❌ SECRET_KEY still using default development value!")
    elif len(secret_key) < 32:
        warnings.append("⚠️  SECRET_KEY seems short (recommend 64+ characters)")
    else:
        print("  ✅ SECRET_KEY is set and appears secure")
    
    # Check MISTRAL_API_KEY
    print("Checking MISTRAL_API_KEY...")
    mistral_key = os.getenv('MISTRAL_API_KEY')
    if not mistral_key:
        issues.append("❌ MISTRAL_API_KEY not set in .env file")
    elif mistral_key == 'your_mistral_api_key_here':
        issues.append("❌ MISTRAL_API_KEY still using placeholder value!")
    elif len(mistral_key) < 20:
        warnings.append("⚠️  MISTRAL_API_KEY seems short or invalid")
    else:
        print("  ✅ MISTRAL_API_KEY is set")
    
    # Check .env file exists
    print("Checking .env file...")
    if not os.path.exists('.env'):
        issues.append("❌ .env file not found in project root!")
    else:
        print("  ✅ .env file exists")
    
    # Check .gitignore
    print("Checking .gitignore...")
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' not in gitignore_content:
                issues.append("❌ .env not in .gitignore - secrets may be committed!")
            else:
                print("  ✅ .gitignore includes .env")
    else:
        warnings.append("⚠️  .gitignore file not found")
    
    # Check debug mode (in web_app_sql.py)
    print("Checking debug mode...")
    if os.path.exists('web_app_sql.py'):
        with open('web_app_sql.py', 'r') as f:
            content = f.read()
            if 'debug=True' in content:
                warnings.append("⚠️  Found debug=True in web_app_sql.py - should be False for production")
            else:
                print("  ✅ Debug mode appears to be off")
    
    # Print results
    print()
    print("="*70)
    print("RESULTS")
    print("="*70)
    print()
    
    if not issues and not warnings:
        print("✅ ✅ ✅ ALL CHECKS PASSED! ✅ ✅ ✅")
        print()
        print("Your application is ready for deployment!")
        print()
        print("Next steps:")
        print("  1. Commit your changes: git add . && git commit -m 'Ready for production'")
        print("  2. Push to GitHub: git push origin main")
        print("  3. Deploy to Heroku: git push heroku main")
        print()
        return True
    
    if issues:
        print("🔴 CRITICAL ISSUES - MUST FIX BEFORE DEPLOYMENT:")
        print()
        for issue in issues:
            print(f"  {issue}")
        print()
    
    if warnings:
        print("🟡 WARNINGS - SHOULD REVIEW:")
        print()
        for warning in warnings:
            print(f"  {warning}")
        print()
    
    print("="*70)
    print()
    
    if issues:
        print("❌ DEPLOYMENT BLOCKED")
        print()
        print("Fix critical issues above before deploying.")
        print()
        print("Quick fixes:")
        print("  - Run: python security_setup.py")
        print("  - Choose option 3 (Do both)")
        print("  - Then run this check again")
        print()
    elif warnings:
        print("⚠️  DEPLOYMENT NOT RECOMMENDED")
        print()
        print("Review warnings above. You may proceed but it's not recommended.")
        print()
    
    return len(issues) == 0

def check_heroku_config():
    """Check Heroku configuration."""
    print()
    print("="*70)
    print("HEROKU DEPLOYMENT CHECKLIST")
    print("="*70)
    print()
    print("Before deploying to Heroku, ensure you've set these config vars:")
    print()
    print("  heroku config:set MISTRAL_API_KEY=your_real_api_key")
    print("  heroku config:set SECRET_KEY=your_generated_secret_key")
    print("  heroku config:set SESSION_COOKIE_SECURE=True")
    print("  heroku config:set FLASK_ENV=production")
    print()
    print("Verify with:")
    print("  heroku config")
    print()
    print("="*70)

if __name__ == '__main__':
    print()
    passed = check_environment()
    
    if passed:
        check_heroku_config()
    
    print()
    exit(0 if passed else 1)
