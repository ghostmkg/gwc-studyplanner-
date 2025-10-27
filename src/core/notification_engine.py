"""
Notification engine for StudySync
Handles sending reminders and notifications via various channels
"""

import smtplib
import json
import requests
from email.mime.text import MimeText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
import os

from ..utils.config import AppConfig


class NotificationEngine:
    """Handles sending notifications through various channels"""

    def __init__(self, config: AppConfig = None):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Notification settings
        self.email_enabled = os.getenv('STUDYSYNC_EMAIL_ENABLED', 'false').lower() == 'true'
        self.slack_enabled = os.getenv('STUDYSYNC_SLACK_ENABLED', 'false').lower() == 'true'
        
        # Email settings
        self.smtp_server = os.getenv('STUDYSYNC_SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('STUDYSYNC_SMTP_PORT', '587'))
        self.email_user = os.getenv('STUDYSYNC_EMAIL_USER', '')
        self.email_password = os.getenv('STUDYSYNC_EMAIL_PASSWORD', '')
        
        # Slack settings
        self.slack_webhook_url = os.getenv('STUDYSYNC_SLACK_WEBHOOK', '')

    def send_session_reminder(self, session_data: Dict[str, Any], recipients: List[str]) -> bool:
        """Send session reminder to recipients"""
        try:
            session_time = datetime.fromisoformat(session_data.get('start_time', ''))
            topic = session_data.get('topic', 'Study Session')
            group_name = session_data.get('group_name', 'Study Group')
            
            message = f"""
🎓 StudySync Reminder

📚 Group: {group_name}
📅 Topic: {topic}
🕐 Time: {session_time.strftime('%Y-%m-%d %H:%M')}
⏱️ Duration: {session_data.get('duration_minutes', 60)} minutes

Don't forget to join your study session!
            """.strip()
            
            success = True
            for recipient in recipients:
                if self.email_enabled:
                    success &= self._send_email(recipient, "StudySync Session Reminder", message)
                if self.slack_enabled:
                    success &= self._send_slack_notification(message)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending session reminder: {e}")
            return False

    def send_session_cancellation(self, session_data: Dict[str, Any], recipients: List[str]) -> bool:
        """Send session cancellation notice"""
        try:
            session_time = datetime.fromisoformat(session_data.get('start_time', ''))
            topic = session_data.get('topic', 'Study Session')
            group_name = session_data.get('group_name', 'Study Group')
            
            message = f"""
❌ StudySync Session Cancelled

📚 Group: {group_name}
📅 Topic: {topic}
🕐 Was scheduled for: {session_time.strftime('%Y-%m-%d %H:%M')}

The study session has been cancelled. Please check for updates.
            """.strip()
            
            success = True
            for recipient in recipients:
                if self.email_enabled:
                    success &= self._send_email(recipient, "StudySync Session Cancelled", message)
                if self.slack_enabled:
                    success &= self._send_slack_notification(message)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending cancellation notice: {e}")
            return False

    def send_attendance_reminder(self, session_data: Dict[str, Any], recipients: List[str]) -> bool:
        """Send attendance reminder for ongoing session"""
        try:
            topic = session_data.get('topic', 'Study Session')
            group_name = session_data.get('group_name', 'Study Group')
            
            message = f"""
📝 StudySync Attendance Reminder

📚 Group: {group_name}
📅 Topic: {topic}

Please mark your attendance for the current study session.
            """.strip()
            
            success = True
            for recipient in recipients:
                if self.email_enabled:
                    success &= self._send_email(recipient, "StudySync Attendance Reminder", message)
                if self.slack_enabled:
                    success &= self._send_slack_notification(message)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending attendance reminder: {e}")
            return False

    def send_weekly_summary(self, user_data: Dict[str, Any], summary_data: Dict[str, Any]) -> bool:
        """Send weekly study summary to user"""
        try:
            username = user_data.get('username', 'User')
            total_sessions = summary_data.get('total_sessions', 0)
            total_hours = summary_data.get('total_hours', 0)
            avg_attendance = summary_data.get('avg_attendance', 0)
            
            message = f"""
📊 StudySync Weekly Summary

👋 Hello {username}!

Here's your study activity for this week:

📈 Total Sessions: {total_sessions}
⏱️ Total Study Time: {total_hours:.1f} hours
👥 Average Attendance: {avg_attendance:.1f} members

Keep up the great work! 🎓
            """.strip()
            
            email = user_data.get('email', '')
            if email and self.email_enabled:
                return self._send_email(email, "StudySync Weekly Summary", message)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending weekly summary: {e}")
            return False

    def _send_email(self, recipient: str, subject: str, message: str) -> bool:
        """Send email notification"""
        try:
            if not self.email_user or not self.email_password:
                self.logger.warning("Email credentials not configured")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MimeText(message, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_user, recipient, text)
            server.quit()
            
            self.logger.info(f"Email sent to {recipient}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending email to {recipient}: {e}")
            return False

    def _send_slack_notification(self, message: str) -> bool:
        """Send Slack notification"""
        try:
            if not self.slack_webhook_url:
                self.logger.warning("Slack webhook URL not configured")
                return False
            
            payload = {
                "text": message,
                "username": "StudySync",
                "icon_emoji": ":books:"
            }
            
            response = requests.post(self.slack_webhook_url, json=payload)
            response.raise_for_status()
            
            self.logger.info("Slack notification sent")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending Slack notification: {e}")
            return False

    def schedule_reminders(self, session_data: Dict[str, Any], recipients: List[str]) -> bool:
        """Schedule reminders for a session"""
        try:
            session_time = datetime.fromisoformat(session_data.get('start_time', ''))
            
            # Schedule reminder 1 hour before
            reminder_time = session_time - timedelta(hours=1)
            if reminder_time > datetime.now():
                # In a real implementation, you would use a task scheduler like Celery
                # For now, we'll just log the reminder
                self.logger.info(f"Reminder scheduled for {reminder_time} for session {session_data.get('id')}")
            
            # Schedule attendance reminder 15 minutes after start
            attendance_time = session_time + timedelta(minutes=15)
            if attendance_time > datetime.now():
                self.logger.info(f"Attendance reminder scheduled for {attendance_time} for session {session_data.get('id')}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error scheduling reminders: {e}")
            return False
