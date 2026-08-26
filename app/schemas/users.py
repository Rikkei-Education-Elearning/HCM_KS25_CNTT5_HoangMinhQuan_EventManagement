from pydantic import BaseModel
from datetime import datetime


class Users(BaseModel):
    id: int
    email: str
    full_name: str | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True} 

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str 