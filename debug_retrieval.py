
from vector_store import search_chunks
from adaptive_rag import rewrite_question, is_relevant

question = "How does AI classify things?"

rewritten = rewrite_question(question)

print("Original question:", question)
print("Rewritten query:", rewritten)

original_docs = search_chunks(question, k=4)

print("\n--- Original query results ---")
for i, doc in enumerate(original_docs, start=1):
    print(f"\nResult {i}")
    print("Source:", doc.metadata.get("source"))
    print("Page:", doc.metadata.get("page"))
    print("Text:", doc.page_content[:350])

print("\nOriginal results relevant?", is_relevant(question, original_docs))

rewritten_docs = search_chunks(rewritten, k=8)

print("\n--- Rewritten query results ---")
for i, doc in enumerate(rewritten_docs, start=1):
    print(f"\nResult {i}")
    print("Source:", doc.metadata.get("source"))
    print("Page:", doc.metadata.get("page"))
    print("Text:", doc.page_content[:350])

print("\nRewritten results relevant?", is_relevant(question, rewritten_docs))
