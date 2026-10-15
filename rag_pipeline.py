
from langchain_ollama import ChatOllama
from vector_store import search_chunks


llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def ask_question(question: str) -> dict:
    documents = search_chunks(question, k=4)

    if not documents:
        return {
            "answer": "I could not find relevant information in the PDF.",
            "sources": []
        }

    context = "\n\n".join(
        f"Source: {doc.metadata['source']}, "
        f"Page: {doc.metadata['page']}\n{doc.page_content}"
        for doc in documents
    )

    prompt = f"""
You are a helpful assistant answering questions about a PDF.

Answer the question using only the context provided below.
If the context does not contain the answer, say that you
could not find the answer in the document.
Do not invent facts.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    sources = [
        {
            "source": doc.metadata["source"],
            "page": doc.metadata["page"]
        }
        for doc in documents
    ]

    return {
        "answer": response.content,
        "sources": sources
    }
