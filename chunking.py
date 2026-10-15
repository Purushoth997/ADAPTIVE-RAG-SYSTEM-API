
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(pages):
    """Split extracted pages into chunks while preserving metadata."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for chunk in page_chunks:
            if chunk.strip():
                chunks.append({
                    "text": chunk,
                    "source": page["source"],
                    "page": page["page"]
                })

    return chunks
