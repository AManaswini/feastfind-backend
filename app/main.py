# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import caterers, inquiries, chat, events, openai_chat
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="FeastFind API",
    description="AI-powered catering marketplace backend",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────────────
app.include_router(caterers.router, prefix="/api")
app.include_router(inquiries.router, prefix="/api")
app.include_router(chat.router,      prefix="/api")
app.include_router(openai_chat.router, prefix="/api")
app.include_router(events.router,    prefix="/api")


# ── Health ──────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "FeastFind API", "version": "0.1.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
