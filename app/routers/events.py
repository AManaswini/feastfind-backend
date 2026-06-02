# app/routers/events.py
from fastapi import APIRouter
from app.data.seed import EVENT_TYPES

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/types")
def get_event_types():
    """Return supported event type labels and icons."""
    return EVENT_TYPES
