import jwt
import re as Regex
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.core.exceptions import (
    InvalidPasswordOrEmailError,
    TooManyLoginAttemts,
    UnauthorizedError,
    UserNotFoundError,
)
from app.models.user import User

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

# In-memory store for rate limiting (module-level so it persists across requests)
_login_attempts: dict[str, dict] = {}


def login_user(email: str, password: str, db: Session) -> dict:
    """Validate credentials, enforce rate limiting, and return token pair."""
    now = datetime.now(timezone.utc)

    # Validate email format
    if Regex.match(EMAIL_REGEX, email) is None:
        raise InvalidPasswordOrEmailError()

    # Check rate-limit block
    attempt = _login_attempts.get(email)
    if attempt:
        if attempt["blocked_until"]:
            if now < attempt["blocked_until"]:
                raise TooManyLoginAttemts()
            else:
                del _login_attempts[email]  # block period passed — reset

    # Verify credentials
    existing = db.query(User).filter(User.email == email).first()
    if not existing or not verify_password(password, existing.hashed_password):
        if email not in _login_attempts:
            _login_attempts[email] = {"count": 1, "blocked_until": None}
        else:
            _login_attempts[email]["count"] += 1

        if _login_attempts[email]["count"] >= 5:
            _login_attempts[email]["blocked_until"] = now + timedelta(minutes=15)
            raise TooManyLoginAttemts()

        raise InvalidPasswordOrEmailError()

    # Ensure account is active
    active = db.query(User).filter(User.email == email, User.is_active == True).first()
    if not active:
        raise UnauthorizedError("User account is not active")

    # Reset attempts on success
    _login_attempts.pop(email, None)

    access_token = create_access_token(data={"sub": existing.email})
    refresh_token = create_refresh_token(data={"sub": existing.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_access_token(refresh_token: str, db: Session) -> dict:
    """Validate refresh token and issue a new access token."""
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise UnauthorizedError()

        if payload.get("type") != "refresh":
            raise UnauthorizedError()

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise UserNotFoundError()

        new_access_token = create_access_token(data={"sub": user.email})

        return {
            "access_token": new_access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    except jwt.ExpiredSignatureError:
        raise UnauthorizedError()

    except jwt.InvalidTokenError:
        raise UnauthorizedError()
