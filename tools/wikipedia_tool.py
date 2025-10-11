"""
Wikipedia Tool - Searches Wikipedia for financial and general knowledge.
"""

import wikipediaapi
from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field


class WikipediaInput(BaseModel):
    """Input schema for Wikipedia tool."""
    query: str = Field(description="Search query for Wikipedia (e.g., 'Warren Buffett', 'diversification', 'Tesla')")


def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for information.
    
    Args:
        query: Search query (person, concept, company, etc.)
        
    Returns:
        Summary from Wikipedia or error message
    """
    try:
        # Validate input
        if not query or not query.strip():
            return "❌ Error: Please provide a search query."
        
        query = query.strip()
        
        # Initialize Wikipedia API with a user agent
        wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent='FinancialAdvisorAgent/1.0'
        )
        
        # Get the page
        page = wiki.page(query)
        
        # Check if page exists
        if not page.exists():
            # Try to find similar pages
            return f"❌ No Wikipedia page found for '{query}'. Please try a different search term or check the spelling."
        
        # Get summary (first 3 sentences or 500 chars)
        summary = page.summary
        
        # Limit summary length for readability
        if len(summary) > 800:
            summary = summary[:800] + "..."
        
        # Format the response
        response = f"""
📚 **Wikipedia Summary: {page.title}**

{summary}

🔗 **Source**: {page.fullurl}

💡 **Categories**: {', '.join(list(page.categories.keys())[:5]) if page.categories else 'N/A'}
"""
        
        return response
        
    except Exception as e:
        return f"❌ Error searching Wikipedia for '{query}': {str(e)}"


def get_wikipedia_tool() -> Tool:
    """
    Create and return the Wikipedia tool for LangChain agent.
    
    Returns:
        Tool: LangChain Tool for Wikipedia search
    """
    return Tool(
        name="Wikipedia_Search",
        func=search_wikipedia,
        description="""
        Useful for finding information about financial concepts, companies, people, or general knowledge.
        Input should be a search query (e.g., "Warren Buffett", "diversification", "Tesla", "stock market").
        Returns a summary from Wikipedia with key information.
        Use this tool when users ask about definitions, background information, or general knowledge.
        """,
        args_schema=WikipediaInput
    )


# For testing purposes
if __name__ == "__main__":
    # Test with various queries
    test_queries = [
        "Warren Buffett",
        "Diversification (finance)",
        "Tesla, Inc.",
        "Stock market",
        "InvalidQueryThatDoesNotExist123"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing: {query}")
        print('='*60)
        result = search_wikipedia(query)
        print(result)

