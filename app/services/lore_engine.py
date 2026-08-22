import os
import re
from pathlib import Path
from typing import List
from pypdf import PdfReader

PDF_TEXT_CHUNKS: List[str] = []
PDF_PATH = Path("app/static/downloads/RSFW_Book_1_The_Blood_Lily_Contract.pdf")

# Canonical World Knowledge Base for core characters and lore entities
CANONICAL_LORE_DATABASE = [
    {
        "keywords": ["father manuel", "manuel", "rector", "exorcist", "chief exorcist"],
        "content": (
            "Father Manuel is the Rector and Chief Exorcist of Our Lady of Tears Academy. "
            "He speaks with theological authority, pastoral firmness, and oversees canonical records, "
            "Eucharistic Sacraments, and Latin Exorcism Rites. He performed Kimbra Woods' Emergency Baptism in the White Room "
            "to sever her Sanguine tether from Damian Boudreaux."
        )
    },
    {
        "keywords": ["roman", "roman de la croix", "de la croix", "shield", "sponsor"],
        "content": (
            "Roman De La Croix is a Shield and Perimeter Marshal at Our Lady of Tears Academy. "
            "Roman IS Kimbra's sacred Sponsor. Roman carries the guilt of leaving high society New Orleans "
            "and guards the perimeter salt line against the Crimson Root."
        )
    },
    {
        "keywords": ["ignatius", "ignatius santiago", "santiago", "sentry", "penitent"],
        "content": (
            "Ignatius Santiago is a Penitent Sentry at Our Lady of Tears Academy. "
            "He stands watch over the perimeter salt lines and brine moat with calm, stoic vigilance. "
            "Ignatius is NOT Kimbra's Sponsor (Roman De La Croix is her Sponsor)."
        )
    },
    {
        "keywords": ["damian", "damian boudreaux", "crimson heir", "root", "boudreaux", "heir", "hearth"],
        "content": (
            "Damian Boudreaux is the Crimson Heir to the Boudreaux Empire and the Crimson Root network. "
            "He seeks to reclaim Kimbra through the Sanguine Law and ancestral tethers."
        )
    },
    {
        "keywords": ["kimbra", "kimbra woods", "mary", "vessel", "consecrated vessel"],
        "content": (
            "Kimberly 'Kimbra' Woods (consecrated as Mary) survived ten years as Damian Boudreaux's Hearth before escaping "
            "to Our Lady of Tears Academy. Roman De La Croix is her Sponsor."
        )
    },
    {
        "keywords": ["genesis", "disruptor", "scrambler"],
        "content": (
            "Genesis is a Tactical Disruptor and Scrambler at Our Lady of Tears Academy. "
            "She uses frequency signal interference technology to counter the Crimson Root's broadcast array."
        )
    },
    {
        "keywords": ["academy", "our lady of tears", "sanctuary", "salt line"],
        "content": (
            "Our Lady of Tears Academy is a Catholic Noir sanctuary in New Orleans protected by coarse salt lines, "
            "sacramental barriers, and vigilant Shields defending against the parasitic Crimson Root network."
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
    """
    Scans manuscript PDF chunks and canonical world registry for matching keywords,
    returning a rich context block.
    """
    query_clean = query.lower()
    
    # 1. First, check Canonical Knowledge Base for entity/character matches
    canonical_matches = []
    for entry in CANONICAL_LORE_DATABASE:
        if any(keyword in query_clean for keyword in entry["keywords"]):
            canonical_matches.append(entry["content"])

    # 2. Extract query keywords for PDF chunk scanning
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

    # 3. Combine canonical entity lore with PDF manuscript excerpts
    all_context_blocks = canonical_matches + pdf_matches

    if not all_context_blocks:
        return (
            "Our Lady of Tears Academy is a Catholic Noir sanctuary in New Orleans guarded by salt lines, "
            "Shields like Roman De La Croix, Penitent Sentries like Ignatius Santiago, and Chief Exorcist Father Manuel. "
            "They defend against Damian Boudreaux and the parasitic Crimson Root network."
        )

    # Combine context and enforce maximum character window (~1200 chars)
    joined_context = "\n---\n".join(all_context_blocks)
    return joined_context[:1200]