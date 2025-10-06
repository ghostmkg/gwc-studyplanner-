"""
Notification engine for StudySync
Handles sending reminders and notifications via various channels
"""

import smtplib
import json
import requests
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

from ..utils.config import AppConfig, NotificationConfig


class NotificationEngine:
    """Handles sending notifications through various channels"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.notification_config = config.notifications
        self.logger = logging.getLogger(__name__)
    
    def send_session_reminder(self, session: Dict[str, Any], 
                            recipients: List[str],
                            hours_before: int = 2) -> bool:
        """
        Send session reminder notification
        
        Args:
            session: Session information
            recipients: List of usernames or email addresses
            hours_before: Hours before session to send reminder
        
        Returns:
            bool: True if notification sent successfully
        """
        try:
            start_time = datetime.fromisoformat(session['start_time'])
            
            # Prepare message content
            subject = f"📚 StudySync Reminder: {session['topic']}"
            
            message_body = self._format_session_reminder(session, hours_before)
            
            # Send via enabled channels
            success = False
            
            if self.notification_config.email_enabled:
                success |= self._send_email_notification(subject, message_body, recipients)
            
            if self.notification_config.slack_webhook:
                success |= self._send_slack_notification(message_body)
            
            if self.notification_config.discord_webhook:
                success |= self._send_discord_notification(message_body)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send session reminder: {e}")
            return False
    
    def send_session_cancelled_notification(self, session: Dict[str, Any], 
                                          recipients: List[str],
                                          reason: str = "") -> bool:
        """Send session cancellation notification"""
        try:
            subject = f"❌ StudySync: Session Cancelled - {session['topic']}"
            
            message_body = self._format_cancellation_message(session, reason)
            
            # Send via enabled channels
            success = False
            
            if self.notification_config.email_enabled:
                success |= self._send_email_notification(subject, message_body, recipients)
            
            if self.notification_config.slack_webhook:
                success |= self._send_slack_notification(message_body)
            
            if self.notification_config.discord_webhook:
                success |= self._send_discord_notification(message_body)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send cancellation notification: {e}")
            return False
    
    def send_session_update_notification(self, session: Dict[str, Any], 
                                       recipients: List[str],
                                       changes: Dict[str, Any]) -> bool:
        """Send session update notification"""
        try:
            subject = f"📝 StudySync: Session Updated - {session['topic']}"
            
            message_body = self._format_update_message(session, changes)
            
            # Send via enabled channels
            success = False
            
            if self.notification_config.email_enabled:
                success |= self._send_email_notification(subject, message_body, recipients)
            
            if self.notification_config.slack_webhook:
                success |= self._send_slack_notification(message_body)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send update notification: {e}")
            return False
    
    def send_group_invitation(self, group: Dict[str, Any], 
                            recipient: str,
                            invited_by: str) -> bool:
        """Send group invitation notification"""
        try:
            subject = f"🎓 StudySync: You're invited to join {group['name']}"
            
            message_body = self._format_invitation_message(group, invited_by)
            
            if self.notification_config.email_enabled:
                return self._send_email_notification(subject, message_body, [recipient])
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to send invitation: {e}")
            return False
    
    def _send_email_notification(self, subject: str, body: str, 
                               recipients: List[str]) -> bool:
        """Send email notification"""
        if not self.notification_config.email_enabled:
            return False
        
        try:
            # Create message
            msg = MimeMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.notification_config.smtp_username
            msg['To'] = ', '.join(recipients)
            
            # Add body
            html_body = self._convert_to_html(body)
            msg.attach(MimeText(body, 'plain'))
            msg.attach(MimeText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.notification_config.smtp_server, 
                            self.notification_config.smtp_port) as server:
                server.starttls()
                server.login(self.notification_config.smtp_username, 
                           self.notification_config.smtp_password)
                server.send_message(msg)
            
            self.logger.info(f"Email sent to {len(recipients)} recipients")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False
    
    def _send_slack_notification(self, message: str) -> bool:
        """Send Slack notification via webhook"""
        if not self.notification_config.slack_webhook:
            return False
        
        try:
            payload = {
                "text": message,
                "username": "StudySync Bot",
                "icon_emoji": ":books:"
            }
            
            response = requests.post(
                self.notification_config.slack_webhook,
                json=payload,
                timeout=10
            )
            
            response.raise_for_status()
            self.logger.info("Slack notification sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {e}")
            return False
    
    def _send_discord_notification(self, message: str) -> bool:
        """Send Discord notification via webhook"""
        if not self.notification_config.discord_webhook:
            return False
        
        try:
            payload = {
                "content": message,
                "username": "StudySync Bot",
                "avatar_url": "https://example.com/studysync-logo.png"  # Optional
            }
            
            response = requests.post(
                self.notification_config.discord_webhook,
                json=payload,
                timeout=10
            )
            
            response.raise_for_status()
            self.logger.info("Discord notification sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Discord notification: {e}")
            return False
    
    def _format_session_reminder(self, session: Dict[str, Any], hours_before: int) -> str:
        """Format session reminder message"""
        start_time = datetime.fromisoformat(session['start_time'])
        duration = session.get('duration_minutes', 60)
        
        message = f"""
📚 StudySync Session Reminder

Topic: {session['topic']}
Start Time: {start_time.strftime('%Y-%m-%d at %H:%M')}
Duration: {duration} minutes
Group: {session.get('group_name', 'Unknown')}

This session starts in {hours_before} hours. Don't forget to join!

Session Details:
- Attendees: {len(session.get('attendees', []))} registered
- Status: {session.get('status', 'scheduled').title()}

Get ready to learn together! 🎓
        """.strip()
        
        return message
    
    def _format_cancellation_message(self, session: Dict[str, Any], reason: str) -> str:
        """Format cancellation message"""
        start_time = datetime.fromisoformat(session['start_time'])
        
        message = f"""
❌ StudySync Session Cancelled

Unfortunately, the following session has been cancelled:

Topic: {session['topic']}
Original Time: {start_time.strftime('%Y-%m-%d at %H:%M')}
Group: {session.get('group_name', 'Unknown')}

Reason: {reason or 'No reason provided'}

We apologize for any inconvenience. Please check for rescheduled sessions.
        """.strip()
        
        return message
    
    def _format_update_message(self, session: Dict[str, Any], changes: Dict[str, Any]) -> str:
        """Format session update message"""
        start_time = datetime.fromisoformat(session['start_time'])
        
        message = f"""
📝 StudySync Session Updated

The following session has been updated:

Topic: {session['topic']}
Time: {start_time.strftime('%Y-%m-%d at %H:%M')}
Group: {session.get('group_name', 'Unknown')}

Changes made:
        """.strip()
        
        for field, new_value in changes.items():
            if field == 'start_time':
                new_time = datetime.fromisoformat(new_value)
                message += f"\n- Start time changed to: {new_time.strftime('%Y-%m-%d at %H:%M')}"
            elif field == 'topic':
                message += f"\n- Topic changed to: {new_value}"
            elif field == 'duration_minutes':
                message += f"\n- Duration changed to: {new_value} minutes"
        
        message += "\n\nPlease update your calendar accordingly."
        
        return message
    
    def _format_invitation_message(self, group: Dict[str, Any], invited_by: str) -> str:
        """Format group invitation message"""
        message = f"""
🎓 StudySync Group Invitation

You've been invited to join a study group!

Group: {group['name']}
Description: {group.get('description', 'No description provided')}
Members: {len(group.get('members', []))}
Invited by: {invited_by}

Join this group to participate in collaborative study sessions and stay organized with your learning goals.

To join, use the StudySync CLI:
studysync join-group "{group['name']}" --username "your-username"

Happy studying! 📚
        """.strip()
        
        return message
    
    def _convert_to_html(self, text: str) -> str:
        """Convert plain text to HTML format"""
        # Simple text-to-HTML conversion
        html = text.replace('\n', '<br>\n')
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        {html}
        </body>
        </html>
        """
        return html
    
    def test_notification_channels(self) -> Dict[str, bool]:
        """Test all configured notification channels"""
        results = {}
        
        test_message = "🧪 StudySync notification test - all systems operational!"
        
        # Test email
        if self.notification_config.email_enabled:
            results['email'] = self._send_email_notification(
                "StudySync Test", 
                test_message, 
                [self.notification_config.smtp_username]
            )
        else:
            results['email'] = False
        
        # Test Slack
        if self.notification_config.slack_webhook:
            results['slack'] = self._send_slack_notification(test_message)
        else:
            results['slack'] = False
        
        # Test Discord
        if self.notification_config.discord_webhook:
            results['discord'] = self._send_discord_notification(test_message)
        else:
            results['discord'] = False
        
        return results