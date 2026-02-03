"""FastAPI backend for the Todo application with authentication."""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from .agents.auth_agent import auth_agent
from .storage import task_storage
from .auth.service import auth_service


# Pydantic models for request/response
class SignupRequest(BaseModel):
    email: str
    password: str
    confirm_password: Optional[str] = None


class SignupResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[dict] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[dict] = None


class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    priority: str
    completed: bool
    user_id: str
    created_at: str
    updated_at: str


class TaskListResponse(BaseModel):
    success: bool
    data: list[TaskResponse]
    message: Optional[str] = None


# Initialize FastAPI app
app = FastAPI(title="Todo App API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication dependency
async def get_current_user(request: Request):
    """Dependency to get current authenticated user from token."""
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required"
        )

    # Verify the token
    auth_result = auth_service.authenticate_request(authorization)

    if not auth_result or not auth_result.get("authenticated"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Store user in request state for later use
    request.state.user = auth_result["user"]
    return auth_result["user"]


@app.post("/api/auth/signup", response_model=SignupResponse)
async def signup(request: SignupRequest):
    """Register a new user account."""
    # Use auth_service directly for signup
    result = auth_service.signup(
        email=request.email,
        password=request.password
    )

    if result["success"]:
        return SignupResponse(**result)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )


@app.post("/api/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Log in an existing user."""
    # Use auth_service directly for login
    result = auth_service.login(
        email=request.email,
        password=request.password
    )

    if result["success"]:
        return LoginResponse(**result)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["message"]
        )


@app.get("/api/tasks")
async def get_tasks(current_user: dict = Depends(get_current_user)):
    """Get all tasks for the authenticated user."""
    # Get tasks filtered by user ID
    user_tasks = task_storage.get_tasks_by_user(current_user.id)

    return {
        "success": True,
        "data": user_tasks
    }


@app.post("/api/tasks")
async def create_task(request: CreateTaskRequest, current_user: dict = Depends(get_current_user)):
    """Create a new task for the authenticated user."""
    # Create task associated with user ID
    task_data = {
        "title": request.title,
        "description": request.description,
        "priority": request.priority,
        "user_id": current_user.id
    }

    task = task_storage.create_task(task_data)

    return {
        "success": True,
        "data": task,
        "message": "Task created successfully"
    }


@app.put("/api/tasks/{task_id}")
async def update_task(task_id: str, request: UpdateTaskRequest, current_user: dict = Depends(get_current_user)):
    """Update a task for the authenticated user."""
    # Check if task belongs to user
    task = task_storage.get_task(task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    # Update the task
    update_data = request.dict(exclude_unset=True)
    updated_task = task_storage.update_task(task_id, update_data)

    return {
        "success": True,
        "data": updated_task,
        "message": "Task updated successfully"
    }


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a task for the authenticated user."""
    # Check if task belongs to user
    task = task_storage.get_task(task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    # Delete the task
    deleted_task = task_storage.delete_task(task_id)

    return {
        "success": True,
        "data": deleted_task,
        "message": "Task deleted successfully"
    }


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"message": "Todo App API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)