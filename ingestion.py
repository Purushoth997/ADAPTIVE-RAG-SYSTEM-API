
import pymupdf
from pathlib import Path


def extract_pdf(
    file_path: str,
    source_name: str | None = None
) -> list[dict]:
    """Extract PDF text while preserving page and source metadata."""

    pages = []

    source = Path(source_name or file_path).name

    with pymupdf.open(file_path) as document:
        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text", sort=True).strip()

            if text:
                pages.append({
                    "text": text,
                    "page": page_number,
                    "source": source
                })

    return pages
