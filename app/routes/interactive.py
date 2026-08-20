from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

STORY_NODES = {
    "start": {
        "id": "start",
        "title": "The South Ramparts Breach",
        "speaker": "Father Manuel",
        "background": "/static/media/bg_courtyard.jpg",
        "dialogue": "The salt line at the eastern gate is crumbling. Roman holds the circuit, but the resonance is wavering. Initiate, where do you direct your focus?",
        "choices": [
            {"text": "Strengthen the salt line with Ignatius", "next_node": "strengthen_salt"},
            {"text": "Reinforce the Co-Link conduit with Roman", "next_node": "link_conduit"}
        ]
    },
    "strengthen_salt": {
        "id": "strengthen_salt",
        "title": "Outer Salt Perimeter",
        "speaker": "Ignatius Santiago",
        "background": "/static/media/bg_courtyard.jpg",
        "dialogue": "The discharge from the marsh is heavy, but the barrier holds! Keep your feet planted and do not look into the mist.",
        "choices": [
            {"text": "Hold ground and complete the rite", "next_node": "start"}
        ]
    },
    "link_conduit": {
        "id": "link_conduit",
        "title": "The High-Rite Sanctuary",
        "speaker": "Roman De La Croix",
        "background": "/static/media/bg_courtyard.jpg",
        "dialogue": "Two heartbeats, one frequency. Hold the connection before the signal fractures!",
        "choices": [
            {"text": "Lock frequency and seal the perimeter", "next_node": "start"}
        ]
    }
}

@router.get("/", response_class=HTMLResponse)
async def render_interactive_engine(request: Request):
    """Renders the main visual novel container page."""
    return templates.TemplateResponse(
        request=request,
        name="pages/interactive.html",
        context={
            "page_title": "Interactive Script Engine | The Reform School for Witches",
            "meta_description": "Navigate real-time visual novel choice paths in the Sacramental Noir universe.",
            "node": STORY_NODES["start"]
        }
    )

@router.post("/choice", response_class=HTMLResponse)
async def process_story_choice(request: Request, next_node: str = Form(...)):
    """Processes a choice selection and returns the next scene fragment via HTMX."""
    node = STORY_NODES.get(next_node, STORY_NODES["start"])
    return templates.TemplateResponse(
        request=request,
        name="components/story_node.html",
        context={"node": node}
    )