
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field

from adaptive_rag import adaptive_ask
from ingestion import extract_pdf
from chunking import create_chunks
from vector_store import store_chunks


# 1. Initialize FastAPI

app = FastAPI(
    title="Adaptive RAG System API",
    description=(
        "Upload PDF documents and ask questions using "
        "Retrieval-Augmented Generation."
    ),
    version="1.0.0"
)


# 2. Configuration

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# 3. Request Model

class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
        description="Question to ask about the documents"
    )


# 4. Home Endpoint

@app.get("/")
def home():
    return {
        "message": "Adaptive RAG API is running",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "upload_pdf": "/upload",
            "ask_question": "/ask"
        }
    }


# 5. Health Check Endpoint

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# 6. PDF Upload Endpoint

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF, extract its text, create chunks,
    and store the chunks in ChromaDB.
    """

    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    saved_path = None

    try:
        content = await file.read(MAX_FILE_SIZE + 1)

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF must be 10 MB or smaller."
            )
        
        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid PDF."
            )

        original_name = Path(file.filename).name
        saved_path = UPLOAD_DIR / f"{uuid4().hex}.pdf"

        saved_path.write_bytes(content)

        pages = extract_pdf(
            str(saved_path),
            source_name=original_name
        )

        if not pages:
            raise HTTPException(
                status_code=400,
                detail=(
                    "No extractable text was found in this PDF. "
                    "Scanned PDFs may require OCR."
                )
            )

        chunks = create_chunks(pages)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks could be created."
            )

        count = store_chunks(chunks)

        return {
            "message": "PDF uploaded and indexed successfully.",
            "filename": original_name,
            "pages_extracted": len(pages),
            "chunks_created": count
        }

    except HTTPException:
        raise

    except Exception as exc:
        print("PDF upload error:", repr(exc))

        if saved_path is not None:
            saved_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Failed to process the uploaded PDF."
        ) from exc

    finally:
        await file.close()


# 7. Ask Question Endpoint

@app.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Answer a question using the Adaptive RAG pipeline.
    """

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        result = adaptive_ask(question)
        return result

    except Exception as exc:
        print("Error processing question:", repr(exc))

        raise HTTPException(
            status_code=500,
            detail="Unable to process the question."
        ) from exc
