import re
from pathlib import Path
from typing import List, Dict, Any
from pypdf import PdfReader

PDF_TEXT_CHUNKS: List[Dict[str, Any]] = []
PDF_PATH = Path("app/static/downloads/RSFW_Book_1_The_Blood_Lily_Contract.pdf")


def initialize_pdf_lore_index():
    """Ingests the manuscript PDF and indexes page contents into searchable chunks."""
    global PDF_TEXT_CHUNKS
    
    if not PDF_PATH.exists():
        print(f"[ LORE ENGINE ] PDF not found at {PDF_PATH}. Static search unavailable.")
        return

    try:
        reader = PdfReader(str(PDF_PATH))
        chunks = []

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
                
            # Clean extra whitespace
            cleaned_text = re.sub(r'\s+', ' ', text).strip()
            
            # Split page into logical paragraphs
            paragraphs = re.split(r'(?<=[.!?]) +', cleaned_text)
            
            current_chunk = ""
            for sentence in paragraphs:
                if len(current_chunk) + len(sentence) < 400:
                    current_chunk += " " + sentence
                else:
                    if len(current_chunk.strip()) > 50:
                        chunks.append({
                            "page": page_num,
                            "text": current_chunk.strip()
                        })
                    current_chunk = sentence

            if current_chunk.strip():
                chunks.append({
                    "page": page_num,
                    "text": current_chunk.strip()
                })

        PDF_TEXT_CHUNKS = chunks
        print(f"[ LORE ENGINE SUCCESS ] Indexed {len(PDF_TEXT_CHUNKS)} manuscript chunks across {len(reader.pages)} pages.")

    except Exception as e:
        print(f"[ LORE ENGINE ERROR ] Ingestion failed: {e}")


# Initialize PDF search index on startup
initialize_pdf_lore_index()


def search_manuscript_lore(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """Scans indexed manuscript chunks for exact keyword matches and returns relevant excerpts."""
    if not PDF_TEXT_CHUNKS:
        return []

    stop_words = {"who", "what", "where", "is", "are", "the", "a", "an", "and", "or", "about", "tell", "me", "how"}
    query_words = [w.lower() for w in re.findall(r'\w+', query) if w.lower() not in stop_words]

    if not query_words:
        query_words = [query.lower().strip()]

    results = []
    for chunk in PDF_TEXT_CHUNKS:
        chunk_lower = chunk["text"].lower()
        # Rank chunks based on how many query keywords match
        matches = sum(1 for word in query_words if word in chunk_lower)
        if matches > 0:
            results.append({
                "page": chunk["page"],
                "text": chunk["text"],
                "score": matches
            })

    # Sort results by highest keyword match frequency
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]