from sqlalchemy.orm import Session
import models, schemas

def create_group(db: Session, group: schemas.StudyGroupCreate):
    db_group = models.StudyGroup(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_session(db: Session, session: schemas.StudySessionCreate):
    db_session = models.StudySession(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def mark_attendance(db: Session, attendance: schemas.AttendanceUpdate):
    db_record = db.query(models.Attendance).filter_by(user_id=attendance.user_id, session_id=attendance.session_id).first()
    if db_record:
        db_record.present = attendance.present
    else:
        db_record = models.Attendance(**attendance.dict())
        db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
