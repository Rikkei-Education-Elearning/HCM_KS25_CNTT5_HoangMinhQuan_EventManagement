from fastapi import APIRouter, Depends, Query, status
from app.models.user import User
from app.core.security import get_current_user
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.users import Users
from app.dependencies.Authorization import require_admin
from app.services.user_services import get_current_user_profile, get_users_list
from app.utils.Api_utils import APIResponse, CreateResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_current_user_profile(current_user, db)
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        data=Users.model_validate(user).model_dump(),
        message="User retrieved successfully",
        path="/users/me",
    )


@router.get("/", response_model=list[Users], status_code=status.HTTP_200_OK)
def get_users_for_admin(
    current_user: User = Depends(require_admin),
    email: str = Query(default="", description="Email of the user to get"),
    is_active: bool | None = Query(default=None, description="Filter by active status"),
    page: int = Query(default=1, description="Page number"),
    limit: int = Query(default=5, description="Limit per page"),
    db: Session = Depends(get_db),
):
    users = get_users_list(current_user, email, is_active, page, limit, db)
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        data=users,
        message="Users retrieved successfully",
        path="/users/",
    )
