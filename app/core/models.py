from pydantic import BaseModel
from typing import Optional

class ListCreate(BaseModel):
    title: str
    report_id: str

class ListUpdate(BaseModel):
    title: Optional[str] = None
    report_id: str

class Task(BaseModel):
    title: str