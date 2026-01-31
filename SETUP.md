# 🛠️ Setup Guide

Complete step-by-step setup instructions for Job Email Classifier.

## Prerequisites

- Python 3.10 or higher
- Gmail account
- Internet connection

## Step 1: Install Python Dependencies

### Option A: Using uv (Recommended - Faster)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### Option B: Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Get Groq API Key (Free)

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Click "Create API Key"
5. Copy the API key

## Step 3: Setup Groq API Key

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# GROQ_API_KEY=your_actual_api_key_here
```

Or create it manually:

```bash
echo "GROQ_API_KEY=your_actual_api_key_here" > .env
```

## Step 4: Setup Gmail API

### 4.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name (e.g., "Job Email Classifier")
4. Click "Create"

### 4.2 Enable Gmail API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on it and click "Enable"

### 4.3 Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: Job Email Classifier
   - User support email: your email
   - Developer contact: your email
   - Click "Save and Continue"
   - Scopes: Skip (click "Save and Continue")
   - Test users: Add your Gmail address
   - Click "Save and Continue"
4. Back to Create OAuth client ID:
   - Application type: Desktop app
   - Name: Job Email Classifier
   - Click "Create"
5. Download the credentials JSON file
6. Rename it to `credentials.json`
7. Place it in the project root directory

### 4.4 Add Test Users (Important!)

Since the app is in testing mode:

1. Go to "OAuth consent screen"
2. Scroll to "Test users"
3. Click "Add Users"
4. Add your Gmail address
5. Click "Save"

## Step 5: Verify Setup

Check that you have these files:

```
job-email-classifier/
├── .env                 # Your Groq API key
├── credentials.json     # Gmail OAuth credentials
├── app.py              # Streamlit app
├── background.py       # Background service
└── ...
```

## Step 6: First Run

### Test with Streamlit UI

```bash
# Using uv
uv run streamlit run app.py

# Or using python
python -m streamlit run app.py
```

1. Click "Connect to Gmail"
2. Browser will open for authorization
3. Select your Gmail account
4. Click "Continue" (ignore warning about unverified app)
5. Click "Allow" to grant permissions
6. Return to Streamlit app
7. Click "Classify Emails"

### Or Test with Background Service

```bash
# Using uv
uv run python background.py

# Or using python
python background.py
```

## Troubleshooting

### "credentials.json not found"

- Make sure you downloaded the OAuth credentials
- Rename the file to exactly `credentials.json`
- Place it in the project root directory

### "GROQ_API_KEY not found"

- Make sure `.env` file exists
- Check that the API key is correct
- No quotes needed around the key

### "This app isn't verified" warning

- This is normal for personal projects
- Click "Advanced" → "Go to Job Email Classifier (unsafe)"
- This is safe because it's your own app

### Gmail API quota exceeded

- Free tier: 1 billion quota units/day
- Each email fetch uses ~5 units
- You can process ~200 million emails/day
- Reduce `MAX_EMAILS` if needed

### Authentication keeps failing

1. Delete `token.json` file
2. Try authenticating again
3. Make sure your email is added as a test user

## Configuration

Edit these in `background.py` or set as environment variables:

```bash
# Check interval (minutes)
CHECK_INTERVAL_MINUTES=15

# Days to look back
DAYS_TO_CHECK=1

# Max emails per check
MAX_EMAILS=50
```

## Next Steps

- ⭐ Star the repo if it helps you!
- 🐛 Report issues on GitHub
- 🤝 Contribute improvements
- 📢 Share with other job seekers

## Need Help?

- Check [README.md](README.md) for FAQ
- Open an issue on GitHub
- Review the code - it's simple and well-commented!

---

Good luck with your job search! 🍀
