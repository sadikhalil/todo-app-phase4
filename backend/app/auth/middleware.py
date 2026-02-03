"""Authentication middleware for FastAPI application."""

from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.auth.service import auth_service


class AuthMiddleware:
    """Authentication middleware to protect API routes."""

    def __init__(self):
        self.security = HTTPBearer(auto_error=False)

    async def __call__(self, request: Request):
        """Process incoming request and validate authentication."""
        # Extract authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is required"
            )

        # Verify the token
        auth_result = auth_service.authenticate_request(auth_header)

        if not auth_result or not auth_result.get("authenticated"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        # Attach user info to request for downstream handlers
        request.state.user = auth_result["user"]
        return auth_result["user"]


# Global auth middleware instance
auth_middleware = AuthMiddleware()