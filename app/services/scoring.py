from typing import List, Dict
from uuid import uuid4
from app.models.schemas import QuizAnswer, ArchetypeEnum, DiocesanLetter, QuizResultResponse

# Direct mapping for the 5 Intake Questions
OPTION_TO_ARCHETYPE: Dict[str, ArchetypeEnum] = {
    "A": ArchetypeEnum.CO_LINK_PARTNER,
    "B": ArchetypeEnum.THE_CHALICE,
    "C": ArchetypeEnum.SONIC_SCRAMBLER,
    "D": ArchetypeEnum.SENTINEL_SHIELD,
}

ARCHETYPE_DETAILS: Dict[ArchetypeEnum, Dict[str, str]] = {
    ArchetypeEnum.CO_LINK_PARTNER: {
        "class": "Co-Link Conduit / High Rite Specialist",
        "patron": "Roman De la Croix / St. Michael",
        "summary": "You possess a rare, symphonic resonance. You do not fight the dark alone; you are forged to stand alongside another, channeling the mass of the One Soul to turn two heartbeats into an unbreakable circuit.",
        "warning": "Beware of symphonic overload. Never allow your fondness to become a crack in the wall."
    },
    ArchetypeEnum.THE_CHALICE: {
        "class": "Consecrated Vessel / Exception",
        "patron": "Kimbra Woods (Mary) / Our Lady of Tears",
        "summary": "You were target-marked because of your extraordinary purity and capacity to hold light. Though the adversary attempted to make you a battery for their legacy, the Sacrament has sealed your temple forever. You are the flame; others are the wall.",
        "warning": "Keep your interior doors locked. Re-examine your mind daily for hidden wires."
    },
    ArchetypeEnum.SONIC_SCRAMBLER: {
        "class": "Tactical Disruptor / Free Conduits",
        "patron": "Genesis / St. Cecilia",
        "summary": "You know the lure of the occult because you once left your own door unlocked. Having been delivered from the noise, you now use fractured dissonance to scramble enemy broadcasts and break the coven's tracking signals.",
        "warning": "A scramble without a seal is a live wire. Do not mistake defiance for spiritual armor."
    },
    ArchetypeEnum.SENTINEL_SHIELD: {
        "class": "Perimeter Guard / Penitent Sentry",
        "patron": "Ignatius Santiago / St. James the Greater",
        "summary": "You stand at the Outer Perimeter where the rock meets the mire. You carry yourself with the quiet density of an anvil, taking the heat of the enemy’s discharge into your own bones so others can remain standing.",
        "warning": "A Shield is a barrier, not a destination. Do not let your penance turn your heart to stone."
    }
}

def evaluate_intake_exam(user_alias: str, answers: List[QuizAnswer]) -> QuizResultResponse:
    scores: Dict[ArchetypeEnum, int] = {archetype: 0 for archetype in ArchetypeEnum}
    
    # Calculate scores based on user choices
    for ans in answers:
        archetype = OPTION_TO_ARCHETYPE.get(ans.selected_option.upper())
        if archetype:
            scores[archetype] += 1

    # Determine dominant archetype (fallback to highest score tie-breaker)
    assigned_archetype = max(scores, key=scores.get)
    details = ARCHETYPE_DETAILS[assigned_archetype]
    seal_code = f"OLT-SEAL-{uuid4().hex[:8].upper()}"

    diocesan_letter = DiocesanLetter(
        recipient_name=user_alias,
        archetype=assigned_archetype,
        classification_class=details["class"],
        patron_example=details["patron"],
        diocesan_seal_code=seal_code,
        file_summary=details["summary"],
        warning_notice=details["warning"]
    )

    return QuizResultResponse(
        submission_id=uuid4(),
        user_alias=user_alias,
        archetype=assigned_archetype,
        scores={k.value: v for k, v in scores.items()},
        diocesan_letter=diocesan_letter
    )