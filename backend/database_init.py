#!/usr/bin/env python3
"""
Database initialization script for the Todo application.

This script creates the necessary database tables based on the specifications:
- Users table for storing user accounts
- Tasks table for storing todo items linked to users
- Proper relationships and constraints for user isolation
"""

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from src.config import DATABASE_URL
import argparse
import sys


def create_database_engine():
    """Create and return a database engine."""
    engine = create_engine(DATABASE_URL)
    return engine


def create_tables(engine):
    """Create all required database tables."""
    print("Creating database tables...")

    # Import models here to avoid circular imports
    from src.db.database import Base

    # Create all tables based on models
    Base.metadata.create_all(bind=engine)

    print("✓ Users table created")
    print("✓ Tasks table created")
    print("✓ Foreign key relationships established")


def verify_tables(engine):
    """Verify that all required tables exist."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    required_tables = ['users', 'tasks']
    missing_tables = [table for table in required_tables if table not in tables]

    if missing_tables:
        print(f"✗ Missing tables: {missing_tables}")
        return False

    print("✓ All required tables exist")

    # Verify table structure
    users_columns = [col['name'] for col in inspector.get_columns('users')]
    tasks_columns = [col['name'] for col in inspector.get_columns('tasks')]

    # Verify users table structure
    required_user_cols = ['id', 'email', 'password_hash', 'created_at', 'updated_at']
    missing_user_cols = [col for col in required_user_cols if col not in users_columns]

    if missing_user_cols:
        print(f"✗ Missing columns in users table: {missing_user_cols}")
        return False

    print("✓ Users table has correct structure")

    # Verify tasks table structure
    required_task_cols = ['id', 'user_id', 'title', 'description', 'status', 'priority', 'due_date', 'created_at', 'updated_at']
    missing_task_cols = [col for col in required_task_cols if col not in tasks_columns]

    if missing_task_cols:
        print(f"✗ Missing columns in tasks table: {missing_task_cols}")
        return False

    print("✓ Tasks table has correct structure")

    # Verify foreign key constraint
    foreign_keys = inspector.get_foreign_keys('tasks')
    user_fk = [fk for fk in foreign_keys if fk['constrained_columns'] == ['user_id']]

    if not user_fk:
        print("✗ Foreign key constraint from tasks.user_id to users.id not found")
        return False

    if user_fk[0]['referred_table'] != 'users':
        print("✗ Foreign key constraint points to wrong table")
        return False

    print("✓ Foreign key relationship between tasks and users verified")

    return True


def create_indexes(engine):
    """Create necessary indexes for performance."""
    print("Creating database indexes...")

    with engine.connect() as conn:
        # Index on user_id in tasks table (for efficient user-based queries)
        try:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks (user_id);"))
            print("✓ Index on tasks.user_id created")
        except Exception as e:
            print(f"! Could not create index on tasks.user_id: {e}")

        # Index on status in tasks table (for filtering)
        try:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks (status);"))
            print("✓ Index on tasks.status created")
        except Exception as e:
            print(f"! Could not create index on tasks.status: {e}")

        # Composite index on user_id and status (for combined queries)
        try:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tasks_user_status ON tasks (user_id, status);"))
            print("✓ Composite index on tasks.user_id and status created")
        except Exception as e:
            print(f"! Could not create composite index on tasks.user_id and status: {e}")

        # Index on due_date for deadline-based queries
        try:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks (due_date);"))
            print("✓ Index on tasks.due_date created")
        except Exception as e:
            print(f"! Could not create index on tasks.due_date: {e}")

        # Index on priority for priority-based queries
        try:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks (priority);"))
            print("✓ Index on tasks.priority created")
        except Exception as e:
            print(f"! Could not create index on tasks.priority: {e}")

        conn.commit()


def reset_database(engine):
    """Drop and recreate all database tables."""
    print("Resetting database (this will delete all data)...")

    # Import models here to avoid circular imports
    from src.db.database import Base

    # Drop all tables
    Base.metadata.drop_all(bind=engine)

    print("✓ Old tables dropped")

    # Create tables again
    create_tables(engine)
    create_indexes(engine)


def main():
    parser = argparse.ArgumentParser(description='Initialize the Todo application database')
    parser.add_argument('--reset', action='store_true', help='Reset the database (deletes all data)')
    parser.add_argument('--verify-only', action='store_true', help='Only verify existing tables')

    args = parser.parse_args()

    print("Todo Application Database Initialization")
    print("=" * 40)

    # Create database engine
    engine = create_database_engine()

    if args.reset:
        reset_database(engine)
    elif args.verify_only:
        if verify_tables(engine):
            print("\n✓ Database verification successful")
            return 0
        else:
            print("\n✗ Database verification failed")
            return 1
    else:
        # Check if tables already exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if 'users' in tables and 'tasks' in tables:
            print("Database tables already exist.")
            if verify_tables(engine):
                print("\n✓ Database is properly configured")
                return 0
            else:
                print("\n✗ Database verification failed")
                return 1
        else:
            print("Setting up new database...")
            create_tables(engine)
            create_indexes(engine)

    # Verify the setup
    if verify_tables(engine):
        print("\n✓ Database setup completed successfully")
        print("\nDatabase schema:")
        print("- users table: id, email, password_hash, created_at, updated_at")
        print("- tasks table: id, user_id, title, description, status, priority, due_date, recurrence_pattern, created_at, updated_at")
        print("- Foreign key: tasks.user_id references users.id (with CASCADE delete)")
        print("- Indexes: on user_id, status, and other frequently queried fields")
        return 0
    else:
        print("\n✗ Database setup verification failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)