---
name: cover-letter-writer
description: >
  Write targeted cover letters for job applications using scored match data and
  tailored resumes. Use this skill whenever the user wants a cover letter for a
  specific role — after resume tailoring, when the user says "write a cover letter,"
  "draft a cover letter for this job," "I need a cover letter," "write the letter,"
  or when proceeding through the application workflow after resume-tailor completes.
  Also trigger when the user says "next step" or "let's keep going" after a resume
  has been tailored. This skill reads the application folder (metadata.json, tailored
  resume, job description) and produces a concise, formal cover letter that addresses
  gaps and reinforces strengths. Outputs .docx, .pdf, and .md versions. Do NOT trigger
  for general writing help, thank-you notes, follow-up emails, or resignation letters —
  those are different workflows.
recommended_model:
  default: opus
  reasoning: >
    Cover letters are persuasive writing where model quality directly affects outcomes.
    The letter needs to sound human, weave specific accomplishments into a narrative,
    address gaps without drawing attention to them, and match the right tone. Opus
    produces noticeably more natural, compelling prose than Sonnet for this task.
  downgrade_to_sonnet_when: >
    The user explicitly asks for a quick draft or says "keep costs low." A Sonnet
    draft that the user edits is better than no letter at all.
---

# Cover Letter Writer — Concise, Targeted Application Letters

Take the scored job data and tailored resume, then write a short, formal cover letter
that makes the case for why this candidate is the right fit.

## Why this skill exists

A cover letter does what a resume can't — it tells a story. The resume proves you
have the skills; the cover letter explains why you want THIS role at THIS company
and how your specific experience maps to their specific needs. It's also the place
to address gaps head-on, turning potential objections into demonstrations of
self-awareness and growth mindset.

This skill writes letters that are short enough to actually get read (3-4 paragraphs)
and specific enough that they couldn't be sent to any other company.

## Prerequisites

This skill expects:
- A completed job-intake evaluation with `metadata.json` and `job-description.md`
- A tailored resume (from resume-tailor) — so the letter can reference the same
  positioning without contradicting it
- `master/achievements.md` — for pulling specific evidence
- `master/narrative.md` — for tone alignment and differentiators

If the tailored resume doesn't exist yet, tell the user to run resume-tailor first.
The cover letter should build on the resume's positioning, not work independently.

## Workflow

### Step 1: Load context

Read from the application folder:
- `metadata.json` — match score, gaps (addressable and hard), keywords, and
  whether this is a former employer
- `job-description.md` — the full posting for company voice and specific language
- `resume.md` or `resume.docx` — the tailored version, so you know what's already
  been emphasized and can complement rather than duplicate

Read from master:
- `narrative.md` — differentiators and role-type themes
- `achievements.md` — for pulling specific evidence the resume may not include

### Step 2: Plan the letter structure

Before writing, decide what the letter needs to accomplish. This changes based on
the match score and context:

**Strong match:** The letter is almost a formality — keep it tight. Lead with
enthusiasm for the specific role, highlight 1-2 differentiators, close with a call
to action. Don't over-explain when the resume already does the talking.

**Good match:** Address the 1-2 addressable gaps. Frame adjacent experience as a
strength ("my AWS architecture work translates directly to GCP"). Show
self-awareness without apologizing.

**Stretch match:** This is where the letter earns its keep. Acknowledge the gap
between requirements and experience honestly, then make the case for why the
candidate's trajectory, learning velocity, and adjacent skills make them worth
interviewing despite the gap. The letter should convey genuine interest in the
specific problems this company faces.

**Former employer:** Skip the generic positioning — they know you. Focus on what's
changed since you left: new skills, broader perspective, expanded scope. Address
why you're coming back. "I've spent the last three years as CTO at ilumed, gaining
experience in AI/ML integration and value-based care that I didn't have during my
previous tenure" is more effective than rehashing your Cognizant achievements.

### Step 3: Write the letter

Use a formal business tone throughout. No contractions, no casual phrasing, but
also not robotic — the letter should read like it was written by a senior
professional, not generated from a template.

**Structure — 3 to 4 paragraphs:**

**Opening paragraph (2-3 sentences):**
State the role you're applying for and why you're interested in THIS company
specifically. Pull something specific from the job description or company context
that shows you've done your homework — not generic praise ("a leader in healthcare")
but something pointed ("your expansion from 200K to 1M lives managed through
value-based care aligns with the exact scaling challenge I solved at ilumed").

**Body paragraph(s) (1-2 paragraphs, 3-5 sentences each):**
This is the core argument. Pick 2-3 of the strongest matches from metadata.json
and connect them to the role with specific evidence. Use numbers from
achievements.md — "expanded beneficiary coverage from 50,000 to 90,000" is
stronger than "grew the user base significantly."

If there are addressable gaps, weave one into the body naturally. Don't start a
sentence with "Although I lack..." — instead, frame the adjacent experience
positively: "While my cloud architecture work has been primarily on AWS, the
multi-cloud scheduling platform I built at Red Spot Interactive (integrating AWS,
Azure, and SaaS components) demonstrates the architectural flexibility this role
requires."

**Closing paragraph (2-3 sentences):**
Express interest in discussing the role further. Reference something forward-looking
— a problem from the job description you're excited to solve, a vision for how
your experience maps to their roadmap. End with a professional close, not a
desperate one.

**What makes a cover letter bad:**
- Opening with "I am writing to express my interest in..." — everyone does this,
  nobody reads past it
- Restating the resume bullet by bullet — the reader has the resume, don't
  repeat it
- Generic company praise that could apply to any company in the industry
- Addressing every single requirement — pick the strongest 2-3 and go deep
- Being longer than one page — if a recruiter has to scroll, they won't
- Mentioning gaps without framing them — "I don't have GCP experience" is a
  red flag; "My multi-cloud work across AWS and Azure positions me to adopt
  GCP rapidly" is a strength

### Step 4: Generate outputs

Produce three versions:

1. **cover-letter.md** — Markdown for quick review in chat. Show this to the user.

2. **cover-letter.docx** — Formal business letter format:
   - Read `references/letter-format.md` for the exact formatting specification
   - Candidate name and contact info at top
   - Date and company address block
   - "Dear Hiring Manager" (or specific name if known from metadata.contact)
   - Letter body
   - "Sincerely," followed by candidate name

3. **cover-letter.pdf** — PDF export for application portals.

Save all three to the application folder.

Update `metadata.json`:
- Set `cover_letter` to the filename (e.g., `"cover-letter.docx"`)
- If `resume_version` already has a value, update `status` to `"ready_to_apply"`

### Step 5: Present and refine

Show the user the markdown version. Summarize:

1. **Strategy used** — what you led with and why
2. **Gaps addressed** — which ones you wove in and how
3. **Tone check** — confirm it matches the formal business voice they want

The user may want changes. Cover letters are personal — the user knows things
about the company, the hiring manager, or the role that the system doesn't. When
they request changes, update all three files (.md, .docx, .pdf) to stay in sync.

Common revision requests:
- "Make it shorter" — cut the body to a single paragraph with the top 2 evidence points
- "I know the hiring manager" — swap "Dear Hiring Manager" for their name and adjust
  the tone to be slightly warmer while staying formal
- "Emphasize [specific skill] more" — restructure the body to lead with that skill
- "Don't mention [gap]" — remove the gap framing; the user may have strategic
  reasons for not addressing it

After the user approves, suggest proceeding to job-tracker to log the application.

## Skill composition

This skill is third in the job application workflow:

| Upstream | This skill | Downstream |
|----------|-----------|-----------|
| job-intake → resume-tailor | **cover-letter-writer** | job-tracker (logs the application) |

The metadata.json is the shared contract. This skill reads match scores, gaps, and
keywords from it; writes the cover letter filename back to it.

## Edge cases

- **No tailored resume yet** — Tell the user to run resume-tailor first. The cover
  letter needs to complement the resume's positioning, not freelance.
- **User wants to skip the cover letter** — That's fine. Not every application
  needs one. Update metadata.status to "ready_to_apply" if the resume is done.
- **Multiple versions** — If the user wants variations (e.g., one addressing a
  specific gap more aggressively), create versioned files:
  `cover-letter-v1.docx`, `cover-letter-v2.docx`.
- **Company research available** — If the user provides additional context about
  the company (recent news, products, culture), weave it into the opening
  paragraph. This is where specificity really shines.
