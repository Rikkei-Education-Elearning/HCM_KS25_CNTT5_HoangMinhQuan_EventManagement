from pydantic import BaseModel
from datetime import datetime

class AttachmentCreate(BaseModel):
    attachment_id: int
    file_name: str
    file_path: str
    file_type: str
    file_size: int
    upload_date: datetime
    upload_by: int
    upload_to: int
    upload_to_type: str
    upload_to_id: int
    upload_to_type: str