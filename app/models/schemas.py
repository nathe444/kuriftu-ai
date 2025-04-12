from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# User interest schemas
class UserInterestBase(BaseModel):
    user_id: str
    interests: str

class UserInterestCreate(UserInterestBase):
    pass

class UserInterestResponse(UserInterestBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Kuriftu service schemas
class KuriftuServiceBase(BaseModel):
    name: str
    description: str
    category: Optional[str] = None
    location: Optional[str] = None

class KuriftuServiceCreate(KuriftuServiceBase):
    pass

class KuriftuServiceResponse(KuriftuServiceBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Itinerary generation request
class ItineraryRequest(BaseModel):
    user_id: str
    days: Optional[int] = 3

# Itinerary response
from pydantic import BaseModel
from typing import List

class Activity(BaseModel):
    time: str
    title: str
    location: str
    description: str

class DayPlan(BaseModel):
    day_number: int
    title: str
    activities: List[Activity]

class ItineraryResponse(BaseModel):
    user_id: str
    title: str
    days: List[DayPlan]