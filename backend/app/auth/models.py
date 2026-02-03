"""User model and authentication utilities."""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4


class User:
    """User model for storing user information."""

    def __init__(self, email: str, password: str):
        self.id = str(uuid4())
        self.email = email
        self.password_hash, self.salt = self._hash_password(password)
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def _hash_password(self, password: str) -> tuple[str, str]:
        """Hash password with salt using SHA-256."""
        salt = secrets.token_hex(32)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return password_hash, salt

    def verify_password(self, password: str) -> bool:
        """Verify password against hash."""
        password_hash = hashlib.sha256((password + self.salt).encode()).hexdigest()
        return password_hash == self.password_hash

    def to_dict(self, include_password: bool = False):
        """Convert user to dictionary representation."""
        data = {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if include_password:
            data["password_hash"] = self.password_hash
            data["salt"] = self.salt
        return data


class UserStorage:
    """In-memory storage for users."""

    def __init__(self):
        self.users = {}  # email -> User mapping
        self.user_ids = {}  # id -> User mapping

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.users.get(email)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.user_ids.get(user_id)

    def add_user(self, user: User):
        """Add a user to storage."""
        self.users[user.email] = user
        self.user_ids[user.id] = user
        return user

    def update_user(self, user: User):
        """Update a user in storage."""
        if user.email in self.users:
            self.users[user.email] = user
            self.user_ids[user.id] = user
            user.updated_at = datetime.now().isoformat()
            return user
        return None


# Global user storage instance
user_storage = UserStorage()