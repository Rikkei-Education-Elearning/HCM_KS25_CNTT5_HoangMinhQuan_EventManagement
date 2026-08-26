from pydantic import BaseModel, Field
from datetime import datetime


class EventResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    owner_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class EventCreate(BaseModel):
    name: str
    description: str | None = None
    created_at: datetime 

class EventUpdate(BaseModel):
    event_id: int | None = None
    name: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    priority: str | None = None
    due_date: datetime | None = None
    status: str | None = None


