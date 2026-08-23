from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Request, HTTPException, status, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models.schemas import CharacterDossier, ClinicalStatus, ProducerArc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

CHARACTER_DB: dict[str, CharacterDossier] = {
    "roman-de-la-croix": CharacterDossier(
        id=uuid4(),
        slug="roman-de-la-croix",
        full_name="Roman De La Croix",
        alias="The Co-Link Conduit",
        patron_saint="St. Michael the Archangel",
        sacramental_affinity="Symphonic Resonance & Sacramental Steel",
        classification_class="High Rite Shield / Perimeter Marshal",
        current_location="Rector's Office",
        biography="Forged in the crucible of the New Orleans Diocesan Tribunal, Roman acts as the primary anchor for High Rite exorcisms. His soul operates as a high-capacity conduit, capable of interlocking spiritual frequencies with a partner to form an unbreakable barrier against demonic broadcast signals.",
        key_quotes=[
            "Two heartbeats, one circuit. The dark cannot break what is held in common.",
            "Keep your feet in the salt and your eyes on the altar."
        ],
        portrait_url="/static/media/dossiers/roman.jpg",
        is_spoiler=False
    ),
    "kimbra-woods": CharacterDossier(
        id=uuid4(),
        slug="kimbra-woods",
        full_name="Kimbra Woods",
        alias="Mary / The Chalice",
        patron_saint="Our Lady of Tears",
        sacramental_affinity="Consecrated Light & Unbroken Vessels",
        classification_class="Consecrated Vessel / Exception",
        current_location="Our Lady of Tears Chapel",
        biography="Sold to the Crimson Root as a child due to her uncorrupted spiritual purity, Kimbra was intended to serve as a power source for an ancestral blood debt. Sealed by the Sacrament at Our Lady of Tears Academy, she has been gifted a raw holy illumination, serving as the flame around which the Academy's perimeter walls are sustained.",
        key_quotes=[
            "They tried to turn my heart into a battery. They forgot that Light consumes the wires.",
            "My interior doors remain locked."
        ],
        portrait_url="/static/media/dossiers/kimbra.jpg",
        is_spoiler=False
    ),
    "genesis": CharacterDossier(
        id=uuid4(),
        slug="genesis",
        full_name="Genesis",
        alias="The Sonic Scrambler",
        patron_saint="St. Cecilia",
        sacramental_affinity="Acoustic Dissonance & Signal Interruption",
        classification_class="Tactical Disruptor / Free Conduits",
        current_location="High Yard",
        biography="A prodigal daughter of the Catholic Church, dabbled in the occult and was left screaming in a mental health facility. The Rector, Father Manuel and his team exorcised the demon afflicting her and she chose to enter the Academy for reform. As a fractured frequency she learned to scramble the enemy's signal.",
        key_quotes=[
            "If they can't lock onto your frequency, they can't harvest your marrow.",
            "Noise is just a prayer that hasn't found its cadence yet."
        ],
        portrait_url="/static/media/dossiers/genesis.jpg",
        is_spoiler=False
    ),
    "ignatius-santiago": CharacterDossier(
        id=uuid4(),
        slug="ignatius-santiago",
        full_name="Ignatius Santiago",
        alias="The Sentinel",
        patron_saint="St. James the Greater",
        sacramental_affinity="Granite Density & Sacramental Fortification",
        classification_class="Perimeter Guard / Penitent Sentry",
        current_location="Perimeter Guard House",
        biography="Standing guard at the outer salt line where the swamp meets the academy stone, Ignatius absorbs the physical discharge of malignant entities. Carrying an immense weight of penance, his body acts as a literal anvil, grounding lethal energetic strikes before they reach the inner courtyard.",
        key_quotes=[
            "Let the swamp take my boots before it touches the sanctuary.",
            "Stand firm. The salt does not yield."
        ],
        portrait_url="/static/media/dossiers/ignatius.jpg",
        is_spoiler=False
    ),
    "damian-boudreaux": CharacterDossier(
        id=uuid4(),
        slug="damian-boudreaux",
        full_name="Damian Boudreaux",
        alias="The Legacy / Former Biological Siphon",
        patron_saint="St. Cyprian of Antioch (Latent)",
        sacramental_affinity="Crimson Siphon (Severed) / Latent Stigmata",
        classification_class="Restricted Case File #009 / Comatose (North Wing)",
        current_location="North Wing Infirmary (Vault 4)",
        biography="Following the catastrophic severance at the South Ramparts, Damian currently lies in a comatose state in the Academy Infirmary, stripped of the demonic entity but clinging to a thread of physical life.",
        key_quotes=[
            "He was a prince who had to die to his name to save his soul."
        ],
        portrait_url="/static/media/dossiers/damian.jpg",
        is_spoiler=False,
        clinical_status=ClinicalStatus(
            heart_rate="42 BPM (Arrhythmic)",
            brainwave_resonance="Deep Sleep / Sub-Spiritual Activity",
            diagnostic_note="Residual scars on wrists & side show abnormal cellular regeneration.",
            threat_assessment="Dormant. Do not attempt ungrounded contact."
        ),
        producer_arc=ProducerArc(
            archetype="The Redemptive Sinner / The Bad Boy Transformed",
            selling_point="Provides a compelling 3-season character transformation arc from tragic antagonist to stigmata-bearing warrior-exorcist.",
            season_breakdown={
                "Season 1": "Tragic, seductive antagonist tethered to the Sanguine Contract.",
                "Season 2": "Dark-night-of-the-soul recovery & awakening in the North Wing Vault.",
                "Season 3": "Wounded, stigmata-bearing warrior-exorcist fighting alongside Roman and Kimbra."
            }
        )
    )
}

@router.get("/", response_class=HTMLResponse)
async def render_dossiers_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/dossiers.html",
        context={
            "page_title": "Confidential Character Dossiers | Our Lady of Tears Academy",
            "meta_description": "Inspect the classified disciplinary files of Roman De La Croix, Kimbra Woods, Genesis, Ignatius Santiago, and Damian Boudreaux.",
            "characters": list(CHARACTER_DB.values())
        }
    )

@router.get("/easter-egg/cyprian", response_class=HTMLResponse)
async def get_cyprian_dossier(request: Request):
    """Returns the secret St. Cyprian file for subscribers or prompts registration for guests."""
    is_authenticated = request.cookies.get("rsfw_member_token") is not None

    if not is_authenticated:
        return templates.TemplateResponse(
            request=request,
            name="components/cyprian_locked.html",
            context={}
        )

    resp = templates.TemplateResponse(
        request=request,
        name="components/cyprian_dossier.html",
        context={}
    )
    resp.headers["HX-Trigger"] = "launchCyprianCutscene"
    return resp

@router.get("/{slug}", response_class=HTMLResponse)
async def get_dossier_modal(request: Request, slug: str, reveal_spoiler: Optional[bool] = False):
    character = CHARACTER_DB.get(slug)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character dossier not found in Diocesan archives."
        )

    return templates.TemplateResponse(
        request=request,
        name="components/dossier_modal.html",
        context={
            "character": character,
            "reveal_spoiler": reveal_spoiler
        }
    )