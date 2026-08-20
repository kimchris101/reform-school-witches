from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def render_media_gallery(request: Request):
    """Renders the Cinematic Unlocks gallery."""
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={
            "page_title": "High Yard Archives | Cinematic Unlocks",
            "meta_description": "View unlocked MP4 cinematic cutscenes from Our Lady of Tears Academy."
        }
    )