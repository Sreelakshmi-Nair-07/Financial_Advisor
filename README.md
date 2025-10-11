# 💰 Financial Advisor AI Agent

An AI-powered financial advisor that provides personalized insights on stocks, investments, budgeting, and financial planning using natural language conversations.

## 🌟 Features

- **Stock Market Insights**: Real-time stock prices, historical data, and price trends
- **Cryptocurrency Support**: Track Bitcoin, Ethereum, and other cryptocurrencies
- **Sentiment Analysis**: Analyze financial news and market sentiment using NLTK VADER
- **Budgeting Help**: Get personalized budgeting recommendations and calculations
- **Financial Knowledge**: Access financial concepts via Wikipedia integration
- **Conversational Interface**: Natural language interaction powered by Google Gemini AI
- **Free to Use**: 100% free with Google Gemini API (no credit card required)
- **Multiple Model Options**: Choose from gemini-2.0-flash-exp, gemini-1.5-flash, or gemini-1.5-pro

## 🏗️ Architecture

- **Frontend**: Streamlit (Low-code UI framework)
- **Agent Framework**: LangChain with ReAct architecture
- **LLM**: Google Gemini (gemini-2.0-flash-exp, gemini-1.5-flash, gemini-1.5-pro)
- **Tools**:
  - yfinance (Stock data)
  - NLTK VADER (Sentiment analysis)
  - Wikipedia API (Financial knowledge)
  - Calculator (Budget calculations)

## 📋 Requirements

- Python 3.9+
- Google Gemini API key (FREE - get it from [Google AI Studio](https://aistudio.google.com/apikey))
- Internet connection for real-time data

## 🆓 Why Google Gemini?

- **100% Free**: No credit card required, generous daily limits
- **High Performance**: Fast response times with advanced reasoning
- **Multiple Models**: Choose the right model for your needs
  - `gemini-2.0-flash-exp`: Latest and fastest (recommended)
  - `gemini-1.5-flash`: Fast and efficient
  - `gemini-1.5-pro`: Most capable for complex queries
- **Easy Setup**: Get your API key in minutes from [Google AI Studio](https://aistudio.google.com/apikey)
- **Generous Limits**: 1,500 requests per day, 1 million tokens per day

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Financial_Advisor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download NLTK Data

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### 4. Get Your FREE Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with AIza...)

### 5. Configure Environment

**Option A: Environment File**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google Gemini API key
# GEMINI_API_KEY=AIza...
```

**Option B: Streamlit Secrets (for deployment)**
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "AIza..."
```

### 6. Run the Application

**Windows:**
```bash
# Double-click start_app.bat or run:
python -m streamlit run app.py
```

**Linux/Mac:**
```bash
# Run the shell script or:
python -m streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 💡 Usage Examples

Try these queries with the AI agent:

- "What's the current price of Apple stock?"
- "Show me the outlook for Tesla"
- "What's Bitcoin trading at today?"
- "Help me budget $5000/month with 30% savings"
- "Analyze this sentiment: 'Stock market rallied today'"
- "Who is Warren Buffett?"
- "Calculate 15% of $10,000"

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Test individual tools:

```bash
pytest tests/test_tools.py -v
```

## 📁 Project Structure

```
Financial_Advisor/
├── app.py                      # Main Streamlit application
├── tools/                      # Custom LangChain tools
│   ├── __init__.py
│   ├── stock_tool.py          # yfinance integration
│   ├── sentiment_tool.py      # VADER sentiment analysis
│   ├── calculator_tool.py     # Calculator functionality
│   └── wikipedia_tool.py      # Wikipedia search
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── agent_setup.py         # Agent configuration
│   └── prompts.py             # Custom prompts
├── tests/                      # Test files
│   ├── __init__.py
│   ├── test_tools.py
│   └── test_queries.csv
├── .streamlit/                 # Streamlit configuration
│   └── config.toml
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore file
├── start_app.bat              # Windows startup script (excluded from git)
├── start_app.sh               # Linux/Mac startup script (excluded from git)
├── QUICKSTART.md              # Quick start guide
├── DEPLOYMENT.md              # Deployment instructions
└── README.md                  # This file
```

## 🔒 Security

- Never commit your `.env` file or API keys
- Use Streamlit secrets for deployment
- API keys are loaded from environment variables only
- Google Gemini API keys are free and don't require credit card information

## ⚠️ Disclaimer

**This application is for informational and educational purposes only.**

The financial insights provided by this AI agent should NOT be considered professional financial advice. Always:
- Consult with a certified financial advisor for investment decisions
- Do your own research before making financial commitments
- Understand that past performance doesn't guarantee future results
- Be aware of the risks involved in investing

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your `GEMINI_API_KEY` in Secrets management
5. Deploy!

### Streamlit Secrets Format

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "AIza..."
```

## 🎯 Performance

- **Target Response Time**: <5 seconds
- **Accuracy Target**: ≥85%
- **Scalability**: Designed to handle 50K+ queries

## 🛠️ Troubleshooting

### Common Issues

**Slow responses?**
- Check your internet connection
- Consider using gemini-1.5-flash instead of gemini-1.5-pro for faster responses
- Stock data is cached for 5 minutes

**Agent not working?**
- Verify your GEMINI_API_KEY is set correctly
- Check that all dependencies are installed
- Review logs for specific error messages
- Ensure you have a valid Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

**Invalid stock ticker?**
- Ensure ticker symbols are valid (e.g., AAPL, TSLA)
- Try adding exchange suffix for international stocks

## 📚 Resources

- [LangChain Documentation](https://python.langchain.com/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Google AI Studio](https://aistudio.google.com/) - Get your free API key

## 📄 License

MIT License - feel free to use this project for learning and development.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using LangChain, Streamlit, and Google Gemini**

