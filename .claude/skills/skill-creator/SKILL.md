---
name: skill-creator
description: Create or update a skill that packages a workflow into a self-contained SKILL.md with scripts, references, and assets. Use when user says "create a skill", "make a new skill", "crystallize this workflow", "turn this into a skill", or asks to build a reusable process.
user-invokable: true
---

# Skill Creator

Create self-contained skills that package workflows into portable, discoverable units.

## Intent

1. **Skills encode operational knowledge, not instructions** — a skill exists because someone did the work, hit the edge cases, and documented what actually works; don't create skills from theory
2. **One script, one job** — deterministic code handles the HOW; Claude handles the WHAT; mixing them makes both unreliable
3. **Descriptions are discovery** — a poorly written description means the skill never triggers; trigger phrases are as important as the workflow itself
4. **Under 500 lines or split it** — a SKILL.md that exceeds 500 lines is burning context on detail that should live in `references/`
5. **Test with natural language, not slash commands** — if the skill only triggers when someone types `/skill-name`, the description is too vague
6. **Shared knowledge belongs in context/, not references/** — if two skills would reference the same doc, it's context, not a skill-specific reference

## Creation Process

### Step 1: Understand the Workflow

Ask the user to describe the workflow. Identify:

- What triggers this workflow (user request, event, schedule)
- What inputs it needs (URLs, files, API keys, config)
- What steps it follows (in order, with dependencies)
- What outputs it produces (files, API calls, messages, data)
- What can go wrong (rate limits, auth failures, missing data)

If the workflow was just completed manually, reverse-engineer it: "Let me crystallize exactly what we just did into a reusable skill."

### Step 2: Plan the Skill Contents

For each step, decide the execution method:

| Question | Maps To |
|----------|---------|
| Needs deterministic code? | `scripts/` — Python script |
| Needs an external service? | MCP tool — reference by name in the step |
| Needs Claude's judgment? | Instructions only — no script, no tool |
| Needs reference docs? | `references/` — Markdown file |
| Needs templates or assets? | `assets/` — Files consumed by scripts |
| Shared business knowledge? | `context/` (project root, NOT in the skill) |

**Rules:**
- Every script has ONE job. If it does multiple things, split it.
- If 2+ skills would reference it, it goes in `context/` not `references/`.
- Default to Python for deterministic work. MCP adds token overhead.

### Step 3: Scaffold the Skill

Run the init script:

```bash
python3 .claude/skills/skill-creator/scripts/init_skill.py SKILL_NAME
```

This creates the directory structure with placeholders. Then populate.

### Step 4: Write the Frontmatter

```yaml
---
name: kebab-case-name
description: What it does. Use when user says "trigger 1", "trigger 2", or asks to do X.
model: sonnet
context: fork
allowed-tools: Bash(python3 .claude/skills/SKILL_NAME/scripts/*)
user-invokable: true
---
```

**Frontmatter decisions:**

| Field | When to Use |
|-------|-------------|
| `model: sonnet` | Most automated pipelines (default) |
| `model: opus` | Complex reasoning, creative work |
| `model: haiku` | Simple tasks, fast lookups |
| `context: fork` | Skill runs as isolated subagent (recommended for pipelines) |
| `allowed-tools` | Restrict to scripts and/or MCP tools |
| `user-invokable: true` | Can be triggered via /name slash command |
| `disable-model-invocation: true` | Manual-only (for destructive operations) |

### Step 5: Write the SKILL.md Body

Use imperative SOP format:

```markdown
# Skill Title

## Objective
One sentence: what this skill achieves.

## Inputs Required
- List all inputs, credentials, config needed

## Execution Steps

### Step 1: Name of Step
\`\`\`bash
python3 .claude/skills/SKILL_NAME/scripts/script_name.py --flag value
\`\`\`
**Input**: What the script takes
**Output**: What the script produces (JSON structure)

## Edge Cases & Error Handling
### Scenario Name
- What goes wrong
- How to handle it
```

**Body rules:**
- Under 500 lines. Move detailed docs to `references/`.
- Every script command includes full path from project root.
- Include expected output JSON structures for each script.

### Step 6: Implement Scripts

Write Python scripts in `scripts/`. Each script:

- Has ONE job
- Accepts input via CLI args
- Returns JSON to stdout on success
- Returns JSON error to stderr on failure
- Handles its own errors

### Step 7: Test the Skill

Three tests:

1. **Trigger test:** Fresh session. Ask naturally without naming the skill. Does Claude find it?
2. **Functional test:** Run 4-5 times with different inputs. Consistent output?
3. **Value test:** Compare output WITH vs WITHOUT the skill. Measurable improvement?

### Step 8: Iterate

After real usage, refine:
- Tighten instructions where Claude improvised incorrectly
- Add edge cases discovered in production
- Move sections to `references/` if SKILL.md exceeds 500 lines

## Skill Anatomy

```
.claude/skills/skill-name/
├── SKILL.md              # Process definition (<500 lines)
├── scripts/              # Python scripts (one job each)
├── references/           # Skill-specific docs
└── assets/               # Templates, fonts, icons
```

**What does NOT go in the skill:**
- Business knowledge used by multiple skills → `context/`
- Runtime behavior settings → `args/`
- Persistent data → `data/`
- Temporary files → `.tmp/`

## Design Patterns

- **Sequential** — Steps in strict order with dependencies
- **Iterative refinement** — Generate → validate → fix → repeat
- **Multi-MCP coordination** — Cross-service workflows
- **Context-aware branching** — Different paths based on input type
- **Domain-specific** — Embedded business rules and compliance
