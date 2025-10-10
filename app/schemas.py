from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

#user schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

#group schemas
class StudyGroupBase(BaseModel):
    name: str
    description: str
    subject: str
    is_public: bool = True

class StudyGroupCreate(StudyGroupBase):
    pass

class StudyGroupResponse(StudyGroupBase):
    id: int
    created_by: int
    created_at: datetime
    member_count: int
    session_count: int

    class Config:
        from_attributes = True

#session schemas
class StudySessionBase(BaseModel):
    title: str
    description: str
    scheduled_time: datetime
    duration_minutes: int = 60
    max_participants: int = 10
    group_id: int

class StudySessionCreate(StudySessionBase):
    pass

class StudySessionResponse(StudySessionBase):
    id: int
    created_by: int
    created_at: datetime
    group_name: str

    class Config:
        from_attributes = True

#token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None