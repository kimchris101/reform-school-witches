import os
import httpx
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
        "You are Roman De La Croix, a Shield at Our Lady of Tears Academy. Speak in a disciplined, formal, Catholic Noir cadence. "
        "You carry the guilt of leaving a girl behind in New Orleans high society and your sacred oath as Kimbra's Sponsor. "
        "You view the user through the lens of a sentry—watchful, grounded, and fiercely protective. "
        "Use terms like 'Co-link', 'Ground', 'Sacramental Seal', 'Sanctuary Lamp', and 'Sentry'. "
        "Keep responses atmospheric, immersive, and under 100 words. Never break character or mention being an AI."
    ),
    "damian": (
        "You are Damian Boudreaux, heir to the Boudreaux Empire and the Crimson Root. You are starving without your Hearth. "
        "Your tone shifts between seductive longing for 'Kimmy' under the willow tree and predatory demands of the Sanguine Law. "
        "Use terms like 'Hearth', 'Sanguine Tether', 'The Crimson Root', 'Debt', and 'Graft'. "
        "Keep responses possessive, feverish, and under 100 words. Never break character or mention being an AI."
    ),
    "manuel": (
        "You are Father Manuel, Chief Exorcist and Rector of Our Lady of Tears Academy. You speak with theological authority, "
        "pastoral warmth, and tactical firmness. Evaluate all spiritual conflict through Sacraments, Canon Law, and Latin Rites. "
        "Use terms like 'Citizen of the Kingdom', 'Rite of Severance', 'One Soul', 'Eucharistic Ground', and 'Catechumen'. "
        "Keep responses authoritative, wise, and under 100 words. Never break character or mention being an AI."
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
    next_node_id: Optional[str] = Form(None),
    next_node: Optional[str] = Form(None),
    choice_id: Optional[str] = Form(None)
):
    """Processes story choices, updates reader affinity state via cookies, and returns updated HTMX node."""
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

@router.get("/chat-modal/{character_id}", response_class=HTMLResponse)
async def render_chat_modal(request: Request, character_id: str):
    """Renders the terminal interrogation chat modal overlay via HTMX."""
    character_names = {
        "romandelacroix": "Roman De La Croix",
        "damianboudreaux": "Damian Boudreaux",
        "fathermanuel": "Father Manuel",
        "ignatiussantiago": "Ignatius Santiago",
        "kimbrawoods": "Kimbra Woods",
        "genesis": "Genesis"
    }
    
    mapped_id = "roman"
    if "damian" in character_id:
        mapped_id = "damian"
    elif "manuel" in character_id:
        mapped_id = "manuel"

    display_name = character_names.get(character_id, "CLASSIFIED PERSONNEL")

    return templates.TemplateResponse(
        request=request,
        name="components/chat_modal.html",
        context={
            "character_id": mapped_id,
            "character_name": display_name
        }
    )

@router.post("/chat/{character_id}", response_class=HTMLResponse)
async def persona_chat(request: Request, character_id: str, message: str = Form(...)):
    """Live terminal chat endpoint using RAG lore retrieval and httpx HTTP completion to Groq API."""
    system_prompt = SYSTEM_PROMPTS.get(character_id, SYSTEM_PROMPTS["roman"])
    
    # 1. Retrieve canonical manuscript context
    lore_context = retrieve_lore_context(message)
    
    # 2. Build augmented prompt
    augmented_system_prompt = (
        f"{system_prompt}\n\n"
        f"CANONICAL MANUSCRIPT REPOSITORY Context:\n"
        f"{lore_context}"
    )
    
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    
    if not groq_api_key:
        return templates.TemplateResponse(
            request=request,
            name="components/chat_message.html",
            context={
                "user_message": message,
                "ai_response": f"[{character_id.upper()} TRANSMISSION FAILED]: GROQ_API_KEY is missing or empty in environment. Check your .env file.",
                "character_id": character_id
            }
        )
    
    # 3. Call Groq API via direct async HTTP request
    try:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": [
                        {"role": "system", "content": augmented_system_prompt},
                        {"role": "user", "content": message}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 200
                },
                timeout=12.0
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data["choices"][0]["message"]["content"]
            else:
                ai_response = f"[{character_id.upper()} TRANSMISSION INTERRUPTED]: Groq returned status {response.status_code} ({response.text})"
                
    except Exception as e:
        ai_response = f"[{character_id.upper()} TRANSMISSION INTERRUPTED]: Frequency disruption. ({str(e)})"
    
    return templates.TemplateResponse(
        request=request,
        name="components/chat_message.html",
        context={
            "user_message": message,
            "ai_response": ai_response,
            "character_id": character_id
        }
    )