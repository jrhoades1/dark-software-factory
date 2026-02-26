---
name: resume-tailor
description: >
  Tailor resumes to specific job descriptions using scored application data from job-intake.
  Use this skill whenever the user wants to customize their resume for a specific role — after
  a job has been evaluated, when the user says "tailor my resume," "customize my resume for
  this job," "adjust my resume," "make my resume match this posting," or when the user says
  "yes" or "let's apply" after a job-intake summary. This skill reads the application folder
  created by job-intake (metadata.json with match scores, gaps, and keywords) and produces a
  tailored resume that emphasizes the candidate's strongest matches and addresses gaps through
  strategic positioning. Outputs .docx, .pdf, and .md versions. Do NOT trigger for writing
  resumes from scratch (that's a different workflow), general career advice, or cover letters
  (that's cover-letter-writer).
recommended_model:
  default: sonnet
  reasoning: >
    Resume tailoring is structured transformation: read scored data, select and reorder
    content, adjust phrasing to hit keywords. Sonnet handles this well. The adaptive
    intensity logic (light vs heavy tailoring) is rule-based, not creative reasoning.
  upgrade_to_opus_when: >
    The match score is "stretch" or "long shot" and the user still wants to apply.
    Heavy repositioning of experience to bridge significant gaps benefits from Opus's
    stronger reasoning about how to frame indirect experience convincingly.
---

# Resume Tailor — Customize Resumes for Specific Jobs

## Intent

1. **Never fabricate experience** — every bullet must trace back to base-resume.docx or achievements.md; repositioning is fine, inventing is not
2. **The candidate must recognize their own resume** — tailoring adjusts emphasis and language, it does not create a document the candidate cannot defend in an interview
3. **User override authority is absolute** — if the candidate says "lead with Red Spot" or "drop Cognizant," that instruction overrides the adaptive logic without question
4. **Maximize apparent fit for the specific role** — surface the right keywords, lead with the most relevant experience, and address gaps through positioning
5. **Automate the tedious rewrite** — the candidate should not hand-edit a resume for every application; structured data from job-intake drives the tailoring
6. **Light tailoring under 5 minutes, moderate under 10, heavy under 15** — speed matters across dozens of applications, but never at the cost of fabrication or a resume that spills to two pages
7. **One page, always** — with 20+ years of experience this requires deliberate compression; bullet budgets and formatting levers exist for this reason

## Why this skill exists

A generic resume is a missed opportunity. Recruiters spend seconds scanning — the
tailored version needs to surface the right keywords, lead with the most relevant
experience, and address gaps through smart positioning rather than ignoring them.
This skill automates that process using the structured data that job-intake already
produced, so every application gets a resume that's tuned for the role without the
candidate rewriting it from scratch each time.

## Prerequisites

This skill expects:
- A completed job-intake evaluation (application folder with `metadata.json` and
  `job-description.md`)
- `master/base-resume.docx` — the candidate's canonical resume
- `master/achievements.md` — categorized accomplishments (may include `[learned]` items)
- `master/narrative.md` — tone and positioning guide

If the application folder doesn't exist or metadata.json is missing, tell the user
to run job-intake first. This skill can't work without scored data — it needs to know
what to emphasize.

## Workflow

### Step 1: Load the application context

Read three files from the application folder:
- `metadata.json` — the match score, requirements matched/partial/gaps, keywords, and
  whether this is a former employer
- `job-description.md` — the full posting for reference

Then read the master files:
- `master/base-resume.docx` — extract the current resume structure and content
- `master/achievements.md` — the full achievement inventory (richer than the resume)
- `master/narrative.md` — tone guide and role-type themes

Understanding the base resume's structure is important — you need to know what sections
exist, how bullets are organized, and what the current emphasis looks like before you
can decide what to change.

### Step 2: Determine tailoring intensity

The amount of change depends on how good the match already is. Check
`metadata.match_score.overall`:

| Match score | Intensity | What changes |
|-------------|-----------|-------------|
| **Strong** | Light | Keyword injection, minor reordering. The resume already fits well — don't over-engineer it. Swap in 2-3 keywords from the job posting, maybe reorder the skills section to lead with what they're asking for. |
| **Good** | Moderate | Keyword injection + bullet repositioning + selective additions from achievements.md. Pull in 1-2 achievements that aren't on the base resume but strengthen partial matches. Reorder experience bullets so the most relevant ones lead each section. |
| **Stretch** | Heavy | Significant restructuring. May rewrite the summary/objective, reorder entire sections (e.g., lead with the most relevant role even if it's not the most recent), pull multiple items from achievements.md, reframe adjacent experience to address gaps. |
| **Long shot** | Heavy + honest | Same as stretch, but include a note to the user that even with heavy tailoring, this is a reach. The resume can only do so much — the cover letter and any personal connections matter more here. |

For **former employer** applications (`former_employer: true`), use light intensity
regardless of score. The candidate's history at that company speaks for itself — heavy
tailoring looks odd when applying back to somewhere you've already worked.

Read `references/tailoring-patterns.md` for specific examples of each intensity level.

### Step 3: Build the tailored resume

Work through the resume section by section. The general structure should stay
recognizable as the candidate's resume — readers don't like disorientation. But
within that structure, make strategic changes.

**Summary / Professional Profile:**
- Read `narrative.md` for the role-type themes that match this job (CTO vs Director
  vs Architect). Use those themes to shape the opening.
- Include 2-3 keywords from `metadata.match_score.keywords` naturally — not stuffed in,
  but woven into sentences that demonstrate the skill.
- If the match has addressable gaps, the summary is the place to pre-emptively address
  the most important one. Example: if the job asks for GCP experience and the candidate
  has AWS, the summary might say "cloud architecture across AWS and Azure with rapid
  adoption of new platforms."

**Experience sections:**
- Reorder bullets within each role so the most relevant ones come first. A recruiter
  who stops reading after 2 bullets should see the strongest matches.
- For **moderate and heavy** tailoring: pull in achievements from `achievements.md` that
  aren't on the base resume but directly address requirements or partial matches. Tag
  pulled-in items in your working notes so you can tell the user what was added.
- For **heavy** tailoring: consider reordering the roles themselves if a non-recent role
  is more relevant. Use a "Relevant Experience" / "Additional Experience" split if
  chronological order buries the best match.
- Match the terminology from the job posting where truthful. If they say "microservices
  architecture" and the resume says "distributed systems," use their language (if accurate).

**Skills / Technical section:**
- Reorder to lead with the technologies mentioned in the job posting.
- Add any skills from `achievements.md` or `master/base-resume.docx` that are relevant
  to this job but currently missing from the skills section.
- Remove or de-emphasize skills that aren't relevant to create space for what matters.

**Education:**
- Generally leave this alone. If the job specifically calls out MBA or a particular
  degree and the candidate has it, make sure it's visible (not buried at the bottom).

**Page-fitting — the single-page target:**

One page is the goal for all tailoring intensities. With 20+ years and 5 roles, this
requires deliberate compression. Use a bullet budget to stay within bounds:

| Role position | Bullet budget (1-page) | Bullet budget (2-page OK) |
|--------------|----------------------|--------------------------|
| Current / most relevant role | 4-5 bullets | 5-6 bullets |
| Roles 2-3 | 3-4 bullets | 4-5 bullets |
| Roles 4+ (oldest) | 2-3 bullets | 3-4 bullets |

For heavy tailoring (stretch matches), compress less-relevant roles aggressively — 2
bullets each is fine if the space goes toward strengthening the relevant roles.

**Self-check before generating files:** After drafting the markdown version, count the
total bullets and estimate length. If over 22-24 total bullets across all roles, the
resume will likely spill to page 2. Trim from the oldest and least relevant roles first.
If it still won't fit, reduce per-role bullet counts by 1 across the board.

Read `references/docx-format.md` for formatting levers (font size, spacing, margins)
that can reclaim space when content compression alone isn't enough.

**What NOT to do:**
- Don't fabricate experience. Every bullet must trace back to either `base-resume.docx`
  or `achievements.md`. Repositioning is fine; inventing is not.
- Don't use hollow filler language. "Results-driven leader" adds nothing. Use the
  narrative.md tone guidelines — specific, quantified, active voice.
- Don't keyword-stuff. If a keyword appears 6 times, the resume reads like SEO spam.
  Use each keyword 1-2 times in context that demonstrates the skill.
- Don't remove experience just because it's not relevant. Shorten it, de-emphasize it,
  but gaps in employment history raise questions.

### Step 4: Generate outputs

Produce three versions of the tailored resume:

1. **resume.md** — Markdown version. Create this first as your working draft. Clean,
   readable, easy to review in chat. This is also what you'll show the user for approval.

2. **resume.docx** — Word document with clean professional formatting:
   - Use a readable font (Calibri or similar), 10-11pt body, 14pt name
   - Clear section headers with consistent styling
   - Appropriate margins (0.75" to 1")
   - Single page strongly preferred; two pages maximum for 15+ years experience
   - Read `references/docx-format.md` for the exact formatting specification

3. **resume.pdf** — PDF export of the .docx for application portals. Generate using
   the appropriate conversion tool after the .docx is finalized.

Save all three to the application folder (e.g.,
`applications/2026-02-24_healthfirst_vp-engineering/`).

Update `metadata.json`:
- Set `resume_version` to the filename (e.g., `"resume.docx"`)
- Update `status` to `"ready_to_apply"` if a cover letter already exists, otherwise
  leave as `"evaluating"`

### Step 5: Present the result

Show the user the markdown version in chat for quick review. Then provide a summary
of what changed:

1. **Tailoring intensity used** and why (based on match score)
2. **Key changes made** — which bullets were reordered, what was pulled from
   achievements.md, how the summary was adjusted
3. **Keywords addressed** — which job posting keywords now appear in the resume
   and where
4. **Gaps still visible** — any hard gaps that the resume can't address (these are
   for the cover letter)

End by asking if they want to proceed to the cover letter (which would trigger
cover-letter-writer) or if they want adjustments to the resume first.

**Important:** If the user asks for changes, make them to all three files (.md, .docx,
.pdf) — don't let the versions drift out of sync.

## Skill composition

This skill sits in the middle of the job application workflow:

| Upstream | This skill | Downstream |
|----------|-----------|-----------|
| job-intake (creates the application folder) | **resume-tailor** (produces tailored resume) | cover-letter-writer (references the tailored resume) |

The metadata.json is the shared contract. This skill reads match scores and keywords
from it, writes the resume filename back to it.

## Edge cases

- **No application folder** — The user wants to tailor a resume but hasn't run
  job-intake. Don't try to wing it — the scored data is essential. Tell them to run
  job-intake first, or offer to run it now if they have the job description.
- **User wants manual overrides** — They might say "lead with the Red Spot experience"
  or "don't include the Cognizant role." Respect these instructions even if they
  contradict the adaptive logic. The user knows things about the application that
  the system doesn't.
- **Multiple tailored versions** — If the user wants a second version (e.g., one
  emphasizing AI and another emphasizing leadership), create versioned filenames:
  `resume-v1-ai-focus.docx`, `resume-v2-leadership-focus.docx`. Update metadata to
  point to the one they plan to submit.
- **Base resume has changed** — If the user updates `base-resume.docx` after previous
  tailoring runs, the old tailored resumes won't reflect the change. If you notice a
  mismatch, mention it.
