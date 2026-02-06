"""
Database Connection Module
Using SQLModel with PostgreSQL
"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os

# Get database URL from config
from app.config import DATABASE_URL

# Create single engine instance with connection pooling and proper SSL settings
if "postgresql" in DATABASE_URL:
    # PostgreSQL-specific settings
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,    # Recycle connections every 5 minutes
        pool_size=5,
        max_overflow=10,
        pool_timeout=20,
        connect_args={
            "connect_timeout": 15,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 3,
        }
    )
else:
    # SQLite settings
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )

# Import models to register them with SQLModel after engine is created
from app.models.user import User
from app.models.chat_models import Task, Conversation, Message

def create_db_and_tables():
    """
    Create database tables and migrate schema if needed
    """
    # Create all tables if they don't exist
    SQLModel.metadata.create_all(engine)

    # For SQLite, add any missing columns that might be needed
    from sqlalchemy import text

    # Check if the tasks table has the required columns and add them if missing
    with engine.connect() as conn:
        # Get current table info
        result = conn.execute(text("PRAGMA table_info(tasks)")).fetchall()
        existing_columns = [row[1] for row in result]  # Column names are in the second position

        # Add missing columns if they don't exist - commit each separately
        if 'due_date' not in existing_columns:
            conn.execute(text("ALTER TABLE tasks ADD COLUMN due_date DATETIME DEFAULT NULL"))
            conn.commit()

        if 'reminder_date' not in existing_columns:
            conn.execute(text("ALTER TABLE tasks ADD COLUMN reminder_date DATETIME DEFAULT NULL"))
            conn.commit()

        if 'priority' not in existing_columns:
            conn.execute(text("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'medium'"))
            conn.commit()

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    One session per request pattern
    """
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """
    Create database tables and migrate schema if needed
    """
    # Create all tables if they don't exist
    SQLModel.metadata.create_all(engine)

    # For SQLite, add any missing columns that might be needed
    from sqlalchemy import text

    # Check if the tasks table has the required columns and add them if missing
    with engine.connect() as conn:
        # Get current table info
        result = conn.execute(text("PRAGMA table_info(tasks)")).fetchall()
        existing_columns = [row[1] for row in result]  # Column names are in the second position

        # Add missing columns if they don't exist - commit each separately
        if 'due_date' not in existing_columns:
            conn.execute(text("ALTER TABLE tasks ADD COLUMN due_date DATETIME DEFAULT NULL"))
            conn.commit()

        if 'reminder_date' not in existing_columns:
            conn.execute(text("ALTER TABLE tasks ADD COLUMN reminder_date DATETIME DEFAULT NULL"))
            conn.commit()

        if 'priority' not in existing_columns:
            conn.execute(text("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'medium'"))
            conn.commit()