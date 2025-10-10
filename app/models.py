from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from auth import get_password_hash

#base directly from database
from database import Base

#association table for many-to-many relationship between users and study groups
user_group_association = Table(
    'user_group_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('study_groups.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    #relationships
    study_groups = relationship("StudyGroup", secondary=user_group_association, back_populates="members")
    created_sessions = relationship("StudySession", back_populates="creator")
    
    def set_password(self, password: str):
        self.hashed_password = get_password_hash(password)

class StudyGroup(Base):
    __tablename__ = "study_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    subject = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_public = Column(Boolean, default=True)
    
    #relationships
    members = relationship("User", secondary=user_group_association, back_populates="study_groups")
    study_sessions = relationship("StudySession", back_populates="study_group")

class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    scheduled_time = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer, default=60)
    max_participants = Column(Integer, default=10)
    group_id = Column(Integer, ForeignKey("study_groups.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    #relationships
    study_group = relationship("StudyGroup", back_populates="study_sessions")
    creator = relationship("User", back_populates="created_sessions")