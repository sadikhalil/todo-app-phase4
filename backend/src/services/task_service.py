from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, func
from ..models.task import Task
from ..models.user import User
from ..schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def get_tasks(
        self,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "created_at",
        order: str = "desc"
    ) -> tuple[List[Task], int]:
        """
        Retrieve tasks for a specific user with optional filtering and pagination.

        Args:
            user_id: ID of the user whose tasks to retrieve
            status: Optional status filter ('complete', 'incomplete')
            limit: Maximum number of results to return
            offset: Number of results to skip
            sort_by: Field to sort by ('created_at', 'updated_at', 'title', 'status', 'priority')
            order: Sort order ('asc', 'desc')

        Returns:
            Tuple of (list of tasks, total count)
        """
        query = self.db.query(Task).filter(Task.user_id == user_id)

        # Apply status filter if provided
        if status:
            query = query.filter(Task.status == status)

        # Apply sorting
        if sort_by == "created_at":
            sort_field = Task.created_at
        elif sort_by == "updated_at":
            sort_field = Task.updated_at
        elif sort_by == "title":
            sort_field = Task.title
        elif sort_by == "status":
            sort_field = Task.status
        elif sort_by == "priority":
            sort_field = Task.priority
        else:
            sort_field = Task.created_at  # Default

        if order == "asc":
            query = query.order_by(sort_field.asc())
        else:
            query = query.order_by(sort_field.desc())

        # Get total count
        total_count = query.count()

        # Apply pagination
        tasks = query.offset(offset).limit(limit).all()

        return tasks, total_count

    def get_task(self, task_id: str, user_id: str) -> Optional[Task]:
        """
        Retrieve a specific task for a user.

        Args:
            task_id: ID of the task to retrieve
            user_id: ID of the user who owns the task

        Returns:
            Task object if found and belongs to user, None otherwise
        """
        task = self.db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
        ).first()
        return task

    def create_task(self, task_data: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for a user.

        Args:
            task_data: Task creation data
            user_id: ID of the user creating the task

        Returns:
            Created Task object
        """
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status or 'incomplete',
            priority=task_data.priority or "medium",
            due_date=task_data.due_date
        )

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

    def update_task(self, task_id: str, task_data: TaskUpdate, user_id: str) -> Optional[Task]:
        """
        Update an existing task for a user.

        Args:
            task_id: ID of the task to update
            task_data: Task update data
            user_id: ID of the user who owns the task

        Returns:
            Updated Task object if successful, None if task doesn't exist or doesn't belong to user
        """
        task = self.db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return None

        # Update only provided fields
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.status is not None:
            task.status = task_data.status
        if task_data.priority is not None:
            task.priority = task_data.priority
        if task_data.due_date is not None:
            task.due_date = task_data.due_date

        task.updated_at = func.now()

        self.db.commit()
        self.db.refresh(task)

        return task

    def delete_task(self, task_id: str, user_id: str) -> bool:
        """
        Delete a task for a user.

        Args:
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            True if task was deleted, False if task doesn't exist or doesn't belong to user
        """
        task = self.db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return False

        self.db.delete(task)
        self.db.commit()

        return True

    def update_task_status(self, task_id: str, status: str, user_id: str) -> Optional[Task]:
        """
        Update the status of a task for a user.

        Args:
            task_id: ID of the task to update
            status: New status value
            user_id: ID of the user who owns the task

        Returns:
            Updated Task object if successful, None if task doesn't exist or doesn't belong to user
        """
        task = self.db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return None

        task.status = status
        task.updated_at = func.now()

        self.db.commit()
        self.db.refresh(task)

        return task

    def get_user_stats(self, user_id: str) -> dict:
        """
        Get statistics for a user's tasks.

        Args:
            user_id: ID of the user

        Returns:
            Dictionary with task statistics
        """
        total_tasks = self.db.query(Task).filter(Task.user_id == user_id).count()
        completed_tasks = self.db.query(Task).filter(
            and_(Task.user_id == user_id, Task.status == 'complete')
        ).count()
        incomplete_tasks = total_tasks - completed_tasks

        # Count tasks by priority
        priority_counts = {}
        priority_query = self.db.query(
            Task.priority,
            func.count(Task.id).label('count')
        ).filter(Task.user_id == user_id).group_by(Task.priority).all()

        for priority, count in priority_query:
            priority_counts[priority] = count if priority else 0

        stats = {
            "total": total_tasks,
            "completed": completed_tasks,
            "incomplete": incomplete_tasks,
            "by_priority": priority_counts
        }

        return stats