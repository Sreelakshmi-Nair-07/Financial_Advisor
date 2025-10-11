"""
Stock Tool - Fetches real-time stock and cryptocurrency data using yfinance.
"""

import yfinance as yf
from datetime import datetime, timedelta
from typing import Optional
from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field


class StockInput(BaseModel):
    """Input schema for stock tool."""
    ticker: str = Field(description="Stock ticker symbol (e.g., AAPL, TSLA) or crypto symbol (e.g., BTC-USD)")


def get_stock_data(ticker: str) -> str:
    """
    Fetch stock or cryptocurrency data using yfinance.
    
    Args:
        ticker: Stock ticker symbol (e.g., AAPL, TSLA, BTC-USD, ETH-USD)
        
    Returns:
        Formatted string with stock information including price, change, and recent history
    """
    try:
        # Clean up ticker symbol
        ticker = ticker.strip().upper()
        
        # Create ticker object
        stock = yf.Ticker(ticker)
        
        # Get basic info
        info = stock.info
        
        # Get historical data (last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            return f"❌ No data found for ticker '{ticker}'. Please verify the ticker symbol is correct."
        
        # Get current price (most recent close)
        current_price = hist['Close'].iloc[-1]
        
        # Calculate price change
        if len(hist) > 1:
            prev_price = hist['Close'].iloc[0]
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price) * 100
        else:
            price_change = 0
            price_change_pct = 0
        
        # Get volume
        current_volume = hist['Volume'].iloc[-1]
        
        # Determine if it's a crypto
        is_crypto = '-USD' in ticker or ticker in ['BTC', 'ETH', 'DOGE']
        asset_type = "Cryptocurrency" if is_crypto else "Stock"
        
        # Get company name if available
        company_name = info.get('longName', info.get('shortName', ticker))
        
        # Format the response
        response = f"""
📊 **{asset_type} Information: {company_name} ({ticker})**

💵 **Current Price**: ${current_price:.2f}
📈 **7-Day Change**: ${price_change:+.2f} ({price_change_pct:+.2f}%)
📊 **Volume**: {current_volume:,.0f}
📅 **Last Updated**: {hist.index[-1].strftime('%Y-%m-%d')}

**7-Day Price Range**:
- High: ${hist['High'].max():.2f}
- Low: ${hist['Low'].min():.2f}

**Recent Performance**:
"""
        
        # Add last 5 days of data
        for i in range(min(5, len(hist))):
            idx = -(i+1)
            date = hist.index[idx].strftime('%Y-%m-%d')
            close = hist['Close'].iloc[idx]
            response += f"- {date}: ${close:.2f}\n"
        
        # Add trend indicator
        if price_change_pct > 5:
            response += "\n🚀 **Trend**: Strong upward momentum"
        elif price_change_pct > 0:
            response += "\n📈 **Trend**: Positive movement"
        elif price_change_pct > -5:
            response += "\n📉 **Trend**: Slight decline"
        else:
            response += "\n⚠️ **Trend**: Significant decline"
        
        # Add market cap if available
        if 'marketCap' in info and info['marketCap']:
            market_cap = info['marketCap']
            response += f"\n💰 **Market Cap**: ${market_cap:,.0f}"
        
        # Add additional info for stocks
        if not is_crypto:
            if 'sector' in info and info['sector']:
                response += f"\n🏢 **Sector**: {info['sector']}"
            if 'industry' in info and info['industry']:
                response += f"\n🔧 **Industry**: {info['industry']}"
        
        return response
        
    except Exception as e:
        return f"❌ Error fetching data for '{ticker}': {str(e)}. Please verify the ticker symbol is correct and try again."


def get_stock_tool() -> Tool:
    """
    Create and return the stock tool for LangChain agent.
    
    Returns:
        Tool: LangChain Tool for stock data retrieval
    """
    return Tool(
        name="Stock_Data",
        func=get_stock_data,
        description="""
        Useful for getting real-time stock prices, cryptocurrency prices, and financial data.
        Input should be a stock ticker symbol (e.g., AAPL for Apple, TSLA for Tesla) 
        or cryptocurrency symbol (e.g., BTC-USD for Bitcoin, ETH-USD for Ethereum).
        Returns current price, 7-day price change, volume, and recent price history.
        Use this tool when users ask about stock prices, stock outlooks, or cryptocurrency prices.
        """,
        args_schema=StockInput
    )


# For testing purposes
if __name__ == "__main__":
    # Test with various tickers
    test_tickers = ["AAPL", "TSLA", "BTC-USD", "INVALID"]
    
    for ticker in test_tickers:
        print(f"\n{'='*60}")
        print(f"Testing: {ticker}")
        print('='*60)
        result = get_stock_data(ticker)
        print(result)

