from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from uuid import UUID


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = "incomplete"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v

    @validator('status')
    def validate_status(cls, v):
        if v is not None and v not in ["incomplete", "complete"]:
            raise ValueError('Status must be either "incomplete" or "complete"')
        return v

    @validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ["low", "medium", "high"]:
            raise ValueError('Priority must be "low", "medium", or "high"')
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None

    @validator('title')
    def title_must_not_be_empty_if_provided(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v

    @validator('status')
    def validate_status(cls, v):
        if v is not None and v not in ["incomplete", "complete"]:
            raise ValueError('Status must be either "incomplete" or "complete"')
        return v

    @validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ["low", "medium", "high"]:
            raise ValueError('Priority must be "low", "medium", or "high"')
        return v


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: str
    priority: Optional[str]
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class TaskStatusUpdate(BaseModel):
    status: str

    @validator('status')
    def validate_status(cls, v):
        if v not in ["incomplete", "complete"]:
            raise ValueError('Status must be either "incomplete" or "complete"')
        return v


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    pagination: dict


class TaskStatsResponse(BaseModel):
    total: int
    completed: int
    incomplete: int
    by_priority: dict


class TaskBulkUpdate(BaseModel):
    task_ids: List[UUID]
    updates: dict


class TaskBulkUpdateResponse(BaseModel):
    updated_count: int
    failed_updates: List[dict]


class ErrorResponse(BaseModel):
    error: dict


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: dict


class RegisterRequest(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    message: str
    user: dict