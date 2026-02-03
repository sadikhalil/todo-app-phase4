import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours

# Application configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
APP_NAME = os.getenv("APP_NAME", "Todo App API")
VERSION = os.getenv("VERSION", "1.0.0")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))