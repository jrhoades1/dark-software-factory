# Model Recommendations — Job Application Skill Chain

## Why model selection matters

Each API call costs tokens. Opus 4.6 is the most capable model but costs roughly
5x more than Sonnet per token. Haiku is the cheapest at roughly 1/60th of Opus.
For a job search where you might evaluate 30-50 postings, tailoring each one adds
up fast. Matching the right model to the right task keeps costs proportional to
the complexity of the work.

## Recommendations by skill

| Skill | Recommended Model | Reasoning |
|-------|------------------|-----------|
| **job-intake** | Sonnet | Structured extraction, pattern matching, file creation. Well-defined tasks with clear criteria. |
| **resume-tailor** | Sonnet / Opus | Sonnet for keyword insertion and section reordering. Upgrade to Opus when the positioning requires creative framing of gaps or career pivots. |
| **cover-letter-writer** | Opus | Persuasive writing that needs to sound human, not templated. Tone, narrative arc, and specificity matter. This is where model quality directly affects outcomes. |
| **job-tracker** | Haiku | Pure file operations — reading metadata.json files, updating spreadsheet rows. No reasoning needed. |

## Decision framework

When choosing a model for a skill, consider three factors:

**1. Output quality sensitivity**
How much does the quality of the output vary between models? For structured data
extraction (job-intake), the difference between Sonnet and Opus is negligible — both
will pull out the same requirements list. For persuasive writing (cover letters),
the difference is significant — Opus produces noticeably more natural, compelling prose.

**2. Task complexity**
How many reasoning steps are required? Scoring a job against an achievements list
is straightforward comparison. Writing a cover letter that weaves specific
accomplishments into a narrative arc while matching the company's voice requires
deeper reasoning. More reasoning steps = more benefit from a stronger model.

**3. Volume**
How many times will this skill run per job application? Job-intake runs once per
posting. Resume-tailor runs once. But if you're iterating on a cover letter with
feedback, that's multiple Opus calls. Factor in the expected number of invocations.

## Cost estimates per application

Rough token estimates for a single job application through the full pipeline:

| Skill | Input tokens | Output tokens | Model | Est. cost |
|-------|-------------|---------------|-------|-----------|
| job-intake | ~3,000 | ~2,000 | Sonnet | ~$0.02 |
| resume-tailor | ~5,000 | ~3,000 | Sonnet | ~$0.04 |
| cover-letter-writer | ~4,000 | ~2,000 | Opus | ~$0.25 |
| job-tracker | ~1,000 | ~500 | Haiku | ~$0.001 |
| **Total per application** | | | | **~$0.31** |

At 50 applications, that's roughly $15.50. Without model optimization (Opus for
everything), the same 50 applications would cost ~$62.50. Smart model selection
saves ~75%.

## When to override the recommendation

The `recommended_model` in each SKILL.md frontmatter is a default, not a rule.
Override when:

- **User explicitly requests higher quality** — "really polish this cover letter"
  → Opus even if Sonnet is the default
- **Complex edge case** — a job description that's unusually ambiguous or a career
  pivot that requires creative positioning → upgrade from Sonnet to Opus
- **Batch operations** — processing 20 jobs at once for initial screening → downgrade
  to Haiku for the first pass, then Sonnet for the ones worth pursuing
- **Budget constraints** — if the user says "keep costs low" → Haiku for everything
  except cover letters
