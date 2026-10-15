
from ingestion import extract_pdf
from chunking import create_chunks
from vector_store import store_chunks, search_chunks

pages = extract_pdf("uploads/sample.pdf")
print("Pages extracted:", len(pages))

chunks = create_chunks(pages)
print("Chunks created:", len(chunks))

count = store_chunks(chunks)
print("Chunks stored:", count)

question = "What are classification algorithms in AI?"

results = search_chunks(question, k=4)

print("\nSearch results:")

for result in results:
    print("\nSource:", result.metadata["source"])
    print("Page:", result.metadata["page"])
    print("Text:", result.page_content[:400])
