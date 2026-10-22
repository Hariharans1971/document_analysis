import unittest

from app.rag import chunk_text, retrieve


class RagRetrievalTests(unittest.TestCase):
    def test_chunk_text_returns_overlapping_chunks(self):
        text = " ".join(f"word{i}" for i in range(11))
        chunks = chunk_text(text, source="guide.txt", chunk_size=5, overlap=2)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0].source, "guide.txt")
        self.assertIn("word3", chunks[1].text)

    def test_retrieval_ranks_relevant_passage_first(self):
        chunks = (
            chunk_text("PostgreSQL indexes improve query lookup speed.", "database.md", 20, 2)
            + chunk_text("CSS grid helps arrange responsive user interfaces.", "frontend.md", 20, 2)
        )
        results = retrieve("How do PostgreSQL indexes improve query speed?", chunks, top_k=2)
        self.assertTrue(results)
        self.assertEqual(results[0]["source"], "database.md")
        self.assertIn("[1]", results[0]["citation"])

    def test_empty_question_and_no_match(self):
        chunks = chunk_text("A small document about databases.", "db.txt")
        self.assertEqual(retrieve("", chunks), [])
        self.assertEqual(retrieve("quantum telescope", chunks), [])

    def test_invalid_chunk_settings_raise(self):
        with self.assertRaises(ValueError):
            chunk_text("hello world", chunk_size=3, overlap=3)
        with self.assertRaises(ValueError):
            retrieve("hello", [], top_k=0)


if __name__ == "__main__":
    unittest.main()
