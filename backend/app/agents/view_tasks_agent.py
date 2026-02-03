"""View Tasks Agent - Handles viewing and listing tasks."""

from app.storage import task_storage


class ViewTasksAgent:
    """Agent responsible for viewing tasks.

    Responsibilities:
    - List all tasks
    - View a single task by ID
    - Filter tasks by completion status
    - Filter tasks by user

    Limitations:
    - Must not modify, add, or delete tasks
    """

    def __init__(self):
        self.name = "ViewTasksAgent"

    def get_all_tasks(self) -> dict:
        """Get all tasks from storage.

        Returns:
            dict with success status and list of tasks
        """
        tasks = task_storage.get_all_tasks()

        return {
            "success": True,
            "message": f"Found {len(tasks)} task(s)",
            "tasks": tasks,
            "count": len(tasks)
        }

    def get_tasks_by_user(self, user_id: str) -> dict:
        """Get all tasks for a specific user.

        Args:
            user_id: The ID of the user whose tasks to retrieve

        Returns:
            dict with success status and list of user's tasks
        """
        tasks = task_storage.get_tasks_by_user(user_id)

        return {
            "success": True,
            "message": f"Found {len(tasks)} task(s) for user",
            "tasks": tasks,
            "count": len(tasks)
        }

    def get_task_by_id(self, task_id: str) -> dict:
        """Get a specific task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            dict with success status and task data or error message
        """
        task = task_storage.get_task(task_id)

        if not task:
            return {
                "success": False,
                "message": "Task not found"
            }

        return {
            "success": True,
            "message": "Task found",
            "task": task
        }

    def get_pending_tasks(self, user_id: str = None) -> dict:
        """Get all pending (incomplete) tasks.

        Args:
            user_id: Optional user ID to filter by

        Returns:
            dict with success status and list of pending tasks
        """
        if user_id:
            all_tasks = task_storage.get_tasks_by_user(user_id)
        else:
            all_tasks = task_storage.get_all_tasks()

        pending = [task for task in all_tasks if not task["completed"]]

        return {
            "success": True,
            "message": f"Found {len(pending)} pending task(s)",
            "tasks": pending,
            "count": len(pending)
        }

    def get_completed_tasks(self, user_id: str = None) -> dict:
        """Get all completed tasks.

        Args:
            user_id: Optional user ID to filter by

        Returns:
            dict with success status and list of completed tasks
        """
        if user_id:
            all_tasks = task_storage.get_tasks_by_user(user_id)
        else:
            all_tasks = task_storage.get_all_tasks()

        completed = [task for task in all_tasks if task["completed"]]

        return {
            "success": True,
            "message": f"Found {len(completed)} completed task(s)",
            "tasks": completed,
            "count": len(completed)
        }

    def execute(self, task_id: str = None, filter_status: str = None, user_id: str = None) -> dict:
        """Execute the view tasks operation.

        Args:
            task_id: Optional specific task ID to view
            filter_status: Optional filter - 'pending', 'completed', or None for all
            user_id: Optional user ID to filter tasks by

        Returns:
            dict with success status and task(s) data
        """
        # If specific task ID provided
        if task_id:
            return self.get_task_by_id(task_id)

        # Filter by user if specified
        if user_id:
            if filter_status == "pending":
                return self.get_pending_tasks(user_id)
            elif filter_status == "completed":
                return self.get_completed_tasks(user_id)
            else:
                return self.get_tasks_by_user(user_id)

        # Filter by status if specified (for all users)
        if filter_status == "pending":
            return self.get_pending_tasks()
        elif filter_status == "completed":
            return self.get_completed_tasks()

        # Return all tasks by default
        return self.get_all_tasks()


# Singleton instance
view_tasks_agent = ViewTasksAgent()
