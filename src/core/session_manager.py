"""
Session management for StudySync
Handles study session creation, scheduling, and lifecycle management
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import uuid

from .storage import Storage
from ..utils.config import AppConfig
from ..utils.helpers import generate_session_id, parse_duration, calculate_time_until


class SessionManager:
    """Manages study sessions and their lifecycle"""
    
    def __init__(self, storage: Storage, config: AppConfig):
        self.storage = storage
        self.config = config
    
    def create_session(self, session_data: Dict[str, Any]) -> str:
        """
        Create a new study session
        
        Args:
            session_data: Session information
        
        Returns:
            str: Session ID
        """
        # Validate session data
        required_fields = ['group_id', 'topic', 'start_time', 'duration_minutes']
        for field in required_fields:
            if field not in session_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate group exists
        group = self.storage.get_group_by_id(session_data['group_id'])
        if not group:
            raise ValueError("Group not found")
        
        # Validate start time
        start_time = datetime.fromisoformat(session_data['start_time'])
        if start_time < datetime.now():
            raise ValueError("Cannot schedule sessions in the past")
        
        # Create session
        session_id = self.storage.create_session(session_data)
        
        # Schedule notifications (if configured)
        self._schedule_notifications(session_id, session_data)
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        return self.storage.get_session_by_id(session_id)
    
    def get_group_sessions(self, group_id: str, 
                          status_filter: Optional[str] = None,
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get sessions for a group with optional filtering
        
        Args:
            group_id: Group ID
            status_filter: Filter by status (scheduled, active, completed, cancelled)
            start_date: Filter sessions after this date
            end_date: Filter sessions before this date
        
        Returns:
            List of sessions
        """
        sessions = self.storage.get_sessions_by_group(group_id)
        
        # Apply filters
        if status_filter:
            sessions = [s for s in sessions if s.get('status') == status_filter]
        
        if start_date:
            sessions = [s for s in sessions 
                       if datetime.fromisoformat(s['start_time']) >= start_date]
        
        if end_date:
            sessions = [s for s in sessions 
                       if datetime.fromisoformat(s['start_time']) <= end_date]
        
        return sessions
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session information"""
        session = self.storage.get_session_by_id(session_id)
        if not session:
            return False
        
        # Merge updates
        session.update(updates)
        
        # Validate if start_time is being updated
        if 'start_time' in updates:
            start_time = datetime.fromisoformat(updates['start_time'])
            if start_time < datetime.now() and session.get('status') != 'completed':
                raise ValueError("Cannot reschedule to past time")
        
        return self.storage.update_session(session_id, session)
    
    def cancel_session(self, session_id: str, reason: Optional[str] = None) -> bool:
        """Cancel a session"""
        session = self.storage.get_session_by_id(session_id)
        if not session:
            return False
        
        if session.get('status') in ['completed', 'cancelled']:
            raise ValueError(f"Cannot cancel session with status: {session['status']}")
        
        updates = {
            'status': 'cancelled',
            'cancelled_at': datetime.now().isoformat(),
            'cancellation_reason': reason or 'No reason provided'
        }
        
        return self.storage.update_session(session_id, updates)
    
    def start_session(self, session_id: str) -> bool:
        """Mark session as started"""
        session = self.storage.get_session_by_id(session_id)
        if not session:
            return False
        
        if session.get('status') != 'scheduled':
            raise ValueError(f"Cannot start session with status: {session['status']}")
        
        updates = {
            'status': 'active',
            'actual_start_time': datetime.now().isoformat()
        }
        
        return self.storage.update_session(session_id, updates)
    
    def end_session(self, session_id: str, notes: Optional[str] = None) -> bool:
        """Mark session as completed"""
        session = self.storage.get_session_by_id(session_id)
        if not session:
            return False
        
        if session.get('status') != 'active':
            raise ValueError(f"Cannot end session with status: {session['status']}")
        
        updates = {
            'status': 'completed',
            'actual_end_time': datetime.now().isoformat(),
            'completion_notes': notes or ''
        }
        
        return self.storage.update_session(session_id, updates)
    
    def add_attendee(self, session_id: str, username: str, 
                    user_info: Optional[Dict[str, Any]] = None) -> bool:
        """Add attendee to session"""
        session = self.storage.get_session_by_id(session_id)
        if not session:
            return False
        
        attendees = session.get('attendees', [])
        
        # Check if already attending
        if any(a.get('username') == username for a in attendees):
            return False  # Already attending
        
        attendee_data = {
            'username': username,
            'joined_at': datetime.now().isoformat(),
            'status': 'confirmed'
        }
        
        if user_info:
            attendee_data.update(user_info)
        
        attendees.append(attendee_data)
        
        return self.storage.update_session(session_id, {'attendees': attendees})
    
    def remove_attendee(self, session_id: str, username: str) -> bool:
        """Remove attendee from session"""
        session = self.storage.get_session_by_id(session_id)
        if not session:
            return False
        
        attendees = session.get('attendees', [])
        original_count = len(attendees)
        
        # Remove the attendee
        attendees = [a for a in attendees if a.get('username') != username]
        
        if len(attendees) == original_count:
            return False  # User was not attending
        
        return self.storage.update_session(session_id, {'attendees': attendees})
    
    def get_upcoming_sessions(self, hours_ahead: int = 24) -> List[Dict[str, Any]]:
        """
        Get upcoming sessions within specified timeframe
        
        Args:
            hours_ahead: Look ahead this many hours
        
        Returns:
            List of upcoming sessions
        """
        cutoff_time = datetime.now() + timedelta(hours=hours_ahead)
        
        # Get all groups and their sessions
        all_sessions = []
        groups = self.storage.get_all_groups()
        
        for group in groups:
            sessions = self.storage.get_sessions_by_group(group['id'])
            for session in sessions:
                start_time = datetime.fromisoformat(session['start_time'])
                if (session.get('status') == 'scheduled' and 
                    datetime.now() <= start_time <= cutoff_time):
                    session['group_name'] = group['name']
                    all_sessions.append(session)
        
        # Sort by start time
        all_sessions.sort(key=lambda x: x['start_time'])
        
        return all_sessions
    
    def get_session_analytics(self, group_id: Optional[str] = None, 
                            days_back: int = 30) -> Dict[str, Any]:
        """
        Get session analytics for a group or all groups
        
        Args:
            group_id: Specific group ID (optional)
            days_back: Number of days to look back
        
        Returns:
            Analytics data
        """
        start_date = datetime.now() - timedelta(days=days_back)
        
        if group_id:
            groups = [self.storage.get_group_by_id(group_id)]
            if not groups[0]:
                return {}
        else:
            groups = self.storage.get_all_groups()
        
        analytics = {
            'total_sessions': 0,
            'completed_sessions': 0,
            'cancelled_sessions': 0,
            'total_participants': 0,
            'average_duration': 0,
            'most_active_group': '',
            'daily_breakdown': {},
            'status_breakdown': {
                'scheduled': 0,
                'active': 0,
                'completed': 0,
                'cancelled': 0
            }
        }
        
        all_durations = []
        group_activity = {}
        
        for group in groups:
            sessions = self.get_group_sessions(
                group['id'], 
                start_date=start_date
            )
            
            group_activity[group['name']] = len(sessions)
            
            for session in sessions:
                analytics['total_sessions'] += 1
                analytics['status_breakdown'][session.get('status', 'scheduled')] += 1
                
                if session.get('status') == 'completed':
                    analytics['completed_sessions'] += 1
                elif session.get('status') == 'cancelled':
                    analytics['cancelled_sessions'] += 1
                
                # Count participants
                attendees = session.get('attendees', [])
                analytics['total_participants'] += len(attendees)
                
                # Track duration
                if session.get('status') == 'completed':
                    all_durations.append(session.get('duration_minutes', 0))
                
                # Daily breakdown
                session_date = datetime.fromisoformat(session['start_time']).date()
                date_key = session_date.strftime('%Y-%m-%d')
                analytics['daily_breakdown'][date_key] = analytics['daily_breakdown'].get(date_key, 0) + 1
        
        # Calculate averages
        if all_durations:
            analytics['average_duration'] = sum(all_durations) / len(all_durations)
        
        # Find most active group
        if group_activity:
            analytics['most_active_group'] = max(group_activity, key=group_activity.get)
        
        return analytics
    
    def _schedule_notifications(self, session_id: str, session_data: Dict[str, Any]) -> None:
        """Schedule notifications for a session (placeholder for future implementation)"""
        # This would integrate with the notification engine
        # For now, it's a placeholder
        pass
    
    def get_session_conflicts(self, group_id: str, start_time: datetime, 
                            duration_minutes: int, exclude_session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Check for session conflicts within a group
        
        Args:
            group_id: Group to check
            start_time: Proposed session start time
            duration_minutes: Proposed session duration
            exclude_session_id: Session ID to exclude from conflict check
        
        Returns:
            List of conflicting sessions
        """
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        sessions = self.storage.get_sessions_by_group(group_id)
        conflicts = []
        
        for session in sessions:
            if exclude_session_id and session['id'] == exclude_session_id:
                continue
            
            if session.get('status') in ['cancelled']:
                continue
            
            session_start = datetime.fromisoformat(session['start_time'])
            session_end = session_start + timedelta(minutes=session['duration_minutes'])
            
            # Check for overlap
            if (start_time < session_end and end_time > session_start):
                conflicts.append(session)
        
        return conflicts