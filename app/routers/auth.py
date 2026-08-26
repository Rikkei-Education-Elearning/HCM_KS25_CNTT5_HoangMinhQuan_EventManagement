from fastapi import APIRouter, Depends, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import UserRegister
from app.schemas.users import Users
from app.services.user_services import create_new_user
from app.services.auth_services import login_user, refresh_access_token
from app.utils.Api_utils import CreateResponse, APIResponse

router = APIRouter(prefix="/auth", tags=["auth"])
token_router = APIRouter(tags=["auth"])


@router.post("/register", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister = Form(...), db: Session = Depends(get_db)):
    new_user = create_new_user(user, db)
    return CreateResponse(
        statusCode=status.HTTP_201_CREATED,
        message="User created successfully",
        data=Users.model_validate(new_user).model_dump(),
        path="/auth/register",
    )


@router.post("/login", response_model=APIResponse, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token_data = login_user(form_data.username, form_data.password, db)
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Login successful",
        data=token_data,
        path="/auth/login",
    )


@router.post("/refresh", response_model=APIResponse, status_code=status.HTTP_200_OK)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    token_data = refresh_access_token(refresh_token, db)
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Token refreshed successfully",
        data=token_data,
        path="/auth/refresh",
    )