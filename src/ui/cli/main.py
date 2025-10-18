"""
StudySync CLI - Main CLI Interface Implementation
"""

import click
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import os
from pathlib import Path

from ..core.session_manager import SessionManager
from ..core.group_manager import GroupManager
from ..core.notification_engine import NotificationEngine
from ..core.storage import Storage
from ...utils.config import load_config
from ...utils.logger import get_logger

logger = get_logger(__name__)


class StudySyncCLI:
    """Command Line Interface for StudySync"""
    
    def __init__(self, config=None):
        """Initialize CLI with configuration"""
        self.config = config or load_config()
        self.storage = Storage(self.config)
        self.session_manager = SessionManager(self.storage, self.config)
        self.group_manager = GroupManager(self.storage, self.config)
        self.notification_engine = NotificationEngine(self.config)
        
        # Initialize storage
        self.storage.initialize()
    
    def create_group(self, name: str, description: str = None, max_members: int = 10):
        """Create a new study group"""
        try:
            group_data = {
                "name": name,
                "description": description or f"Study group: {name}",
                "max_members": max_members,
                "created_at": datetime.now().isoformat(),
                "members": [],
                "sessions": []
            }
            
            group_id = self.group_manager.create_group(group_data)
            
            click.echo(click.style(f"✅ Study group '{name}' created successfully!", fg='green'))
            click.echo(f"   Group ID: {group_id}")
            click.echo(f"   Max Members: {max_members}")
            click.echo(f"   Description: {description or 'No description provided'}")
            
        except Exception as e:
            click.echo(click.style(f"❌ Error creating group: {e}", fg='red'))
            logger.error(f"Error creating group: {e}")
    
    def schedule_session(self, group_name: str, date: str, time: str, 
                        duration: str = "1h", topic: str = None):
        """Schedule a study session"""
        try:
            # Parse date and time
            session_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            
            # Parse duration
            duration_minutes = self._parse_duration(duration)
            end_time = session_datetime + timedelta(minutes=duration_minutes)
            
            session_data = {
                "group_name": group_name,
                "topic": topic or "General Study Session",
                "start_time": session_datetime.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_minutes": duration_minutes,
                "status": "scheduled",
                "attendees": [],
                "created_at": datetime.now().isoformat()
            }
            
            session_id = self.session_manager.create_session(session_data)
            
            click.echo(click.style(f"✅ Study session scheduled successfully!", fg='green'))
            click.echo(f"   Session ID: {session_id}")
            click.echo(f"   Group: {group_name}")
            click.echo(f"   Date: {date}")
            click.echo(f"   Time: {time}")
            click.echo(f"   Duration: {duration}")
            click.echo(f"   Topic: {topic or 'General Study Session'}")
            
        except ValueError as e:
            click.echo(click.style(f"❌ Invalid date/time format: {e}", fg='red'))
        except Exception as e:
            click.echo(click.style(f"❌ Error scheduling session: {e}", fg='red'))
            logger.error(f"Error scheduling session: {e}")
    
    def list_groups(self):
        """List all study groups"""
        try:
            groups = self.group_manager.get_all_groups()
            
            if not groups:
                click.echo(click.style("📝 No study groups found.", fg='yellow'))
                return
            
            click.echo(click.style("📚 Study Groups:", fg='blue', bold=True))
            click.echo("=" * 50)
            
            for group in groups:
                click.echo(f"🏷️  {group['name']}")
                click.echo(f"   ID: {group.get('id', 'N/A')}")
                click.echo(f"   Description: {group.get('description', 'No description')}")
                click.echo(f"   Members: {len(group.get('members', []))}/{group.get('max_members', 'N/A')}")
                click.echo(f"   Sessions: {len(group.get('sessions', []))}")
                click.echo(f"   Created: {group.get('created_at', 'N/A')}")
                click.echo()
                
        except Exception as e:
            click.echo(click.style(f"❌ Error listing groups: {e}", fg='red'))
            logger.error(f"Error listing groups: {e}")
    
    def join_group(self, group_name: str, username: str = None):
        """Join a study group"""
        try:
            if not username:
                username = click.prompt("Enter your username")
            
            success = self.group_manager.add_member(group_name, username)
            
            if success:
                click.echo(click.style(f"✅ Successfully joined '{group_name}'!", fg='green'))
                click.echo(f"   Username: {username}")
            else:
                click.echo(click.style(f"❌ Failed to join group '{group_name}'", fg='red'))
                click.echo("   Group might not exist or be full.")
                
        except Exception as e:
            click.echo(click.style(f"❌ Error joining group: {e}", fg='red'))
            logger.error(f"Error joining group: {e}")
    
    def show_analytics(self, group_name: str = None, period: str = "last-week"):
        """Show study analytics"""
        try:
            analytics = self.session_manager.get_analytics(group_name, period)
            
            click.echo(click.style("📊 Study Analytics", fg='blue', bold=True))
            click.echo("=" * 30)
            
            if group_name:
                click.echo(f"Group: {group_name}")
            else:
                click.echo("All Groups")
            
            click.echo(f"Period: {period}")
            click.echo()
            
            # Display analytics
            click.echo(f"📈 Total Sessions: {analytics.get('total_sessions', 0)}")
            click.echo(f"⏱️  Total Study Time: {analytics.get('total_hours', 0):.1f} hours")
            click.echo(f"👥 Average Attendance: {analytics.get('avg_attendance', 0):.1f} members")
            click.echo(f"📅 Most Active Day: {analytics.get('most_active_day', 'N/A')}")
            
            # Show recent sessions
            recent_sessions = analytics.get('recent_sessions', [])
            if recent_sessions:
                click.echo()
                click.echo(click.style("🕒 Recent Sessions:", fg='cyan'))
                for session in recent_sessions[:5]:  # Show last 5
                    click.echo(f"   • {session.get('topic', 'N/A')} - {session.get('date', 'N/A')}")
            
        except Exception as e:
            click.echo(click.style(f"❌ Error showing analytics: {e}", fg='red'))
            logger.error(f"Error showing analytics: {e}")
    
    def show_version(self):
        """Show version information"""
        version_info = {
            "StudySync": "1.0.0",
            "Python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "CLI": "1.0.0"
        }
        
        click.echo(click.style("📋 StudySync Version Information", fg='blue', bold=True))
        click.echo("=" * 35)
        
        for key, value in version_info.items():
            click.echo(f"{key}: {value}")
    
    def _parse_duration(self, duration: str) -> int:
        """Parse duration string to minutes"""
        duration = duration.lower().strip()
        
        if duration.endswith('h'):
            hours = float(duration[:-1])
            return int(hours * 60)
        elif duration.endswith('m'):
            return int(duration[:-1])
        elif duration.endswith('min'):
            return int(duration[:-3])
        else:
            # Assume minutes if no unit specified
            return int(duration)
    
    def interactive_mode(self):
        """Start interactive mode"""
        click.echo(click.style("🎓 Welcome to StudySync Interactive Mode!", fg='green', bold=True))
        click.echo("Type 'help' for available commands or 'exit' to quit.")
        click.echo()
        
        while True:
            try:
                command = click.prompt("studysync", type=str).strip()
                
                if command.lower() in ['exit', 'quit', 'q']:
                    click.echo(click.style("👋 Goodbye!", fg='yellow'))
                    break
                elif command.lower() == 'help':
                    self._show_interactive_help()
                elif command.lower() == 'groups':
                    self.list_groups()
                elif command.lower().startswith('create '):
                    parts = command.split(' ', 1)
                    if len(parts) > 1:
                        self.create_group(parts[1])
                elif command.lower().startswith('join '):
                    parts = command.split(' ', 1)
                    if len(parts) > 1:
                        self.join_group(parts[1])
                elif command.lower() == 'analytics':
                    self.show_analytics()
                else:
                    click.echo(click.style(f"Unknown command: {command}", fg='red'))
                    click.echo("Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                click.echo(click.style("\n👋 Goodbye!", fg='yellow'))
                break
            except Exception as e:
                click.echo(click.style(f"Error: {e}", fg='red'))
    
    def _show_interactive_help(self):
        """Show help for interactive mode"""
        help_text = """
🎓 StudySync Interactive Commands:

📚 Groups:
  groups                    - List all study groups
  create <group_name>       - Create a new study group
  join <group_name>         - Join a study group

📅 Sessions:
  schedule                  - Schedule a new session (interactive)
  
📊 Analytics:
  analytics                 - Show study analytics

🔧 General:
  help                      - Show this help message
  exit/quit/q               - Exit interactive mode
        """
        click.echo(help_text)


# CLI Commands using Click decorators
@click.group()
@click.version_option(version="1.0.0", prog_name="StudySync")
def cli():
    """StudySync - Group Study Scheduler"""
    pass


@cli.command()
@click.argument('name')
@click.option('--description', '-d', help='Description of the study group')
@click.option('--max-members', '-m', default=10, help='Maximum number of members')
def create_group(name, description, max_members):
    """Create a new study group"""
    cli_instance = StudySyncCLI()
    cli_instance.create_group(name, description, max_members)


@cli.command()
@click.option('--group', '-g', required=True, help='Study group name')
@click.option('--date', '-d', required=True, help='Date (YYYY-MM-DD)')
@click.option('--time', '-t', required=True, help='Time (HH:MM)')
@click.option('--duration', '-dur', default='1h', help='Duration (e.g., 1h, 90m)')
@click.option('--topic', help='Session topic')
def schedule(group, date, time, duration, topic):
    """Schedule a study session"""
    cli_instance = StudySyncCLI()
    cli_instance.schedule_session(group, date, time, duration, topic)


@cli.command()
def list_groups():
    """List all study groups"""
    cli_instance = StudySyncCLI()
    cli_instance.list_groups()


@cli.command()
@click.argument('group_name')
@click.option('--username', '-u', help='Your username')
def join_group(group_name, username):
    """Join a study group"""
    cli_instance = StudySyncCLI()
    cli_instance.join_group(group_name, username)


@cli.command()
@click.option('--group', '-g', help='Specific group (optional)')
@click.option('--period', '-p', default='last-week', 
              type=click.Choice(['today', 'last-week', 'last-month', 'all']),
              help='Time period for analytics')
def analytics(group, period):
    """View study analytics"""
    cli_instance = StudySyncCLI()
    cli_instance.show_analytics(group, period)


@cli.command()
def interactive():
    """Start interactive mode"""
    cli_instance = StudySyncCLI()
    cli_instance.interactive_mode()


if __name__ == '__main__':
    cli()