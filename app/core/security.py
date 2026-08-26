from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
from app.core.config import settings
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.database import get_db
from app.models.user import User
from app.core.exceptions import UnauthorizedError, UserNotFoundError, TokenExpiredError
from sqlalchemy.orm import Session

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

security = HTTPBearer()

def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        email: str = payload.get("sub")
        if email is None:
            raise UnauthorizedError()

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise UserNotFoundError()

        return user

    except jwt.ExpiredSignatureError:
        raise UnauthorizedError('Token expired')

    except jwt.InvalidTokenError:
        raise UnauthorizedError('Token invalid')