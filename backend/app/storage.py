"""In-memory storage for Todo tasks."""

from datetime import datetime
from uuid import uuid4
from typing import Optional, List, Dict, Any


# In-memory task storage
tasks = {}  # task_id -> Task mapping


class Task:
    """Task model for storing todo items."""

    def __init__(self, title: str, user_id: str, date: Optional[str] = None, note: Optional[str] = None, priority: str = "medium"):
        self.id = str(uuid4())
        self.title = title
        self.user_id = user_id  # Associate task with user
        self.date = date
        self.note = note
        self.priority = priority  # Task priority: low, medium, high
        self.completed = False
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "date": self.date,
            "note": self.note,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class TaskStorage:
    """Class-based storage for tasks with user association."""

    def __init__(self):
        self.tasks = {}  # task_id -> Task mapping

    def get_all_tasks(self):
        """Get all tasks from storage."""
        return [task.to_dict() for task in self.tasks.values()]

    def get_task(self, task_id: str):
        """Get a specific task by ID."""
        return self.tasks.get(task_id)

    def get_tasks_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a specific user."""
        user_tasks = []
        for task in self.tasks.values():
            if task.user_id == user_id:
                user_tasks.append(task.to_dict())
        return user_tasks

    def create_task(self, task_data: Dict[str, Any]):
        """Add a new task to storage."""
        task = Task(
            title=task_data["title"],
            user_id=task_data["user_id"],
            date=task_data.get("date"),
            note=task_data.get("note"),
            priority=task_data.get("priority", "medium")
        )
        self.tasks[task.id] = task
        return task.to_dict()

    def delete_task(self, task_id: str):
        """Delete a task from storage."""
        if task_id in self.tasks:
            deleted_task = self.tasks[task_id].to_dict()
            del self.tasks[task_id]
            return deleted_task
        return None

    def update_task(self, task_id: str, update_data: Dict[str, Any]):
        """Update an existing task."""
        if task_id in self.tasks:
            task = self.tasks[task_id]

            # Update fields if provided
            if "title" in update_data and update_data["title"] is not None:
                task.title = update_data["title"]
            if "date" in update_data and update_data["date"] is not None:
                task.date = update_data["date"]
            if "note" in update_data and update_data["note"] is not None:
                task.note = update_data["note"]
            if "priority" in update_data and update_data["priority"] is not None:
                task.priority = update_data["priority"]
            if "completed" in update_data and update_data["completed"] is not None:
                task.completed = update_data["completed"]

            task.updated_at = datetime.now().isoformat()
            return task.to_dict()
        return None

    def mark_complete(self, task_id: str, completed: bool = True):
        """Mark a task as complete or incomplete."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.completed = completed
            task.updated_at = datetime.now().isoformat()
            return task.to_dict()
        return None


# Global task storage instance
task_storage = TaskStorage()
