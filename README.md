
# MediMate — Upgraded (Production-ready) 

This upgraded MediMate includes:
- Improved chunking (section-aware + overlap)
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
