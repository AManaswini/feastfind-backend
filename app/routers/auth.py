# app/routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.database import get_db
from app.db.models import User, UserSession
from app.schemas.caterer import UserRegister, UserLogin, TokenResponse
from app.core.auth import hash_password, verify_password, create_token, session_expiry, require_user, require_admin

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/setup", response_model=TokenResponse, status_code=201)
async def setup_first_admin(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    """One-time endpoint to create the first admin account. Returns 409 if any admin exists."""
    count = await db.scalar(select(func.count()).select_from(User).where(User.is_admin == True))
    if count and count > 0:
        raise HTTPException(status_code=409, detail="Admin account already exists. Use /auth/login.")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_active=True,
        is_admin=True,
    )
    db.add(user)
    await db.flush()

    token = create_token()
    session = UserSession(user_id=user.id, token=token, expires_at=session_expiry())
    db.add(session)
    await db.commit()

    return TokenResponse(token=token, email=user.email, is_admin=True)


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(func.count()).select_from(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_active=True,
        is_admin=False,
    )
    db.add(user)
    await db.flush()

    token = create_token()
    session = UserSession(user_id=user.id, token=token, expires_at=session_expiry())
    db.add(session)
    await db.commit()

    return TokenResponse(token=token, email=user.email, is_admin=False)


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token()
    session = UserSession(user_id=user.id, token=token, expires_at=session_expiry())
    db.add(session)
    await db.commit()

    return TokenResponse(token=token, email=user.email, is_admin=user.is_admin)


@router.post("/logout", status_code=204)
async def logout(user: User = Depends(require_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserSession).where(UserSession.user_id == user.id))
    for session in result.scalars().all():
        await db.delete(session)
    await db.commit()


@router.get("/me")
async def me(user: User = Depends(require_user)):
    return {"id": user.id, "email": user.email, "is_admin": user.is_admin}


# ── Admin: user management ───────────────────────────────────────

@router.get("/users")
async def list_users(admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).order_by(User.id))
    users = result.scalars().all()
    return [{"id": u.id, "email": u.email, "is_admin": u.is_admin, "is_active": u.is_active} for u in users]


@router.patch("/users/{user_id}/make-admin", status_code=200)
async def make_admin(user_id: int, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_admin:
        return {"id": user.id, "email": user.email, "is_admin": True}
    user.is_admin = True
    await db.commit()
    return {"id": user.id, "email": user.email, "is_admin": True}


@router.patch("/users/{user_id}/revoke-admin", status_code=200)
async def revoke_admin(user_id: int, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot revoke your own admin access")
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = False
    await db.commit()
    return {"id": user.id, "email": user.email, "is_admin": False}
