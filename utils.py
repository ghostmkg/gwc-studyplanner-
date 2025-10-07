from datetime import datetime, timedelta
import re

# ---------------------------
# Time & Date Utilities
# ---------------------------
def format_datetime(dt: datetime) -> str:
    """Format datetime object into readable string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def add_minutes_to_datetime(dt: datetime, minutes: int) -> datetime:
    """Return datetime after adding given minutes."""
    return dt + timedelta(minutes=minutes)

# ---------------------------
# Email Utilities
# ---------------------------
def is_valid_email(email: str) -> bool:
    """Check if the email is in valid format."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

# ---------------------------
# Notification Utilities
# ---------------------------
def schedule_reminder(session_time: datetime, reminder_minutes: int = 30) -> datetime:
    """
    Schedule reminder for a session.
    Returns the datetime when the reminder should be sent.
    """
    return session_time - timedelta(minutes=reminder_minutes)
