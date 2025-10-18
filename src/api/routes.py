"""
API routes for StudySync
FastAPI-based REST API endpoints
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import time
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .models import (
    GroupCreateModel, GroupUpdateModel, GroupModel,
    SessionCreateModel, SessionUpdateModel, SessionModel,
    JoinGroupModel, SessionAttendanceModel,
    NotificationTestModel, AnalyticsQuery, AnalyticsResponse,
    ErrorResponse, SuccessResponse, HealthResponse, ConfigResponse
)
from ..core.storage import Storage
from ..core.session_manager import SessionManager
from ..core.notification_engine import NotificationEngine
from ..utils.config import AppConfig, load_config, get_app_info


# Global variables for dependency injection
app_config: Optional[AppConfig] = None
storage: Optional[Storage] = None
session_manager: Optional[SessionManager] = None
notification_engine: Optional[NotificationEngine] = None
app_start_time: float = time.time()


def get_storage() -> Storage:
    """Dependency to get storage instance"""
    global storage
    if storage is None:
        raise HTTPException(status_code=500, detail="Storage not initialized")
    return storage


def get_session_manager() -> SessionManager:
    """Dependency to get session manager instance"""
    global session_manager
    if session_manager is None:
        raise HTTPException(status_code=500, detail="Session manager not initialized")
    return session_manager


def get_notification_engine() -> NotificationEngine:
    """Dependency to get notification engine instance"""
    global notification_engine
    if notification_engine is None:
        raise HTTPException(status_code=500, detail="Notification engine not initialized")
    return notification_engine


def create_app(config: Optional[AppConfig] = None) -> FastAPI:
    """Create and configure FastAPI application"""
    global app_config, storage, session_manager, notification_engine, app_start_time
    
    # Load configuration
    if config is None:
        config = load_config()
    app_config = config
    
    # Initialize components
    storage = Storage(config.database.url)
    session_manager = SessionManager(storage, config)
    notification_engine = NotificationEngine(config)
    app_start_time = time.time()
    
    # Create FastAPI app
    app_info = get_app_info()
    app = FastAPI(
        title=app_info['name'],
        description=app_info['description'],
        version=app_info['version'],
        docs_url="/docs" if config.debug else None,
        redoc_url="/redoc" if config.debug else None
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Error handlers
    @app.exception_handler(ValueError)
    async def value_error_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(error="ValidationError", message=str(exc)).dict()
        )
    
    @app.exception_handler(404)
    async def not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content=ErrorResponse(error="NotFound", message="Resource not found").dict()
        )
    
    # Health check endpoint
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint"""
        try:
            # Test database connection
            stats = storage.get_stats()
            db_status = "connected"
        except Exception:
            db_status = "disconnected"
        
        uptime = time.time() - app_start_time
        
        return HealthResponse(
            version=app_info['version'],
            database_status=db_status,
            uptime_seconds=uptime
        )
    
    # Configuration endpoint
    @app.get("/config", response_model=ConfigResponse)
    async def get_config():
        """Get application configuration"""
        notification_channels = []
        if config.notifications.email_enabled:
            notification_channels.append("email")
        if config.notifications.slack_webhook:
            notification_channels.append("slack")
        if config.notifications.discord_webhook:
            notification_channels.append("discord")
        
        return ConfigResponse(
            debug_mode=config.debug,
            database_type="sqlite" if "sqlite" in config.database.url else "postgresql",
            notification_channels=notification_channels,
            max_group_size=config.max_group_size,
            version=app_info['version']
        )
    
    # Group endpoints
    @app.post("/groups", response_model=SuccessResponse)
    async def create_group(
        group_data: GroupCreateModel,
        storage: Storage = Depends(get_storage)
    ):
        """Create a new study group"""
        try:
            # Check if group name already exists
            existing = storage.get_group_by_name(group_data.name)
            if existing:
                raise HTTPException(status_code=409, detail="Group name already exists")
            
            # Create group
            group_dict = {
                'name': group_data.name,
                'description': group_data.description or "",
                'max_members': group_data.max_members,
                'created_at': datetime.now().isoformat(),
                'members': [],
                'sessions': []
            }
            
            group_id = storage.create_group(group_dict)
            
            return SuccessResponse(
                message="Group created successfully",
                data={"group_id": group_id}
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create group: {str(e)}")
    
    @app.get("/groups", response_model=List[GroupModel])
    async def list_groups(storage: Storage = Depends(get_storage)):
        """List all study groups"""
        try:
            groups = storage.get_all_groups()
            return [GroupModel(**group) for group in groups]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch groups: {str(e)}")
    
    @app.get("/groups/{group_id}", response_model=GroupModel)
    async def get_group(group_id: str, storage: Storage = Depends(get_storage)):
        """Get specific group by ID"""
        try:
            group = storage.get_group_by_id(group_id)
            if not group:
                raise HTTPException(status_code=404, detail="Group not found")
            return GroupModel(**group)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch group: {str(e)}")
    
    @app.put("/groups/{group_id}", response_model=SuccessResponse)
    async def update_group(
        group_id: str,
        updates: GroupUpdateModel,
        storage: Storage = Depends(get_storage)
    ):
        """Update group information"""
        try:
            # Get existing group
            group = storage.get_group_by_id(group_id)
            if not group:
                raise HTTPException(status_code=404, detail="Group not found")
            
            # Apply updates
            update_dict = updates.dict(exclude_unset=True)
            group.update(update_dict)
            
            # Check for name conflicts if name is being updated
            if 'name' in update_dict:
                existing = storage.get_group_by_name(update_dict['name'])
                if existing and existing['id'] != group_id:
                    raise HTTPException(status_code=409, detail="Group name already exists")
            
            success = storage.update_group(group_id, group)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to update group")
            
            return SuccessResponse(message="Group updated successfully")
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update group: {str(e)}")
    
    @app.delete("/groups/{group_id}", response_model=SuccessResponse)
    async def delete_group(group_id: str, storage: Storage = Depends(get_storage)):
        """Delete a group"""
        try:
            success = storage.delete_group(group_id)
            if not success:
                raise HTTPException(status_code=404, detail="Group not found")
            
            return SuccessResponse(message="Group deleted successfully")
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete group: {str(e)}")
    
    @app.post("/groups/{group_id}/join", response_model=SuccessResponse)
    async def join_group(
        group_id: str,
        join_data: JoinGroupModel,
        storage: Storage = Depends(get_storage)
    ):
        """Join a study group"""
        try:
            # Get group
            group = storage.get_group_by_id(group_id)
            if not group:
                raise HTTPException(status_code=404, detail="Group not found")
            
            # Check if already a member
            members = group.get('members', [])
            if any(m.get('username') == join_data.username for m in members):
                raise HTTPException(status_code=409, detail="Already a member of this group")
            
            # Check capacity
            if len(members) >= group.get('max_members', 10):
                raise HTTPException(status_code=409, detail="Group is full")
            
            # Add member
            member_data = {
                'username': join_data.username,
                'joined_at': datetime.now().isoformat(),
                'role': 'member'
            }
            if join_data.user_info:
                member_data.update(join_data.user_info)
            
            members.append(member_data)
            group['members'] = members
            
            success = storage.update_group(group_id, group)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to join group")
            
            return SuccessResponse(message="Successfully joined group")
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to join group: {str(e)}")
    
    # Session endpoints
    @app.post("/sessions", response_model=SuccessResponse)
    async def create_session(
        session_data: SessionCreateModel,
        session_manager: SessionManager = Depends(get_session_manager)
    ):
        """Create a new study session"""
        try:
            session_dict = {
                'group_id': session_data.group_id,
                'topic': session_data.topic,
                'start_time': session_data.start_time.isoformat(),
                'duration_minutes': session_data.duration_minutes,
                'description': session_data.description or "",
                'status': 'scheduled',
                'created_at': datetime.now().isoformat(),
                'attendees': []
            }
            
            session_id = session_manager.create_session(session_dict)
            
            return SuccessResponse(
                message="Session created successfully",
                data={"session_id": session_id}
            )
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")
    
    @app.get("/sessions/{session_id}", response_model=SessionModel)
    async def get_session(
        session_id: str,
        session_manager: SessionManager = Depends(get_session_manager)
    ):
        """Get specific session by ID"""
        try:
            session = session_manager.get_session(session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            
            # Convert start_time back to datetime
            session['start_time'] = datetime.fromisoformat(session['start_time'])
            session['created_at'] = datetime.fromisoformat(session['created_at'])
            
            return SessionModel(**session)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch session: {str(e)}")
    
    @app.get("/groups/{group_id}/sessions", response_model=List[SessionModel])
    async def get_group_sessions(
        group_id: str,
        status: Optional[str] = Query(None),
        session_manager: SessionManager = Depends(get_session_manager)
    ):
        """Get sessions for a specific group"""
        try:
            sessions = session_manager.get_group_sessions(group_id, status_filter=status)
            
            # Convert timestamps
            for session in sessions:
                session['start_time'] = datetime.fromisoformat(session['start_time'])
                session['created_at'] = datetime.fromisoformat(session['created_at'])
            
            return [SessionModel(**session) for session in sessions]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch sessions: {str(e)}")
    
    @app.put("/sessions/{session_id}", response_model=SuccessResponse)
    async def update_session(
        session_id: str,
        updates: SessionUpdateModel,
        session_manager: SessionManager = Depends(get_session_manager)
    ):
        """Update session information"""
        try:
            update_dict = updates.dict(exclude_unset=True)
            
            # Convert datetime to ISO string if present
            if 'start_time' in update_dict:
                update_dict['start_time'] = update_dict['start_time'].isoformat()
            
            success = session_manager.update_session(session_id, update_dict)
            if not success:
                raise HTTPException(status_code=404, detail="Session not found")
            
            return SuccessResponse(message="Session updated successfully")
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update session: {str(e)}")
    
    @app.post("/sessions/{session_id}/attend", response_model=SuccessResponse)
    async def attend_session(
        session_id: str,
        attendance: SessionAttendanceModel,
        session_manager: SessionManager = Depends(get_session_manager)
    ):
        """Register attendance for a session"""
        try:
            success = session_manager.add_attendee(
                session_id, 
                attendance.username, 
                {'status': attendance.status}
            )
            
            if not success:
                raise HTTPException(status_code=400, detail="Already attending or session not found")
            
            return SuccessResponse(message="Attendance registered successfully")
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to register attendance: {str(e)}")
    
    # Analytics endpoint
    @app.get("/analytics", response_model=AnalyticsResponse)
    async def get_analytics(
        group_id: Optional[str] = Query(None),
        period: str = Query("last-week"),
        session_manager: SessionManager = Depends(get_session_manager)
    ):
        """Get analytics data"""
        try:
            # Calculate date range based on period
            days_map = {
                "today": 1,
                "last-week": 7,
                "last-month": 30,
                "all": 365  # Arbitrary large number
            }
            
            days_back = days_map.get(period, 7)
            analytics = session_manager.get_session_analytics(group_id, days_back)
            
            return AnalyticsResponse(**analytics)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")
    
    # Notification testing endpoint
    @app.post("/notifications/test", response_model=SuccessResponse)
    async def test_notifications(
        test_data: NotificationTestModel,
        notification_engine: NotificationEngine = Depends(get_notification_engine)
    ):
        """Test notification channels"""
        try:
            results = notification_engine.test_notification_channels()
            
            return SuccessResponse(
                message="Notification test completed",
                data={"results": results}
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to test notifications: {str(e)}")
    
    return app


# Create the app instance (for uvicorn)
app = create_app()