"""
Test cases for storage functionality
"""

import pytest
from datetime import datetime

from src.core.storage import Storage


class TestStorage:
    """Test cases for Storage class"""
    
    def test_database_initialization(self, storage):
        """Test that database is properly initialized"""
        assert storage is not None
        assert storage.db_path.exists()
    
    def test_create_group(self, storage, sample_group_data):
        """Test group creation"""
        group_id = storage.create_group(sample_group_data)
        
        assert group_id is not None
        assert len(group_id) > 0
        
        # Verify group was created
        retrieved_group = storage.get_group_by_id(group_id)
        assert retrieved_group is not None
        assert retrieved_group['name'] == sample_group_data['name']
        assert retrieved_group['description'] == sample_group_data['description']
    
    def test_get_group_by_name(self, storage, sample_group_data):
        """Test retrieving group by name"""
        group_id = storage.create_group(sample_group_data)
        
        retrieved_group = storage.get_group_by_name(sample_group_data['name'])
        assert retrieved_group is not None
        assert retrieved_group['id'] == group_id
        assert retrieved_group['name'] == sample_group_data['name']
    
    def test_get_all_groups(self, storage):
        """Test retrieving all groups"""
        # Create multiple groups
        group1_data = {
            'name': 'Group 1',
            'description': 'First test group',
            'max_members': 10,
            'created_at': datetime.now().isoformat(),
            'members': [],
            'sessions': []
        }
        
        group2_data = {
            'name': 'Group 2',
            'description': 'Second test group',
            'max_members': 15,
            'created_at': datetime.now().isoformat(),
            'members': [],
            'sessions': []
        }
        
        id1 = storage.create_group(group1_data)
        id2 = storage.create_group(group2_data)
        
        all_groups = storage.get_all_groups()
        assert len(all_groups) == 2
        
        group_ids = [g['id'] for g in all_groups]
        assert id1 in group_ids
        assert id2 in group_ids
    
    def test_update_group(self, storage, sample_group_data):
        """Test group update"""
        group_id = storage.create_group(sample_group_data)
        
        # Update group
        updated_data = sample_group_data.copy()
        updated_data['name'] = 'Updated Group Name'
        updated_data['description'] = 'Updated description'
        updated_data['max_members'] = 20
        
        success = storage.update_group(group_id, updated_data)
        assert success is True
        
        # Verify update
        retrieved_group = storage.get_group_by_id(group_id)
        assert retrieved_group['name'] == 'Updated Group Name'
        assert retrieved_group['description'] == 'Updated description'
        assert retrieved_group['max_members'] == 20
    
    def test_delete_group(self, storage, sample_group_data):
        """Test group deletion"""
        group_id = storage.create_group(sample_group_data)
        
        # Verify group exists
        assert storage.get_group_by_id(group_id) is not None
        
        # Delete group
        success = storage.delete_group(group_id)
        assert success is True
        
        # Verify group is deleted
        assert storage.get_group_by_id(group_id) is None
    
    def test_create_session(self, storage, sample_group_data):
        """Test session creation"""
        # Create a group first
        group_id = storage.create_group(sample_group_data)
        
        session_data = {
            'group_id': group_id,
            'topic': 'Test Session',
            'start_time': datetime.now().isoformat(),
            'duration_minutes': 60,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat(),
            'attendees': []
        }
        
        session_id = storage.create_session(session_data)
        assert session_id is not None
        assert len(session_id) > 0
        
        # Verify session was created
        retrieved_session = storage.get_session_by_id(session_id)
        assert retrieved_session is not None
        assert retrieved_session['group_id'] == group_id
        assert retrieved_session['topic'] == session_data['topic']
    
    def test_get_sessions_by_group(self, storage, sample_group_data):
        """Test retrieving sessions by group"""
        # Create a group
        group_id = storage.create_group(sample_group_data)
        
        # Create multiple sessions
        session1_data = {
            'group_id': group_id,
            'topic': 'Session 1',
            'start_time': datetime.now().isoformat(),
            'duration_minutes': 60,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat(),
            'attendees': []
        }
        
        session2_data = {
            'group_id': group_id,
            'topic': 'Session 2',
            'start_time': datetime.now().isoformat(),
            'duration_minutes': 90,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat(),
            'attendees': []
        }
        
        id1 = storage.create_session(session1_data)
        id2 = storage.create_session(session2_data)
        
        # Get sessions for the group
        sessions = storage.get_sessions_by_group(group_id)
        assert len(sessions) == 2
        
        session_ids = [s['id'] for s in sessions]
        assert id1 in session_ids
        assert id2 in session_ids
    
    def test_update_session(self, storage, sample_group_data):
        """Test session update"""
        # Create a group
        group_id = storage.create_group(sample_group_data)
        
        # Create a session
        session_data = {
            'group_id': group_id,
            'topic': 'Original Topic',
            'start_time': datetime.now().isoformat(),
            'duration_minutes': 60,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat(),
            'attendees': []
        }
        
        session_id = storage.create_session(session_data)
        
        # Update session
        updated_data = session_data.copy()
        updated_data['topic'] = 'Updated Topic'
        updated_data['duration_minutes'] = 120
        updated_data['status'] = 'active'
        
        success = storage.update_session(session_id, updated_data)
        assert success is True
        
        # Verify update
        retrieved_session = storage.get_session_by_id(session_id)
        assert retrieved_session['topic'] == 'Updated Topic'
        assert retrieved_session['duration_minutes'] == 120
        assert retrieved_session['status'] == 'active'
    
    def test_delete_session(self, storage, sample_group_data):
        """Test session deletion"""
        # Create a group
        group_id = storage.create_group(sample_group_data)
        
        # Create a session
        session_data = {
            'group_id': group_id,
            'topic': 'Test Session',
            'start_time': datetime.now().isoformat(),
            'duration_minutes': 60,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat(),
            'attendees': []
        }
        
        session_id = storage.create_session(session_data)
        
        # Verify session exists
        assert storage.get_session_by_id(session_id) is not None
        
        # Delete session
        success = storage.delete_session(session_id)
        assert success is True
        
        # Verify session is deleted
        assert storage.get_session_by_id(session_id) is None
    
    def test_get_stats(self, storage, sample_group_data):
        """Test database statistics"""
        # Initially should be empty
        stats = storage.get_stats()
        initial_groups = stats['total_groups']
        initial_sessions = stats['total_sessions']
        
        # Create a group with members
        group_data = sample_group_data.copy()
        group_data['members'] = [
            {'username': 'user1', 'joined_at': datetime.now().isoformat()},
            {'username': 'user2', 'joined_at': datetime.now().isoformat()}
        ]
        
        group_id = storage.create_group(group_data)
        
        # Create a session
        session_data = {
            'group_id': group_id,
            'topic': 'Test Session',
            'start_time': datetime.now().isoformat(),
            'duration_minutes': 60,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat(),
            'attendees': []
        }
        
        storage.create_session(session_data)
        
        # Check updated stats
        updated_stats = storage.get_stats()
        assert updated_stats['total_groups'] == initial_groups + 1
        assert updated_stats['total_sessions'] == initial_sessions + 1
        assert updated_stats['total_members'] >= 2