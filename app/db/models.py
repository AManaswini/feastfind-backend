from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)


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
