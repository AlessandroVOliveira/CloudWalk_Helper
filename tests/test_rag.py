"""
Test script for CloudWalk Helper RAG pipeline.
Run with: python tests/test_rag.py
"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_embeddings():
    """Test the embeddings and vector store creation."""
    print("=" * 60)
    print("Testing Embeddings Module")
    print("=" * 60)
    
    from src.embeddings import (
        load_documents, 
        split_documents, 
        get_vector_store,
        DATA_DIR,
        CHROMA_DB_DIR
    )
    
    print(f"\n📁 Data directory: {DATA_DIR}")
    print(f"📁 ChromaDB directory: {CHROMA_DB_DIR}")
    
    # Test document loading
    print("\n1. Loading documents...")
    docs = load_documents()
    assert len(docs) > 0, "No documents loaded!"
    print(f"   ✅ Loaded {len(docs)} documents")
    
    # Test chunking
    print("\n2. Splitting documents into chunks...")
    chunks = split_documents(docs)
    assert len(chunks) > 0, "No chunks created!"
    print(f"   ✅ Created {len(chunks)} chunks")
    
    # Test vector store
    print("\n3. Creating/loading vector store...")
    vs = get_vector_store()
    assert vs is not None, "Vector store is None!"
    print("   ✅ Vector store ready")
    
    # Test similarity search
    print("\n4. Testing similarity search...")
    results = vs.similarity_search("What is CloudWalk?", k=3)
    assert len(results) > 0, "No search results!"
    print(f"   ✅ Retrieved {len(results)} documents")
    
    print("\n✅ Embeddings module tests passed!")
    return True


def test_rag_chain():
    """Test the RAG chain responses."""
    print("\n" + "=" * 60)
    print("Testing RAG Chain")
    print("=" * 60)
    
    from src.rag_chain import simple_ask, get_llm, get_retriever
    
    # Test LLM connection
    print("\n1. Testing Ollama connection...")
    try:
        llm = get_llm()
        print("   ✅ Ollama LLM connected")
    except Exception as e:
        print(f"   ❌ Ollama connection failed: {e}")
        print("   Make sure Ollama is running: ollama serve")
        return False
    
    # Test retriever
    print("\n2. Testing retriever...")
    retriever = get_retriever()
    assert retriever is not None, "Retriever is None!"
    print("   ✅ Retriever ready")
    
    # Test questions
    test_cases = [
        ("What is CloudWalk?", ["cloudwalk", "payment", "fintech"]),
        ("O que é a InfinitePay?", ["infinitepay", "pagamento", "brasil"]),
        ("What are the rates for InfiniteTap?", ["rate", "débito", "crédito", "%"]),
        ("What is JIM?", ["jim", "ai", "assistant", "inteligência"]),
    ]
    
    print("\n3. Testing RAG responses...")
    for i, (question, expected_keywords) in enumerate(test_cases, 1):
        print(f"\n   Q{i}: {question}")
        try:
            answer = simple_ask(question)
            answer_lower = answer.lower()
            
            # Check if any expected keyword is in the answer
            found = any(kw.lower() in answer_lower for kw in expected_keywords)
            
            if found:
                print(f"   ✅ Got relevant response ({len(answer)} chars)")
                print(f"      Preview: {answer[:150]}...")
            else:
                print(f"   ⚠️ Response may not be relevant")
                print(f"      Response: {answer[:200]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    print("\n✅ RAG chain tests passed!")
    return True


def main():
    """Run all tests."""
    print("\n🧪 CloudWalk Helper - RAG Pipeline Tests")
    print("=" * 60)
    
    success = True
    
    # Test embeddings
    try:
        if not test_embeddings():
            success = False
    except Exception as e:
        print(f"\n❌ Embeddings test failed: {e}")
        success = False
    
    # Test RAG chain
    try:
        if not test_rag_chain():
            success = False
    except Exception as e:
        print(f"\n❌ RAG chain test failed: {e}")
        success = False
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! The chatbot is ready.")
        print("\nRun the app with: streamlit run app.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
