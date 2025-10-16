# StudySync CLI Usage Guide

This document explains how to use the StudySync CLI to manage groups, sessions, and analytics.

## Installation (local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Commands

### Create a group
```bash
python main.py create-group "CS101 Study Group" -d "Computer Science fundamentals" -m 20
```

### List groups
```bash
python main.py list-groups
```

### Join a group
```bash
python main.py join-group "CS101 Study Group" -u alice
```

### Schedule a session
```bash
python main.py schedule -g "CS101 Study Group" -d 2025-10-20 -t 14:00 -dur 90m --topic "Graphs & Trees"
```

### View analytics
```bash
python main.py analytics -g "CS101 Study Group" -p last-week
```

### Interactive mode
```bash
python -m src.ui.cli.main interactive
```

## Tips
- Use ISO date (YYYY-MM-DD) and 24h time (HH:MM)
- Duration accepts `m`, `h`, or minutes (e.g., `90m`, `1.5h`, `60`)
- Run `python main.py --help` to view available commands


