"""
Agent setup and configuration for the Financial Advisor AI Agent.
"""

import os
from typing import Optional, List
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from dotenv import load_dotenv

from tools import (
    get_stock_tool,
    get_sentiment_tool,
    get_calculator_tool,
    get_wikipedia_tool
)
from .prompts import get_react_prompt


def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()


def get_api_key() -> Optional[str]:
    """
    Get API key from environment or Streamlit secrets.
    Supports Gemini, Blackbox AI, and OpenAI.
    
    Returns:
        API key or None if not found
    """
    # Try Gemini key first, then Blackbox, then OpenAI
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("BLACKBOX_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    # Try to get from Streamlit secrets if available
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("BLACKBOX_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        except:
            pass
    
    return api_key


def initialize_tools() -> List[Tool]:
    """
    Initialize all tools for the agent.
    
    Returns:
        List of LangChain tools
    """
    tools = [
        get_stock_tool(),
        get_sentiment_tool(),
        get_calculator_tool(),
        get_wikipedia_tool()
    ]
    return tools


def create_financial_agent(
    api_key: Optional[str] = None,
    model: str = "gemini-2.0-flash-exp",
    temperature: float = 0,
    max_iterations: int = 5,
    verbose: bool = True,
    provider: str = "gemini"
) -> AgentExecutor:
    """
    Create and configure the Financial Advisor AI Agent.
    
    Args:
        api_key: API key (if None, will try to load from environment)
        model: Model to use (default: gemini-2.0-flash-exp)
        temperature: LLM temperature (default: 0 for consistency)
        max_iterations: Maximum agent iterations (default: 5)
        verbose: Whether to show agent reasoning (default: True)
        provider: AI provider - "gemini", "blackbox", or "openai" (default: gemini)
        
    Returns:
        AgentExecutor: Configured LangChain agent
        
    Raises:
        ValueError: If API key is not provided or found
    """
    # Load environment variables
    load_environment()
    
    # Get API key
    if not api_key:
        api_key = get_api_key()
    
    if not api_key:
        raise ValueError(
            "API key not found. Please set GEMINI_API_KEY in your "
            ".env file or Streamlit secrets."
        )
    
    # Initialize LLM based on provider
    if provider.lower() == "gemini":
        # Google Gemini AI configuration
        llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature,
            convert_system_message_to_human=True  # Required for ReAct agents
        )
    else:
        raise ValueError(f"Provider '{provider}' not supported. Use 'gemini'.")
    
    # Initialize tools
    tools = initialize_tools()
    
    # Get custom prompt
    prompt = get_react_prompt()
    
    # Create ReAct agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        max_iterations=max_iterations,
        handle_parsing_errors=True,
        return_intermediate_steps=False
    )
    
    return agent_executor


def test_agent(agent_executor: AgentExecutor, query: str) -> dict:
    """
    Test the agent with a sample query.
    
    Args:
        agent_executor: Configured agent executor
        query: Test query
        
    Returns:
        Agent response
    """
    try:
        response = agent_executor.invoke({"input": query})
        return response
    except Exception as e:
        return {"error": str(e)}


# For testing purposes
if __name__ == "__main__":
    print("Initializing Financial Advisor AI Agent...")
    
    try:
        # Create agent
        agent = create_financial_agent(model="gpt-3.5-turbo")
        
        print("✅ Agent initialized successfully!")
        print("\n" + "="*60)
        
        # Test queries
        test_queries = [
            "What's the current price of Apple stock?",
            "Calculate 30% of 5000",
            "Analyze sentiment: Stock market crashed today"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🧪 Test {i}: {query}")
            print("-"*60)
            
            response = test_agent(agent, query)
            
            if "error" in response:
                print(f"❌ Error: {response['error']}")
            else:
                print(f"✅ Response: {response.get('output', 'No output')}")
            
            print("="*60)
            
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        print("\n💡 Make sure your OPENAI_API_KEY is set in .env file")

