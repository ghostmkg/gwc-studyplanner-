from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, crud, schemas
from database import engine, get_db
import notifications

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="StudySync")

@app.post("/groups/")
def create_group(group: schemas.StudyGroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db, group)

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/sessions/")
def create_session(session: schemas.StudySessionCreate, db: Session = Depends(get_db)):
    new_session = crud.create_session(db, session)
    # Send reminders to all group members (using scheduled reminders)
    for member in new_session.group.members:
        notifications.schedule_session_reminder(
            user_email=member.email,
            topic=new_session.topic,
            session_time=new_session.scheduled_time,
            reminder_minutes=30  # Reminder 30 mins before
        )
    return new_session

@app.put("/attendance/")
def update_attendance(attendance: schemas.AttendanceUpdate, db: Session = Depends(get_db)):
    return crud.mark_attendance(db, attendance)
