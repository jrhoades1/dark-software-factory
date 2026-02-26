"""
Tool: Session Status Gatherer
Purpose: Collect project state for session-start briefing.
Usage: python3 hooks/session_status.py

Reads local project files and outputs a JSON summary.
Works from any project directory that follows DSF structure.
"""

import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MEMORY_DIR = PROJECT_ROOT / "memory"
MEMORY_MD = MEMORY_DIR / "MEMORY.md"
LOGS_DIR = MEMORY_DIR / "logs"
RULES_DIR = PROJECT_ROOT / ".claude" / "rules"
TASKS_DB = PROJECT_ROOT / "data" / "tasks.db"


def get_project_identity():
    """Extract project name and type from MEMORY.md."""
    identity = {"name": PROJECT_ROOT.name, "type": "unknown", "project_code": None}

    if MEMORY_MD.exists():
        content = MEMORY_MD.read_text(encoding="utf-8")
        for line in content.splitlines():
            line_stripped = line.strip()
            if line_stripped.startswith("- Project:"):
                identity["name"] = line_stripped.split(":", 1)[1].strip()
            elif line_stripped.startswith("- Project Code:"):
                identity["project_code"] = line_stripped.split(":", 1)[1].strip()
            elif line_stripped.startswith("- Billing:"):
                billing = line_stripped.split(":", 1)[1].strip().lower()
                if billing in ("internal", "internal/research"):
                    identity["type"] = "internal"
                else:
                    identity["type"] = "client"

    # Fallback: check if billing-protocol rule exists
    if identity["type"] == "unknown":
        if (RULES_DIR / "billing-protocol.md").exists():
            identity["type"] = "client"
        else:
            identity["type"] = "internal"

    return identity


def get_last_session():
    """Find the most recent daily log and extract last entry."""
    if not LOGS_DIR.exists():
        return None

    logs = sorted(LOGS_DIR.glob("*.md"), reverse=True)
    for log_path in logs[:3]:  # Check last 3 days
        content = log_path.read_text(encoding="utf-8")
        lines = [l.strip() for l in content.splitlines() if l.strip().startswith("- [")]
        if lines:
            return {
                "date": log_path.stem,
                "last_entry": lines[-1],
                "entry_count": len(lines),
            }

    return None


def get_task_summary():
    """Get task counts from SQLite if database exists."""
    if not TASKS_DB.exists():
        return None

    try:
        conn = sqlite3.connect(str(TASKS_DB))
        pending = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status='pending'"
        ).fetchone()[0]
        overdue = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status='pending' AND due_date < date('now')"
        ).fetchone()[0]
        due_this_week = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status='pending' AND due_date BETWEEN date('now') AND date('now', '+7 days')"
        ).fetchone()[0]
        conn.close()
        return {
            "pending": pending,
            "overdue": overdue,
            "due_this_week": due_this_week,
        }
    except Exception:
        return None


def get_today_log_exists():
    """Check if today's log already exists."""
    today = datetime.now().strftime("%Y-%m-%d")
    return (LOGS_DIR / f"{today}.md").exists()


def get_time_of_day():
    """Return morning/afternoon/evening based on current hour."""
    hour = datetime.now().hour
    if hour < 12:
        return "morning"
    elif hour < 17:
        return "afternoon"
    else:
        return "evening"


def main():
    now = datetime.now()
    status = {
        "timestamp": now.isoformat(),
        "time_of_day": get_time_of_day(),
        "project": get_project_identity(),
        "last_session": get_last_session(),
        "tasks": get_task_summary(),
        "today_log_exists": get_today_log_exists(),
        "memory_exists": MEMORY_MD.exists(),
    }
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
