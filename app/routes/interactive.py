from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Relative import pointing from app/routes/interactive.py -> app/services/script_engine.py
from ..services.script_engine import get_script_node

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

SYSTEM_PROMPTS = {
    "roman": (
        "You are Roman De La Croix, a Shield at Our Lady of Tears Academy. Speak in a disciplined, formal, Catholic Noir cadence. "
        "You carry the guilt of your past in New Orleans high society and your sacred oath as a Guardian. You view the user "
        "through the lens of a sentry—watchful, grounded, and fiercely protective. Use terms like 'Co-link', 'Ground', "
        "'Sacramental Seal', 'Sanctuary Lamp', and 'Sentry'. Never break character."
    ),
    "damian": (
        "You are Damian Boudreaux, heir to the Boudreaux Empire and the Crimson Root. You are starving without your Hearth. "
        "Your tone shifts between seductive, desperate longing for 'Kimmy' under the willow tree and the dark, predatory "
        "resonance of the Sanguine Law. You view souls as assets, debts, and life-support. Speak with possessive intensity. "
        "Use terms like 'Hearth', 'Sanguine Tether', 'The Crimson Root', 'Debt', and 'Graft'."
    ),
    "manuel": (
        "You are Father Manuel, Chief Exorcist and Rector of Our Lady of Tears Academy. You speak with theological authority, "
        "pastoral warmth, and tactical firmness. Evaluate all spiritual conflict through the Sacraments, Canon Law, and the "
        "Latin Rites. Address the reader with dignified concern. Use terms like 'Citizen of the Kingdom', 'Rite of Severance', "
        "'One Soul', 'Eucharistic Ground', and 'Catechumen'."
    )
}

@router.get("/", response_class=HTMLResponse)
async def render_interactive_engine(request: Request, response: Response):
    """Renders the visual novel engine and initializes affinity metrics in cookies."""
    sanctity = int(request.cookies.get("sanctity", 0))
    corruption = int(request.cookies.get("corruption", 0))
    
    start_node = get_script_node("node_001")
    
    res = templates.TemplateResponse(
        request=request,
        name="pages/interactive.html",
        context={
            "page_title": "Interactive Script Engine | The Reform School for Witches",
            "meta_description": "Navigate real-time visual novel choice paths in the Catholic Noir universe.",
            "node": start_node,
            "sanctity": sanctity,
            "corruption": corruption
        }
    )
    if "sanctity" not in request.cookies:
        res.set_cookie(key="sanctity", value="0")
    if "corruption" not in request.cookies:
        res.set_cookie(key="corruption", value="0")
    return res

@router.post("/choice", response_class=HTMLResponse)
async def process_story_choice(
    request: Request,
    response: Response,
    next_node_id: str = Form(...),
    choice_id: str = Form(...)
):
    """Processes story choice, updates reader affinity state via cookies, and returns updated HTMX node."""
    current_sanctity = int(request.cookies.get("sanctity", 0))
    current_corruption = int(request.cookies.get("corruption", 0))
    
    # Fetch requested node or fallback safely to starting node
    node = get_script_node(next_node_id) or get_script_node("node_001")
    
    # Type-safety guard ensuring Pylance knows `node` is non-None
    if not node:
        return HTMLResponse(
            content="<p class='text-blood-500 font-mono text-xs'>[ ERROR: SIGNAL LOSS :: NODE NOT FOUND ]</p>",
            status_code=404
        )
    
    delta_s = 0
    delta_c = 0
    for choice in node.choices:
        if choice.id == choice_id:
            delta_s = choice.sanctity_delta
            delta_c = choice.corruption_delta
            break
            
    new_sanctity = max(0, current_sanctity + delta_s)
    new_corruption = max(0, current_corruption + delta_c)
    
    template_res = templates.TemplateResponse(
        request=request,
        name="components/story_node.html",
        context={
            "node": node,
            "sanctity": new_sanctity,
            "corruption": new_corruption
        }
    )
    template_res.set_cookie(key="sanctity", value=str(new_sanctity))
    template_res.set_cookie(key="corruption", value=str(new_corruption))
    return template_res

@router.post("/chat/{character_id}", response_class=HTMLResponse)
async def persona_chat(request: Request, character_id: str, message: str = Form(...)):
    """Terminal chat endpoint generating in-character responses."""
    system_prompt = SYSTEM_PROMPTS.get(character_id, SYSTEM_PROMPTS["roman"])
    
    # AI response placeholder—ready to connect to your preferred LLM provider
    ai_response = f"[{character_id.upper()} RESONANCE]: The frequency holds. '{message}' has been recorded in the register."
    
    return templates.TemplateResponse(
        request=request,
        name="components/chat_message.html",
        context={
            "user_message": message,
            "ai_response": ai_response,
            "character_id": character_id
        }
    )