"""
Main entry point for the Todo Application API Server
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api import router as api_router
from app.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.api.mcp_endpoints import mcp_router
from app.db.database import create_db_and_tables

# Create main app
app = FastAPI(
    title="Todo Application API",
    version="1.0.0",
    description="Todo application API with chat functionality"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    allow_origin_regex=r"https?://localhost(:[0-9]+)?|https?://127\.0\.0\.1(:[0-9]+)?",
)

# Include the API routes (includes chat routes)
app.include_router(api_router, prefix="/api", tags=["chat"])

# Include tasks routes directly (so the full path will be /tasks)
from app.api.tasks import router as tasks_router
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

# Include MCP routes for task operations via tools
app.include_router(mcp_router, prefix="", tags=["mcp"])

# Include auth routes at the app level (not under /api prefix)
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Todo Application API v1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )