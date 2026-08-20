from typing import List, Optional
from pydantic import BaseModel

class ScriptChoice(BaseModel):
    id: str
    text: str
    next_node_id: str
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

# Mock Visual Novel Branching Node Registry
SCRIPT_NODES: dict[str, ScriptNode] = {
    "node_001": ScriptNode(
        node_id="node_001",
        speaker="Roman De La Croix",
        speaker_title="Perimeter Marshal",
        portrait_url="/static/media/dossiers/roman.jpg",
        background_url="/static/media/bg_courtyard.jpg",
        dialogue="The fog off the river is heavy tonight. Step across the salt line before the broadcast signal catches your trailing frequency. Once you cross this boundary, the Sanguine Coven loses your trace.",
        choices=[
            ScriptChoice(
                id="c1",
                text="Step across the salt barrier immediately.",
                next_node_id="node_002_salt",
                archetype_affinity="The Sentinel Shield"
            ),
            ScriptChoice(
                id="c2",
                text="Check your pulse and listen for high-frequency feedback.",
                next_node_id="node_002_listen",
                archetype_affinity="The Sonic Scrambler"
            ),
            ScriptChoice(
                id="c3",
                text="Reach for Roman's arm to lock frequencies.",
                next_node_id="node_002_colink",
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
        dialogue="Firm footing. Good. The iron gates of Our Lady of Tears only hold if those inside know how to anchor themselves. Follow me to the Archivist tower.",
        choices=[
            ScriptChoice(
                id="c1_sub",
                text="Follow Ignatius into the inner courtyard.",
                next_node_id="node_001"  # Loops back for testing
            )
        ]
    ),
    "node_002_listen": ScriptNode(
        node_id="node_002_listen",
        speaker="Genesis",
        speaker_title="Tactical Disruptor",
        portrait_url="/static/media/dossiers/genesis.jpg",
        background_url="/static/media/bg_archivist.jpg",
        dialogue="You hear that faint high-pitched whine too, don't you? That's a low-orbit coven scanner. Hold still while I activate the scrambler frequency.",
        choices=[
            ScriptChoice(
                id="c2_sub",
                text="Assist Genesis with the signal override.",
                next_node_id="node_001"
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
                next_node_id="node_001"
            )
        ]
    )
}

def get_script_node(node_id: str) -> Optional[ScriptNode]:
    return SCRIPT_NODES.get(node_id)