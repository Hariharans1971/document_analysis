# Document Q&A with Retrieval-Augmented Generation (RAG)

This repository now includes an educational RAG retrieval core in `app/rag.py`. It chunks a text or Markdown document, ranks relevant passages, returns source labels, and can optionally ask Gemini to draft an answer grounded in those passages.

## Why RAG?

A language model's internal knowledge is not a substitute for a specific source document. RAG first retrieves evidence from the document and then passes that evidence to the model. The numbered source labels make the response easier to verify.

## Architecture

```text
Text / Markdown file
        |
        v
Chunking with overlap
        |
        v
Token normalization + TF-IDF-style retrieval
        |
        v
Top-k evidence passages + source labels
        |
        +---- no API key ----> print retrieved evidence
        |
        +---- Gemini API ----> grounded answer with citations
```

The current implementation intentionally uses a transparent, lightweight lexical retriever. It does not use embeddings or a vector database yet. This keeps the retrieval layer runnable without a paid service or API key and makes the scoring easy to inspect.

## Setup

```bash
python -m venv .venv
```

Activate the virtual environment, then install project dependencies:

```bash
python -m pip install -r requirements.txt
```

## Retrieve passages without an API key

Create a local file such as `sample.md`, then run:

```bash
python -m app.rag sample.md "How does the system handle errors?" --top-k 4
```

Only `.txt` and `.md` are supported by this CLI retrieval function. The existing document-analysis parser supports PDF and DOCX for its analysis workflow; extending ingestion to those formats is a planned improvement.

## Optional Gemini generation

Set `GEMINI_API_KEY` in your shell. The existing requirements include the Google GenAI SDK.

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY = "your-key"
python -m app.rag sample.md "Summarize the setup steps" --generate
```

macOS/Linux:

```bash
export GEMINI_API_KEY="your-key"
python -m app.rag sample.md "Summarize the setup steps" --generate
```

Optional environment variable: `GEMINI_MODEL` (defaults to `gemini-2.5-flash`). Do not commit API keys. Retrieved passages are untrusted document content; the prompt instructs the model not to follow instructions embedded in source documents. This is a defense-in-depth measure, not a guarantee against prompt injection.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Limitations and next steps

- Lexical retrieval can miss semantically similar passages that use different words.
- No embedding model, vector store, reranker, or document-level access control is included yet.
- Citation labels point to retrieved chunks; they do not guarantee every generated claim is supported.
- Large or scanned PDFs need OCR and bounded ingestion before they can be indexed safely.
- Production deployments should add file-size/type validation, access control, tenant isolation, logging, evaluation datasets, and retrieval-quality metrics.

## Evaluation plan

For a serious portfolio version, create 20–50 question/expected-source pairs and measure Recall@k, citation correctness, and answer faithfulness. Compare lexical retrieval against an embedding-based baseline before claiming quality improvements.
