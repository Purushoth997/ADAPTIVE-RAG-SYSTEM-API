
import re


STOP_WORDS = {
    "what", "which", "when", "where", "who", "why", "how",
    "does", "do", "did", "is", "are", "was", "were",
    "the", "a", "an", "in", "on", "of", "to", "for",
    "and", "or", "with", "about", "can", "could", "would",
    "things", "thing", "tell", "me", "please"
}


def tokenize(text):
    """Convert text into lowercase words."""
    return set(re.findall(r"\b[a-zA-Z0-9]+\b", text.lower()))


def check_relevance(question, documents, threshold=0.5):
    """
    Estimate relevance using question keyword overlap.
    This is a simple baseline, not semantic understanding.
    """

    if not documents:
        return {
            "relevant": False,
            "score": 0.0,
            "reason": "No documents were retrieved."
        }

    question_words = tokenize(question) - STOP_WORDS

    if not question_words:
        return {
            "relevant": False,
            "score": 0.0,
            "reason": "No useful keywords were found."
        }

    best_score = 0.0

    for doc in documents:
        document_words = tokenize(doc.page_content)
        overlap = question_words & document_words

        score = len(overlap) / len(question_words)
        best_score = max(best_score, score)

    relevant = best_score >= threshold

    return {
        "relevant": relevant,
        "score": round(best_score, 3),
        "reason": (
            "Question keywords matched retrieved content."
            if relevant
            else "Retrieved content has insufficient keyword overlap."
        )
    }
