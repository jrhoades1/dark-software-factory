# Dark Software Factory — Open Source Claude Code Skills

Battle-tested workflow packages that teach Claude repeatable development processes.
Built from real client engagements. Free to use, copy, and adapt.

## Why Open Source

Skills are markdown files. There's no binary to protect, no build step to gate.
Once someone reads one, they can copy it. So we share them openly.

The value isn't the file — it's the operational knowledge baked into it. Every skill
in this repo exists because a real engagement produced a real lesson. The
[Five-Dimension Check](skills/servicetitan-analysis/references/analysis-methodology.md)
wasn't invented in a vacuum — it was extracted from an analysis that got the answer
188% wrong on the first pass and self-corrected in the same session.

**Skills are the portfolio, not the product.** If you can run them yourself, great.
If you want the person who wrote them to run them for you, [that's the business](https://darksoftwarefactory.com).

## Skills

| Skill | References | Model | Purpose |
|---|---|---|---|
| **[project-bootstrap](skills/project-bootstrap/SKILL.md)** | 5 refs + script + evals | Sonnet | Scaffold full-stack applications |
| **[citadel-workflow](skills/citadel-workflow/SKILL.md)** | 9 refs | Opus | 7-step secure build process (Conceive-Inventory-Tie-Assemble-Drill-Enforce-Look) |
| **[security-hardening](skills/security-hardening/SKILL.md)** | 4 refs | Sonnet | Pre-deployment audit + monitoring |
| **[hipaa-scaffold](skills/hipaa-scaffold/SKILL.md)** | — | Opus | HIPAA compliance layer for healthcare apps |
| **[onboarding-setup](skills/onboarding-setup/SKILL.md)** | — | Haiku | Beginner-safe Claude Code environment setup |
| **[servicetitan-analysis](skills/servicetitan-analysis/SKILL.md)** | 2 refs | Sonnet | Operational analytics for home services businesses via MCP |
| **[job-intake](skills/job-intake/SKILL.md)** | 3 refs + evals | Sonnet | Parse job postings, score fit, create application folders with learning loop |
| **[resume-tailor](skills/resume-tailor/SKILL.md)** | 2 refs + evals | Sonnet | Adaptive resume tailoring with page-fitting — light/moderate/heavy based on match score |
| **[cover-letter-writer](skills/cover-letter-writer/SKILL.md)** | 1 ref + evals | Opus | Concise formal cover letters — adapts strategy to match score, addresses gaps, former-employer awareness |
| **[job-tracker](skills/job-tracker/SKILL.md)** | 1 ref + evals | Haiku | Status tracking, follow-up management, and tracker.xlsx sync — the bookkeeping layer that closes the loop |

**Total:** ~50 files, 10,000+ lines across all skills and references.

## Quick Start

### Install into Claude Code
```bash
# Copy skills to your Claude Code skills directory
cp -r skills/* ~/.claude/skills/

# Copy global standards to your project
cp global/CLAUDE.md ~/your-project/CLAUDE.md
```

### Or add to a project repo
```bash
cp -r skills/ .claude/skills/
```

## How Skills Work

Each skill follows progressive disclosure — load only what's needed:

| Level | What loads | When |
|-------|-----------|------|
| **Metadata** | Name + description (YAML frontmatter) | Always in context |
| **SKILL.md** | Core workflow instructions | When skill triggers |
| **References** | Detailed patterns, examples, case studies | On demand |

This means Claude doesn't burn context on the full IR playbook when scaffolding a project, or load attack scenarios when setting up monitoring.

## Skill Composition

Skills chain together for common workflows:

| Workflow | Skills |
|----------|--------|
| New SaaS product | project-bootstrap → citadel-workflow → security-hardening |
| Healthcare app | project-bootstrap → citadel-workflow → hipaa-scaffold → security-hardening |
| Pre-deployment audit | security-hardening (standalone) |
| ServiceTitan analytics | servicetitan-analysis (standalone, requires MCP server) |
| New developer onboarding | onboarding-setup (standalone) |
| Job application | job-intake → resume-tailor → cover-letter-writer → job-tracker |

## Architecture

```
dark-software-factory/
├── README.md
├── global/
│   └── CLAUDE.md                          # Always-loaded standards
└── skills/
    ├── project-bootstrap/
    │   ├── SKILL.md
    │   ├── scripts/bootstrap.py           # Automated scaffolding
    │   ├── references/                    # 5 files: stack defaults, templates, quality gates
    │   └── evals/evals.json              # 20 trigger test cases
    │
    ├── citadel-workflow/
    │   ├── SKILL.md
    │   └── references/                    # 9 files: zero-trust, AI security, attack scenarios, etc.
    │
    ├── security-hardening/
    │   ├── SKILL.md
    │   └── references/                    # 4 files: IR playbook, alert thresholds, infra checklist
    │
    ├── hipaa-scaffold/
    │   └── SKILL.md
    │
    ├── onboarding-setup/
    │   └── SKILL.md
    │
    ├── servicetitan-analysis/
    │   ├── SKILL.md
    │   └── references/                    # 2 files: Five-Dimension methodology, ALD case study
    │
    ├── job-intake/
    │   ├── SKILL.md                       # recommended_model: sonnet
    │   ├── references/                    # 3 files: scoring criteria, folder schema, model recs
    │   └── evals/evals.json              # 10 trigger test cases
    │
    ├── resume-tailor/
    │   ├── SKILL.md                       # recommended_model: sonnet
    │   ├── references/                    # 2 files: tailoring patterns, docx format spec
    │   └── evals/evals.json              # 3 test cases
    │
    ├── cover-letter-writer/
    │   ├── SKILL.md                       # recommended_model: opus
    │   ├── references/                    # 1 file: letter format spec
    │   └── evals/evals.json              # 3 test cases
    │
    └── job-tracker/
        ├── SKILL.md                       # recommended_model: haiku
        ├── references/                    # 1 file: xlsx operations patterns
        └── evals/evals.json              # 3 test cases
```

## Security Coverage

| Framework | Coverage | Provided by |
|-----------|----------|------------|
| OWASP Top 10 (2021) | 100% | security-hardening + citadel-workflow |
| OWASP LLM Top 10 | 100% | citadel-workflow/ai-security.md |
| CWE Top 25 | 90% | security-hardening + attack-scenarios.md |
| HIPAA Security Rule | Full | hipaa-scaffold |
| Zero-Trust | Full | citadel-workflow/zero-trust-patterns.md |
| Incident Response | Full | security-hardening/ir-playbook.md |

## Origin

These skills were extracted from production consulting work — not designed in theory.
Each one represents a pattern that was tested, failed, corrected, and codified.

- **citadel-workflow** — evolved from a 1,848-line monolithic build doc that was too heavy for context
- **servicetitan-analysis** — born from an ALD compensation analysis where the first answer was 188% low
- **security-hardening** — built after auditing real deployments and finding the same gaps repeatedly
- **hipaa-scaffold** — extracted from healthcare project compliance requirements

- **job-intake** — built from a manual walkthrough of the job application process, proving the folder structure and scoring system before codifying it into a skill. Introduced the learning loop pattern where the skill updates its own reference data when corrected.
- **resume-tailor** — developed through iteration when the first version consistently spilled resumes to 2 pages. The bullet budget system and 4-level formatting levers were added after observing the failure across all test cases.
- **cover-letter-writer** — passed all tests on the first iteration. The match-score-adaptive strategy (strong=tight, stretch=make the case, former=what's changed) emerged from analyzing what makes cover letters effective for different scenarios.
- **job-tracker** — the bookkeeping layer. Pure file operations that keep metadata.json and tracker.xlsx in sync so nothing falls through the cracks.

The framework improves every time it runs. Mistakes become guardrails. Edge cases become reference docs.

## Contributing

Found a gap? Built a skill for your own domain? PRs welcome.

A good skill has:
1. **A SKILL.md** with clear trigger conditions and step-by-step workflow
2. **A `recommended_model`** in the YAML frontmatter — Haiku for mechanical tasks, Sonnet for structured work, Opus for nuanced reasoning. Include the reasoning so others can evaluate the choice.
3. **References** for anything too detailed for the main SKILL.md
4. **Real-world origin** — it should come from actual work, not hypothetical best practices
5. **Eval cases** — trigger tests that validate when the skill should and shouldn't fire

## License

MIT. Use it, fork it, build on it. If it helps you ship better software, that's the point.
