from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from app.core.config import settings

def check_and_seed_data():
    try:
        db = SessionLocal()
        # Check if KuriftuService table is empty
        from app.db.models import KuriftuService
        service_count = db.query(KuriftuService).count()
        
        if service_count == 0:
            print("KuriftuService table is empty. Seeding initial data...")
            from app.db.seed_data import seed_data
            seed_data()
            print("Data seeding completed successfully")
        
        db.close()
    except Exception as e:
        print(f"Error checking/seeding data: {e}")

def create_database():
    try:
        if settings.ENV == "production":
            # For production, just create tables and extension
            Base.metadata.create_all(bind=engine)
            print("Tables created successfully")
            
            # Create vector extension
            with engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()
            print("Vector extension created successfully")
        else:
            # Local development setup
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="nati"
            )
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'kuriftu_planner'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute('CREATE DATABASE kuriftu_planner')
            
            cursor.close()
            conn.close()
            
            Base.metadata.create_all(bind=engine)
            
            with engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()
                
    except Exception as e:
        print(f"Error in database setup: {e}")

# Create engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize database and seed data
create_database()
check_and_seed_data()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()