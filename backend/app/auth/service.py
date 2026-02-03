"""Authentication service for user registration and login."""

from typing import Dict, Any, Optional
from .models import User, user_storage
from .jwt_utils import jwt_manager


class AuthService:
    """Authentication service handling user registration and login."""

    @staticmethod
    def signup(email: str, password: str) -> Dict[str, Any]:
        """Register a new user."""
        # Check if user already exists
        existing_user = user_storage.get_user_by_email(email)
        if existing_user:
            return {
                "success": False,
                "message": "User with this email already exists",
                "token": None
            }

        # Validate email format (basic validation)
        if "@" not in email or "." not in email:
            return {
                "success": False,
                "message": "Invalid email format",
                "token": None
            }

        # Validate password length
        if len(password) < 6:
            return {
                "success": False,
                "message": "Password must be at least 6 characters long",
                "token": None
            }

        # Create new user
        user = User(email=email, password=password)
        user_storage.add_user(user)

        # Generate JWT token
        token = jwt_manager.generate_token(user)

        return {
            "success": True,
            "message": "User registered successfully",
            "token": token,
            "user": user.to_dict()
        }

    @staticmethod
    def login(email: str, password: str) -> Dict[str, Any]:
        """Authenticate user and return JWT token."""
        user = user_storage.get_user_by_email(email)

        if not user:
            return {
                "success": False,
                "message": "Invalid email or password",
                "token": None
            }

        if not user.verify_password(password):
            return {
                "success": False,
                "message": "Invalid email or password",
                "token": None
            }

        # Generate JWT token
        token = jwt_manager.generate_token(user)

        return {
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": user.to_dict()
        }

    @staticmethod
    def authenticate_request(token: str) -> Optional[Dict[str, Any]]:
        """Authenticate a request using JWT token."""
        if not token:
            return None

        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]

        # Decode and validate token
        user = jwt_manager.get_user_from_token(token)

        if user:
            return {
                "authenticated": True,
                "user": user,
                "token_valid": True
            }

        return {
            "authenticated": False,
            "user": None,
            "token_valid": False
        }


# Global auth service instance
auth_service = AuthService()