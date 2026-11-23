"""
DocuVerse AI - Project Environment Check (test_stage1.py)
---------------------------------------------------------
Run: python test_stage1.py
"""

import sys
from pathlib import Path

def test_project():
    print("\n" + "=" * 60)
    print("🚀 DocuVerse AI - System Environment Check")
    print("=" * 60)

    # 1. Check Python Version
    py_version = sys.version_info
    print(f"\n[1] Python Version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version.major == 3 and py_version.minor >= 9:
        print("    ✅ Python version is compatible (>= 3.9)")
    else:
        print("    ⚠️ Recommended Python version is 3.10 or 3.11")

    # 2. Check Core Project Files
    print("\n[2] Checking Essential Project Files:")
    essential_files = [
        "config.py",
        "pdf_reader.py",
        "text_splitter.py",
        "embeddings.py",
        "vector_store.py",
        "api_handler.py",
        "app.py",
        "requirements.txt",
        ".gitignore"
    ]
    for filename in essential_files:
        if Path(filename).exists():
            print(f"    ✅ {filename} found.")
        else:
            print(f"    ❌ {filename} NOT found.")

    # 3. Check .env File
    print("\n[3] Checking Environment Configuration:")
    env_file = Path(".env")
    if env_file.exists():
        print("    ✅ .env file found.")
    else:
        print("    ℹ️  .env file not yet created. (Copy .env.example to .env and add your Gemini API Key)")

    # 4. Check Config Import
    print("\n[4] Testing config.py Import:")
    try:
        import config
        print("    ✅ config.py successfully imported!")
        print(f"       - Gemini Model: {config.GEMINI_MODEL_NAME}")
        print(f"       - Embedding Model: {config.EMBEDDING_MODEL_NAME}")
        print(f"       - Chunk Size: {config.CHUNK_SIZE}")
        print(f"       - Overlap: {config.CHUNK_OVERLAP}")
        if config.is_api_key_valid():
            print("       - Gemini API Key: ✅ Configured")
        else:
            print("       - Gemini API Key: ⚠️ Missing or Default (Add to .env)")
    except Exception as e:
        print(f"    ❌ Error importing config.py: {e}")

    # 5. Check Installed Libraries
    print("\n[5] Checking Installed Libraries:")
    packages = [
        ("streamlit", "Streamlit (UI)"),
        ("pymupdf", "PyMuPDF (PDF Parser)"),
        ("faiss", "FAISS (Vector Store)"),
        ("google.genai", "Google GenAI (Gemini SDK)"),
        ("dotenv", "python-dotenv (Environment Manager)")
    ]

    for mod_name, label in packages:
        try:
            __import__(mod_name)
            print(f"    ✅ {label} is installed.")
        except ImportError:
            print(f"    ❌ {label} not found.")

    print("\n" + "=" * 60)
    print("🎉 DocuVerse AI is ready to run with Streamlit!")
    print("Command: streamlit run app.py")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    test_project()
