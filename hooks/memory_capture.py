#!/usr/bin/env python3
"""
Hook: Memory Auto-Capture (Stop Hook)
Purpose: Automatically ensure daily log exists and capture session markers.
Trigger: Runs async after every Claude response via the Stop hook.

This is the BASIC version (Tier 1+2 memory — no API keys required).
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Resolve project root (hooks/ is at project root level)
PROJECT_ROOT = Path(__file__).parent.parent
MEMORY_DIR = PROJECT_ROOT / "memory"
LOGS_DIR = MEMORY_DIR / "logs"
MEMORY_MD = MEMORY_DIR / "MEMORY.md"


def get_today_log_path():
    """Get path to today's daily log file."""
    today = datetime.now().strftime("%Y-%m-%d")
    return LOGS_DIR / f"{today}.md"


def ensure_today_log():
    """Create today's log file if it doesn't exist."""
    log_path = get_today_log_path()
    if not log_path.exists():
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        today = datetime.now()
        log_path.write_text(
            f"# Daily Log: {today.strftime('%Y-%m-%d')}\n\n"
            f"> Session log for {today.strftime('%A, %B %d, %Y')}\n\n"
            f"---\n\n"
            f"## Events & Notes\n\n"
        )
    return log_path


def append_to_log(content: str):
    """Append a timestamped entry to today's log."""
    log_path = ensure_today_log()
    timestamp = datetime.now().strftime("%H:%M")
    with open(log_path, "a") as f:
        f.write(f"- [{timestamp}] {content}\n")


def main():
    """
    Basic memory capture hook.

    In the basic version, this ensures the daily log exists and is ready.
    The advanced version (mem0) reads the transcript, extracts facts,
    and stores them as vectors in Pinecone.
    """
    try:
        # Ensure today's log exists
        ensure_today_log()

        # Read hook input from stdin (Claude Code passes context)
        hook_input = sys.stdin.read() if not sys.stdin.isatty() else ""

        if hook_input:
            try:
                data = json.loads(hook_input)
                # Log session activity marker
                append_to_log("Session activity captured")
            except json.JSONDecodeError:
                pass

    except Exception as e:
        # Hooks should never crash Claude — fail silently
        pass


if __name__ == "__main__":
    main()
