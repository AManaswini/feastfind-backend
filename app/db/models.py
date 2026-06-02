from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
from app.db.database import Base


class Caterer(Base):
    __tablename__ = "caterers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    emoji = Column(String)
    rating = Column(Float)
    reviews = Column(Integer)
    cuisines = Column(ARRAY(String))
    tags = Column(ARRAY(String))
    price_display = Column(String)
    price_min = Column(Integer)
    price_max = Column(Integer)
    price_note = Column(String)
    min_guests = Column(Integer)
    max_guests = Column(Integer)
    location = Column(String)
    phone = Column(String)
    email = Column(String)
    verified = Column(Boolean, default=False)
    description = Column(Text)
    specialties = Column(ARRAY(String))
    menu = Column(ARRAY(String))
    photos_count = Column(Integer)
    match_keywords = Column(ARRAY(String))
    embedding = Column(Vector(1536), nullable=True)


class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    caterer_id = Column(Integer, nullable=False)
    name = Column(String)
    phone = Column(String, nullable=True)
    email = Column(String)
    notes = Column(Text, nullable=True)
    event_type = Column(String, nullable=True)
    guest_count = Column(Integer, nullable=True)
    budget = Column(String, nullable=True)
    status = Column(String, default="pending")
