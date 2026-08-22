import os
import re
from pathlib import Path
from typing import List
from pypdf import PdfReader

PDF_TEXT_CHUNKS: List[str] = []
PDF_PATH = Path("app/static/downloads/RSFW_Book_1_The_Blood_Lily_Contract.pdf")

CANONICAL_LORE_DATABASE = [
    {
        "keywords": ["father manuel", "manuel", "rector", "exorcist", "chief exorcist"],
        "content": (
            "Father Manuel is the Chief Exorcist and Rector of Our Lady of Tears Academy. "
            "He is the ordained priest in authority at the academy. He performed Kimbra Woods' Emergency Baptism in the White Room "
            "to sever her Sanguine tether from Damian Boudreaux."
        )
    },
    {
        "keywords": ["roman", "roman de la croix", "de la croix", "shield", "sponsor"],
        "content": (
            "Roman De La Croix is a student initiate and Shield Marshal at Our Lady of Tears Academy. "
            "Roman is NOT a priest. He is Kimbra's sacred Sponsor, carrying the guilt of leaving high society New Orleans "
            "while guarding the perimeter salt line."
        )
    },
    {
        "keywords": ["ignatius", "ignatius santiago", "santiago", "sentry", "penitent"],
        "content": (
            "Ignatius Santiago is a student initiate and Penitent Sentry at Our Lady of Tears Academy. "
            "He is NOT a priest, and NOT Kimbra's Sponsor. He stands watch over the perimeter salt line."
        )
    },
    {
        "keywords": ["damian", "damian boudreaux", "crimson heir", "root", "boudreaux", "heir", "hearth"],
        "content": (
            "Damian Boudreaux is the Crimson Heir to the Boudreaux Empire and the Crimson Root network. "
            "He seeks to reclaim Kimbra through the Sanguine Law."
        )
    },
    {
        "keywords": ["kimbra", "kimbra woods", "mary", "vessel", "consecrated vessel"],
        "content": (
            "Kimberly 'Kimbra' Woods (consecrated as Mary) is a student vessel at Our Lady of Tears Academy. "
            "Roman De La Croix is her Sponsor."
        )
    },
    {
        "keywords": ["genesis", "disruptor", "scrambler"],
        "content": (
            "Genesis is a student Tactical Disruptor and Scrambler at Our Lady of Tears Academy. "
            "She uses frequency signal interference technology to counter the Crimson Root."
        )
    }
]

def initialize_pdf_lore_index():
    """Reads the PDF from app/static/downloads and slices it into compact search chunks."""
    global PDF_TEXT_CHUNKS
    
    if not PDF_PATH.exists():
        print(f"[ LORE ENGINE ] PDF not found at {PDF_PATH}. Utilizing canonical registry.")
        return

    try:
        reader = PdfReader(str(PDF_PATH))
        full_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
                
        combined_text = "\n".join(full_text)
        cleaned_text = re.sub(r'\s+', ' ', combined_text)
        sentences = re.split(r'(?<=[.!?]) +', cleaned_text)
        
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

initialize_pdf_lore_index()

def retrieve_lore_context(query: str) -> str:
    """Scans manuscript PDF chunks and canonical registry for matching keywords."""
    query_clean = query.lower()
    
    canonical_matches = []
    for entry in CANONICAL_LORE_DATABASE:
        if any(keyword in query_clean for keyword in entry["keywords"]):
            canonical_matches.append(entry["content"])

    stop_words = {"who", "what", "where", "is", "are", "the", "a", "an", "and", "or", "about", "tell", "me"}
    query_words = [w.lower() for w in re.findall(r'\w+', query) if w.lower() not in stop_words]

    if not query_words:
        query_words = [query_clean]

    pdf_matches = []
    if PDF_TEXT_CHUNKS:
        for chunk in PDF_TEXT_CHUNKS:
            chunk_lower = chunk.lower()
            if any(word in chunk_lower for word in query_words):
                pdf_matches.append(chunk)
                if len(pdf_matches) >= 2:
                    break

    all_context_blocks = canonical_matches + pdf_matches

    if not all_context_blocks:
        return (
            "Our Lady of Tears Academy is a sanctuary guarded by student initiates like Roman De La Croix "
            "under Chief Exorcist Father Manuel."
        )

    joined_context = "\n---\n".join(all_context_blocks)
    return joined_context[:1000]