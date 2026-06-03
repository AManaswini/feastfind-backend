# app/routers/admin.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.database import get_db
from app.db.models import Admin, AdminSession
from app.schemas.caterer import AdminSetup, AdminLogin, TokenResponse
from app.core.auth import hash_password, verify_password, create_token, session_expiry, require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/setup", response_model=TokenResponse, status_code=201)
async def setup_first_admin(payload: AdminSetup, db: AsyncSession = Depends(get_db)):
    """One-time endpoint to create the first admin account. Returns 409 if any admin exists."""
    count = await db.scalar(select(func.count()).select_from(Admin))
    if count and count > 0:
        raise HTTPException(status_code=409, detail="Admin account already exists. Use /login instead.")

    admin = Admin(
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_active=True,
    )
    db.add(admin)
    await db.flush()

    token = create_token()
    session = AdminSession(admin_id=admin.id, token=token, expires_at=session_expiry())
    db.add(session)
    await db.commit()

    return TokenResponse(token=token, email=admin.email)


@router.post("/login", response_model=TokenResponse)
async def login(payload: AdminLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admin).where(Admin.email == payload.email))
    admin = result.scalar_one_or_none()

    if not admin or not admin.is_active or not verify_password(payload.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token()
    session = AdminSession(admin_id=admin.id, token=token, expires_at=session_expiry())
    db.add(session)
    await db.commit()

    return TokenResponse(token=token, email=admin.email)


@router.post("/logout", status_code=204)
async def logout(
    admin: Admin = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    # The require_admin dependency already validated the token; delete all sessions for this admin
    result = await db.execute(select(AdminSession).where(AdminSession.admin_id == admin.id))
    for session in result.scalars().all():
        await db.delete(session)
    await db.commit()


@router.get("/me")
async def me(admin: Admin = Depends(require_admin)):
    return {"id": admin.id, "email": admin.email}
