
import re
from io import StringIO

def summarize_text_download(text):
    # naive placeholder - in production use LLM for high-quality summary
    bullets = []
    sents = re.split(r'(?<=[.!?])\s+', text)
    for s in sents[:6]:
        bullets.append('- ' + (s.strip()[:300]))
    return '\n'.join(bullets)

def highlight_context_text(context, query):
    # very naive highlighter: bold query words
    q_words = [w.lower() for w in re.findall(r"\w+", query) if len(w)>2]
    out = context
    for w in set(q_words):
        out = re.sub(fr'(?i)({w})', r'**\1**', out)
    return out
