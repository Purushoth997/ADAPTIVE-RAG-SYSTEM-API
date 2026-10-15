
from vector_store import search_chunks
from adaptive_rag import is_relevant

question = "What are classification algorithms in AI?"

documents = search_chunks(question, k=4)

print("Retrieved chunks:", len(documents))

for index, doc in enumerate(documents, start=1):
    print(f"\n--- Chunk {index} ---")
    print("Page:", doc.metadata.get("page"))
    print(doc.page_content[:500])

print("\nRelevance grader result:")
print(is_relevant(question, documents))
