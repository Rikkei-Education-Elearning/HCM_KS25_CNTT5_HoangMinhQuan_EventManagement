from pydantic import BaseModel

class commentCreate(BaseModel):
    comment_id: int
    content: str