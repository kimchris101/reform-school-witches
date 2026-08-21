from typing import List, Optional
from pydantic import BaseModel

class ScriptChoice(BaseModel):
    id: str
    text: str
    next_node_id: str
    sanctity_delta: int = 0      # Points added toward Sacramental Sanctity
    corruption_delta: int = 0    # Points added toward Sanguine Corruption
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

# Script Registry using canonical Crimson Root lore
SCRIPT_NODES: dict[str, ScriptNode] = {
    "node_001": ScriptNode(
        node_id="node_001",
        speaker="Roman De La Croix",
        speaker_title="Perimeter Marshal",
        portrait_url="/static/media/dossiers/roman.jpg",
        background_url="/static/media/bg_courtyard.jpg",
        dialogue="The river fog is heavy tonight. Step across the salt line before the broadcast signal catches your trailing frequency. Once you cross, the Crimson Root loses your trace.",
        choices=[
            ScriptChoice(
                id="c1",
                text="Step across the salt barrier and invoke the Holy Name.",
                next_node_id="node_002_salt",
                sanctity_delta=15,
                corruption_delta=0,
                archetype_affinity="The Sentinel Shield"
            ),
            ScriptChoice(
                id="c2",
                text="Listen closely to the high-frequency hum calling from the swamp.",
                next_node_id="node_002_listen",
                sanctity_delta=0,
                corruption_delta=15,
                archetype_affinity="The Sanguine Initiate"
            ),
            ScriptChoice(
                id="c3",
                text="Reach for Roman's arm to lock Co-Link frequencies.",
                next_node_id="node_002_colink",
                sanctity_delta=10,
                corruption_delta=0,
                archetype_affinity="The Co-Link Partner"
            )
        ]
    ),
    "node_002_salt": ScriptNode(
        node_id="node_002_salt",
        speaker="Ignatius Santiago",
        speaker_title="Penitent Sentry",
        portrait_url="/static/media/dossiers/ignatius.jpg",
        background_url="/static/media/bg_perimeter.jpg",
        dialogue="Firm footing. The iron gates of Our Lady of Tears only hold if those inside know how to anchor themselves. Follow me to the Archivist tower.",
        choices=[
            ScriptChoice(
                id="c1_sub",
                text="Follow Ignatius into the inner courtyard.",
                next_node_id="node_001",
                sanctity_delta=5,
                corruption_delta=0
            )
        ]
    ),
    "node_002_listen": ScriptNode(
        node_id="node_002_listen",
        speaker="Damian Boudreaux",
        speaker_title="The Crimson Heir",
        portrait_url="/static/media/dossiers/damian.jpg",
        background_url="/static/media/bg_archivist.jpg",
        dialogue="You feel the pull of the Crimson Root, don't you? The salt is a cage. The tether is a gift.",
        choices=[
            ScriptChoice(
                id="c2_sub",
                text="Resist the whisper and retreat to the gate.",
                next_node_id="node_001",
                sanctity_delta=10,
                corruption_delta=-5
            )
        ]
    ),
    "node_002_colink": ScriptNode(
        node_id="node_002_colink",
        speaker="Kimbra Woods",
        speaker_title="Consecrated Vessel",
        portrait_url="/static/media/dossiers/kimbra.jpg",
        background_url="/static/media/bg_chapel.jpg",
        dialogue="Your spiritual resonance flares when you lock in like that. Keep your interior doors locked—the light in this courtyard burns hot.",
        choices=[
            ScriptChoice(
                id="c3_sub",
                text="Proceed together toward the chapel sanctuary.",
                next_node_id="node_001",
                sanctity_delta=10,
                corruption_delta=0
            )
        ]
    )
}

def get_script_node(node_id: str) -> Optional[ScriptNode]:
    return SCRIPT_NODES.get(node_id)