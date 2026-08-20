from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def render_industry_portal(request: Request):
    """Renders the executive pitch deck and character arc overview."""
    return templates.TemplateResponse(
        request=request,
        name="pages/industry.html",
        context={
            "page_title": "Industry & Production Portal | The Reform School for Witches",
            "meta_description": "Series overview, pitch materials, demographic metrics, and multi-season character transformation arcs for executive partners.",
            "seasons": [
                {
                    "number": "Season 1",
                    "subtitle": "The Sanguine Contract",
                    "role": "Tragic Antagonist & Siphon",
                    "focus": "Damian operates as a seductive, lethal weapon for the Crimson Root, tethered by an ancestral blood debt until the South Ramparts collision."
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
                    "role": "Redeemed Soldier & Co-Link",
                    "focus": "Awakening with latent holy stigmata, Damian joins Roman and Kimbra as a wounded, high-risk anchor in the fight against the forces of darkness."
                }
            ]
        }
    )