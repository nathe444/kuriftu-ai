from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, func
from pgvector.sqlalchemy import Vector

from app.db.database import Base
from app.core.config import settings

class UserInterest(Base):
    __tablename__ = "user_interests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    interests = Column(Text, nullable=False)
    embedding = Column(Vector(768))  # Fixed dimension to match the actual embedding size
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class KuriftuService(Base):
    __tablename__ = "kuriftu_services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String)
    location = Column(String)
    price = Column(Integer, nullable=False)
    coinValue = Column(Integer, nullable=False)
    embedding = Column(Vector(768))  # Fixed dimension to match the actual embedding size
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ItineraryPlan(Base):
    __tablename__ = "itinerary_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    days = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())