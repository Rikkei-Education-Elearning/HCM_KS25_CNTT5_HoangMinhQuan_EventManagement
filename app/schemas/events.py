from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    created_at: datetime
    owner: User
    
class EventCreate(BaseModel):
    name: str
    description: str
    owner_id: int
    created_at: datetime

class EventUpdate(BaseModel):
    event_id: int
    name: str
    description: str
    assignee_id: int
    priority: str
    due_date: datetime
    status: str


