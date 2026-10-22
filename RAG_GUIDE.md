# Document Q&A with Retrieval-Augmented Generation (RAG)

This project now includes a browser-based RAG workspace and a FastAPI API. It accepts TXT, Markdown, PDF, and DOCX documents, retrieves relevant text passages, returns source labels, and optionally uses Gemini to draft a grounded answer.

## Architecture

```text
Browser UI (HTML/CSS/JavaScript)
        | multipart upload / JSON question
        v
FastAPI API (upload validation, extraction, endpoints)
        |
        v
Document parsing + overlapping chunks
        |
        v
Lexical TF-IDF-style retrieval
        |
        +---- retrieval-only response with source passages
        |
        +---- optional Gemini answer grounded in passages
```

The retrieval core deliberately uses transparent lexical scoring rather than embeddings today. It is inexpensive to run, has no vector-store dependency, and is easy to test. Embedding retrieval is a planned upgrade, not a feature currently claimed.

## Setup

Requires Python 3.10+.

```bash
git clone https://github.com/Hariharans1971/document_analysis.git
cd document_analysis
python -m venv .venv
python -m pip install -r requirements-dev.txt
```

Activate the virtual environment:

- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

## Run the full-stack RAG app

```bash
uvicorn app.rag_api:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) for the browser workspace or [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

### Run with Docker

```bash
docker build -t document-rag .
docker run --rm -p 8000:8000 --env-file .env document-rag
```

Create a local `.env` from `.env.example` only if you want optional Gemini generation. Do not commit the real `.env` file. Uploaded files are held in memory; this container does not persist the index.

### API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check and current document count |
| GET | `/api/documents` | List documents currently indexed |
| POST | `/api/documents` | Upload TXT, MD, PDF, or DOCX using multipart form data |
| DELETE | `/api/documents/{document_id}` | Remove a document and its chunks |
| POST | `/api/query` | Retrieve source passages and optionally generate an answer |

The upload endpoint has a 10 MB limit. Retrieval-only mode works without a model API key. To generate answers, set `GEMINI_API_KEY`; optionally set `GEMINI_MODEL` (defaults to `gemini-2.5-flash`).

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY = "your-key"
uvicorn app.rag_api:app --reload
```

macOS/Linux:

```bash
export GEMINI_API_KEY="your-key"
uvicorn app.rag_api:app --reload
```

Never commit API keys. Retrieved document content is untrusted input; prompt-injection defenses are best-effort, not a security guarantee.

## CLI retrieval without a server

```bash
python -m app.rag sample.pdf "What does the document say about setup?" --top-k 4
```

The CLI supports TXT, Markdown, PDF, and DOCX. Scanned PDFs without an embedded text layer need OCR.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m unittest tests.test_rag tests.test_rag_api -v
```

GitHub Actions runs these retrieval and API tests on pushes and pull requests. Check the repository's Actions tab for the current result.

## Current limitations

- Documents and chunks are held in process memory and disappear when the server restarts.
- The app is a single-process portfolio demo; it has no login, tenant isolation, or persistent index.
- Lexical retrieval can miss semantically similar passages with different vocabulary.
- Source labels help verification but do not prove every generated claim is supported.
- Scanned PDFs need OCR; no OCR pipeline is included.
- Do not upload confidential or regulated documents to this demo.

## Next engineering upgrades

1. Add embedding-based retrieval and a persistent vector database.
2. Add a small question/expected-source evaluation set and report Recall@k.
3. Add authentication, per-user document access, persistent storage, and audit logging.
4. Evaluate citation correctness and answer faithfulness before claiming model quality.
5. Containerize the service and deploy with appropriate limits and secrets management.
