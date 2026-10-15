
from uuid import uuid4

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# 1. Connect to the local Ollama embedding model.
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# 2. Configure the persistent ChromaDB database.
vector_db = Chroma(
    collection_name="ai_documents",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


def store_chunks(chunks):
    """Store text chunks and metadata in ChromaDB."""

    if not chunks:
        raise ValueError("No chunks available to store.")

    texts = []
    metadatas = []

    for chunk in chunks:
        texts.append(chunk["text"])

        metadatas.append({
            "source": chunk["source"],
            "page": int(chunk["page"])
        })

    # Generate unique IDs so different uploads do not collide.
    ids = [
        f"chunk-{uuid4().hex}"
        for _ in chunks
    ]

    # Store the chunks, metadata, and embeddings.
    vector_db.add_texts(
        texts=texts,
        metadatas=metadatas,
        ids=ids
    )

    return len(chunks)


def search_chunks(question, k=4):
    if not question or not question.strip():
        return []

    if k < 1:
        raise ValueError("k must be at least 1.")

    # Retrieve extra candidates so we can remove duplicate pages.
    candidates = vector_db.similarity_search(
        question.strip(),
        k=max(k * 3, k)
    )

    results = []
    seen_pages = set()

    for doc in candidates:
        source = doc.metadata.get("source", "")
        page = doc.metadata.get("page")
        page_key = (source, page)

        if page_key in seen_pages:
            continue

        seen_pages.add(page_key)
        results.append(doc)

        if len(results) == k:
            break

    return results

def search_chunks_by_source(question, source, k=4):
    """Search only within chunks belonging to a PDF filename."""

    if not question or not question.strip():
        return []

    if not source or not source.strip():
        raise ValueError("Source filename cannot be empty.")

    if k < 1:
        raise ValueError("k must be at least 1.")

    return vector_db.similarity_search(
        question.strip(),
        k=k,
        filter={"source": source}
    )
