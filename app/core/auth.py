# app/core/auth.py
import hashlib
import hmac
import secrets
import base64
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import UserSession, User


# ── Password hashing (pbkdf2-sha256, stdlib only) ────────────────
def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000)
    return f"pbkdf2:sha256:260000:{salt}:{base64.b64encode(dk).decode()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        _, _, iterations, salt, b64_hash = stored.split(":")
        dk = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), int(iterations)
        )
        return hmac.compare_digest(dk, base64.b64decode(b64_hash))
    except Exception:
        return False


# ── Session token generation ─────────────────────────────────────
SESSION_TTL_HOURS = 24


def create_token() -> str:
    return secrets.token_urlsafe(32)


def session_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=SESSION_TTL_HOURS)


# ── FastAPI dependency: any authenticated user ───────────────────
async def require_user(
    authorization: str | None = Header(None),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization[len("Bearer "):]
    result = await db.execute(
        select(UserSession).where(
            UserSession.token == token,
            UserSession.expires_at > datetime.now(timezone.utc),
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    user = await db.get(User, session.user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

    return user


# ── FastAPI dependency: admin-only ───────────────────────────────
async def require_admin(user: User = Depends(require_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
