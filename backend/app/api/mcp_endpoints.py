"""
MCP (Micro Control Plane) endpoints integrated into the main server
Handles task operations through API endpoints using shared service layer
"""
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session
from datetime import datetime

from app.services.task_service import MCPTaskService
from app.db.database import get_session
from app.api.main import get_current_user_from_token  # Reuse authentication

# Define request/response models
class AddTaskRequest(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None


class CompleteTaskRequest(BaseModel):
    user_id: str
    task_id: int


class DeleteTaskRequest(BaseModel):
    user_id: str
    task_id: int


class ListTasksRequest(BaseModel):
    user_id: str


class ListTasksResponse(BaseModel):
    status: str
    tasks: List[Dict]


class TaskOperationResponse(BaseModel):
    status: str
    message: Optional[str] = None
    task: Optional[Dict] = None


# Create router for MCP endpoints
mcp_router = APIRouter(prefix="/mcp", tags=["mcp"])


@mcp_router.post("/tools/add_task", response_model=TaskOperationResponse)
def add_task(
    request: AddTaskRequest,
    current_user = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """Add a task via MCP interface"""
    # Verify that the requesting user matches the authenticated user
    if str(current_user.id) != request.user_id:
        raise HTTPException(status_code=403, detail="Forbidden: Cannot modify other users' tasks")

    try:
        result = MCPTaskService.add_task(
            session=session,
            user_id=request.user_id,
            title=request.title,
            description=request.description
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@mcp_router.post("/tools/list_tasks", response_model=ListTasksResponse)
def list_tasks(
    request: ListTasksRequest,
    current_user = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """List tasks via MCP interface"""
    # Verify that the requesting user matches the authenticated user
    if str(current_user.id) != request.user_id:
        raise HTTPException(status_code=403, detail="Forbidden: Cannot access other users' tasks")

    try:
        result = MCPTaskService.list_tasks(
            session=session,
            user_id=request.user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@mcp_router.post("/tools/complete_task", response_model=TaskOperationResponse)
def complete_task(
    request: CompleteTaskRequest,
    current_user = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """Complete a task via MCP interface"""
    # Verify that the requesting user matches the authenticated user
    if str(current_user.id) != request.user_id:
        raise HTTPException(status_code=403, detail="Forbidden: Cannot modify other users' tasks")

    try:
        result = MCPTaskService.complete_task(
            session=session,
            task_id=request.task_id,
            user_id=request.user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@mcp_router.post("/tools/delete_task", response_model=TaskOperationResponse)
def delete_task(
    request: DeleteTaskRequest,
    current_user = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """Delete a task via MCP interface"""
    # Verify that the requesting user matches the authenticated user
    if str(current_user.id) != request.user_id:
        raise HTTPException(status_code=403, detail="Forbidden: Cannot modify other users' tasks")

    try:
        result = MCPTaskService.delete_task(
            session=session,
            task_id=request.task_id,
            user_id=request.user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@mcp_router.get("/", response_model=Dict)
def mcp_root():
    """Root endpoint for MCP functionality"""
    return {"message": "Todo MCP Endpoints - Integrated into Main Server", "status": "active"}


@mcp_router.get("/health", response_model=Dict)
def mcp_health_check():
    """Health check for MCP endpoints"""
    return {"status": "healthy", "service": "mcp-integrated"}