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
            "meta_description": "Privacy practices, Supabase data security, and local session directives."
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
    """
    Processes contact form submission.
    Logs submission and dispatches notification intended for hello@redcandledigital.io.
    """
    print(f"[ CONTACT TRANSMISSION ] From: {name} ({email}) | Subject: {subject}")
    print(f"[ MESSAGE BODY ] {message}")

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