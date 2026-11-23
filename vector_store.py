"""
DocuVerse AI - FAISS Vector Store Module (vector_store.py)
---------------------------------------------------------
Yeh module Facebook AI Similarity Search (FAISS) use karke
embeddings ko memory ya disk par index karta hai aur user ke query se
top-K sabse relevant document chunks ko retrieve karta hai.
"""

from typing import List, Dict, Any, Tuple
import os
import pickle
import numpy as np
import faiss
import config
from embeddings import get_embedding_model

class FaissVectorStore:
    """
    FAISS index aur corresponding document chunk metadata ko manage karne wali class.
    IndexFlatIP (Inner Product) use karta hai jo normalized vectors par
    exact Cosine Similarity deta hai.
    """
    def __init__(self, dimension: int = None):
        self.embedder = get_embedding_model()
        self.dimension = dimension or self.embedder.dimension
        
        # IndexFlatIP = Cosine similarity for unit-normalized vectors
        self.index = faiss.IndexFlatIP(self.dimension)
        # Chunks lookup list: index position -> chunk dict
        self.chunks: List[Dict[str, Any]] = []

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """
        Text chunks ke embeddings banakar FAISS index mein add karta hai.
        
        Returns:
            Total chunks currently indexed.
        """
        if not chunks:
            print("[Vector Store] Warning: Empty chunks list provided.")
            return len(self.chunks)
            
        print(f"[Vector Store] Generating embeddings for {len(chunks)} chunks...")
        texts = [c["chunk_text"] for c in chunks]
        vectors = self.embedder.embed_texts(texts)
        
        # Ensure vectors are float32 and 2D
        vectors = np.ascontiguousarray(vectors, dtype=np.float32)
        
        # FAISS index mein add karte hain
        self.index.add(vectors)
        self.chunks.extend(chunks)
        
        print(f"[Vector Store] Successfully indexed {len(chunks)} chunks. Total in store: {self.index.ntotal}")
        return self.index.ntotal

    def search(self, query: str, top_k: int = config.TOP_K_RESULTS) -> List[Dict[str, Any]]:
        """
        User ke question ke basis par top-K sabse relevant chunks search karta hai.
        
        Returns:
            List of chunks with similarity scores:
            [
                {
                    "chunk_text": "...",
                    "metadata": {"source": "ai.pdf", "page": 2, "chunk_id": 3},
                    "score": 0.892
                }, ...
            ]
        """
        if self.index.ntotal == 0 or not query.strip():
            return []
            
        # Limit top_k to total available chunks
        k = min(top_k, self.index.ntotal)
        
        # Query ka embedding vector
        query_vector = self.embedder.embed_query(query)
        query_vector = np.ascontiguousarray([query_vector], dtype=np.float32)
        
        # FAISS search execute karte hain
        scores, indices = self.index.search(query_vector, k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx < len(self.chunks):
                matched_chunk = dict(self.chunks[idx])
                matched_chunk["score"] = float(score)
                results.append(matched_chunk)
                
        return results

    def clear(self):
        """Index aur chunks ko reset karta hai."""
        self.index.reset()
        self.chunks = []
        print("[Vector Store] Vector store cleared.")

    def save_to_disk(self, directory: str = "faiss_index"):
        """Index aur metadata ko disk par save karta hai."""
        os.makedirs(directory, exist_ok=True)
        faiss.write_index(self.index, os.path.join(directory, "index.faiss"))
        with open(os.path.join(directory, "chunks.pkl"), "wb") as f:
            pickle.dump(self.chunks, f)
        print(f"[Vector Store] Saved FAISS index and chunks to '{directory}'")

    def load_from_disk(self, directory: str = "faiss_index") -> bool:
        """Disk se pehle se saved FAISS index aur chunks load karta hai."""
        index_path = os.path.join(directory, "index.faiss")
        chunks_path = os.path.join(directory, "chunks.pkl")
        
        if os.path.exists(index_path) and os.path.exists(chunks_path):
            self.index = faiss.read_index(index_path)
            with open(chunks_path, "rb") as f:
                self.chunks = pickle.load(f)
            print(f"[Vector Store] Loaded {self.index.ntotal} chunks from '{directory}'")
            return True
        return False


if __name__ == "__main__":
    print("Testing vector_store.py...")
    store = FaissVectorStore()
    
    test_chunks = [
        {"chunk_text": "Machine Learning algorithms build a model based on sample data.", "metadata": {"source": "ml.pdf", "page": 1, "chunk_id": 0}},
        {"chunk_text": "Deep Learning utilizes artificial neural networks with multiple layers.", "metadata": {"source": "dl.pdf", "page": 5, "chunk_id": 1}},
        {"chunk_text": "Database normalization reduces data redundancy in SQL tables.", "metadata": {"source": "dbms.pdf", "page": 12, "chunk_id": 2}}
    ]
    
    store.add_chunks(test_chunks)
    query = "Explain neural networks and deep learning"
    results = store.search(query, top_k=2)
    
    print(f"\nQuery: '{query}'")
    print(f"Top results returned: {len(results)}")
    for r in results:
        print(f" - [{r['metadata']['source']} | Page {r['metadata']['page']}] Score: {r['score']:.4f}")
        print(f"   Text: {r['chunk_text']}")
        
    assert results[0]["metadata"]["source"] == "dl.pdf", "Search check failed! DL chunk should be rank 1."
    print("vector_store.py test PASSED! ✅")
