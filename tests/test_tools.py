"""
Unit tests for Financial Advisor AI Agent tools.

Run with: pytest tests/test_tools.py -v
"""

import pytest
from tools.stock_tool import get_stock_data
from tools.sentiment_tool import analyze_sentiment
from tools.calculator_tool import safe_calculate
from tools.wikipedia_tool import search_wikipedia


class TestStockTool:
    """Tests for stock data retrieval tool."""
    
    def test_valid_stock_ticker(self):
        """Test with a valid stock ticker."""
        result = get_stock_data("AAPL")
        assert "AAPL" in result
        assert "Current Price" in result
        assert "❌" not in result  # Should not contain error
    
    def test_crypto_ticker(self):
        """Test with a cryptocurrency ticker."""
        result = get_stock_data("BTC-USD")
        assert "BTC-USD" in result or "Bitcoin" in result
        assert "Current Price" in result
    
    def test_invalid_ticker(self):
        """Test with an invalid ticker."""
        result = get_stock_data("INVALIDTICKER123")
        assert "❌" in result or "No data found" in result.lower()
    
    def test_empty_ticker(self):
        """Test with empty ticker."""
        result = get_stock_data("")
        assert "❌" in result or "error" in result.lower()


class TestSentimentTool:
    """Tests for sentiment analysis tool."""
    
    def test_positive_sentiment(self):
        """Test positive sentiment."""
        result = analyze_sentiment("Stock market rallied today with record gains!")
        assert "Positive" in result
        assert "Compound Score" in result
    
    def test_negative_sentiment(self):
        """Test negative sentiment."""
        result = analyze_sentiment("Stock market crashed with massive losses")
        assert "Negative" in result
        assert "Compound Score" in result
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment."""
        result = analyze_sentiment("The market opened today")
        assert "Neutral" in result or "neutral" in result
    
    def test_empty_text(self):
        """Test with empty text."""
        result = analyze_sentiment("")
        assert "❌" in result or "error" in result.lower()


class TestCalculatorTool:
    """Tests for calculator tool."""
    
    def test_percentage_calculation(self):
        """Test percentage calculation."""
        result = safe_calculate("15% of 10000")
        assert "1500" in result
        assert "Result" in result
    
    def test_basic_arithmetic(self):
        """Test basic arithmetic."""
        result = safe_calculate("100 + 200")
        assert "300" in result
    
    def test_complex_expression(self):
        """Test complex expression."""
        result = safe_calculate("(5000 - 1000) / 12")
        assert "333" in result  # Should be around 333.33
    
    def test_division_by_zero(self):
        """Test division by zero error handling."""
        result = safe_calculate("100 / 0")
        assert "❌" in result
        assert "zero" in result.lower()
    
    def test_invalid_expression(self):
        """Test invalid expression."""
        result = safe_calculate("invalid expression !!!")
        assert "❌" in result


class TestWikipediaTool:
    """Tests for Wikipedia search tool."""
    
    def test_valid_search(self):
        """Test valid Wikipedia search."""
        result = search_wikipedia("Warren Buffett")
        assert "Warren" in result or "Buffett" in result
        assert "Wikipedia Summary" in result
    
    def test_financial_concept(self):
        """Test searching for financial concept."""
        result = search_wikipedia("Stock market")
        assert "stock" in result.lower()
    
    def test_invalid_search(self):
        """Test with invalid search query."""
        result = search_wikipedia("InvalidQueryThatDoesNotExist123456789")
        assert "❌" in result or "not found" in result.lower()
    
    def test_empty_search(self):
        """Test with empty search."""
        result = search_wikipedia("")
        assert "❌" in result or "error" in result.lower()


class TestIntegration:
    """Integration tests combining multiple tools."""
    
    def test_stock_and_sentiment(self):
        """Test combining stock data retrieval and sentiment analysis."""
        stock_result = get_stock_data("TSLA")
        assert "TSLA" in stock_result
        
        sentiment_result = analyze_sentiment("Tesla stock surged today")
        assert "Sentiment" in sentiment_result
    
    def test_calculator_and_wikipedia(self):
        """Test calculator and Wikipedia tools."""
        calc_result = safe_calculate("20% of 5000")
        assert "1000" in calc_result
        
        wiki_result = search_wikipedia("Budgeting")
        assert "budget" in wiki_result.lower()


# Performance tests
class TestPerformance:
    """Basic performance tests."""
    
    def test_stock_tool_speed(self):
        """Test stock tool response time."""
        import time
        start = time.time()
        get_stock_data("AAPL")
        duration = time.time() - start
        assert duration < 10  # Should complete within 10 seconds
    
    def test_sentiment_tool_speed(self):
        """Test sentiment tool response time."""
        import time
        start = time.time()
        analyze_sentiment("Market is bullish today")
        duration = time.time() - start
        assert duration < 5  # Should complete within 5 seconds


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

