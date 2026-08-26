from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import UserNotFoundError, EventNotFoundError, EventTaskNotFoundError, BadRequestError, UnauthorizedError, ForbiddenError, EmailAlreadyExistsError, InvalidPasswordOrEmailError, TokenExpiredError, TooManyLoginAttemts
from app.utils.Api_utils import *

async def exception_handler(request: Request, exc: Exception):
    if isinstance(exc, UserNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content=CreateResponse(statusCode = status.HTTP_404_NOT_FOUND, error = "User not found", message = exc.message, data = None, path = request.url.path).model_dump(mode="json")
        )
    elif isinstance(exc, EventNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content=CreateResponse(statusCode = status.HTTP_404_NOT_FOUND, error = "Event not found", message = exc.message, data = None, path = request.url.path).model_dump(mode="json")
        )
    elif isinstance(exc, EventTaskNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content=CreateResponse(statusCode = status.HTTP_404_NOT_FOUND, error = "Event task not found", message = exc.message, data = None, path = request.url.path).model_dump(mode="json")
        )
    elif isinstance(exc, BadRequestError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content=CreateResponse(statusCode = status.HTTP_400_BAD_REQUEST, error = exc.message or "Bad request", message = exc.message, data = None, path = request.url.path).model_dump(mode="json")
        )
    elif isinstance(exc, UnauthorizedError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            content=CreateResponse(statusCode = status.HTTP_401_UNAUTHORIZED, error = exc.message or "Unauthorized", message = exc.message, data = None, path = request.url.path).model_dump(mode="json")
        )
    elif isinstance(exc, ForbiddenError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, 
            content=CreateResponse(statusCode = status.HTTP_403_FORBIDDEN, error = "Forbidden", message = exc.message, data = None, path = request.url.path).model_dump(mode="json")
        )
    elif isinstance(exc, EmailAlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content=CreateResponse(statusCode = status.HTTP_400_BAD_REQUEST, error = "Email already exists", message = exc.message, data = None, path = request.url.path).model_dump(mode="json")
        )
    elif isinstance(exc, InvalidPasswordOrEmailError):
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST, 
            content=CreateResponse(statusCode = status.HTTP_400_BAD_REQUEST, error = "Invalid password or email", message = exc.message, data = None, path = request.url.path).model_dump(mode="json")
        )
    elif isinstance(exc, TokenExpiredError):
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED, 
            content=CreateResponse(statusCode = status.HTTP_401_UNAUTHORIZED, error = "Token expired", message = exc.message, data = None, path = request.url.path).model_dump(mode="json")
        )
    elif isinstance(exc, TooManyLoginAttemts):
        return JSONResponse(
            status_code= status.HTTP_429_TOO_MANY_REQUESTS, 
            content=CreateResponse(statusCode = status.HTTP_429_TOO_MANY_REQUESTS, error = "Too many login attempts. Please try again later.", message = exc.message, data = None, path = request.url.path).model_dump(mode="json")
        )
