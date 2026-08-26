from pydantic import BaseModel
from datetime import datetime

class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class AddMember(BaseModel):
    event_id: int
    user_id: int

class MemberResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: RoleResponse | None
    joined_at: datetime

    class Config:
        from_attributes = True

class MemberDelete(BaseModel):
    event_id: int
    user_id: int

