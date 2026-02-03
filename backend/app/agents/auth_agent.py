"""Auth Agent - Handles user authentication and authorization for the Todo application.

Responsibilities:
• Allow users to sign up with email and password
• Allow users to log in with email and password
• Issue a JWT token on successful authentication
• Validate JWT tokens on protected requests
• Extract user identity from JWT token
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from ..auth.service import auth_service


class AuthAgent:
    """Authentication agent for handling user authentication operations."""

    def signup(self, email: str, password: str, confirm_password: str = None) -> Dict[str, Any]:
        """Register a new user account."""
        # If confirm_password is provided, validate that passwords match
        if confirm_password and password != confirm_password:
            return {
                "success": False,
                "message": "Passwords do not match",
                "token": None
            }

        # Use the auth service for signup
        return auth_service.signup(email, password)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Log in an existing user."""
        # Use the auth service for login
        return auth_service.login(email, password)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return user information."""
        return auth_service.authenticate_request(token)

    def authenticate_request(self, auth_header: str) -> Optional[Dict[str, Any]]:
        """Authenticate a request using authorization header."""
        if not auth_header:
            return None

        # Extract token from header (remove 'Bearer ' prefix)
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
        else:
            token = auth_header

        return self.verify_token(token)


# Global auth agent instance
auth_agent = AuthAgent()