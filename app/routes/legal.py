import os
import json
import ssl
import urllib.request
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/privacy", response_class=HTMLResponse)
async def render_privacy_policy(request: Request):
    """Renders Privacy Policy page."""
    return templates.TemplateResponse(
        request=request,
        name="pages/privacy.html",
        context={
            "page_title": "Privacy Policy | The Reform School for Witches",
            "meta_description": "Privacy practices and data usage protocols for The Reform School for Witches."
        }
    )


@router.get("/terms", response_class=HTMLResponse)
async def render_terms_of_service(request: Request):
    """Renders Terms of Service page."""
    return templates.TemplateResponse(
        request=request,
        name="pages/terms.html",
        context={
            "page_title": "Terms of Service | The Reform School for Witches",
            "meta_description": "Terms of service and user agreements for accessing interactive content."
        }
    )


@router.get("/cookies", response_class=HTMLResponse)
async def render_cookie_policy(request: Request):
    """Renders Cookie Policy page."""
    return templates.TemplateResponse(
        request=request,
        name="pages/cookies.html",
        context={
            "page_title": "Cookie Policy | The Reform School for Witches",
            "meta_description": "Information on session tracking and client-side cookie usage."
        }
    )


@router.get("/contact-modal", response_class=HTMLResponse)
async def render_contact_modal(request: Request):
    """Renders the contact form modal overlay."""
    return templates.TemplateResponse(
        request=request,
        name="components/contact_modal.html"
    )


def send_brevo_payload(payload: dict, api_key: str, ssl_context: ssl.SSLContext) -> bool:
    """Helper function to execute HTTPS POST requests to Brevo API."""
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    
    req = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    with urllib.request.urlopen(req, context=ssl_context) as response:
        return response.status in (200, 201)


@router.post("/contact-send", response_class=HTMLResponse)
async def process_contact_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    """
    Dispatches contact form submission to hello@redcandledigital.io AND 
    sends an automated confirmation receipt back to the submitter.
    """
    api_key = os.getenv("BREVO_API_KEY", "").strip()
    recipient_email = "hello@redcandledigital.io"
    sender_email = os.getenv("BREVO_SENDER_EMAIL", recipient_email).strip()

    if not api_key:
        print(f"[ CONTACT LOG ] (No API Key Found) From: {name} ({email}) | Subject: {subject}")
        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-amber-500/60 p-6 rounded text-center space-y-3 font-mono">
                <span class="text-amber-400 font-bold">[ LOCAL DEV MODE ]</span>
                <p class="text-xs text-parchment-200">Set <code class="text-blood-400">BREVO_API_KEY</code> in .env to enable live delivery.</p>
                <button onclick="document.getElementById('modal-container').remove()" class="bg-blood-900 text-parchment-100 text-xs px-4 py-2 uppercase font-bold">DISMISS</button>
            </div>
            """
        )

    # SSL Context Setup
    try:
        import certifi
        ssl_context = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ssl_context = ssl._create_unverified_context()

    # 1. Payload: Internal Notification (Sent to hello@redcandledigital.io)
    admin_payload = {
        "sender": {"name": "RSFW Portal Contact Form", "email": sender_email},
        "to": [{"email": recipient_email, "name": "RSFW Registrar"}],
        "replyTo": {"email": email, "name": name},
        "subject": f"[RSFW PORTAL INQUIRY] {subject}",
        "htmlContent": f"""
            <h3>New Contact Form Submission from RSFW Portal</h3>
            <p><strong>Sender Name:</strong> {name}</p>
            <p><strong>Sender Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <hr />
            <p><strong>Message:</strong></p>
            <p style="white-space: pre-wrap;">{message}</p>
        """
    }

    # 2. Payload: User Confirmation Email (Sent to user who filled the form)
    user_payload = {
        "sender": {"name": "The Reform School for Witches", "email": sender_email},
        "to": [{"email": email, "name": name}],
        "replyTo": {"email": recipient_email, "name": "RSFW Registrar"},
        "subject": f"✝ Confirmation Receipt: {subject}",
        "htmlContent": f"""
            <div style="font-family: Georgia, serif; background-color: #070a0f; color: #f4f0e6; padding: 24px; border: 1px solid #38050e;">
                <h2 style="color: #c7153a; margin-top: 0;">Transmission Received</h2>
                <p>Greetings, <strong>{name}</strong>,</p>
                <p>Your message has been logged by the Academy Registrar and dispatched to <code>hello@redcandledigital.io</code>.</p>
                <hr style="border-color: #38050e; margin: 20px 0;" />
                <p style="font-size: 13px; color: #b8a37d;"><strong>Summary of your transmission:</strong></p>
                <p style="font-size: 13px; color: #e5dccb;"><strong>Subject:</strong> {subject}</p>
                <p style="font-size: 13px; color: #e5dccb; white-space: pre-wrap;"><em>"{message}"</em></p>
                <hr style="border-color: #38050e; margin: 20px 0;" />
                <p style="font-size: 11px; color: #717c8d;">The Reform School for Witches — Official Series Portal</p>
            </div>
        """
    }

    try:
        # Dispatch email to Admin
        send_brevo_payload(admin_payload, api_key, ssl_context)

        # Dispatch automated confirmation receipt to User
        send_brevo_payload(user_payload, api_key, ssl_context)

        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-amber-500/60 p-6 rounded text-center space-y-3 animate-fade-in font-mono">
                <span class="text-amber-400 text-lg font-bold">✝ TRANSMISSION RECEIVED ✝</span>
                <p class="text-xs text-parchment-200">Your message has been dispatched. A confirmation receipt has been sent to your email.</p>
                <button onclick="document.getElementById('modal-container').remove()" class="mt-2 bg-blood-900 hover:bg-blood-800 text-parchment-100 text-xs px-4 py-2 uppercase tracking-widest font-bold transition-colors">
                    DISMISS
                </button>
            </div>
            """
        )

    except Exception as e:
        print(f"[ BREVO API DISPATCH ERROR ] {e}")
        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-blood-700 p-6 rounded text-center space-y-3 font-mono">
                <span class="text-blood-500 font-bold">[ TRANSMISSION ERROR ]</span>
                <p class="text-xs text-parchment-200">Unable to route message. Please write directly to <span class="text-blood-400">hello@redcandledigital.io</span>.</p>
                <button onclick="document.getElementById('modal-container').remove()" class="bg-blood-900 text-parchment-100 text-xs px-4 py-2 uppercase font-bold">DISMISS</button>
            </div>
            """
        )