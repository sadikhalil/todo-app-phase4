"""
User Model for Authentication
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str  # Store hashed passwords
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


from pydantic import field_validator

class UserCreate(SQLModel):
    email: str
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Your password is too long. Please use a password with 72 characters or fewer.')
        return v[:72]  # Truncate to 72 characters maximum to prevent bcrypt issues


class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(SQLModel):
    id: str
    email: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class Token(SQLModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(SQLModel):
    email: Optional[str] = None