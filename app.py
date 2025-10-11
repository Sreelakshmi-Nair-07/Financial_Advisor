"""
Financial Advisor AI Agent - Main Streamlit Application

A conversational AI agent that provides personalized financial insights using:
- Real-time stock data (yfinance)
- Sentiment analysis (NLTK VADER)
- Wikipedia knowledge
- Calculator for budgeting

Built with LangChain ReAct architecture and Streamlit.
"""

import streamlit as st
import os
from datetime import datetime
from typing import Optional

# Import utilities
from utils.agent_setup import create_financial_agent, get_api_key
from utils.prompts import get_welcome_message, get_error_message


# Page configuration
st.set_page_config(
    page_title="Financial Advisor AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .disclaimer {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_agent(api_key: str, model: str = "gemini-2.0-flash-exp", provider: str = "gemini"):
    """
    Initialize the AI agent with caching for performance.
    
    Args:
        api_key: API key (Google Gemini)
        model: Model to use (gemini-2.0-flash-exp, gemini-1.5-pro, etc.)
        provider: AI provider (gemini)
        
    Returns:
        Configured agent executor
    """
    try:
        agent = create_financial_agent(
            api_key=api_key,
            model=model,
            temperature=0,
            max_iterations=5,
            verbose=False,  # Set to False for production
            provider=provider
        )
        return agent
    except Exception as e:
        st.error(f"Error initializing agent: {e}")
        return None


def get_api_key_from_sidebar() -> Optional[str]:
    """
    Get API key from sidebar input or environment.
    
    Returns:
        API key or None
    """
    # Try to get from environment/secrets first
    api_key = get_api_key()
    
    if api_key:
        st.sidebar.success("✅ API Key loaded from environment")
        return api_key
    
    # If not found, ask user to input
    st.sidebar.warning("⚠️ API Key not found in environment")
    api_key = st.sidebar.text_input(
        "Enter Google Gemini API Key:",
        type="password",
        help="Your Google Gemini API key (free from https://aistudio.google.com/apikey)"
    )
    
    if api_key:
        st.sidebar.success("✅ API Key provided")
        return api_key
    
    return None


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = None
    
    if "total_queries" not in st.session_state:
        st.session_state.total_queries = 0


def add_message(role: str, content: str):
    """
    Add a message to the chat history.
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
    """
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })


def display_chat_history():
    """Display all messages in the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Optionally show timestamp
            # st.caption(f"🕐 {message['timestamp']}")


def process_user_query(query: str, agent) -> str:
    """
    Process user query through the AI agent.
    
    Args:
        query: User's question
        agent: Configured agent executor
        
    Returns:
        Agent's response
    """
    try:
        with st.spinner("🤔 Thinking..."):
            response = agent.invoke({"input": query})
            return response.get("output", "I apologize, but I couldn't generate a response.")
    except Exception as e:
        return get_error_message(str(e))


def sidebar_content():
    """Render sidebar content."""
    st.sidebar.title("⚙️ Settings")
    
    # Provider selection
    provider = st.sidebar.selectbox(
        "AI Provider:",
        ["Google Gemini (Free)"],
        index=0,
        help="Google Gemini is 100% free with generous limits!"
    )
    provider = "gemini"
    
    # Model selection for Gemini
    model_options = [
        "gemini-2.0-flash-exp",  # Latest and fastest
        "gemini-1.5-flash",       # Fast and efficient
        "gemini-1.5-pro"          # Most capable
    ]
    
    model = st.sidebar.selectbox(
        "Select Model:",
        model_options,
        index=0,
        help="gemini-2.0-flash-exp is the fastest and latest model"
    )
    
    st.sidebar.markdown("---")
    
    # Example queries
    st.sidebar.subheader("💡 Example Queries")
    example_queries = [
        "What's the price of Apple stock?",
        "Bitcoin price today",
        "Analyze sentiment: Market rallied",
        "Help me budget $5000/month",
        "What is diversification?",
        "Calculate 30% of 10000"
    ]
    
    for query in example_queries:
        if st.sidebar.button(query, key=f"example_{query}"):
            return query, model
    
    st.sidebar.markdown("---")
    
    # Statistics
    st.sidebar.subheader("📊 Session Stats")
    st.sidebar.metric("Total Queries", st.session_state.total_queries)
    st.sidebar.metric("Messages", len(st.session_state.messages))
    
    st.sidebar.markdown("---")
    
    # Clear chat button
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Disclaimer
    st.sidebar.markdown("""
    <div class="disclaimer">
    <strong>⚠️ Disclaimer</strong><br>
    This AI provides educational information only. 
    Always consult a certified financial advisor for investment decisions.
    </div>
    """, unsafe_allow_html=True)
    
    # About
    with st.sidebar.expander("ℹ️ About"):
        st.markdown("""
        **Financial Advisor AI Agent**
        
        Built with:
        - 🤖 LangChain ReAct
        - 🧠 OpenAI GPT
        - 📊 yfinance
        - 💭 NLTK VADER
        - 🌐 Wikipedia
        
        Version: 1.0.0
        """)
    
    return None, model, provider


def main():
    """Main application logic."""
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    example_query, selected_model, selected_provider = sidebar_content()
    
    # Main header
    st.markdown('<p class="main-header">💰 Financial Advisor AI Agent</p>', unsafe_allow_html=True)
    
    # Check for API key
    api_key = get_api_key_from_sidebar()
    
    if not api_key:
        st.warning("👆 Please provide your Google Gemini API key in the sidebar to get started.")
        st.info("""
        **How to get a FREE Google Gemini API key:**
        1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy the key (starts with AIza...)
        5. Paste it in the sidebar or `.env` file
        
        **Google Gemini is 100% FREE** with generous limits:
        - 🆓 1,500 requests per day
        - 🆓 1 million tokens per day
        - 🆓 No credit card required
        - 🆓 Never expires!
        """)
        
        # Show welcome message
        st.markdown(get_welcome_message())
        return
    
    # Initialize agent if not already done
    if st.session_state.agent is None:
        st.session_state.agent = initialize_agent(api_key, selected_model, selected_provider)
        
        if st.session_state.agent is None:
            st.error("Failed to initialize AI agent. Please check your API key.")
            return
    
    # Welcome message (show only if no chat history)
    if len(st.session_state.messages) == 0:
        st.markdown(get_welcome_message())
    
    # Display chat history
    display_chat_history()
    
    # Handle example query from sidebar
    if example_query:
        # Add user message
        add_message("user", example_query)
        
        # Get agent response
        response = process_user_query(example_query, st.session_state.agent)
        
        # Add assistant message
        add_message("assistant", response)
        
        # Update statistics
        st.session_state.total_queries += 1
        
        # Rerun to display new messages
        st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask me about stocks, budgeting, investments, or financial planning..."):
        # Add user message
        add_message("user", prompt)
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        response = process_user_query(prompt, st.session_state.agent)
        
        # Display assistant message
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add assistant message to history
        add_message("assistant", response)
        
        # Update statistics
        st.session_state.total_queries += 1
        
        # Rerun to update sidebar stats
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Built with ❤️ using LangChain, Streamlit, and OpenAI | 
        <a href="https://github.com" target="_blank">GitHub</a> | 
        Data sources: yfinance, Wikipedia, NLTK
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

