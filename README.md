# 📧 Job Email Classifier

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> Never miss an important job application email again!

A simple, free, and privacy-focused tool that automatically organizes your job-related emails using AI. Runs entirely on your machine with Groq's free API.

## ✨ Features

- 🤖 **AI-Powered Classification** - Uses Groq's fast LLM API (free tier available)
- 🏷️ **Auto-Labeling** - Automatically creates and applies Gmail labels
- 🔒 **Privacy First** - All processing happens locally, emails never leave your machine
- 🎯 **Smart Filtering** - Distinguishes real applications from marketing emails
- ⚡ **Fast & Simple** - No complex setup, no local models to download
- 🆓 **Completely Free** - Uses free Groq API and Gmail API

## 📋 What It Does

Automatically categorizes your job emails into:

- **🚀 Seeds Planted** - Confirmations when you submit applications
- **⚡ Action Required** - Interviews, offers, urgent follow-ups
- **📦 Inbox Clutter** - Job alerts, marketing, rejections

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Gmail account
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/job-email-classifier.git
   cd job-email-classifier
   ```

2. **Quick setup (recommended)**
   ```bash
   python setup.py
   ```

3. **Manual setup**
   ```bash
   # Install dependencies
   uv sync  # or pip install -r requirements.txt
   
   # Create environment file
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

4. **Setup Gmail API**
   
   a. Go to [Google Cloud Console](https://console.cloud.google.com/)
   
   b. Create a new project
   
   c. Enable Gmail API
   
   d. Create OAuth 2.0 credentials (Desktop application)
   
   e. Download credentials and save as `credentials.json` in project folder

5. **Verify setup**
   ```bash
   python test_setup.py
   ```

### Usage

#### Option 1: Web Interface (Recommended)

```bash
# Using uv
uv run streamlit run app.py

# Or using python
python -m streamlit run app.py
```

Then:
1. Click "Connect to Gmail" and authorize
2. Click "Classify Emails" to process your inbox
3. Enable "Auto-Process" for continuous monitoring

#### Option 2: Background Service

```bash
# Using uv
uv run python background.py

# Or using python
python background.py

# With custom settings
python background.py --days 7 --interval 30
```

Runs continuously in the background, checking every 15 minutes by default.

## 🎯 How It Works

1. **Connects to Gmail** - Securely authenticates using OAuth2
2. **Fetches Emails** - Gets recent unread/unlabeled emails
3. **AI Classification** - Groq's LLM analyzes email content
4. **Auto-Labels** - Applies appropriate Gmail labels
5. **Continuous Monitoring** - Optionally runs in background

## 📁 Project Structure

```
job-email-classifier/
├── app.py              # Streamlit web interface
├── background.py       # Background monitoring service
├── gmail_client.py     # Gmail API wrapper
├── classifier.py       # Groq-based email classifier
├── setup.py            # Quick setup script
├── test_setup.py       # Setup verification
├── requirements.txt    # Dependencies
└── docs/
    ├── GETTING_STARTED.md
    ├── SETUP.md
    └── CONTRIBUTING.md
```

**Files you need to create:**
- `credentials.json` - Download from Google Cloud Console
- `.env` - Create from `.env.example` with your Groq API key

## 🔧 Configuration

Edit these settings in the code:

- **Check Interval**: Change `CHECK_INTERVAL_MINUTES` in `background.py`
- **Days to Fetch**: Modify `days` parameter in fetch functions
- **Model**: Change `model` in `GroqClassifier` (default: openai/gpt-oss-20b)
- **Labels**: Modify `LABELS` dict in `classifier.py`

## 🤝 Contributing

Contributions are welcome! This project is built to help job seekers. Feel free to:

- Report bugs
- Suggest features
- Submit pull requests
- Share with others who might benefit

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📝 License

MIT License - feel free to use, modify, and share!

## 🙏 Acknowledgments

Built for the job-seeking community. If this helps you land your dream job, consider:
- ⭐ Starring the repo
- 🐛 Reporting issues
- 🤝 Contributing improvements
- 📢 Sharing with others

## 🔐 Privacy & Security

- Your emails are processed locally
- Only Gmail API and Groq API are used
- No data is stored or sent to third parties
- Credentials are stored securely on your machine
- Open source - audit the code yourself!

---

Made for job seekers everywhere. Good luck with your applications! 🍀
