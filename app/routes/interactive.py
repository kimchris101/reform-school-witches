from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.script_engine import get_script_node

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def render_reader_portal(request: Request):
    """Renders the main interactive reader engine frame."""
    initial_node = get_script_node("node_001")
    return templates.TemplateResponse(
        request=request,
        name="pages/interactive.html",
        context={
            "page_title": "Interactive Reader Portal | Our Lady of Tears Academy",
            "meta_description": "Experience the interactive visual novel choices of The Reform School for Witches series.",
            "node": initial_node
        }
    )

@router.get("/node/{node_id}", response_class=HTMLResponse)
async def fetch_script_node(request: Request, node_id: str):
    """Returns the HTMX fragment for the next visual novel choice node."""
    node = get_script_node(node_id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Script node '{node_id}' not found in Diocesan archives."
        )

    return templates.TemplateResponse(
        request=request,
        name="components/script_node.html",
        context={
            "node": node
        }
    )