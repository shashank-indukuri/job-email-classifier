#!/usr/bin/env python3
"""
Quick setup script for Job Email Classifier
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is 3.10+"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install dependencies using uv or pip"""
    if shutil.which("uv"):
        print("✅ Using uv for dependency management")
        # Create virtual environment if it doesn't exist
        if not os.path.exists(".venv"):
            subprocess.run(["uv", "venv"], check=True)
            print("✅ Created virtual environment (.venv)")
        # Install dependencies in the virtual environment
        subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], check=True)
    else:
        print("⚠️  uv not found, using pip")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("✅ Dependencies installed")

def setup_env_file():
    """Create .env file from template"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env and add your GROQ_API_KEY")
        else:
            with open(".env", "w") as f:
                f.write("GROQ_API_KEY=your_groq_api_key_here\n")
            print("✅ Created .env file")
            print("⚠️  Please add your GROQ_API_KEY to .env")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Job Email Classifier - Setup")
    print("=" * 40)
    
    if not check_python_version():
        sys.exit(1)
    
    try:
        install_dependencies()
        setup_env_file()
        
        print("\n" + "=" * 40)
        print("✅ Setup complete!")
        print("\n📋 Next steps:")
        print("1. Get Groq API key: https://console.groq.com")
        print("2. Edit .env file and add your API key")
        print("3. Get Gmail credentials from Google Cloud Console")
        print("4. Save as credentials.json in this directory")
        print("5. Run: python test_setup.py")
        print("\n🚀 Then start with:")
        print("   uv run streamlit run app.py")
        print("   # or: source .venv/bin/activate && python -m streamlit run app.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
