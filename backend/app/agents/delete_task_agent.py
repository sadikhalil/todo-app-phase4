"""Delete Task Agent - Handles deleting tasks from the todo list."""

from app.storage import task_storage


class DeleteTaskAgent:
    """Agent responsible for deleting tasks.

    Responsibilities:
    - Verify task exists before deletion
    - Provide confirmation request before deletion
    - Execute deletion after confirmation
    - Return confirmation that the task was deleted

    Limitations:
    - Must not modify task content
    - Must not add or list tasks
    """

    def __init__(self):
        self.name = "DeleteTaskAgent"

    def get_task_for_confirmation(self, task_id: str, user_id: str = None) -> dict:
        """Get task details for deletion confirmation.

        Args:
            task_id: The ID of the task to delete
            user_id: ID of the user requesting deletion (optional for console, required for API)

        Returns:
            dict with task details or error if not found
        """
        task = task_storage.get_task(task_id)
        if not task:
            return {
                "success": False,
                "message": "Task not found",
                "requires_confirmation": False
            }

        # For API calls, verify the task belongs to the user
        if user_id and task.get("user_id") != user_id:
            return {
                "success": False,
                "message": "Unauthorized: Task does not belong to user.",
                "requires_confirmation": False
            }

        return {
            "success": True,
            "message": f"Are you sure you want to delete '{task['title']}'?",
            "requires_confirmation": True,
            "task": task
        }

    def execute(self, task_id: str, confirmed: bool = False, user_id: str = None) -> dict:
        """Execute the delete task operation.

        Args:
            task_id: The ID of the task to delete
            confirmed: Whether deletion has been confirmed by user
            user_id: ID of the user performing the deletion (optional for console, required for API)

        Returns:
            dict with success status and message
        """
        # Check if task exists
        task = task_storage.get_task(task_id)
        if not task:
            return {
                "success": False,
                "message": "Task not found. It may have already been deleted."
            }

        # For API calls, verify the task belongs to the user
        if user_id and task.get("user_id") != user_id:
            return {
                "success": False,
                "message": "Unauthorized: Task does not belong to user."
            }

        # If not confirmed, return confirmation request
        if not confirmed:
            return self.get_task_for_confirmation(task_id, user_id)

        # Store task title before deletion for message
        task_title = task['title']

        # Execute deletion
        deleted_task = task_storage.delete_task(task_id)

        if deleted_task:
            return {
                "success": True,
                "message": f"Task '{task_title}' has been deleted successfully!"
            }
        else:
            return {
                "success": False,
                "message": "Failed to delete task. Please try again."
            }


# Singleton instance
delete_task_agent = DeleteTaskAgent()
