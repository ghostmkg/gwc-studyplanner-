"""
Command-line interface for StudySync
"""

import sys
from typing import Optional, List
from datetime import datetime
from pathlib import Path

# Rich library for beautiful CLI output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None

from ..core.session_manager import SessionManager
from ..core.storage import Storage
from ..utils.config import AppConfig, get_app_info
from ..utils.helpers import validate_group_name, parse_duration, parse_date_time


class StudySyncCLI:
    """Command-line interface for StudySync"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.console = Console() if RICH_AVAILABLE else None
        self.storage = Storage(config.database.url)
        self.session_manager = SessionManager(self.storage, config)
    
    def _print(self, message: str, style: Optional[str] = None) -> None:
        """Print message with optional styling"""
        if self.console and style:
            self.console.print(message, style=style)
        else:
            print(message)
    
    def _print_error(self, message: str) -> None:
        """Print error message"""
        if self.console:
            self.console.print(f"❌ Error: {message}", style="bold red")
        else:
            print(f"Error: {message}")
    
    def _print_success(self, message: str) -> None:
        """Print success message"""
        if self.console:
            self.console.print(f"✅ {message}", style="bold green")
        else:
            print(f"Success: {message}")
    
    def _print_warning(self, message: str) -> None:
        """Print warning message"""
        if self.console:
            self.console.print(f"⚠️  Warning: {message}", style="bold yellow")
        else:
            print(f"Warning: {message}")
    
    def create_group(self, name: str, description: Optional[str] = None, max_members: int = 10) -> None:
        """Create a new study group"""
        
        # Validate input
        if not validate_group_name(name):
            self._print_error("Invalid group name. Use 2-50 characters, alphanumeric, spaces, hyphens, and underscores only.")
            return
        
        if max_members < 1 or max_members > self.config.max_group_size:
            self._print_error(f"Max members must be between 1 and {self.config.max_group_size}")
            return
        
        try:
            # Check if group already exists
            existing_groups = self.storage.get_all_groups()
            if any(group['name'].lower() == name.lower() for group in existing_groups):
                self._print_error(f"Group '{name}' already exists!")
                return
            
            # Create the group
            group_data = {
                'name': name,
                'description': description or "",
                'max_members': max_members,
                'created_at': datetime.now().isoformat(),
                'members': [],
                'sessions': []
            }
            
            if self.console:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console,
                ) as progress:
                    task = progress.add_task("Creating group...", total=None)
                    group_id = self.storage.create_group(group_data)
                    progress.update(task, completed=True)
            else:
                print("Creating group...")
                group_id = self.storage.create_group(group_data)
            
            self._print_success(f"Created study group '{name}' with ID: {group_id}")
            
            if description:
                self._print(f"Description: {description}")
            self._print(f"Max members: {max_members}")
            
        except Exception as e:
            self._print_error(f"Failed to create group: {e}")
    
    def list_groups(self) -> None:
        """List all study groups"""
        try:
            groups = self.storage.get_all_groups()
            
            if not groups:
                self._print("No study groups found. Create one with 'studysync create-group'")
                return
            
            if self.console:
                table = Table(title="📚 Study Groups")
                table.add_column("Name", style="cyan", no_wrap=True)
                table.add_column("Description", style="magenta")
                table.add_column("Members", justify="center", style="green")
                table.add_column("Sessions", justify="center", style="blue")
                table.add_column("Created", style="yellow")
                
                for group in groups:
                    member_count = len(group.get('members', []))
                    session_count = len(group.get('sessions', []))
                    created_date = group.get('created_at', 'Unknown')[:10]  # Just the date part
                    
                    table.add_row(
                        group['name'],
                        group.get('description', 'No description')[:50],
                        str(member_count),
                        str(session_count),
                        created_date
                    )
                
                self.console.print(table)
            else:
                print("\nStudy Groups:")
                print("-" * 60)
                for group in groups:
                    member_count = len(group.get('members', []))
                    session_count = len(group.get('sessions', []))
                    print(f"Name: {group['name']}")
                    print(f"Description: {group.get('description', 'No description')}")
                    print(f"Members: {member_count}, Sessions: {session_count}")
                    print("-" * 60)
                    
        except Exception as e:
            self._print_error(f"Failed to list groups: {e}")
    
    def schedule_session(self, group_name: str, date: str, time: str, 
                        duration: str = "1h", topic: Optional[str] = None) -> None:
        """Schedule a study session"""
        
        try:
            # Validate and parse input
            session_datetime = parse_date_time(date, time)
            if not session_datetime:
                self._print_error("Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time.")
                return
            
            if session_datetime < datetime.now():
                self._print_error("Cannot schedule sessions in the past.")
                return
            
            duration_minutes = parse_duration(duration)
            if not duration_minutes or duration_minutes <= 0:
                self._print_error("Invalid duration format. Use formats like '1h', '90m', '2h30m'.")
                return
            
            # Find the group
            groups = self.storage.get_all_groups()
            target_group = None
            for group in groups:
                if group['name'].lower() == group_name.lower():
                    target_group = group
                    break
            
            if not target_group:
                self._print_error(f"Group '{group_name}' not found.")
                return
            
            # Schedule the session
            session_data = {
                'group_id': target_group.get('id'),
                'topic': topic or "Study Session",
                'start_time': session_datetime.isoformat(),
                'duration_minutes': duration_minutes,
                'status': 'scheduled',
                'created_at': datetime.now().isoformat(),
                'attendees': []
            }
            
            session_id = self.session_manager.create_session(session_data)
            
            self._print_success(f"Scheduled session for '{group_name}'")
            self._print(f"Session ID: {session_id}")
            self._print(f"Topic: {topic or 'Study Session'}")
            self._print(f"Date & Time: {session_datetime.strftime('%Y-%m-%d at %H:%M')}")
            self._print(f"Duration: {duration}")
            
        except Exception as e:
            self._print_error(f"Failed to schedule session: {e}")
    
    def join_group(self, group_name: str, username: Optional[str] = None) -> None:
        """Join a study group"""
        
        if not username:
            username = input("Enter your username: ").strip()
        
        if not username:
            self._print_error("Username is required.")
            return
        
        try:
            # Find the group
            groups = self.storage.get_all_groups()
            target_group = None
            for group in groups:
                if group['name'].lower() == group_name.lower():
                    target_group = group
                    break
            
            if not target_group:
                self._print_error(f"Group '{group_name}' not found.")
                return
            
            # Check if already a member
            members = target_group.get('members', [])
            if any(member.get('username', '').lower() == username.lower() for member in members):
                self._print_warning(f"You are already a member of '{group_name}'.")
                return
            
            # Check group capacity
            if len(members) >= target_group.get('max_members', 10):
                self._print_error(f"Group '{group_name}' is full.")
                return
            
            # Add member
            member_data = {
                'username': username,
                'joined_at': datetime.now().isoformat(),
                'role': 'member'
            }
            
            members.append(member_data)
            target_group['members'] = members
            
            self.storage.update_group(target_group['id'], target_group)
            
            self._print_success(f"Successfully joined '{group_name}'!")
            self._print(f"Welcome, {username}!")
            
        except Exception as e:
            self._print_error(f"Failed to join group: {e}")
    
    def show_analytics(self, group_name: Optional[str] = None, period: str = "last-week") -> None:
        """Show study analytics"""
        
        try:
            if self.console:
                self.console.print(Panel(
                    "📊 Study Analytics (Coming Soon)",
                    title="StudySync Analytics",
                    border_style="blue"
                ))
                self.console.print("This feature will show:")
                self.console.print("• Total study hours")
                self.console.print("• Session attendance rates")
                self.console.print("• Group participation statistics")
                self.console.print("• Progress tracking")
            else:
                print("\n=== Study Analytics (Coming Soon) ===")
                print("This feature will show:")
                print("- Total study hours")
                print("- Session attendance rates")
                print("- Group participation statistics")
                print("- Progress tracking")
                
        except Exception as e:
            self._print_error(f"Failed to show analytics: {e}")
    
    def show_version(self) -> None:
        """Show version information"""
        
        app_info = get_app_info()
        
        if self.console:
            info_text = f"""
[bold cyan]{app_info['name']}[/bold cyan] v{app_info['version']}

{app_info['description']}

[dim]Author: {app_info['author']}
License: {app_info['license']}[/dim]
            """
            self.console.print(Panel(info_text.strip(), title="About StudySync", border_style="green"))
        else:
            print(f"\n{app_info['name']} v{app_info['version']}")
            print(f"{app_info['description']}")
            print(f"\nAuthor: {app_info['author']}")
            print(f"License: {app_info['license']}")
            print()


def main():
    """Main CLI entry point (for testing)"""
    from ..utils.config import load_config
    
    config = load_config()
    cli = StudySyncCLI(config)
    cli.show_version()


if __name__ == "__main__":
    main()