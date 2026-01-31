# 🤝 Contributing to Job Email Classifier

Thank you for considering contributing! This project is built to help job seekers, and every contribution makes a difference.

## How to Contribute

### 🐛 Report Bugs

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)

### 💡 Suggest Features

Have an idea? Open an issue with:
- Clear description of the feature
- Why it would be helpful
- How it might work

### 🔧 Submit Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/job-email-classifier.git
cd job-email-classifier

# Install dependencies
uv sync

# Create .env with your API keys
cp .env.example .env
# Edit .env with your keys

# Run tests (if available)
uv run pytest

# Run the app
uv run streamlit run app.py
```

## Code Style

- Keep it simple and readable
- Add comments for complex logic
- Follow existing code patterns
- Use type hints where helpful

## Testing

Before submitting:
- Test with real Gmail account
- Test both UI and background service
- Verify classification accuracy
- Check error handling

## Areas We Need Help

- 📝 Documentation improvements
- 🐛 Bug fixes
- ✨ New features (keep it simple!)
- 🌍 Internationalization
- 🧪 Test coverage
- 📱 Mobile-friendly UI

## Questions?

Open an issue or discussion - we're happy to help!

## Code of Conduct

Be kind, respectful, and helpful. We're all here to help job seekers succeed.

---

Thank you for contributing! 🙏
