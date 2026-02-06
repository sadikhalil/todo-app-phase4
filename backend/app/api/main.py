"""
Main Todo Application API Server
Stateless server that handles task operations directly in the database
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List
import os
from datetime import datetime
from sqlmodel import Session, select
import httpx
import jwt
from datetime import datetime, timedelta

from app.db.database import get_session
from app.models.chat_models import Conversation, Message, Task, TaskCreate
from app.models.user import User, TokenData
from app.api.tasks import router as tasks_router

# Create router
router = APIRouter()

# NOTE: Tasks routes are now included directly in main.py at /tasks
# to match frontend expectations

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-and-long-random-string-here-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user_from_token(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    from fastapi import status
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception

    statement = select(User).where(User.email == token_data.email)
    user = session.exec(statement).first()

    if user is None:
        raise credentials_exception
    return user

# Configuration
INTERNAL_TOKEN = os.getenv("INTERNAL_TOKEN", "secret-token-change-in-production")

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None  # Made optional since we get it from the URL path

from typing import Optional, List, Dict, Any

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tool_calls: Optional[List[Dict[str, Any]]] = None  # Track tool calls made during the interaction
    task_operations: Optional[Dict[str, Any]] = None  # Track any task operations performed


# Task-related models and endpoints
class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    priority: str = "medium"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]


class TaskStatsResponse(BaseModel):
    total: int
    completed: int
    pending: int

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Chat endpoint that handles task operations directly in the database.
    Server holds NO conversational state in memory.
    """
    try:
        # Use the authenticated user's ID for all operations
        # This is more secure than trusting the path parameter
        effective_user_id = str(current_user.id)

        # Validate that the authenticated user matches the requested user_id
        if effective_user_id != user_id:
            print(f"Warning: Path user_id {user_id} does not match authenticated user_id {effective_user_id}")
            # For security, we'll use the authenticated user's ID instead of the path parameter
            # This prevents unauthorized access to other users' tasks

        # Log for debugging
        print(f"Chat endpoint called for user_id: {user_id}, effective_user_id: {effective_user_id}")

        # Determine intent from the message
        message_lower = request.message.lower()

        # Initialize variables for response
        response_text = ""
        tool_calls = []
        task_operations = {}

        # Handle different task operations based on intent
        if any(word in message_lower for word in ["add", "create", "make"]) and any(word in message_lower for word in ["task", "todo"]):
            # Extract task information from message
            import re
            # Look for task title in quotes or after task keywords
            title_match = re.search(r'"([^"]*)"', request.message) or re.search(r'(?:add|create|make) (?:a |an |the )?(?:task|todo) (?:to |for |about )?([^.!?]+?)(?:\.|!|\?|$)', request.message, re.IGNORECASE)

            if title_match:
                title = title_match.group(1).strip()
                # Clean up the title by removing common prefixes
                title = re.sub(r'^(to |that |will )', '', title, flags=re.IGNORECASE).strip()

                print(f"Creating task with title: {title}, user_id: {effective_user_id}")

                # Use shared service to add task
                from app.services.task_service import TaskService
                # Use the TaskCreate model from the models module
                from app.models.chat_models import TaskCreate as ModelTaskCreate
                task_data = ModelTaskCreate(
                    title=title,
                    description="Added via chatbot",
                    completed=False,
                    due_date=None,
                    reminder_date=None,
                    priority="medium"
                )

                new_task = TaskService.create_task(session, effective_user_id, task_data)
                print(f"Task created successfully: {new_task.id}")

                tool_calls.append({"name": "add_task", "arguments": {"title": title}})
                task_operations["add_task"] = {"status": "success", "task_id": new_task.id, "title": title}

                response_text = f"I've added the task '{title}' to your list (ID: {new_task.id})."
            else:
                response_text = "I need a title for the new task. Please specify what task you'd like to add."
                task_operations["add_task"] = {"status": "error", "message": "No task title found in message"}

        elif any(word in message_lower for word in ["list", "show", "display", "get"]) and any(word in message_lower for word in ["task", "todo", "my"]):
            # List tasks for the user using shared service
            from app.services.task_service import TaskService
            tasks = TaskService.get_tasks_for_user(session, effective_user_id)
            print(f"Fetched {len(tasks)} tasks for user {effective_user_id}")

            tool_calls.append({"name": "list_tasks", "arguments": {"count": len(tasks)}})

            if tasks:
                # Create a detailed list with IDs
                task_details = []
                for task in tasks:
                    status = 'completed' if task.completed else 'pending'
                    task_details.append(f"- #{task.id}: {task.title} ({status})")

                response_text = f"Here are your {len(tasks)} tasks:\n" + "\n".join(task_details)
                task_operations["list_tasks"] = {
                    "status": "success",
                    "count": len(tasks),
                    "tasks": [{"id": task.id, "title": task.title, "completed": task.completed} for task in tasks]
                }
            else:
                response_text = "You have no tasks."
                task_operations["list_tasks"] = {"status": "success", "count": 0, "tasks": []}

        elif any(word in message_lower for word in ["complete", "finish", "done", "mark"]) and any(word in message_lower for word in ["task", "todo"]):
            # Extract task ID - look for numbers in the message
            import re
            id_matches = re.findall(r'#?(\d+)', request.message)

            if id_matches:
                # Take the first number found as the task ID
                task_id = int(id_matches[0])
                print(f"Toggling completion for task {task_id} for user {effective_user_id}")

                # Use shared service to update task status
                from app.services.task_service import TaskService
                updated_task = TaskService.toggle_task_completion(session, task_id, effective_user_id)

                if updated_task:
                    response_text = f"I've marked task #{task_id} '{updated_task.title}' as completed."
                    print(f"Successfully completed task {task_id}")

                    tool_calls.append({"name": "complete_task", "arguments": {"task_id": task_id}})
                    task_operations["complete_task"] = {
                        "status": "success",
                        "task_id": task_id,
                        "title": updated_task.title,
                        "completed": updated_task.completed
                    }
                else:
                    response_text = f"Task #{task_id} not found."
                    print(f"Task {task_id} not found for user {effective_user_id}")

                    task_operations["complete_task"] = {
                        "status": "error",
                        "task_id": task_id,
                        "message": "Task not found"
                    }
            else:
                response_text = "Please specify which task number you'd like to complete (e.g., 'complete task 1')."
                task_operations["complete_task"] = {"status": "error", "message": "No task ID found in message"}

        elif any(word in message_lower for word in ["delete", "remove", "cancel"]) and any(word in message_lower for word in ["task", "todo"]):
            # Extract task ID
            import re
            id_matches = re.findall(r'#?(\d+)', request.message)

            if id_matches:
                task_id = int(id_matches[0])
                print(f"Deleting task {task_id} for user {effective_user_id}")

                # Use shared service to delete task
                from app.services.task_service import TaskService
                success = TaskService.delete_task(session, task_id, effective_user_id)

                if success:
                    response_text = f"I've deleted task #{task_id}."
                    print(f"Successfully deleted task {task_id}")

                    tool_calls.append({"name": "delete_task", "arguments": {"task_id": task_id}})
                    task_operations["delete_task"] = {"status": "success", "task_id": task_id}
                else:
                    response_text = f"Task #{task_id} not found."
                    print(f"Task {task_id} not found for user {effective_user_id}")

                    task_operations["delete_task"] = {
                        "status": "error",
                        "task_id": task_id,
                        "message": "Task not found"
                    }
            else:
                response_text = "Please specify which task number you'd like to delete (e.g., 'delete task 1')."
                task_operations["delete_task"] = {"status": "error", "message": "No task ID found in message"}

        elif any(word in message_lower for word in ["update", "change", "modify"]) and any(word in message_lower for word in ["task", "todo"]):
            # Handle task updates - look for task ID and new information
            import re
            id_matches = re.findall(r'#?(\d+)', request.message)

            if id_matches:
                task_id = int(id_matches[0])

                # Look for title updates
                title_update_match = re.search(r'(?:to|as|is) "([^"]*)"', request.message)

                if title_update_match:
                    new_title = title_update_match.group(1).strip()

                    from app.services.task_service import TaskService
                    from app.models.chat_models import TaskUpdate as ModelTaskUpdate

                    update_data = ModelTaskUpdate(title=new_title)
                    updated_task = TaskService.update_task(session, task_id, effective_user_id, update_data)

                    if updated_task:
                        response_text = f"I've updated task #{task_id} title to '{new_title}'."

                        tool_calls.append({"name": "update_task", "arguments": {"task_id": task_id, "field": "title", "value": new_title}})
                        task_operations["update_task"] = {
                            "status": "success",
                            "task_id": task_id,
                            "field": "title",
                            "new_value": new_title
                        }
                    else:
                        response_text = f"Task #{task_id} not found."
                        task_operations["update_task"] = {
                            "status": "error",
                            "task_id": task_id,
                            "message": "Task not found"
                        }
                else:
                    response_text = f"Please specify what you'd like to update for task #{task_id} (e.g., 'update task {task_id} title to \"new title\"')."
                    task_operations["update_task"] = {"status": "error", "message": "No update details found in message"}
            else:
                response_text = "Please specify which task number you'd like to update (e.g., 'update task 1')."
                task_operations["update_task"] = {"status": "error", "message": "No task ID found in message"}

        else:
            # Default response for non-task-related queries
            response_text = f"I received your message: '{request.message}'. How can I help you with your tasks today? You can say things like 'add task Buy groceries', 'list my tasks', 'complete task 1', or 'delete task 2'."
            task_operations["general_query"] = {"status": "success", "message": "General query processed"}

        # Generate or retrieve conversation ID
        conversation_id = getattr(request, 'conversation_id', None) or f"conv_{effective_user_id}_{int(datetime.now().timestamp())}"

        # Store the conversation and message in the database
        from app.models.chat_models import Conversation, Message

        # Check if conversation exists, create if not
        from sqlmodel import select
        existing_conv = session.exec(select(Conversation).where(Conversation.id == conversation_id)).first()

        if not existing_conv:
            # Create new conversation
            conversation = Conversation(
                id=conversation_id,
                user_id=effective_user_id,
                title=request.message[:50] + "..." if len(request.message) > 50 else request.message
            )
            session.add(conversation)

        # Add the user's message
        user_message = Message(
            conversation_id=conversation_id,
            user_id=effective_user_id,
            role="user",
            content=request.message
        )
        session.add(user_message)

        # Add the assistant's response
        assistant_message = Message(
            conversation_id=conversation_id,
            user_id=effective_user_id,  # The assistant acts on behalf of the user
            role="assistant",
            content=response_text
        )
        session.add(assistant_message)

        # Commit all changes
        session.commit()

        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
            tool_calls=tool_calls,
            task_operations=task_operations
        )
    except Exception as e:
        print(f"Chat processing error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing error: {str(e)}"
        )




@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}