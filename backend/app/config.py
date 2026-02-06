import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
TODO_DB_PATH = PROJECT_ROOT / "todo_app.db"

# Use PostgreSQL from environment variable, fallback to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{TODO_DB_PATH}"