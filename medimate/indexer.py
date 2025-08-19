import faiss, os, pickle, time
import numpy as np
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text
from sqlalchemy.orm import sessionmaker

class FaissSqlIndexer:
    def __init__(self, dim, index_path='models/faiss.index', db_path='models/metadata.db'):
        os.makedirs(os.path.dirname(index_path) or '.', exist_ok=True)
        self.dim = dim
        self.index_path = index_path
        self.db_path = db_path
        self.index = faiss.IndexFlatIP(dim)
        self.metadatas = []  # in-memory mirror

        # Setup SQLite
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False, future=True)
        self.Session = sessionmaker(bind=self.engine)
        self.meta = MetaData()
        self.docs = Table(
            'documents', self.meta,
            Column('id', Integer, primary_key=True),
            Column('text', Text),
            Column('page', Integer),
            Column('section', String(200))
        )
        self.meta.create_all(self.engine)

        # Load if exists
        if os.path.exists(index_path):
            try:
                self.index = faiss.read_index(index_path)
                with open(index_path + '.meta.pkl', 'rb') as f:
                    self.metadatas = pickle.load(f)
            except Exception:
                pass

    def add(self, embeddings, metadatas):
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        with self.engine.begin() as conn:
            for m in metadatas:
                ins = self.docs.insert().values(
                    text=m.get('text'),
                    page=m.get('page'),
                    section=m.get('section')
                )
                conn.execute(ins)
                self.metadatas.append({
                    'text': m.get('text'),
                    'page': m.get('page'),
                    'section': m.get('section')
                })

    def search(self, query_embedding, k=5):
        faiss.normalize_L2(query_embedding)
        D, I = self.index.search(query_embedding, k)
        results = []
        seen_sections = set()

        for idx in I[0]:
            if idx < len(self.metadatas):
                meta = self.metadatas[idx]
                key = (meta['page'], meta['section'])
                if key not in seen_sections:
                    seen_sections.add(key)
                    results.append(meta)

        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + '.meta.pkl', 'wb') as f:
            pickle.dump(self.metadatas, f)

    def clear(self):
        # Close connections before deletion
        self.engine.dispose()

        self.index = faiss.IndexFlatIP(self.dim)
        self.metadatas = []

        # Retry deletion if locked (Windows fix)
        for file in [self.index_path, self.index_path + '.meta.pkl', self.db_path]:
            if os.path.exists(file):
                for _ in range(5):
                    try:
                        os.remove(file)
                        break
                    except PermissionError:
                        time.sleep(0.5)
