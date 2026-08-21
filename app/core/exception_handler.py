from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import UserNotFoundError, EventNotFoundError, EventTaskNotFoundError, BadRequestError, UnauthorizedError, ForbiddenError

async def exception_handler(request: Request, exc: Exception):
    if isinstance(exc, UserNotFoundError):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})
    elif isinstance(exc, EventNotFoundError):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Event not found"})
    elif isinstance(exc, EventTaskNotFoundError):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Event task not found"})
    elif isinstance(exc, BadRequestError):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Bad request"})
    elif isinstance(exc, UnauthorizedError):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Unauthorized"})
    elif isinstance(exc, ForbiddenError):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Forbidden"})