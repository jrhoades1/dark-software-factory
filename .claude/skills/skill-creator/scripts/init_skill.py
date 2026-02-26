#!/usr/bin/env python3
"""Scaffold a new skill directory with standard structure and SKILL.md template."""

import argparse
import json
import os
import sys
import re


SKILL_MD_TEMPLATE = """---
name: {name}
description: TODO — What this skill does in plain language. Use when user says "trigger 1", "trigger 2", or asks to do X.
model: sonnet
context: fork
allowed-tools: Bash(python3 .claude/skills/{name}/scripts/*)
user-invokable: true
---

# {title}

## Objective

TODO — One sentence: what this skill achieves.

## Inputs Required

- TODO — List inputs, credentials, config

## Execution Steps

### Step 1: TODO

```bash
python3 .claude/skills/{name}/scripts/TODO.py --input VALUE
```

**Input**: TODO
**Output**: TODO (JSON)
**Dependencies**: TODO

## Process Flow

```
1. TODO → output
   ↓
2. TODO → output
   ↓
3. TODO → final result
```

## Edge Cases & Error Handling

### TODO — Scenario
- What goes wrong: TODO
- How to handle it: TODO

## Environment Variables Required

```bash
# TODO — list required env vars
API_KEY=your_key_here
```
"""

SCRIPT_TEMPLATE = """#!/usr/bin/env python3
\"""{description}\"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, help='Input file or value')
    parser.add_argument('--output', help='Output file path (default: stdout)')
    args = parser.parse_args()

    try:
        # TODO — implement
        result = {{"success": True, "data": {{}}}}

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Output saved to {{args.output}}")
        else:
            print(json.dumps(result, indent=2))

    except Exception as e:
        print(json.dumps({{"success": False, "error": str(e)}}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
"""


def validate_name(name: str) -> str:
    """Validate skill name: lowercase, numbers, hyphens only. Max 64 chars."""
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', name) and not re.match(r'^[a-z0-9]$', name):
        print(f"Error: Skill name must be lowercase letters, numbers, and hyphens only.", file=sys.stderr)
        print(f"  Got: '{name}'", file=sys.stderr)
        print(f"  Example: 'email-digest', 'build-website', 'research-lead'", file=sys.stderr)
        sys.exit(1)
    if len(name) > 64:
        print(f"Error: Skill name must be 64 characters or less. Got {len(name)}.", file=sys.stderr)
        sys.exit(1)
    return name


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 init_skill.py email-digest
  python3 init_skill.py email-digest --path /custom/location
  python3 init_skill.py data-pipeline --no-scripts
        """
    )
    parser.add_argument('name', help='Skill name in kebab-case (e.g., email-digest)')
    parser.add_argument('--path', default='.claude/skills',
                        help='Parent directory for the skill (default: .claude/skills)')
    parser.add_argument('--no-scripts', action='store_true',
                        help='Skip creating scripts/ directory (for instruction-only skills)')
    args = parser.parse_args()

    name = validate_name(args.name)
    title = name.replace('-', ' ').title()
    skill_dir = os.path.join(args.path, name)

    if os.path.exists(skill_dir):
        print(f"Error: Directory already exists: {skill_dir}", file=sys.stderr)
        print(f"  To update an existing skill, edit it directly.", file=sys.stderr)
        sys.exit(1)

    # Create directory structure
    os.makedirs(os.path.join(skill_dir, 'references'), exist_ok=True)
    if not args.no_scripts:
        os.makedirs(os.path.join(skill_dir, 'scripts'), exist_ok=True)
        os.makedirs(os.path.join(skill_dir, 'assets'), exist_ok=True)

    # Write SKILL.md
    skill_md = SKILL_MD_TEMPLATE.format(name=name, title=title)
    with open(os.path.join(skill_dir, 'SKILL.md'), 'w') as f:
        f.write(skill_md.lstrip('\n'))

    # Write example script
    if not args.no_scripts:
        script_content = SCRIPT_TEMPLATE.format(
            description=f"TODO — Implement the main logic for {title}."
        )
        script_path = os.path.join(skill_dir, 'scripts', f'{name.replace("-", "_")}.py')
        with open(script_path, 'w') as f:
            f.write(script_content.lstrip('\n'))
        os.chmod(script_path, 0o755)

    # Summary
    print(json.dumps({
        "success": True,
        "skill_name": name,
        "path": skill_dir,
        "created": {
            "SKILL.md": f"{skill_dir}/SKILL.md",
            "scripts/": f"{skill_dir}/scripts/" if not args.no_scripts else None,
            "references/": f"{skill_dir}/references/",
            "assets/": f"{skill_dir}/assets/" if not args.no_scripts else None,
        },
        "next_steps": [
            "Edit SKILL.md — replace all TODO placeholders",
            "Write description with trigger words in frontmatter",
            "Implement scripts in scripts/ directory",
            "Test in a fresh session with natural language"
        ]
    }, indent=2))


if __name__ == '__main__':
    main()
