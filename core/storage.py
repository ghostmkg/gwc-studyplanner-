import json
from pathlib import Path

DATA_FILE = Path("data/sessions.json")

def load_sessions():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_sessions(sessions):
    with open(DATA_FILE, "w") as f:
        json.dump(sessions, f, indent=4)
