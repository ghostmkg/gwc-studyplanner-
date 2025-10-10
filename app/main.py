from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
import uvicorn
import database
import models
import schemas
import auth

models.Base.metadata.create_all(bind=database.engine)

#FastAPI app
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

app = FastAPI(title="StudySync API", version="0.1.0")

#static files and templates
static_dir = os.path.join(project_root, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

#security
security = HTTPBearer()

#dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

#routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#authentication endpoints
@app.post("/api/auth/register", response_model=schemas.UserResponse)
async def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    #check if user already exists
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    #create new user
    user = models.User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        is_active=True
    )
    user.set_password(user_data.password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@app.post("/api/auth/login", response_model=schemas.Token)
async def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=schemas.UserResponse)
async def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    return current_user

#study Groups endpoints
@app.get("/api/groups", response_model=list[schemas.StudyGroupResponse])
async def get_groups(db: Session = Depends(get_db)):
    groups = db.query(models.StudyGroup).all()
    return [
        {
            **group.__dict__,
            "member_count": len(group.members),
            "session_count": len(group.study_sessions)
        }
        for group in groups
    ]

@app.post("/api/groups", response_model=schemas.StudyGroupResponse)
async def create_group(
    group_data: schemas.StudyGroupCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    group = models.StudyGroup(
        **group_data.dict(),
        created_by=current_user.id
    )
    group.members.append(current_user)
    
    db.add(group)
    db.commit()
    db.refresh(group)
    
    return {
        **group.__dict__,
        "member_count": 1,
        "session_count": 0
    }

#study Sessions endpoints
@app.get("/api/sessions", response_model=list[schemas.StudySessionResponse])
async def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(models.StudySession).all()
    return [
        {
            **session.__dict__,
            "group_name": session.study_group.name if session.study_group else "No Group"
        }
        for session in sessions
    ]

@app.post("/api/sessions", response_model=schemas.StudySessionResponse)
async def create_session(
    session_data: schemas.StudySessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    #verify group exists and user is member
    group = db.query(models.StudyGroup).filter(models.StudyGroup.id == session_data.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if current_user not in group.members:
        raise HTTPException(status_code=403, detail="You are not a member of this group")
    
    session = models.StudySession(
        **session_data.dict(),
        created_by=current_user.id
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return {
        **session.__dict__,
        "group_name": group.name
    }

#utility endpoints
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "StudySync API is running"}

if __name__ == "__main__":
    print("🚀 Starting StudySync server...")
    print("📚 Visit: http://127.0.0.1:8000")
    print("🔐 API endpoints ready with authentication!")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)