from fastapi import APIRouter, Request
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