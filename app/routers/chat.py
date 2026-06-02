# app/routers/chat.py
# Pure rule-based chat — no Anthropic API key required.
# Parses user messages with keyword extraction and runs the matcher engine.

import re
from fastapi import APIRouter, Depends
from app.db.database import get_db
from app.schemas.caterer import ChatRequest, ChatResponse, MatchedCaterer
from app.models.matcher import get_db_recommendations

router = APIRouter(prefix="/chat", tags=["Chat"])

# ── Keyword extractors ────────────────────────────────────────────

CUISINE_KEYWORDS = {
    "telugu":       "Telugu",
    "south indian": "South Indian",
    "north indian": "North Indian",
    "punjabi":      "North Indian",
    "mughlai":      "Mughlai",
    "multi":        "Multi Cuisine",
    "vegan":        "Vegan",
    "chinese":      "Chinese",
    "continental":  "Continental",
}

DIETARY_KEYWORDS = {
    "vegetarian": "vegetarian",
    "veg":        "vegetarian",
    "non-veg":    "non-veg",
    "nonveg":     "non-veg",
    "chicken":    "non-veg",
    "mutton":     "non-veg",
    "meat":       "non-veg",
    "vegan":      "vegan",
    "jain":       "jain",
}

EVENT_KEYWORDS = {
    "wedding":    "wedding",
    "engagement": "engagement",
    "birthday":   "birthday",
    "corporate":  "corporate",
    "religious":  "religious",
    "house party":"house_party",
    "housewarming":"house_party",
    "baby shower":"baby_shower",
}

SPECIAL_KEYWORDS = [
    "live dosa", "dosa counter", "live counter", "chaat", "pani puri",
    "elder", "elder-friendly", "gluten", "nut-free",
]

BAY_AREA_CITIES = [
    "san jose", "sunnyvale", "santa clara", "fremont",
    "milpitas", "cupertino", "mountain view", "palo alto",
]


def _extract_info(text: str) -> dict:
    """Extract structured event info from raw user text."""
    t = text.lower()
    info = {}

    # Guest count — look for numbers near guest/people/person/pax
    guest_match = re.search(
        r'(\d+)\s*(?:guests?|people|persons?|pax|attendees?)', t
    )
    if not guest_match:
        guest_match = re.search(r'(?:for|around|about)\s+(\d+)', t)
    if guest_match:
        info["guest_count"] = int(guest_match.group(1))

    # Budget — look for $ amounts
    budget_match = re.search(r'\$\s*(\d+(?:,\d+)?(?:\.\d+)?)', t)
    if budget_match:
        raw = int(budget_match.group(1).replace(",", ""))
        # Heuristic: if >500 treat as total budget, estimate per plate
        if raw > 500 and info.get("guest_count"):
            info["budget_per_plate"] = raw // info["guest_count"]
        elif raw <= 100:
            info["budget_per_plate"] = raw
        else:
            info["budget_per_plate"] = raw

    # Cuisine
    for kw, label in CUISINE_KEYWORDS.items():
        if kw in t:
            info["cuisine"] = label
            break

    # Dietary
    for kw, label in DIETARY_KEYWORDS.items():
        if kw in t:
            info["dietary"] = label
            break

    # Event type
    for kw, label in EVENT_KEYWORDS.items():
        if kw in t:
            info["event_type"] = label
            break

    # Location
    for city in BAY_AREA_CITIES:
        if city in t:
            info["location"] = city.title()
            break

    # Special requests
    found = [kw for kw in SPECIAL_KEYWORDS if kw in t]
    if found:
        info["special_requests"] = ", ".join(found)

    return info


def _merge_info(history: list) -> dict:
    """Accumulate extracted info across all user messages."""
    merged = {}
    for msg in history:
        if msg["role"] == "user":
            extracted = _extract_info(msg["content"])
            merged.update({k: v for k, v in extracted.items() if v})
    return merged


def _missing_fields(info: dict) -> list:
    """Return list of key fields still needed."""
    missing = []
    if not info.get("guest_count"):
        missing.append("guest_count")
    if not info.get("cuisine") and not info.get("dietary"):
        missing.append("cuisine")
    return missing


FOLLOW_UP_QUESTIONS = {
    "guest_count": "How many guests are you expecting? 😊",
    "cuisine":     "What cuisine are you thinking — Telugu, South Indian, North Indian, or something else?",
    "budget":      "Do you have a rough budget in mind (total or per plate)?",
}

GREETING = (
    "Hi! I'm FeastFind AI 🌿 Tell me about your event and "
    "I'll find the perfect caterers for you! You can say something like: "
    "\"150 guests, Telugu engagement in San Jose, vegetarian with live dosa counter.\""
)


def _build_reply(info: dict, missing: list, is_first: bool) -> str:
    if is_first:
        return GREETING

    if missing:
        field = missing[0]
        ack = ""
        if info.get("event_type"):
            ack = f"Got it — {info['event_type'].replace('_', ' ')}! "
        elif info.get("guest_count"):
            ack = f"Great, {info['guest_count']} guests! "
        return ack + FOLLOW_UP_QUESTIONS.get(field, "Can you tell me more about your event?")

    # We have enough info — confirm and say results are ready
    parts = []
    if info.get("event_type"):
        parts.append(info["event_type"].replace("_", " ").title())
    if info.get("guest_count"):
        parts.append(f"{info['guest_count']} guests")
    if info.get("cuisine"):
        parts.append(info["cuisine"])
    if info.get("dietary"):
        parts.append(info["dietary"])
    if info.get("location"):
        parts.append(info["location"])

    summary = " · ".join(parts)
    return f"Perfect! Here's what I found for your {summary} event:"


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest, db=Depends(get_db)):
    messages = [m.model_dump() for m in payload.messages]
    is_first  = all(m["role"] != "user" for m in messages)

    info    = _merge_info(messages)
    missing = _missing_fields(info)
    reply   = _build_reply(info, missing, is_first)

    recommendations = None
    if not missing and info:
        query_text = " ".join(
            m["content"] for m in messages if m["role"] == "user"
        )
        matched = await get_db_recommendations(query_text, info, db, top_n=4)
        recommendations = [MatchedCaterer(**c) for c in matched]

    return ChatResponse(
        reply=reply,
        extracted_info=info if info else None,
        recommendations=recommendations,
    )
