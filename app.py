"""
DocuVerse AI - Smart Hybrid Frontend (app.py)
==============================================
Zero-Config, Self-Healing Streamlit Application with Responsive Cosmic Dark Theme:
- Auto-Detects FastAPI Backend: If backend is online, uses REST API.
- Intelligent Fallback: If backend is offline or waking up, executes seamless in-memory RAG.
- Works 100% out-of-the-box on Streamlit Cloud without manual secrets configuration!
"""

import os
import requests
import streamlit as st

import config
from pdf_reader import extract_text_from_pdf
from text_splitter import chunk_documents
from vector_store import FaissVectorStore
import api_handler

# --------------------------------------------------------------------
# 1. BACKEND URL AUTO-DETECTION
# --------------------------------------------------------------------
def get_backend_url() -> str:
    """Fetches configured backend URL from env, Streamlit secrets, or defaults."""
    url = os.getenv("BACKEND_URL", "").strip()
    if not url:
        try:
            if hasattr(st, "secrets") and "BACKEND_URL" in st.secrets:
                url = str(st.secrets["BACKEND_URL"]).strip()
        except Exception:
            pass
    if not url:
        url = "http://127.0.0.1:8000"
    return url.rstrip("/")

BACKEND_URL = get_backend_url()


def is_backend_online() -> bool:
    """Quick 1-second ping to check if FastAPI backend is live."""
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=1.2)
        return r.status_code == 200
    except Exception:
        return False


# --------------------------------------------------------------------
# 2. PAGE SETUP & EXACT RESPONSIVE THEME
# --------------------------------------------------------------------
st.set_page_config(
    page_title="PDF Assistant - DocuVerse AI",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Dark Theme Core Background */
    .stApp {
        background-color: #0B0D1B !important;
        color: #F8FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Streamlit Default Header Fix (Prevent cutting off custom header) */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 2.2rem !important;
        z-index: 10 !important;
    }
    
    /* Central Responsive Container - Tight & Clean Top Spacing */
    .block-container {
        max-width: 1060px !important;
        padding-top: 2.4rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: clamp(1rem, 3vw, 2.5rem) !important;
        padding-right: clamp(1rem, 3vw, 2.5rem) !important;
        margin: 0 auto !important;
    }
    
    /* Top Bar Header */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 0px !important;
        padding: 0px 0 20px 0 !important;
    }
    .brand-title {
        font-size: clamp(1.15rem, 3vw, 1.4rem);
        font-weight: 700;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .helper-badge {
        background: rgba(139, 92, 246, 0.15);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.35);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: clamp(0.78rem, 2vw, 0.88rem);
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    
    /* Hero Title with Fluid Sizing */
    .hero-container {
        text-align: center;
        margin-bottom: 25px;
        padding: 0 5px;
    }
    .hero-title {
        font-size: clamp(1.8rem, 5vw, 2.5rem);
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        color: #A5B4FC;
        margin-bottom: 0px;
    }
    
    /* Section Cards */
    .step-card {
        background: #13162C;
        border: 1px solid #23284A;
        border-radius: 18px;
        padding: clamp(16px, 3vw, 24px);
        margin-bottom: 22px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    }
    
    /* Step Header */
    .step-header-row {
        display: flex;
        align-items: center;
        margin-bottom: 4px;
    }
    .step-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        background: #6366F1;
        color: white;
        border-radius: 50%;
        font-weight: 700;
        font-size: 0.95rem;
        margin-right: 12px;
        flex-shrink: 0;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.45);
    }
    .step-title-text {
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        font-weight: 700;
        color: #FFFFFF;
    }
    .step-subtitle-text {
        color: #94A3B8;
        font-size: clamp(0.82rem, 2vw, 0.92rem);
        margin-left: 42px;
        margin-top: -2px;
        margin-bottom: 16px;
    }
    
    /* Tips Box */
    .tips-box {
        background: rgba(30, 35, 68, 0.6);
        border: 1px solid #2E3566;
        border-radius: 14px;
        padding: 16px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .tips-header {
        color: #C084FC;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .tip-item {
        color: #CBD5E1;
        font-size: clamp(0.78rem, 2vw, 0.85rem);
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .tip-check {
        color: #10B981;
        font-weight: bold;
    }
    
    /* Status Pills */
    .status-pill-ready {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 10px 16px;
        border-radius: 10px;
        font-size: clamp(0.78rem, 2vw, 0.88rem);
        font-weight: 600;
        margin-top: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        word-break: break-word;
    }
    
    /* File Chip Preview */
    .file-chip {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
        background: #1A1E3B;
        border: 1px solid #2C3360;
        border-radius: 10px;
        padding: 10px 14px;
        margin-top: 10px;
    }
    .file-chip-left {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        word-break: break-all;
    }
    .pdf-icon-tag {
        background: #EF4444;
        color: white;
        padding: 3px 6px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 800;
    }
    
    /* Output Box */
    .output-card {
        background: #141732;
        border: 1px solid #3B4278;
        border-left: 4px solid #8B5CF6;
        border-radius: 14px;
        padding: clamp(16px, 3vw, 24px);
        margin-top: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Responsive Buttons & Inputs */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: clamp(0.85rem, 2vw, 0.95rem) !important;
        min-height: 42px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }
    
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        min-height: 44px !important;
        font-size: 16px !important;
        background: #121528 !important;
        border: 1px solid #282E57 !important;
        color: #F8FAFC !important;
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        border-radius: 10px !important;
        background: #121528 !important;
        border: 1px solid #282E57 !important;
    }

    .app-footer {
        text-align: center;
        color: #64748B;
        font-size: clamp(0.78rem, 2vw, 0.88rem);
        padding: 30px 0 10px 0;
        letter-spacing: 0.5px;
    }
    
    @media screen and (max-width: 768px) {
        .block-container {
            padding-top: 2.6rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 10px !important;
        }
        .top-bar {
            flex-direction: column !important;
            align-items: center !important;
            text-align: center !important;
        }
        .step-subtitle-text {
            margin-left: 0px !important;
        }
        .file-chip {
            flex-direction: column !important;
            align-items: flex-start !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------
# 3. SESSION STATE MANAGEMENT
# --------------------------------------------------------------------
if "collection_id" not in st.session_state:
    st.session_state.collection_id = None

if "local_vector_store" not in st.session_state:
    st.session_state.local_vector_store = FaissVectorStore()

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

if "total_pages" not in st.session_state:
    st.session_state.total_pages = 0

if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0

if "full_text" not in st.session_state:
    st.session_state.full_text = ""

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "model_used" not in st.session_state:
    st.session_state.model_used = None


# --------------------------------------------------------------------
# 4. TOP NAVIGATION BAR & HERO HEADER
# --------------------------------------------------------------------
st.markdown("""
<div class="top-bar">
    <div class="brand-title">
        <span>📑✨</span>
        <span>PDF Assistant</span>
    </div>
    <div class="helper-badge">
        ✨ Your AI Study Helper
    </div>
</div>

<div class="hero-container">
    <div class="hero-title">Upload Your PDF Document</div>
    <div class="hero-subtitle">Get instant answers from your documents with AI ✨</div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------
# 5. CARD 1: UPLOAD PDF FILE
# --------------------------------------------------------------------
st.markdown("""
<div class="step-header-row">
    <div class="step-badge">1</div>
    <div class="step-title-text">Upload PDF File</div>
</div>
<div class="step-subtitle-text">Choose one or more PDF files (Notes, Books, Resumes, Reports)</div>
""", unsafe_allow_html=True)

col_upload, col_tips = st.columns([2.4, 1.1])

with col_upload:
    uploaded_files = st.file_uploader(
        "Drag & Drop your PDF files here",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Upload PDF files up to 15MB each."
    )
    
    if uploaded_files:
        for f in uploaded_files:
            size_mb = round(f.size / (1024 * 1024), 2)
            st.markdown(f"""
            <div class="file-chip">
                <div class="file-chip-left">
                    <span class="pdf-icon-tag">PDF</span>
                    <span style="font-weight: 500; color: #E2E8F0;">{f.name}</span>
                    <span style="color: #64748B; font-size: 0.85rem;">({size_mb} MB)</span>
                </div>
                <div style="color: #10B981; font-size: 0.85rem; font-weight: 600;">
                    ✔ Ready
                </div>
            </div>
            """, unsafe_allow_html=True)

with col_tips:
    st.markdown("""
    <div class="tips-box">
        <div class="tips-header">
            <span>💡</span> Tips:
        </div>
        <div class="tip-item">
            <span class="tip-check">✔</span>
            <span>You can upload multiple files</span>
        </div>
        <div class="tip-item">
            <span class="tip-check">✔</span>
            <span>Make sure files are clear</span>
        </div>
        <div class="tip-item">
            <span class="tip-check">✔</span>
            <span>Wait for processing to finish</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Action Buttons: Process and Reset
col_proc, col_res = st.columns([3.2, 1.1])

with col_proc:
    process_btn = st.button("⚡ Process & Index Documents", type="primary", use_container_width=True)

with col_res:
    reset_btn = st.button("🔄 Reset", use_container_width=True)

# Reset Logic
if reset_btn:
    st.session_state.local_vector_store.clear()
    st.session_state.collection_id = None
    st.session_state.processed_files = []
    st.session_state.total_pages = 0
    st.session_state.total_chunks = 0
    st.session_state.full_text = ""
    st.session_state.last_answer = None
    st.session_state.last_sources = []
    st.session_state.last_query = ""
    st.session_state.model_used = None
    st.success("Documents reset successfully!")
    st.rerun()

# Processing Logic (Auto-Detect Backend vs Direct Engine)
if process_btn:
    if not uploaded_files:
        st.warning("⚠️ Kripya pehle kam se kam ek PDF file select kijiye.")
    else:
        backend_active = is_backend_online()
        processed_successfully = False
        
        # 1. Try FastAPI Backend if live
        if backend_active:
            try:
                with st.spinner("📄 Uploading and indexing via FastAPI backend..."):
                    files_payload = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded_files]
                    res = requests.post(f"{BACKEND_URL}/api/documents/upload", files=files_payload, timeout=60)
                    if res.status_code == 201:
                        data = res.json()
                        st.session_state.collection_id = data["collection_id"]
                        st.session_state.processed_files = data["file_names"]
                        st.session_state.total_pages = data["total_pages"]
                        st.session_state.total_chunks = data["total_chunks"]
                        st.session_state.last_answer = None
                        processed_successfully = True
                        st.rerun()
            except Exception:
                processed_successfully = False

        # 2. Seamless Direct Execution if backend not reachable (Zero-configuration fallback!)
        if not processed_successfully:
            with st.spinner("📄 Reading PDF pages and building FAISS semantic index..."):
                all_pages = []
                text_collector = []
                for file in uploaded_files:
                    pages = extract_text_from_pdf(file, file_name=file.name)
                    all_pages.extend(pages)
                    for p in pages:
                        text_collector.append(f"--- Document: {file.name} | Page {p['metadata']['page']} ---\n" + p["text"])

                if not all_pages:
                    st.error("Uploaded PDFs se koi readable text extract nahi ho saka.")
                else:
                    chunks = chunk_documents(all_pages, chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
                    st.session_state.local_vector_store.clear()
                    total_indexed = st.session_state.local_vector_store.add_chunks(chunks)

                    st.session_state.collection_id = "local_active"
                    st.session_state.processed_files = [f.name for f in uploaded_files]
                    st.session_state.total_pages = len(all_pages)
                    st.session_state.total_chunks = total_indexed
                    st.session_state.full_text = "\n\n".join(text_collector)
                    st.session_state.last_answer = None
                    st.rerun()

# Success Status Pill
if st.session_state.processed_files:
    file_names_str = ", ".join(st.session_state.processed_files)
    st.markdown(f"""
    <div class="status-pill-ready">
        <span style="font-size: 1.1rem; color: #10B981;">✔</span>
        <span><b>Loaded Documents:</b> {file_names_str} &nbsp;|&nbsp; <b>Pages:</b> {st.session_state.total_pages} &nbsp;|&nbsp; <b>FAISS Chunks:</b> {st.session_state.total_chunks}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# --------------------------------------------------------------------
# 6. CARD 2: ASK YOUR QUESTION
# --------------------------------------------------------------------
st.markdown("""
<div class="step-header-row">
    <div class="step-badge">2</div>
    <div class="step-title-text">Ask Your Question</div>
</div>
<div class="step-subtitle-text">Type your question here:</div>
""", unsafe_allow_html=True)

# Question Input + Get Answer Button
col_inp, col_get = st.columns([3.8, 1.2])

with col_inp:
    user_question = st.text_input(
        "Question Input",
        placeholder="💬 What is the conclusion? Or explain key concepts...",
        label_visibility="collapsed"
    )

with col_get:
    get_answer_btn = st.button("✈ Get Answer", type="primary", use_container_width=True)

# Bottom Settings & Feature Row: Responsive 2-column + 3-button layout
row2_col_left, row2_col_right = st.columns([1.6, 2.4])

with row2_col_left:
    subcol_lbl, subcol_sel = st.columns([1, 1.6])
    with subcol_lbl:
        st.markdown("<div style='margin-top: 10px; font-weight: 600; color: #CBD5E1; font-size: 0.9rem;'>Language:</div>", unsafe_allow_html=True)
    with subcol_sel:
        selected_language = st.selectbox(
            "Response Language",
            options=["English", "Hinglish (Roman)", "Hindi (हिंदी)"],
            index=0,
            label_visibility="collapsed"
        )

with row2_col_right:
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        summary_btn = st.button("📄 Summary", use_container_width=True)
    with btn_col2:
        mcq_btn = st.button("🎯 MCQs", use_container_width=True)
    with btn_col3:
        key_points_btn = st.button("⭐ Key Points", use_container_width=True)


# --------------------------------------------------------------------
# 7. ACTION HANDLERS (Auto-Detect Backend vs Direct Groq Engine)
# --------------------------------------------------------------------
if get_answer_btn:
    if not st.session_state.processed_files or st.session_state.total_chunks == 0:
        st.warning("⚠️ Kripya pehle upar Step 1 mein PDF upload aur process karein!")
    elif not user_question.strip():
        st.warning("⚠️ Kripya question box mein kuch type kijiye.")
    else:
        answered = False
        # Try backend if available and collection is backend-hosted
        if is_backend_online() and st.session_state.collection_id and st.session_state.collection_id != "local_active":
            try:
                with st.spinner("🔍 Querying FastAPI backend and generating answer..."):
                    payload = {"collection_id": st.session_state.collection_id, "question": user_question, "language": selected_language}
                    r = requests.post(f"{BACKEND_URL}/api/chat", json=payload, timeout=60)
                    if r.status_code == 200:
                        data = r.json()
                        st.session_state.last_answer = data.get("answer", "")
                        st.session_state.last_sources = data.get("sources", [])
                        st.session_state.last_query = user_question
                        st.session_state.model_used = data.get("model_used")
                        answered = True
            except Exception:
                answered = False
        
        # Fallback to direct execution
        if not answered:
            with st.spinner("🔍 Searching FAISS index and generating factual answer with Groq LPU..."):
                relevant_chunks = st.session_state.local_vector_store.search(
                    query=user_question,
                    top_k=config.TOP_K_RESULTS
                )
                res = api_handler.generate_rag_answer(
                    query=user_question,
                    context_chunks=relevant_chunks,
                    language=selected_language
                )
                st.session_state.last_answer = res.get("answer", "No answer generated.")
                st.session_state.last_sources = res.get("sources", [])
                st.session_state.last_query = user_question
                st.session_state.model_used = res.get("model_used")

if summary_btn:
    if not st.session_state.processed_files:
        st.warning("⚠️ Pehle PDF upload aur process kijiye.")
    else:
        with st.spinner("📝 Generating Executive Summary with Groq..."):
            res = api_handler.generate_document_summary(st.session_state.full_text, language=selected_language)
            st.session_state.last_answer = res.get("summary", "Summary could not be generated.")
            st.session_state.last_sources = []
            st.session_state.last_query = "Document Executive Summary"
            st.session_state.model_used = res.get("model_used")

if mcq_btn:
    if not st.session_state.processed_files:
        st.warning("⚠️ Pehle PDF upload aur process kijiye.")
    else:
        with st.spinner("🎯 Generating Practice MCQs with Groq..."):
            res = api_handler.generate_document_mcqs(st.session_state.full_text, num_questions=4)
            st.session_state.last_answer = res.get("mcqs", "MCQs could not be generated.")
            st.session_state.last_sources = []
            st.session_state.last_query = "Document Practice MCQs"
            st.session_state.model_used = res.get("model_used")

if key_points_btn:
    if not st.session_state.processed_files:
        st.warning("⚠️ Pehle PDF upload aur process kijiye.")
    else:
        with st.spinner("⭐ Extracting Key Points with Groq..."):
            res = api_handler.generate_document_key_points(st.session_state.full_text, language=selected_language)
            st.session_state.last_answer = res.get("key_points", "Key points could not be generated.")
            st.session_state.last_sources = []
            st.session_state.last_query = "Key Points & Main Takeaways"
            st.session_state.model_used = res.get("model_used")


# --------------------------------------------------------------------
# 8. CARD 3: OUTPUT AREA (Adaptive Result Display)
# --------------------------------------------------------------------
if st.session_state.last_answer:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💡 Step 3: Output Area")
    
    st.markdown(f"""
    <div class="output-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
            <div style="font-size: clamp(1rem, 2.5vw, 1.2rem); font-weight: 700; color: #FFFFFF;">
                🎯 Result for: <i>"{st.session_state.last_query}"</i>
            </div>
            <div style="background: rgba(99, 102, 241, 0.2); color: #A5B4FC; padding: 4px 12px; border-radius: 999px; font-size: 0.8rem; font-weight: 600;">
                ⚡ {st.session_state.model_used or 'Groq LPU'}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(st.session_state.last_answer)
    st.markdown("</div>", unsafe_allow_html=True)

    # Adaptive Source References & Citations
    if st.session_state.last_sources:
        st.write("")
        st.markdown("##### 📌 Source References & Citations:")
        for idx, src in enumerate(st.session_state.last_sources, 1):
            with st.expander(f"Reference #{idx}: 📄 {src['source']} (Page {src['page']}) - Relevance: {src['score']}"):
                st.markdown(f"> *\"{src['snippet']}\"*")


# --------------------------------------------------------------------
# 9. FOOTER
# --------------------------------------------------------------------
st.markdown("""
<div class="app-footer">
    ✨ Study Smarter • Learn Better • Achieve More &nbsp;|&nbsp; Powered by Groq LPU
</div>
""", unsafe_allow_html=True)
