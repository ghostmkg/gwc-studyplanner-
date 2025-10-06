"""
Configuration management for StudySync
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    url: str = "sqlite:///studysync.db"
    echo: bool = False


@dataclass
class NotificationConfig:
    """Notification settings"""
    email_enabled: bool = False
    smtp_server: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    slack_webhook: str = ""
    discord_webhook: str = ""


@dataclass
class AppConfig:
    """Main application configuration"""
    debug: bool = False
    log_level: str = "INFO"
    data_dir: str = "data"
    backup_enabled: bool = True
    backup_interval_hours: int = 24
    max_group_size: int = 50
    session_reminder_hours: int = 2
    database: DatabaseConfig = None
    notifications: NotificationConfig = None

    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig()
        if self.notifications is None:
            self.notifications = NotificationConfig()


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    Load configuration from file or environment variables
    
    Args:
        config_path: Path to configuration file (optional)
    
    Returns:
        AppConfig: Loaded configuration
    """
    config = AppConfig()
    
    # Try to load from file first
    if config_path is None:
        config_path = os.environ.get("STUDYSYNC_CONFIG", "config.json")
    
    config_file = Path(config_path)
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                config = _merge_config(config, file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file {config_path}: {e}")
    
    # Override with environment variables
    config = _load_from_env(config)
    
    # Ensure data directory exists
    Path(config.data_dir).mkdir(parents=True, exist_ok=True)
    
    return config


def save_config(config: AppConfig, config_path: str = "config.json") -> None:
    """
    Save configuration to file
    
    Args:
        config: Configuration to save
        config_path: Path to save configuration
    """
    config_dict = asdict(config)
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
    except IOError as e:
        print(f"Error: Could not save config file {config_path}: {e}")


def _merge_config(base_config: AppConfig, file_config: Dict[str, Any]) -> AppConfig:
    """Merge file configuration with base configuration"""
    
    # Update main app config
    for key, value in file_config.items():
        if hasattr(base_config, key) and not isinstance(getattr(base_config, key), (DatabaseConfig, NotificationConfig)):
            setattr(base_config, key, value)
    
    # Update database config
    if "database" in file_config:
        db_config = file_config["database"]
        for key, value in db_config.items():
            if hasattr(base_config.database, key):
                setattr(base_config.database, key, value)
    
    # Update notification config
    if "notifications" in file_config:
        notif_config = file_config["notifications"]
        for key, value in notif_config.items():
            if hasattr(base_config.notifications, key):
                setattr(base_config.notifications, key, value)
    
    return base_config


def _load_from_env(config: AppConfig) -> AppConfig:
    """Load configuration from environment variables"""
    
    # Main app settings
    config.debug = os.environ.get("STUDYSYNC_DEBUG", "false").lower() == "true"
    config.log_level = os.environ.get("STUDYSYNC_LOG_LEVEL", config.log_level)
    config.data_dir = os.environ.get("STUDYSYNC_DATA_DIR", config.data_dir)
    
    # Database settings
    if "DATABASE_URL" in os.environ:
        config.database.url = os.environ["DATABASE_URL"]
    
    # Notification settings
    if "SMTP_SERVER" in os.environ:
        config.notifications.smtp_server = os.environ["SMTP_SERVER"]
        config.notifications.email_enabled = True
    
    if "SMTP_USERNAME" in os.environ:
        config.notifications.smtp_username = os.environ["SMTP_USERNAME"]
    
    if "SMTP_PASSWORD" in os.environ:
        config.notifications.smtp_password = os.environ["SMTP_PASSWORD"]
    
    if "SLACK_WEBHOOK" in os.environ:
        config.notifications.slack_webhook = os.environ["SLACK_WEBHOOK"]
    
    if "DISCORD_WEBHOOK" in os.environ:
        config.notifications.discord_webhook = os.environ["DISCORD_WEBHOOK"]
    
    return config


def get_version() -> str:
    """Get application version"""
    return "0.1.0"


def get_app_info() -> Dict[str, str]:
    """Get application information"""
    return {
        "name": "StudySync",
        "version": get_version(),
        "description": "Group Study Scheduler",
        "author": "StudySync Community",
        "license": "MIT"
    }