"""Mark Complete Agent - Handles marking tasks as complete/incomplete."""

from app.storage import task_storage


class MarkCompleteAgent:
    """Agent responsible for marking tasks as complete or incomplete.

    Responsibilities:
    - Mark a task as completed (with green tick)
    - Mark a task as incomplete (toggle back)
    - Validate task exists before marking

    Limitations:
    - Must not modify task content (title, date, note)
    - Must not add or delete tasks
    """

    def __init__(self):
        self.name = "MarkCompleteAgent"

    def execute(self, task_id: str, completed: bool = True, user_id: str = None) -> dict:
        """Execute the mark complete operation.

        Args:
            task_id: The ID of the task to mark
            completed: True to mark as complete, False to mark as incomplete
            user_id: ID of the user performing the action (optional for console, required for API)

        Returns:
            dict with success status and updated task data or error message
        """
        # Check if task exists
        existing_task = task_storage.get_task(task_id)
        if not existing_task:
            return {
                "success": False,
                "message": "Task not found. Cannot update completion status."
            }

        # For API calls, verify the task belongs to the user
        if user_id and existing_task.get("user_id") != user_id:
            return {
                "success": False,
                "message": "Unauthorized: Task does not belong to user."
            }

        # Check if already in desired state
        if existing_task['completed'] == completed:
            status_text = "completed" if completed else "incomplete"
            return {
                "success": True,
                "message": f"Task '{existing_task['title']}' is already marked as {status_text}.",
                "task": existing_task
            }

        # Mark the task
        updated_task = task_storage.mark_complete(task_id, completed)

        if updated_task:
            if completed:
                return {
                    "success": True,
                    "message": f"Task '{updated_task['title']}' marked as completed!",
                    "task": updated_task
                }
            else:
                return {
                    "success": True,
                    "message": f"Task '{updated_task['title']}' marked as incomplete.",
                    "task": updated_task
                }
        else:
            return {
                "success": False,
                "message": "Failed to update task status. Please try again."
            }

    def toggle(self, task_id: str, user_id: str = None) -> dict:
        """Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle
            user_id: ID of the user performing the action (optional for console, required for API)

        Returns:
            dict with success status and updated task data or error message
        """
        existing_task = task_storage.get_task(task_id)
        if not existing_task:
            return {
                "success": False,
                "message": "Task not found."
            }

        # For API calls, verify the task belongs to the user
        if user_id and existing_task.get("user_id") != user_id:
            return {
                "success": False,
                "message": "Unauthorized: Task does not belong to user."
            }

        # Toggle the current status
        new_status = not existing_task['completed']
        return self.execute(task_id, new_status, user_id)


# Singleton instance
mark_complete_agent = MarkCompleteAgent()
