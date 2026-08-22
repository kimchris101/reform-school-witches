import os
import json
import urllib.request
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/contact-send", response_class=HTMLResponse)
async def process_contact_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    """Dispatches contact form submission via Brevo REST API using urllib."""
    api_key = os.getenv("BREVO_API_KEY", "").strip()
    recipient_email = "hello@redcandledigital.io"

    if not api_key:
        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-amber-500/60 p-6 rounded text-center space-y-3 font-mono">
                <span class="text-amber-400 font-bold">[ LOCAL DEV MODE ]</span>
                <p class="text-xs text-parchment-200">Set <code class="text-blood-400">BREVO_API_KEY</code> in .env to enable live delivery.</p>
                <button onclick="document.getElementById('modal-container').remove()" class="bg-blood-900 text-parchment-100 text-xs px-4 py-2 uppercase font-bold">DISMISS</button>
            </div>
            """
        )

    # Prepare Brevo API Payload
    payload = {
        "sender": {"name": "RSFW Portal Contact Form", "email": recipient_email},
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

        with urllib.request.urlopen(req) as response:
            if response.status in (200, 201):
                return HTMLResponse(
                    content="""
                    <div class="bg-black/90 border border-amber-500/60 p-6 rounded text-center space-y-3 animate-fade-in font-mono">
                        <span class="text-amber-400 text-lg font-bold">✝ TRANSMISSION RECEIVED ✝</span>
                        <p class="text-xs text-parchment-200">Your message has been dispatched to the Registrar at <span class="text-blood-400 font-bold">hello@redcandledigital.io</span>.</p>
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