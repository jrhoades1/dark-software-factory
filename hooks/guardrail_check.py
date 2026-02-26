#!/usr/bin/env python3
"""
Hook: Guardrail Check (PreToolUse Hook)
Purpose: Block dangerous commands before they execute.
Trigger: Runs before every Bash tool use.

Exit code 0 = allow the command
Exit code 2 = block the command (with reason on stdout)
"""

import json
import sys

# Commands that should ALWAYS be blocked
BLOCKED_PATTERNS = [
    "rm -rf /",
    "rm -rf ~",
    "rm -rf .",
    "git push --force",
    "git push -f",
    "git reset --hard",
    "DROP TABLE",
    "DROP DATABASE",
    "DELETE FROM",         # Without WHERE clause protection
    "--no-verify",         # Never skip git hooks
]

# Files that should never be deleted or overwritten
PROTECTED_FILES = [
    ".env",
    "credentials.json",
    "token.json",
    "CLAUDE.md",
    "memory/MEMORY.md",
    "billing.json",
    ".claude/project-code.txt",
]

# Patterns that need explicit confirmation (not blocked, but flagged)
CAUTION_PATTERNS = [
    "git push",
    "npm publish",
    "deploy",
    "send",
    "post_to_slack",
]


def check_command(command: str) -> dict:
    """Check a command against guardrails. Returns {allow: bool, reason: str}."""
    cmd_lower = command.lower().strip()

    # Check blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if pattern.lower() in cmd_lower:
            return {
                "allow": False,
                "reason": f"BLOCKED: Command contains dangerous pattern '{pattern}'. "
                         f"This is blocked by guardrail rules. If you need to do this, "
                         f"ask the user for explicit confirmation first."
            }

    # Check protected files for deletion
    for protected in PROTECTED_FILES:
        if protected in command and ("rm " in cmd_lower or "delete" in cmd_lower):
            return {
                "allow": False,
                "reason": f"BLOCKED: Cannot delete protected file '{protected}'. "
                         f"This file is critical to the system."
            }

    # Allow the command
    return {"allow": True, "reason": ""}


def main():
    """Read hook input from stdin, check the command, exit appropriately."""
    try:
        hook_input = sys.stdin.read()
        if not hook_input:
            sys.exit(0)  # No input = allow

        data = json.loads(hook_input)
        tool_input = data.get("tool_input", {})

        # Extract the command being run
        command = tool_input.get("command", "")
        if not command:
            sys.exit(0)  # No command = allow

        result = check_command(command)

        if not result["allow"]:
            # Exit code 2 = block the tool use
            # Print the reason so Claude sees it
            print(result["reason"])
            sys.exit(2)

        # Exit code 0 = allow
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)  # Can't parse = allow (don't break things)
    except Exception:
        sys.exit(0)  # Any error = allow (hooks shouldn't block on errors)


if __name__ == "__main__":
    main()
