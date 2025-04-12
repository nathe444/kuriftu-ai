import uvicorn
from app.db.database import Base, engine
from app.db.models import UserInterest, KuriftuService, ItineraryPlan  # Add this import

# Create all tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)