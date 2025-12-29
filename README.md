<p align="center">
  <img src="logo.svg" alt="CloudWalk Helper" width="300">
</p>

# CloudWalk Helper

A RAG-powered chatbot that answers questions about CloudWalk, InfinitePay, JIM, and Stratus. Built with LangChain, ChromaDB, HuggingFace Embeddings, and OpenRouter.

---

## 1. Overview

**CloudWalk Helper** is an intelligent chatbot that provides accurate information about CloudWalk and its ecosystem of products:

- **CloudWalk** — Fintech company building the best payment network on Earth
- **InfinitePay** — Payment platform for Brazilian entrepreneurs
- **JIM** — AI-powered financial assistant
- **Stratus** — Open-source blockchain for global payments

### Key Features

| Feature | Description |
|---------|-------------|
| 🌐 **Bilingual** | Supports English and Portuguese with automatic language detection |
| 🔍 **RAG-powered** | Retrieval-Augmented Generation for contextual, accurate answers |
| 📚 **Knowledge Base** | Curated information from official CloudWalk sources |
| 🔗 **Source Citations** | Responses include relevant URLs when available |
| ⏱️ **Response Timing** | Shows processing time for transparency |
| 🐳 **Docker Ready** | One-command deployment with Docker |


---

## 2. Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Streamlit     │────▶│   RAG Chain     │────▶│   OpenRouter    │
│   Chat UI       │◀────│   (LangChain)   │◀────│   (LLM API)     │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    ChromaDB     │
                        │  + HuggingFace  │
                        │   Embeddings    │
                        └─────────────────┘
```

### Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Modern chat interface with dark theme |
| **RAG Framework** | LangChain | Orchestrates retrieval and generation |
| **Vector Database** | ChromaDB | Stores and retrieves document embeddings |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) | Converts text to vectors locally |
| **LLM** | OpenRouter (Llama 3.2 free tier) | Generates responses from context |

### Data Flow

1. **User Input** → User sends a question via the Streamlit chat interface
2. **Language Detection** → System detects if the question is in English or Portuguese
3. **Retrieval** → Relevant documents are fetched from ChromaDB using semantic search
4. **Generation** → Retrieved context + question are sent to OpenRouter LLM
5. **Response** → LLM generates a contextual response displayed to the user

### Project Structure

```
CloudWalk-Helper/
├── app.py                    # Streamlit chat interface
├── src/
│   ├── embeddings.py         # HuggingFace embeddings + ChromaDB
│   └── rag_chain.py          # RAG chain with OpenRouter/Ollama
├── data/
│   ├── cloudwalk_knowledge.md    # English knowledge base
│   └── cloudwalk_knowledge_pt.md # Portuguese knowledge base
├── chroma_db/                # Vector database (generated)
├── Dockerfile                # Container configuration
├── docker-compose.yml        # Docker Compose setup
├── start.bat / start.sh      # One-command launchers
└── .env.example              # Environment template
```

---

## 3. How to Run

### Prerequisites

- Docker and Docker Compose **OR** Python 3.9+
- OpenRouter API key (free) — Get one at [openrouter.ai](https://openrouter.ai)

### Option A: Docker (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

The script will:
1. Create `.env` file from template
2. Prompt you to add your API key
3. Build and start the Docker container
4. Open the browser at http://localhost:8501

**Manual Docker:**
```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
docker-compose up --build
```

### Option B: Local Python

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY

# Run the chatbot
streamlit run app.py
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | Yes* | - | Your OpenRouter API key |
| `LLM_PROVIDER` | No | `openrouter` | `openrouter` or `ollama` |
| `OPENROUTER_MODEL` | No | `meta-llama/llama-3.2-3b-instruct:free` | Model to use |
| `DEBUG` | No | `false` | Enable debug logging |

*Required if using OpenRouter (default). Not needed if using Ollama.

### Using Ollama (Local LLM Alternative)

```bash
# In .env file:
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2:3b

# Start Ollama and pull the model:
ollama serve
ollama pull llama3.2:3b
```

---

## 4. Demo Guide

### Quick Demo

1. **Start the application** using one of the methods above
2. **Open the browser** at http://localhost:8501
3. **Ask a question** in the chat input

### Sample Questions to Try

**English:**
- "What is CloudWalk?"
- "How does InfinitePay work?"
- "What is Stratus blockchain?"
- "Tell me about JIM"

**Portuguese:**
- "O que é a CloudWalk?"
- "Como funciona a InfinitePay?"
- "Quais são os valores da empresa?"

### Expected Behavior

- **Response Time**: Displayed at the bottom of each response (typically 5-15 seconds)
- **Language Detection**: System automatically responds in the same language as the question
- **Source Links**: Relevant URLs are included when the knowledge base contains them

### Observability & Logs

The application provides comprehensive logging for debugging and traceability:

```bash
# View logs in Docker
docker-compose logs -f

# Sample log output:
2025-12-28 19:44:21 | CloudWalkHelper.RAG | INFO | === New Question ===
2025-12-28 19:44:21 | CloudWalkHelper.RAG | INFO | Using OpenRouter with model: meta-llama/llama-3.2-3b-instruct:free
2025-12-28 19:44:22 | CloudWalkHelper.Embeddings | INFO | Loading embeddings model: sentence-transformers/all-MiniLM-L6-v2
2025-12-28 19:44:24 | CloudWalkHelper.RAG | INFO | Processing question: 'What is CloudWalk?...' (Language: English)
2025-12-28 19:44:24 | CloudWalkHelper.RAG | INFO | Retrieved 8 documents in 0.02s
2025-12-28 19:44:29 | CloudWalkHelper.RAG | INFO | Total response time: 7.54s
```

### Debug Mode

Enable detailed logging by setting in `.env`:
```bash
DEBUG=true
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **429 Too Many Requests** | OpenRouter rate limit reached. Wait a few seconds between requests. |
| **Model Not Found (Ollama)** | Run `ollama pull llama3.2:3b` to download the model. |
| **Slow First Response** | Initial query loads embeddings model. Subsequent queries are faster. |
| **Connection Error** | Verify your API key is correct and you have internet access. |

---

## Links

- [CloudWalk](https://www.cloudwalk.io/)
- [InfinitePay](https://www.infinitepay.io/)
- [Stratus](https://www.cloudwalk.io/stratus)
- [OpenRouter](https://openrouter.ai/)

---

## License

MIT License
