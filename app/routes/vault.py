from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Mock Book Database for the RSFW Series
BOOKS_DB = [
    {
        "id": "book-1",
        "title": "The Blood Lily Contract",
        "subtitle": "Book 1 of The Reform School for Witches",
        "cover_url": "/static/media/dossiers/rsfwbook1.jpg", # Or your book cover path
        "file_name": "RSFW_Book_1_The_Blood_Lily_Contract.pdf",
        "pdf_path": "app/static/downloads/RSFW_Book_1_The_Blood_Lily_Contract.pdf",
        "tagline": "She was sold to the root. He was forged to be a shield.",
        "description": "In the deep shadows of New Orleans, time isn't measured by clocks, but by contracts. Kimbra Woods flees a nightmare ritual and storms Our Lady of Tears Academy, colliding with Roman De La Croix.",
       "is_members_only": True,
        "is_released": True,  # RELEASED
        "release_status": "Available Now"
    },
    {
        "id": "book-2",
        "title": "Serpent in the Sanctuary",
        "subtitle": "Book 2 of The Reform School for Witches",
        "cover_url": "/static/media/dossiers/rsfwbook2.jpg",
        "file_name": "RSFW_Book_2_Serpent_in_the_Sanctuary.pdf",
        "pdf_path": "app/static/downloads/RSFW_Book_2_Serpent_in_the_Sanctuary.pdf",
        "tagline": "The refuge has cracks. The serpent is inside.",
        "description": "As Damian Boudreaux stirs in the North Wing Vault, a threat from the inside has already breached the perimeter salt-line, forcing Roman and Kimbra into a holy alliance.",
        "is_members_only": True,
        "is_released": False,  # LOCKED / UNRELEASED
        "release_status": "Coming Soon"
    },
    {
        "id": "book-3",
        "title": "Blood, Iron and Tears",
        "subtitle": "Book 3 of The Reform School for Witches",
        "cover_url": "/static/media/dossiers/rsfwbook3.jpg",
        "file_name": "RSFW_Book_3_Blood_Iron_and_Tears.pdf",
        "pdf_path": "app/static/downloads/RSFW_Book_3_Blood_Iron_and_Tears.pdf",
        "tagline": "The harvest has begun. New Orleans has run out of time.",
        "description": "Vincent Boudreaux weaves an ancient parasitic text into the New Orleans power grid, causing the French Quarter sky to bleed electric violet. Roman, Kimbra, and a restored Damian descend into St. Louis Cathedral for a final audit to save a city swallowing itself in debt.",
        "is_members_only": True,
        "is_released": False,  # LOCKED / UNRELEASED
        "release_status": "In Archival Preparation"
    }
]
@router.get("/", response_class=HTMLResponse)
async def render_vault_page(request: Request):
    is_authenticated = request.cookies.get("rsfw_member_token") is not None

    return templates.TemplateResponse(
        request=request,
        name="pages/vault.html",
        context={
            "page_title": "Classified Book Vault | The Reform School for Witches Series",
            "meta_description": "Access and download official PDF releases of The Reform School for Witches trilogy (rsfwseries.com). Free access for registered initiates.",
            "books": BOOKS_DB,
            "is_authenticated": is_authenticated
        }
    )

@router.get("/download/{book_id}")
async def download_book_pdf(request: Request, book_id: str):
    is_authenticated = request.cookies.get("rsfw_member_token") is not None
    
    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Diocesan Clearance Required. Please register for member access."
        )

    book = next((b for b in BOOKS_DB if b["id"] == book_id), None)
    
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")

    # Guard against downloading unreleased books
    if not book["is_released"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This archival record is sealed until official publication."
        )

    if not os.path.exists(book["pdf_path"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archival PDF record file missing from server."
        )

    return FileResponse(
        path=book["pdf_path"],
        filename=book["file_name"],
        media_type="application/pdf"
    )

@router.post("/register", response_class=HTMLResponse)
async def register_member(request: Request):
    form_data = await request.form()
    email = form_data.get("email")
    alias = form_data.get("alias")

    response = templates.TemplateResponse(
        request=request,
        name="components/vault_access_granted.html",
        context={"user_alias": alias}
    )
    response.set_cookie(key="rsfw_member_token", value=f"initiate_{email}", max_age=2592000)
    return response

