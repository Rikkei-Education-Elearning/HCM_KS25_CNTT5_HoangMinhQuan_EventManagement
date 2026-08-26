from app.core.exceptions import ForbiddenError
from app.core.exceptions import UnauthorizedError
from fastapi import APIRouter, Depends, Form, status, Query
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas.events import EventCreate, EventUpdate, EventResponse
from app.schemas.members import MemberResponse
from app.schemas.event_tasks import EventTaskCreate, EventTaskResponse
from app.services.event_services import (
    create_new_event,
    get_event_by_name_or_owner,
    get_event_by_id_authorized,
    update_event_by_id,
    patch_event_by_id,
    delete_event_by_id,
    add_member_to_event,
    remove_member_from_event,
    get_event_members,
    create_event_task,
    get_all_event_tasks,
)
from app.core.logging import logger
from app.utils.Api_utils import CreateResponse, APIResponse

router = APIRouter(prefix="/events", tags=["events"])


# ──────────────────────────────── Event CRUD ────────────────────────────────

@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_event(owner=Depends(get_current_user), event: EventCreate = Form(...), db: Session = Depends(get_db)):
    new_event = create_new_event(owner, event, db)
    logger.info(f"Event created: {new_event.name}")
    return CreateResponse(
        statusCode=status.HTTP_201_CREATED,
        message="Event created successfully",
        data=EventResponse.model_validate(new_event),
        path="/events",
    )


@router.get("", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_event(user=Depends(get_current_user), event_name: str = None, db: Session = Depends(get_db)):
    if not user:
        raise ForbiddenError("User not authenticated")
    event = get_event_by_name_or_owner(user, event_name, db)
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Event found",
        data=EventResponse.model_validate(event),
        path="/events",
    )


@router.get("/{event_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_event_by_id(event_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise UnauthorizedError("User not authenticated")
    event = get_event_by_id_authorized(event_id, user, db)
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Event found",
        data=EventResponse.model_validate(event),
        path=f"/events/{event_id}",
    )


@router.put("/{event_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_event(event_id: int, event_update: EventUpdate = Form(...), user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_event = update_event_by_id(event_id, event_update, user, db)
    logger.info(f"Event updated: {event_id}")
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Event updated",
        data=EventResponse.model_validate(new_event).model_dump(),
        path=f"/events/{event_id}",
    )


@router.patch("/{event_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def patch_event(event_id: int, event_update: EventUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_event = patch_event_by_id(event_id, event_update, user, db)
    logger.info(f"Event patched: {event_id}")
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Event patched",
        data=EventResponse.model_validate(new_event).model_dump(exclude_unset=True),
        path=f"/events/{event_id}",
    )


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    delete_event_by_id(event_id, user, db)
    logger.info(f"Event deleted: {event_id}")
    return None


# ──────────────────────────────── Members ────────────────────────────────

@router.post("/{event_id}/members", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def add_member(event_id: int, user_id: int = Form(...), current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise UnauthorizedError("User not authenticated")
    event = add_member_to_event(event_id, user_id, current_user, db)
    logger.info(f"Member added to event: {event_id}")
    return CreateResponse(
        statusCode=status.HTTP_201_CREATED,
        message="Member added to event",
        data=EventResponse.model_validate(event).model_dump(),
        path=f"/events/{event_id}/members",
    )


@router.delete("/{event_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(event_id: int, user_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise UnauthorizedError("User not authenticated")
    remove_member_from_event(event_id, user_id, current_user, db)
    logger.info(f"Member removed from event: {event_id}")
    return None


@router.get("/{event_id}/members", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_members(event_id: int, page: int = Query(ge=1, default=1), limit: int = Query(ge=1, default=5), current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise UnauthorizedError("User not authenticated")
    member_list = get_event_members(event_id, page, limit, current_user, db)
    member_data = [MemberResponse.model_validate(m) for m in member_list]
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Members retrieved successfully",
        data=member_data,
        path=f"/events/{event_id}/members",
    )


# ──────────────────────────────── Event Tasks ────────────────────────────────

@router.post("/{event_id}/event-tasks", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_task(event_task: EventTaskCreate = Form(...), member=Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = create_event_task(event_task, member, db)
    return CreateResponse(
        statusCode=status.HTTP_201_CREATED,
        message="Event task created successfully",
        data=EventTaskResponse.model_validate(new_task).model_dump(),
        path="/events/{event_id}/event-tasks",
    )


@router.get("/{event_id}/event-tasks", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_tasks(event_id: int, page: int = Query(ge=1, default=1), limit: int = Query(ge=1, default=5), user=Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = get_all_event_tasks(event_id, page, limit, user, db)
    task_data = [EventTaskResponse.model_validate(t).model_dump() for t in tasks]
    return CreateResponse(
        statusCode=status.HTTP_200_OK,
        message="Event task retrieved successfully",
        data=task_data,
        path=f"/events/{event_id}/event-tasks",
    )
