# Requirements Template

Copy this file to your project's `requirements/` directory when creating a new requirement.
Rename to `REQ-NNN-short-slug.md`.

---

```markdown
---
id: REQ-NNN
title: Short descriptive title
status: proposed
priority: medium
author: jimmy
requested_by: client
created: YYYY-MM-DD
approved: null
scheduled: null
implemented: null
verified: null
decision: null
tags: []
---

## Problem
What problem does this solve? One paragraph max.

## Solution
How should it be solved? Describe the approach, not the implementation details.

## Acceptance Criteria
- [ ] Criterion 1 — specific, testable
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes
- Implementation hints, relevant files, dependencies
- Existing code to reuse
- Constraints or gotchas

## Decision Log
<!-- Append entries as status changes, e.g.: -->
<!-- 2026-02-22 — proposed by claude: noticed gap in reporting tools -->
<!-- 2026-02-23 — approved by jimmy: fits within retainer scope -->
```

---

## Frontmatter Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | `REQ-NNN` — sequential, never reused |
| `title` | string | yes | Short human-readable title |
| `status` | string | yes | `proposed`, `approved`, `rejected`, `deferred`, `scheduled`, `in_progress`, `implemented`, `verified` |
| `priority` | string | yes | `critical`, `high`, `medium`, `low` |
| `author` | string | yes | Who created this: `jimmy`, `claude`, or a name |
| `requested_by` | string | yes | Who wants this: `client`, `jimmy`, `claude`, or a name |
| `created` | date | yes | When the requirement was created |
| `approved` | date/null | no | When approved for implementation |
| `scheduled` | date/null | no | When assigned to a sprint/week |
| `implemented` | date/null | no | When code was complete |
| `verified` | date/null | no | When end-user confirmed it works |
| `decision` | string/null | no | Reason for approval/rejection/deferral |
| `tags` | list | no | Freeform tags for filtering |

## Status Workflow

```
proposed → approved → scheduled → in_progress → implemented → verified
         → rejected
         → deferred
```

## Workflow Rules

- Only Jimmy can approve, reject, or verify requirements
- Claude can create proposed requirements, start scheduled work, and mark work as implemented
- Nothing moves from `proposed` to `approved` without Jimmy's sign-off
- Claude should NOT implement anything that isn't `approved` or `scheduled`

## Cross-project Reports

```bash
python C:\Users\Tracy\Projects\claude-tracking\req_report.py
python C:\Users\Tracy\Projects\claude-tracking\req_report.py --project ALD-SERVICETITAN
python C:\Users\Tracy\Projects\claude-tracking\req_report.py --status proposed --detail
```
