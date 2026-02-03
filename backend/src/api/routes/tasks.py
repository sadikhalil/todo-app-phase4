from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...db.database import get_db
from ...auth.jwt import get_current_user
from ...services.task_service import TaskService
from ...models.user import User
from ...models.task import Task
from ...schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, TaskStatusUpdate,
    TaskStatsResponse, TaskBulkUpdate, TaskBulkUpdateResponse
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=TaskListResponse)
async def get_tasks(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("created_at", regex="^(created_at|updated_at|title|status|priority)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all tasks belonging to the authenticated user.

    Supports filtering by status, pagination, and sorting.
    """
    task_service = TaskService(db)

    # Validate status parameter
    if status_filter and status_filter not in ["complete", "incomplete"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be 'complete' or 'incomplete'"
        )

    tasks, total_count = task_service.get_tasks(
        user_id=current_user.id,
        status=status_filter,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        order=order
    )

    task_responses = []
    for task in tasks:
        task_responses.append(TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        ))

    return TaskListResponse(
        tasks=task_responses,
        pagination={
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total_count
        }
    )


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user.
    """
    task_service = TaskService(db)

    # Validate status parameter
    if task_data.status and task_data.status not in ["complete", "incomplete"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be 'complete' or 'incomplete'"
        )

    task = task_service.create_task(task_data, str(current_user.id))

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific task belonging to the authenticated user.
    """
    task_service = TaskService(db)
    task = task_service.get_task(task_id, str(current_user.id))

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing task belonging to the authenticated user.
    """
    task_service = TaskService(db)

    # Validate status parameter if provided
    if task_data.status and task_data.status not in ["complete", "incomplete"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be 'complete' or 'incomplete'"
        )

    updated_task = task_service.update_task(task_id, task_data, str(current_user.id))

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        status=updated_task.status,
        priority=updated_task.priority,
        due_date=updated_task.due_date,
        user_id=updated_task.user_id,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific task belonging to the authenticated user.
    """
    task_service = TaskService(db)
    deleted = task_service.delete_task(task_id, str(current_user.id))

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: str,
    status_update: TaskStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update only the status of a specific task.
    """
    task_service = TaskService(db)

    # Validate status parameter
    if status_update.status not in ["complete", "incomplete"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be 'complete' or 'incomplete'"
        )

    updated_task = task_service.update_task_status(
        task_id,
        status_update.status,
        str(current_user.id)
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        status=updated_task.status,
        priority=updated_task.priority,
        due_date=updated_task.due_date,
        user_id=updated_task.user_id,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )


@router.get("/stats", response_model=TaskStatsResponse)
async def get_task_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistics about the authenticated user's tasks.
    """
    task_service = TaskService(db)
    stats = task_service.get_user_stats(str(current_user.id))

    return TaskStatsResponse(
        total=stats["total"],
        completed=stats["completed"],
        incomplete=stats["incomplete"],
        by_priority=stats["by_priority"]
    )


@router.post("/bulk-update", response_model=TaskBulkUpdateResponse)
async def bulk_update_tasks(
    bulk_update_data: TaskBulkUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update multiple tasks for the authenticated user simultaneously.
    """
    task_service = TaskService(db)

    updated_count = 0
    failed_updates = []

    for task_id in bulk_update_data.task_ids:
        # Create a temporary update object
        temp_update = TaskUpdate(**bulk_update_data.updates)

        # Validate status parameter if provided in updates
        if temp_update.status and temp_update.status not in ["complete", "incomplete"]:
            failed_updates.append({
                "task_id": str(task_id),
                "error": "Invalid status value"
            })
            continue

        updated_task = task_service.update_task(str(task_id), temp_update, str(current_user.id))

        if updated_task:
            updated_count += 1
        else:
            failed_updates.append({
                "task_id": str(task_id),
                "error": "Task not found or does not belong to user"
            })

    return TaskBulkUpdateResponse(
        updated_count=updated_count,
        failed_updates=failed_updates
    )