"""Main Agent Handler - Central point for importing and handling all task agents."""

from app.agents.add_task_agent import add_task_agent
from app.agents.delete_task_agent import delete_task_agent
from app.agents.view_tasks_agent import view_tasks_agent
from app.agents.update_task_agent import update_task_agent
from app.agents.mark_complete_agent import mark_complete_agent
from app.agents.auth_agent import auth_agent


class AgentHandler:
    """Central handler for all task agents.

    This class provides a single entry point for all task operations,
    routing requests to the appropriate agent.
    """

    def __init__(self):
        self.add_agent = add_task_agent
        self.delete_agent = delete_task_agent
        self.view_agent = view_tasks_agent
        self.update_agent = update_task_agent
        self.complete_agent = mark_complete_agent
        self.auth_agent = auth_agent

    def add_task(self, title: str, date: str = None, note: str = None, user_id: str = None) -> dict:
        """Add a new task."""
        return self.add_agent.execute(title, user_id, date, note)

    def delete_task(self, task_id: str, confirmed: bool = False, user_id: str = None) -> dict:
        """Delete a task (requires confirmation)."""
        return self.delete_agent.execute(task_id, confirmed, user_id)

    def view_tasks(self, task_id: str = None, filter_status: str = None, user_id: str = None) -> dict:
        """View all tasks or a specific task."""
        return self.view_agent.execute(task_id, filter_status, user_id)

    def update_task(self, task_id: str, title: str = None, date: str = None, note: str = None, user_id: str = None) -> dict:
        """Update an existing task."""
        return self.update_agent.execute(task_id, title, date, note, user_id)

    def mark_complete(self, task_id: str, completed: bool = True, user_id: str = None) -> dict:
        """Mark a task as complete or incomplete."""
        return self.complete_agent.execute(task_id, completed, user_id)

    def toggle_complete(self, task_id: str, user_id: str = None) -> dict:
        """Toggle task completion status."""
        return self.complete_agent.toggle(task_id, user_id)

    def signup(self, email: str, password: str) -> dict:
        """Sign up a new user."""
        return self.auth_agent.signup(email, password)

    def login(self, email: str, password: str) -> dict:
        """Log in a user."""
        return self.auth_agent.login(email, password)

    def authenticate_request(self, token: str) -> dict:
        """Authenticate a request with JWT token."""
        return self.auth_agent.authenticate_request(token)


# Singleton instance
agent_handler = AgentHandler()
