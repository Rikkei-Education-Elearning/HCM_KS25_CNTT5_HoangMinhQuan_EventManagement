import datetime
from sqlalchemy.orm import Session
from app.schemas.events import EventCreate, EventUpdate
from app.schemas.members import MemberResponse, RoleResponse
from app.schemas.event_tasks import EventTaskCreate
from app.models.event import Event, EventStaff
from app.models.user import User
from app.models.event_task import EventTask
from app.core.exceptions import (
    BadRequestError,
    UnauthorizedError,
    EventNotFoundError,
    UserNotFoundError,
    EventTaskNotFoundError,
)


# ──────────────────────────────── Event CRUD ────────────────────────────────

def create_new_event(owner, event: EventCreate, db: Session) -> Event:
    if len(event.name) < 1:
        raise BadRequestError("Event name must be a valid string")

    if len(event.name) > 80:
        raise BadRequestError("Event name must be less than 80 characters")

    new_event = Event(
        name=event.name,
        description=event.description,
        owner_id=owner.id,
        created_at=event.created_at or datetime.datetime.now(datetime.timezone.utc),
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


def get_event_by_name_or_owner(user, event_name: str | None, db: Session) -> Event:
    """Return event matching name (partial) or fall back to the first event owned by user."""
    event = None
    if event_name:
        event = db.query(Event).filter(Event.name.like(f"%{event_name}%")).first()

    if not event:
        event = db.query(Event).filter(Event.owner_id == user.id).first()

    if not event:
        raise EventNotFoundError("Event not found")

    return event


def get_event_by_id_authorized(event_id: int, user, db: Session) -> Event:
    """Return event by ID if the user is owner or a staff member."""
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise EventNotFoundError("Event not found")

    is_staff = (
        db.query(EventStaff)
        .filter(EventStaff.event_id == event_id, EventStaff.user_id == user.id)
        .first()
    )

    if not is_staff and event.owner_id != user.id:
        raise UnauthorizedError("User not authorized to access this event")

    return event


def update_event_by_id(event_id: int, event_update: EventUpdate, user, db: Session) -> Event:
    if not user:
        raise UnauthorizedError("User not authenticated")

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise EventNotFoundError("Event not found")

    if event.owner_id != user.id:
        raise UnauthorizedError("User not authorized to update this event")

    for key, value in event_update.model_dump(exclude_unset=True).items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)

    return event


def patch_event_by_id(event_id: int, event_update: EventUpdate, user, db: Session) -> Event:
    if not user:
        raise UnauthorizedError("User not authenticated")

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise EventNotFoundError("Event not found")

    if event.owner_id != user.id:
        raise UnauthorizedError("User not authorized to update this event")

    for key, value in event_update.model_dump(exclude_unset=True).items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)

    return event


def delete_event_by_id(event_id: int, user, db: Session) -> str:
    try:
        if not user:
            raise UnauthorizedError("User not authenticated")

        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise EventNotFoundError("Event not found")

        if event.owner_id != user.id:
            raise UnauthorizedError("User not authorized to delete this event")

        db.delete(event)
        db.commit()

        return "Event deleted successfully"

    except Exception as e:
        db.rollback()
        raise e


# ──────────────────────────────── Event Members ────────────────────────────────

def add_member_to_event(event_id: int, user_id: int, current_user, db: Session) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise EventNotFoundError("Event not found")

    if event.owner_id != current_user.id:
        raise UnauthorizedError("User not authorized to add members to this event")

    if (
        db.query(EventStaff)
        .filter(EventStaff.event_id == event_id, EventStaff.user_id == user_id)
        .first()
    ):
        raise BadRequestError("User is already a member of this event")

    new_member_user = db.query(User).filter(User.id == user_id).first()
    if not new_member_user:
        raise UserNotFoundError("User not found")

    new_staff = EventStaff(
        event_id=event_id,
        user_id=new_member_user.id,
        role=new_member_user.role_id,
        joined_at=datetime.datetime.now(datetime.timezone.utc),
    )
    db.add(new_staff)
    db.commit()
    db.refresh(event)

    return event


def remove_member_from_event(event_id: int, user_id: int, current_user, db: Session) -> None:
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise EventNotFoundError("Event not found")

    if event.owner_id != current_user.id:
        raise UnauthorizedError("User not authorized to remove members from this event")

    member_to_remove = db.query(User).filter(User.id == user_id).first()
    if not member_to_remove:
        raise UserNotFoundError("User not found")

    if member_to_remove.id == current_user.id:
        raise BadRequestError("You cannot remove yourself from the event")

    member_record = (
        db.query(EventStaff)
        .filter(EventStaff.event_id == event_id, EventStaff.user_id == user_id)
        .first()
    )

    if not member_record:
        raise BadRequestError("User is not a member of this event")

    db.delete(member_record)
    db.commit()


def get_event_members(
    event_id: int, page: int, limit: int, current_user, db: Session
) -> list[MemberResponse]:
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise EventNotFoundError("Event not found")

    if event.owner_id != current_user.id:
        raise UnauthorizedError("User not authorized to view members of this event")

    members = (
        db.query(User, EventStaff)
        .join(EventStaff, User.id == EventStaff.user_id)
        .filter(EventStaff.event_id == event_id)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return [
        MemberResponse(
            id=m.User.id,
            email=m.User.email,
            full_name=m.User.full_name,
            role=(
                RoleResponse(id=m.EventStaff.role.id, name=m.EventStaff.role.name)
                if m.EventStaff.role
                else None
            ),
            joined_at=m.EventStaff.joined_at,
        )
        for m in members
    ]


# ──────────────────────────────── Event Tasks ────────────────────────────────

def create_event_task(event_task: EventTaskCreate, member, db: Session) -> EventTask:
    event = db.query(Event).filter(Event.id == event_task.event_id).first()

    if not event:
        raise EventNotFoundError("Event not found")

    event_staff = (
        db.query(EventStaff)
        .filter(EventStaff.event_id == event_task.event_id, EventStaff.user_id == member.id)
        .first()
    )

    if not event_staff and event.owner_id != member.id:
        raise UnauthorizedError("User not authorized to create tasks for this event")

    # Owner can assign to anyone; staff can only assign to themselves
    if event.owner_id != member.id and event_task.assignee_id != member.id:
        raise BadRequestError("You can only assign tasks to yourself")

    new_task = EventTask(
        event_id=event_task.event_id,
        assignee_id=event_task.assignee_id,
        title=event_task.title,
        description=event_task.description,
        status=event_task.status,
        priority=event_task.priority,
        due_date=event_task.due_date,
        created_at=datetime.datetime.now(),
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_all_event_tasks(
    event_id: int, page: int, limit: int, user, db: Session
) -> list[EventTask]:
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise EventNotFoundError("Event not found")

    event_staff = (
        db.query(EventStaff)
        .filter(EventStaff.event_id == event_id, EventStaff.user_id == user.id)
        .first()
    )

    if not event_staff and event.owner_id != user.id:
        raise UnauthorizedError("User not authorized to view tasks for this event")

    tasks = (
        db.query(EventTask)
        .filter(EventTask.event_id == event_id)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    if not tasks:
        raise EventTaskNotFoundError("No event tasks found")

    return tasks