#!/usr/bin/env python3
"""Simple setup verification script"""

import os
import sys


def check_file(filename, description):
    """Check if a file exists"""
    exists = os.path.exists(filename)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filename}")
    return exists


def check_env_var(var_name):
    """Check if environment variable is set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    value = os.getenv(var_name)
    exists = value is not None and value != ""
    status = "✅" if exists else "❌"
    print(f"{status} Environment variable: {var_name}")
    return exists


def test_groq_api():
    """Test Groq API connection"""
    try:
        from classifier import GroqClassifier
        classifier = GroqClassifier()
        print("✅ Groq API: Connected")
        print(f"   Model: {classifier.model}")
        return True
    except Exception as e:
        print(f"❌ Groq API: {e}")
        return False


def test_gmail_credentials():
    """Test Gmail credentials file"""
    try:
        import json
        with open('credentials.json', 'r') as f:
            data = json.load(f)
            if 'installed' in data or 'web' in data:
                print("✅ Gmail credentials: Valid format")
                return True
            else:
                print("❌ Gmail credentials: Invalid format")
                return False
    except Exception as e:
        print(f"❌ Gmail credentials: {e}")
        return False


def main():
    """Run all setup checks"""
    print("🔍 Job Email Classifier - Setup Verification")
    print("=" * 50)
    print()
    
    all_good = True
    
    # Check Python version
    print("📋 Python Version")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (need 3.10+)")
        all_good = False
    print()
    
    # Check required files
    print("📁 Required Files")
    all_good &= check_file('.env', 'Environment config')
    all_good &= check_file('credentials.json', 'Gmail credentials')
    print()
    
    # Check environment variables
    print("🔑 Environment Variables")
    all_good &= check_env_var('GROQ_API_KEY')
    print()
    
    # Check dependencies
    print("📦 Dependencies")
    try:
        import groq
        print("✅ groq")
    except ImportError:
        print("❌ groq (run: uv sync)")
        all_good = False
    
    try:
        import streamlit
        print("✅ streamlit")
    except ImportError:
        print("❌ streamlit (run: uv sync)")
        all_good = False
    
    try:
        from google.oauth2.credentials import Credentials
        print("✅ google-auth")
    except ImportError:
        print("❌ google-auth (run: uv sync)")
        all_good = False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4")
    except ImportError:
        print("❌ beautifulsoup4 (run: uv sync)")
        all_good = False
    print()
    
    # Test API connections
    print("🌐 API Connections")
    all_good &= test_groq_api()
    all_good &= test_gmail_credentials()
    print()
    
    # Summary
    print("=" * 50)
    if all_good:
        print("✅ All checks passed! You're ready to go!")
        print()
        print("Next steps:")
        print("  1. Run web interface: uv run streamlit run app.py")
        print("  2. Or background service: uv run python background.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        print("See SETUP.md for detailed instructions:")
        print("  - Get Groq API key: https://console.groq.com")
        print("  - Setup Gmail API: See SETUP.md Step 4")
        print("  - Install dependencies: uv sync")
    print()


if __name__ == "__main__":
    main()
