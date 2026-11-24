"""
DocuVerse AI - Automated Test Suite (test_backend.py)
=====================================================
Comprehensive tests covering:
- Root & Health endpoints
- PDF upload & validation (valid, invalid extension, corrupt)
- Document collection creation & isolation
- Question answering (RAG) & Citation formatting
- Executive Summary generation
- Practice MCQs generation
- Key Points extraction
- Collection deletion & cleanup
- Missing API key & error handling
"""

import io
import pytest
from fastapi.testclient import TestClient
import pymupdf

import config
from main import app
from vector_store import get_collection_manager

client = TestClient(app)


@pytest.fixture(scope="module")
def sample_pdf_bytes():
    """Generates a valid 2-page in-memory PDF for testing."""
    doc = pymupdf.open()
    
    # Page 1
    p1 = doc.new_page()
    p1.insert_text(
        (50, 72),
        "DocuVerse AI is an intelligent document Q&A assistant created by Pankaj Kumar. "
        "It uses Retrieval-Augmented Generation (RAG) to answer questions strictly from uploaded documents."
    )
    
    # Page 2
    p2 = doc.new_page()
    p2.insert_text(
        (50, 72),
        "Machine Learning algorithms learn from sample data to make predictions. "
        "Deep Learning utilizes multi-layered artificial neural networks. "
        "FAISS is an efficient vector similarity search library."
    )
    
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


# --------------------------------------------------------------------
# 1. ROOT & HEALTH TESTS
# --------------------------------------------------------------------
def test_root_endpoint():
    """Tests GET / returns application info and online status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "DocuVerse AI Backend"
    assert data["status"] == "online"
    assert data["docs_url"] == "/docs"


def test_health_endpoint():
    """Tests GET /health returns backend health status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "groq_api_configured" in data
    assert "supported_languages" in data


# --------------------------------------------------------------------
# 2. PDF UPLOAD & VALIDATION TESTS
# --------------------------------------------------------------------
def test_upload_invalid_file_extension():
    """Tests uploading a non-PDF file returns 400 Bad Request."""
    file_content = b"This is just a plain text file, not a PDF."
    response = client.post(
        "/api/documents/upload",
        files=[("files", ("notes.txt", file_content, "text/plain"))]
    )
    assert response.status_code == 400
    assert "Only PDF documents (.pdf) are supported" in response.json()["detail"]


def test_upload_corrupt_pdf():
    """Tests uploading a corrupt fake PDF without %PDF header returns 400."""
    fake_pdf_content = b"Not a real PDF stream content"
    response = client.post(
        "/api/documents/upload",
        files=[("files", ("corrupt.pdf", fake_pdf_content, "application/pdf"))]
    )
    assert response.status_code == 400
    assert "missing %PDF signature" in response.json()["detail"]


def test_upload_valid_pdf_and_create_collection(sample_pdf_bytes):
    """Tests uploading a valid PDF successfully creates an isolated collection."""
    response = client.post(
        "/api/documents/upload",
        files=[("files", ("ai_syllabus.pdf", sample_pdf_bytes, "application/pdf"))]
    )
    assert response.status_code == 201
    data = response.json()
    assert "collection_id" in data
    assert data["total_files"] == 1
    assert data["total_pages"] == 2
    assert data["total_chunks"] >= 2
    assert "ai_syllabus.pdf" in data["file_names"]


# --------------------------------------------------------------------
# 3. CHAT, RAG & CITATION FORMATTING TESTS
# --------------------------------------------------------------------
def test_chat_question_answering(sample_pdf_bytes, monkeypatch):
    """Tests POST /api/chat retrieves context and returns formatted answer & citations."""
    # 1. Upload document first
    up_res = client.post(
        "/api/documents/upload",
        files=[("files", ("ai_notes.pdf", sample_pdf_bytes, "application/pdf"))]
    )
    collection_id = up_res.json()["collection_id"]

    # 2. Ask question
    chat_payload = {
        "collection_id": collection_id,
        "question": "Who created DocuVerse AI?",
        "language": "English"
    }
    response = client.post("/api/chat", json=chat_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["collection_id"] == collection_id
    assert data["success"] is True
    assert len(data["answer"]) > 0

    # 3. Verify exact citation formatting
    assert "sources" in data
    assert len(data["sources"]) > 0
    citation = data["sources"][0]
    assert citation["source"] == "ai_notes.pdf"
    assert citation["page"] in [1, 2]
    assert isinstance(citation["score"], float)
    assert len(citation["snippet"]) > 0


def test_chat_nonexistent_collection():
    """Tests POST /api/chat with an invalid collection_id returns 404."""
    chat_payload = {
        "collection_id": "non_existent_12345",
        "question": "What is machine learning?",
        "language": "English"
    }
    response = client.post("/api/chat", json=chat_payload)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_chat_empty_question(sample_pdf_bytes):
    """Tests POST /api/chat with empty question returns 400 Bad Request."""
    up_res = client.post(
        "/api/documents/upload",
        files=[("files", ("test.pdf", sample_pdf_bytes, "application/pdf"))]
    )
    collection_id = up_res.json()["collection_id"]

    chat_payload = {
        "collection_id": collection_id,
        "question": "   ",
        "language": "English"
    }
    response = client.post("/api/chat", json=chat_payload)
    assert response.status_code == 400


# --------------------------------------------------------------------
# 4. DOCUMENT INTELLIGENCE (SUMMARY, MCQS, KEY POINTS)
# --------------------------------------------------------------------
def test_document_summary(sample_pdf_bytes, monkeypatch):
    """Tests POST /api/documents/{id}/summary returns executive summary."""
    up_res = client.post(
        "/api/documents/upload",
        files=[("files", ("paper.pdf", sample_pdf_bytes, "application/pdf"))]
    )
    collection_id = up_res.json()["collection_id"]

    # Mock or live call
    response = client.post(
        f"/api/documents/{collection_id}/summary",
        json={"language": "English"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["collection_id"] == collection_id
    assert len(data["summary"]) > 0


def test_document_mcqs(sample_pdf_bytes):
    """Tests POST /api/documents/{id}/mcqs returns practice questions."""
    up_res = client.post(
        "/api/documents/upload",
        files=[("files", ("mcq_doc.pdf", sample_pdf_bytes, "application/pdf"))]
    )
    collection_id = up_res.json()["collection_id"]

    response = client.post(
        f"/api/documents/{collection_id}/mcqs",
        json={"num_questions": 3}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["collection_id"] == collection_id
    assert len(data["mcqs"]) > 0


def test_document_key_points(sample_pdf_bytes):
    """Tests POST /api/documents/{id}/key-points returns bulleted takeaways."""
    up_res = client.post(
        "/api/documents/upload",
        files=[("files", ("takeaways.pdf", sample_pdf_bytes, "application/pdf"))]
    )
    collection_id = up_res.json()["collection_id"]

    response = client.post(
        f"/api/documents/{collection_id}/key-points",
        json={"language": "English"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["collection_id"] == collection_id
    assert len(data["key_points"]) > 0


# --------------------------------------------------------------------
# 5. COLLECTION DELETION & ISOLATION CLEANUP
# --------------------------------------------------------------------
def test_delete_collection(sample_pdf_bytes):
    """Tests DELETE /api/documents/{id} properly purges index and memory."""
    up_res = client.post(
        "/api/documents/upload",
        files=[("files", ("delete_me.pdf", sample_pdf_bytes, "application/pdf"))]
    )
    collection_id = up_res.json()["collection_id"]

    # Verify collection exists in manager
    mgr = get_collection_manager()
    assert mgr.get_collection(collection_id) is not None

    # Delete collection
    del_res = client.delete(f"/api/documents/{collection_id}")
    assert del_res.status_code == 200
    assert del_res.json()["deleted"] is True

    # Verify collection no longer exists
    assert mgr.get_collection(collection_id) is None

    # Subsequent access should return 404
    sub_res = client.post(
        f"/api/documents/{collection_id}/summary",
        json={"language": "English"}
    )
    assert sub_res.status_code == 404


def test_delete_nonexistent_collection():
    """Tests DELETE on invalid collection returns 404."""
    response = client.delete("/api/documents/invalid_collection_999")
    assert response.status_code == 404


# --------------------------------------------------------------------
# 6. MISSING API KEY HANDLING TEST
# --------------------------------------------------------------------
def test_missing_api_key_handling(sample_pdf_bytes, monkeypatch):
    """Tests that missing GROQ_API_KEY returns a clean error without crashing."""
    up_res = client.post(
        "/api/documents/upload",
        files=[("files", ("key_test.pdf", sample_pdf_bytes, "application/pdf"))]
    )
    collection_id = up_res.json()["collection_id"]

    # Temporarily unset GROQ_API_KEY
    monkeypatch.setattr(config, "GROQ_API_KEY", "")

    response = client.post(
        "/api/chat",
        json={"collection_id": collection_id, "question": "What is AI?", "language": "English"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "GROQ_API_KEY" in data["answer"]
