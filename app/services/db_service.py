from sqlalchemy.orm import Session
from sqlalchemy import func
from pgvector.sqlalchemy import Vector
import numpy as np

from app.db.models import UserInterest, KuriftuService
from app.services.embedding_service import embedding_service

class DatabaseService:
    def create_user_interest(self, db: Session, user_id: str, interests: str):
        """Create or update user interests with embeddings"""
        # Check if user already exists
        existing_interest = db.query(UserInterest).filter(UserInterest.user_id == user_id).first()
        
        # Generate embedding for interests
        embedding = embedding_service.get_embedding(interests)
        
        # Convert NumPy array to list for PostgreSQL compatibility
        embedding_list = embedding.tolist() if hasattr(embedding, 'tolist') else embedding
        
        if existing_interest:
            # Update existing record
            existing_interest.interests = interests
            existing_interest.embedding = embedding_list
            db.commit()
            db.refresh(existing_interest)
            return existing_interest
        else:
            # Create new record
            user_interest = UserInterest(
                user_id=user_id,
                interests=interests,
                embedding=embedding_list
            )
            db.add(user_interest)
            db.commit()
            db.refresh(user_interest)
            return user_interest
    
    def add_kuriftu_service(self, db: Session, name: str, description: str, category: str = None, location: str = None):
        """Add a Kuriftu service with embedding"""
        # Generate embedding from name and description
        text_to_embed = f"{name} {description}"
        if category:
            text_to_embed += f" {category}"
        if location:
            text_to_embed += f" {location}"
            
        embedding = embedding_service.get_embedding(text_to_embed)
        
        # Convert NumPy array to list for PostgreSQL compatibility
        embedding_list = embedding.tolist() if hasattr(embedding, 'tolist') else embedding
        
        service = KuriftuService(
            name=name,
            description=description,
            category=category,
            location=location,
            embedding=embedding_list
        )
        
        db.add(service)
        db.commit()
        db.refresh(service)
        return service
    
    def find_matching_services(self, db: Session, user_id: str, limit: int = 10):
        """Find Kuriftu services that match user interests"""
        # Get user interests
        user_interest = db.query(UserInterest).filter(UserInterest.user_id == user_id).first()
        
        if not user_interest:
            return []
        
        # Convert embedding to list if it's a NumPy array
        user_embedding = user_interest.embedding
        if hasattr(user_embedding, 'tolist'):
            user_embedding = user_embedding.tolist()
        
        # Find services with similar embeddings using L2 distance
        services = db.query(KuriftuService).order_by(
            KuriftuService.embedding.l2_distance(user_embedding)
        ).limit(limit).all()
        
        return services
    
    def get_user_interest(self, db: Session, user_id: str):
        """Get user interests by user_id"""
        return db.query(UserInterest).filter(UserInterest.user_id == user_id).first()
    
    def get_all_kuriftu_services(self, db: Session, skip: int = 0, limit: int = 100):
        """Get all Kuriftu services"""
        return db.query(KuriftuService).offset(skip).limit(limit).all()
    
    def get_kuriftu_services_by_category(self, db: Session, category: str):
        """Get Kuriftu services by category"""
        return db.query(KuriftuService).filter(KuriftuService.category == category).all()

# Create a singleton instance
db_service = DatabaseService()