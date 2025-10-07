"""
Data models for StudySync API
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


class UserModel(BaseModel):
    """User data model"""
    username: str = Field(..., min_length=2, max_length=50)
    email: Optional[str] = None
    display_name: Optional[str] = None
    
    @validator('email')
    def validate_email(cls, v):
        if v is not None:
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, v):
                raise ValueError('Invalid email format')
        return v


class GroupCreateModel(BaseModel):
    """Model for creating a study group"""
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    max_members: int = Field(default=10, ge=1, le=100)
    
    @validator('name')
    def validate_name(cls, v):
        import re
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', v):
            raise ValueError('Group name can only contain alphanumeric characters, spaces, hyphens, and underscores')
        return v


class GroupUpdateModel(BaseModel):
    """Model for updating a study group"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    max_members: Optional[int] = Field(None, ge=1, le=100)


class GroupModel(BaseModel):
    """Study group data model"""
    id: str
    name: str
    description: str = ""
    max_members: int = 10
    created_at: datetime
    members: List[Dict[str, Any]] = []
    sessions: List[str] = []  # Session IDs


class SessionCreateModel(BaseModel):
    """Model for creating a study session"""
    group_id: str
    topic: str = Field(..., min_length=1, max_length=200)
    start_time: datetime
    duration_minutes: int = Field(..., ge=15, le=480)  # 15 minutes to 8 hours
    description: Optional[str] = Field(None, max_length=1000)
    
    @validator('start_time')
    def validate_future_time(cls, v):
        if v <= datetime.now():
            raise ValueError('Session must be scheduled for future time')
        return v


class SessionUpdateModel(BaseModel):
    """Model for updating a study session"""
    topic: Optional[str] = Field(None, min_length=1, max_length=200)
    start_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=15, le=480)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None, regex=r'^(scheduled|active|completed|cancelled)$')


class SessionModel(BaseModel):
    """Study session data model"""
    id: str
    group_id: str
    topic: str
    start_time: datetime
    duration_minutes: int
    status: str = "scheduled"
    description: str = ""
    created_at: datetime
    attendees: List[Dict[str, Any]] = []
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None


class AttendeeModel(BaseModel):
    """Session attendee model"""
    username: str
    status: str = Field(default="confirmed", regex=r'^(confirmed|tentative|declined)$')
    joined_at: datetime = Field(default_factory=datetime.now)


class JoinGroupModel(BaseModel):
    """Model for joining a group"""
    username: str = Field(..., min_length=2, max_length=50)
    user_info: Optional[Dict[str, Any]] = None


class SessionAttendanceModel(BaseModel):
    """Model for session attendance"""
    username: str
    status: str = Field(..., regex=r'^(confirmed|tentative|declined)$')


class NotificationTestModel(BaseModel):
    """Model for testing notifications"""
    channels: List[str] = Field(default=["email"], regex=r'^(email|slack|discord)$')
    message: Optional[str] = None


class AnalyticsQuery(BaseModel):
    """Model for analytics queries"""
    group_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    period: str = Field(default="last-week", regex=r'^(today|last-week|last-month|all)$')


class AnalyticsResponse(BaseModel):
    """Analytics response model"""
    total_sessions: int = 0
    completed_sessions: int = 0
    cancelled_sessions: int = 0
    total_participants: int = 0
    average_duration: float = 0.0
    most_active_group: str = ""
    daily_breakdown: Dict[str, int] = {}
    status_breakdown: Dict[str, int] = {}


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


class SuccessResponse(BaseModel):
    """Success response model"""
    message: str
    data: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = "healthy"
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)
    database_status: str = "connected"
    uptime_seconds: float = 0.0


class ConfigResponse(BaseModel):
    """Configuration response model"""
    debug_mode: bool
    database_type: str
    notification_channels: List[str]
    max_group_size: int
    version: str