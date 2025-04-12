from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.schemas import (
    UserInterestCreate, UserInterestResponse,
    KuriftuServiceCreate, KuriftuServiceResponse,
    ItineraryRequest, ItineraryResponse
)
from app.services.db_service import db_service
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/interests/", response_model=UserInterestResponse)
def create_user_interest(interest: UserInterestCreate, db: Session = Depends(get_db)):
    """Create or update user interests"""
    return db_service.create_user_interest(db, interest.user_id, interest.interests)

@router.get("/interests/{user_id}", response_model=UserInterestResponse)
def get_user_interest(user_id: str, db: Session = Depends(get_db)):
    """Get user interests by user_id"""
    interest = db_service.get_user_interest(db, user_id)
    if not interest:
        raise HTTPException(status_code=404, detail="User interests not found")
    return interest

@router.post("/kuriftu-services/", response_model=KuriftuServiceResponse)
def create_kuriftu_service(service: KuriftuServiceCreate, db: Session = Depends(get_db)):
    """Add a Kuriftu service"""
    return db_service.add_kuriftu_service(
        db, 
        service.name, 
        service.description, 
        service.category, 
        service.location
    )

@router.get("/kuriftu-services/", response_model=List[KuriftuServiceResponse])
def get_kuriftu_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all Kuriftu services"""
    return db_service.get_all_kuriftu_services(db, skip, limit)

@router.get("/kuriftu-services/category/{category}", response_model=List[KuriftuServiceResponse])
def get_kuriftu_services_by_category(category: str, db: Session = Depends(get_db)):
    """Get Kuriftu services by category"""
    return db_service.get_kuriftu_services_by_category(db, category)

@router.post("/generate-itinerary/", response_model=ItineraryResponse)
def generate_itinerary(request: ItineraryRequest, db: Session = Depends(get_db)):
    """Generate a personalized itinerary"""
    # Get user interests and matched services
    user_interest = db_service.get_user_interest(db, request.user_id)
    if not user_interest:
        raise HTTPException(status_code=404, detail="User interests not found")
    
    # Find matching services
    matched_services = db_service.find_matching_services(db, request.user_id)
    
    # Generate itinerary
    itinerary_content = ai_service.generate_itinerary(
        user_interest.interests, 
        matched_services, 
        days=request.days
    )
    
    # Parse the content into structured format
    try:
        days = []
        current_day = None
        current_activities = []
        
        for line in itinerary_content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('Day'):
                if current_day and current_activities:
                    days.append({
                        'day_number': len(days) + 1,
                        'title': current_day,
                        'activities': current_activities
                    })
                current_day = line.split(':')[0]
                current_activities = []
            
            elif line.startswith('*'):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    time = parts[0].replace('*', '').strip()
                    desc_parts = parts[1].split('(')
                    if len(desc_parts) == 2:
                        title = desc_parts[0].strip()
                        location = desc_parts[1].replace(')', '').strip()
                        description = desc_parts[1].split('-')[-1].strip() if '-' in desc_parts[1] else ''
                        
                        current_activities.append({
                            'time': time,
                            'title': title,
                            'location': location,
                            'description': description
                        })
        
        # Add the last day
        if current_day and current_activities:
            days.append({
                'day_number': len(days) + 1,
                'title': current_day,
                'activities': current_activities
            })
        
        return {
            "user_id": request.user_id,
            "title": "Your Personalized Kuriftu Resort Itinerary",
            "days": days
        }
        
    except Exception as e:
        print(f"Error parsing itinerary: {e}")
        return {
            "user_id": request.user_id,
            "title": "Error generating itinerary",
            "days": []
        }