---
name: mvp-gate
description: >
  Pre-demo readiness gate for MVP milestones. Run this before showing any build to a client,
  stakeholder, or end user. Produces a structured readiness report and demo script. Trigger
  when the user says "is this ready to show," "MVP checklist," "demo prep," "client review,"
  "ready to present," "pre-demo check," "what's left before we show this," or "ship check."
  Sits between Drill and Enforce in the CITADEL workflow — Enforce is for production security;
  this is for "can we show it without embarrassment." Pairs with e2e-testing for automated
  verification and compliance-gate for formal audits.
model: sonnet
user-invokable: true
---

# MVP Gate

## Intent

1. **An MVP demo is a promise** — showing something to a client creates expectations. Make sure every expectation is met or explicitly scoped out before the meeting.
2. **Three verdicts: ready, conditional, not ready** — conditional means "showable with caveats"; not ready means stop and fix.
3. **Automated checks first, judgment second** — run the tests, then evaluate what the numbers mean.
4. **Known limitations are strengths, not weaknesses** — documenting what the MVP does NOT do is more professional than hoping nobody notices.
5. **The demo script is a deliverable** — never demo without a script. Improvised demos find every bug.
6. **The gate document persists** — written to the project for future reference.

## When to Use

- Before any client demo, stakeholder review, or user testing session
- At MVP milestone before moving to next phase
- When transitioning from "building" to "showing"
- Before recording a demo video or screenshot walkthrough
- Any time the user asks "is this ready?"

## Process

### Step 1: Run Automated Verification

Run the E2E test suite. If no tests exist, flag this as a blocker.

```bash
cd <app-directory> && npm test
```

Record: total tests, passed, failed, skipped.

**Verdict rules:**
- All tests pass -> proceed
- Any test fails -> fix or document as known limitation
- No tests exist -> not ready (set up e2e-testing skill first)

### Step 2: Functional Checklist

Walk through each item. Mark: pass / fail / N/A / known limitation.

#### Core Functionality
```
[ ] App loads without errors (no blank screens, no console errors)
[ ] Primary user flow works end-to-end (the main thing the app does)
[ ] All navigation paths work (no dead-end pages, no broken links)
[ ] Data persists correctly (save, reload, data still there)
[ ] All interactive elements respond (buttons, inputs, dropdowns, sliders)
[ ] Error states are handled gracefully (not raw error messages or blank screens)
```

#### UI / Presentation
```
[ ] Looks professional on the target device (desktop, mobile, or both)
[ ] No placeholder text visible ("Lorem ipsum", "TODO", "test")
[ ] No debug UI visible (console logs, dev toolbars, test buttons)
[ ] Brand elements correct (colors, logo, name, copy)
[ ] Typography is readable (no text overflow, no tiny fonts)
[ ] Loading states exist (no frozen screens while data loads)
```

#### Data & Content
```
[ ] Test/seed data is realistic (not "asdf" or "test123")
[ ] No dummy API keys or placeholder credentials visible in UI
[ ] Content matches what the client expects to see
[ ] Empty states are handled (what does a new user see?)
```

#### Security Basics (MVP level, not full Enforce)
```
[ ] No secrets in source code or visible in browser
[ ] API keys stored in .env, not hardcoded
[ ] .env is in .gitignore
[ ] No sensitive data in console logs
[ ] HTTPS works (if deployed)
```

### Step 3: Identify Known Limitations

Document everything the MVP does NOT do. Be specific and honest.

Format each limitation as:
```
- [LIMITATION]: What it is
  - Impact: What the user will notice
  - Workaround: How to handle it during demo (if any)
  - Timeline: When it will be addressed (next sprint, phase 2, etc.)
```

Common MVP limitations to check:
- No authentication / single user only
- No error recovery (must refresh on failure)
- No mobile responsiveness
- Hardcoded data or configuration
- No email/notification system
- No export/download functionality
- Performance not optimized
- No accessibility features

### Step 4: Write Demo Script

Create a step-by-step demo script that:

1. **Opens with context** — 1-2 sentences on what we're showing and why
2. **Follows the happy path** — walk through the primary user flow
3. **Highlights key features** — pause at moments that demonstrate value
4. **Avoids known issues** — route around limitations, don't trigger them
5. **Ends with a clear next step** — what happens after this demo

Format:
```
## Demo Script: [Project Name] MVP

### Setup (before the call)
- [ ] Clear test data / seed fresh data
- [ ] Open app in [browser] at [URL]
- [ ] Close dev tools
- [ ] Check internet connection

### Opening (30 seconds)
"[Context sentence. What we built and what it does.]"

### Walkthrough (3-5 minutes)
1. [Step]: [What to click/show] -> [What they'll see] -> [What to say]
2. [Step]: ...
3. [Step]: ...

### Key Moments to Highlight
- [Feature]: [Why it matters to the client]
- [Feature]: [Why it matters to the client]

### Questions to Expect
- Q: [Likely question] -> A: [Prepared answer]
- Q: [Likely question] -> A: [Prepared answer]

### Closing
"[Next steps. What we're building next. When they'll see it.]"

### DO NOT
- [Thing to avoid during demo]
- [Thing to avoid during demo]
```

### Step 5: Determine Verdict

| Condition | Verdict |
|-----------|---------|
| All functional checks pass, E2E tests pass, demo script ready | **Ready** |
| Minor issues exist but are documented as known limitations | **Conditional** |
| Core flow broken, E2E tests failing, or security basics violated | **Not Ready** |

### Step 6: Produce Gate Report

Write the report to the project:
```
<project-root>/docs/mvp-gate-[YYYY-MM-DD].md
```

Include:
- Verdict with justification
- E2E test results summary
- Functional checklist results
- Known limitations list
- Demo script
- Recommended next actions

Present the verdict to the user with a clear recommendation.

## Rules

- Never declare "ready" when E2E tests are failing
- Never skip the demo script — improvised demos always hit bugs
- Known limitations must be documented BEFORE the demo, not discovered during it
- Debug/dev UI must be hidden or removed before showing to a client
- Seed/test data must be realistic — "test123" in a client demo is unprofessional
- The gate report is a project artifact — don't delete it after the demo

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| `e2e-testing` | Provides the automated test results for Step 1 |
| `compliance-gate` | Formal security/compliance audit (heavier than MVP gate) |
| `citadel-workflow` | MVP gate sits between Drill (D) and Enforce (E) |
| `client-follow-up` | Use after the demo for thank-you and next steps |
| `project-bootstrap` | Should have set up the project structure this gate checks |

## CITADEL Integration

MVP Gate is an optional checkpoint between **Drill** and **Enforce**:

```
C -> I -> T -> A -> D -> [MVP Gate] -> E -> L
                         ^^^^^^^^^^^
                         Show client
                         Get feedback
                         Iterate in A/D
                         Then Enforce for production
```

This lets you get client feedback early without waiting for the full security audit.
The client sees a working prototype; production deployment still requires Enforce.
