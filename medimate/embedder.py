
from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name='all-mpnet-base-v2'):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        embs = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return embs
