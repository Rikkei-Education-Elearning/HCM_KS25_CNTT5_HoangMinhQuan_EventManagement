from fastapi import APIRouter
from app.db.database import engine

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/health")
def health_check():
    if engine.connect():
        return {"status": "healthy"}
    else:
        return {"status": "unhealthy"}






