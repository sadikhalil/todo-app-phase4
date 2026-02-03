from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...services.auth_service import AuthService
from ...schemas.task import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from ...models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    Creates a new user account with the provided email and password.
    """
    auth_service = AuthService(db)
    user = auth_service.register_user(register_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    return {
        "message": "User registered successfully",
        "user": {
            "id": str(user.id),
            "email": user.email
        }
    }


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.

    Verifies user credentials and returns an access token for subsequent requests.
    """
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(login_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return auth_service.create_login_response(user)