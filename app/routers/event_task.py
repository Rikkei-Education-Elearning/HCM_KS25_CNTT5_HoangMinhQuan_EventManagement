from fastapi import status, APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.event_tasks import EventTaskResponse, EventTaskUpdate
from app.core.security import get_current_user
from app.db.database import get_db
from app.services.event_task_services import (
    get_event_task_by_id,
    update_event_task,
    delete_event_task,
)
from app.utils.Api_utils import CreateResponse, APIResponse

router = APIRouter(prefix="/event-tasks", tags=["event-tasks"])


@router.get("/{id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_event_task(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    event_task = get_event_task_by_id(id, user, db)
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Event Task found",
        data=EventTaskResponse.model_validate(event_task),
        path=f"/event-tasks/{id}",
    )


@router.patch("/{id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def patch_event_task(id: int, event_task_update: EventTaskUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    event_task = update_event_task(id, event_task_update, user, db)
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Event Task updated",
        data=EventTaskResponse.model_validate(event_task),
        path=f"/event-tasks/{id}",
    )


@router.delete("/{id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def remove_event_task(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    event_task = delete_event_task(id, user, db)
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Event Task deleted",
        data=EventTaskResponse.model_validate(event_task),
        path=f"/event-tasks/{id}",
    )