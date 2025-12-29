"""
RAG Chain module for CloudWalk Helper.
Implements the retrieval-augmented generation logic using LangChain.
Supports OpenRouter (cloud) or Ollama (local) LLM providers.
"""

import os
import logging
import time
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

from .embeddings import get_vector_store, get_embeddings

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("CloudWalkHelper.RAG")

# Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = "meta-llama/llama-3.2-3b-instruct:free"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
RETRIEVAL_K = 8  # Number of documents to retrieve


def get_llm():
    """Get LLM instance based on LLM_PROVIDER environment variable."""
    if LLM_PROVIDER == "openrouter":
        from langchain_openai import ChatOpenAI
        
        if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_api_key_here":
            raise ValueError(
                "OpenRouter API key not configured. "
                "Please set OPENROUTER_API_KEY in your .env file. "
                "Get a free key at https://openrouter.ai"
            )
        
        logger.info(f"Using OpenRouter with model: {OPENROUTER_MODEL}")
        return ChatOpenAI(
            model=OPENROUTER_MODEL,
            openai_api_key=OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.7,
            default_headers={
                "HTTP-Referer": "https://github.com/cloudwalk-helper",
                "X-Title": "CloudWalk Helper"
            }
        )
    else:
        from langchain_ollama import ChatOllama
        logger.info(f"Using Ollama with model: {OLLAMA_MODEL}")
        return ChatOllama(
            model=OLLAMA_MODEL,
            temperature=0.7,
        )


def get_retriever():
    """Get the document retriever from vector store."""
    logger.debug("Setting up document retriever...")
    embeddings = get_embeddings()
    vector_store = get_vector_store(embeddings)
    logger.debug(f"Retriever configured with k={RETRIEVAL_K}")
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVAL_K}
    )


def format_docs(docs):
    """Format retrieved documents into a string."""
    formatted = "\n\n---\n\n".join(doc.page_content for doc in docs)
    logger.debug(f"Formatted {len(docs)} documents ({len(formatted)} chars)")
    return formatted


def detect_language(text: str) -> str:
    """Simple language detection based on common words."""
    portuguese_words = ['o', 'a', 'que', 'de', 'do', 'da', 'é', 'em', 'para', 'com', 'não', 'uma', 'um', 'os', 'as', 'por', 'mais', 'qual', 'quais', 'como', 'isso', 'esse', 'essa', 'são', 'sobre', 'pode', 'fazer', 'seu', 'sua']
    english_words = ['the', 'is', 'what', 'how', 'can', 'do', 'does', 'are', 'have', 'has', 'will', 'would', 'could', 'should', 'about', 'this', 'that', 'which', 'where', 'when', 'why', 'who', 'tell', 'me', 'explain', 'describe']
    
    text_lower = text.lower()
    words = text_lower.split()
    
    pt_count = sum(1 for word in words if word in portuguese_words)
    en_count = sum(1 for word in words if word in english_words)
    
    result = "Portuguese" if pt_count > en_count else "English"
    logger.debug(f"Language detected: {result} (PT words: {pt_count}, EN words: {en_count})")
    return result


# System prompt for the CloudWalk Helper chatbot
SYSTEM_PROMPT = """You are CloudWalk Helper, a helpful assistant that answers questions about CloudWalk, InfinitePay, JIM, and Stratus.

**MANDATORY: You MUST respond in {language}. This is non-negotiable.**

The user asked their question in {language}, so your entire response must be in {language}.

Use the following retrieved context to answer questions. The context may contain information in different languages - you must translate it to {language} for your response.

If the answer is not in the context, say you don't have that specific information but offer to help with related topics.

Be friendly, professional, and concise.

Context:
{context}

Guidelines:
- Your response MUST be entirely in {language}
- Be accurate and only use information from the provided context
- If asked about pricing/rates, provide the specific numbers from the context
- **SOURCE CITATION**: Always include relevant URLs at the end of your response when discussing specific products or services. Use format:
  - CloudWalk info: https://www.cloudwalk.io/
  - InfinitePay info: https://www.infinitepay.io/
  - JIM info: https://www.infinitepay.io/jim
  - Stratus info: https://www.cloudwalk.io/stratus or https://github.com/cloudwalk/stratus
- When providing facts, ground them in the context provided - do not make up information
"""



def get_prompt():
    """Get the chat prompt template."""
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}")
    ])


def create_rag_chain():
    """Create the full RAG chain using LCEL pattern."""
    llm = get_llm()
    retriever = get_retriever()
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}")
    ])
    
    # Create the RAG chain using LCEL with language detection
    def process_input(question: str):
        retrieval_start = time.time()
        language = detect_language(question)
        logger.info(f"Processing question: '{question[:50]}...' (Language: {language})")
        
        docs = retriever.invoke(question)
        retrieval_time = time.time() - retrieval_start
        logger.info(f"Retrieved {len(docs)} documents in {retrieval_time:.2f}s")
        
        context = format_docs(docs)
        return {
            "context": context,
            "input": question,
            "language": language
        }
    
    rag_chain = (
        process_input
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain


def ask(question: str, chat_history: list = None) -> dict:
    """
    Ask a question to the CloudWalk Helper.
    
    Args:
        question: The user's question
        chat_history: Optional list of previous messages
        
    Returns:
        Dictionary with 'answer' key
    """
    chain = create_rag_chain()
    
    # LCEL chain takes the question directly
    result = chain.invoke(question)
    
    return {
        "answer": result if isinstance(result, str) else str(result),
        "context": []
    }


def simple_ask(question: str) -> str:
    """
    Simple interface to ask a question and get just the answer string.
    
    Args:
        question: The user's question
        
    Returns:
        The answer string
    """
    start_time = time.time()
    logger.info(f"=== New Question ===")
    
    chain = create_rag_chain()
    result = chain.invoke(question)
    
    total_time = time.time() - start_time
    logger.info(f"Total response time: {total_time:.2f}s")
    logger.info(f"Response length: {len(result)} chars")
    
    return result


if __name__ == "__main__":
    # Test the RAG chain
    print("Testing RAG chain...")
    print("-" * 50)
    
    test_questions = [
        "What is CloudWalk?",
        "O que é a InfinitePay?",
        "What are the rates for InfiniteTap?",
        "What can JIM do?"
    ]
    
    for q in test_questions:
        print(f"\nQ: {q}")
        answer = simple_ask(q)
        print(f"A: {answer[:500]}...")
        print("-" * 50)
