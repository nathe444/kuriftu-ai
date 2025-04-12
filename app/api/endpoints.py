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
from app.models.schemas import ItineraryPlanResponse

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
    
    # Log the AI response
    print("\nAI Response:")
    print(itinerary_content)
    print("\n")
    
    try:
        days = []
        current_day = None
        current_activities = []
        title = "Your Personalized Kuriftu Resort Itinerary"
        
        lines = itinerary_content.split('\n')
        print("\nParsing lines:")
        for line in lines:
            print(f"Processing line: {line}")
            line = line.strip()
            if not line:
                continue
            
            # Extract day information
            if 'Day' in line and ':' in line:
                print(f"Found day: {line}")
                if current_day and current_activities:
                    days.append({
                        'day_number': len(days) + 1,
                        'title': current_day,
                        'activities': current_activities.copy()
                    })
                current_day = line
                current_activities = []
            
            # Extract activities
            elif any(period in line for period in ['Morning:', 'Afternoon:', 'Evening:']):
                try:
                    print(f"Found activity: {line}")
                    # Split time and details
                    time_part, details = [x.strip() for x in line.split(':', 1)]
                    
                    # Parse location and description
                    location_start = details.find('(')
                    location_end = details.find(')')
                    
                    if location_start != -1 and location_end != -1:
                        activity_title = details[:location_start].strip()
                        location = details[location_start + 1:location_end].strip()
                        description = details[location_end + 1:].strip('- ').strip()
                        
                        current_activities.append({
                            'time': time_part,
                            'title': activity_title,
                            'location': location,
                            'description': description
                        })
                        print(f"Added activity: {current_activities[-1]}")
                except Exception as e:
                    print(f"Error parsing activity: {e}")
                    continue
        
        # Add the last day
        if current_day and current_activities:
            days.append({
                'day_number': len(days) + 1,
                'title': current_day,
                'activities': current_activities.copy()
            })
        
        print("\nFinal days structure:")
        print(days)
        
        response_data = {
            "user_id": request.user_id,
            "title": title,
            "days": days
        }
        
        if days:  # Only save if we have valid days
            db_service.save_itinerary_plan(
                db=db,
                user_id=request.user_id,
                title=response_data["title"],
                days=days
            )
        
        return response_data
        
    except Exception as e:
        print(f"Error parsing itinerary: {e}")
        return {
            "user_id": request.user_id,
            "title": "Error generating itinerary",
            "days": []
        }

@router.get("/itinerary-plans/{user_id}", response_model=List[ItineraryPlanResponse])
def get_user_itinerary_plans(user_id: str, db: Session = Depends(get_db)):
    """Get all itinerary plans for a user"""
    plans = db_service.get_user_plans(db, user_id)
    if not plans:
        raise HTTPException(status_code=404, detail="No itinerary plans found for this user")
    return plans