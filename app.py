"""
DocuVerse AI - PDF Assistant
"""

import importlib
import os

import streamlit as st

import config
importlib.reload(config)

from pdf_reader import extract_text_from_pdf
from text_splitter import chunk_documents
from vector_store import FaissVectorStore
import api_handler
importlib.reload(api_handler)


st.set_page_config(
    page_title="DocuVerse AI",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
:root {
    --page: #090b20;
    --panel: #171a35;
    --panel-2: #202449;
    --panel-3: #11152f;
    --border: #303760;
    --text: #f7f8ff;
    --muted: #aab1d5;
    --purple: #7957ee;
    --purple-2: #9c55ff;
}

.stApp {
    background:
        radial-gradient(circle at 78% 12%, rgba(109, 63, 196, .10), transparent 22rem),
        radial-gradient(circle at 18% 100%, rgba(67, 91, 212, .10), transparent 25rem),
        var(--page) !important;
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}
[data-testid="stToolbar"] { visibility: hidden; }
[data-testid="stSidebar"] {
    background: #11142d;
    border-right: 1px solid #242a50;
    width: 148px !important;
}
[data-testid="stSidebarContent"] {
    width: 148px !important;
    padding: 0 14px 18px 14px;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.35rem;
}
[data-testid="stMainBlockContainer"] {
    max-width: 1120px;
    padding: 16px 26px 28px 24px;
}

.sidebar-logo {
    height: 84px;
    display: flex;
    align-items: center;
    color: white;
    font-size: 21px;
}
.sidebar-logo span {
    color: #9a78f4;
}
[data-testid="stSidebar"] .stButton > button {
    height: 46px;
    justify-content: flex-start;
    border: 0;
    border-radius: 11px;
    background: transparent;
    color: #9ba3c9;
    font-size: 13px;
    text-align: left;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #1d2348;
    color: white;
}
[data-testid="stSidebar"] .nav-active > button,
[data-testid="stSidebar"] .nav-active button {
    background: linear-gradient(90deg, #4d4ec0, #5a2b9b) !important;
    color: white !important;
}

.card {
    background: rgba(23, 26, 53, .96);
    border: 1px solid #30365f;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 12px 30px rgba(3, 5, 24, .18);
}
.step-title {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 3px;
}
.step-number {
    width: 38px;
    height: 38px;
    flex: 0 0 38px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    background: linear-gradient(145deg, #714cff, #8f55ed);
    color: white;
    font-weight: 800;
    box-shadow: 0 0 18px rgba(124, 92, 255, .35);
}
.step-name {
    font-size: 16px;
    font-weight: 750;
}
.step-copy {
    margin-left: 49px;
    margin-bottom: 12px;
    color: #9fa6cc;
    font-size: 12px;
}

[data-testid="stFileUploader"] {
    border: 1px dashed #5964bc;
    border-radius: 13px;
    background: #14183a;
    padding: 8px;
}
[data-testid="stFileUploader"] section {
    background: transparent;
    border: 0;
}
[data-testid="stFileUploaderDropzone"] {
    min-height: 178px;
}
[data-testid="stFileUploaderDropzone"] small { color: #8f97bd; }

.file-chip, .success-chip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 49px;
    margin-top: 10px;
    padding: 8px 12px;
    border-radius: 10px;
    background: #202546;
    border: 1px solid #30375e;
    font-size: 12px;
}
.pdf-tag {
    display: inline-grid;
    width: 34px;
    height: 38px;
    place-items: center;
    border-radius: 7px;
    background: #ed5264;
    color: white;
    font-size: 10px;
    font-weight: 800;
}
.file-info { display: flex; align-items: center; gap: 10px; }
.uploaded { color: #59d38c; }

div.stButton > button {
    min-height: 42px;
    border-radius: 10px;
    border: 1px solid #3a4277;
    font-weight: 650;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #6960ed, #7c35db);
    border: 0;
    color: white;
}

.question-box [data-testid="stTextInput"] input {
    min-height: 55px;
    background: #11142e;
    border: 1px solid #30375f;
    border-radius: 12px;
    color: white;
}

.language-row [data-testid="stSelectbox"] {
    max-width: 150px;
}

.response-card {
    min-height: 150px;
    margin-top: 16px;
    background: #171a35;
    border: 1px solid #303760;
    border-radius: 16px;
    padding: 16px;
}
.response-title {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #9f73ff;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 12px;
}
.response-empty {
    min-height: 82px;
    display: grid;
    place-items: center;
    border: 1px solid #30375f;
    border-radius: 10px;
    background: #11142c;
    color: #8c94b5;
    font-size: 12px;
}

.feature-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-top: 18px;
}
.feature {
    text-align: center;
    color: #bdc4df;
    font-size: 11px;
    line-height: 1.25;
}
.feature-icon {
    height: 42px;
    display: grid;
    place-items: center;
    font-size: 24px;
}

.app-footer {
    text-align: center;
    color: #7f87aa;
    font-size: 11px;
    padding: 18px 0 4px;
}

@media (max-width: 900px) {
    [data-testid="stSidebar"] {
        width: 72px !important;
    }
    [data-testid="stSidebarContent"] {
        width: 72px !important;
    }
    [data-testid="stMainBlockContainer"] {
        padding-left: 12px;
        padding-right: 12px;
    }
    .feature-row { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stMainBlockContainer"] { padding: 8px; }
    .card { padding: 14px 12px; }
    .step-copy { margin-left: 49px; }
}
</style>
""", unsafe_allow_html=True)


# Session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = FaissVectorStore()
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


# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-logo">DocuVerse <span>&nbsp;AI</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-active">', unsafe_allow_html=True)
    st.button("⌂  Home", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.button("▣  My Documents", use_container_width=True)
    st.button("◷  History", use_container_width=True)
    st.button("ⓘ  About", use_container_width=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#9a78f4;font-size:13px;text-align:center;'>Study Smarter<br>with AI ✦</div>",
        unsafe_allow_html=True,
    )


left, right = st.columns([1, 1], gap="medium")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-title"><div class="step-number">1</div><div class="step-name">Upload Your PDF Document</div></div>
    <div class="step-copy">Drag & drop or choose a file to get started</div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "PDF uploader",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Upload PDF files up to 10MB each.",
    )

    if uploaded_files:
        for f in uploaded_files:
            size_mb = round(f.size / (1024 * 1024), 2)
            st.markdown(
                f'<div class="file-chip"><div class="file-info"><span class="pdf-tag">PDF</span>'
                f'<span>{f.name}<br><small style="color:#8e96b8">{size_mb} MB</small></span></div>'
                f'<span class="uploaded">✓ Uploaded</span></div>',
                unsafe_allow_html=True,
            )

    proc_col, reset_col = st.columns([2.4, 1])
    with proc_col:
        process_btn = st.button("⚙  Process & Index Document", type="primary", width="stretch")
    with reset_col:
        reset_btn = st.button("↻  Reset", width="stretch")

    if reset_btn:
        st.session_state.vector_store.clear()
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

    if process_btn:
        if not uploaded_files:
            st.warning("Please select at least one PDF file.")
        else:
            with st.spinner("Reading PDF pages and building the semantic index..."):
                all_pages = []
                text_collector = []
                for file in uploaded_files:
                    pages = extract_text_from_pdf(file, file_name=file.name)
                    all_pages.extend(pages)
                    for p in pages:
                        text_collector.append(
                            f"--- Document: {file.name} | Page {p['metadata']['page']} ---\n" + p["text"]
                        )

                if not all_pages:
                    st.error("No readable text could be extracted from the uploaded PDFs.")
                else:
                    chunks = chunk_documents(
                        all_pages,
                        chunk_size=config.CHUNK_SIZE,
                        chunk_overlap=config.CHUNK_OVERLAP,
                    )
                    st.session_state.vector_store.clear()
                    total_indexed = st.session_state.vector_store.add_chunks(chunks)
                    st.session_state.processed_files = [f.name for f in uploaded_files]
                    st.session_state.total_pages = len(all_pages)
                    st.session_state.total_chunks = total_indexed
                    st.session_state.full_text = "\n\n".join(text_collector)
                    st.session_state.last_answer = None
                    st.rerun()

    if st.session_state.processed_files:
        names = ", ".join(st.session_state.processed_files)
        st.markdown(
            f'<div class="success-chip"><span>✓ &nbsp; Document processed successfully. You can now ask questions.</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("""
    <div class="feature-row">
        <div class="feature"><div class="feature-icon">⚡</div>Fast<br>& Accurate</div>
        <div class="feature"><div class="feature-icon">🛡️</div>Secure<br>& Private</div>
        <div class="feature"><div class="feature-icon">🧠</div>RAG Powered</div>
        <div class="feature"><div class="feature-icon">◆</div>Smart<br>Summarization</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-title"><div class="step-number">2</div><div class="step-name">Ask Your Question</div></div>
    <div class="step-copy">Type your query below</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    input_col, answer_col = st.columns([4, 1.15], vertical_alignment="bottom")
    with input_col:
        user_question = st.text_input(
            "Question",
            placeholder="Enter your question here...",
            label_visibility="collapsed",
        )
    with answer_col:
        get_answer_btn = st.button("➤  Get Answer", type="primary", width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

    language_col, action_col = st.columns([1.3, 3], vertical_alignment="bottom")
    with language_col:
        selected_language = st.selectbox(
            "Language",
            options=["English", "Hinglish (Roman)", "Hindi (हिंदी)"],
            index=0,
        )
    with action_col:
        summary_col, mcq_col, key_col = st.columns(3)
        with summary_col:
            summary_btn = st.button("Summary", width="stretch")
        with mcq_col:
            mcq_btn = st.button("MCQs", width="stretch")
        with key_col:
            key_points_btn = st.button("Key Points", width="stretch")


    if get_answer_btn:
        if not st.session_state.processed_files or st.session_state.total_chunks == 0:
            st.warning("Please upload and process a PDF in step 1.")
        elif not user_question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching the document and generating an answer..."):
                relevant_chunks = st.session_state.vector_store.search(
                    query=user_question,
                    top_k=config.TOP_K_RESULTS,
                )
                res = api_handler.generate_rag_answer(
                    query=user_question,
                    context_chunks=relevant_chunks,
                    language=selected_language,
                )
                st.session_state.last_answer = res.get("answer", "No answer generated.")
                st.session_state.last_sources = res.get("sources", [])
                st.session_state.last_query = user_question
                st.session_state.model_used = res.get("model_used")

    if summary_btn:
        if not st.session_state.full_text:
            st.warning("Please upload and process a PDF first.")
        else:
            with st.spinner("Generating executive summary..."):
                res = api_handler.generate_document_summary(
                    st.session_state.full_text,
                    language=selected_language,
                )
                st.session_state.last_answer = res.get("summary", "Summary could not be generated.")
                st.session_state.last_sources = []
                st.session_state.last_query = "Document Executive Summary"
                st.session_state.model_used = res.get("model_used")

    if mcq_btn:
        if not st.session_state.full_text:
            st.warning("Please upload and process a PDF first.")
        else:
            with st.spinner("Generating practice MCQs..."):
                res = api_handler.generate_document_mcqs(
                    st.session_state.full_text,
                    num_questions=4,
                )
                st.session_state.last_answer = res.get("mcqs", "MCQs could not be generated.")
                st.session_state.last_sources = []
                st.session_state.last_query = "Document Practice MCQs"
                st.session_state.model_used = res.get("model_used")

    if key_points_btn:
        if not st.session_state.full_text:
            st.warning("Please upload and process a PDF first.")
        else:
            with st.spinner("Extracting key points..."):
                res = api_handler.generate_document_key_points(
                    st.session_state.full_text,
                    language=selected_language,
                )
                st.session_state.last_answer = res.get(
                    "key_points",
                    "Key points could not be generated.",
                )
                st.session_state.last_sources = []
                st.session_state.last_query = "Key Points & Main Takeaways"
                st.session_state.model_used = res.get("model_used")

    st.markdown('<div class="response-card"><div class="response-title">✦ &nbsp; AI Response</div>', unsafe_allow_html=True)
    if st.session_state.last_answer:
        st.markdown(f"**Result for: *{st.session_state.last_query}***")
        st.markdown(st.session_state.last_answer)
        if st.session_state.last_sources:
            st.markdown("##### Source references")
            for idx, src in enumerate(st.session_state.last_sources, 1):
                with st.expander(
                    f"Reference #{idx}: {src['source']} (Page {src['page']})"
                ):
                    st.markdown(f'> *"{src["snippet"]}"*')
    else:
        st.markdown(
            '<div class="response-empty">Your answer will appear here...</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    '<div class="app-footer">DocuVerse AI  •  Turn Your Documents into Knowledge</div>',
    unsafe_allow_html=True,
)
