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
        "subtitle": "The Blood Lily Tether",
        "video_url": "/static/media/cutscenes/greenhouse_rain.mp4",
        "classification": "Memory Record #001",
        "description": "Kimbra and Damian outside the Academy glasshouse during a sudden downpour as the Sanguine tether tightens."
    },
    "library-awakening": {
        "id": "library-awakening",
        "title": "II. Shadows in the Archival Vault",
        "subtitle": "The Crimson Resonance",
        "video_url": "/static/media/cutscenes/library_awakening.mp4",
        "classification": "Classified Log #009",
        "description": "In the Cathedral archives, a dark presence manifests as red eyes ignite in the gloom."
    },
    "reminiscence": {
        "id": "reminiscence",
        "title": "III. Fractured Reminiscence",
        "subtitle": "The Innocence Before the Root",
        "video_url": "/static/media/cutscenes/reminiscence.mp4",
        "classification": "Restricted Flashback Feed",
        "description": "A haunting montage tracing years of stolen moments, masquerade balls, fireflies, and unfulfilled promises."
    },
    "sacramental-bond": {
        "id": "sacramental-bond",
        "title": "IV. Sanctification of the Co-Link",
        "subtitle": "Sacramental Steel & Light",
        "video_url": "/static/media/cutscenes/sacramental_bond.mp4",
        "classification": "Diocesan Rite Log #042",
        "description": "Roman De La Croix seals the Co-Link bond, channeling golden holy light to interlock their spiritual frequencies."
    },
    "masquerade-shatter": {
        "id": "masquerade-shatter",
        "title": "V. The Shattered Chalice",
        "subtitle": "Balcony at the Grand Masquerade",
        "video_url": "/static/media/cutscenes/masquerade_shatter.mp4",
        "classification": "Perimeter Surveillance Feed",
        "description": "Watching from the balcony during the masquerade, Roman grips his champagne flute until the glass shatters."
    }
}

@router.get("/", response_class=HTMLResponse)
async def render_cinematics_gallery(request: Request):
    """Renders the main Cinematics Gallery Page."""
    return templates.TemplateResponse(
        request=request,
        name="pages/cinematics.html",
        context={
            "page_title": "Cinematic Archives | The Reform School for Witches",
            "meta_description": "Stream official animated cutscenes from The Reform School for Witches Series (rsfwseries.com).",
            "cutscenes": list(CUTSCENE_DB.values())
        }
    )

@router.get("/cutscene/{scene_id}", response_class=HTMLResponse)
async def get_cutscene_modal(request: Request, scene_id: str):
    """Returns the HTMX video player modal overlay."""
    scene = CUTSCENE_DB.get(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Cinematic record missing.")

    return templates.TemplateResponse(
        request=request,
        name="components/cutscene_modal.html",
        context={"scene": scene}
    )