import os
from pathlib import Path
from typing import List
from pypdf import PdfReader

# Track parsed PDF chunks in memory
PDF_TEXT_CHUNKS: List[str] = []

PDF_PATH = Path("app/static/downloads/RSFW_Book_1_The_Blood_Lily_Contract.pdf")

def initialize_pdf_lore_index():
    """Reads the PDF from app/static/downloads and slices it into readable search chunks."""
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
                
        # Combine pages and split into ~500-character searchable paragraphs
        combined_text = "\n".join(full_text)
        paragraphs = combined_text.split("\n\n")
        PDF_TEXT_CHUNKS = [p.strip() for p in paragraphs if len(p.strip()) > 50]
        print(f"[ LORE ENGINE SUCCESS ] Loaded {len(PDF_TEXT_CHUNKS)} canonical manuscript chunks from {PDF_PATH.name}.")
    except Exception as e:
        print(f"[ LORE ENGINE ERROR ] Failed to parse PDF: {e}")

# Run PDF ingestion at startup
initialize_pdf_lore_index()

def retrieve_lore_context(query: str) -> str:
    """Scans parsed manuscript PDF chunks for matching keywords from the user's transmission."""
    if not PDF_TEXT_CHUNKS:
        return "No manuscript PDF loaded."

    query_words = [w.lower() for w in query.split() if len(w) > 3]
    if not query_words:
        query_words = [query.lower()]

    matched_chunks = []
    
    # Scan manuscript PDF chunks for keyword matches
    for chunk in PDF_TEXT_CHUNKS:
        chunk_lower = chunk.lower()
        if any(word in chunk_lower for word in query_words):
            matched_chunks.append(chunk)
            if len(matched_chunks) >= 3:  # Limit context window to 3 relevant paragraphs
                break

    if not matched_chunks:
        return "No specific manuscript lore matched; rely strictly on core character system prompt."

    return "\n---\n".join(matched_chunks)