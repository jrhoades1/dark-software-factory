# Application Folder Schema

## Workspace layout

```
job-applications/
├── master/
│   ├── base-resume.docx          # Canonical resume — source of truth
│   ├── achievements.md           # Categorized, quantified accomplishments
│   └── narrative.md              # Tone guide, differentiators, themes by role type
├── applications/
│   └── YYYY-MM-DD_company-slug_role-slug/
│       ├── job-description.md    # Full posting, cleaned up
│       ├── metadata.json         # Structured data (see schema below)
│       ├── resume.docx           # Tailored version (created by resume-tailor)
│       └── cover-letter.docx     # Tailored version (created by cover-letter-writer)
└── tracker.xlsx                  # Master spreadsheet, one row per application
```

## Naming conventions

**Folder names:** `YYYY-MM-DD_company-slug_role-slug`
- Date is when the job was first evaluated (not necessarily applied)
- Company slug: lowercase, hyphens for spaces, no special characters
- Role slug: lowercase, hyphens, abbreviated if long

Examples:
- `2026-02-24_healthfirst_vp-engineering`
- `2026-03-01_amazon-web-services_senior-sde`
- `2026-03-05_johns-hopkins_dir-eng`

## metadata.json schema

```json
{
  "company": "string — full company name",
  "role": "string — exact job title from posting",
  "location": "string — city, state / remote / hybrid",
  "compensation": "string | null — salary range if listed",
  "applied_date": "string | null — YYYY-MM-DD when application submitted",
  "source": "string — where the job was found (LinkedIn, Indeed, referral, etc.)",
  "source_url": "string — URL of the original posting",
  "status": "string — evaluating | ready_to_apply | applied | interviewing | offered | rejected | withdrawn",
  "follow_up_date": "string | null — YYYY-MM-DD for next follow-up",
  "contact": "string — recruiter or referral name if known",
  "resume_version": "string | null — filename of tailored resume",
  "cover_letter": "string | null — filename of tailored cover letter",
  "former_employer": "boolean — true if company appears in achievements.md",
  "former_employer_role": "string | null — candidate's previous role at this company",
  "notes": "string — freeform notes",
  "match_score": {
    "overall": "string — strong | good | stretch | long_shot",
    "requirements_matched": ["array of matched requirement strings"],
    "requirements_partial": ["array of partial match strings"],
    "gaps": ["array of all gap strings"],
    "addressable_gaps": ["subset of gaps that can be bridged"],
    "hard_gaps": ["subset of gaps with no realistic bridge"],
    "keywords": ["array of terms for resume/cover letter targeting"]
  }
}
```

## Status lifecycle

```
evaluating → ready_to_apply → applied → interviewing → offered
                                   ↘ rejected
                           ↘ withdrawn
```

- **evaluating** — job-intake has parsed it, candidate is deciding
- **ready_to_apply** — resume and cover letter are tailored, ready to submit
- **applied** — application has been submitted
- **interviewing** — in active interview process
- **offered** — received an offer
- **rejected** — received a rejection at any stage
- **withdrawn** — candidate decided not to continue

## tracker.xlsx columns

| Column | Source | Notes |
|--------|--------|-------|
| Date Applied | metadata.applied_date | Blank until submitted |
| Company | metadata.company | |
| Role | metadata.role | |
| Source | metadata.source | |
| Status | metadata.status | |
| Match Score | metadata.match_score.overall | |
| Follow-up Date | metadata.follow_up_date | |
| Contact | metadata.contact | |
| Resume Version | metadata.resume_version | |
| Cover Letter | metadata.cover_letter | |
| Notes | metadata.notes | |

The tracker can be regenerated at any time by scanning all `applications/*/metadata.json`
files. The individual folders are the source of truth — the spreadsheet is a convenience view.
