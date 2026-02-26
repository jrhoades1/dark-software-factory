# Session Start Protocol

At the **very start** of every new conversation, before doing anything else:

1. Run `python3 hooks/session_status.py` to gather project state
2. Read `memory/MEMORY.md` for curated facts
3. Read today's daily log if it exists: `memory/logs/YYYY-MM-DD.md`
4. Read yesterday's log for continuity (if it exists)
5. Present a brief status to Jimmy (4-6 lines max):

```
## Good [morning/afternoon/evening], Jimmy

**Project:** [name] ([client/internal])
**Last session:** [date — what happened]
**Open tasks:** [count] ([overdue] overdue)  ← only if tasks exist

What are we working on today?
```

6. After Jimmy responds, log the session start to today's daily log

**If the user opens with a direct task or question:** Still run the briefing first (keep it to 2-3 lines), then immediately address their request. Don't make them wait.

**If memory/MEMORY.md doesn't exist:** Skip the briefing, note that memory isn't set up, and proceed normally.
