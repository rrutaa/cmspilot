# CMS RAG Assistant

This project is a Retrieval-Augmented Generation (RAG) pipeline that uses Ollama, ChromaDB, and LangChain to answer questions about CMS Python analysis code using hint files (code, variables, common errors).

## Features
- Loads and chunks hint files (`.md`).
- Embeds with `mxbai-embed-large` via Ollama.
- Stores and retrieves context in ChromaDB.
- Generates Python code with `llama3` and retries until it runs or reaches the iteration limit.
- Configurable via `config.yaml`.

Please note since an LLM is used, the output may differ slightly between runs.
