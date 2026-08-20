from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

INDUSTRY_PASSKEY = "SACRAMENTAL2026"  # Set your desired access code here


@router.get("/", response_class=HTMLResponse)
async def render_industry_portal(request: Request):
    """Renders the standard industry portal layout."""
    return templates.TemplateResponse(
        request=request,
        name="pages/industry.html",
        context={
            "page_title": "Industry & Production Portal | The Reform School for Witches",
            "meta_description": "Series overview, pitch materials, demographic metrics, and multi-season character transformation arcs for executive partners.",
            "authorized": False,
            "seasons": [
                {
                    "number": "Season 1",
                    "subtitle": "The Sanguine Contract",
                    "role": "Tragic Antagonist & Siphon",
                    "focus": "Damian operates as a seductive, lethal weapon for the Sanguine Coven, tethered by an ancestral blood debt until the South Ramparts collision."
                },
                {
                    "number": "Season 2",
                    "subtitle": "The North Wing Vault",
                    "role": "Comatose Penitent & Recovery",
                    "focus": "Severed from the entity, Damian lies in a mystic coma in the Academy infirmary while Roman and Kimbra defend his physical form from coven retrieval strikes."
                },
                {
                    "number": "Season 3",
                    "subtitle": "Stigmata Warrior",
                    "role": "Redeemed Exorcist & Co-Link",
                    "focus": "Awakening with latent holy stigmata, Damian joins Roman and Kimbra as a wounded, high-risk warrior-exorcist in high-rite tribunal actions."
                }
            ]
        }
    )


@router.post("/verify", response_class=HTMLResponse)
async def verify_industry_access(request: Request, passkey: str = Form(...)):
    """Verifies access code and returns the unlocked pitch deck or error fragment."""
    if passkey.strip().upper() != INDUSTRY_PASSKEY:
        return HTMLResponse(
            content='''
            <div id="passkey-error" class="text-xs font-mono text-blood-500 font-bold uppercase mt-2">
                ⛔ INVALID CLEARANCE CODE. ACCESS DENIED.
            </div>
            ''',
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    # Return HTMX redirect trigger upon successful code entry
    response = HTMLResponse(content="")
    response.headers["HX-Redirect"] = "/industry?access=granted"
    return response