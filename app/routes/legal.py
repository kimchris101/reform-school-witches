import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    """Dispatches contact form submission via Brevo SMTP to bypass REST API IP whitelisting."""
    smtp_key = os.getenv("BREVO_API_KEY", "").strip()
    sender_email = "hello@redcandledigital.io"

    if not smtp_key:
        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-amber-500/60 p-6 rounded text-center space-y-3 font-mono">
                <span class="text-amber-400 font-bold">[ LOCAL DEV MODE ]</span>
                <p class="text-xs text-parchment-200">Set <code class="text-blood-400">BREVO_API_KEY</code> in .env to enable live delivery.</p>
                <button onclick="document.getElementById('modal-container').remove()" class="bg-blood-900 text-parchment-100 text-xs px-4 py-2 uppercase font-bold">DISMISS</button>
            </div>
            """
        )

    try:
        # Create Email Envelope
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[RSFW PORTAL INQUIRY] {subject}"
        msg["From"] = f"RSFW Portal Contact Form <{sender_email}>"
        msg["To"] = sender_email
        msg["Reply-To"] = f"{name} <{email}>"

        html_body = f"""
            <h3>New Contact Form Submission from RSFW Portal</h3>
            <p><strong>Sender Name:</strong> {name}</p>
            <p><strong>Sender Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <hr />
            <p><strong>Message:</strong></p>
            <p style="white-space: pre-wrap;">{message}</p>
        """
        msg.attach(MIMEText(html_body, "html"))

        # Connect to Brevo SMTP Server (Port 587)
        with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
            server.starttls()
            # Login using your Brevo SMTP login email and API Key
            server.login(sender_email, smtp_key)
            server.sendmail(sender_email, [sender_email], msg.as_string())

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
        print(f"[ SMTP DISPATCH ERROR ] {e}")
        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-blood-700 p-6 rounded text-center space-y-3 font-mono">
                <span class="text-blood-500 font-bold">[ TRANSMISSION ERROR ]</span>
                <p class="text-xs text-parchment-200">Unable to route message via Brevo. Please write directly to <span class="text-blood-400">hello@redcandledigital.io</span>.</p>
                <button onclick="document.getElementById('modal-container').remove()" class="bg-blood-900 text-parchment-100 text-xs px-4 py-2 uppercase font-bold">DISMISS</button>
            </div>
            """
        )