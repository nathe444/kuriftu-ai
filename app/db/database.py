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
        # Drop existing tables first
        Base.metadata.drop_all(bind=engine)
        print("Existing tables dropped")
        
        # Create vector extension
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        print("Vector extension created successfully")
        
        # Create tables with new dimension
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
        
    except Exception as e:
        print(f"Error in database setup: {e}")
        raise  # Re-raise the exception to see the full error stack

def check_and_seed_data():
    try:
        db = SessionLocal()
        # Verify table exists before querying
        with engine.connect() as conn:
            result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'kuriftu_services')"))
            table_exists = result.scalar()
            
        if not table_exists:
            print("Table does not exist, creating tables...")
            create_database()
            
        # Now check if table is empty
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
        raise  # Re-raise the exception to see the full error stack

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