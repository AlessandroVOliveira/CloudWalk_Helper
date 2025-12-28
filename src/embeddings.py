"""
Embeddings module for CloudWalk Helper.
Handles document loading, chunking, and vector database operations.
"""

import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
CHROMA_DB_DIR = Path(__file__).parent.parent / "chroma_db"
COLLECTION_NAME = "cloudwalk_knowledge"


def get_embeddings():
    """Get Ollama embeddings model."""
    return OllamaEmbeddings(model="mxbai-embed-large:latest")


def load_documents():
    """Load all markdown documents from the data directory."""
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from {DATA_DIR}")
    return documents


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Split documents into smaller chunks for better retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n---\n", "\n## ", "\n### ", "\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def create_vector_store(chunks, embeddings=None):
    """Create or update ChromaDB vector store with document chunks."""
    if embeddings is None:
        embeddings = get_embeddings()
    
    # Ensure directory exists
    CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create vector store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DB_DIR)
    )
    print(f"Created vector store with {len(chunks)} documents at {CHROMA_DB_DIR}")
    return vector_store


def get_vector_store(embeddings=None):
    """Get existing ChromaDB vector store or create new one."""
    if embeddings is None:
        embeddings = get_embeddings()
    
    # Check if vector store exists
    if CHROMA_DB_DIR.exists() and any(CHROMA_DB_DIR.iterdir()):
        print("Loading existing vector store...")
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=str(CHROMA_DB_DIR)
        )
        return vector_store
    else:
        print("Creating new vector store...")
        documents = load_documents()
        chunks = split_documents(documents)
        return create_vector_store(chunks, embeddings)


def rebuild_vector_store():
    """Force rebuild of the vector store from documents."""
    import shutil
    
    # Remove existing store
    if CHROMA_DB_DIR.exists():
        shutil.rmtree(CHROMA_DB_DIR)
        print("Removed existing vector store")
    
    # Rebuild
    embeddings = get_embeddings()
    documents = load_documents()
    chunks = split_documents(documents)
    return create_vector_store(chunks, embeddings)


if __name__ == "__main__":
    # Test the embeddings module
    print("Testing embeddings module...")
    print(f"Data directory: {DATA_DIR}")
    print(f"ChromaDB directory: {CHROMA_DB_DIR}")
    
    # Load and process documents
    docs = load_documents()
    chunks = split_documents(docs)
    
    # Create vector store
    vs = create_vector_store(chunks)
    
    # Test retrieval
    results = vs.similarity_search("What is CloudWalk?", k=3)
    print(f"\nTest query results ({len(results)} documents):")
    for i, doc in enumerate(results):
        print(f"  {i+1}. {doc.page_content[:100]}...")
