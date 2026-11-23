"""
DocuVerse AI - Text Splitter Module (text_splitter.py)
------------------------------------------------------
Yeh module extracted pages ke text ko smaller, semantically coherent chunks
mein break karta hai with overlap taaki sentence context break na ho.
Har chunk ke sath source file name, page number aur chunk_id attach hota hai.
"""

from typing import List, Dict, Any
import config

def split_text_recursive(text: str, chunk_size: int = config.CHUNK_SIZE, chunk_overlap: int = config.CHUNK_OVERLAP) -> List[str]:
    """
    Ek string ko smart separator hierarchy (\n\n -> \n -> . -> space) ke sath
    overlapping chunks mein divide karta hai. Words ko beech se cut nahi hone deta.
    """
    if not text or not text.strip():
        return []
        
    text = text.strip()
    
    # Agar text pehle se chunk_size se chota hai, direct return karo
    if len(text) <= chunk_size:
        return [text]
        
    separators = ["\n\n", "\n", ". ", "? ", "! ", " ", ""]
    
    def _split_with_separators(text_to_split: str, sep_index: int) -> List[str]:
        if sep_index >= len(separators):
            # Fallback: Hard character slice agar koi separator na mile
            return [text_to_split[i:i + chunk_size] for i in range(0, len(text_to_split), chunk_size - chunk_overlap)]
            
        separator = separators[sep_index]
        if separator == "":
            parts = list(text_to_split)
        else:
            parts = text_to_split.split(separator)
            
        final_chunks = []
        current_chunk = ""
        
        for part in parts:
            candidate = current_chunk + (separator if current_chunk else "") + part
            
            if len(candidate) <= chunk_size:
                current_chunk = candidate
            else:
                if current_chunk:
                    final_chunks.append(current_chunk.strip())
                    # Overlap handling: pichle chunk ka end part naye chunk ke shuru mein laate hain
                    if chunk_overlap > 0 and len(current_chunk) > chunk_overlap:
                        overlap_text = current_chunk[-chunk_overlap:]
                        # Space ya boundary par cut karne ki koshish
                        space_idx = overlap_text.find(" ")
                        if space_idx != -1:
                            overlap_text = overlap_text[space_idx + 1:]
                        current_chunk = overlap_text + (separator if overlap_text else "") + part
                    else:
                        current_chunk = part
                else:
                    # Agar single part hi chunk_size se bada hai, agle deep separator par jao
                    sub_splits = _split_with_separators(part, sep_index + 1)
                    final_chunks.extend(sub_splits)
                    current_chunk = ""
                    
        if current_chunk and current_chunk.strip():
            final_chunks.append(current_chunk.strip())
            
        return final_chunks

    raw_chunks = _split_with_separators(text, 0)
    # Remove any empty or whitespace-only chunks
    return [c.strip() for c in raw_chunks if c and len(c.strip()) > 20]


def chunk_documents(pages_data: List[Dict[str, Any]], 
                    chunk_size: int = config.CHUNK_SIZE, 
                    chunk_overlap: int = config.CHUNK_OVERLAP) -> List[Dict[str, Any]]:
    """
    pdf_reader.py se aane wale pages ko chunks mein convert karta hai
    aur metadata (source file, page number, chunk_id) attach karta hai.
    
    Args:
        pages_data: List of dicts from pdf_reader.py (contains text and metadata)
        chunk_size: Max characters per chunk (default from config)
        chunk_overlap: Overlapping characters (default from config)
        
    Returns:
        List of chunk dicts:
        [
            {
                "chunk_text": "Text snippet...",
                "metadata": {
                    "source": "AI_Notes.pdf",
                    "page": 2,
                    "chunk_id": 5
                }
            }, ...
        ]
    """
    all_chunks = []
    global_chunk_id = 0
    
    for page_item in pages_data:
        text = page_item.get("text", "")
        meta = page_item.get("metadata", {})
        
        # Split page text into overlapping pieces
        text_pieces = split_text_recursive(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        for piece in text_pieces:
            chunk_entry = {
                "chunk_text": piece,
                "metadata": {
                    "source": meta.get("source", "unknown.pdf"),
                    "page": meta.get("page", 1),
                    "total_pages": meta.get("total_pages", 1),
                    "chunk_id": global_chunk_id
                }
            }
            all_chunks.append(chunk_entry)
            global_chunk_id += 1
            
    print(f"[Text Splitter] Successfully created {len(all_chunks)} chunks from {len(pages_data)} page(s).")
    return all_chunks


if __name__ == "__main__":
    print("Testing text_splitter.py...")
    sample_pages = [
        {
            "text": "Artificial Intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Machine learning is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention. Deep learning is a subset of machine learning based on artificial neural networks.",
            "metadata": {"source": "sample_ai_notes.pdf", "page": 1, "total_pages": 1}
        }
    ]
    chunks = chunk_documents(sample_pages, chunk_size=150, chunk_overlap=30)
    print(f"Generated {len(chunks)} chunks.")
    for c in chunks:
        print(f" Chunk #{c['metadata']['chunk_id']} (Page {c['metadata']['page']}): {c['chunk_text'][:60]}...")
    print("text_splitter.py test PASSED! ✅")
