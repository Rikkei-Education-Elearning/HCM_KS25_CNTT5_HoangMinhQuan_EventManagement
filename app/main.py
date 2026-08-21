from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import auth, event, event_task, users
from app.routers.health import router as health_router
from app.core.exception_handler import exception_handler
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.event import router as event_router
from app.routers.event_task import router as event_task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management API")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(event_router)
app.include_router(event_task_router)
app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "Event Management API"}
