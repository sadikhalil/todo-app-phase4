"""
REST API endpoints for tasks
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session
from typing import List
import os

from app.models.chat_models import TaskCreate, TaskUpdate, TaskResponse
from app.db.database import get_session
from app.auth import get_current_user
from app.models.user import User
from app.services.task_service import TaskService

router = APIRouter()

# GET /tasks - Retrieve all tasks for the authenticated user
@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    """
    tasks = TaskService.get_tasks_for_user(session, str(current_user.id))
    return tasks

# POST /tasks/ - Create a new task for the authenticated user (with trailing slash to match frontend)
@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    task = TaskService.create_task(session, str(current_user.id), task_data)
    return task

# PUT /tasks/{id} - Update an existing task
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task for the authenticated user.
    """
    task = TaskService.update_task(session, task_id, str(current_user.id), task_data)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

# DELETE /tasks/{id} - Delete a task
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task for the authenticated user.
    """
    success = TaskService.delete_task(session, task_id, str(current_user.id))

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"detail": "Task deleted successfully"}

# PATCH /tasks/{id}/status - Update task status
@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle/update the status of a task for the authenticated user.
    """
    task = TaskService.toggle_task_completion(session, task_id, str(current_user.id))

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

# GET /tasks/stats - Get task statistics
@router.get("/stats")
def get_task_stats(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get task statistics for the authenticated user.
    """
    return TaskService.get_task_stats(session, str(current_user.id))