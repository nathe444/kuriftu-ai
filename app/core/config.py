import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:nati@localhost/kuriftu_planner")
    
    # If on Render, update the DATABASE_URL to use sslmode
    if ENV == "production" and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Vector dimensions for embeddings
    EMBEDDING_DIMENSION: int = 768  # Match your DB schema

settings = Settings()