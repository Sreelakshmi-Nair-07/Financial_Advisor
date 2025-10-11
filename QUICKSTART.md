# ⚡ Quick Start Guide

Get your Financial Advisor AI Agent running in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies (2 minutes)

```bash
cd "Freework 3"
pip install -r requirements.txt
```

### 2. Download NLTK Data (30 seconds)

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### 3. Configure API Key (1 minute)

Option A - Using environment file:
```bash
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here
```

Option B - Using Streamlit secrets:
```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and add your API key
```

### 4. Run the App (30 seconds)

```bash
streamlit run app.py
```

That's it! The app opens at `http://localhost:8501` 🎉

---

## 🧪 Quick Test

Try these queries in the app:

1. **Stock**: "What's the price of Apple stock?"
2. **Crypto**: "Bitcoin price today"
3. **Sentiment**: "Analyze sentiment: Market rallied today"
4. **Budget**: "Calculate 30% of 5000"
5. **Knowledge**: "Who is Warren Buffett?"

---

## 🐛 Quick Troubleshooting

**Problem**: "API key not found"
→ **Fix**: Set `OPENAI_API_KEY` in `.env` or provide in sidebar

**Problem**: "VADER lexicon not found"
→ **Fix**: Run `python -c "import nltk; nltk.download('vader_lexicon')"`

**Problem**: "Module not found"
→ **Fix**: Run `pip install -r requirements.txt`

---

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) to deploy to Streamlit Cloud
- Review [PROJECT_PLAN.md](PROJECT_PLAN.md) for architecture details

---

**Need help?** Create an issue on GitHub or check the documentation.

