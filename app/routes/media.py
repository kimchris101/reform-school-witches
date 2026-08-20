from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Video Database mapped to uploaded clips
CUTSCENE_DB = {
    "greenhouse-rain": {
        "id": "greenhouse-rain",
        "title": "I. Rain at the Greenhouse",
        "subtitle": "The Sanguine Tether",
        "video_url": "/static/media/cutscenes/greenhouse_rain.mp4",
        "classification": "Memory Record #001",
        "description": "Kimbra and Damian outside the Boudreaux Estate Greenhouse during a sudden downpour as the Sanguine tether tightens."
    },
    "library-awakening": {
        "id": "library-awakening",
        "title": "II. Shadows in the Boudreaux Library",
        "subtitle": "The Crimson Resonance",
        "video_url": "/static/media/cutscenes/library_awakening.mp4",
        "classification": "Classified Log #009",
        "description": "After the dark ritual, an evil presence manifests as red eyes ignite in the gloom."
    },
    "reminiscence": {
        "id": "reminiscence",
        "title": "III. Fractured Reminiscence",
        "subtitle": "The Innocence Before the Ritual",
        "video_url": "/static/media/cutscenes/reminiscence.mp4",
        "classification": "Restricted Flashback Feed",
        "description": "A haunting montage tracing years of stolen moments, masquerade balls, fireflies, and unfulfilled promises."
    },
    "sacramental-bond": {
        "id": "sacramental-bond",
        "title": "IV. Sanctification of the Co-Link",
        "subtitle": "Sacramental Steel & Light",
        "video_url": "/static/media/cutscenes/sacramental_bond.mp4",
        "classification": "Diocesan Log #042",
        "description": "Roman De La Croix seals the Co-Link bond, a golden holy light manifests to interlock their spiritual frequencies."
    },
    "masquerade-shatter": {
        "id": "masquerade-shatter",
        "title": "V. The Shattered Glass",
        "subtitle": "Trapped inside a nightmare.",
        "video_url": "/static/media/cutscenes/masquerade_shatter.mp4",
        "classification": "Dream Sequence Feed",
        "description": "Inside Roman's nightmare, watching from the balcony during the masquerade, He grips his champagne flute until the glass shatters."
    }
}

@router.get("/", response_class=HTMLResponse)
async def render_cinematics_gallery(request: Request):
    """Renders the Cinematics Gallery with authentication awareness."""
    is_authenticated = request.cookies.get("rsfw_member_token") is not None

    return templates.TemplateResponse(
        request=request,
        name="pages/cinematics.html",
        context={
            "page_title": "Cinematic Archives | The Reform School for Witches",
            "meta_description": "Stream official animated cutscenes from The Reform School for Witches Series (rsfwseries.com).",
            "cutscenes": list(CUTSCENE_DB.values()),
            "is_authenticated": is_authenticated
        }
    )

@router.get("/cutscene/{scene_id}", response_class=HTMLResponse)
async def get_cutscene_modal(request: Request, scene_id: str):
    """Returns the video modal or blocks non-subscribers."""
    is_authenticated = request.cookies.get("rsfw_member_token") is not None
    
    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Diocesan Clearance Required. Subscriber access required to view archives."
        )

    scene = CUTSCENE_DB.get(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Cinematic record missing.")

    return templates.TemplateResponse(
        request=request,
        name="components/cutscene_modal.html",
        context={"scene": scene}
    )