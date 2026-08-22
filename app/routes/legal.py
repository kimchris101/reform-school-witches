import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

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


@router.post("/contact-send", response_class=HTMLResponse)
async def process_contact_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    """Dispatches contact form submission to hello@redcandledigital.io via Brevo API."""
    api_key = os.getenv("BREVO_API_KEY", "").strip()

    if not api_key:
        print(f"[ CONTACT LOG ] (No API Key) From: {name} ({email}) | Subject: {subject}")
        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-amber-500/60 p-6 rounded text-center space-y-3 font-mono">
                <span class="text-amber-400 font-bold">[ LOCAL DEV MODE ]</span>
                <p class="text-xs text-parchment-200">Form captured in server logs. Set <code class="text-blood-400">BREVO_API_KEY</code> in .env to enable live delivery to hello@redcandledigital.io.</p>
                <button onclick="document.getElementById('modal-container').remove()" class="bg-blood-900 text-parchment-100 text-xs px-4 py-2 uppercase font-bold">DISMISS</button>
            </div>
            """
        )

    # Configure Brevo Client
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Define Email Envelope
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": "hello@redcandledigital.io", "name": "RSFW Registrar"}],
        reply_to={"email": email, "name": name},
        sender={"email": "hello@redcandledigital.io", "name": "RSFW Portal Contact Form"},
        subject=f"[RSFW PORTAL INQUIRY] {subject}",
        html_content=f"""
            <h3>New Contact Form Submission from RSFW Portal</h3>
            <p><strong>Sender Name:</strong> {name}</p>
            <p><strong>Sender Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <hr />
            <p><strong>Message:</strong></p>
            <p style="white-space: pre-wrap;">{message}</p>
        """
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
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

    except ApiException as e:
        print(f"[ BREVO API ERROR ] Exception when calling TransactionalEmailsApi->send_transac_email: {e}")
        return HTMLResponse(
            content="""
            <div class="bg-black/90 border border-blood-700 p-6 rounded text-center space-y-3 font-mono">
                <span class="text-blood-500 font-bold">[ TRANSMISSION ERROR ]</span>
                <p class="text-xs text-parchment-200">Unable to route message via Brevo. Please write directly to <span class="text-blood-400">hello@redcandledigital.io</span>.</p>
                <button onclick="document.getElementById('modal-container').remove()" class="bg-blood-900 text-parchment-100 text-xs px-4 py-2 uppercase font-bold">DISMISS</button>
            </div>
            """
        )
        