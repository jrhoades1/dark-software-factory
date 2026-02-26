---
name: job-tracker
description: >
  Update application status, log follow-ups, and maintain the job tracker spreadsheet.
  Use this skill whenever the user wants to update the status of a job application — "I
  applied," "I got a rejection," "they scheduled an interview," "mark it as withdrawn,"
  "update the tracker," "log this application," "I submitted it," "any follow-ups due?"
  Also trigger when the user says "I'm done" or "submitted" after the resume and cover
  letter are ready, or asks to check on pending applications, review follow-up dates, or
  get a status overview of all active applications. This is the bookkeeping skill — it
  keeps metadata.json and tracker.xlsx in sync so nothing falls through the cracks.
  Do NOT trigger for evaluating new jobs (job-intake), tailoring resumes (resume-tailor),
  or writing cover letters (cover-letter-writer).
recommended_model:
  default: haiku
  reasoning: >
    This skill does pure file operations: read metadata.json, update a field, write it
    back, update a spreadsheet row. No reasoning, no creative writing, no analysis.
    Haiku handles this at a fraction of the cost of Sonnet.
  upgrade_to_sonnet_when: >
    The user asks for a status summary or analysis across multiple applications (e.g.,
    "how's my job search going?"). Summarizing patterns across many applications benefits
    from Sonnet's reasoning. For individual status updates, Haiku is sufficient.
---

# Job Tracker — Keep Applications Organized

## Intent

1. **metadata.json is the single source of truth** — tracker.xlsx is a convenience view; when they conflict, metadata.json wins and the spreadsheet gets corrected
2. **Follow-up discipline prevents lost opportunities** — every "applied" status gets a follow-up date; every passed follow-up date gets surfaced; no application silently expires
3. **Folder completeness before status advancement** — warn when advancing to "applied" if resume or cover letter files are missing from the application folder
4. **No lost applications** — every status change is persistent across both metadata.json and tracker.xlsx; nothing falls through the cracks between sessions
5. **Searchable history enables learning** — past applications are data for analytics and strategy, not dead folders; the tracker is the index that makes them findable
6. **Single status update under 1 minute; full overview under 5 minutes** — bookkeeping should be invisible, never a bottleneck in the application workflow

## Why this skill exists

Applying to jobs without tracking means losing context. Three weeks after submitting,
you forget which version of your resume you sent, whether you had a contact name,
or when you planned to follow up. This skill makes every status change persistent —
updating both the application's metadata.json (source of truth) and the tracker.xlsx
(convenience view) so neither drifts.

## Prerequisites

This skill expects:
- `job-applications/tracker.xlsx` — the master spreadsheet
- At least one application folder in `job-applications/applications/` with a
  `metadata.json` file

If tracker.xlsx doesn't exist, offer to create it using the schema from
job-intake's `references/folder-schema.md`.

## Workflow

### Step 1: Understand the update

The user will tell you what happened. Common triggers:

| User says | Action |
|-----------|--------|
| "I applied" / "submitted" / "sent it" | Set status → `applied`, set `applied_date` to today |
| "Got a rejection" / "they passed" | Set status → `rejected` |
| "They want an interview" / "scheduled a call" | Set status → `interviewing` |
| "Got an offer" | Set status → `offered` |
| "I'm pulling out" / "withdrawing" | Set status → `withdrawn` |
| "Follow up next week" / "remind me on March 5" | Set `follow_up_date` |
| "The recruiter's name is Sarah" | Set `contact` field |
| "Add a note: they want references" | Append to `notes` field |

If the user doesn't specify which application, check context — did they just
finish tailoring a resume or writing a cover letter? If so, use that application.
If it's ambiguous, list the active applications and ask which one.

### Step 2: Update metadata.json

Read the application's `metadata.json`, make the change, and write it back.

**Status transitions follow this lifecycle:**
```
evaluating → ready_to_apply → applied → interviewing → offered
                                  ↘ rejected
                          ↘ withdrawn
```

Validate the transition makes sense. If someone says "I got an offer" but the
status is still `evaluating`, that's unusual — confirm before updating. The user
might mean a different application.

**When setting status to `applied`:**
- Set `applied_date` to today's date (YYYY-MM-DD) unless the user specifies a
  different date
- Set a default `follow_up_date` two weeks out unless the user specifies one
- Confirm the resume and cover letter filenames are populated — if they're null,
  warn the user that the application folder doesn't have tailored materials saved

**When setting status to `interviewing`:**
- If the user mentions a date, set `follow_up_date` to the day after the interview
- If they mention a name, update `contact`

### Step 3: Update tracker.xlsx

After updating metadata.json, sync the change to tracker.xlsx. The spreadsheet
is a convenience view — metadata.json is the source of truth, and the spreadsheet
should reflect it.

Read the existing tracker.xlsx. Find the row matching this application by company
and role. Update the relevant columns:

| Column | Source |
|--------|--------|
| Date Applied | `metadata.applied_date` |
| Company | `metadata.company` |
| Role | `metadata.role` |
| Source | `metadata.source` |
| Status | `metadata.status` |
| Match Score | `metadata.match_score.overall` |
| Follow-up Date | `metadata.follow_up_date` |
| Contact | `metadata.contact` |
| Resume Version | `metadata.resume_version` |
| Cover Letter | `metadata.cover_letter` |
| Notes | `metadata.notes` |

If no row exists for this application (e.g., the user applied without going through
the full skill chain), add a new row.

Read `references/xlsx-operations.md` for the specific openpyxl patterns for reading
and updating the spreadsheet.

### Step 4: Confirm the update

Tell the user what you changed, briefly:
- "Updated HealthFirst VP of Engineering to **applied** — applied date set to
  Feb 24, follow-up date set to March 10. Tracker spreadsheet is in sync."

If there are other applications with follow-up dates that have passed, mention
them: "By the way, you have 2 applications with follow-up dates that have passed —
want me to review them?"

## Bulk operations

The user may ask for operations across multiple applications:

**"How's my job search going?" / "Give me a status overview"**
Scan all `applications/*/metadata.json` files. Summarize by status:
- X applications in evaluating
- X applied, waiting to hear back
- X in interview process
- X with follow-ups due (list them with dates)

**"Update the tracker from all folders"**
Rebuild tracker.xlsx entirely by scanning all metadata.json files. This is useful
if the spreadsheet has drifted or the user has been updating metadata manually.

**"What follow-ups are due?"**
Scan for applications where `follow_up_date` is today or earlier and status is
`applied` or `interviewing`. List them with company, role, and how many days
overdue.

## Skill composition

This skill is the final step in the job application workflow:

| Upstream | This skill |
|----------|-----------|
| job-intake → resume-tailor → cover-letter-writer | **job-tracker** (logs and tracks) |

After this skill runs, the application is fully tracked. The workflow is complete
until the user gets a response and needs another status update.

## Edge cases

- **Application not in the system** — The user applied outside the skill chain
  (e.g., quick-applied on LinkedIn). Create a minimal metadata.json and folder
  from whatever info the user provides, then add to the tracker.
- **Duplicate applications** — If a folder already exists for this company+role
  at a different date, ask if this is a re-application or if they meant the
  existing one.
- **Tracker spreadsheet is missing** — Offer to create it. Scan all existing
  application folders to populate it.
- **Bulk rejection** — The user might say "reject everything from last month that
  I haven't heard back from." Process each one individually but confirm the list
  before making changes.
