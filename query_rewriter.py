
"""Simple rule-based query rewriting for Adaptive RAG."""

def rewrite_query(question: str) -> str:
    """Rewrite known queries to improve retrieval."""

    normalized = question.strip().lower()

    rewrites = {
        "what questions help define a problem for an algorithm?":
            "What are the inputs, outputs, decisions, and repeated "
            "steps when understanding a problem?"
    }

    return rewrites.get(normalized, question.strip())
