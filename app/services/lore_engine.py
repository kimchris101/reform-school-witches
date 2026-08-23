import re
from pathlib import Path
from typing import List, Dict, Any
from pypdf import PdfReader

from ..config import settings

PDF_TEXT_CHUNKS: List[Dict[str, Any]] = []

# Primary Curated Lore Records (Guarantees 100% accuracy for key character queries)
CURATED_LORE_DATABASE = [
    {
        "keywords": ["roman", "roman de la croix", "sponsor", "shield"],
        "title": "ROMAN DE LA CROIX :: CHARACTER PROFILE",
        "content": (
            "Roman De La Croix is a student initiate and Shield at Our Lady of Tears Academy. "
            "Having renounced his high-society New Orleans origins for a uniform of salt and stone, "
            "Roman serves as Kimbra Woods' sacred Sponsor, bound by oath to protect her from the Crimson Root."
        ),
        "page": "Official Character Record"
    },
    {
        "keywords": ["father manuel", "manuel", "rector", "exorcist"],
        "title": "FATHER MANUEL :: RECTOR & CHIEF EXORCIST",
        "content": (
            "Father Manuel is the Rector and Chief Exorcist of Our Lady of Tears Academy. "
            "As the primary ordained authority at the academy, he oversees canonical records, "
            "sacramental barriers, and performed Kimbra's Emergency Baptism in the White Room."
        ),
        "page": "Official Character Record"
    },
    {
        "keywords": ["damian", "damian boudreaux", "root", "crimson heir"],
        "title": "DAMIAN BOUDREAUX :: CRIMSON HEIR",
        "content": (
            "Damian Boudreaux is the heir to the Boudreaux Empire and leader of the parasitic Crimson Root network. "
            "He views Kimbra as his 'Hearth' and seeks to enforce ancestral graft tethers under the Sanguine Law."
        ),
        "page": "Official Character Record"
    },
    {
        "keywords": ["kimbra", "kimbra woods", "mary", "vessel"],
        "title": "KIMBRA WOODS :: STUDENT VESSEL",
        "content": (
            "Kimberly 'Kimbra' Woods (consecrated as Mary) is a student vessel at Our Lady of Tears Academy. "
            "After surviving ten years tied to Damian Boudreaux, she escaped to the sanctuary where her emergency baptism severed her tether."
        ),
        "page": "Official Character Record"
    },
    {
        "keywords": ["ignatius", "ignatius santiago", "sentry"],
        "title": "IGNATIUS SANTIAGO :: PENITENT SENTRY",
        "content": (
            "Ignatius Santiago is a student initiate and Penitent Sentry at Our Lady of Tears Academy. "
            "He stands watch over the perimeter salt lines and brine moat with calm, stoic vigilance."
        ),
        "page": "Official Character Record"
    }
]


def clean_manuscript_text(text: str) -> str:
    """Strips headers, page numbers, and formatting artifacts from PDF text."""
    cleaned = re.sub(r'RSFW:\s*The\s*Blood\s*Lily\s*Contract\s*\d*', '', text, flags=re.IGNORECASE)
    cleaned = re.sub(r'Page\s*\d+', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def initialize_pdf_lore_index():
    """Ingests the manuscript PDF from settings.MANUSCRIPT_PATH and indexes clean page contents into searchable chunks."""
    global PDF_TEXT_CHUNKS
    
    # Resolve absolute path relative to project root (up 3 levels from app/services/lore_engine.py)
    project_root = Path(__file__).resolve().parent.parent.parent
    pdf_path = project_root / settings.MANUSCRIPT_PATH
    
    if not pdf_path.exists():
        print(f"[ LORE ENGINE ] PDF not found at '{pdf_path}'. Utilizing primary curated database only.")
        return

    try:
        reader = PdfReader(str(pdf_path))
        chunks = []

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
                
            cleaned_text = clean_manuscript_text(text)
            if not cleaned_text:
                continue

            paragraphs = re.split(r'(?<=[.!?])\s+', cleaned_text)
            
            current_chunk = ""
            for sentence in paragraphs:
                if len(current_chunk) + len(sentence) < 350:
                    current_chunk += " " + sentence
                else:
                    if len(current_chunk.strip()) > 60:
                        chunks.append({
                            "page": f"Page {page_num}",
                            "text": current_chunk.strip(),
                            "content": current_chunk.strip()
                        })
                    current_chunk = sentence

            if len(current_chunk.strip()) > 60:
                chunks.append({
                    "page": f"Page {page_num}",
                    "text": current_chunk.strip(),
                    "content": current_chunk.strip()
                })

        PDF_TEXT_CHUNKS = chunks
        print(f"[ LORE ENGINE SUCCESS ] Indexed {len(PDF_TEXT_CHUNKS)} manuscript chunks across {len(reader.pages)} pages.")

    except Exception as e:
        print(f"[ LORE ENGINE ERROR ] PDF Ingestion failed: {e}")


def search_manuscript_lore(query: str, max_results: int = 2) -> List[Dict[str, Any]]:
    """
    Searches curated canonical records first; falls back to exact PDF manuscript scanning
    if no curated match is found.
    """
    query_clean = query.lower().strip()
    
    # 1. First, check Curated Lore Registry for character entity matches
    curated_matches = []
    for entry in CURATED_LORE_DATABASE:
        if any(keyword in query_clean for keyword in entry["keywords"]):
            curated_matches.append({
                "page": entry["page"],
                "text": entry["content"],
                "content": entry["content"]
            })

    if curated_matches:
        return curated_matches[:max_results]

    # 2. Fall back to scanning PDF manuscript chunks if query is not a main character name
    stop_words = {"who", "what", "where", "is", "are", "the", "a", "an", "and", "or", "about", "tell", "me", "how"}
    query_words = [w for w in re.findall(r'\w+', query_clean) if w not in stop_words]

    if not query_words:
        query_words = [query_clean]

    pdf_results = []
    if PDF_TEXT_CHUNKS:
        for chunk in PDF_TEXT_CHUNKS:
            chunk_lower = chunk["text"].lower()
            matches = sum(1 for word in query_words if word in chunk_lower)
            if matches > 0:
                pdf_results.append({
                    "page": chunk["page"],
                    "text": chunk["text"],
                    "content": chunk["text"],
                    "score": matches
                })

        pdf_results.sort(key=lambda x: x["score"], reverse=True)

    return pdf_results[:max_results]