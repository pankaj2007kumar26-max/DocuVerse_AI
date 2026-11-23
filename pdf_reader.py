"""
DocuVerse AI - PDF Reader Module (pdf_reader.py)
-----------------------------------------------
Yeh module PyMuPDF (fitz) use karke uploaded PDFs se high-speed text
aur metadata (filename, page numbers) extract karta hai.
Streamlit uploaded files (in-memory bytes) aur disk file paths dono support karta hai.
"""

import io
from typing import List, Dict, Any, Union
import pymupdf  # PyMuPDF library

def extract_text_from_pdf(pdf_source: Union[str, bytes, io.BytesIO], file_name: str = "document.pdf") -> List[Dict[str, Any]]:
    """
    Ek single PDF se page-by-page text aur metadata extract karta hai.
    
    Args:
        pdf_source: File path (str) YA in-memory bytes/BytesIO (Streamlit upload)
        file_name: PDF file ka display name (source reference ke liye)
        
    Returns:
        List of dicts:
        [
            {
                "text": "Extracted text content...",
                "metadata": {
                    "source": "notes.pdf",
                    "page": 1,
                    "total_pages": 5
                }
            },
            ...
        ]
    """
    pages_data = []
    
    try:
        # Check source type: bytes, file-like object, or file path
        if isinstance(pdf_source, (bytes, bytearray)):
            doc = pymupdf.open(stream=pdf_source, filetype="pdf")
        elif hasattr(pdf_source, "read"):
            # Streamlit UploadedFile ya BytesIO
            pdf_bytes = pdf_source.read()
            doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        else:
            # Normal disk path string
            doc = pymupdf.open(str(pdf_source))
            
        total_pages = len(doc)
        
        if total_pages == 0:
            print(f"[PDF Reader] Warning: '{file_name}' mein koi page nahi mila.")
            return pages_data
            
        for page_idx in range(total_pages):
            page = doc[page_idx]
            # Extract plain text with layout preservation
            page_text = page.get_text("text").strip()
            
            # Agar page blank nahi hai, tabhi add karenge
            if page_text:
                pages_data.append({
                    "text": page_text,
                    "metadata": {
                        "source": file_name,
                        "page": page_idx + 1,  # 1-indexed for human readability
                        "total_pages": total_pages
                    }
                })
                
        doc.close()
        
    except pymupdf.FileDataError:
        print(f"[PDF Reader] Error: '{file_name}' corrupt ya invalid PDF hai.")
    except Exception as e:
        print(f"[PDF Reader] Unexpected error while reading '{file_name}': {e}")
        
    return pages_data


def extract_text_from_multiple_pdfs(pdf_list: List[Any], file_names: List[str] = None) -> List[Dict[str, Any]]:
    """
    Multiple PDFs ko process karta hai aur ek unified list of pages return karta hai.
    
    Args:
        pdf_list: List of PDF file paths YA list of Streamlit UploadedFile objects.
        file_names: Optional custom list of file names.
        
    Returns:
        Combined list of all pages across all uploaded PDFs.
    """
    all_pages = []
    
    for idx, pdf in enumerate(pdf_list):
        # Name determine karte hain
        if file_names and idx < len(file_names):
            name = file_names[idx]
        elif hasattr(pdf, "name"):
            name = pdf.name
        else:
            name = f"document_{idx + 1}.pdf"
            
        print(f"[PDF Reader] Processing: {name}...")
        extracted_pages = extract_text_from_pdf(pdf, file_name=name)
        all_pages.extend(extracted_pages)
        print(f"[PDF Reader] Extracted {len(extracted_pages)} non-empty page(s) from {name}")
        
    return all_pages


if __name__ == "__main__":
    # Standalone quick test: Ek dummy PDF banakar extract karke dekhte hain
    print("Testing pdf_reader.py...")
    test_doc = pymupdf.open()
    page = test_doc.new_page()
    page.insert_text((50, 72), "DocuVerse AI - Hello World Test Page\nThis is a sample document for testing.")
    pdf_bytes = test_doc.tobytes()
    test_doc.close()
    
    results = extract_text_from_pdf(pdf_bytes, file_name="sample_test.pdf")
    print(f"Result count: {len(results)}")
    if results:
        print("Page 1 Metadata:", results[0]["metadata"])
        print("Page 1 Text Preview:", results[0]["text"])
        print("pdf_reader.py test PASSED! ✅")
