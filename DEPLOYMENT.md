# 🚀 Deployment Guide - Financial Advisor AI Agent

This guide will walk you through deploying your Financial Advisor AI Agent to Streamlit Cloud.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [x] GitHub account
- [x] OpenAI API key (get from [platform.openai.com](https://platform.openai.com))
- [x] All code tested locally
- [x] requirements.txt with correct dependencies
- [x] .gitignore configured (to prevent committing secrets)

## 🔧 Local Testing

Before deployment, test the application locally:

### 1. Install Dependencies

```bash
cd "Freework 3"
pip install -r requirements.txt
```

### 2. Download NLTK Data

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### 3. Setup Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-key-here
```

### 4. Run the App Locally

```bash
streamlit run app.py
```

The app should open at `http://localhost:8501`

### 5. Test All Features

- ✅ Stock price queries
- ✅ Cryptocurrency queries
- ✅ Sentiment analysis
- ✅ Calculator functions
- ✅ Wikipedia searches
- ✅ Error handling

---

## 🌐 Deploying to Streamlit Cloud

### Step 1: Prepare GitHub Repository

1. **Initialize Git Repository** (if not already done)

```bash
cd "Freework 3"
git init
git add .
git commit -m "Initial commit: Financial Advisor AI Agent"
```

2. **Create GitHub Repository**
   - Go to [github.com](https://github.com)
   - Click "New Repository"
   - Name it: `financial-advisor-ai-agent`
   - Don't initialize with README (we already have one)
   - Create repository

3. **Push to GitHub**

```bash
git remote add origin https://github.com/YOUR_USERNAME/financial-advisor-ai-agent.git
git branch -M main
git push -u origin main
```

**Important**: Verify `.gitignore` includes:
- `.env`
- `.streamlit/secrets.toml`
- `__pycache__/`

### Step 2: Deploy to Streamlit Cloud

1. **Sign in to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Select your repository: `financial-advisor-ai-agent`
   - Branch: `main`
   - Main file path: `app.py`

3. **Configure Advanced Settings**
   - Python version: `3.9` or higher
   - Click "Advanced settings..."

4. **Add Secrets**
   - In the "Secrets" section, add:

```toml
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
```

5. **Deploy**
   - Click "Deploy!"
   - Wait for the app to build (2-5 minutes)

### Step 3: Verify Deployment

Once deployed, test your live app:

1. **Check the URL**: `https://your-app-name.streamlit.app`

2. **Test all features**:
   - Stock queries
   - Sentiment analysis
   - Calculator
   - Wikipedia search
   - Error handling

3. **Monitor Performance**:
   - Check response times (<5 seconds)
   - Verify agent reasoning
   - Test with multiple concurrent users

---

## 🔒 Security Considerations

### API Key Management

1. **Never commit API keys to GitHub**
   - Always use `.env` locally
   - Use Streamlit secrets in production

2. **Use environment variables**
   ```python
   import os
   api_key = os.getenv("OPENAI_API_KEY")
   ```

3. **Rotate keys regularly**
   - Change API keys periodically
   - Update in Streamlit Cloud secrets

### Rate Limiting

Consider implementing rate limiting to prevent abuse:

```python
# In app.py, add rate limiting logic
if st.session_state.total_queries > 100:
    st.warning("Query limit reached. Please try again later.")
```

---

## 📊 Post-Deployment Monitoring

### Monitor These Metrics

1. **Response Time**: Should be <5 seconds
2. **Accuracy**: Target ≥85%
3. **Error Rate**: Should be minimal
4. **API Usage**: Monitor OpenAI costs

### Streamlit Cloud Analytics

- View app analytics in Streamlit Cloud dashboard
- Check:
  - Number of viewers
  - Average session duration
  - Error logs

### Error Logging

Check logs in Streamlit Cloud:
1. Go to your app dashboard
2. Click "Manage app"
3. View logs for errors

---

## 🐛 Troubleshooting

### Common Issues

#### 1. App Won't Start

**Problem**: App fails to build
**Solution**:
- Check `requirements.txt` for correct versions
- Verify Python version compatibility
- Check logs for specific errors

#### 2. API Key Not Working

**Problem**: "API key not found" error
**Solution**:
- Verify secrets are configured in Streamlit Cloud
- Check secret key name matches exactly: `OPENAI_API_KEY`
- Ensure no extra spaces or quotes

#### 3. Slow Response Times

**Problem**: Agent takes >5 seconds to respond
**Solution**:
- Switch to `gpt-3.5-turbo` instead of `gpt-4`
- Implement caching for frequently asked queries
- Reduce `max_iterations` in agent config

#### 4. NLTK Data Missing

**Problem**: "VADER lexicon not found"
**Solution**:
- Add download command to app startup:
```python
import nltk
nltk.download('vader_lexicon', quiet=True)
```

#### 5. Wikipedia Timeout

**Problem**: Wikipedia searches timing out
**Solution**:
- Increase timeout in wikipedia-api calls
- Add error handling for slow connections

---

## 🔄 Updating the Deployed App

To update your deployed app:

1. **Make changes locally**
2. **Test thoroughly**
3. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
4. **Streamlit Cloud auto-deploys** within 1-2 minutes

---

## 💰 Cost Management

### OpenAI API Costs

**Estimate for GPT-3.5-turbo**:
- Input: $0.50 / 1M tokens
- Output: $1.50 / 1M tokens
- Average query: ~500 tokens ($0.001 per query)

**Estimate for GPT-4**:
- Input: $5.00 / 1M tokens
- Output: $15.00 / 1M tokens
- Average query: ~500 tokens ($0.01 per query)

### Cost Optimization Tips

1. **Use GPT-3.5-turbo by default**
2. **Implement caching** for repeated queries
3. **Set token limits** in LLM config
4. **Monitor usage** in OpenAI dashboard

---

## 📈 Scaling Considerations

### For High Traffic (>50K queries)

1. **Implement Redis caching**:
   - Cache stock data (5-minute TTL)
   - Cache Wikipedia results (1-hour TTL)

2. **Add rate limiting**:
   - Per user: 10 queries/minute
   - Per IP: 100 queries/hour

3. **Consider API alternatives**:
   - Use Alpha Vantage for stock data (free tier)
   - Self-host sentiment analysis

4. **Optimize agent config**:
   - Reduce verbose logging
   - Lower max_iterations
   - Use streaming responses

---

## ✅ Deployment Checklist

- [ ] Code tested locally
- [ ] All dependencies in requirements.txt
- [ ] .gitignore configured
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed on Streamlit Cloud
- [ ] Secrets configured (OPENAI_API_KEY)
- [ ] Live app tested with all features
- [ ] Response times checked (<5 seconds)
- [ ] Error handling verified
- [ ] Documentation updated (README.md)
- [ ] Monitoring setup configured

---

## 🆘 Support

### Need Help?

1. **Check Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
2. **LangChain Docs**: [python.langchain.com](https://python.langchain.com)
3. **OpenAI Support**: [help.openai.com](https://help.openai.com)
4. **GitHub Issues**: Create an issue in your repository

---

## 🎉 Success!

Once deployed, your Financial Advisor AI Agent will be live at:
**`https://your-app-name.streamlit.app`**

Share the URL with users and gather feedback for improvements!

---

**Built with ❤️ using LangChain, Streamlit, and OpenAI**

