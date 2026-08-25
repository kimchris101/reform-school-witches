from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.utils.auth import is_authenticated_session

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
        "description": "Inside Roman's nightmare. Taunted by Amira, Roman watches Kimbra & Damian from the balcony, He grips his champagne flute until the glass shatters."
    }
}


@router.get("/", response_class=HTMLResponse)
async def render_cinematics_gallery(request: Request):
    """Renders the Cinematics Gallery with authentication awareness."""
    is_authenticated = is_authenticated_session(request)

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
    """Returns the video modal or blocks non-verified initiates with a modal warning."""
    if not is_authenticated_session(request):
        return HTMLResponse(
            content="""
            <div id="modal-container" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-md animate-fade-in font-mono">
                <div class="bg-archive-card border border-blood-900/80 w-full max-w-md p-6 rounded shadow-[0_0_50px_rgba(163,15,46,0.3)] text-center space-y-4">
                    <div class="text-blood-500 font-bold text-xs uppercase tracking-widest">✝ ACCESS RESTRICTED :: EMAIL VERIFICATION REQUIRED ✝</div>
                    <h3 class="text-lg font-gothic text-parchment-100 uppercase font-bold">Classified Surveillance Feed</h3>
                    <p class="text-xs text-parchment-200 leading-relaxed font-serif">
                        Streaming access to animated cutscene archives requires a verified email session passcode.
                    </p>
                    <div class="pt-2 flex flex-col gap-2">
                        <button onclick="document.getElementById('modal-container').remove(); document.getElementById('register-modal').classList.remove('hidden');" 
                                class="w-full bg-blood-900 hover:bg-blood-800 text-parchment-100 py-2.5 text-xs uppercase tracking-wider font-bold transition-colors border border-blood-700">
                            Enter 6-Digit Passcode / Request Code
                        </button>
                        <button onclick="document.getElementById('modal-container').remove()" 
                                class="text-archive-muted hover:text-parchment-100 py-1 uppercase text-[10px]">
                            DISMISS
                        </button>
                    </div>
                </div>
            </div>
            """,
            status_code=200
        )

    scene = CUTSCENE_DB.get(scene_id)
    if not scene:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cinematic record missing.")

    return templates.TemplateResponse(
        request=request,
        name="components/cutscene_modal.html",
        context={"scene": scene}
    )