"""
MCP (Micro Control Plane) Server for Todo Application
Handles task operations through API endpoints using shared service layer
"""
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, create_engine
from datetime import datetime
import os
import uvicorn

# Import the shared service
from app.services.task_service import MCPTaskService
from app.db.database import get_session, engine

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

def create_db_and_tables():
    from sqlmodel import SQLModel
    from app.models.chat_models import Task
    SQLModel.metadata.create_all(engine)

# Create FastAPI app
app = FastAPI(title="Todo MCP Server", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Tool endpoints - using shared service layer
@app.post("/mcp/tools/add_task")
def add_task(request: AddTaskRequest):
    session = get_session()
    try:
        result = MCPTaskService.add_task(
            session=session,
            user_id=request.user_id,
            title=request.title,
            description=request.description
        )
        return result
    finally:
        session.close()

@app.post("/mcp/tools/list_tasks")
def list_tasks(request: ListTasksRequest):
    session = get_session()
    try:
        result = MCPTaskService.list_tasks(
            session=session,
            user_id=request.user_id
        )
        return result
    finally:
        session.close()

@app.post("/mcp/tools/complete_task")
def complete_task(request: CompleteTaskRequest):
    session = get_session()
    try:
        result = MCPTaskService.complete_task(
            session=session,
            task_id=request.task_id,
            user_id=request.user_id
        )
        return result
    finally:
        session.close()

@app.post("/mcp/tools/delete_task")
def delete_task(request: DeleteTaskRequest):
    session = get_session()
    try:
        result = MCPTaskService.delete_task(
            session=session,
            task_id=request.task_id,
            user_id=request.user_id
        )
        return result
    finally:
        session.close()

@app.get("/")
def read_root():
    return {"message": "Todo MCP Server v1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "mcp-server"}

if __name__ == "__main__":
    uvicorn.run(
        "mcp.mcp_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )