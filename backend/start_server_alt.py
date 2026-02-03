import uvicorn
from src.config import HOST

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host=HOST,
        port=8001,  # Changed to port 8001 to avoid conflicts
        reload=True,  # Enable auto-reload in debug mode
        log_level="info"
    )