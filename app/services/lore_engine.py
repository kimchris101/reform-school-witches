import os
import re
from pathlib import Path
from typing import List
from pypdf import PdfReader

PDF_TEXT_CHUNKS: List[str] = []
PDF_PATH = Path("app/static/downloads/RSFW_Book_1_The_Blood_Lily_Contract.pdf")

def initialize_pdf_lore_index():
    """Reads the PDF from app/static/downloads and slices it into compact search chunks."""
    global PDF_TEXT_CHUNKS
    
    if not PDF_PATH.exists():
        print(f"[ LORE ENGINE ] PDF not found at {PDF_PATH}. Falling back to default registry.")
        return

    try:
        reader = PdfReader(str(PDF_PATH))
        full_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
                
        combined_text = "\n".join(full_text)
        
        # Clean extra whitespace and split into smaller paragraphs
        cleaned_text = re.sub(r'\s+', ' ', combined_text)
        sentences = re.split(r'(?<=[.!?]) +', cleaned_text)
        
        # Group sentences into compact chunks (~300 characters max)
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < 300:
                current_chunk += " " + sentence
            else:
                if len(current_chunk.strip()) > 40:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk.strip())

        PDF_TEXT_CHUNKS = chunks
        print(f"[ LORE ENGINE SUCCESS ] Loaded {len(PDF_TEXT_CHUNKS)} compact manuscript chunks from {PDF_PATH.name}.")
    except Exception as e:
        print(f"[ LORE ENGINE ERROR ] Failed to parse PDF: {e}")

# Run PDF ingestion at startup
initialize_pdf_lore_index()

def retrieve_lore_context(query: str) -> str:
    """Scans manuscript chunks for matching keywords and returns a strict character-limited context."""
    if not PDF_TEXT_CHUNKS:
        return "No manuscript PDF loaded."

    # Filter out common stop words to improve keyword precision
    stop_words = {"who", "what", "where", "is", "are", "the", "a", "an", "and", "or", "about", "tell", "me"}
    query_words = [w.lower() for w in re.findall(r'\w+', query) if w.lower() not in stop_words]

    if not query_words:
        query_words = [query.lower()]

    matched_chunks = []
    
    # Match up to 2 small paragraphs
    for chunk in PDF_TEXT_CHUNKS:
        chunk_lower = chunk.lower()
        if any(word in chunk_lower for word in query_words):
            matched_chunks.append(chunk)
            if len(matched_chunks) >= 2:
                break

    if not matched_chunks:
        return "No specific manuscript lore matched; rely strictly on core character system prompt."

    # Hard cap the total context length to 1,000 characters (~200 tokens)
    joined_context = "\n---\n".join(matched_chunks)
    return joined_context[:1000]