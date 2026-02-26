---
name: session-start
description: Unified session startup protocol. Runs automatically at the start of every conversation. Reads memory, detects project type, gives a status briefing, and asks what to work on. Do NOT wait for the user to ask — run this immediately when a new conversation begins.
user-invokable: true
---

# Session Start

Unified entry point for every project. Same flow everywhere — adapts to context.

## Intent

1. **Every session starts the same way** — consistency reduces cognitive load; Jimmy shouldn't need to remember different startup procedures per project
2. **Context before action** — reading memory and logs before asking "what now?" prevents repeating past mistakes or duplicating work
3. **Project type drives behavior** — client projects surface billing and deadlines; internal projects skip the overhead
4. **One question, then go** — the briefing is fast, the question is simple: "What are we working on?"
5. **The log captures everything** — session start gets recorded so weekly reviews show exactly when work happened

## Process

### Step 1: Gather Context

Run the status script to collect project state:

```bash
python3 hooks/session_status.py
```

This returns JSON with:
- Project identity (from memory/MEMORY.md)
- Project type (client vs internal)
- Last session activity (from daily logs)
- Overdue tasks (if task DB exists)
- Open task count

### Step 2: Read Memory

Read these files (skip if missing):
1. `memory/MEMORY.md` — curated facts
2. `memory/logs/YYYY-MM-DD.md` — today's log (may not exist yet)
3. Yesterday's log — for continuity

### Step 3: Present Briefing

Format the status as a concise briefing:

```
## Good [morning/afternoon], Jimmy

**Project:** [name] ([client/internal])
**Last session:** [date — summary of what happened]
**Open tasks:** [count] ([overdue count] overdue)

[If client project: **Project code:** XXX-XXX]

What are we working on today?
```

Keep it tight — 4-6 lines max. Don't dump the full task list unless asked.

### Step 4: Log Session Start

Append to today's daily log:

```
- [HH:MM] Session started — [topic from user's response]
```

## Rules

- Run this at the **very start** of every new conversation
- Don't skip the briefing even if the user opens with a task — do briefing first, then address their request
- If memory/MEMORY.md doesn't exist, note it and still ask what to work on
- If the user says "skip" or jumps straight into a task, respect that — log the session start and go
- Time of day for greeting: before 12 = morning, 12-17 = afternoon, after 17 = evening
