
import streamlit as st
from medimate.parser import extract_text_from_pdf, chunk_text_with_sections
from medimate.embedder import Embedder
from medimate.indexer import FaissSqlIndexer
from medimate.retriever import Retriever
from medimate.llm_client import LLMClient
from medimate.utils import summarize_text_download, highlight_context_text
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title='MediMate — Health Report Assistant', layout='wide')
st.title('MediMate — Health Report Assistant ')

# Initialize components (lazy to reduce startup cost)
@st.cache_resource
def get_embedder():
    return Embedder(model_name='all-mpnet-base-v2')

@st.cache_resource
def get_indexer(dim):
    return FaissSqlIndexer(dim=dim, index_path='models/faiss.index', db_path='models/metadata.db')

embedder = get_embedder()
indexer = get_indexer(embedder.model.get_sentence_embedding_dimension())
retriever = Retriever(indexer=indexer, embedder=embedder)
llm = LLMClient()

# Sidebar controls
st.sidebar.header('Controls')
with st.sidebar.expander('Index Management'):
    if st.button('Clear index and metadata'):
        indexer.clear()
        st.sidebar.success('Index & metadata cleared.')

uploaded = st.file_uploader('Upload PDF report (single file)', type=['pdf'])
if uploaded:
    st.info('Parsing PDF and creating chunks...')
    raw_pages = extract_text_from_pdf(uploaded)
    chunks = chunk_text_with_sections(raw_pages, chunk_size=700, overlap=120)
    st.success(f'Created {len(chunks)} chunks.')

    if st.button('Index this report (persist)'):
        texts = [c['text'] for c in chunks]
        embeddings = embedder.embed(texts)
        metas = [{'text': c['text'], 'page': c['page'], 'section': c['section']} for c in chunks]
        indexer.add(embeddings, metas)
        indexer.save()
        st.success('Indexed and persisted.')

    if st.button('Auto summarize report'):
        # use retriever to get top contexts for a synthesis prompt
        q = 'Provide a concise 6-bullet summary of the report.'
        contexts = retriever.retrieve(q, k=8)
        system, prompt = retriever.build_prompt(q, contexts)
        ans = llm.ask(system, prompt, max_tokens=400)
        st.markdown('**Auto-summary**')
        st.write(ans)
        st.download_button('Download summary (txt)', ans, file_name='medimate_summary.txt')

# Q&A area
st.subheader('Ask about indexed reports')
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input('Ask a question about any indexed report:')
if st.button('Get Answer') and question.strip():
    contexts = retriever.retrieve(question, k=5)
    system, prompt = retriever.build_prompt(question, contexts)
    answer = llm.ask(system, prompt, max_tokens=300)
    st.session_state.chat_history.append({'q': question, 'a': answer, 'contexts': contexts})

# Display chat history with highlighted contexts
for i, item in enumerate(reversed(st.session_state.chat_history)):
    st.markdown('---')
    st.markdown(f'**Q:** {item['q']}')
    st.markdown(f'**A:** {item['a']}')
    # Highlighted contexts
    for c in item['contexts']:
        highlighted = highlight_context_text(c['text'], item['q'])
        st.caption(f"page: {c.get('page')} | section: {c.get('section')}")
        st.write(highlighted)
