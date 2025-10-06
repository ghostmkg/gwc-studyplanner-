"""
Data storage and persistence layer for StudySync
"""

import json
import sqlite3
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import uuid


class Storage:
    """Storage manager for StudySync data"""
    
    def __init__(self, database_url: str = "sqlite:///studysync.db"):
        self.database_url = database_url
        self.db_path = self._extract_db_path(database_url)
        self._init_database()
    
    def _extract_db_path(self, url: str) -> Path:
        """Extract database file path from URL"""
        if url.startswith("sqlite:///"):
            return Path(url[10:])  # Remove 'sqlite:///'
        return Path("studysync.db")  # Default
    
    def _init_database(self) -> None:
        """Initialize database tables"""
        
        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create groups table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS groups (
                    id TEXT PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    max_members INTEGER DEFAULT 10,
                    created_at TEXT NOT NULL,
                    data TEXT  -- JSON data for members and other info
                )
            ''')
            
            # Create sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    group_id TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    status TEXT DEFAULT 'scheduled',
                    created_at TEXT NOT NULL,
                    data TEXT,  -- JSON data for attendees and other info
                    FOREIGN KEY (group_id) REFERENCES groups (id)
                )
            ''')
            
            # Create users table (for future use)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT,
                    created_at TEXT NOT NULL,
                    data TEXT  -- JSON data for preferences and other info
                )
            ''')
            
            conn.commit()
    
    def create_group(self, group_data: Dict[str, Any]) -> str:
        """
        Create a new study group
        
        Args:
            group_data: Group information
        
        Returns:
            str: Generated group ID
        """
        group_id = str(uuid.uuid4())
        
        # Extract main fields
        name = group_data['name']
        description = group_data.get('description', '')
        max_members = group_data.get('max_members', 10)
        created_at = group_data.get('created_at', datetime.now().isoformat())
        
        # Store additional data as JSON
        additional_data = {
            'members': group_data.get('members', []),
            'sessions': group_data.get('sessions', []),
            'settings': group_data.get('settings', {})
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO groups (id, name, description, max_members, created_at, data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (group_id, name, description, max_members, created_at, json.dumps(additional_data)))
            conn.commit()
        
        return group_id
    
    def get_group_by_id(self, group_id: str) -> Optional[Dict[str, Any]]:
        """Get group by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM groups WHERE id = ?', (group_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_group_dict(row)
            return None
    
    def get_group_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get group by name"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM groups WHERE name = ?', (name,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_group_dict(row)
            return None
    
    def get_all_groups(self) -> List[Dict[str, Any]]:
        """Get all study groups"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM groups ORDER BY created_at DESC')
            rows = cursor.fetchall()
            
            return [self._row_to_group_dict(row) for row in rows]
    
    def update_group(self, group_id: str, group_data: Dict[str, Any]) -> bool:
        """Update group data"""
        # Extract main fields
        name = group_data.get('name')
        description = group_data.get('description', '')
        max_members = group_data.get('max_members', 10)
        
        # Store additional data as JSON
        additional_data = {
            'members': group_data.get('members', []),
            'sessions': group_data.get('sessions', []),
            'settings': group_data.get('settings', {})
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE groups 
                SET name = ?, description = ?, max_members = ?, data = ?
                WHERE id = ?
            ''', (name, description, max_members, json.dumps(additional_data), group_id))
            conn.commit()
            
            return cursor.rowcount > 0
    
    def delete_group(self, group_id: str) -> bool:
        """Delete a group and its sessions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Delete associated sessions first
            cursor.execute('DELETE FROM sessions WHERE group_id = ?', (group_id,))
            # Delete the group
            cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
            conn.commit()
            
            return cursor.rowcount > 0
    
    def create_session(self, session_data: Dict[str, Any]) -> str:
        """Create a new study session"""
        session_id = str(uuid.uuid4())
        
        # Extract main fields
        group_id = session_data['group_id']
        topic = session_data['topic']
        start_time = session_data['start_time']
        duration_minutes = session_data['duration_minutes']
        status = session_data.get('status', 'scheduled')
        created_at = session_data.get('created_at', datetime.now().isoformat())
        
        # Store additional data as JSON
        additional_data = {
            'attendees': session_data.get('attendees', []),
            'notes': session_data.get('notes', ''),
            'resources': session_data.get('resources', [])
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sessions (id, group_id, topic, start_time, duration_minutes, 
                                    status, created_at, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (session_id, group_id, topic, start_time, duration_minutes, 
                  status, created_at, json.dumps(additional_data)))
            conn.commit()
        
        return session_id
    
    def get_session_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sessions WHERE id = ?', (session_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_session_dict(row)
            return None
    
    def get_sessions_by_group(self, group_id: str) -> List[Dict[str, Any]]:
        """Get all sessions for a group"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sessions WHERE group_id = ? ORDER BY start_time', (group_id,))
            rows = cursor.fetchall()
            
            return [self._row_to_session_dict(row) for row in rows]
    
    def update_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Update session data"""
        # Extract main fields
        topic = session_data.get('topic')
        start_time = session_data.get('start_time')
        duration_minutes = session_data.get('duration_minutes')
        status = session_data.get('status')
        
        # Store additional data as JSON
        additional_data = {
            'attendees': session_data.get('attendees', []),
            'notes': session_data.get('notes', ''),
            'resources': session_data.get('resources', [])
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE sessions 
                SET topic = ?, start_time = ?, duration_minutes = ?, 
                    status = ?, data = ?
                WHERE id = ?
            ''', (topic, start_time, duration_minutes, status, 
                  json.dumps(additional_data), session_id))
            conn.commit()
            
            return cursor.rowcount > 0
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
            conn.commit()
            
            return cursor.rowcount > 0
    
    def _row_to_group_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert database row to group dictionary"""
        group_dict = {
            'id': row['id'],
            'name': row['name'],
            'description': row['description'],
            'max_members': row['max_members'],
            'created_at': row['created_at']
        }
        
        # Parse additional data
        if row['data']:
            additional_data = json.loads(row['data'])
            group_dict.update(additional_data)
        
        return group_dict
    
    def _row_to_session_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert database row to session dictionary"""
        session_dict = {
            'id': row['id'],
            'group_id': row['group_id'],
            'topic': row['topic'],
            'start_time': row['start_time'],
            'duration_minutes': row['duration_minutes'],
            'status': row['status'],
            'created_at': row['created_at']
        }
        
        # Parse additional data
        if row['data']:
            additional_data = json.loads(row['data'])
            session_dict.update(additional_data)
        
        return session_dict
    
    def backup_database(self, backup_path: Optional[Path] = None) -> Path:
        """Create a backup of the database"""
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.db_path.parent / f"studysync_backup_{timestamp}.db"
        
        # Simple file copy for SQLite
        import shutil
        shutil.copy2(self.db_path, backup_path)
        
        return backup_path
    
    def get_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Count groups
            cursor.execute('SELECT COUNT(*) FROM groups')
            group_count = cursor.fetchone()[0]
            
            # Count sessions
            cursor.execute('SELECT COUNT(*) FROM sessions')
            session_count = cursor.fetchone()[0]
            
            # Count total members across all groups
            cursor.execute('SELECT data FROM groups')
            total_members = 0
            for row in cursor.fetchall():
                if row[0]:
                    data = json.loads(row[0])
                    total_members += len(data.get('members', []))
            
            return {
                'total_groups': group_count,
                'total_sessions': session_count,
                'total_members': total_members
            }