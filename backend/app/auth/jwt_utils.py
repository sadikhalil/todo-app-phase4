"""JWT token utilities for authentication."""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from .models import User


class JWTManager:
    """Manages JWT token creation and validation."""

    def __init__(self, secret_key: str = "todo_app_secret_key_change_in_prod", algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry = timedelta(hours=24)  # Token expires in 24 hours

    def generate_token(self, user: User) -> str:
        """Generate JWT token for a user."""
        payload = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + self.token_expiry,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode and validate JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Invalid token
            return None

    def validate_token(self, token: str) -> bool:
        """Validate JWT token."""
        decoded = self.decode_token(token)
        return decoded is not None

    def get_user_from_token(self, token: str) -> Optional[User]:
        """Extract user information from token."""
        decoded = self.decode_token(token)
        if decoded:
            from .models import user_storage
            return user_storage.get_user_by_id(decoded["user_id"])
        return None


# Global JWT manager instance
jwt_manager = JWTManager()