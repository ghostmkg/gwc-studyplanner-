"""
Group management for StudySync
Handles study group creation, member management, and group operations
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

from .storage import Storage
from ..utils.config import AppConfig


class GroupManager:
    """Manages study groups and their members"""

    def __init__(self, storage: Storage, config: AppConfig):
        self.storage = storage
        self.config = config

    def create_group(self, group_data: Dict[str, Any]) -> str:
        """Create a new study group"""
        group_id = str(uuid.uuid4())
        group_data['id'] = group_id
        group_data['created_at'] = datetime.now().isoformat()
        group_data['members'] = group_data.get('members', [])
        group_data['sessions'] = group_data.get('sessions', [])
        
        # Store group
        self.storage.save_group(group_data)
        
        return group_id

    def get_group(self, group_id: str) -> Optional[Dict[str, Any]]:
        """Get group by ID"""
        return self.storage.get_group(group_id)

    def get_group_by_name(self, group_name: str) -> Optional[Dict[str, Any]]:
        """Get group by name"""
        return self.storage.get_group_by_name(group_name)

    def update_group(self, group_id: str, updates: Dict[str, Any]) -> bool:
        """Update group data"""
        group = self.get_group(group_id)
        if not group:
            return False
        
        group.update(updates)
        group['updated_at'] = datetime.now().isoformat()
        
        return self.storage.save_group(group)

    def delete_group(self, group_id: str) -> bool:
        """Delete a group"""
        return self.storage.delete_group(group_id)

    def get_all_groups(self) -> List[Dict[str, Any]]:
        """Get all groups"""
        return self.storage.get_all_groups()

    def add_member(self, group_name: str, username: str) -> bool:
        """Add a member to a group"""
        group = self.get_group_by_name(group_name)
        if not group:
            return False
        
        # Check if group is full
        current_members = len(group.get('members', []))
        max_members = group.get('max_members', 10)
        
        if current_members >= max_members:
            return False
        
        # Add member if not already in group
        members = group.get('members', [])
        if username not in members:
            members.append(username)
            group['members'] = members
            group['updated_at'] = datetime.now().isoformat()
            return self.storage.save_group(group)
        
        return True  # Already a member

    def remove_member(self, group_name: str, username: str) -> bool:
        """Remove a member from a group"""
        group = self.get_group_by_name(group_name)
        if not group:
            return False
        
        members = group.get('members', [])
        if username in members:
            members.remove(username)
            group['members'] = members
            group['updated_at'] = datetime.now().isoformat()
            return self.storage.save_group(group)
        
        return False  # Member not found

    def get_group_members(self, group_name: str) -> List[str]:
        """Get all members of a group"""
        group = self.get_group_by_name(group_name)
        if not group:
            return []
        
        return group.get('members', [])

    def is_member(self, group_name: str, username: str) -> bool:
        """Check if user is a member of the group"""
        members = self.get_group_members(group_name)
        return username in members

    def get_group_stats(self, group_name: str) -> Dict[str, Any]:
        """Get statistics for a group"""
        group = self.get_group_by_name(group_name)
        if not group:
            return {}
        
        sessions = self.storage.get_sessions_by_group(group_name)
        
        return {
            'name': group.get('name', ''),
            'description': group.get('description', ''),
            'member_count': len(group.get('members', [])),
            'max_members': group.get('max_members', 10),
            'session_count': len(sessions),
            'created_at': group.get('created_at', ''),
            'members': group.get('members', [])
        }