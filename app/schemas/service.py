from pydantic import BaseModel
from datetime import datetime

class KuriftuService(BaseModel):
    id: int
    name: str
    description: str
    category: str | None = None
    location: str | None = None
    price: int
    coinValue: int
    created_at: datetime

    class Config:
        from_attributes = True