<p align="center">
  <img src="logo.svg" alt="CloudWalk Helper" width="300">
</p>

# CloudWalk Helper 🚀

A RAG-powered chatbot that answers questions about CloudWalk, InfinitePay, JIM, and Stratus using LangChain, ChromaDB, and Ollama.

## Features

- 💬 **Natural Language Q&A**: Ask questions in English or Portuguese
- 🔍 **RAG-powered**: Retrieval-Augmented Generation for accurate, contextual answers
- 🎨 **Modern UI**: Clean, dark-themed chat interface inspired by GPT/Gemini
- 📚 **Knowledge Base**: Curated information about CloudWalk products and services
- 🔗 **Source Links**: Responses include relevant URLs when helpful

## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai/) installed and running
- llama3.2 model pulled in Ollama

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   cd CloudWalk-Helper
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Ollama**:
   ```bash
   ollama serve
   ollama pull llama3.2:3b
   ollama pull mxbai-embed-large
   ```

## Usage

### Run the Chatbot

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

### Test the RAG Pipeline

```bash
python -m src.embeddings  # Test embeddings and vector store
python -m src.rag_chain   # Test RAG chain
```

## Sample Conversations

### Conversation 1: Company Overview

```
User: What is CloudWalk?

CloudWalk Helper: CloudWalk is a fintech company that aims to create the best 
payment network on Earth and eventually expand it to other planets. The company's 
mission is to democratize the financial industry, empower entrepreneurs through 
innovative solutions, and provide them with technological, inclusive, and 
life-changing experiences.

As part of this mission, CloudWalk focuses on delivering high-quality services 
using cutting-edge technologies like AI and blockchain. They strive to create a 
customer-centric approach, putting their customers at the forefront of everything 
they do.

CloudWalk is also behind InfinitePay, which is their flagship payment platform in 
Brazil. InfiniteTap, a part of InfinitePay, offers smartphone payments for 
individuals who don't have a CNPJ (Brazilian Business Register), allowing them to 
make sales using their CPF and smartphone.

Additionally, CloudWalk has developed JIM, an AI assistant that helps with 
financial management, creates marketing campaigns, makes payments, reminds about 
commitments, and provides business insights 24/7.

You can learn more about CloudWalk by visiting their official website: 
https://www.cloudwalk.io/
```

### Conversation 2: Product Inquiry (Portuguese)

```
User: O que é a InfinitePay?

CloudWalk Helper: A InfinitePay é uma plataforma de pagamentos financeira 
brasileira criada pela CloudWalk. Ela oferece serviços de pagamento para 
consumidores e empresas, permitindo realizar transações de forma segura e 
conveniente.

Com a InfinitePay, é possível realizar pagamentos com cartões de débito ou 
crédito, parcelamentos até 12x sem taxas adicionais, e também utilizar o Pix 
(com taxa zero). Além disso, a plataforma oferece contas digitais integradas 
para gerenciar receitas, pagamentos e outras operações financeiras.

A InfinitePay é uma empresa líder no mercado de pagamentos do Brasil, com uma 
equipe especializada em tecnologia e inovação. Ela visa democratizar o acesso a 
produtos de pagamento e software de classe mundial, facilitando a vida das 
pessoas e dos negócios.

Para saber mais sobre os serviços da InfinitePay, você pode visitar o site 
oficial: https://www.infinitepay.io/
```

### Conversation 3: Technical Features

```
User: What is Stratus and how does it work?

CloudWalk Helper: Stratus is an open-source blockchain developed by CloudWalk 
that's designed for global payment networks. It allows for high scalability, 
security, and customization.

Here are some key features of Stratus:
1. **High Scalability:** Stratus can process up to 1,800 transactions per second 
   (TPS) with a potential capacity of 160 million transactions per day.
2. **Ethereum Compatibility:** Stratus is integrated with the Ethereum Virtual 
   Machine (EVM), allowing for the creation of smart contracts and advanced 
   functionalities for financial transactions.
3. **Enhanced Security:** The blockchain has a permissioned architecture, where 
   only authorized nodes can participate, ensuring security and control over 
   the network.
4. **Layered Architecture:** Stratus uses a layered architecture with JSON-RPC 
   for communication and RocksDB for optimized storage.

Stratus works by allowing users to create a node on the network, which validates 
transactions and verifies data. The blockchain's sharding and multi-raft consensus 
models enable exponential capacity expansion, making it an ideal solution for 
businesses seeking secure, scalable, and customizable blockchain infrastructure.

To learn more about Stratus, I recommend checking out its GitHub repository: 
https://github.com/cloudwalk/stratus
```

## Project Structure

```
CloudWalk-Helper/
├── app.py                    # Streamlit chat interface
├── src/
│   ├── __init__.py
│   ├── embeddings.py         # Vector store management
│   └── rag_chain.py          # RAG chain logic
├── data/
│   ├── cloudwalk_knowledge.md    # English knowledge base
│   └── cloudwalk_knowledge_pt.md # Portuguese knowledge base
├── chroma_db/                # Vector database (generated)
├── context/
│   └── prd.md                # Product requirements
├── requirements.txt
└── README.md
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| LLM | Ollama (llama3.2:3b) |
| Embeddings | Ollama (mxbai-embed-large) |
| Vector DB | ChromaDB |
| RAG Framework | LangChain |
| Frontend | Streamlit |

## Troubleshooting

### Ollama Connection Error
Make sure Ollama is running:
```bash
ollama serve
```

### Model Not Found
Pull the required models:
```bash
ollama pull llama3.2:3b
ollama pull mxbai-embed-large
```

### Slow First Response
The first query may be slow as it loads the model and creates embeddings. Subsequent queries will be faster.

## License

MIT License

## Links

- [CloudWalk](https://www.cloudwalk.io/)
- [InfinitePay](https://www.infinitepay.io/)
- [Stratus](https://www.cloudwalk.io/stratus)
