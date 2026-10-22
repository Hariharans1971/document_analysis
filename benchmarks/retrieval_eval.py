"""Small deterministic retrieval benchmark for the portfolio RAG demo.

Run from the repository root:
    python benchmarks/retrieval_eval.py

This is a tiny synthetic smoke benchmark, not a representative real-world RAG
quality evaluation. It measures whether the expected source appears in the
retrieved top-k results and reports mean reciprocal rank.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.rag import chunk_text, retrieve  # noqa: E402


DOCUMENTS = {
    "database.md": (
        "PostgreSQL query performance can improve when a suitable database index "
        "supports filtering and lookup operations. Use EXPLAIN to inspect the "
        "query plan and compare measured execution time before and after indexing."
    ),
    "uploads.md": (
        "The document upload API accepts TXT Markdown PDF and DOCX files. "
        "The maximum upload size is 10 MB. Invalid formats and oversized files "
        "should be rejected with a clear validation error."
    ),
    "api.md": (
        "The FastAPI endpoint accepts a JSON request and returns a JSON response. "
        "HTTP status codes communicate whether a request succeeded or failed. "
        "The interactive API documentation is available at the docs endpoint."
    ),
    "configuration.md": (
        "Configure the GEMINI_API_KEY environment variable to enable optional "
        "Gemini answer generation. Retrieval-only mode works without a model key. "
        "Never commit API keys to the repository."
    ),
    "retrieval.md": (
        "The current RAG prototype uses transparent lexical TF-IDF-style ranking "
        "with query term coverage. It does not use embeddings or a vector database. "
        "Lexical retrieval can miss semantically related passages with different words."
    ),
    "memory.md": (
        "Uploaded documents and chunks are held in process memory and disappear "
        "when the application restarts. Persistent storage and authentication are "
        "future improvements, not current features."
    ),
}

CASES = [
    ("How do PostgreSQL indexes improve query performance?", "database.md"),
    ("What is the maximum document upload size?", "uploads.md"),
    ("How does the API return a JSON response and HTTP status?", "api.md"),
    ("How do I configure GEMINI_API_KEY for answer generation?", "configuration.md"),
    ("Does the retriever use lexical ranking or vector embeddings?", "retrieval.md"),
    ("What happens to uploaded documents when the server restarts?", "memory.md"),
]


def main() -> int:
    chunks = []
    for source, text in DOCUMENTS.items():
        chunks.extend(chunk_text(text, source=source, chunk_size=120, overlap=15))

    reciprocal_ranks = []
    hits_at_1 = 0
    hits_at_3 = 0
    for question, expected_source in CASES:
        results = retrieve(question, chunks, top_k=3)
        ranked_sources = [item["source"] for item in results]
        rank = ranked_sources.index(expected_source) + 1 if expected_source in ranked_sources else 0
        reciprocal_ranks.append(1 / rank if rank else 0)
        hits_at_1 += rank == 1
        hits_at_3 += rank > 0
        print(f"expected={expected_source:<18} rank={rank or 'miss'} question={question}")

    count = len(CASES)
    recall_at_1 = hits_at_1 / count
    recall_at_3 = hits_at_3 / count
    mrr = sum(reciprocal_ranks) / count
    print("\nSynthetic retrieval benchmark")
    print(f"Queries: {count}")
    print(f"Recall@1: {recall_at_1:.3f} ({hits_at_1}/{count})")
    print(f"Recall@3: {recall_at_3:.3f} ({hits_at_3}/{count})")
    print(f"MRR:      {mrr:.3f}")
    print("These scores apply only to this tiny synthetic fixture.")
    return 0 if hits_at_3 == count else 1


if __name__ == "__main__":
    raise SystemExit(main())
