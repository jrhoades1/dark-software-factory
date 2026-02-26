# Dark Software Factory — Open Source Claude Code Skills

Battle-tested workflow packages that teach Claude repeatable development processes.
Built from real client engagements. Free to use, copy, and adapt.

## Why Open Source

Skills are markdown files. There's no binary to protect, no build step to gate.
Once someone reads one, they can copy it. So we share them openly.

The value isn't the file — it's the operational knowledge baked into it. Every skill
in this repo exists because a real engagement produced a real lesson. The
[Five-Dimension Check](.claude/skills/servicetitan-analysis/references/analysis-methodology.md)
wasn't invented in a vacuum — it was extracted from an analysis that got the answer
188% wrong on the first pass and self-corrected in the same session.

**Skills are the portfolio, not the product.** If you can run them yourself, great.
If you want the person who wrote them to run them for you, [that's the business](https://darksoftwarefactory.com).

## Skills

| Skill | References | Model | Purpose |
|---|---|---|---|
| **[citadel-workflow](.claude/skills/citadel-workflow/SKILL.md)** | 9 refs | Opus | 7-step secure build process (Conceive-Inventory-Tie-Assemble-Drill-Enforce-Look) |
| **[project-bootstrap](.claude/skills/project-bootstrap/SKILL.md)** | 5 refs + script + evals | Sonnet | Scaffold full-stack applications |
| **[security-hardening](.claude/skills/security-hardening/SKILL.md)** | 4 refs | Sonnet | Pre-deployment audit + monitoring |
| **[hipaa-scaffold](.claude/skills/hipaa-scaffold/SKILL.md)** | — | Opus | HIPAA compliance layer for healthcare apps |
| **[onboarding-setup](.claude/skills/onboarding-setup/SKILL.md)** | — | Haiku | Beginner-safe Claude Code environment setup |
| **[servicetitan-analysis](.claude/skills/servicetitan-analysis/SKILL.md)** | 2 refs | Sonnet | Operational analytics for home services businesses via MCP |
| **[job-intake](.claude/skills/job-intake/SKILL.md)** | 3 refs + evals | Sonnet | Parse job postings, score fit, create application folders |
| **[resume-tailor](.claude/skills/resume-tailor/SKILL.md)** | 2 refs + evals | Sonnet | Adaptive resume tailoring — light/moderate/heavy based on match score |
| **[cover-letter-writer](.claude/skills/cover-letter-writer/SKILL.md)** | 1 ref + evals | Opus | Formal cover letters — adapts strategy to match score |
| **[job-tracker](.claude/skills/job-tracker/SKILL.md)** | 1 ref + evals | Haiku | Status tracking, follow-up management, tracker.xlsx sync |
| **[skill-creator](.claude/skills/skill-creator/SKILL.md)** | scripts | — | Create new skills from workflows |
| **[task-manager](.claude/skills/task-manager/SKILL.md)** | scripts | — | SQLite-backed task and project tracking |
| **[research](.claude/skills/research/SKILL.md)** | — | Sonnet | Deep research on any topic with structured output |

## Quick Start

### Clone and use directly
```bash
git clone https://github.com/your-org/dark-software-factory.git
cd dark-software-factory

# Copy .claude/settings.local.json to activate hooks
# (Review it first — it registers PreToolUse, PostToolUse, and Stop hooks)
```

### Or install skills into an existing project
```bash
cp -r .claude/skills/* /your-project/.claude/skills/
cp -r .claude/rules/* /your-project/.claude/rules/
cp -r .claude/agents/* /your-project/.claude/agents/
```

## Architecture

```
dark-software-factory/
├── CLAUDE.md                                # Lean kernel — identity, architecture, philosophy
├── README.md
│
├── .claude/
│   ├── settings.local.json                  # Hook registration (Stop, PreToolUse, PostToolUse)
│   │
│   ├── rules/                               # Modular standards (always loaded)
│   │   ├── security-standards.md            # OWASP, CWE, merge checklist
│   │   ├── guardrails.md                    # Destructive action blocks, protected files
│   │   ├── memory-protocol.md               # 3-tier memory system
│   │   ├── billing-protocol.md              # Session tracking, project codes
│   │   └── analysis-protocol.md             # 6-dimension completion check
│   │
│   ├── agents/                              # Specialized subagents
│   │   ├── researcher.md                    # Sonnet — read-only research
│   │   ├── code-reviewer.md                 # Opus — code quality review
│   │   └── security-auditor.md              # Opus — OWASP/CWE security audit
│   │
│   └── skills/                              # 14 workflow packages
│       ├── citadel-workflow/                 # 7-step secure build (9 references)
│       ├── project-bootstrap/               # Full-stack scaffolding (5 refs + script + evals)
│       ├── security-hardening/              # Pre-deployment audit (4 refs)
│       ├── hipaa-scaffold/                  # HIPAA compliance layer
│       ├── onboarding-setup/                # Beginner Claude Code setup
│       ├── servicetitan-analysis/           # MCP analytics (2 refs)
│       ├── csr-training/                    # CSR call scripts for ALD (8 refs)
│       ├── job-intake/                      # Parse & score jobs (3 refs + evals)
│       ├── resume-tailor/                   # Adaptive resume tailoring (2 refs + evals)
│       ├── cover-letter-writer/             # Match-score cover letters (1 ref + evals)
│       ├── job-tracker/                     # Status tracking (1 ref + evals)
│       ├── skill-creator/                   # Meta-skill: create new skills (scripts)
│       ├── task-manager/                    # SQLite task tracking (scripts)
│       └── research/                        # Deep research with structured output
│
├── context/                                 # Business knowledge
│   └── business-model.md                    # Contractor methodology, customer ladder
│
├── global/
│   └── references/                          # Detailed reference docs
│       ├── billing-guide.md                 # Expense schema, rate card, invoicing
│       └── requirements-template.md         # YAML frontmatter spec format
│
├── hooks/                                   # Lifecycle automation (Python)
│   ├── guardrail_check.py                   # PreToolUse — block dangerous commands
│   ├── memory_capture.py                    # Stop — auto-create daily logs
│   └── validate_output.py                   # PostToolUse — validate JSON output
│
├── args/
│   └── preferences.yaml                     # Runtime config (model routing, timezone)
│
├── memory/                                  # 3-tier persistent memory
│   ├── MEMORY.md                            # Tier 1: curated facts (always loaded)
│   └── logs/                                # Tier 2: daily session logs
│
├── data/                                    # SQLite databases (tasks, tracking)
└── .tmp/                                    # Disposable scratch files
```

## How Skills Work

Each skill follows progressive disclosure — load only what's needed:

| Level | What loads | When |
|-------|-----------|------|
| **Metadata** | Name + description (YAML frontmatter) | Always in context |
| **SKILL.md** | Core workflow instructions | When skill triggers |
| **References** | Detailed patterns, examples, case studies | On demand |

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

## Hooks

Three lifecycle hooks enforce safety and persistence:

| Hook | Type | Purpose |
|------|------|---------|
| `guardrail_check.py` | PreToolUse | Blocks `rm -rf`, `--force`, `--no-verify`, protected file deletion |
| `validate_output.py` | PostToolUse | Validates JSON output from skill scripts |
| `memory_capture.py` | Stop (async) | Ensures daily log exists, captures session markers |

Hooks are registered in `.claude/settings.local.json`. Copy it to activate.

## Memory System

Three-tier persistence across sessions:

| Tier | File | Purpose |
|------|------|---------|
| 1 | `memory/MEMORY.md` | Curated facts, always loaded (~200 lines max) |
| 2 | `memory/logs/YYYY-MM-DD.md` | Daily session logs, auto-created by Stop hook |
| 3 | mem0 + Pinecone (optional) | Vector memory with semantic search |

## Agents

Three specialized subagents for parallel work:

| Agent | Model | Purpose |
|-------|-------|---------|
| `researcher` | Sonnet | Read-only topic investigation with structured briefs |
| `code-reviewer` | Opus | Code quality review (correctness, security, performance, design) |
| `security-auditor` | Opus | OWASP/CWE security audit for the CITADEL Enforce step |

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
- **job-intake** — built from a manual walkthrough proving the scoring system before codifying it
- **resume-tailor** — iterated after the first version consistently spilled to 2 pages
- **cover-letter-writer** — passed all tests on the first iteration
- **job-tracker** — pure bookkeeping that keeps metadata.json and tracker.xlsx in sync

The framework improves every time it runs. Mistakes become guardrails. Edge cases become reference docs.

## Contributing

Found a gap? Built a skill for your own domain? PRs welcome.

A good skill has:
1. **A SKILL.md** with clear trigger conditions and step-by-step workflow
2. **A `recommended_model`** in the YAML frontmatter with reasoning
3. **References** for anything too detailed for the main SKILL.md
4. **Real-world origin** — it should come from actual work, not hypothetical best practices
5. **Eval cases** — trigger tests that validate when the skill should and shouldn't fire

## License

MIT. Use it, fork it, build on it. If it helps you ship better software, that's the point.
