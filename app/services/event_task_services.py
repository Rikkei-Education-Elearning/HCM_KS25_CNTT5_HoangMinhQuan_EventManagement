from sqlalchemy.orm import Session
from app.models.event import Event, EventStaff
from app.models.user import User
from app.models.event_task import EventTask
from app.schemas.event_tasks import EventTaskUpdate
from app.core.exceptions import UnauthorizedError, EventTaskNotFoundError


def get_event_task_by_id(task_id: int, user, db: Session) -> EventTask:
    """Return an event task if the user is the event owner or a staff member."""
    event_task = db.query(EventTask).filter(EventTask.id == task_id).first()

    if not event_task:
        raise EventTaskNotFoundError("Event Task not found")

    event = db.query(Event).filter(Event.id == event_task.event_id).first()
    staff = (
        db.query(EventStaff)
        .filter(EventStaff.user_id == user.id, EventStaff.event_id == event_task.event_id)
        .first()
    )

    if not staff and event.owner_id != user.id:
        raise UnauthorizedError("User not authorized to access this event task")

    return event_task


def update_event_task(task_id: int, event_task_update: EventTaskUpdate, user, db: Session) -> EventTask:
    """Partially update an event task."""
    event_task = db.query(EventTask).filter(EventTask.id == task_id).first()

    if not event_task:
        raise EventTaskNotFoundError("Event Task not found")

    event = db.query(Event).filter(Event.id == event_task.event_id).first()
    staff = (
        db.query(EventStaff)
        .filter(EventStaff.user_id == user.id, EventStaff.event_id == event_task.event_id)
        .first()
    )

    if not staff and event.owner_id != user.id:
        raise UnauthorizedError("User not authorized to access this event task")

    for key, value in event_task_update.model_dump(exclude_unset=True).items():
        setattr(event_task, key, value)

    db.commit()
    db.refresh(event_task)

    return event_task


def delete_event_task(task_id: int, user, db: Session) -> EventTask:
    """Delete an event task and return the deleted record (for response serialization)."""
    event_task = db.query(EventTask).filter(EventTask.id == task_id).first()

    if not event_task:
        raise EventTaskNotFoundError("Event Task not found")

    staff = (
        db.query(EventStaff)
        .filter(EventStaff.event_id == event_task.event_id, EventStaff.user_id == user.id)
        .first()
    )

    event = db.query(Event).filter(Event.id == event_task.event_id).first()

    if staff is None and (event is None or event.owner_id != user.id):
        raise UnauthorizedError("User not authorized to delete this event task")

    db.delete(event_task)
    db.commit()

    return event_task
