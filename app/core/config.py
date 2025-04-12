import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Kuriftu Resort Itinerary Planner"
    PROJECT_VERSION: str = "1.0.0"
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Vector dimensions for embeddings
    EMBEDDING_DIMENSION: int = 768  # Match your DB schema

settings = Settings()