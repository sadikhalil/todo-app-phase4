"""
Shared task service layer for both REST API and MCP tools
Ensures consistent database operations across all interfaces
"""

from typing import List, Optional, Dict
from sqlmodel import Session, select
from datetime import datetime

from app.models.chat_models import Task as TaskModel
from app.models.chat_models import TaskCreate, TaskUpdate, TaskResponse


class TaskService:
    """Shared service layer for task operations"""

    @staticmethod
    def create_task(session: Session, user_id: str, task_data: TaskCreate) -> TaskResponse:
        """Create a new task in the database"""
        new_task = TaskModel(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=getattr(task_data, 'completed', False),
            due_date=getattr(task_data, 'due_date', None),
            reminder_date=getattr(task_data, 'reminder_date', None),
            priority=getattr(task_data, 'priority', 'medium')
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        # Convert to response format
        return TaskResponse(
            id=new_task.id,
            user_id=new_task.user_id,
            title=new_task.title,
            description=new_task.description,
            completed=new_task.completed,
            created_at=new_task.created_at,
            updated_at=new_task.updated_at,
            due_date=new_task.due_date,
            reminder_date=new_task.reminder_date,
            priority=new_task.priority
        )

    @staticmethod
    def get_tasks_for_user(session: Session, user_id: str) -> List[TaskResponse]:
        """Get all tasks for a specific user"""
        statement = select(TaskModel).where(TaskModel.user_id == user_id)
        tasks = session.exec(statement).all()

        task_responses = []
        for task in tasks:
            task_response = TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at,
                due_date=task.due_date,
                reminder_date=task.reminder_date,
                priority=task.priority
            )
            task_responses.append(task_response)

        return task_responses

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: str) -> Optional[TaskModel]:
        """Get a specific task by ID for a specific user"""
        statement = select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def update_task(session: Session, task_id: int, user_id: str, task_data: TaskUpdate) -> Optional[TaskResponse]:
        """Update an existing task"""
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        # Update task fields
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        # Convert to response format
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at,
            due_date=task.due_date,
            reminder_date=task.reminder_date,
            priority=task.priority
        )

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        """Delete a task by ID for a specific user"""
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[TaskResponse]:
        """Toggle the completion status of a task"""
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        # Convert to response format
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at,
            due_date=task.due_date,
            reminder_date=task.reminder_date,
            priority=task.priority
        )

    @staticmethod
    def get_task_stats(session: Session, user_id: str) -> Dict[str, int]:
        """Get task statistics for a user"""
        statement = select(TaskModel).where(TaskModel.user_id == user_id)
        all_tasks = session.exec(statement).all()

        total = len(all_tasks)
        completed = len([t for t in all_tasks if t.completed])
        pending = total - completed

        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }


# MCP-specific convenience functions that map to the shared service
class MCPTaskService:
    """Convenience wrapper for MCP tools to use the shared service"""

    @staticmethod
    def add_task(session: Session, user_id: str, title: str, description: Optional[str] = None) -> Dict:
        """Add a task via MCP interface"""
        task_data = TaskCreate(
            title=title,
            description=description or "Added via chatbot",
            completed=False
        )

        task_response = TaskService.create_task(session, user_id, task_data)

        return {
            "status": "success",
            "message": f"Task '{title}' added successfully",
            "task_id": task_response.id
        }

    @staticmethod
    def list_tasks(session: Session, user_id: str) -> Dict:
        """List tasks via MCP interface"""
        tasks = TaskService.get_tasks_for_user(session, user_id)

        task_list = []
        for task in tasks:
            task_list.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "reminder_date": task.reminder_date.isoformat() if task.reminder_date else None,
                "priority": task.priority
            })

        return {
            "status": "success",
            "tasks": task_list
        }

    @staticmethod
    def complete_task(session: Session, task_id: int, user_id: str) -> Dict:
        """Complete a task via MCP interface"""
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return {"status": "error", "error": "Task not found"}

        updated_task = TaskService.toggle_task_completion(session, task_id, user_id)

        return {
            "status": "success",
            "message": f"Task '{task.title}' marked as completed"
        }

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> Dict:
        """Delete a task via MCP interface"""
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return {"status": "error", "error": "Task not found"}

        success = TaskService.delete_task(session, task_id, user_id)

        if success:
            return {
                "status": "success",
                "message": f"Task '{task.title}' deleted successfully"
            }
        else:
            return {"status": "error", "error": "Failed to delete task"}