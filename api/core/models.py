from pydantic import BaseModel
from typing import Optional

class ListCreate(BaseModel):
    title: str
    report_id: str

class ListUpdate(BaseModel):
    title: Optional[str] = None
    report_id: Optional[str] = None

class TaskCreate(BaseModel):
    list_id: int
    title: str
    type: str
    severity: str
    location: Optional[str] = None
    details: Optional[str] = None
    status: int
    archived: bool

class TaskUpdate(BaseModel):
    list_id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None
    severity: Optional[str] = None
    location: Optional[str] = None
    details: Optional[str] = None
    status: Optional[int] = None
    archived: Optional[bool] = None