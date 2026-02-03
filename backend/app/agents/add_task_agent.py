"""Add Task Agent - Handles adding new tasks to the todo list."""

from app.storage import task_storage


class AddTaskAgent:
    """Agent responsible for adding new tasks.

    Responsibilities:
    - Extract task title, date, and note from user input
    - Validate that title exists
    - Call the task creation storage function
    - Return confirmation that the task was added

    Limitations:
    - Must not modify existing tasks
    - Must not list or delete tasks
    """

    def __init__(self):
        self.name = "AddTaskAgent"

    def validate_input(self, title: str) -> dict:
        """Validate the task input.

        Args:
            title: The task title to validate

        Returns:
            dict with 'valid' boolean and 'message' string
        """
        if not title or not title.strip():
            return {"valid": False, "message": "Task title cannot be empty"}
        if len(title) > 255:
            return {"valid": False, "message": "Task title cannot exceed 255 characters"}
        return {"valid": True, "message": "Valid input"}

    def execute(self, title: str, user_id: str = None, date: str = None, note: str = None) -> dict:
        """Execute the add task operation.

        Args:
            title: Task title (required)
            user_id: ID of the user creating the task (optional for console, required for API)
            date: Task due date (optional)
            note: Task note/description (optional)

        Returns:
            dict with success status and task data or error message
        """
        # Validate input
        validation = self.validate_input(title)
        if not validation["valid"]:
            return {
                "success": False,
                "message": validation["message"]
            }

        # Prepare task data
        task_data = {
            "title": title.strip(),
            "date": date if date else None,
            "note": note if note else None
        }

        # Add user_id if provided (for API calls)
        if user_id:
            task_data["user_id"] = user_id
        else:
            # For console app, we can assign a default user ID or handle differently
            task_data["user_id"] = "console_user"  # Default for console app

        # Add the task to storage
        task = task_storage.create_task(task_data)

        return {
            "success": True,
            "message": f"Task '{task['title']}' has been added successfully!",
            "task": task
        }


# Singleton instance
add_task_agent = AddTaskAgent()
