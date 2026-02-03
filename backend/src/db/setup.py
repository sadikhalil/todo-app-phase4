from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .database import Base
from ..config import DATABASE_URL
import os

# Create database engine
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool if "sqlite" in DATABASE_URL else None,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency function to get database session.
    This function is meant to be used as a FastAPI dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all database tables based on the defined models.
    This function creates both User and Task tables.
    """
    print("Creating database tables...")

    # Create all tables from the unified Base
    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")

def check_tables_exist():
    """
    Check if the required tables exist in the database.

    Returns:
        dict: A dictionary indicating the existence of each table
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    return {
        "users_table_exists": "users" in tables,
        "tasks_table_exists": "tasks" in tables,
        "all_tables_exist": "users" in tables and "tasks" in tables
    }

def reset_database():
    """
    Drop and recreate all tables.
    WARNING: This will delete all data in the database.
    """
    print("Resetting database...")

    # Drop all tables
    Base.metadata.drop_all(bind=engine)

    # Create tables again
    create_tables()

    print("Database reset successfully!")

def initialize_database(reset=False):
    """
    Initialize the database by creating tables if they don't exist.

    Args:
        reset (bool): If True, reset the database (drop and recreate)
    """
    if reset:
        reset_database()
        return

    # Check if tables already exist
    table_status = check_tables_exist()

    if table_status['all_tables_exist']:
        print("Database tables already exist.")
        return

    # Create missing tables
    create_tables()

if __name__ == "__main__":
    # This allows the script to be run directly for initialization
    import sys

    reset_flag = "--reset" in sys.argv
    initialize_database(reset=reset_flag)