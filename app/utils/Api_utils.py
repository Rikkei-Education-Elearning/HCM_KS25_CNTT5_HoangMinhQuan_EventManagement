from pydantic import BaseModel 
from typing import Any
from datetime import datetime

class APIResponse (BaseModel):
    statusCode: int
    message: str
    data: Any | None = None
    error: str | None = None
    timestamp: datetime
    path: str

def CreateResponse(statusCode: int, message: str, data: Any | None, error: str | None = None, path: str = ""):
    return APIResponse(statusCode=statusCode, message=message, data=data, error=error, timestamp=datetime.now(), path=path)