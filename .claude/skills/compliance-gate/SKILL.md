---
name: compliance-gate
description: >
  Run a compliance gate review at any checkpoint in a workflow. Produces a
  structured pass/conditional/rejected verdict with an audit document. Use when
  the user says "compliance gate," "gate review," "pre-deployment check,"
  "enforce gate," "quality gate," "checkpoint," or when citadel-workflow reaches
  the Enforce step. Also trigger when security-hardening or hipaa-scaffold
  completes and a formal gate record is needed. Pairs with citadel-workflow,
  security-hardening, and hipaa-scaffold.
model: sonnet
context: fork
user-invokable: true
allowed-tools: Bash(python3 .claude/skills/compliance-gate/scripts/*)
---

# Compliance Gate

Formal checkpoint that produces a written verdict — pass, conditional, or rejected —
before a workflow proceeds. The gate review document is the audit artifact.

## Intent

1. **Gates are decision points, not rubber stamps** — every gate produces a written record that someone signed off on or explicitly accepted risk
2. **Automated checks surface facts; human judgment closes the gate** — the script finds missing files and failing patterns; Jimmy decides whether to proceed
3. **Three outcomes only: pass, conditional, or rejected** — conditional means "proceed with listed remediations"; rejected means full stop
4. **Gate scope is declared upfront** — the invoker specifies the gate type (security, hipaa, pre-deployment, custom) and the skill applies the right checklist
5. **Conditional gates are time-bounded** — every conditional item must have an owner and a remediation action, or the gate defaults to rejected
6. **Gates compose** — a workflow can have multiple gates; each produces its own document; the final gate references all prior gates
7. **The gate document persists** — written to `.tmp/gates/` for the session; handed off via the handoff template if the workflow continues to another skill

## Workflow

### Step 1 — Declare Gate Scope

Ask Jimmy (or read from context):
- **Gate type:** `security` | `hipaa` | `pre-deployment` | `custom`
- **Project path:** the root of the project being reviewed
- **Prior skills:** what ran before this gate (e.g., security-hardening, hipaa-scaffold)

If gate type is unclear, default to `pre-deployment` and note it in the review document.

### Step 2 — Run Automated Checks

```bash
python3 .claude/skills/compliance-gate/scripts/gate_check.py \
  --gate-type [security|hipaa|pre-deployment|custom] \
  --project-path [path]
```

The script returns JSON with individual check results (pass/fail/not-applicable/unable-to-verify)
and a summary. Read the output carefully — these are objective facts, not verdicts.

### Step 3 — Review Checklist

Read `references/gate-schemas.md` for the relevant gate type checklist. Walk through each
item. For items the automated script already checked, use its result. For items requiring
judgment (architecture decisions, documentation quality, threat model coverage), evaluate
manually based on project files.

Mark each item: **pass** | **fail** | **N/A**

### Step 4 — Determine Verdict

| Condition | Verdict |
|-----------|---------|
| All items pass or N/A | `pass` |
| Failures exist but are remediable before proceeding | `conditional` |
| Any hard-fail condition (see gate-schemas.md) | `rejected` |

Hard-fail conditions that force `rejected`:
- Secrets found in source code or git history
- .env tracked in git
- No encryption for data classified as PHI (hipaa gate only)
- BAA missing (hipaa gate only)

### Step 5 — Produce Gate Review Document

Write the gate review document to:
```
.tmp/gates/[gate-type]-[YYYY-MM-DD].md
```

Use the template from `references/gate-schemas.md`. Include:
- Gate metadata (type, project, date, prior skills)
- Every check item with its result
- Verdict with justification
- For `conditional`: each remediation item with owner and action
- For `rejected`: what must change before re-review

### Step 6 — Handoff (if applicable)

If the workflow continues to another skill after the gate:
- Use the handoff template from `global/references/handoff-template.md`
- Map gate verdict to handoff status: pass → `ready`, conditional → `conditional`, rejected → `blocked`
- Include the gate review document path in the Artifacts table

Present the verdict summary to Jimmy with the path to the full review document.

## Rules

- Never produce a `pass` verdict when the automated script returns hard failures
- Never skip the automated check step — Claude's judgment alone is not sufficient for gate closure
- Conditional items must include: description, owner, remediation action
- Never overwrite a prior gate document — each run creates a new timestamped file
- If gate type is `hipaa`, recommend pairing with `hipaa-scaffold` if it hasn't run yet
- If gate type is `security` or `pre-deployment`, recommend pairing with `security-hardening` if it hasn't run yet

## Edge Cases

- **Gate type unknown:** Default to `pre-deployment`, note in review document
- **Script can't access project path:** Record all file-access checks as `unable-to-verify`, escalate to Jimmy
- **Prior skill handoff missing:** Note the gap, ask Jimmy to confirm what the prior skill produced
- **No failures found:** Still produce the review document — a clean gate record has audit value
- **Re-review after conditional:** Create a new gate document referencing the prior one

## Related Skills

- `citadel-workflow` — calls this skill at the E (Enforce) step
- `security-hardening` — provides audit findings that feed gate review
- `hipaa-scaffold` — provides HIPAA compliance verification
- Handoff template: `global/references/handoff-template.md`
