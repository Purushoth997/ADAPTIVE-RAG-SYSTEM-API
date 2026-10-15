
from ingestion import extract_pdf

pages = extract_pdf("uploads/sample.pdf")

for page in pages:
    print(f"\nSource: {page['source']}")
    print(f"Page: {page['page']}")
    print(page["text"][:500])
