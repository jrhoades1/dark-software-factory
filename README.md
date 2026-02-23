# Dark Software Factory — Claude Code Skills

Portable workflow packages that teach Claude your repeatable development processes.
Write once, run forever.

## Migration from v1 (Monolithic Files)

This package replaces the three monolithic framework files with composable, progressively-
disclosed skills:

| Old File | Lines | New Skill(s) | Status |
|----------|-------|--------------|--------|
| `CLAUDE.md` (v2.0) | 467 | `global/CLAUDE.md` (101 lines) | Migrated |
| `BUILD_APP.md` (v4.0) | 1,848 | `citadel-workflow` + `security-hardening` | Migrated |
| `SETUP_GUIDE.md` (v2.0) | 607 | `onboarding-setup` | Migrated |
| `REQUIREMENTS_TEMPLATE.md` | 80 | Referenced from `citadel-workflow` | Referenced |

**Key improvement:** BUILD_APP.md alone was 1,848 lines dumped into context every time.
Now the CITADEL workflow is 320 lines in the SKILL.md with detailed content in 9 reference
files loaded only when needed.

## Skills Overview

| Skill | Status | SKILL.md | References | Purpose |
|---|---|---|---|---|
| **project-bootstrap** | Complete | 174 lines | 5 refs + script + evals | Scaffold full-stack applications |
| **citadel-workflow** | Complete | 320 lines | 9 refs | 7-step secure build process |
| **security-hardening** | Complete | 221 lines | 4 refs | Pre-deployment audit + monitoring |
| **hipaa-scaffold** | Complete | 226 lines | — | HIPAA compliance layer |
| **onboarding-setup** | Complete | 244 lines | — | Beginner-safe Claude Code setup |
| **servicetitan-analysis** | Stub | 101 lines | — | MCP-based operational analytics |

**Total:** 28 files, 6,315 lines across all skills and references.

## Architecture

```
dark-software-factory/
├── README.md                              ← You are here
├── global/
│   └── CLAUDE.md                          # Always-loaded rules (101 lines)
└── skills/
    ├── project-bootstrap/                 # Scaffolding & project structure
    │   ├── SKILL.md                       # Bootstrap process
    │   ├── scripts/bootstrap.py           # Automated scaffolding (FastAPI/Next.js/minimal)
    │   ├── references/
    │   │   ├── stack-defaults.md          # Opinionated stack choices
    │   │   ├── claude-md-template.md      # Template for project CLAUDE.md files
    │   │   ├── quality-gates.md           # Linting, type checking, security scanning
    │   │   ├── project-structure.md       # Manual setup guide
    │   │   └── monorepo-setup.md          # Multi-service architecture
    │   └── evals/evals.json               # 20 trigger test cases (all skills)
    │
    ├── citadel-workflow/                   # 7-step secure build methodology
    │   ├── SKILL.md                       # C-I-T-A-D-E-L process
    │   └── references/
    │       ├── schema-patterns.md         # Secure schema with RLS + constraints
    │       ├── zero-trust-patterns.md     # Middleware, mTLS, field encryption
    │       ├── ai-security.md             # LLM security (OWASP LLM Top 10)
    │       ├── attack-scenarios.md        # 11-scenario threat catalog
    │       ├── integration-security.md    # External service security requirements
    │       ├── enterprise-secrets.md      # AWS/GCP/Azure vault patterns
    │       ├── security-testing.md        # Full security test checklist
    │       ├── perf-security-balance.md   # Caching, rate limiting, encryption overhead
    │       └── api-security.md            # Versioning, signing, GraphQL, webhooks
    │
    ├── security-hardening/                # Pre-deployment audit + monitoring
    │   ├── SKILL.md                       # 10-section audit checklist
    │   └── references/
    │       ├── ir-playbook.md             # 5-phase incident response
    │       ├── ir-templates.md            # Internal + external notification templates
    │       ├── alert-thresholds.md        # Monitoring stack + alert config
    │       └── infrastructure-checklist.md # Cloud, container, DB, CI/CD security
    │
    ├── hipaa-scaffold/                    # Healthcare compliance layer
    │   └── SKILL.md                       # PHI boundaries, audit logging, encryption,
    │                                      # BAA requirements, FHIR/HL7 patterns
    │
    ├── onboarding-setup/                  # Beginner-safe environment setup
    │   └── SKILL.md                       # Install, security training, first session
    │
    └── servicetitan-analysis/             # MCP-based operational analytics
        └── SKILL.md                       # (stub — formalize from ALD work)
```

## Progressive Disclosure Model

Each skill follows a three-level loading pattern:

| Level | What loads | Size | When |
|-------|-----------|------|------|
| **1. Metadata** | Name + description (YAML frontmatter) | ~100 words | Always in context |
| **2. SKILL.md** | Core workflow instructions | <500 lines | When skill triggers |
| **3. References** | Detailed patterns, examples, templates | Unlimited | On demand |

**Why this matters:** The old BUILD_APP.md was 1,848 lines loaded every time. Now:
- CITADEL workflow SKILL.md: 320 lines (the process)
- Zero-trust patterns: loaded only during Inventory/Assemble steps
- IR playbook: loaded only during Look step
- Alert config: loaded only when setting up monitoring

Scripts (like `bootstrap.py`) execute without loading into context at all.

## How to Install

### In Claude Code
```bash
# Copy skills to your Claude Code skills directory
cp -r skills/* ~/.claude/skills/

# Copy global CLAUDE.md to your projects
cp global/CLAUDE.md ~/your-project/CLAUDE.md
```

### In a project repo
```bash
# Add skills as a subdirectory
cp -r skills/ .claude/skills/

# Or symlink for shared development
ln -s /path/to/dark-software-factory/skills .claude/skills
```

## Skill Composition

Skills are designed to compose. Common workflows:

**New healthcare app:**
```
project-bootstrap → citadel-workflow → hipaa-scaffold → security-hardening
```

**New SaaS product:**
```
project-bootstrap → citadel-workflow → security-hardening
```

**Pre-deployment check:**
```
security-hardening (standalone)
```

**Onboard new developer:**
```
onboarding-setup (standalone)
```

**Analyze ALD operations:**
```
servicetitan-analysis (standalone, requires MCP server)
```

## Security Coverage

| Framework | Coverage | Covered by |
|-----------|----------|------------|
| OWASP Top 10 (2021) | 100% | security-hardening + citadel-workflow |
| OWASP LLM Top 10 | 100% | citadel-workflow/ai-security.md |
| CWE Top 25 | 90% | security-hardening + attack-scenarios.md |
| HIPAA Security Rule | Full | hipaa-scaffold |
| Zero-Trust | Full | citadel-workflow/zero-trust-patterns.md |
| Incident Response | Full | security-hardening/ir-playbook.md |

## Reference File Index

### citadel-workflow references (9 files, 2,193 lines)
| File | Lines | Loaded during |
|------|-------|---------------|
| schema-patterns.md | 211 | Inventory step (data modeling) |
| zero-trust-patterns.md | 357 | Inventory + Assemble steps |
| ai-security.md | 336 | Assemble step (AI features) |
| attack-scenarios.md | 277 | Inventory step (threat modeling) |
| integration-security.md | 124 | Inventory + Tie steps |
| enterprise-secrets.md | 156 | Tie step (secret management) |
| security-testing.md | 194 | Drill step |
| perf-security-balance.md | 239 | Drill step |
| api-security.md | 299 | Assemble step (API-heavy apps) |

### security-hardening references (4 files, 930 lines)
| File | Lines | Loaded during |
|------|-------|---------------|
| ir-playbook.md | 222 | Look step (incident response) |
| ir-templates.md | 271 | Active incident |
| alert-thresholds.md | 216 | Look step (monitoring setup) |
| infrastructure-checklist.md | 221 | Enforce step (cloud/container) |

### project-bootstrap references (5 files, 1,098 lines)
| File | Lines | Loaded during |
|------|-------|---------------|
| stack-defaults.md | 142 | Step 1 (stack selection) |
| claude-md-template.md | 145 | Step 3 (CLAUDE.md generation) |
| quality-gates.md | 302 | Step 4 (quality gate setup) |
| project-structure.md | 220 | Step 2 (manual setup) |
| monorepo-setup.md | 289 | Multi-service projects only |

## Design Principles

1. **Skills != prompts** — Real skills have scripts, references, and execution steps.
   If it's just a wall of text, it's a prompt masquerading as a skill.

2. **Progressive disclosure saves tokens** — Claude doesn't need the full IR playbook
   when scaffolding a project. Load context only when the task demands it.

3. **Scripts > context window** — `bootstrap.py` creates 30+ files without burning
   context on directory creation. Anything deterministic should be a script.

4. **Compose, don't monolith** — Six focused skills beat one 2,800-line file.
   Each skill has a clear responsibility and hands off to others when appropriate.

5. **Test like you ship** — Every skill gets eval cases. 20 trigger tests cover all
   skills including positive triggers, negative triggers, and composition scenarios.

## Roadmap

### Done
- [x] project-bootstrap (full skill + script + 5 references + evals)
- [x] citadel-workflow (full skill + 9 reference files)
- [x] security-hardening (full skill + 4 reference files)
- [x] hipaa-scaffold (full skill with PHI patterns + FHIR/HL7)
- [x] onboarding-setup (full skill)
- [x] Global CLAUDE.md (streamlined)
- [x] Eval test cases (20 trigger tests across all skills)

### Next
- [ ] servicetitan-analysis — formalize MCP query patterns from ALD work
- [ ] Description optimization (trigger accuracy tuning)
- [ ] .skill packaging for marketplace distribution
- [ ] Cross-skill composition automation
- [ ] "Software Factory as a Service" client packaging
