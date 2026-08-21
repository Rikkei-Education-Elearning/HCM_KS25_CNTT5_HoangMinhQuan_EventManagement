from pydantic import BaseModel

class AddMember(BaseModel):
    event_id: int
    user_id: int

class MemberResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True

class MemberDelete(BaseModel):
    event_id: int
    user_id: int

