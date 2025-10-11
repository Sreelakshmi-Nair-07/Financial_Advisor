"""
Sentiment Analysis Tool - Analyzes financial text sentiment using NLTK VADER.
"""

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional


class SentimentInput(BaseModel):
    """Input schema for sentiment analysis tool."""
    text: str = Field(description="Text to analyze for sentiment (e.g., financial news, market commentary)")


def ensure_vader_downloaded():
    """Ensure VADER lexicon is downloaded."""
    try:
        # Try to create SentimentIntensityAnalyzer
        # If it fails, download the lexicon
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        print("Downloading VADER lexicon...")
        nltk.download('vader_lexicon', quiet=True)


def analyze_sentiment(text: str) -> str:
    """
    Analyze sentiment of financial text using VADER.
    
    Args:
        text: Text to analyze (financial news, market commentary, etc.)
        
    Returns:
        Formatted string with sentiment analysis results
    """
    try:
        # Ensure VADER is available
        ensure_vader_downloaded()
        
        # Validate input
        if not text or not text.strip():
            return "❌ Error: Please provide text to analyze."
        
        text = text.strip()
        
        # Initialize VADER sentiment analyzer
        sia = SentimentIntensityAnalyzer()
        
        # Get sentiment scores
        scores = sia.polarity_scores(text)
        
        # Extract individual scores
        compound = scores['compound']
        positive = scores['pos']
        negative = scores['neg']
        neutral = scores['neu']
        
        # Determine overall sentiment
        if compound >= 0.05:
            sentiment = "Positive 😊"
            emoji = "📈"
            interpretation = "The text expresses positive sentiment."
        elif compound <= -0.05:
            sentiment = "Negative 😟"
            emoji = "📉"
            interpretation = "The text expresses negative sentiment."
        else:
            sentiment = "Neutral 😐"
            emoji = "➡️"
            interpretation = "The text expresses neutral sentiment."
        
        # Add strength indicator
        abs_compound = abs(compound)
        if abs_compound >= 0.75:
            strength = "Very Strong"
        elif abs_compound >= 0.5:
            strength = "Strong"
        elif abs_compound >= 0.25:
            strength = "Moderate"
        else:
            strength = "Weak"
        
        # Format the response
        response = f"""
{emoji} **Sentiment Analysis Result**

📝 **Analyzed Text**: "{text[:100]}{'...' if len(text) > 100 else ''}"

**Overall Sentiment**: {sentiment}
**Strength**: {strength}

**Detailed Scores**:
- Compound Score: {compound:.3f} (range: -1 to +1)
- Positive: {positive:.1%}
- Negative: {negative:.1%}
- Neutral: {neutral:.1%}

**Interpretation**: {interpretation}

**Score Guide**:
- Compound ≥ 0.05: Positive sentiment
- Compound ≤ -0.05: Negative sentiment
- -0.05 < Compound < 0.05: Neutral sentiment

**Financial Context**:
"""
        
        # Add financial interpretation
        if compound >= 0.5:
            response += "- Strong bullish sentiment detected\n"
            response += "- May indicate positive market outlook\n"
        elif compound >= 0.05:
            response += "- Mild bullish sentiment detected\n"
            response += "- Generally favorable market tone\n"
        elif compound <= -0.5:
            response += "- Strong bearish sentiment detected\n"
            response += "- May indicate negative market outlook\n"
        elif compound <= -0.05:
            response += "- Mild bearish sentiment detected\n"
            response += "- Some market concerns present\n"
        else:
            response += "- Balanced sentiment detected\n"
            response += "- No clear directional bias\n"
        
        return response
        
    except Exception as e:
        return f"❌ Error analyzing sentiment: {str(e)}"


def get_sentiment_tool() -> Tool:
    """
    Create and return the sentiment analysis tool for LangChain agent.
    
    Returns:
        Tool: LangChain Tool for sentiment analysis
    """
    return Tool(
        name="Sentiment_Analyzer",
        func=analyze_sentiment,
        description="""
        Useful for analyzing sentiment of financial text, news headlines, or market commentary.
        Input should be text you want to analyze (e.g., "Stock market crashed today" or "Company reports record profits").
        Returns sentiment classification (Positive/Negative/Neutral), confidence scores, and interpretation.
        Use this tool when users want to understand the sentiment or tone of financial news or statements.
        """,
        args_schema=SentimentInput
    )


# For testing purposes
if __name__ == "__main__":
    # Test with various financial texts
    test_texts = [
        "Stock market rallied today with record gains!",
        "Company reports massive losses and layoffs",
        "Market opens flat with mixed signals",
        "Bitcoin surges to new all-time high",
        "Economic indicators show declining growth"
    ]
    
    for text in test_texts:
        print(f"\n{'='*60}")
        print(f"Testing: {text}")
        print('='*60)
        result = analyze_sentiment(text)
        print(result)

