from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from ..models.user import User
from ..auth.jwt import get_password_hash, verify_password, create_access_token
from ..schemas.task import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, register_data: RegisterRequest) -> Optional[User]:
        """
        Register a new user.

        Args:
            register_data: Registration data containing email and password

        Returns:
            User object if registration successful, None if email already exists
        """
        # Check if user already exists
        existing_user = self.db.query(User).filter(User.email == register_data.email).first()
        if existing_user:
            return None

        # Create new user
        hashed_password = get_password_hash(register_data.password)
        user = User(
            email=register_data.email,
            password_hash=hashed_password
        )

        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            return None

    def authenticate_user(self, login_data: LoginRequest) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            login_data: Login data containing email and password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = self.db.query(User).filter(User.email == login_data.email).first()

        if not user or not verify_password(login_data.password, user.password_hash):
            return None

        return user

    def create_login_response(self, user: User) -> dict:
        """
        Create a login response with JWT token.

        Args:
            user: Authenticated user object

        Returns:
            Dictionary containing access token and user info
        """
        access_token_expires = timedelta(minutes=1440)  # 24 hours
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 86400,  # 24 hours in seconds
            "user": {
                "id": str(user.id),
                "email": user.email
            }
        }