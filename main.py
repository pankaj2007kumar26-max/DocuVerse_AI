"""
DocuVerse AI - Production FastAPI Backend (main.py)
===================================================
Production-ready REST API for Intelligent Document Reading & Q&A (RAG).
Reuses existing modules: pdf_reader, text_splitter, embeddings, vector_store, and api_handler.
"""

import os
import uuid
import logging
import asyncio
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import config
from pdf_reader import extract_text_from_pdf
from text_splitter import chunk_documents
from vector_store import get_collection_manager, FaissVectorStore
import api_handler

# --------------------------------------------------------------------
# 1. LOGGING & APPLICATION SETUP
# --------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("DocuVerseBackend")

app = FastAPI(
    title="DocuVerse AI Backend",
    description="Production-ready FastAPI backend for Intelligent Document Reading and Question Answering System with RAG & Groq LPU.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration (Configurable for local dev & production deployments)
raw_cors = os.getenv("CORS_ORIGINS", "*")
allowed_origins = [o.strip() for o in raw_cors.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

collection_manager = get_collection_manager()
MAX_FILE_SIZE_BYTES = int(os.getenv("MAX_FILE_SIZE_MB", "15")) * 1024 * 1024


# --------------------------------------------------------------------
# 2. PYDANTIC REQUEST & RESPONSE SCHEMAS
# --------------------------------------------------------------------
class AppInfoResponse(BaseModel):
    name: str
    version: str
    status: str
    description: str
    docs_url: str

class HealthResponse(BaseModel):
    status: str
    groq_api_configured: bool
    active_collections: int
    supported_languages: List[str]

class DocumentUploadResponse(BaseModel):
    collection_id: str
    file_names: List[str]
    total_files: int
    total_pages: int
    total_chunks: int
    message: str

class SourceReference(BaseModel):
    source: str
    page: int
    score: float
    snippet: str

class ChatRequest(BaseModel):
    collection_id: str = Field(..., description="Unique ID of the uploaded document collection")
    question: str = Field(..., min_length=1, description="Question about the document content")
    language: Optional[str] = Field(default="English", description="Target answer language: English, Hindi, or Hinglish")

class ChatResponse(BaseModel):
    collection_id: str
    question: str
    answer: str
    model_used: Optional[str] = None
    sources: List[SourceReference] = []
    success: bool

class SummaryRequest(BaseModel):
    language: Optional[str] = Field(default="English", description="Language for executive summary")

class SummaryResponse(BaseModel):
    collection_id: str
    summary: str
    model_used: Optional[str] = None
    success: bool

class MCQRequest(BaseModel):
    num_questions: Optional[int] = Field(default=4, ge=1, le=10, description="Number of practice MCQs")

class MCQResponse(BaseModel):
    collection_id: str
    mcqs: str
    model_used: Optional[str] = None
    success: bool

class KeyPointsRequest(BaseModel):
    language: Optional[str] = Field(default="English", description="Language for key points")

class KeyPointsResponse(BaseModel):
    collection_id: str
    key_points: str
    model_used: Optional[str] = None
    success: bool

class DeleteCollectionResponse(BaseModel):
    collection_id: str
    deleted: bool
    message: str


# --------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# --------------------------------------------------------------------
def _sync_process_pdfs(files_data: List[tuple]) -> tuple:
    """
    Synchronous worker for PDF reading, text chunking, and FAISS indexing.
    Executed in threadpool to prevent blocking FastAPI's async event loop.
    """
    all_pages = []
    full_text_collector = []
    file_names = []

    for name, content in files_data:
        file_names.append(name)
        pages = extract_text_from_pdf(content, file_name=name)
        all_pages.extend(pages)
        for p in pages:
            full_text_collector.append(
                f"--- Document: {name} | Page {p['metadata']['page']} ---\n" + p["text"]
            )

    if not all_pages:
        return file_names, 0, "", []

    chunks = chunk_documents(
        all_pages,
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    full_text = "\n\n".join(full_text_collector)
    return file_names, len(all_pages), full_text, chunks


# --------------------------------------------------------------------
# 4. API ENDPOINTS
# --------------------------------------------------------------------

@app.get("/", response_model=AppInfoResponse, tags=["General"])
async def root():
    """Application information and API status."""
    return AppInfoResponse(
        name="DocuVerse AI Backend",
        version="1.0.0",
        status="online",
        description="Production-ready FastAPI backend for Intelligent Document Reading and Question Answering System (RAG).",
        docs_url="/docs"
    )


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Backend health check and configuration status."""
    return HealthResponse(
        status="healthy",
        groq_api_configured=config.is_groq_api_key_valid(),
        active_collections=collection_manager.count(),
        supported_languages=config.SUPPORTED_LANGUAGES
    )


@app.post(
    "/api/documents/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Documents"]
)
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Accepts one or multiple PDF files, validates them, extracts text using PyMuPDF,
    chunks text using recursive splitting, generates embeddings into an isolated FAISS index,
    and returns a unique collection_id.
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files uploaded. Please upload at least one PDF file."
        )

    files_data = []

    for upload in files:
        filename = upload.filename or "uploaded_document.pdf"

        # 1. Validate File Extension
        if not filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type for '{filename}'. Only PDF documents (.pdf) are supported."
            )

        # 2. Read File Bytes
        content = await upload.read()
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File '{filename}' is empty."
            )

        # 3. Validate File Size
        if len(content) > MAX_FILE_SIZE_BYTES:
            max_mb = MAX_FILE_SIZE_BYTES // (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File '{filename}' exceeds the maximum allowed size of {max_mb}MB."
            )

        # 4. Validate PDF Structure
        if not content.startswith(b"%PDF"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File '{filename}' is not a valid PDF document (missing %PDF signature)."
            )

        files_data.append((filename, content))

    logger.info("Processing %d uploaded PDF file(s)...", len(files_data))

    # Run CPU-bound extraction and indexing in a threadpool to prevent event loop blocking
    file_names, total_pages, full_text, chunks = await asyncio.to_thread(_sync_process_pdfs, files_data)

    if total_pages == 0 or not chunks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract readable text from the uploaded PDF(s). Scanned image PDFs without OCR are not supported."
        )

    # Generate Unique Isolated Collection ID
    collection_id = uuid.uuid4().hex[:12]

    # Store in isolated multi-index manager
    collection = await asyncio.to_thread(
        collection_manager.create_collection,
        collection_id=collection_id,
        file_names=file_names,
        total_pages=total_pages,
        full_text=full_text,
        chunks=chunks
    )

    logger.info("Created collection '%s' with %d page(s) and %d chunk(s)", collection_id, total_pages, len(chunks))

    return DocumentUploadResponse(
        collection_id=collection_id,
        file_names=file_names,
        total_files=len(file_names),
        total_pages=total_pages,
        total_chunks=len(chunks),
        message=f"Successfully indexed {len(file_names)} file(s) into collection '{collection_id}'"
    )


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_with_documents(request: ChatRequest):
    """
    Retrieves top relevant chunks from the isolated FAISS vector index of the specified collection_id,
    and generates a strictly factual answer with source filename and page references via Groq LPU.
    """
    collection = collection_manager.get_collection(request.collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document collection '{request.collection_id}' not found. Please upload documents first."
        )

    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty."
        )

    language = request.language or "English"

    # Search isolated FAISS index in threadpool
    relevant_chunks = await asyncio.to_thread(
        collection.vector_store.search,
        query=question,
        top_k=config.TOP_K_RESULTS
    )

    # Generate Answer via Groq in threadpool
    result = await asyncio.to_thread(
        api_handler.generate_rag_answer,
        query=question,
        context_chunks=relevant_chunks,
        language=language
    )

    # Format Source Citations
    sources = [
        SourceReference(
            source=s["source"],
            page=s["page"],
            score=s["score"],
            snippet=s["snippet"]
        )
        for s in result.get("sources", [])
    ]

    return ChatResponse(
        collection_id=request.collection_id,
        question=question,
        answer=result.get("answer", "No answer generated."),
        model_used=result.get("model_used"),
        sources=sources,
        success=result.get("success", True)
    )


@app.post("/api/documents/{collection_id}/summary", response_model=SummaryResponse, tags=["Document Intelligence"])
async def get_document_summary(collection_id: str, request: SummaryRequest = SummaryRequest()):
    """Generates an executive summary of the document collection using Groq LPU."""
    collection = collection_manager.get_collection(collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document collection '{collection_id}' not found."
        )

    language = request.language or "English"
    res = await asyncio.to_thread(
        api_handler.generate_document_summary,
        full_text_sample=collection.full_text,
        language=language
    )

    return SummaryResponse(
        collection_id=collection_id,
        summary=res.get("summary", "Summary could not be generated."),
        model_used=res.get("model_used"),
        success=res.get("success", False)
    )


@app.post("/api/documents/{collection_id}/mcqs", response_model=MCQResponse, tags=["Document Intelligence"])
async def get_document_mcqs(collection_id: str, request: MCQRequest = MCQRequest()):
    """Generates practice multiple-choice questions with answer key and explanations."""
    collection = collection_manager.get_collection(collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document collection '{collection_id}' not found."
        )

    res = await asyncio.to_thread(
        api_handler.generate_document_mcqs,
        full_text_sample=collection.full_text,
        num_questions=request.num_questions
    )

    return MCQResponse(
        collection_id=collection_id,
        mcqs=res.get("mcqs", "MCQs could not be generated."),
        model_used=res.get("model_used"),
        success=res.get("success", False)
    )


@app.post("/api/documents/{collection_id}/key-points", response_model=KeyPointsResponse, tags=["Document Intelligence"])
async def get_document_key_points(collection_id: str, request: KeyPointsRequest = KeyPointsRequest()):
    """Generates core key points and takeaways from the document collection."""
    collection = collection_manager.get_collection(collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document collection '{collection_id}' not found."
        )

    language = request.language or "English"
    res = await asyncio.to_thread(
        api_handler.generate_document_key_points,
        full_text_sample=collection.full_text,
        language=language
    )

    return KeyPointsResponse(
        collection_id=collection_id,
        key_points=res.get("key_points", "Key points could not be generated."),
        model_used=res.get("model_used"),
        success=res.get("success", False)
    )


@app.delete("/api/documents/{collection_id}", response_model=DeleteCollectionResponse, tags=["Documents"])
async def delete_document_collection(collection_id: str):
    """Deletes a document collection and its isolated FAISS vector index."""
    deleted = collection_manager.delete_collection(collection_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document collection '{collection_id}' not found."
        )

    logger.info("Deleted collection '%s'", collection_id)
    return DeleteCollectionResponse(
        collection_id=collection_id,
        deleted=True,
        message=f"Collection '{collection_id}' and its FAISS index successfully deleted."
    )


@app.get("/api/documents", tags=["Documents"])
async def list_document_collections():
    """Lists all active in-memory document collections."""
    return {
        "total_collections": collection_manager.count(),
        "collections": collection_manager.list_collections()
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
