from fastapi import Depends
from app.models.user import User
from app.core.security import get_current_user

from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.exceptions import UserNotFoundError, ForbiddenError


def require_admin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user.email).first()
    if user is None:
        raise UserNotFoundError()
    role_name = user.role.name if user.role is not None else None
    if role_name != "admin":
        raise ForbiddenError()
    return current_user
