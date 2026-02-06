import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use SQLite for immediate functionality - switch back to PostgreSQL after submission
DATABASE_URL = "sqlite:///./todo_app.db"