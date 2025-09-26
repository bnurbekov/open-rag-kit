# 📚 Open RAG Template

Open RAG Template is a plug-and-play Retrieval-Augmented Generation (RAG) framework built with LangChain. It lets you instantly chat with your own documents (PDF, Markdown, CSV, text, etc.) — while showcasing best practices in prompt engineering, retrieval design, agents, evaluation, and fine-tuning.

## ⚡️ Why this project?

Most RAG tutorials are toy-level. This repo gives you a production-ready, modular, open-source template you can actually use, extend, and learn from.

## ✨ Features

📂 Multi-format ingestion → PDF, Markdown, TXT, CSV loaders out of the box.

🔎 Advanced retrieval → FAISS vector store (default) + hybrid search + metadata filtering.

🧩 Prompt engineering → Well-structured system/user prompts with context injection.

🤖 Agent mode (LangChain) → SQL queries, calculator, and web search tools included.

📊 Evaluation harness → Test factuality, relevance, and grounding with LLM-based metrics.

🎛️ Configurable → Easily adjust chunk sizes, embedding models, and retrieval settings.

🚀 Deploy anywhere → Run locally (Docker, pip) or in the cloud (AWS/GCP).

## 🖼️ Demo

<p align="center"> <img src="docs/demo.gif" width="600" alt="Demo: Chat with your docs" /> </p>

### Quick Start

Chat with your own PDF in 3 steps:

git clone https://github.com/your-username/open-rag-template.git
cd open-rag-template
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key-here"
streamlit run src/app.py


Then open http://localhost:8501
 🎉

## 🏗️ Architecture

<p align="center"> <img src="docs/architecture.png" width="650" alt="Architecture diagram" /> </p>

1. Ingest documents → chunk + embed into FAISS (or another DB).
2. Retrieve relevant chunks per query.
3. Construct prompt with query + context.
4. Generate answer with an LLM (OpenAI, Anthropic, Llama 3, etc.).
5. (Optional) Agent → use tools like SQL or web search if needed.
6. Evaluate outputs with metrics + logs.

## 📂 Project Structure
open-rag-template/
├── src/
│   ├── ingest/         # PDF/Markdown/CSV loaders
│   ├── embeddings/     # Vectorstore + retriever setup
│   ├── prompts/        # Prompt templates
│   ├── chains/         # RAG chain logic
│   ├── agents/         # Agents + tools (SQL, search, calculator)
│   ├── eval/           # Evaluation harness
│   ├── app.py          # Streamlit/FastAPI entrypoint
│   └── config.py       # Global settings
├── tests/              # Unit tests
└── docs/               # Docs + diagrams + demo GIF

## 🛠️ Installation

### Requirements

- Python 3.9+
- `pip install -r requirements.txt`
- (Optional) Docker + docker-compose

### Setup
# Clone repo
git clone https://github.com/your-username/open-rag-template.git
cd open-rag-template

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run app
streamlit run src/app.py

## ⚡ Usage

### Ingest documents
```bash
python src/ingest/pdf_loader.py data/my_docs/
```

### Run chatbot
```bash
streamlit run src/app.py
```

### Agent mode (SQL + tools)

Enable in config.py:
```python
ENABLE_AGENT_MODE = True
```

## 🧪 Evaluation

### Run test suite:
```bash
python src/eval/evaluator.py
```

### Metrics included:

- Embedding similarity (semantic closeness).
- LLM-as-judge scoring (quality, groundedness, helpfulness).
- Custom test cases via eval/test_cases.json.

## 🌱 Roadmap

✅ Phase 1: Core RAG chatbot

✅ Phase 2: Hybrid retrieval & re-ranking

🔄 Phase 3: LangChain agent mode (SQL, web search, calculator)

🔄 Phase 4: Evaluation harness + dashboard

🔲 Phase 5: Fine-tuning (LoRA, instruction datasets)

## 🤝 Contributing

Contributions welcome! Open issues, suggest features, or submit PRs.

## 📜 License

MIT License — free to use, modify, and share.

## ⭐ Why Star This Repo?

If you find this useful, give it a ⭐ on GitHub! It helps others discover the project and keeps development going.

## 🔥 With this README, anyone can:

- Understand what the project does.
- Install + run it in minutes.
- See that it's modular and professional.
- Know there's a roadmap for growth.