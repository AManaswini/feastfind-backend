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


class CatererCreate(BaseModel):
    name: str
    emoji: Optional[str] = "🍽️"
    rating: Optional[float] = 0.0
    reviews: Optional[int] = 0
    cuisines: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    price_display: Optional[str] = ""
    price_min: Optional[int] = 0
    price_max: Optional[int] = 0
    price_note: Optional[str] = ""
    min_guests: Optional[int] = 1
    max_guests: Optional[int] = 500
    location: Optional[str] = ""
    phone: Optional[str] = ""
    email: Optional[str] = ""
    verified: Optional[bool] = False
    description: Optional[str] = ""
    specialties: Optional[List[str]] = []
    menu: Optional[List[str]] = []
    photos_count: Optional[int] = 0
    match_keywords: Optional[List[str]] = []


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


# ── User Auth ──────────────────────────────────────────────────
class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    token: str
    email: str
    is_admin: bool


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
