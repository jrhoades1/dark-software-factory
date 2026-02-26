#!/usr/bin/env python3
"""
Hook: Output Validation (PostToolUse Hook)
Purpose: Auto-validate JSON output from skill scripts after execution.
Trigger: Runs after Bash tool use when configured.

Exit code 0 = validation passed (or not applicable)
Non-zero = validation failed (prints feedback)
"""

import json
import sys


def validate_json_output(output: str) -> dict:
    """Check if script output is valid JSON with expected structure."""
    if not output.strip():
        return {"valid": True, "reason": "Empty output (may be intentional)"}

    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "reason": f"Script output is not valid JSON: {str(e)}"
        }

    # Check for error indicators
    if isinstance(data, dict):
        if data.get("success") is False:
            error = data.get("error", "Unknown error")
            return {
                "valid": False,
                "reason": f"Script reported failure: {error}"
            }

    return {"valid": True, "reason": "Valid JSON output"}


def main():
    """Read hook input, validate the tool output."""
    try:
        hook_input = sys.stdin.read()
        if not hook_input:
            sys.exit(0)

        data = json.loads(hook_input)
        tool_output = data.get("tool_output", "")

        # Only validate if the output looks like it should be JSON
        # (starts with { or [)
        stripped = tool_output.strip()
        if stripped and (stripped.startswith("{") or stripped.startswith("[")):
            result = validate_json_output(stripped)
            if not result["valid"]:
                print(f"Output validation warning: {result['reason']}")
                # Don't block (exit 0) — just inform
                sys.exit(0)

        sys.exit(0)

    except Exception:
        sys.exit(0)  # Never block on validation errors


if __name__ == "__main__":
    main()
