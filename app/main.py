from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import Event, EventStaff, EventTask, Role, User  # noqa: F401
from app.routers.health import router as health_router
from app.core.exception_handler import exception_handler
from app.core.exceptions import (
    BadRequestError,
    EmailAlreadyExistsError,
    EventNotFoundError,
    EventTaskNotFoundError,
    ForbiddenError,
    UnauthorizedError,
    InvalidPasswordOrEmailError,
    TooManyLoginAttemts,
    UserNotFoundError,
)
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.event import router as event_router
from app.routers.event_task import router as event_task_router
from app.core.middleware import logging_middleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management API")

for exc in (
    UserNotFoundError,
    EventNotFoundError,
    EventTaskNotFoundError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    EmailAlreadyExistsError,
    InvalidPasswordOrEmailError,
    TooManyLoginAttemts,
):
    app.add_exception_handler(exc, exception_handler)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(event_router)
app.include_router(event_task_router)
app.include_router(health_router)

app.middleware('http')(logging_middleware)

@app.get("/")
def root():
    return {"message": "Event Management API"}
