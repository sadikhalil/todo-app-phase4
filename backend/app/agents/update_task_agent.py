"""Update Task Agent - Handles updating/editing existing tasks."""

from app.storage import task_storage


class UpdateTaskAgent:
    """Agent responsible for updating tasks.

    Responsibilities:
    - Validate task exists before update
    - Update task title, date, and/or note
    - Replace old values with new ones
    - Return confirmation of update

    Limitations:
    - Must not add or delete tasks
    - Must not change completion status (use MarkCompleteAgent)
    """

    def __init__(self):
        self.name = "UpdateTaskAgent"

    def validate_input(self, title: str = None) -> dict:
        """Validate the update input.

        Args:
            title: The new task title to validate (if provided)

        Returns:
            dict with 'valid' boolean and 'message' string
        """
        if title is not None:
            if not title.strip():
                return {"valid": False, "message": "Task title cannot be empty"}
            if len(title) > 255:
                return {"valid": False, "message": "Task title cannot exceed 255 characters"}
        return {"valid": True, "message": "Valid input"}

    def execute(self, task_id: str, title: str = None, date: str = None, note: str = None, user_id: str = None) -> dict:
        """Execute the update task operation.

        Args:
            task_id: The ID of the task to update
            title: New task title (optional)
            date: New task due date (optional)
            note: New task note/description (optional)
            user_id: ID of the user performing the update (optional for console, required for API)

        Returns:
            dict with success status and updated task data or error message
        """
        # Check if task exists
        existing_task = task_storage.get_task(task_id)
        if not existing_task:
            return {
                "success": False,
                "message": "Task not found. Cannot update a non-existent task."
            }

        # For API calls, verify the task belongs to the user
        if user_id and existing_task.get("user_id") != user_id:
            return {
                "success": False,
                "message": "Unauthorized: Task does not belong to user."
            }

        # Validate input if title is being updated
        if title is not None:
            validation = self.validate_input(title)
            if not validation["valid"]:
                return {
                    "success": False,
                    "message": validation["message"]
                }

        # Check if any update is provided
        if title is None and date is None and note is None:
            return {
                "success": False,
                "message": "No update provided. Please specify title, date, or note to update."
            }

        # Prepare update data
        update_data = {}
        if title is not None:
            update_data["title"] = title.strip()
        if date is not None:
            update_data["date"] = date
        if note is not None:
            update_data["note"] = note

        # Update the task
        updated_task = task_storage.update_task(
            task_id=task_id,
            update_data=update_data
        )

        if updated_task:
            changes = []
            if title is not None:
                changes.append("title")
            if date is not None:
                changes.append("date")
            if note is not None:
                changes.append("note")

            return {
                "success": True,
                "message": f"Task '{existing_task['title']}' has been updated! Changed: {', '.join(changes)}",
                "task": updated_task
            }
        else:
            return {
                "success": False,
                "message": "Failed to update task. Please try again."
            }


# Singleton instance
update_task_agent = UpdateTaskAgent()
