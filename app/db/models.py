from sqlalchemy import Column, Integer, String, Text, DateTime, func
from pgvector.sqlalchemy import Vector

from app.db.database import Base
from app.core.config import settings

class UserInterest(Base):
    __tablename__ = "user_interests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    interests = Column(Text, nullable=False)
    embedding = Column(Vector(settings.EMBEDDING_DIMENSION))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class KuriftuService(Base):
    __tablename__ = "kuriftu_services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String)  # spa, restaurant, activity, event
    location = Column(String)
    embedding = Column(Vector(settings.EMBEDDING_DIMENSION))
    created_at = Column(DateTime(timezone=True), server_default=func.now())