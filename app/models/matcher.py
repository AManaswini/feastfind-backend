# app/models/matcher.py
from typing import List, Dict, Any, Optional
from app.data.seed import CATERERS


def score_caterer(caterer: Any, info: Dict[str, Any]) -> int:
    """Score a caterer 0–100 based on extracted event info. Works with dict or ORM object."""
    def _get(obj, key):
        return obj[key] if isinstance(obj, dict) else getattr(obj, key, None)

    score = 50
    keywords = _get(caterer, "match_keywords") or []
    cuisine  = (info.get("cuisine") or "").lower()
    dietary  = (info.get("dietary") or "").lower()
    requests = (info.get("special_requests") or "").lower()
    event    = (info.get("event_type") or "").lower()
    budget   = info.get("budget_per_plate")
    guests   = info.get("guest_count")

    combined_text = f"{cuisine} {dietary} {requests} {event}"
    matched = sum(1 for kw in keywords if kw in combined_text)
    score += matched * 8

    if guests:
        min_g = _get(caterer, "min_guests")
        max_g = _get(caterer, "max_guests")
        if min_g <= guests <= max_g:
            score += 10
        elif guests < min_g or guests > max_g:
            score -= 15

    if budget:
        p_min = _get(caterer, "price_min")
        p_max = _get(caterer, "price_max")
        if p_min <= budget <= p_max:
            score += 10
        elif budget < p_min:
            score -= 10

    score += int((_get(caterer, "rating") - 4.0) * 10)
    if _get(caterer, "verified"):
        score += 5

    return max(0, min(100, score))


def get_recommendations(info: Dict[str, Any], top_n: int = 4) -> List[Dict[str, Any]]:
    """Keyword-based recommendations from in-memory seed data (fallback)."""
    scored = [{**c, "match_score": score_caterer(c, info)} for c in CATERERS]
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:top_n]


async def get_db_recommendations(
    query_text: str,
    info: Dict[str, Any],
    db,
    top_n: int = 4,
) -> List[Dict[str, Any]]:
    """Vector similarity search + keyword scoring using pgvector."""
    from openai import AsyncOpenAI
    from sqlalchemy import select
    from app.db.models import Caterer
    from app.core.config import settings

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    resp = await client.embeddings.create(model="text-embedding-3-small", input=query_text)
    embedding = resp.data[0].embedding

    stmt = (
        select(Caterer)
        .order_by(Caterer.embedding.cosine_distance(embedding))
        .limit(top_n * 2)
    )
    result = await db.execute(stmt)
    caterers = result.scalars().all()

    scored = [
        {
            "id": c.id, "name": c.name, "emoji": c.emoji, "rating": c.rating,
            "reviews": c.reviews, "cuisines": c.cuisines, "tags": c.tags,
            "price_display": c.price_display, "price_min": c.price_min,
            "price_max": c.price_max, "min_guests": c.min_guests,
            "location": c.location, "verified": c.verified,
            "photos_count": c.photos_count,
            "match_score": score_caterer(c, info),
        }
        for c in caterers
    ]
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:top_n]


def get_caterer_by_id(caterer_id: int) -> Optional[Dict[str, Any]]:
    return next((c for c in CATERERS if c["id"] == caterer_id), None)


def get_all_caterers() -> List[Dict[str, Any]]:
    return CATERERS
