import os
import random
import json
import re
import urllib.request
import urllib.parse
import urllib.error
from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.utils.auth import is_authenticated_session, get_ssl_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Temporary in-memory OTP store: { "email@domain.com": {"code": "123456", "alias": "Initiate", "is_returning": False} }
VERIFICATION_CODES = {}

BOOKS_DB = [
    {
        "id": "book-1",
        "title": "The Blood Lily Contract",
        "subtitle": "Book 1 of The Reform School for Witches",
        "cover_url": "/static/media/dossiers/rsfwbook1.jpg",
        "file_name": "RSFW_Book_1_The_Blood_Lily_Contract.pdf",
        "pdf_path": "app/static/downloads/RSFW_Book_1_The_Blood_Lily_Contract.pdf",
        "tagline": "She was sold to the root. He was forged to be a shield.",
        "description": "In the deep shadows of New Orleans, time isn't measured by clocks, but by contracts. Kimbra Woods flees a nightmare ritual and storms Our Lady of Tears Academy, colliding with Roman De La Croix.",
        "is_members_only": True,
        "is_released": True,
        "release_status": "Available Now",
        "required_type": None,
        "required_score": 0,
        "unlock_perk": "Full Manuscript Access"
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
        "is_released": False,
        "release_status": "Archival Seal Locked",
        "required_type": "sanctity",
        "required_score": 100,
        "unlock_perk": "Decrypted Chapter 1 Preview (100% Sanctity Reached)"
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
        "is_released": False,
        "release_status": "In Archival Preparation",
        "required_type": "sanctity",
        "required_score": 100,
        "unlock_perk": "Classified Sanguine Audit Ledger (100% Sanctity Reached)"
    }
]

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_contact_registered_in_brevo(email: str) -> tuple[bool, str]:
    """
    Checks Brevo to verify if an email address is an existing registered member.
    Returns (True, firstName) if registered, or (False, "Initiate") if new.
    """
    api_key = os.getenv("BREVO_API_KEY", "").strip()
    if not api_key:
        return False, "Initiate"

    headers = {
        "accept": "application/json",
        "api-key": api_key
    }

    try:
        url = f"https://api.brevo.com/v3/contacts/{urllib.parse.quote(email)}"
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, context=get_ssl_context()) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                attributes = data.get("attributes", {})
                first_name = attributes.get("FIRSTNAME", "Initiate")
                return True, first_name
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, "Initiate"
        print(f"[ BREVO CONTACT CHECK HTTP ERROR ] {e.code}")
    except Exception as e:
        print(f"[ BREVO CONTACT CHECK ERROR ] {e}")

    return False, "Initiate"


def send_otp_via_brevo(recipient_email: str, otp_code: str, is_returning: bool = False) -> bool:
    """Dispatches a 6-digit verification code via Brevo with contextual subject lines."""
    api_key = os.getenv("BREVO_API_KEY", "").strip()
    sender_email = os.getenv("BREVO_SENDER_EMAIL", "hello@redcandledigital.io").strip()

    if not api_key:
        print(f"[ LOCAL DEV OTP ] Code for {recipient_email}: {otp_code} (Returning: {is_returning})")
        return True

    subject_title = "✝ Re-Authentication Passcode" if is_returning else "✝ Your Access Passcode"
    header_title = "Diocesan Clearance Restoration" if is_returning else "Diocesan Clearance Verification"
    body_text = "Enter the following 6-digit passcode to restore your active clearance and re-authenticate your browser session:" if is_returning else "Enter the following 6-digit passcode to verify your email and unlock vault access:"

    payload = {
        "sender": {"name": "Our Lady of Tears Academy", "email": sender_email},
        "to": [{"email": recipient_email}],
        "subject": f"{subject_title}: {otp_code}",
        "htmlContent": f"""
            <div style="font-family: Georgia, serif; background-color: #070a0f; color: #f4f0e6; padding: 24px; border: 1px solid #38050e; text-align: center;">
                <h2 style="color: #c7153a; margin-top: 0;">{header_title}</h2>
                <p style="font-size: 14px;">{body_text}</p>
                <div style="background-color: #0f141d; border: 1px solid #c7153a; color: #f59e0b; font-size: 28px; font-family: monospace; font-weight: bold; letter-spacing: 6px; padding: 16px; margin: 20px 0; display: inline-block;">
                    {otp_code}
                </div>
                <p style="font-size: 11px; color: #717c8d;">This single-use passcode expires shortly. If you did not request clearance restoration, ignore this message.</p>
            </div>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    try:
        req = urllib.request.Request(
            "https://api.brevo.com/v3/smtp/email",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req, context=get_ssl_context()) as response:
            return response.status in (200, 201)
    except Exception as e:
        print(f"[ BREVO OTP DISPATCH ERROR ] {e}")
        return False


def sync_contact_to_brevo(email: str, alias: str) -> bool:
    """Syncs a verified user's email and alias directly into Brevo Contacts."""
    api_key = os.getenv("BREVO_API_KEY", "").strip()
    list_id_env = os.getenv("BREVO_LIST_ID", "").strip()

    if not api_key:
        print(f"[ BREVO CONTACT SYNC SKIPPED (DEV) ] Email: {email} | Alias: {alias}")
        return True

    payload = {
        "email": email,
        "attributes": {
            "FIRSTNAME": alias
        },
        "updateEnabled": True
    }

    if list_id_env.isdigit():
        payload["listIds"] = [int(list_id_env)]

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    try:
        req = urllib.request.Request(
            "https://api.brevo.com/v3/contacts",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req, context=get_ssl_context()) as response:
            if response.status in (200, 201, 204):
                print(f"[ BREVO CONTACT SYNC SUCCESS ] Synced {email} ({alias})")
                return True
    except urllib.error.HTTPError as e:
        if e.code in (204, 400):
            print(f"[ BREVO CONTACT SYNC NOTICE ] Contact updated: {email}")
            return True
        print(f"[ BREVO CONTACT SYNC HTTP ERROR ] {e.code}: {e.read().decode()}")
    except Exception as e:
        print(f"[ BREVO CONTACT SYNC ERROR ] {e}")

    return False


@router.get("/", response_class=HTMLResponse)
async def render_vault_page(request: Request):
    is_authenticated = is_authenticated_session(request)
    
    try:
        sanctity = min(100, max(0, int(request.cookies.get("sanctity", 0))))
    except (ValueError, TypeError):
        sanctity = 0

    try:
        corruption = min(100, max(0, int(request.cookies.get("corruption", 0))))
    except (ValueError, TypeError):
        corruption = 0

    processed_books = []
    for book in BOOKS_DB:
        book_data = book.copy()
        current_score = sanctity if book["required_type"] == "sanctity" else 0
        req_score = book["required_score"]
        
        if req_score > 0:
            book_data["affinity_score"] = current_score
            book_data["clearance_progress"] = min(100, int((current_score / req_score) * 100))
            book_data["is_clearance_unlocked"] = current_score >= req_score
        else:
            book_data["affinity_score"] = 0
            book_data["clearance_progress"] = 100
            book_data["is_clearance_unlocked"] = True

        processed_books.append(book_data)

    return templates.TemplateResponse(
        request=request,
        name="pages/vault.html",
        context={
            "page_title": "Classified Book Vault | The Reform School for Witches Series",
            "meta_description": "Access and download official PDF releases of The Reform School for Witches trilogy.",
            "books": processed_books,
            "is_authenticated": is_authenticated,
            "sanctity": sanctity,
            "corruption": corruption
        }
    )


@router.get("/download/{book_id}")
async def download_book_pdf(request: Request, book_id: str):
    if not is_authenticated_session(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Diocesan Clearance Required. Please verify your email."
        )

    book = next((b for b in BOOKS_DB if b["id"] == book_id), None)
    
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")

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


@router.post("/request-verification", response_class=HTMLResponse)
async def request_verification_code(
    request: Request,
    email: str = Form(...),
    alias: str = Form(default="Initiate")
):
    """
    Detects if email belongs to an existing member. Generates a 6-digit OTP code,
    dispatches it via Brevo, and renders Step 2 with tailored messaging.
    """
    clean_email = email.strip().lower()

    if not EMAIL_REGEX.match(clean_email):
        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-blood-700 p-4 rounded text-center font-mono space-y-2">
                <span class="text-blood-500 font-bold text-xs">[ INVALID EMAIL ]</span>
                <p class="text-xs text-parchment-200">Please provide a valid email address to receive your passcode.</p>
            </div>
            """,
            status_code=400
        )

    # Check Brevo to see if contact exists
    is_registered, stored_alias = is_contact_registered_in_brevo(clean_email)
    final_alias = stored_alias if is_registered else (alias or "Initiate")

    otp_code = str(random.randint(100000, 999999))
    VERIFICATION_CODES[clean_email] = {
        "code": otp_code,
        "alias": final_alias,
        "is_returning": is_registered
    }

    sent = send_otp_via_brevo(clean_email, otp_code, is_returning=is_registered)

    if not sent:
        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-blood-700 p-4 rounded text-center font-mono space-y-2">
                <span class="text-blood-500 font-bold text-xs">[ DISPATCH ERROR ]</span>
                <p class="text-xs text-parchment-200">Unable to send verification email. Please try again.</p>
            </div>
            """,
            status_code=500
        )

    return templates.TemplateResponse(
        request=request,
        name="components/verify_code_form.html",
        context={
            "email": clean_email,
            "alias": final_alias,
            "is_returning": is_registered
        }
    )


@router.post("/verify-code", response_class=HTMLResponse)
async def verify_code_and_grant_access(
    request: Request,
    email: str = Form(...),
    code: str = Form(...)
):
    """Validates submitted OTP code, syncs contact to Brevo, and restores session token."""
    clean_email = email.strip().lower()
    clean_code = code.strip()

    record = VERIFICATION_CODES.get(clean_email)

    if not record or record["code"] != clean_code:
        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-blood-700 p-4 rounded text-center font-mono space-y-2 animate-shake">
                <span class="text-blood-500 font-bold text-xs">[ ACCESS DENIED ]</span>
                <p class="text-xs text-parchment-200">Incorrect or expired passcode. Please check your inbox and try again.</p>
            </div>
            """,
            status_code=400
        )

    alias = record.get("alias", "Initiate")
    is_returning = record.get("is_returning", False)
    
    # 1. Ensure contact record is saved/updated in Brevo
    sync_contact_to_brevo(clean_email, alias)

    # 2. Clean up used passcode
    del VERIFICATION_CODES[clean_email]

    # 3. Return clearance confirmation template & issue 30-day session cookie
    response = templates.TemplateResponse(
        request=request,
        name="components/vault_access_granted.html",
        context={
            "user_alias": alias,
            "is_returning": is_returning
        }
    )
    
    response.set_cookie(
        key="rsfw_member_token",
        value=f"initiate_{clean_email}",
        path="/",
        max_age=2592000,
        httponly=True,
        samesite="lax"
    )
    return response