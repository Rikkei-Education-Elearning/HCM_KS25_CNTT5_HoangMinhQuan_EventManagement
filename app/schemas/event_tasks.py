from pydantic import BaseModel
from datetime import datetime 
from enum import Enum 

class EventTaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class EventTaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class EventTaskCreate(BaseModel):
    event_id: int
    title: str
    description: str
    assignee_id: int
    status: EventTaskStatus
    priority: EventTaskPriority
    due_date: datetime
    created_at: datetime 

class EventTaskResponse(BaseModel):
    id: int  
    event_id: int
    assignee_id: int | None
    title: str | None
    description: str | None
    status: str
    priority: str
    due_date: datetime | None
    created_at: datetime | None

    class Config:
        from_attributes = True

class EventTaskUpdate(BaseModel):
    event_task_id: int | None = None
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    status: EventTaskStatus | None = EventTaskStatus.pending
    priority: EventTaskPriority | None = EventTaskPriority.medium
    due_date: datetime | None = None

class EventTaskDelete(BaseModel):
    event_task_id: int

