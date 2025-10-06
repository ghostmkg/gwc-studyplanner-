"""
StudySync - Group Study Scheduler (CLI Entry Point)
"""

import sys
import argparse
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from src.ui.cli import StudySyncCLI
from src.utils.config import load_config


def main():
    """Main entry point for StudySync application"""
    parser = argparse.ArgumentParser(
        description="StudySync - Group Study Scheduler",
        prog="studysync"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create group command
    create_parser = subparsers.add_parser("create-group", help="Create a new study group")
    create_parser.add_argument("name", help="Name of the study group")
    create_parser.add_argument("--description", "-d", help="Description of the study group")
    create_parser.add_argument("--max-members", "-m", type=int, default=10, 
                              help="Maximum number of members (default: 10)")
    
    # Schedule session command
    schedule_parser = subparsers.add_parser("schedule", help="Schedule a study session")
    schedule_parser.add_argument("--group", "-g", required=True, help="Study group name")
    schedule_parser.add_argument("--date", "-d", required=True, help="Date (YYYY-MM-DD)")
    schedule_parser.add_argument("--time", "-t", required=True, help="Time (HH:MM)")
    schedule_parser.add_argument("--duration", "-dur", default="1h", help="Duration (e.g., 1h, 90m)")
    schedule_parser.add_argument("--topic", help="Session topic")
    
    # List groups command
    subparsers.add_parser("list-groups", help="List all study groups")
    
    # Join group command
    join_parser = subparsers.add_parser("join-group", help="Join a study group")
    join_parser.add_argument("group_name", help="Name of the group to join")
    join_parser.add_argument("--username", "-u", help="Your username")
    
    # Analytics command
    analytics_parser = subparsers.add_parser("analytics", help="View study analytics")
    analytics_parser.add_argument("--group", "-g", help="Specific group (optional)")
    analytics_parser.add_argument("--period", "-p", default="last-week", 
                                 choices=["today", "last-week", "last-month", "all"],
                                 help="Time period for analytics")
    
    # Version command
    subparsers.add_parser("version", help="Show version information")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Load configuration
    config = load_config()
    cli = StudySyncCLI(config)
    
    try:
        if args.command == "create-group":
            cli.create_group(args.name, args.description, args.max_members)
        elif args.command == "schedule":
            cli.schedule_session(args.group, args.date, args.time, args.duration, args.topic)
        elif args.command == "list-groups":
            cli.list_groups()
        elif args.command == "join-group":
            cli.join_group(args.group_name, args.username)
        elif args.command == "analytics":
            cli.show_analytics(args.group, args.period)
        elif args.command == "version":
            cli.show_version()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
