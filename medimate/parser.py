import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file_stream):
    # Reset stream pointer to the beginning before reading
    file_stream.seek(0)
    doc = fitz.open(stream=file_stream.read(), filetype='pdf')
    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text('text')
        pages.append({'page': i, 'text': text})
    return pages

def split_into_sections(page_text):
    # Naive section splitter using headings (all caps, or lines ending with ':')
    lines = [ln.strip() for ln in page_text.splitlines() if ln.strip()]
    sections = []
    current = {'title': 'Unknown', 'text': ''}
    for ln in lines:
        if ln.isupper() and len(ln.split()) < 8:
            # treat as heading
            if current['text']:
                sections.append(current)
            current = {'title': ln, 'text': ''}
        elif ln.endswith(':') and len(ln) < 80:
            if current['text']:
                sections.append(current)
            current = {'title': ln.rstrip(':'), 'text': ''}
        else:
            current['text'] += ln + ' '
    if current['text']:
        sections.append(current)
    return sections

def chunk_text_with_sections(pages, chunk_size=800, overlap=150):
    chunks = []
    for p in pages:
        page_num = p['page']
        sections = split_into_sections(p['text'])
        if not sections:
            sections = [{'title': 'Unknown', 'text': p['text'] or ''}]
        for sec in sections:
            words = sec['text'].split()
            i = 0
            while i < len(words):
                chunk_words = words[i:i+chunk_size]
                chunks.append({'text': ' '.join(chunk_words), 'page': page_num, 'section': sec['title']})
                i += chunk_size - overlap
    return [c for c in chunks if c['text'].strip()]
