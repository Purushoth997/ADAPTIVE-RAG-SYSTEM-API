from ingestion import extract_pdf

pages = extract_pdf("uploads/sample.pdf")

print("Total pages:", len(pages))

for page_num in [123, 124, 125, 126, 151]:
    print(f"\n{'=' * 15} PAGE {page_num} {'=' * 15}")
    page = pages[page_num - 1]

    if isinstance(page, dict):
        text = page.get("text", str(page))
    else:
        text = str(page)

    print(text[:2000])
