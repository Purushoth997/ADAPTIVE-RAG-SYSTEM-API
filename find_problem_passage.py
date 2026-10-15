from ingestion import extract_pdf

pages = extract_pdf("uploads/sample.pdf")

keywords = [
    "big picture",
    "final goal",
    "individual stages",
    "inputs",
    "outputs",
    "logical reasoning",
    "problem-solving",
]

print("Total pages:", len(pages))

for index, page in enumerate(pages, start=1):
    text = page.get("text", "") if isinstance(page, dict) else str(page)

    matches = [word for word in keywords if word.lower() in text.lower()]

    if matches:
        print(f"\n--- PDF PAGE {index} ---")
        print("Matched:", ", ".join(matches))
        print(text[:1000])
