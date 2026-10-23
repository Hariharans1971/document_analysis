"""Deterministic synthetic regression benchmark for the portfolio RAG demo.

Run from the repository root:
    python benchmarks/retrieval_eval.py

The labelled questions are authored for this small fixture. Results compare the
TF-IDF-style retriever to simple distinct-term overlap and include negative
queries that should return no passages. This is regression evidence, not an
independent or representative real-world retrieval evaluation.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.rag import Chunk, chunk_text, retrieve, tokenize  # noqa: E402


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

# One expected source per question. The set covers each fixture document with
# varied but intentionally synthetic queries.
CASES = [
    ("How can PostgreSQL indexes accelerate selective lookups?", "database.md"),
    ("Which command exposes SQL query plans and measured execution times around indexing?", "database.md"),
    ("What can speed up filtering operations in a relational database?", "database.md"),
    ("Does the example compare performance before and after indexing?", "database.md"),
    ("Which extensions are accepted by the document upload API?", "uploads.md"),
    ("How large can an uploaded file be?", "uploads.md"),
    ("What should happen to invalid formats and files over the size limit?", "uploads.md"),
    ("What is the maximum size limit for a DOCX file?", "uploads.md"),
    ("Which framework's endpoints accept JSON and return JSON?", "api.md"),
    ("What does an HTTP status code signal about request outcome?", "api.md"),
    ("Where can I see interactive API docs?", "api.md"),
    ("Which interface exposes the docs endpoint for the service?", "api.md"),
    ("How do I configure optional Gemini answer generation?", "configuration.md"),
    ("Can retrieval work without a model key?", "configuration.md"),
    ("What is the security rule for provider keys in source control?", "configuration.md"),
    ("Which environment variable activates Gemini responses?", "configuration.md"),
    ("Does this prototype use a vector database?", "retrieval.md"),
    ("How are passages ranked by the retriever?", "retrieval.md"),
    ("Why might lexical search miss semantically related text?", "retrieval.md"),
    ("Is semantic vector search available in the current implementation?", "retrieval.md"),
    ("Where are uploaded document contents stored?", "memory.md"),
    ("What happens to documents after the application restarts?", "memory.md"),
    ("Is the document index persistent across restarts?", "memory.md"),
    ("Does the demo currently implement persistent index storage?", "memory.md"),
]

# Queries intentionally use vocabulary outside the six synthetic documents.
# They check the current retriever's ability to return an empty result when no
# query term occurs in the indexed fixture; they do not measure semantic safety.
NEGATIVE_CASES = [
    "quantum entanglement superconducting telescopes",
    "Kubernetes GPU drivers",
    "Botswana population demographics",
    "cryptocurrency blockchains taxation wallets",
    "Martian weather forecast",
    "CRISPR protein synthesis",
]


def build_chunks() -> list[Chunk]:
    chunks: list[Chunk] = []
    for source, text in DOCUMENTS.items():
        chunks.extend(chunk_text(text, source=source, chunk_size=120, overlap=15))
    return chunks


def overlap_baseline(question: str, chunks: list[Chunk], top_k: int = 3) -> list[str]:
    """Return source ranks from a simple distinct-query-term overlap baseline."""
    query_terms = set(tokenize(question))
    if not query_terms:
        return []

    scored: list[tuple[int, Chunk]] = []
    for chunk in chunks:
        overlap = len(query_terms.intersection(chunk.tokens))
        if overlap:
            scored.append((overlap, chunk))

    scored.sort(key=lambda item: (-item[0], item[1].source, item[1].index))
    return [chunk.source for _, chunk in scored[:top_k]]


def rank_of(expected_source: str, ranked_sources: list[str]) -> int:
    try:
        return ranked_sources.index(expected_source) + 1
    except ValueError:
        return 0


def summarize_ranks(ranks: list[int]) -> dict[str, float | int]:
    if not ranks:
        return {"queries": 0, "recall_at_1": 0.0, "recall_at_3": 0.0, "mrr": 0.0}
    return {
        "queries": len(ranks),
        "recall_at_1": sum(rank == 1 for rank in ranks) / len(ranks),
        "recall_at_3": sum(0 < rank <= 3 for rank in ranks) / len(ranks),
        "mrr": sum((1 / rank) if rank else 0.0 for rank in ranks) / len(ranks),
    }


def main() -> int:
    chunks = build_chunks()
    if len(CASES) < 20:
        print("FAIL: expected at least 20 positive synthetic cases.")
        return 1
    if any(source not in DOCUMENTS for _, source in CASES):
        print("FAIL: a labelled case references a source outside the fixture.")
        return 1
    if len({question for question, _ in CASES}) != len(CASES):
        print("FAIL: duplicate positive questions found.")
        return 1

    retriever_ranks: list[int] = []
    baseline_ranks: list[int] = []
    for question, expected_source in CASES:
        results = retrieve(question, chunks, top_k=3)
        ranked_sources = [item["source"] for item in results]
        retriever_rank = rank_of(expected_source, ranked_sources)
        baseline_rank = rank_of(
            expected_source,
            overlap_baseline(question, chunks, top_k=3),
        )
        retriever_ranks.append(retriever_rank)
        baseline_ranks.append(baseline_rank)
        print(
            f"expected={expected_source:<18} "
            f"retriever_rank={retriever_rank or 'miss'} "
            f"overlap_rank={baseline_rank or 'miss'} "
            f"question={question}"
        )

    retriever_metrics = summarize_ranks(retriever_ranks)
    baseline_metrics = summarize_ranks(baseline_ranks)

    print("\nSynthetic positive-query regression set")
    print(f"Queries:    {retriever_metrics['queries']}")
    print(
        f"Retriever Recall@1: {retriever_metrics['recall_at_1']:.3f} "
        f"({sum(rank == 1 for rank in retriever_ranks)}/{len(CASES)})"
    )
    print(
        f"Retriever Recall@3: {retriever_metrics['recall_at_3']:.3f} "
        f"({sum(0 < rank <= 3 for rank in retriever_ranks)}/{len(CASES)})"
    )
    print(f"Retriever MRR:      {retriever_metrics['mrr']:.3f}")
    print(
        f"Overlap baseline Recall@1: {baseline_metrics['recall_at_1']:.3f} "
        f"({sum(rank == 1 for rank in baseline_ranks)}/{len(CASES)})"
    )
    print(
        f"Overlap baseline Recall@3: {baseline_metrics['recall_at_3']:.3f} "
        f"({sum(0 < rank <= 3 for rank in baseline_ranks)}/{len(CASES)})"
    )
    print(f"Overlap baseline MRR:      {baseline_metrics['mrr']:.3f}")

    negative_hits = 0
    for question in NEGATIVE_CASES:
        results = retrieve(question, chunks, top_k=3)
        if results:
            negative_hits += 1
            print(
                "UNEXPECTED PASSAGE FOR NEGATIVE QUERY: "
                f"{question!r} -> {[item['source'] for item in results]}"
            )
    negative_abstention_rate = (
        (len(NEGATIVE_CASES) - negative_hits) / len(NEGATIVE_CASES)
        if NEGATIVE_CASES
        else 1.0
    )
    print("\nSynthetic negative-query smoke check")
    print(
        f"Empty-result rate: {negative_abstention_rate:.3f} "
        f"({len(NEGATIVE_CASES) - negative_hits}/{len(NEGATIVE_CASES)})"
    )
    print(
        "Interpretation: authored synthetic cases exercise regression behavior; "
        "they are not an independent, representative quality evaluation."
    )

    all_positive_retrieved = all(0 < rank <= 3 for rank in retriever_ranks)
    all_negative_abstained = negative_hits == 0
    return 0 if all_positive_retrieved and all_negative_abstained else 1


if __name__ == "__main__":
    raise SystemExit(main())
