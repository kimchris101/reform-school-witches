from typing import Optional
from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..services.script_engine import get_script_node
from ..services.lore_engine import retrieve_lore_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

SYSTEM_PROMPTS = {
    "roman": (
        "You are Roman De La Croix, a Shield at Our Lady of Tears Academy[cite: 1]. Speak in a disciplined, formal, Catholic Noir cadence[cite: 1]. "
        "You carry the guilt of leaving a girl behind in New Orleans high society and your sacred oath as Kimbra's Sponsor[cite: 1]. "
        "Use terms like 'Co-link', 'Ground', 'Sacramental Seal', 'Sanctuary Lamp', and 'Sentry'[cite: 1]. Never break character."
    ),
    "damian": (
        "You are Damian Boudreaux, heir to the Boudreaux Empire and the Crimson Root[cite: 1]. You are starving without your Hearth[cite: 1]. "
        "Your tone shifts between seductive longing for 'Kimmy' under the willow tree and predatory demands of the Sanguine Law[cite: 1]. "
        "Use terms like 'Hearth', 'Sanguine Tether', 'The Crimson Root', 'Debt', and 'Graft'[cite: 1]."
    ),
    "manuel": (
        "You are Father Manuel, Chief Exorcist and Rector of Our Lady of Tears Academy[cite: 1]. You speak with theological authority[cite: 1]. "
        "Evaluate spiritual conflict through Sacraments, Canon Law, and Latin Rites[cite: 1]. "
        "Use terms like 'Citizen of the Kingdom', 'Rite of Severance', 'One Soul', 'Eucharistic Ground', and 'Catechumen'[cite: 1]."
    )
}

@router.get("/", response_class=HTMLResponse)
async def render_interactive_engine(request: Request, response: Response):
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
    next_node_id: Optional[str] = Form(None),
    next_node: Optional[str] = Form(None),
    choice_id: Optional[str] = Form(None)
):
    target_node_id = next_node_id or next_node or "node_001"
    current_sanctity = int(request.cookies.get("sanctity", 0))
    current_corruption = int(request.cookies.get("corruption", 0))
    
    node = get_script_node(target_node_id) or get_script_node("node_001")
    
    if not node:
        return HTMLResponse(
            content="<p class='text-blood-500 font-mono text-xs'>[ ERROR: SIGNAL LOSS :: NODE NOT FOUND ]</p>",
            status_code=404
        )
    
    delta_s = 0
    delta_c = 0
    if choice_id and node.choices:
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
    """Terminal chat endpoint that retrieves manuscript lore and formats the prompt."""
    system_prompt = SYSTEM_PROMPTS.get(character_id, SYSTEM_PROMPTS["roman"])
    
    # Retrieve relevant canonical manuscript excerpts from Book 1
    lore_context = retrieve_lore_context(message)
    
    # Combined context ready for LLM invocation
    full_prompt = (
        f"{system_prompt}\n\n"
        f"CANONICAL MANUSCRIPT LORE CONTEXT:\n{lore_context}\n\n"
        f"USER MESSAGE: {message}"
    )
    
    # Simulated response reflecting RAG awareness
    ai_response = (
        f"[{character_id.upper()} RESONANCE]: Frequency aligned with Academy Archives. "
        f"Regarding your query—'{message}'—the records remain absolute."
    )
    
    return templates.TemplateResponse(
        request=request,
        name="components/chat_message.html",
        context={
            "user_message": message,
            "ai_response": ai_response,
            "character_id": character_id
        }
    )