
from ingestion import extract_pdf
from chunking import create_chunks

pages = extract_pdf("uploads/sample.pdf")
chunks = create_chunks(pages)

print("Total pages:", len(pages))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks[:5], start=1):
    print(f"\n--- Chunk {i} ---")
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print("Text:", chunk["text"])
