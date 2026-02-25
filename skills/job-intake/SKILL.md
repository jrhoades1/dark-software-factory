---
name: job-intake
description: >
  Parse job descriptions, score candidate fit, and set up application tracking folders.
  Use this skill whenever the user shares a job posting — pasted into chat, saved as a file,
  or referenced by URL — and wants to evaluate whether it's a good match. Also trigger when
  the user says "check this job," "is this a fit," "parse this posting," "new application,"
  "evaluate this role," "score this job," or shares a block of text that looks like a job
  description (title, company, requirements, responsibilities). This skill feeds into
  resume-tailor and cover-letter-writer — run it first to create the application folder
  that downstream skills expect. Do NOT trigger for general career advice, salary research,
  or interview prep — those are different workflows.
recommended_model:
  default: sonnet
  reasoning: >
    This skill does structured extraction, pattern matching against an achievements
    inventory, file creation, and scoring. These are well-defined tasks that don't
    require deep creative reasoning or nuanced prose generation. Sonnet handles
    this reliably at ~5x lower cost than Opus. The learning loop (Step 6) involves
    simple append operations and rescoring — no model upgrade needed.
  upgrade_to_opus_when: >
    The job description is unusually ambiguous or the candidate asks for strategic
    advice beyond scoring (e.g., "should I pivot my career toward this kind of role?").
    Career-level reasoning benefits from Opus. For standard intake, Sonnet is sufficient.
---

# Job Intake — Parse, Score, and Track Job Applications

Take a raw job description, extract what matters, score it against the candidate's
background, and set up a tracked application folder so nothing gets lost.

## Why this skill exists

Applying to jobs without a system means losing track of what you sent where, missing
follow-up windows, and spending time on roles that aren't a good fit. This skill is
the front door — every application starts here, and every downstream skill (resume
tailoring, cover letter writing, tracking) depends on the structured output it produces.

## Prerequisites

This skill expects a workspace at `job-applications/` with:
- `master/base-resume.docx` — the candidate's canonical resume
- `master/achievements.md` — categorized, quantified accomplishments
- `master/narrative.md` — tone and positioning guide
- `tracker.xlsx` — master application spreadsheet

If any of these are missing, tell the user and offer to help set them up before proceeding.

## Workflow

### Step 1: Accept the job description

The user will provide the job description in one of three ways:

- **Pasted into chat** — the most common case. The text might be messy (copied from a
  web page with formatting artifacts). Clean it up mentally but preserve all content.
- **File in the workspace** — a `.md`, `.txt`, or `.docx` file in the job-applications
  folder or uploads. Read it with the appropriate tool.
- **URL** — fetch the page and extract the job posting content.

**Handling partial or incomplete input:**

Not every trigger comes with a full job description. The user might say "saw a VP of Eng
role at Google, sounds like me right?" or "what do you think about this — Chief Architect
at Cognizant, cloud migration, healthcare." When the input has a company and role but is
missing a full requirements list:

1. **Give a preliminary read** — use what you DO have plus `master/achievements.md` to
   give quick directional feedback. Example: "Based on what you've shared, healthcare AI
   and cloud architecture are strong matches in your background. A Chief Architect role
   at a consultancy like Cognizant aligns well with your experience there."
2. **Be explicit about what you CAN'T assess** — "Without the full requirements list,
   I can't give you a proper match score or identify specific gaps."
3. **Ask for the full posting** — "Can you grab the full job description so I can do a
   proper evaluation? I'll set up the application folder and score it against your resume."
4. **Do NOT create a folder or metadata.json** from partial info — the application folder
   is only created in Step 4 after a full parse. Premature folder creation pollutes the
   workspace with incomplete data.

If the input is truly minimal (just a company name with no role, or a vague "any jobs in
healthcare?"), this isn't a job-intake trigger. Respond conversationally and help them
narrow down what they're looking for.

### Step 2: Extract structured data

Pull out these fields from the job description. If a field isn't present, mark it as
"Not specified" rather than guessing:

| Field | What to extract |
|-------|----------------|
| **Company** | Organization name |
| **Role** | Exact job title |
| **Location** | City/state, remote status, hybrid details |
| **Compensation** | Salary range, equity, benefits if listed |
| **Requirements** | Hard requirements (years of experience, specific skills, degrees) |
| **Preferred** | Nice-to-haves that aren't dealbreakers |
| **Responsibilities** | What the role actually does day-to-day |
| **Red flags** | Unrealistic combos (e.g., "10 years of Kubernetes"), vague language, signs of dysfunction |
| **Keywords** | Technical terms, tools, frameworks, and domain language that should appear in a tailored resume |

### Step 2b: Check for former-employer connection

Before scoring, scan `master/achievements.md` for the **company name** extracted in Step 2.
Look for exact and fuzzy matches — "Cognizant" should match "Cognizant Softvision," and
"Red Spot" should match "Red Spot Interactive."

If the company appears in the candidate's achievement history:

1. **Flag it immediately** — tell the user: "This is at **[Company]**, where you previously
   worked as [Role]. That's a very different application strategy than a cold apply."
2. **Note it in metadata.json** — add `"former_employer": true` and
   `"former_employer_role": "Previous role title"` to the metadata.
3. **Adjust the scoring context** — when a candidate previously held a role at the same
   company (or a very similar one), most "requirements" are automatically strong matches
   because they literally did the job. The scoring in Step 3 should reflect this — don't
   manufacture gaps for skills the candidate demonstrably used at that exact company.
4. **Surface strategic considerations** — returning to a former employer means the user
   likely has internal contacts, knows the culture, and may be able to skip parts of the
   interview process. Mention this in the Step 5 summary.

If no match is found, proceed normally — no flag needed.

### Step 3: Score the match

Read `master/achievements.md` and compare the extracted requirements against the
candidate's background. For each requirement, classify it:

- **Strong match** — direct experience with quantified results
- **Partial match** — related experience that could be positioned
- **Gap** — no clear experience to point to

Produce an overall fit assessment:

| Score | Meaning |
|-------|---------|
| **Strong** | 80%+ requirements matched, no critical gaps |
| **Good** | 60-80% matched, gaps are addressable in cover letter |
| **Stretch** | 40-60% matched, significant positioning needed |
| **Long shot** | Below 40%, probably not worth tailoring materials |

Be honest about gaps. The goal isn't to be encouraging — it's to help the candidate
spend time on the right applications. A "long shot" assessment with clear reasoning
saves hours of wasted effort.

For each gap identified, note whether it's addressable (can be positioned through
adjacent experience) or hard (no realistic way to bridge it).

### Step 4: Create the application folder

Create a dated folder in `job-applications/applications/` using the naming convention:

```
YYYY-MM-DD_company-name_role-slug/
```

Company name and role slug should be lowercase, hyphenated, with special characters
removed. Examples:
- `2026-02-24_healthfirst_vp-engineering`
- `2026-03-01_amazon-web-services_senior-sde`

Inside the folder, create:

**job-description.md** — the full job description, cleaned up with a header containing
company, role, location, and the source URL if available.

**metadata.json** — structured data for tracking and downstream skills:

```json
{
  "company": "Company Name",
  "role": "Job Title",
  "location": "City, State / Remote",
  "compensation": "Range if listed, otherwise null",
  "applied_date": null,
  "source": "LinkedIn / Indeed / Referral / etc.",
  "source_url": "URL if available",
  "status": "evaluating",
  "follow_up_date": null,
  "contact": "",
  "resume_version": null,
  "cover_letter": null,
  "former_employer": false,
  "former_employer_role": null,
  "notes": "",
  "match_score": {
    "overall": "strong | good | stretch | long_shot",
    "requirements_matched": ["list of matched requirements"],
    "requirements_partial": ["list of partial matches"],
    "gaps": ["list of gaps"],
    "addressable_gaps": ["gaps that could be positioned"],
    "hard_gaps": ["gaps with no realistic bridge"],
    "keywords": ["terms to use in tailored resume"]
  }
}
```

### Step 5: Present the summary

Give the user a clear, conversational summary covering:

1. **The role in one sentence** — what this job actually is
2. **Match score** with reasoning — not just the label, but why
3. **Top strengths** — the 3-4 requirements where the candidate's experience is strongest
4. **Gaps to address** — what's missing and whether it's bridgeable
5. **Keywords to hit** — terms the resume and cover letter should include
6. **Recommendation** — should they apply? If stretch or long shot, say so clearly

End by asking if they want to proceed to resume tailoring (which would trigger the
resume-tailor skill).

### Step 6: Learn from corrections

After presenting the summary, the user may push back on gaps. They might say something
like "actually, I did SOC2 at Red Spot — we went through the audit in 2019" or "I forgot
to mention, I managed a $5M budget at MedQuest, not just $2M."

This is new information. Don't just use it for the current scoring — **persist it** so
every future job evaluation benefits. When the user provides a correction or new
accomplishment:

1. **Update `master/achievements.md`** — add the new item under the appropriate category.
   Include a `[learned]` tag and the date so the user can see what was added through
   conversation versus what was in the original resume. Format:

   ```
   - Led SOC2 Type II audit preparation and remediation (Red Spot, 2019) [learned: 2026-02-24]
   ```

2. **Rescore the current job** — rerun Step 3 with the updated achievements. The gap
   that triggered the correction should now show as a strong or partial match. Update
   the `metadata.json` in the application folder with the new score.

3. **Confirm the update** — tell the user what you added and where. They should know
   their achievements file is growing. Example: "Added your SOC2 audit experience to
   the compliance section of achievements.md. This bumped the HealthFirst match from
   'good' to 'strong' — that gap is closed now."

This learning loop is one of the most valuable parts of the system. Over time,
achievements.md becomes a comprehensive inventory of everything the candidate can
claim — far richer than any single resume version. It captures experience the user
might not think to put on a resume but that matters for specific roles.

**When NOT to update achievements.md:**
- Aspirational statements ("I could learn Terraform quickly") — these aren't accomplishments
- Vague claims without specifics ("I've done compliance stuff") — ask for details first
- Information that contradicts existing entries — flag the conflict and let the user resolve it

## Skill composition

This skill is the entry point for the job application workflow:

| Next step | Skill | When |
|-----------|-------|------|
| Tailor resume | resume-tailor | User decides to apply |
| Write cover letter | cover-letter-writer | After resume is tailored |
| Update tracker | job-tracker | After application is submitted |

The metadata.json created by this skill is the contract that downstream skills read.

## Edge cases

- **Multiple jobs at once** — If the user pastes several job descriptions, process each
  one separately. Create individual folders. Don't try to batch the analysis.
- **Incomplete postings** — Some listings are just a title and a paragraph. Follow the
  partial-input handling in Step 1: give a preliminary read from what's available, be
  clear about what you can't assess, and ask for the full posting. Don't create folders.
- **Internal referrals** — If the user mentions a referral or connection, capture it in
  the metadata contact field and notes.
- **Reprocessing** — If a folder already exists for this company+role, warn the user and
  ask if they want to update it or create a new version.
