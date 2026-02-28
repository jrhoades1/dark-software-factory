# Handoff Template

Standard format for passing context between skills, agents, or workflow stages.
Copy the template below into a new file when one skill's output feeds another's input.

## When to Use

- One skill's output is another skill's required context
- A workflow pauses for human review and must resume later
- An agent hands control to a subagent or a different skill

## Template

```markdown
---
handoff_id: [from-skill]-to-[to-skill]-[YYYY-MM-DD]
from: [originating skill or agent]
to: [receiving skill or agent]
status: ready | conditional | blocked
---

### Summary

[2-3 sentences. What was accomplished and what comes next.]

### Context Items

| Type | Item | Detail |
|------|------|--------|
| constraint | [name] | [hard boundary — must not be violated] |
| decision | [name] | [choice already made — do not revisit] |
| warning | [name] | [risk the receiver must handle] |

### Artifacts

| File | Description | Path |
|------|-------------|------|
| [filename] | [what it contains] | [relative path] |

### Open Items

- [ ] [Thing the receiving skill or human must resolve before proceeding]

### Inherited Constraints

[Any hard constraints from earlier in the workflow that remain binding.]
```

## Field Reference

| Field | Values | Meaning |
|-------|--------|---------|
| status | `ready` | Receiving skill may proceed immediately |
| status | `conditional` | Proceed only after resolving Open Items |
| status | `blocked` | Do not proceed — requires human decision |
| type | `constraint` | Hard boundary that must not be violated |
| type | `decision` | Architectural or process choice already made |
| type | `warning` | Risk or edge case the receiver must handle |

## File Naming

Handoff files are session-scoped scratch:

```
.tmp/handoffs/[from-skill]-to-[to-skill]-[YYYY-MM-DD].md
```
