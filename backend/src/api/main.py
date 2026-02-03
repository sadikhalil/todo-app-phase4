from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, tasks
from ...api.chat_api import router as chat_router
from ..config import APP_NAME, VERSION, DEBUG
from ..db.database import Base, engine
from ...models.chat_models import Conversation, Message, Task  # Import new models

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    debug=DEBUG,
    description="Todo application API with JWT authentication and user-based task isolation"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat_router)  # Include chat API router

@app.get("/")
def read_root():
    return {"message": f"{APP_NAME} API v{VERSION}"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}

@app.get("/health/ready")
def readiness_check():
    # Add any readiness checks here (database connections, etc.)
    return {"status": "ready", "service": "todo-api"}

@app.get("/health/live")
def liveness_check():
    # Add any liveness checks here
    return {"status": "alive", "service": "todo-api"}