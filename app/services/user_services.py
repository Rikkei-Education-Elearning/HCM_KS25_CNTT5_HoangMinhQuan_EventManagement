import bcrypt
from sqlalchemy.orm import Session
from app.core.exceptions import EmailAlreadyExistsError, UserNotFoundError, UnauthorizedError
from app.models.user import User
from app.schemas.auth import UserRegister


def create_new_user(user: UserRegister, db: Session) -> User:
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise EmailAlreadyExistsError()

    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(
        email=user.email,
        hashed_password=hashed,
        full_name=user.full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_current_user_profile(current_user, db: Session) -> User:
    """Return the full User record for the authenticated user."""
    user = db.query(User).filter(User.email == current_user.email).first()
    if user is None:
        raise UserNotFoundError()
    return user


def get_users_list(
    current_user,
    email: str,
    is_active: bool | None,
    page: int,
    limit: int,
    db: Session,
) -> list[User]:
    """Return a paginated, optionally-filtered list of users (admin only)."""
    if not current_user:
        raise UnauthorizedError("User not authenticated")

    query = db.query(User)
    if email:
        query = query.filter(User.email.like(f"%{email}%"))
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.offset((page - 1) * limit).limit(limit).all()