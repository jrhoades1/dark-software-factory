# Memory Protocol

Rules for how memory is managed across sessions.

## At Session Start
1. Read `memory/MEMORY.md` for curated facts and preferences
2. Read today's log: `memory/logs/YYYY-MM-DD.md` (create if missing)
3. Read yesterday's log for continuity (if exists)

## During Session
- Append notable events, decisions, and completed tasks to today's log
- If the user states a preference or important fact, update MEMORY.md
- Keep MEMORY.md under ~200 lines — move detailed notes to daily logs

## Creating Daily Logs
If today's log doesn't exist, create it with this format:

```
# Daily Log: YYYY-MM-DD

> Session log for [Day, Month DD, YYYY]

---

## Events & Notes

```

## What Goes Where
- **MEMORY.md** — Stable facts: preferences, business details, goals, learned behaviors
- **Daily logs** — Session-specific: what happened today, decisions made, tasks completed
- **Don't duplicate** — If it's in MEMORY.md, don't repeat it in the log

## Tier 3: mem0 Vector Memory (When Installed)

If `.claude/skills/memory/` exists with scripts:
- **Auto-capture is active** — the Stop hook handles memory extraction. Do not duplicate manually.
- **Search before deciding** — Run `smart_search.py` before repeating past work or making architectural decisions.
- **Use the memory skill** for manual operations (add, search, sync, list, delete).
- **MEMORY.md is synced from mem0** — run `mem0_sync_md.py` to regenerate it. Do not manually edit MEMORY.md if Tier 3 is active.
