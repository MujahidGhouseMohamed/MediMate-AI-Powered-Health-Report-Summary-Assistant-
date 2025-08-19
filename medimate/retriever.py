from medimate.embedder import Embedder

SYSTEM_PROMPT_QA = (
    "You are MediMate, a medical assistant. "
    "Use ONLY the provided report excerpts to answer the user. "
    "If the answer is not in the report, say: 'I don't know — please consult a medical professional.'"
)

SYSTEM_PROMPT_SUMMARY = (
    "You are MediMate, a medical report summarizer. "
    "Using ONLY the provided report excerpts, write a concise, logically ordered summary. "
    "Group related findings together, remove duplicates, and use natural medical language. "
    "Present the summary as exactly 6 clean bullet points and sort each points and retrive data from RAG, don't perform AI hallucination."
)

# Optional: priority ordering for better logical summaries
SECTION_PRIORITY = {
    "PATIENT INFO": 1,
    "CLINICAL HISTORY": 2,
    "FINDINGS": 3,
    "IMPRESSION": 4,
    "RECOMMENDATIONS": 5
}

class Retriever:
    def __init__(self, indexer, embedder: Embedder):
        self.indexer = indexer
        self.embedder = embedder

    def retrieve(self, question, k=5):
        """Embed the question and retrieve top-k chunks from FAISS."""
        q_emb = self.embedder.embed([question])
        results = self.indexer.search(q_emb, k)
        return self.sort_contexts(results)

    def sort_contexts(self, contexts):
        """Sort chunks by page and section priority for better summaries."""
        return sorted(
            contexts,
            key=lambda c: (
                c.get("page", 999),
                SECTION_PRIORITY.get(c.get("section", "").upper(), 999)
            )
        )

    def build_prompt(self, question, contexts):
        """Builds system & user prompts for the LLM."""
        # Detect summary request
        if any(word in question.lower() for word in ["summary", "summarize", "overview", "auto-summary"]):
            system_prompt = SYSTEM_PROMPT_SUMMARY
        else:
            system_prompt = SYSTEM_PROMPT_QA

        # Remove [page | section] headers for cleaner context
        context_text = "\n\n".join(c.get("text") for c in contexts)

        user_prompt = (
            f"Context:\n{context_text}\n\n"
            f"Question:\n{question}\n\n"
            "Answer concisely and in a human-friendly tone."
        )

        return system_prompt, user_prompt
