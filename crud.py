from sqlalchemy.orm import Session
import models, schemas

# Reusable helper to add & refresh
def save_and_refresh(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance

def create_group(db: Session, group: schemas.StudyGroupCreate):
    return save_and_refresh(db, models.StudyGroup(name=group.name))

def create_user(db: Session, user: schemas.UserCreate):
    return save_and_refresh(db, models.User(**user.dict()))

def create_session(db: Session, session: schemas.StudySessionCreate):
    return save_and_refresh(db, models.StudySession(**session.dict()))

def mark_attendance(db: Session, attendance: schemas.AttendanceUpdate):
    db_record = (
        db.query(models.Attendance)
        .filter_by(user_id=attendance.user_id, session_id=attendance.session_id)
        .first()
    )

    if db_record:
        db_record.present = attendance.present
    else:
        db_record = models.Attendance(**attendance.dict())

    return save_and_refresh(db, db_record)
