# Gate Schemas

Reference for gate review documents and checklists used by the compliance-gate skill.

## Gate Review Document Template

```markdown
---
gate_id: [gate-type]-[YYYY-MM-DD]
gate_type: [security | hipaa | pre-deployment | custom]
project: [project name]
project_path: [path]
date: [YYYY-MM-DD]
prior_skills: [list of skills that ran before this gate]
verdict: [pass | conditional | rejected]
---

# Gate Review: [gate_type] — [project name]

## Automated Check Results

| Check | Result | Blocking | Detail |
|-------|--------|----------|--------|
| [id] | [pass/fail/N-A] | [yes/no] | [detail] |

## Manual Review Items

| Item | Result | Notes |
|------|--------|-------|
| [checklist item] | [pass/fail/N-A] | [notes] |

## Verdict: [PASS / CONDITIONAL / REJECTED]

**Justification:** [1-2 sentences explaining the verdict]

### Conditional Items (if applicable)

| Item | Owner | Remediation | Deadline |
|------|-------|-------------|----------|
| [description] | [who fixes it] | [what to do] | [when] |

### Blocking Issues (if rejected)

- [Issue 1 — what must change before re-review]
- [Issue 2]
```

---

## Gate Type Checklists

### Security Gate

| # | Item | Automated | Blocking |
|---|------|-----------|----------|
| 1 | .env in .gitignore | Yes | Yes |
| 2 | .env not in git history | Yes | Yes |
| 3 | No hardcoded secrets in source | Yes | Yes |
| 4 | Dependency lockfile present | Yes | No |
| 5 | Authentication uses secure tokens | Manual | Yes |
| 6 | API endpoints require authorization | Manual | Yes |
| 7 | Error responses don't leak internals | Manual | No |
| 8 | Input validation on all user-facing endpoints | Manual | Yes |
| 9 | No SQL injection vectors (parameterized queries) | Manual | Yes |
| 10 | CORS configured restrictively | Manual | No |

### HIPAA Gate

Includes all Security Gate items, plus:

| # | Item | Automated | Blocking |
|---|------|-----------|----------|
| 11 | PHI boundary directory exists | Yes | Yes |
| 12 | Audit log table in schema | Yes | Yes |
| 13 | BAA documentation present | Yes | Yes |
| 14 | PHI encrypted at rest | Manual | Yes |
| 15 | PHI encrypted in transit (TLS) | Manual | Yes |
| 16 | No PHI in application logs | Manual | Yes |
| 17 | Access controls enforce least privilege | Manual | Yes |
| 18 | Data retention policy documented | Manual | No |

### Pre-Deployment Gate

Includes all Security Gate items, plus:

| # | Item | Automated | Blocking |
|---|------|-----------|----------|
| 11 | README exists | Yes | No |
| 12 | Test directory exists | Yes | No |
| 13 | No TODO/FIXME/HACK in source | Yes | No (advisory) |
| 14 | CI/CD pipeline configured | Manual | No |
| 15 | Monitoring/alerting set up | Manual | No |
| 16 | Environment variables documented | Manual | No |
| 17 | Database migrations are reversible | Manual | No |

### Custom Gate

Baseline only (items 1-4 from Security Gate). Add custom items as needed
and document them in the gate review.

---

## Hard-Fail Conditions (Auto-Rejected)

These findings force a `rejected` verdict regardless of other results:

- Secrets found in source code or git history
- .env tracked in git
- No encryption for data classified as PHI (hipaa gate only)
- BAA missing for any project handling PHI (hipaa gate only)

## Verdict Decision Matrix

| Hard failures | Remediable failures | Advisory only | Verdict |
|---------------|--------------------:|---------------|---------|
| 0 | 0 | any | **pass** |
| 0 | ≥1 | any | **conditional** |
| ≥1 | any | any | **rejected** |
