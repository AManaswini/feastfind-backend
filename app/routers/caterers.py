# app/routers/caterers.py
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.db.database import get_db
from app.db.models import Caterer as CatererModel, User
from app.schemas.caterer import CatererSummary, CatererDetail, CatererCreate
from app.core.auth import require_admin

router = APIRouter(prefix="/caterers", tags=["Caterers"])


@router.get("", response_model=List[CatererSummary])
async def list_caterers(
    cuisine: Optional[str] = Query(None, description="Filter by cuisine keyword"),
    verified: Optional[bool] = Query(None, description="Only verified caterers"),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    location: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CatererModel)

    if verified is not None:
        stmt = stmt.where(CatererModel.verified == verified)
    if min_rating is not None:
        stmt = stmt.where(CatererModel.rating >= min_rating)
    if location:
        stmt = stmt.where(CatererModel.location.ilike(f"%{location}%"))

    result = await db.execute(stmt)
    caterers = result.scalars().all()

    if cuisine:
        kw = cuisine.lower()
        caterers = [
            c for c in caterers
            if any(kw in cu.lower() for cu in (c.cuisines or []))
            or any(kw in tag.lower() for tag in (c.tags or []))
        ]

    return caterers


@router.get("/{caterer_id}", response_model=CatererDetail)
async def get_caterer(caterer_id: int, db: AsyncSession = Depends(get_db)):
    caterer = await db.get(CatererModel, caterer_id)
    if not caterer:
        raise HTTPException(status_code=404, detail="Caterer not found")
    return caterer


@router.post("", response_model=CatererDetail, status_code=201)
async def create_caterer(
    payload: CatererCreate,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    caterer = CatererModel(**payload.model_dump())
    db.add(caterer)
    await db.commit()
    await db.refresh(caterer)
    return caterer
