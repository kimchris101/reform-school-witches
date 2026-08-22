from typing import Optional
from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..services.script_engine import get_script_node, SCRIPT_NODES

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def render_interactive_engine(request: Request, response: Response):
    """Renders engine if authenticated via Intake Exam; otherwise displays clearance restriction screen."""
    is_authenticated = request.cookies.get("rsfw_member_token") is not None

    if not is_authenticated:
        return templates.TemplateResponse(
            request=request,
            name="pages/intake_required.html",
            context={
                "page_title": "Intake Exam Required | The Reform School for Witches",
                "meta_description": "Complete your intake exam registration to unlock access to the interactive script engine."
            }
        )

    try:
        sanctity = min(100, max(0, int(request.cookies.get("sanctity", 0))))
    except (ValueError, TypeError):
        sanctity = 0

    try:
        corruption = min(100, max(0, int(request.cookies.get("corruption", 0))))
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
    """Processes story choice actions with zero-sum metric calculation."""
    is_authenticated = request.cookies.get("rsfw_member_token") is not None
    if not is_authenticated:
        return HTMLResponse(
            content="<p class='text-blood-500 font-mono text-xs'>[ ERROR: INTAKE EXAM CLEARANCE EXPIRED ]</p>",
            status_code=401
        )

    target_node_id = next_node_id or next_node or "node_001"
    
    try:
        current_sanctity = int(request.cookies.get("sanctity", 0))
    except (ValueError, TypeError):
        current_sanctity = 0

    try:
        current_corruption = int(request.cookies.get("corruption", 0))
    except (ValueError, TypeError):
        current_corruption = 0

    target_node = get_script_node(target_node_id) or get_script_node("node_001")
    
    if not target_node:
        return HTMLResponse(
            content="<p class='text-blood-500 font-mono text-xs'>[ ERROR: SIGNAL LOSS :: NODE NOT FOUND ]</p>",
            status_code=404
        )
    
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

    raw_sanctity = current_sanctity + delta_s - delta_c
    raw_corruption = current_corruption + delta_c - delta_s

    new_sanctity = min(100, max(0, raw_sanctity))
    new_corruption = min(100, max(0, raw_corruption))
    
    template_res = templates.TemplateResponse(
        request=request,
        name="components/story_node.html",
        context={
            "node": target_node,
            "sanctity": new_sanctity,
            "corruption": new_corruption
        }
    )
    
    template_res.set_cookie(key="sanctity", value=str(new_sanctity), path="/", samesite="lax", max_age=2592000)
    template_res.set_cookie(key="corruption", value=str(new_corruption), path="/", samesite="lax", max_age=2592000)
    
    return template_res