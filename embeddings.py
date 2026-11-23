"""
DocuVerse AI - Embeddings Engine (embeddings.py)
-----------------------------------------------
Yeh module text chunks aur user ke questions ko high-dimensional
mathematical vectors (numerical representations) mein convert karta hai.

Supports:
1. Sentence Transformers ('all-MiniLM-L6-v2') - Local & Free (When available)
2. Google Gemini Embeddings ('text-embedding-004') - Cloud
3. Lightweight Fast Vectorizer - Zero-dependency fallback
"""

import hashlib
import re
from typing import List, Union
import numpy as np
import config

import socket

def _is_network_available() -> bool:
    try:
        socket.setdefaulttimeout(0.5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("8.8.8.8", 53))
        s.close()
        return True
    except Exception:
        return False

# Try importing Sentence Transformers
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

# Try importing Google GenAI
try:
    from google import genai
    HAS_GOOGLE_GENAI = True
except ImportError:
    HAS_GOOGLE_GENAI = False


class EmbeddingsManager:
    """
    Text ko numerical vectors (embeddings) mein convert karne ka manager class.
    FAISS ke sath 100% compatible float32 numpy arrays return karta hai.
    """
    def __init__(self, model_name: str = config.EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        self.backend = None
        self.model = None
        self.dimension = 384
        self._initialize_backend()

    def _initialize_backend(self):
        # Priority 1: Sentence Transformers (Requested in requirements)
        if HAS_SENTENCE_TRANSFORMERS:
            try:
                # If network is available or model cached
                if _is_network_available():
                    self.model = SentenceTransformer(self.model_name)
                else:
                    self.model = SentenceTransformer(self.model_name, local_files_only=True)
                self.dimension = self.model.get_sentence_embedding_dimension()
                self.backend = "sentence_transformers"
                print(f"[Embeddings] SentenceTransformer ready! Vector Dimension: {self.dimension}")
                return
            except Exception as e:
                print(f"[Embeddings] SentenceTransformer not available locally: {e}. Falling back...")

        # Priority 2: Google GenAI Embeddings (text-embedding-004)
        if HAS_GOOGLE_GENAI and config.is_api_key_valid():
            try:
                print("[Embeddings] Initializing Google Gemini Embeddings (text-embedding-004)...")
                self.client = genai.Client(api_key=config.GEMINI_API_KEY)
                self.dimension = 768
                self.backend = "google_genai"
                print(f"[Embeddings] Google Gemini Embeddings ready! Vector Dimension: {self.dimension}")
                return
            except Exception as e:
                print(f"[Embeddings] Google GenAI Embeddings failed: {e}. Falling back...")

        # Priority 3: Built-in Robust Semantic N-Gram Vectorizer (Guarantees zero-crash)
        print("[Embeddings] Using Built-in Lightweight Semantic Vectorizer (CPU Optimized)...")
        self.dimension = 384
        self.backend = "fallback"

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        List of texts ko (N, dimension) float32 numpy array mein convert karta hai.
        Vectors are L2-normalized taaki dot product = cosine similarity ho.
        """
        if not texts:
            return np.empty((0, self.dimension), dtype=np.float32)

        # 1. Sentence Transformers
        if self.backend == "sentence_transformers":
            vectors = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
            return vectors.astype(np.float32)

        # 2. Google GenAI
        elif self.backend == "google_genai":
            try:
                vectors = []
                for t in texts:
                    res = self.client.models.embed_content(
                        model="text-embedding-004",
                        contents=t
                    )
                    vectors.append(res.embedding.values)
                arr = np.array(vectors, dtype=np.float32)
                # L2 Normalize
                norms = np.linalg.norm(arr, axis=1, keepdims=True)
                norms[norms == 0] = 1e-9
                return arr / norms
            except Exception as e:
                print(f"[Embeddings] Cloud embedding error: {e}. Using fallback...")

        # 3. Fallback: Semantic Token Hash Projection
        return self._fallback_embed(texts)

    def embed_query(self, query: str) -> np.ndarray:
        """Single search query ke liye 1D vector (dimension,) return karta hai."""
        vecs = self.embed_texts([query])
        if len(vecs) > 0:
            return vecs[0]
        return np.zeros(self.dimension, dtype=np.float32)

    def _fallback_embed(self, texts: List[str]) -> np.ndarray:
        """
        Deterministic, stop-word filtered semantic token projection.
        Words aur 3-grams ko hashing ke zariye 384 dimensions par project karta hai.
        """
        n_samples = len(texts)
        matrix = np.zeros((n_samples, self.dimension), dtype=np.float32)
        stop_words = {"a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "is", "are", "with", "this", "that"}
        
        for i, text in enumerate(texts):
            words = [w for w in re.findall(r"\b[a-zA-Z0-9]{2,}\b", text.lower()) if w not in stop_words]
            if not words:
                continue
            
            for idx, word in enumerate(words):
                h1 = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16) % self.dimension
                matrix[i, h1] += 2.0
                # Character trigrams for morphological similarity
                for k in range(len(word) - 2):
                    sub = word[k:k+3]
                    h_sub = int(hashlib.sha1(sub.encode("utf-8")).hexdigest(), 16) % self.dimension
                    matrix[i, h_sub] += 0.5

            # L2 Normalization
            norm = np.linalg.norm(matrix[i])
            if norm > 0:
                matrix[i] = matrix[i] / norm
                
        return matrix


# Global Singleton Instance for fast reuse across modules
_embedding_instance = None

def get_embedding_model() -> EmbeddingsManager:
    """Returns singleton instance of EmbeddingsManager."""
    global _embedding_instance
    if _embedding_instance is None:
        _embedding_instance = EmbeddingsManager()
    return _embedding_instance


if __name__ == "__main__":
    print("Testing embeddings.py...")
    embedder = get_embedding_model()
    test_texts = [
        "Artificial intelligence and deep learning in computer science.",
        "Machine learning algorithms identify patterns in large datasets.",
        "A delicious recipe for chocolate chip cookies."
    ]
    vectors = embedder.embed_texts(test_texts)
    print(f"Generated vectors shape: {vectors.shape} (Expected: {len(test_texts)}, {embedder.dimension})")
    
    # Check similarity between AI texts vs cookie recipe
    sim_ai_ml = np.dot(vectors[0], vectors[1])
    sim_ai_food = np.dot(vectors[0], vectors[2])
    print(f"Similarity (AI vs Machine Learning): {sim_ai_ml:.4f}")
    print(f"Similarity (AI vs Cookie Recipe):    {sim_ai_food:.4f}")
    assert sim_ai_ml > sim_ai_food, "Semantic check: AI and ML should be closer than AI and cookies!"
    print("embeddings.py test PASSED! ✅")
