from time import perf_counter
from langchain_ollama import ChatOllama
from vector_store import search_chunks
from relevance_checker import check_relevance
from time import perf_counter


llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def rewrite_question(question):
    """Rewrite the question to improve document retrieval."""

    prompt = f"""
Rewrite the question as a search query for an AI textbook.
Preserve its meaning and use relevant technical keywords.
Do not answer the question.
Return only the rewritten query.

Question: {question}

Search query:
"""

    response = llm.invoke(prompt)
    rewritten = response.content.strip().strip('"')

    print("Rewritten query:", rewritten)

    return rewritten or question


def generate_answer(question, documents):
    """Generate an answer using retrieved PDF chunks."""

    if not documents:
        return "NOT_FOUND"

    context = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'Unknown')}, "
        f"Page: {doc.metadata.get('page', 'Unknown')}\n"
        f"{doc.page_content}"
        for doc in documents
    )

    prompt = f"""
Answer the question using only the supplied context.

Rules:
- Use only facts supported by the context.
- Do not use outside knowledge.
- If the context does not contain enough information
  to answer the question, return exactly: NOT_FOUND
- Do not explain the NOT_FOUND response.
- Otherwise, provide a clear and concise answer.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content.strip()


def get_sources(documents):
    """Return unique source and page combinations."""

    sources = []
    seen = set()

    for doc in documents:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "Unknown")
        key = (source, page)

        if key not in seen:
            seen.add(key)

            sources.append({
                "source": source,
                "page": page
            })

    return sources


def merge_documents(*groups):
    """Combine retrieval results without duplicate chunks."""

    merged = []
    seen = set()

    for documents in groups:
        for doc in documents:
            key = (
                doc.metadata.get("source"),
                doc.metadata.get("page"),
                doc.page_content
            )

            if key not in seen:
                seen.add(key)
                merged.append(doc)

    return merged



def adaptive_ask(question):
    """Retrieve documents, check relevance, generate an answer, and measure latency."""
    total_start = perf_counter()

    # Attempt 1: Search using the original question.
    print("\nAttempt 1: Original query")
    retrieval_start = perf_counter()
    original_docs = search_chunks(question, k=4)
    original_retrieval_time = perf_counter() - retrieval_start
    print("Retrieved chunks:", len(original_docs))

    # Attempt 2: Rewrite the question and search again.
    print("\nAttempt 2: Rewritten query")
    rewrite_start = perf_counter()
    rewritten = rewrite_question(question)
    rewrite_time = perf_counter() - rewrite_start

    retrieval_start = perf_counter()
    rewritten_docs = search_chunks(rewritten, k=8)
    rewritten_retrieval_time = perf_counter() - retrieval_start

    # Combine both retrieval results.
    documents = merge_documents(original_docs, rewritten_docs)
    print("Combined unique chunks:", len(documents))

    # Check whether retrieved documents match the question.
    relevance_start = perf_counter()
    relevance = check_relevance(question, documents)
    relevance_time = perf_counter() - relevance_start

    print("Relevance score:", relevance["score"])
    print("Relevant context:", relevance["relevant"])
    print("Reason:", relevance["reason"])

    answer_supported = False
    sources = []

    # Generate an answer only if the relevance check passes.
    generation_time = 0.0

    if relevance["relevant"]:
        generation_start = perf_counter()
        answer = generate_answer(question, documents)
        generation_time = perf_counter() - generation_start

        if answer.strip().upper() == "NOT_FOUND":
            answer = (
                "I could not find enough information "
                "to answer this question in the document."
            )
        else:
            answer_supported = True
            sources = get_sources(documents)
    else:
        answer = (
            "I could not find relevant information "
            "to answer this question in the document."
        )

    total_time = perf_counter() - total_start

    # Return answer, sources, and measurable performance data.
    return {
        "answer": answer,
        "sources": sources,
        "retrieval_attempts": 2,
        "relevant_context_found": bool(relevance["relevant"]),
        "answer_supported": answer_supported,
        "relevance_score": relevance["score"],
        "rewritten_query": rewritten,
        "latency_seconds": {
            "original_retrieval": round(original_retrieval_time, 4),
            "query_rewriting": round(rewrite_time, 4),
            "rewritten_retrieval": round(rewritten_retrieval_time, 4),
            "relevance_check": round(relevance_time, 4),
            "answer_generation": round(generation_time, 4),
            "total": round(total_time, 4)
        }
    }
