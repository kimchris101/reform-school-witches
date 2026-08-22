import re
from pathlib import Path
from typing import List, Dict, Any
from pypdf import PdfReader

PDF_TEXT_CHUNKS: List[Dict[str, Any]] = []
PDF_PATH = Path("app/static/downloads/RSFW_Book_1_The_Blood_Lily_Contract.pdf")


def clean_manuscript_text(text: str) -> str:
    """Removes running headers, page numbers, and formatting artifacts from PDF text."""
    # Strip running manuscript title and chapter header artifacts
    cleaned = re.sub(r'RSFW:\s*The\s*Blood\s*Lily\s*Contract\s*\d*', '', text, flags=re.IGNORECASE)
    cleaned = re.sub(r'Page\s*\d+', '', cleaned, flags=re.IGNORECASE)
    # Clean broken character spacing artifacts (e.g., 'u n i f o r m' -> 'uniform')
    cleaned = re.sub(r'(?<=\b\w)\s(?=\w\b)', '', cleaned)
    # Normalize multiple whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def initialize_pdf_lore_index():
    """Ingests the manuscript PDF and indexes sanitized page contents into searchable chunks."""
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
                
            cleaned_text = clean_manuscript_text(text)
            if not cleaned_text:
                continue

            # Split page into logical sentences/paragraphs
            paragraphs = re.split(r'(?<=[.!?])\s+', cleaned_text)
            
            current_chunk = ""
            for sentence in paragraphs:
                if len(current_chunk) + len(sentence) < 350:
                    current_chunk += " " + sentence
                else:
                    if len(current_chunk.strip()) > 60:
                        chunks.append({
                            "page": page_num,
                            "text": current_chunk.strip()
                        })
                    current_chunk = sentence

            if len(current_chunk.strip()) > 60:
                chunks.append({
                    "page": page_num,
                    "text": current_chunk.strip()
                })

        PDF_TEXT_CHUNKS = chunks
        print(f"[ LORE ENGINE SUCCESS ] Indexed {len(PDF_TEXT_CHUNKS)} clean manuscript chunks across {len(reader.pages)} pages.")

    except Exception as e:
        print(f"[ LORE ENGINE ERROR ] Ingestion failed: {e}")


# Initialize PDF search index on startup
initialize_pdf_lore_index()


def search_manuscript_lore(query: str, max_results: int = 2) -> List[Dict[str, Any]]:
    """Scans indexed manuscript chunks for exact keyword matches and returns verified excerpts."""
    if not PDF_TEXT_CHUNKS:
        return []

    stop_words = {"who", "what", "where", "is", "are", "the", "a", "an", "and", "or", "about", "tell", "me", "how"}
    query_words = [w.lower() for w in re.findall(r'\w+', query) if w.lower() not in stop_words]

    if not query_words:
        query_words = [query.lower().strip()]

    results = []
    
    for chunk in PDF_TEXT_CHUNKS:
        chunk_lower = chunk["text"].lower()
        
        # Calculate how many explicit query keywords match this exact chunk
        matches = sum(1 for word in query_words if word in chunk_lower)
        
        # Require at least one direct keyword match
        if matches > 0:
            # If searching for a specific character, enforce that the chunk explicitly contains their name
            if "roman" in query_words and "roman" not in chunk_lower:
                continue
            if "manuel" in query_words and "manuel" not in chunk_lower:
                continue
            if "damian" in query_words and "damian" not in chunk_lower:
                continue
            if "kimbra" in query_words and "kimbra" not in chunk_lower:
                continue

            results.append({
                "page": chunk["page"],
                "text": chunk["text"],
                "score": matches
            })

    # Sort results by highest keyword match frequency
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]