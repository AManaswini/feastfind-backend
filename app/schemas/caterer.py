# app/schemas/caterer.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class CatererSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    emoji: str
    rating: float
    reviews: int
    cuisines: List[str]
    tags: List[str]
    price_display: str
    price_min: int
    price_max: int
    min_guests: int
    location: str
    verified: bool
    photos_count: int


class CatererDetail(CatererSummary):
    price_note: str
    max_guests: int
    phone: str
    email: str
    description: str
    specialties: List[str]
    menu: List[str]


class MatchedCaterer(CatererSummary):
    match_score: int  # 0–100


# ── Inquiry ────────────────────────────────────────────────────
class InquiryCreate(BaseModel):
    caterer_id: int
    name: str
    phone: Optional[str] = None
    email: str
    notes: Optional[str] = None
    event_type: Optional[str] = None
    guest_count: Optional[int] = None
    budget: Optional[str] = None


class InquiryOut(InquiryCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str = "pending"


# ── Chat ───────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    role: str   # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: str
    extracted_info: Optional[dict] = None
    recommendations: Optional[List[MatchedCaterer]] = None
