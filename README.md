
# MediMate AI Powered Health Report Summary Assistant

This MediMate includes:
- Built a medical assistant that summarizes health reports and answers user queries using LLM + RAG.
- Implemented PDF parsing and chunk embedding with PyMuPDF + Sentence Transformers, and vector retrieval with FAISS.
- Deployed the solution via a Streamlit UI for easy report upload and interactive Q&A with the assistant.  
-  PyMuPDF for chunking (section-aware + overlap)
- Metadata (page, section) captured and persisted
- FAISS index persistence + SQLite metadata store
- Streamlit app with session chat, highlighted context, downloadable summary
- Dockerfile for easy deployment
- .env support for API keys
- Basic logging

Run locally:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
