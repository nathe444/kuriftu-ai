import os
import psycopg2
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.db.models import Base
from app.db.database import engine
from urllib.parse import urlparse

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Enable pgvector extension and create the necessary operators
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.execute(text("ALTER TABLE kuriftu_services ALTER COLUMN embedding TYPE vector USING embedding::vector;"))
        conn.execute(text("ALTER TABLE user_interests ALTER COLUMN embedding TYPE vector USING embedding::vector;"))
        conn.commit()
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()