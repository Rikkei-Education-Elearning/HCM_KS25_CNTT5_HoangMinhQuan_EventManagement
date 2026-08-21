from pydantic import BaseModel
from datetime import datetime

class Users(BaseModel):
    id: int
    email: str 
    full_name: str
    is_active: bool
    created_at: datetime    