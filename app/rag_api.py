"""HTTP API for a small in-memory document RAG demo.

This is a local portfolio application, not a multi-user production service.
Documents stay in process memory and disappear when the server restarts.
"""
from __future__ import annotations

import tempfile
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.rag import answer_with_gemini, chunk_text, retrieve
from app.parser import parse_document

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}

app = FastAPI(
    title="Document RAG API",
    description="Upload a document, retrieve source passages, and optionally generate a cited answer.",
    version="1.0.0",
)


@app.get("/", include_in_schema=False)
def workspace():
    return FileResponse(Path(__file__).resolve().parent.parent / "static" / "rag.html")


@app.on_event("startup")
def initialize_store() -> None:
    app.state.documents = {}
    app.state.chunks = []


class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=4, ge=1, le=10)
    generate_answer: bool = False


def _extract_text(filename: str, payload: bytes) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Supported formats: .txt, .md, .pdf, and .docx",
        )
    if not payload:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if extension in {".txt", ".md"}:
        try:
            return payload.decode("utf-8-sig").strip()
        except UnicodeDecodeError as exc:
            raise HTTPException(status_code=400, detail="Text files must use UTF-8 encoding.") from exc

    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as temporary:
            temporary.write(payload)
            temporary_path = temporary.name
        return parse_document(temporary_path)["text"].strip()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not parse this document.") from exc
    finally:
        if temporary_path:
            Path(temporary_path).unlink(missing_ok=True)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "documents_indexed": len(app.state.documents)}


@app.get("/api/documents")
def list_documents() -> list[dict]:
    return [
        {"id": document_id, **metadata}
        for document_id, metadata in app.state.documents.items()
    ]


@app.post("/api/documents", status_code=201)
async def ingest_document(file: UploadFile = File(...)) -> dict:
    filename = Path(file.filename or "").name
    if not filename or Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Supported formats: .txt, .md, .pdf, and .docx",
        )

    payload = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(payload) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Maximum upload size is 10 MB.")
    text = _extract_text(filename, payload)
    if not text:
        raise HTTPException(
            status_code=422,
            detail="No text could be extracted. Scanned PDFs may require OCR.",
        )

    document_id = uuid.uuid4().hex
    chunks = chunk_text(text, source=filename)
    if not chunks:
        raise HTTPException(status_code=422, detail="No searchable text was found.")

    app.state.documents[document_id] = {
        "filename": filename,
        "characters": len(text),
        "chunk_count": len(chunks),
    }
    app.state.chunks.extend(
        type(chunk)(
            source=f"{document_id}:{filename}",
            index=chunk.index,
            text=chunk.text,
            tokens=chunk.tokens,
        )
        for chunk in chunks
    )
    return {"id": document_id, **app.state.documents[document_id]}


@app.delete("/api/documents/{document_id}", status_code=204)
def delete_document(document_id: str) -> None:
    if document_id not in app.state.documents:
        raise HTTPException(status_code=404, detail="Document not found.")
    del app.state.documents[document_id]
    prefix = f"{document_id}:"
    app.state.chunks = [chunk for chunk in app.state.chunks if not chunk.source.startswith(prefix)]


@app.post("/api/query")
def query_documents(request: QueryRequest) -> dict:
    if not app.state.chunks:
        raise HTTPException(status_code=409, detail="Upload a document before asking a question.")

    passages = retrieve(request.question, app.state.chunks, top_k=request.top_k)
    if not passages:
        return {
            "answer": "No relevant passages were found in the uploaded documents.",
            "sources": [],
            "mode": "retrieval_only",
        }

    for passage in passages:
        passage["source"] = passage["source"].split(":", 1)[-1]

    if request.generate_answer:
        try:
            answer = answer_with_gemini(request.question, passages)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail="The answer provider request failed.") from exc
        mode = "gemini_grounded"
    else:
        answer = "Retrieved relevant passages. Review the sources below to verify the answer."
        mode = "retrieval_only"

    return {"answer": answer, "sources": passages, "mode": mode}
