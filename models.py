from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class StudyGroup(Base):
    __tablename__ = "study_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    members = relationship("User", back_populates="group")
    sessions = relationship("StudySession", back_populates="group")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    group_id = Column(Integer, ForeignKey("study_groups.id"))
    group = relationship("StudyGroup", back_populates="members")
    attendance = relationship("Attendance", back_populates="user")

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    scheduled_time = Column(DateTime, default=datetime.datetime.utcnow)
    group_id = Column(Integer, ForeignKey("study_groups.id"))
    group = relationship("StudyGroup", back_populates="sessions")
    attendance = relationship("Attendance", back_populates="session")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(Integer, ForeignKey("study_sessions.id"))
    present = Column(Boolean, default=False)
    user = relationship("User", back_populates="attendance")
    session = relationship("StudySession", back_populates="attendance")
