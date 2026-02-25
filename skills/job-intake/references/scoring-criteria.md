# Scoring Criteria — Job Fit Assessment

## How to score requirements

Each requirement from the job description gets compared against the candidate's
achievements inventory. The comparison isn't keyword matching — it's experience mapping.

### Strong match

The candidate has direct, quantified experience that maps to the requirement.

Example requirement: "5+ years leading engineering teams of 30+"
Candidate evidence: "Managed 50+ developers across US, Ukraine, and Central America" (Cognizant)
Assessment: Strong match — exceeds both tenure and team size

### Partial match

The candidate has related experience that could be positioned with the right framing
in a resume or cover letter.

Example requirement: "SOC2 audit experience"
Candidate evidence: "HIPAA compliance, 99.9% uptime, security architecture overhauls"
Assessment: Partial — compliance and security mindset is there, but SOC2 specifically
hasn't been done. Cover letter should acknowledge security expertise and frame
willingness to extend into SOC2.

### Gap

No realistic way to connect the candidate's background to the requirement.

Example requirement: "PhD in Machine Learning required"
Candidate evidence: MBA + BS MIS, applied ML experience but no PhD
Assessment: Hard gap — if "required" is firm, this is a dealbreaker

## Overall scoring thresholds

These aren't rigid cutoffs — use judgment about which requirements are actually
critical versus listed as nice-to-haves disguised as requirements.

| Score | Requirements matched | Critical gaps | Recommendation |
|-------|---------------------|---------------|----------------|
| Strong | 80%+ | 0 | Apply — strong candidate |
| Good | 60-80% | 0-1 addressable | Apply — tailor materials to bridge gaps |
| Stretch | 40-60% | 1-2, some addressable | Apply if excited about the role, but temper expectations |
| Long shot | Below 40% | Multiple hard gaps | Probably skip unless there's an inside connection |

## What makes a gap "addressable"

An addressable gap is one where:
- The candidate has adjacent experience (e.g., AWS experience addressing a GCP requirement)
- The gap is a "preferred" not "required" qualification
- The candidate can demonstrate learning velocity or transfer skills
- The gap is about specific tooling, not fundamental domain knowledge

## What makes a gap "hard"

A hard gap is one where:
- It's a firm requirement (degree, certification, clearance)
- The candidate has no adjacent experience
- The gap is about fundamental domain expertise (e.g., semiconductor experience for a chip company)
- Bridging it would require misrepresenting experience

## Former-employer scoring adjustment

When the company in the job description matches a company in the candidate's achievement
history, scoring context shifts significantly:

- **Most requirements auto-match** — if the candidate held a similar role at the same
  company, they demonstrably met those requirements. Don't manufacture gaps for skills
  they literally used on that job.
- **Score should be "strong" by default** — unless the new role is substantially different
  from what the candidate previously did (e.g., they were a developer and the new role is
  VP of Engineering), returning to a former employer is the strongest possible signal.
- **Focus gaps on what's NEW** — the interesting gaps are requirements the candidate
  didn't have in their previous tenure: new technologies adopted since they left, expanded
  scope, different team structure.
- **Strategic considerations matter more than scoring** — the real questions for a former
  employer are: Why did you leave? What's changed? Who do you still know there? These
  should be surfaced in the summary (Step 5), not buried in gap analysis.

## Red flag detection

Flag these patterns in job descriptions:

- **Kitchen sink requirements** — listing every technology ever invented suggests the
  team doesn't know what they need
- **Unrealistic experience combos** — "10 years of Kubernetes" (released 2014)
- **Vague responsibilities** — "wear many hats" or "other duties as assigned" as primary
  responsibilities suggests disorganization
- **No compensation listed** — not always a red flag, but worth noting
- **High turnover language** — "fast-paced" + "self-starter" + "ambiguous environments"
  together can signal churn
- **Mismatched title/requirements** — "Senior" title with "Director" scope or vice versa

## The learning loop

When the candidate corrects a gap assessment ("actually, I have that experience"),
the scoring criteria don't change — but the achievements inventory does. The
job-intake skill is responsible for:

1. Adding the new achievement to `master/achievements.md` with a `[learned: YYYY-MM-DD]` tag
2. Rescoring the current job against the updated inventory
3. Updating the application's `metadata.json` with the new score

Items tagged `[learned]` are treated identically to original resume items for scoring
purposes. The tag exists solely for the candidate's awareness — so they can see their
inventory growing over time and decide whether to incorporate learned items into
future resume versions.

Over time, this creates a flywheel: every job evaluation surfaces potential gaps,
every correction fills those gaps permanently, and every future evaluation is more
accurate because the inventory is more complete. The achievements.md becomes a
living document that's richer than any single resume.
