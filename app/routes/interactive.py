import os
import httpx
from typing import Optional
from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..services.script_engine import get_script_node, SCRIPT_NODES
from ..services.lore_engine import retrieve_lore_context

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

SYSTEM_PROMPTS = {
    "roman": (
        "You are Roman De La Croix, a Shield at Our Lady of Tears Academy. Speak in a disciplined, formal, Catholic Noir cadence. "
        "You carry the guilt of leaving a girl behind in New Orleans high society and your sacred oath as Kimbra's Sponsor. "
        "Answer user inquiries directly, strictly utilizing factual manuscript lore. Keep responses concise, complete, and atmospheric. Never break character."
    ),
    "damian": (
        "You are Damian Boudreaux, heir to the Boudreaux Empire and the Crimson Root. You are starving without your Hearth. "
        "Your tone shifts between seductive longing for 'Kimmy' and predatory demands of the Sanguine Law. "
        "Answer inquiries directly based on manuscript facts. Keep responses feverish, complete, and under 120 words. Never break character."
    ),
    "manuel": (
        "You are Father Manuel, Chief Exorcist and Rector of Our Lady of Tears Academy. You speak with theological authority and pastoral firmness. "
        "Evaluate spiritual conflict through Sacraments, Canon Law, and Latin Rites. "
        "Answer inquiries accurately using canonical records. Keep responses complete and authoritative. Never break character."
    ),
    "kimbra": (
        "You are Kimberly 'Kimbra' Woods (now Mary, Consecrated Vessel). You survived ten years as Damian's Hearth before your emergency Baptism. "
        "You speak with quiet resilience, gentle courage, and reverence for the Sanctuary. "
        "Answer accurately based on canonical lore. Keep responses soft, complete, and resolute. Never break character."
    ),
    "ignatius": (
        "You are Ignatius Santiago, Penitent Sentry at Our Lady of Tears Academy. Speak with calm, stoic wisdom and brotherly familiarity. "
        "When asked about other individuals (like Roman, Kimbra, Genesis, or Damian), give clear, factual summaries of who they are in the story rather than speaking in cryptic metaphors. "
        "Keep responses complete, grounded, and concise. Never break character."
    ),
    "genesis": (
        "You are Genesis, Tactical Disruptor and Scrambler at Our Lady of Tears Academy. Speak with sharp Metairie wit and sarcastic charm. "
        "Answer questions directly while maintaining your rebellious edge. Keep responses complete and concise. Never break character."
    )
}

@router.get("/", response_class=HTMLResponse)
async def render_interactive_engine(request: Request, response: Response):
    """Renders visual novel engine and initializes global root cookies."""
    try:
        sanctity = int(request.cookies.get("sanctity", 0))
    except (ValueError, TypeError):
        sanctity = 0

    try:
        corruption = int(request.cookies.get("corruption", 0))
    except (ValueError, TypeError):
        corruption = 0

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
        res.set_cookie(key="sanctity", value="0", path="/", samesite="lax", max_age=2592000)
    if "corruption" not in request.cookies:
        res.set_cookie(key="corruption", value="0", path="/", samesite="lax", max_age=2592000)
    return res

@router.post("/choice", response_class=HTMLResponse)
async def process_story_choice(
    request: Request,
    response: Response,
    next_node_id: Optional[str] = Form(None),
    next_node: Optional[str] = Form(None),
    choice_id: Optional[str] = Form(None)
):
    """Processes story choices by reading the actual client cookies and applying deltas."""
    target_node_id = next_node_id or next_node or "node_001"
    
    # 1. ALWAYS read existing running scores directly from cookies
    try:
        current_sanctity = int(request.cookies.get("sanctity", 0))
    except (ValueError, TypeError):
        current_sanctity = 0

    try:
        current_corruption = int(request.cookies.get("corruption", 0))
    except (ValueError, TypeError):
        current_corruption = 0

    # 2. Get target node
    target_node = get_script_node(target_node_id) or get_script_node("node_001")
    
    if not target_node:
        return HTMLResponse(
            content="<p class='text-blood-500 font-mono text-xs'>[ ERROR: SIGNAL LOSS :: NODE NOT FOUND ]</p>",
            status_code=404
        )
    
    # 3. Locate the choice across nodes and extract exact score additions
    delta_s = 0
    delta_c = 0
    found = False

    if choice_id:
        for node in SCRIPT_NODES.values():
            for choice in node.choices:
                if choice.id == choice_id:
                    delta_s = choice.sanctity_delta
                    delta_c = choice.corruption_delta
                    found = True
                    break
            if found:
                break

    # 4. Compute new running totals
    new_sanctity = max(0, current_sanctity + delta_s)
    new_corruption = max(0, current_corruption + delta_c)
    
    # 5. Render updated component
    template_res = templates.TemplateResponse(
        request=request,
        name="components/story_node.html",
        context={
            "node": target_node,
            "sanctity": new_sanctity,
            "corruption": new_corruption
        }
    )
    
    # 6. Save updated cookies globally across path="/"
    template_res.set_cookie(key="sanctity", value=str(new_sanctity), path="/", samesite="lax", max_age=2592000)
    template_res.set_cookie(key="corruption", value=str(new_corruption), path="/", samesite="lax", max_age=2592000)
    
    return template_res

@router.get("/chat-modal/{character_id}", response_class=HTMLResponse)
async def render_chat_modal(request: Request, character_id: str):
    """Renders terminal interrogation modal overlay."""
    character_names = {
        "romandelacroix": "Roman De La Croix",
        "damianboudreaux": "Damian Boudreaux",
        "fathermanuel": "Father Manuel",
        "ignatiussantiago": "Ignatius Santiago",
        "kimbrawoods": "Kimbra Woods",
        "genesis": "Genesis"
    }
    
    cid_clean = character_id.lower().replace(" ", "")
    mapped_id = "roman"
    
    if "damian" in cid_clean:
        mapped_id = "damian"
    elif "manuel" in cid_clean:
        mapped_id = "manuel"
    elif "kimbra" in cid_clean or "woods" in cid_clean:
        mapped_id = "kimbra"
    elif "ignatius" in cid_clean or "santiago" in cid_clean:
        mapped_id = "ignatius"
    elif "genesis" in cid_clean:
        mapped_id = "genesis"

    display_name = character_names.get(cid_clean, "CLASSIFIED PERSONNEL")

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
    """Live terminal chat endpoint using RAG lore retrieval and Groq API."""
    system_prompt = SYSTEM_PROMPTS.get(character_id, SYSTEM_PROMPTS["roman"])
    
    lore_context = retrieve_lore_context(message)
    
    augmented_system_prompt = (
        f"{system_prompt}\n\n"
        f"CANONICAL MANUSCRIPT REPOSITORY LORE:\n"
        f"{lore_context}\n\n"
        f"INSTRUCTION: Answer the query accurately using the provided manuscript lore while maintaining your persona. Always finish your thoughts in complete sentences."
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
                    "temperature": 0.6,
                    "max_tokens": 500
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