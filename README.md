# Document Analysis, Migration Readiness & RAG

A Python portfolio project combining PDF/DOCX analysis with a browser-based Retrieval-Augmented Generation (RAG) workspace. Upload documents, retrieve source passages, and optionally generate answers with Gemini.

## What is implemented

- **Document analysis:** PDF/DOCX parsing, structure metrics, readability heuristics, migration-readiness reports, and existing analysis workflow.
- **Full-stack RAG:** FastAPI endpoints plus an HTML/CSS/JavaScript browser interface.
- **Ingestion:** TXT, Markdown, PDF, and DOCX uploads, with a 10 MB limit and text-extraction checks.
- **Retrieval:** overlapping chunks and transparent lexical ranking with source labels.
- **Optional generation:** Gemini answers grounded in retrieved passages when `GEMINI_API_KEY` is configured.
- **Engineering:** API validation, document removal, unit/API tests, and GitHub Actions.

## Technology

Python · FastAPI · SQLite-free in-memory demo store · HTML/CSS/JavaScript · PyMuPDF · python-docx · Google GenAI SDK · unittest

## Quick start

Requires Python 3.10+.

```bash
git clone https://github.com/Hariharans1971/document_analysis.git
cd document_analysis
python -m venv .venv
python -m pip install -r requirements-dev.txt
uvicorn app.rag_api:app --reload
```

Open:
- Browser workspace: http://127.0.0.1:8000
- Interactive REST API: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Docker

```bash
docker build -t document-rag .
docker run --rm -p 8000:8000 document-rag
```

To enable Gemini generation, create a local `.env` from `.env.example` and pass it with `--env-file .env`. Never commit your real key. The in-memory document index resets when the container stops.

RAG works in retrieval-only mode without an API key. To enable answer generation, configure `GEMINI_API_KEY` in your environment before starting the app.

## Tests and retrieval evaluation

Run the automated tests:

```bash
python -m unittest tests.test_rag tests.test_rag_api -v
```

Run the deterministic synthetic retrieval benchmark:

```bash
python benchmarks/retrieval_eval.py
```

The latest recorded CI run passed the automated tests and six-query synthetic retrieval benchmark: Recall@1 = 6/6 (1.000), Recall@3 = 6/6 (1.000), and MRR = 1.000. These scores apply only to a tiny synthetic fixture built around the demo's own documents; they are a smoke-test baseline, not production-quality evidence. A later CI run is checking the PyMuPDF import cleanup. Evaluate a larger, independently labelled dataset before making quality or business-impact claims.

## Architecture and API documentation

See [RAG_GUIDE.md](RAG_GUIDE.md) for the request flow and API reference, and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design decisions, trade-offs, security constraints, and evaluation strategy.

## Important limitations

This is an educational single-process demo. Uploaded documents and chunks stay in memory and are lost on restart. Retrieval currently uses lexical ranking, not embeddings or a vector database. There is no authentication, multi-user isolation, OCR, or production security layer. Do not upload confidential or regulated documents.

## Roadmap

- Embedding retrieval and persistent vector storage
- Retrieval evaluation (Recall@k) and citation-faithfulness checks
- Authentication and per-user document permissions
- Persistent index, structured logging, and Docker deployment
- OCR support for scanned PDFs
