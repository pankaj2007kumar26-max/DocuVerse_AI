"""
DocuVerse AI - Central Configuration Module (config.py)
-------------------------------------------------------
Yeh file hamare pure project ka "Control Center" hai.
Yaha hum saari settings, API keys, Model names aur Hyperparameters define karte hain
taaki code mein kahi bhi hardcoding na karni pade.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Project Root Directory path
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
# override=True ensures fresh values are picked if .env is edited
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

# ----------------------------------------------------
# 1. API KEYS & SECURITY
# ----------------------------------------------------
# Groq API Key (Local .env or Streamlit Cloud Secrets)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

# Google Gemini API Key (Fallback)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Streamlit Cloud deployment support (Reads from Streamlit Secrets securely)
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        if not GROQ_API_KEY and "GROQ_API_KEY" in st.secrets:
            GROQ_API_KEY = str(st.secrets["GROQ_API_KEY"]).strip()
        if not GEMINI_API_KEY and "GEMINI_API_KEY" in st.secrets:
            GEMINI_API_KEY = str(st.secrets["GEMINI_API_KEY"]).strip()
except Exception:
    pass

def is_groq_api_key_valid() -> bool:
    """Check karta hai ki Groq API key set hai ya nahi."""
    return bool(GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_"))

def is_api_key_valid() -> bool:
    """Check karta hai ki Groq ya Gemini me se koi bhi valid key available hai."""
    if is_groq_api_key_valid():
        return True
    if GEMINI_API_KEY and GEMINI_API_KEY != "your_actual_gemini_api_key_here":
        return True
    return False

# ----------------------------------------------------
# 2. AI MODEL CONFIGURATIONS
# ----------------------------------------------------
# Groq Models (Active & Verified on Groq Cloud)
# Primary: qwen/qwen3.8-27b (Fast, multilingual, SOTA quality)
GROQ_MODEL_NAME = "qwen/qwen3.8-27b"
GROQ_FALLBACK_MODELS = [
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "allam-2-7b"
]

# Gemini Fallback Models
GEMINI_MODEL_NAME = "gemini-1.5-flash"
GEMINI_FALLBACK_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-2.0-flash",
    "gemini-1.5-pro"
]

# Sentence Transformers: Free local embeddings, runs smoothly on CPU
# 384-dimensional vector representation
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Gemini Generation Parameters
# Temperature 0.3 rakha hai taaki AI facts par stick rahe aur hallucinate na kare
GEMINI_GENERATION_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.85,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# ----------------------------------------------------
# 3. TEXT CHUNKING (SPLITTING) CONFIGURATION
# ----------------------------------------------------
# Ek chunk mein kitne characters honge
CHUNK_SIZE = 1000

# Do lagatar chunks ke beech kitne characters repeat honge (context continuity ke liye)
CHUNK_OVERLAP = 200

# ----------------------------------------------------
# 4. VECTOR STORE & RETRIEVAL CONFIGURATION
# ----------------------------------------------------
# FAISS index se question ke liye top kitne relevant chunks retrieve karne hain
TOP_K_RESULTS = 4

# ----------------------------------------------------
# 5. UI & LANGUAGE SETTINGS
# ----------------------------------------------------
APP_TITLE = "DocuVerse AI"
APP_SUBTITLE = "Intelligent Document Reading & Question Answering System"

SUPPORTED_LANGUAGES = [
    "English",
    "Hinglish (Hindi in Roman script)",
    "Hindi (हिंदी)"
]

DEFAULT_LANGUAGE = "English"

def print_config_summary():
    """Debug helper: Current config status print karta hai."""
    print("=" * 50)
    print("DocuVerse AI - Configuration Status")
    print("=" * 50)
    print(f"Base Directory       : {BASE_DIR}")
    print(f"Gemini Model         : {GEMINI_MODEL_NAME}")
    print(f"Embedding Model      : {EMBEDDING_MODEL_NAME}")
    print(f"Chunk Size / Overlap : {CHUNK_SIZE} / {CHUNK_OVERLAP}")
    print(f"Top K Chunks         : {TOP_K_RESULTS}")
    print(f"API Key Configured?  : {'YES [Valid]' if is_api_key_valid() else 'NO [Missing or Default]'}")
    print("=" * 50)

if __name__ == "__main__":
    print_config_summary()
