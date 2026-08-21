from typing import List, Optional
from pydantic import BaseModel

class ScriptChoice(BaseModel):
    id: str
    text: str
    next_node_id: str
    sanctity_delta: int = 0
    corruption_delta: int = 0
    archetype_affinity: Optional[str] = None

class ScriptNode(BaseModel):
    node_id: str
    speaker: str
    speaker_title: Optional[str] = None
    portrait_url: Optional[str] = None
    background_url: str
    dialogue: str
    choices: List[ScriptChoice]
    unlock_media_id: Optional[str] = None

SCRIPT_NODES: dict[str, ScriptNode] = {
    # ------------------------------------------------------------------
    # ACT I: THE SALT LINE
    # ------------------------------------------------------------------
    "node_001": ScriptNode(
        node_id="node_001",
        speaker="Roman De La Croix",
        speaker_title="Perimeter Marshal",
        portrait_url="/static/media/dossiers/roman.jpg",
        background_url="/static/media/dossiers/bg_courtyard.jpg",
        dialogue="The river fog is heavy tonight. Step across the salt line before the broadcast signal catches your trailing frequency. Once you cross, the Crimson Root loses your trace.",
        choices=[
            ScriptChoice(
                id="c1",
                text="Step across the salt barrier and invoke the Holy Name.",
                next_node_id="node_002_salt",
                sanctity_delta=35,
                corruption_delta=0,
                archetype_affinity="The Sentinel Shield"
            ),
            ScriptChoice(
                id="c2",
                text="Listen closely to the high-frequency hum calling from the swamp.",
                next_node_id="node_002_listen",
                sanctity_delta=0,
                corruption_delta=35,
                archetype_affinity="The Sanguine Initiate"
            ),
            ScriptChoice(
                id="c3",
                text="Reach for Roman's arm to lock Co-Link frequencies.",
                next_node_id="node_002_colink",
                sanctity_delta=25,
                corruption_delta=0,
                archetype_affinity="The Co-Link Partner"
            )
        ]
    ),

    # ------------------------------------------------------------------
    # BRANCH A: THE SACRED SENTRY
    # ------------------------------------------------------------------
    "node_002_salt": ScriptNode(
        node_id="node_002_salt",
        speaker="Ignatius Santiago",
        speaker_title="Penitent Sentry",
        portrait_url="/static/media/dossiers/ignatius.jpg",
        background_url="/static/media/dossiers/bg_perimeter.jpg",
        dialogue="Firm footing. The iron gates of Our Lady of Tears only hold if those inside know how to anchor themselves. The sanctuary lamp burns in the north tower—Father Manuel awaits.",
        choices=[
            ScriptChoice(
                id="c1_1",
                text="Proceed directly to Father Manuel in the North Tower.",
                next_node_id="node_003_manuel",
                sanctity_delta=35,
                corruption_delta=0
            ),
            ScriptChoice(
                id="c1_2",
                text="Inspect the salt line perimeter with Ignatius first.",
                next_node_id="node_003_sentry_patrol",
                sanctity_delta=30,
                corruption_delta=0
            )
        ]
    ),
    "node_003_manuel": ScriptNode(
        node_id="node_003_manuel",
        speaker="Father Manuel",
        speaker_title="Rector & Chief Exorcist",
        portrait_url="/static/media/dossiers/manuel.jpg",
        background_url="/static/media/dossiers/bg_chapel.jpg",
        dialogue="Welcome to the Sanctuary. You carry the static of the outer world, but here, the Sacramental Seal covers all debts. Are you prepared to take the Sponsor's Vow?",
        choices=[
            ScriptChoice(
                id="c_m1",
                text="Kneel before the Eucharistic Altar and take the sacred Vow.",
                next_node_id="node_004_sanctified_end",
                sanctity_delta=30,
                corruption_delta=0
            ),
            ScriptChoice(
                id="c_m2",
                text="Ask Father Manuel about the true cost of Kimbra's Emergency Baptism.",
                next_node_id="node_003_colink",
                sanctity_delta=15,
                corruption_delta=0
            )
        ]
    ),
    "node_003_sentry_patrol": ScriptNode(
        node_id="node_003_sentry_patrol",
        speaker="Ignatius Santiago",
        speaker_title="Penitent Sentry",
        portrait_url="/static/media/dossiers/ignatius.jpg",
        background_url="/static/media/dossiers/bg_perimeter.jpg",
        dialogue="Look out into the brine moat. Damian's siphons are pressing hard against our southern boundary. Without a strong Chalice and Shield co-link, these salt lines won't survive the harvest season.",
        choices=[
            ScriptChoice(
                id="c_p1",
                text="Strengthen the defensive salt line using the Crown of Tears Rosary.",
                next_node_id="node_004_sanctified_end",
                sanctity_delta=35,
                corruption_delta=0
            ),
            ScriptChoice(
                id="c_p2",
                text="Return to Roman at the courtyard threshold.",
                next_node_id="node_001",
                sanctity_delta=0,
                corruption_delta=0
            )
        ]
    ),

    # ------------------------------------------------------------------
    # BRANCH B: THE SANGUINE PACT
    # ------------------------------------------------------------------
    "node_002_listen": ScriptNode(
        node_id="node_002_listen",
        speaker="Damian Boudreaux",
        speaker_title="The Crimson Heir",
        portrait_url="/static/media/dossiers/damian.jpg",
        background_url="/static/media/dossiers/bg_archivist.jpg",
        dialogue="You feel the pull of the Crimson Root, don't you? The salt is a cage designed by frightened old men. The Sanguine Tether is not a curse—it is an eternal inheritance.",
        choices=[
            ScriptChoice(
                id="c2_1",
                text="Accept the graft line and offer your vitality to the Boudreaux dynasty.",
                next_node_id="node_003_damian_pact",
                sanctity_delta=0,
                corruption_delta=35
            ),
            ScriptChoice(
                id="c2_2",
                text="Demand to see the Livre de la Racine ledger before making a choice.",
                next_node_id="node_003_ledger",
                sanctity_delta=0,
                corruption_delta=25
            )
        ]
    ),
    "node_003_damian_pact": ScriptNode(
        node_id="node_003_damian_pact",
        speaker="Damian Boudreaux",
        speaker_title="The Crimson Heir",
        portrait_url="/static/media/dossiers/damian.jpg",
        background_url="/static/media/dossiers/bg_archivist.jpg",
        dialogue="Delicious. The biological graft locks into place. You are no longer bound by weak mortal decay. Together, we will bleed the Academy's defenses dry.",
        choices=[
            ScriptChoice(
                id="c_d1",
                text="Seize full control of the Crimson Root network.",
                next_node_id="node_004_corrupted_end",
                sanctity_delta=0,
                corruption_delta=30
            )
        ]
    ),
    "node_003_ledger": ScriptNode(
        node_id="node_003_ledger",
        speaker="Genesis",
        speaker_title="Tactical Disruptor",
        portrait_url="/static/media/dossiers/genesis.jpg",
        background_url="/static/media/dossiers/bg_vault.jpg",
        dialogue="Shh! Keep your voice low. I'm intercepting Vincent Boudreaux's ledger transmissions. If you touch that ledger without scrambling your frequency, Damian will harvest your soul in six seconds flat.",
        choices=[
            ScriptChoice(
                id="c_g1",
                text="Help Genesis scramble the Crimson Root signal.",
                next_node_id="node_002_salt",
                sanctity_delta=30,
                corruption_delta=0
            ),
            ScriptChoice(
                id="c_g2",
                text="Bypass Genesis and take the ledger for yourself.",
                next_node_id="node_003_damian_pact",
                sanctity_delta=0,
                corruption_delta=40
            )
        ]
    ),

    # ------------------------------------------------------------------
    # BRANCH C: THE CO-LINK CIRCUIT
    # ------------------------------------------------------------------
    "node_002_colink": ScriptNode(
        node_id="node_002_colink",
        speaker="Kimbra Woods",
        speaker_title="Consecrated Vessel",
        portrait_url="/static/media/dossiers/kimbra.jpg",
        background_url="/static/media/dossiers/bg_chapel.jpg",
        dialogue="Your spiritual resonance flares when you lock in like that. Keep your interior doors locked—the light in this courtyard burns hot, but the darkness outside is starving.",
        choices=[
            ScriptChoice(
                id="c3_1",
                text="Stand beside Kimbra in the sanctuary and ground the energy.",
                next_node_id="node_003_manuel",
                sanctity_delta=40,
                corruption_delta=0
            ),
            ScriptChoice(
                id="c3_2",
                text="Ask Kimbra how she severed her tether from Damian.",
                next_node_id="node_003_kimbra_story",
                sanctity_delta=35,
                corruption_delta=0
            )
        ]
    ),
    "node_003_kimbra_story": ScriptNode(
        node_id="node_003_kimbra_story",
        speaker="Kimbra Woods",
        speaker_title="Consecrated Vessel",
        portrait_url="/static/media/dossiers/kimbra.jpg",
        background_url="/static/media/dossiers/bg_chapel.jpg",
        dialogue="It was the Emergency Baptism in the White Room. When Father Manuel poured the holy water, my scar burned like molten silver. The tether snapped, and for the first time in ten years... I could breathe.",
        choices=[
            ScriptChoice(
                id="c_k1",
                text="Reaffirm your devotion to protecting Kimbra and the Academy.",
                next_node_id="node_004_sanctified_end",
                sanctity_delta=40,
                corruption_delta=0
            )
        ]
    ),

    # ------------------------------------------------------------------
    # ACT II: ACT CLIMAXES
    # ------------------------------------------------------------------
    "node_004_sanctified_end": ScriptNode(
        node_id="node_004_sanctified_end",
        speaker="Father Manuel",
        speaker_title="Rector & Chief Exorcist",
        portrait_url="/static/media/dossiers/manuel.jpg",
        background_url="/static/media/dossiers/bg_chapel.jpg",
        dialogue="The Sacramental Shield stands firm. Your spirit is anchored in the Kingdom, and no Sanguine Tether can claim you. You are officially an Exception of Our Lady of Tears.",
        choices=[
            ScriptChoice(
                id="c_reset_1",
                text="[ RE-ENTER THE ARCHIVES :: RESTART INTERACTIVE PATH ]",
                next_node_id="node_001",
                sanctity_delta=0,
                corruption_delta=0
            )
        ]
    ),
    "node_004_corrupted_end": ScriptNode(
        node_id="node_004_corrupted_end",
        speaker="Damian Boudreaux",
        speaker_title="The Crimson Heir",
        portrait_url="/static/media/dossiers/damian.jpg",
        background_url="/static/media/dossiers/bg_archivist.jpg",
        dialogue="The salt line crumbles. The Crimson Root has claimed another soul for the Boudreaux ledger. You are tethered to the Hearth forever.",
        choices=[
            ScriptChoice(
                id="c_reset_2",
                text="[ RE-ENTER THE ARCHIVES :: RESTART INTERACTIVE PATH ]",
                next_node_id="node_001",
                sanctity_delta=0,
                corruption_delta=0
            )
        ]
    )
}

def get_script_node(node_id: str) -> Optional[ScriptNode]:
    """Retrieves a script node by its unique node_id string."""
    return SCRIPT_NODES.get(node_id)