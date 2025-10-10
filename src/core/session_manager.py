"""
Session management for StudySync
Handles study session creation, scheduling, and lifecycle management
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid

from .storage import Storage
from ..utils.config import AppConfig


class SessionManager:
    """Manages study sessions and their lifecycle"""

    def __init__(self, storage: Storage, config: AppConfig):
        self.storage = storage
        self.config = config

    def create_session(self, session_data: Dict[str, Any]) -> str:
        """Create a new study session"""
        session_id = str(uuid.uuid4())
        session_data['id'] = session_id
        session_data['created_at'] = datetime.now().isoformat()
        
        # Store session
        self.storage.save_session(session_data)
        
        # Add to group if specified
        if 'group_name' in session_data:
            self.storage.add_session_to_group(session_data['group_name'], session_id)
        
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        return self.storage.get_session(session_id)

    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session data"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.update(updates)
        session['updated_at'] = datetime.now().isoformat()
        
        return self.storage.save_session(session)

    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        return self.storage.delete_session(session_id)

    def get_sessions_by_group(self, group_name: str) -> List[Dict[str, Any]]:
        """Get all sessions for a group"""
        return self.storage.get_sessions_by_group(group_name)

    def get_upcoming_sessions(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Get upcoming sessions within specified days"""
        all_sessions = self.storage.get_all_sessions()
        now = datetime.now()
        cutoff = now + timedelta(days=days_ahead)
        
        upcoming = []
        for session in all_sessions:
            session_time = datetime.fromisoformat(session.get('start_time', ''))
            if now <= session_time <= cutoff:
                upcoming.append(session)
        
        return sorted(upcoming, key=lambda x: x.get('start_time', ''))

    def mark_attendance(self, session_id: str, username: str, attended: bool = True) -> bool:
        """Mark attendance for a session"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        attendees = session.get('attendees', [])
        if attended and username not in attendees:
            attendees.append(username)
        elif not attended and username in attendees:
            attendees.remove(username)
        
        session['attendees'] = attendees
        return self.update_session(session_id, {'attendees': attendees})

    def get_analytics(self, group_name: str = None, period: str = "last-week") -> Dict[str, Any]:
        """Get analytics for sessions"""
        sessions = self.storage.get_all_sessions()
        
        # Filter by group if specified
        if group_name:
            sessions = [s for s in sessions if s.get('group_name') == group_name]
        
        # Filter by period
        now = datetime.now()
        if period == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            sessions = [s for s in sessions if datetime.fromisoformat(s.get('start_time', '')) >= start_date]
        elif period == "last-week":
            start_date = now - timedelta(days=7)
            sessions = [s for s in sessions if datetime.fromisoformat(s.get('start_time', '')) >= start_date]
        elif period == "last-month":
            start_date = now - timedelta(days=30)
            sessions = [s for s in sessions if datetime.fromisoformat(s.get('start_time', '')) >= start_date]
        
        # Calculate analytics
        total_sessions = len(sessions)
        total_hours = sum(s.get('duration_minutes', 0) for s in sessions) / 60
        avg_attendance = sum(len(s.get('attendees', [])) for s in sessions) / max(total_sessions, 1)
        
        # Most active day
        day_counts = {}
        for session in sessions:
            day = datetime.fromisoformat(session.get('start_time', '')).strftime('%A')
            day_counts[day] = day_counts.get(day, 0) + 1
        
        most_active_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else 'N/A'
        
        # Recent sessions
        recent_sessions = sorted(sessions, key=lambda x: x.get('start_time', ''), reverse=True)[:5]
        recent_sessions = [
            {
                'topic': s.get('topic', 'N/A'),
                'date': datetime.fromisoformat(s.get('start_time', '')).strftime('%Y-%m-%d')
            }
            for s in recent_sessions
        ]
        
        return {
            'total_sessions': total_sessions,
            'total_hours': total_hours,
            'avg_attendance': avg_attendance,
            'most_active_day': most_active_day,
            'recent_sessions': recent_sessions
        }
