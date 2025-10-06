"""
Test configuration and utilities for StudySync
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from src.utils.config import AppConfig, DatabaseConfig, NotificationConfig
from src.core.storage import Storage
from src.core.session_manager import SessionManager


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = Path(f.name)
    
    yield f"sqlite:///{db_path}"
    
    # Clean up
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def test_config(temp_db):
    """Create test configuration"""
    return AppConfig(
        debug=True,
        log_level="DEBUG",
        data_dir="test_data",
        database=DatabaseConfig(url=temp_db),
        notifications=NotificationConfig()
    )


@pytest.fixture
def storage(test_config):
    """Create storage instance for testing"""
    return Storage(test_config.database.url)


@pytest.fixture
def session_manager(storage, test_config):
    """Create session manager for testing"""
    return SessionManager(storage, test_config)


@pytest.fixture
def sample_group_data():
    """Sample group data for testing"""
    return {
        'name': 'Test Study Group',
        'description': 'A test group for unit testing',
        'max_members': 5,
        'created_at': datetime.now().isoformat(),
        'members': [],
        'sessions': []
    }


@pytest.fixture
def sample_session_data():
    """Sample session data for testing"""
    return {
        'group_id': 'test-group-id',
        'topic': 'Test Session',
        'start_time': (datetime.now().replace(microsecond=0) + 
                      datetime.timedelta(hours=2)).isoformat(),
        'duration_minutes': 60,
        'status': 'scheduled',
        'created_at': datetime.now().isoformat(),
        'attendees': []
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'joined_at': datetime.now().isoformat(),
        'role': 'member'
    }