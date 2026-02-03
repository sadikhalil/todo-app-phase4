from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.task import Base
from src.config import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """
    Initialize the database by creating all tables.
    This function creates all tables based on the defined models.
    """
    print("Initializing database...")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()