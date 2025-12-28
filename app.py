"""
CloudWalk Helper - Streamlit Chat Interface
A RAG-powered chatbot for CloudWalk, InfinitePay, JIM, and Stratus.
"""

import streamlit as st
from src.rag_chain import simple_ask, ask


# Page configuration
st.set_page_config(
    page_title="CloudWalk Helper",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern chat UI
st.markdown("""
<style>
    /* Main container */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Chat container */
    .stChatFloatingInputContainer {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Chat input */
    .stChatInput > div > div > input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 25px !important;
        color: white !important;
        padding: 15px 20px !important;
    }
    
    .stChatInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* User message */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px 20px 5px 20px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Assistant message */
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px 20px 20px 5px;
        padding: 15px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Quick action buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        color: white;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: transparent;
        transform: translateY(-2px);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Links */
    a {
        color: #667eea !important;
    }
    
    /* Markdown in messages */
    .stMarkdown {
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "initialized" not in st.session_state:
        st.session_state.initialized = False


def display_header():
    """Display the chat header with logo."""
    # Display logo centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.svg", use_container_width=True)
    
    st.markdown(
        '<p class="subtitle">Ask me anything about CloudWalk, InfinitePay, JIM, or Stratus</p>',
        unsafe_allow_html=True
    )


def display_quick_actions():
    """Display quick action buttons for common questions."""
    if not st.session_state.messages:
        st.markdown("---")
        st.markdown("**Quick questions:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏢 What is CloudWalk?", use_container_width=True):
                return "What is CloudWalk?"
            if st.button("💳 InfinitePay rates", use_container_width=True):
                return "What are the fees and rates for InfinitePay debit and credit card transactions?"
        
        with col2:
            if st.button("🤖 What is JIM?", use_container_width=True):
                return "What is JIM?"
            if st.button("⛓️ About Stratus", use_container_width=True):
                return "What is Stratus blockchain?"
    
    return None


def display_chat_history():
    """Display the chat message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_response(user_input: str) -> str:
    """Get response from the RAG chain."""
    try:
        response = simple_ask(user_input)
        return response
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}. Please make sure Ollama is running with the llama3.2 model."


def main():
    """Main application function."""
    init_session_state()
    display_header()
    
    # Check for quick action clicks
    quick_question = display_quick_actions()
    
    # Display chat history
    display_chat_history()
    
    # Handle quick action or chat input
    user_input = quick_question or st.chat_input("Ask me about CloudWalk, InfinitePay, JIM, or Stratus...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_response(user_input)
            st.markdown(response)
        
        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update UI
        st.rerun()


if __name__ == "__main__":
    main()
