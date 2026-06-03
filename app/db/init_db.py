import asyncio
from openai import AsyncOpenAI
from sqlalchemy import text, select
from app.db.database import engine, AsyncSessionLocal, Base
from app.db.models import Caterer
from app.data.seed import CATERERS
from app.core.config import settings


def _caterer_text(c: dict) -> str:
    return " | ".join([
        c["name"],
        c["description"],
        ", ".join(c["cuisines"]),
        ", ".join(c["tags"]),
        ", ".join(c["specialties"]),
        ", ".join(c["menu"]),
        c["location"],
        " ".join(c.get("match_keywords", [])),
    ])


async def _embed(client: AsyncOpenAI, blob: str) -> list[float]:
    resp = await client.embeddings.create(model="text-embedding-3-small", input=blob)
    return resp.data[0].embedding


async def create_tables():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        # Drop old separate admin tables (replaced by unified users/user_sessions)
        await conn.execute(text("DROP TABLE IF EXISTS admin_sessions CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS admins CASCADE"))
        await conn.run_sync(Base.metadata.create_all)


async def seed_caterers():
    async with AsyncSessionLocal() as session:
        count = (await session.execute(text("SELECT COUNT(*) FROM caterers"))).scalar()
        if count > 0:
            return

        client = AsyncOpenAI(api_key=settings.openai_api_key)

        for c in CATERERS:
            embedding = await _embed(client, _caterer_text(c))
            session.add(Caterer(
                id=c["id"],
                name=c["name"],
                emoji=c["emoji"],
                rating=c["rating"],
                reviews=c["reviews"],
                cuisines=c["cuisines"],
                tags=c["tags"],
                price_display=c["price_display"],
                price_min=c["price_min"],
                price_max=c["price_max"],
                price_note=c["price_note"],
                min_guests=c["min_guests"],
                max_guests=c["max_guests"],
                location=c["location"],
                phone=c["phone"],
                email=c["email"],
                verified=c["verified"],
                description=c["description"],
                specialties=c["specialties"],
                menu=c["menu"],
                photos_count=c["photos_count"],
                match_keywords=c.get("match_keywords", []),
                embedding=embedding,
            ))

        await session.commit()
        print(f"Seeded {len(CATERERS)} caterers with embeddings.")


async def init_db():
    await create_tables()
    await seed_caterers()


if __name__ == "__main__":
    asyncio.run(init_db())
