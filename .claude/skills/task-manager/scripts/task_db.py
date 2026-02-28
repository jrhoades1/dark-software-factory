"""
Tool: Task Database Manager
Purpose: SQLite CRUD operations for task tracking.
Usage: python3 .claude/skills/task-manager/scripts/task_db.py <command> [options]

Commands:
  add       Add a new task
  list      List tasks (with filters)
  complete  Mark a task as completed
  update    Update task fields
  delete    Delete a task
  stats     Show task statistics
"""

import argparse
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent.parent.parent / "data" / "tasks.db"


def get_connection():
    """Get or create database connection with table setup."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            due_date TEXT,
            project TEXT DEFAULT '',
            tags TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            completed_at TEXT
        )
    """)
    conn.commit()
    return conn


def add_task(args):
    """Add a new task."""
    conn = get_connection()
    conn.execute(
        """INSERT INTO tasks (title, description, priority, due_date, project, tags)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (args.title, args.description or "", args.priority or "medium",
         args.due or None, args.project or "", args.tags or "")
    )
    conn.commit()
    task_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    print(json.dumps({"status": "added", "id": task_id, "title": args.title}))


def list_tasks(args):
    """List tasks with optional filters."""
    conn = get_connection()
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if args.status:
        query += " AND status = ?"
        params.append(args.status)
    else:
        query += " AND status != 'deleted'"

    if args.priority:
        query += " AND priority = ?"
        params.append(args.priority)

    if args.project:
        query += " AND project = ?"
        params.append(args.project)

    if args.due_this_week:
        today = datetime.now().strftime("%Y-%m-%d")
        week_end = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        query += " AND due_date BETWEEN ? AND ?"
        params.extend([today, week_end])

    if args.overdue:
        today = datetime.now().strftime("%Y-%m-%d")
        query += " AND due_date < ? AND status = 'pending'"
        params.append(today)

    # Sort: overdue first, then by due date, then by priority
    query += """
        ORDER BY
            CASE WHEN due_date < date('now') AND status = 'pending' THEN 0 ELSE 1 END,
            CASE WHEN due_date IS NULL THEN 1 ELSE 0 END,
            due_date,
            CASE priority WHEN 'high' THEN 0 WHEN 'medium' THEN 1 WHEN 'low' THEN 2 ELSE 3 END
    """

    rows = conn.execute(query, params).fetchall()
    conn.close()

    tasks = [dict(row) for row in rows]
    print(json.dumps({"tasks": tasks, "count": len(tasks)}, indent=2))


def complete_task(args):
    """Mark a task as completed."""
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute(
        "UPDATE tasks SET status = 'completed', completed_at = ? WHERE id = ?",
        (now, args.id)
    )
    conn.commit()

    task = conn.execute("SELECT title FROM tasks WHERE id = ?", (args.id,)).fetchone()
    conn.close()

    title = task["title"] if task else "(unknown)"
    print(json.dumps({"status": "completed", "id": args.id, "title": title}))


def update_task(args):
    """Update task fields."""
    conn = get_connection()
    updates = []
    params = []

    if args.title:
        updates.append("title = ?")
        params.append(args.title)
    if args.priority:
        updates.append("priority = ?")
        params.append(args.priority)
    if args.due:
        updates.append("due_date = ?")
        params.append(args.due)
    if args.project:
        updates.append("project = ?")
        params.append(args.project)
    if args.description:
        updates.append("description = ?")
        params.append(args.description)

    if not updates:
        print(json.dumps({"error": "No fields to update"}))
        return

    params.append(args.id)
    # SAFETY: updates list contains only hardcoded "column = ?" strings from the
    # if-blocks above. Never derive column names from user input. (CWE-89)
    conn.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", params)
    conn.commit()
    conn.close()
    print(json.dumps({"status": "updated", "id": args.id, "fields": len(updates)}))


def delete_task(args):
    """Soft-delete a task."""
    conn = get_connection()
    conn.execute("UPDATE tasks SET status = 'deleted' WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(json.dumps({"status": "deleted", "id": args.id}))


def task_stats(args):
    """Show task statistics."""
    conn = get_connection()
    stats = {
        "pending": conn.execute("SELECT COUNT(*) FROM tasks WHERE status='pending'").fetchone()[0],
        "completed": conn.execute("SELECT COUNT(*) FROM tasks WHERE status='completed'").fetchone()[0],
        "overdue": conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status='pending' AND due_date < date('now')"
        ).fetchone()[0],
        "due_this_week": conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status='pending' AND due_date BETWEEN date('now') AND date('now', '+7 days')"
        ).fetchone()[0],
    }
    conn.close()
    print(json.dumps(stats, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Task database manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add
    add_p = subparsers.add_parser("add")
    add_p.add_argument("--title", required=True)
    add_p.add_argument("--description")
    add_p.add_argument("--priority", choices=["high", "medium", "low"])
    add_p.add_argument("--due")
    add_p.add_argument("--project")
    add_p.add_argument("--tags")

    # List
    list_p = subparsers.add_parser("list")
    list_p.add_argument("--status")
    list_p.add_argument("--priority")
    list_p.add_argument("--project")
    list_p.add_argument("--due-this-week", action="store_true")
    list_p.add_argument("--overdue", action="store_true")

    # Complete
    comp_p = subparsers.add_parser("complete")
    comp_p.add_argument("--id", type=int, required=True)

    # Update
    upd_p = subparsers.add_parser("update")
    upd_p.add_argument("--id", type=int, required=True)
    upd_p.add_argument("--title")
    upd_p.add_argument("--description")
    upd_p.add_argument("--priority", choices=["high", "medium", "low"])
    upd_p.add_argument("--due")
    upd_p.add_argument("--project")

    # Delete
    del_p = subparsers.add_parser("delete")
    del_p.add_argument("--id", type=int, required=True)

    # Stats
    subparsers.add_parser("stats")

    args = parser.parse_args()

    commands = {
        "add": add_task,
        "list": list_tasks,
        "complete": complete_task,
        "update": update_task,
        "delete": delete_task,
        "stats": task_stats,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
