import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:nati@localhost/kuriftu_planner")
    EMBEDDING_DIMENSION: int = 768  # Update to match the actual embedding dimension
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    
    # Modify DATABASE_URL for production
    if ENV == "production":
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        if "?sslmode=" not in DATABASE_URL:
            DATABASE_URL += "?sslmode=require"

settings = Settings()