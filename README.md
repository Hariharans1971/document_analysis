# Document Analysis, Migration Readiness & RAG

A Python project for analyzing PDF/DOCX structure and evaluating documentation migration readiness, now with a small Retrieval-Augmented Generation (RAG) module for source-grounded document Q&A.

## Features

- PDF and DOCX parsing for document analysis
- Structural metrics, readability heuristics, and migration readiness reports
- Optional LLM-assisted document analysis using the existing provider integration
- Text/Markdown chunking and lexical retrieval with source labels
- Optional Gemini answer generation grounded in retrieved passages
- Unit tests for retrieval and ranking

## Technology

- Python
- PyMuPDF and python-docx
- FastAPI/Streamlit dependencies included for existing app workflows
- Google GenAI SDK for optional RAG generation
- Python standard-library retrieval core

## Quick start

Requires Python 3.10+.

```bash
git clone https://github.com/Hariharans1971/document_analysis.git
cd document_analysis
python -m venv .venv
python -m pip install -r requirements.txt
```

Activate the virtual environment before running the commands below.

## RAG: retrieve evidence from a document

Create a local `sample.md` or `sample.txt`, then run:

```bash
python -m app.rag sample.md "What does the document say about setup?" --top-k 4
```

This works without an API key and prints the passages ranked as relevant. For a generated answer with source labels, configure `GEMINI_API_KEY` and add `--generate`.

Full details: [RAG_GUIDE.md](RAG_GUIDE.md).

## Existing document analysis workflow

The repository also includes the existing document parsing, metrics, migration-readiness analysis, and optional LLM analysis modules. Check `run.py` and `ui.py` for the current entry points.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Security and limitations

- Never commit API keys, passwords, or confidential documents.
- Use synthetic or public documents while testing.
- RAG retrieval is lexical today; embeddings and vector databases are future improvements.
- LLM responses can still be wrong. Verify important claims against the cited source passages.
- Do not upload private or regulated documents to external model providers without authorization.

## Roadmap

- PDF/DOCX ingestion into the RAG index
- Persistent vector storage and embedding retrieval
- Evaluation set with Recall@k and citation faithfulness checks
- FastAPI endpoints and a document-chat interface
- Docker deployment and structured observability

## Author

Hariharan S. — B.Tech Computer Science and Engineering (AI & ML), 2026
