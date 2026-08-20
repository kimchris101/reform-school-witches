from typing import List, Optional, Dict
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field

class ArchetypeEnum(str, Enum):
    CO_LINK_PARTNER = "The Co-Link Partner"
    MARY_CHALICE = "Mary / The Chalice"
    THE_CHALICE = "Mary / The Chalice"
    SONIC_SCRAMBLER = "The Sonic Scrambler"
    THE_SONIC_SCRAMBLER = "The Sonic Scrambler"
    SENTINEL_SHIELD = "The Sentinel Shield"
    THE_SENTINEL_SHIELD = "The Sentinel Shield"

class ClinicalStatus(BaseModel):
    heart_rate: str = "42 BPM (Arrhythmic)"
    brainwave_resonance: str = "Deep Sleep / Sub-Spiritual Activity"
    diagnostic_note: str = "Residual scars on wrists & side show abnormal cellular regeneration."
    threat_assessment: str = "Dormant. Do not attempt ungrounded contact."

class ProducerArc(BaseModel):
    archetype: str
    selling_point: str
    season_breakdown: Dict[str, str]

class CharacterDossier(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    slug: str
    full_name: str
    alias: Optional[str] = None
    patron_saint: str
    sacramental_affinity: str
    classification_class: str
    biography: str
    key_quotes: List[str]
    portrait_url: str
    voice_sample_url: Optional[str] = None
    is_spoiler: bool = False
    clinical_status: Optional[ClinicalStatus] = None
    producer_arc: Optional[ProducerArc] = None

class QuizAnswer(BaseModel):
    question_id: int
    selected_option: str

class QuizSubmission(BaseModel):
    user_email: str
    user_alias: str
    answers: List[QuizAnswer]

class DiocesanLetter(BaseModel):
    recipient_name: str
    archetype: ArchetypeEnum
    diocesan_seal_code: str
    classification_class: str
    patron_example: str
    file_summary: str
    warning_notice: str

class AssessmentResult(BaseModel):
    archetype: ArchetypeEnum
    diocesan_letter: DiocesanLetter

# Alias required by app/services/scoring.py
QuizResultResponse = AssessmentResult