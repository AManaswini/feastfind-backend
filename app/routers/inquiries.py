# app/routers/inquiries.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.database import get_db
from app.db.models import Caterer as CatererModel, Inquiry as InquiryModel
from app.schemas.caterer import InquiryCreate, InquiryOut

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])


@router.post("", response_model=InquiryOut, status_code=201)
async def create_inquiry(payload: InquiryCreate, db: AsyncSession = Depends(get_db)):
    caterer = await db.get(CatererModel, payload.caterer_id)
    if not caterer:
        raise HTTPException(status_code=404, detail="Caterer not found")

    inquiry = InquiryModel(**payload.model_dump(), status="pending")
    db.add(inquiry)
    await db.commit()
    await db.refresh(inquiry)
    return inquiry


@router.get("", response_model=List[InquiryOut])
async def list_inquiries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InquiryModel))
    return result.scalars().all()


@router.get("/{inquiry_id}", response_model=InquiryOut)
async def get_inquiry(inquiry_id: int, db: AsyncSession = Depends(get_db)):
    inquiry = await db.get(InquiryModel, inquiry_id)
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry
