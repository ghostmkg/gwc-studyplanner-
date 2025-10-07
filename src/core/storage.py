"""
Data storage and persistence layer for StudySync
"""

import json
import sqlite3
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import uuid
import os


class Storage:
    """Storage manager for StudySync data"""

    def __init__(self, config=None):
        self.config = config
        self.data_dir = Path.home() / ".studysync"
        self.data_dir.mkdir(exist_ok=True)
        
        # File paths
        self.groups_file = self.data_dir / "groups.json"
        self.sessions_file = self.data_dir / "sessions.json"
        self.users_file = self.data_dir / "users.json"
        
        self.initialize()

    def initialize(self):
        """Initialize storage files"""
        # Initialize groups file
        if not self.groups_file.exists():
            with open(self.groups_file, 'w') as f:
                json.dump({}, f)
        
        # Initialize sessions file
        if not self.sessions_file.exists():
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f)
        
        # Initialize users file
        if not self.users_file.exists():
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def _load_data(self, file_path: Path) -> Dict[str, Any]:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_data(self, file_path: Path, data: Dict[str, Any]):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    # Group operations
    def save_group(self, group_data: Dict[str, Any]) -> bool:
        """Save group data"""
        try:
            groups = self._load_data(self.groups_file)
            group_id = group_data.get('id')
            if group_id:
                groups[group_id] = group_data
                self._save_data(self.groups_file, groups)
                return True
            return False
        except Exception:
            return False

    def get_group(self, group_id: str) -> Optional[Dict[str, Any]]:
        """Get group by ID"""
        groups = self._load_data(self.groups_file)
        return groups.get(group_id)

    def get_group_by_name(self, group_name: str) -> Optional[Dict[str, Any]]:
        """Get group by name"""
        groups = self._load_data(self.groups_file)
        for group in groups.values():
            if group.get('name') == group_name:
                return group
        return None

    def get_all_groups(self) -> List[Dict[str, Any]]:
        """Get all groups"""
        groups = self._load_data(self.groups_file)
        return list(groups.values())

    def delete_group(self, group_id: str) -> bool:
        """Delete group"""
        try:
            groups = self._load_data(self.groups_file)
            if group_id in groups:
                del groups[group_id]
                self._save_data(self.groups_file, groups)
                return True
            return False
        except Exception:
            return False

    # Session operations
    def save_session(self, session_data: Dict[str, Any]) -> bool:
        """Save session data"""
        try:
            sessions = self._load_data(self.sessions_file)
            session_id = session_data.get('id')
            if session_id:
                sessions[session_id] = session_data
                self._save_data(self.sessions_file, sessions)
                return True
            return False
        except Exception:
            return False

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        sessions = self._load_data(self.sessions_file)
        return sessions.get(session_id)

    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get all sessions"""
        sessions = self._load_data(self.sessions_file)
        return list(sessions.values())

    def get_sessions_by_group(self, group_name: str) -> List[Dict[str, Any]]:
        """Get sessions by group name"""
        sessions = self._load_data(self.sessions_file)
        return [s for s in sessions.values() if s.get('group_name') == group_name]

    def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        try:
            sessions = self._load_data(self.sessions_file)
            if session_id in sessions:
                del sessions[session_id]
                self._save_data(self.sessions_file, sessions)
                return True
            return False
        except Exception:
            return False

    def add_session_to_group(self, group_name: str, session_id: str) -> bool:
        """Add session to group's session list"""
        try:
            group = self.get_group_by_name(group_name)
            if group:
                sessions = group.get('sessions', [])
                if session_id not in sessions:
                    sessions.append(session_id)
                    group['sessions'] = sessions
                    return self.save_group(group)
            return False
        except Exception:
            return False

    # User operations
    def save_user(self, user_data: Dict[str, Any]) -> bool:
        """Save user data"""
        try:
            users = self._load_data(self.users_file)
            user_id = user_data.get('id')
            if user_id:
                users[user_id] = user_data
                self._save_data(self.users_file, users)
                return True
            return False
        except Exception:
            return False

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        users = self._load_data(self.users_file)
        return users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        users = self._load_data(self.users_file)
        for user in users.values():
            if user.get('username') == username:
                return user
        return None

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        users = self._load_data(self.users_file)
        return list(users.values())

    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        try:
            users = self._load_data(self.users_file)
            if user_id in users:
                del users[user_id]
                self._save_data(self.users_file, users)
                return True
            return False
        except Exception:
            return False
