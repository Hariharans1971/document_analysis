import unittest
from io import BytesIO

from fastapi.testclient import TestClient

from app.rag_api import app


class RagApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None, None, None)

    def test_upload_query_and_delete_document(self):
        payload = (
            b"PostgreSQL indexes can improve query performance by reducing "
            b"the amount of data scanned for selective queries."
        )
        uploaded = self.client.post(
            "/api/documents",
            files={"file": ("database-guide.txt", BytesIO(payload), "text/plain")},
        )
        self.assertEqual(uploaded.status_code, 201, uploaded.text)
        document_id = uploaded.json()["id"]
        self.assertEqual(uploaded.json()["chunk_count"], 1)

        result = self.client.post(
            "/api/query",
            json={"question": "How do PostgreSQL indexes improve query performance?", "top_k": 3},
        )
        self.assertEqual(result.status_code, 200, result.text)
        self.assertTrue(result.json()["sources"])
        self.assertIn("database-guide.txt", result.json()["sources"][0]["source"])

        deleted = self.client.delete(f"/api/documents/{document_id}")
        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(self.client.get("/api/documents").json(), [])

    def test_query_without_documents_returns_conflict(self):
        response = self.client.post("/api/query", json={"question": "What is this about?"})
        self.assertEqual(response.status_code, 409)

    def test_rejects_unsupported_file_extension(self):
        response = self.client.post(
            "/api/documents",
            files={"file": ("script.exe", BytesIO(b"not a document"), "application/octet-stream")},
        )
        self.assertEqual(response.status_code, 415)

    def test_rejects_empty_text_file(self):
        response = self.client.post(
            "/api/documents",
            files={"file": ("empty.txt", BytesIO(b"  "), "text/plain")},
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
