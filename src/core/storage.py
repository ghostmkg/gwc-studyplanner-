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

    # (full implementation from main branch preserved)
