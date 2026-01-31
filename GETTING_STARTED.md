# 🎯 Getting Started in 5 Minutes

The fastest way to get Job Email Classifier running.

## ⚡ Super Quick Start

```bash
# 1. Clone and enter directory
git clone https://github.com/yourusername/job-email-classifier.git
cd job-email-classifier

# 2. Run quick start script
./quickstart.sh

# 3. Follow the prompts!
```

That's it! The script will guide you through everything.

## 📋 Manual Setup (If You Prefer)

### Step 1: Install Dependencies (30 seconds)

```bash
# Option A: Using uv (faster)
uv sync

# Option B: Using pip
pip install -r requirements.txt
```

### Step 2: Get Groq API Key (2 minutes)

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up (it's free!)
3. Create an API key
4. Copy it

### Step 3: Configure API Key (10 seconds)

```bash
# Create .env file
cp .env.example .env

# Add your key (replace xxx with your actual key)
echo "GROQ_API_KEY=xxx" > .env
```

### Step 4: Setup Gmail (2 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project
3. Enable Gmail API
4. Create OAuth credentials (Desktop app)
5. Download as `credentials.json`
6. Place in project folder

**Detailed instructions**: See [SETUP.md](SETUP.md) Step 4

### Step 5: Run! (10 seconds)

```bash
# Web interface
uv run streamlit run app.py

# Or background service
uv run python background.py
```

## 🎉 First Time Usage

### Using Web Interface

1. Click "Connect to Gmail"
2. Browser opens → Select your Gmail
3. Click "Continue" (ignore unverified app warning)
4. Click "Allow"
5. Return to app
6. Click "Classify Emails"
7. Watch the magic happen! ✨

### Using Background Service

1. Run `python background.py`
2. Browser opens for Gmail auth (first time only)
3. Authorize the app
4. Service starts monitoring
5. Check `classifier.log` for activity

## 🔍 Verify Everything Works

```bash
# Run verification script
python test_setup.py

# Should see all ✅ checks pass
```

## 📊 What Happens Next?

The classifier will:
1. Fetch recent unlabeled emails
2. Analyze each one with AI
3. Apply Gmail labels:
   - 🚀 Application Sent
   - ⚡ Action Needed
   - 📦 Inbox Clutter
4. Log all activity

## 🎯 Common First-Time Issues

### "credentials.json not found"
→ Download OAuth credentials from Google Cloud Console

### "GROQ_API_KEY not found"
→ Create `.env` file with your API key

### "This app isn't verified"
→ Normal! Click "Advanced" → "Go to app (unsafe)"
→ It's safe because it's YOUR app

### Gmail API quota exceeded
→ Unlikely on first run, but reduce `MAX_EMAILS` if needed

## 💡 Pro Tips

1. **Start with Web Interface**
   - Easier to see what's happening
   - Good for testing

2. **Then Use Background Service**
   - Set it and forget it
   - Runs continuously

3. **Check the Logs**
   - `classifier.log` shows all activity
   - Helpful for debugging

4. **Adjust Settings**
   - Edit `background.py` for check intervals
   - Modify `classifier.py` for classification rules

## 📚 Next Steps

- ⭐ Star the repo if it helps!
- 📖 Read [EXAMPLES.md](EXAMPLES.md) for classification examples
- 🔧 Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) to understand the code
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## 🆘 Need Help?

1. Check [README.md](README.md) FAQ section
2. Review [SETUP.md](SETUP.md) for detailed instructions
3. Open an issue on GitHub
4. Check existing issues for solutions

## 🎊 Success!

Once you see emails being classified and labeled in Gmail, you're all set!

The classifier will help you:
- Never miss interview invitations
- Track application confirmations
- Filter out job alert spam
- Stay organized during your job search

Good luck with your applications! 🍀

---

**Time to first classification**: ~5 minutes  
**Difficulty**: Easy  
**Cost**: $0 (completely free!)
