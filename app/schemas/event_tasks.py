from pydantic import BaseModel
from datetime import datetime 

class EventTaskCreate(BaseModel):
    event_id: int
    title: str
    description: str
    assignee_id: int
    status: str
    priority: str
    due_date: datetime
    created_at: datetime

class EventTasks(BaseModel):
    id: int
    event_id: int
    assignee_id: int
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime

    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    event_task_id: int
    title: str
    description: str
    assignee_id: int
    status: str
    priority: str
    due_date: datetime

class EventTaskDelete(BaseModel):
    event_task_id: int

