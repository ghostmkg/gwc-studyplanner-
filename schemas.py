from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    group_id: Optional[int]

class StudyGroupCreate(BaseModel):
    name: str

class StudySessionCreate(BaseModel):
    topic: str
    scheduled_time: datetime
    group_id: int

class AttendanceUpdate(BaseModel):
    user_id: int
    session_id: int
    present: bool
