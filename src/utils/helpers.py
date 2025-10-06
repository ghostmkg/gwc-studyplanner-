"""
Utility helper functions for StudySync
"""

import re
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path


def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_group_name(name: str) -> bool:
    """
    Validate study group name
    
    Args:
        name: Group name to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not name or len(name) < 2:
        return False
    if len(name) > 50:
        return False
    # Allow alphanumeric, spaces, hyphens, and underscores
    pattern = r'^[a-zA-Z0-9\s\-_]+$'
    return re.match(pattern, name) is not None


def parse_duration(duration_str: str) -> Optional[int]:
    """
    Parse duration string to minutes
    
    Args:
        duration_str: Duration string (e.g., "1h", "90m", "2h30m")
    
    Returns:
        int: Duration in minutes, or None if invalid
    """
    if not duration_str:
        return None
    
    duration_str = duration_str.lower().strip()
    
    # Simple patterns: 1h, 90m, 2.5h
    if duration_str.endswith('h'):
        try:
            hours = float(duration_str[:-1])
            return int(hours * 60)
        except ValueError:
            return None
    
    if duration_str.endswith('m'):
        try:
            return int(duration_str[:-1])
        except ValueError:
            return None
    
    # Complex pattern: 1h30m
    pattern = r'(?:(\d+)h)?(?:(\d+)m)?'
    match = re.match(pattern, duration_str)
    if match:
        hours_str, minutes_str = match.groups()
        hours = int(hours_str) if hours_str else 0
        minutes = int(minutes_str) if minutes_str else 0
        return hours * 60 + minutes
    
    return None


def format_duration(minutes: int) -> str:
    """
    Format minutes to human-readable duration
    
    Args:
        minutes: Duration in minutes
    
    Returns:
        str: Formatted duration string
    """
    if minutes < 60:
        return f"{minutes}m"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if remaining_minutes == 0:
        return f"{hours}h"
    else:
        return f"{hours}h{remaining_minutes}m"


def parse_date_time(date_str: str, time_str: str) -> Optional[datetime]:
    """
    Parse date and time strings to datetime object
    
    Args:
        date_str: Date string (YYYY-MM-DD)
        time_str: Time string (HH:MM)
    
    Returns:
        datetime: Parsed datetime, or None if invalid
    """
    try:
        date_part = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_part = datetime.strptime(time_str, '%H:%M').time()
        return datetime.combine(date_part, time_part)
    except ValueError:
        return None


def generate_session_id(group_name: str, start_time: datetime) -> str:
    """
    Generate unique session ID
    
    Args:
        group_name: Name of the study group
        start_time: Session start time
    
    Returns:
        str: Unique session ID
    """
    data = f"{group_name}_{start_time.isoformat()}"
    return hashlib.md5(data.encode()).hexdigest()[:8]


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system operations
    
    Args:
        filename: Original filename
    
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    return filename


def get_file_size_human(file_path: Path) -> str:
    """
    Get human-readable file size
    
    Args:
        file_path: Path to file
    
    Returns:
        str: Human-readable file size
    """
    try:
        size = file_path.stat().st_size
    except OSError:
        return "Unknown"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def create_backup_filename(original_name: str) -> str:
    """
    Create backup filename with timestamp
    
    Args:
        original_name: Original filename
    
    Returns:
        str: Backup filename
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = original_name.rsplit('.', 1) if '.' in original_name else (original_name, '')
    backup_name = f"{name}_backup_{timestamp}"
    return f"{backup_name}.{ext}" if ext else backup_name


def calculate_time_until(target_time: datetime) -> Tuple[bool, str]:
    """
    Calculate time until target datetime
    
    Args:
        target_time: Target datetime
    
    Returns:
        Tuple[bool, str]: (is_future, time_description)
    """
    now = datetime.now()
    diff = target_time - now
    
    if diff.total_seconds() <= 0:
        # Past time
        diff = now - target_time
        if diff.days > 0:
            return False, f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return False, f"{hours} hours ago"
        else:
            minutes = diff.seconds // 60
            return False, f"{minutes} minutes ago"
    else:
        # Future time
        if diff.days > 0:
            return True, f"in {diff.days} days"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return True, f"in {hours} hours"
        else:
            minutes = diff.seconds // 60
            return True, f"in {minutes} minutes"


def get_week_bounds(date: datetime) -> Tuple[datetime, datetime]:
    """
    Get start and end of week for given date
    
    Args:
        date: Reference date
    
    Returns:
        Tuple[datetime, datetime]: (week_start, week_end)
    """
    # Monday as start of week
    days_since_monday = date.weekday()
    week_start = date - timedelta(days=days_since_monday)
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    return week_start, week_end


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks of specified size
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
    
    Returns:
        List[List[Any]]: List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_dict(d: Dict[str, Any], parent_key: str = '', separator: str = '.') -> Dict[str, Any]:
    """
    Flatten nested dictionary
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        separator: Key separator
    
    Returns:
        Dict[str, Any]: Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, separator).items())
        else:
            items.append((new_key, v))
    return dict(items)