---
name: project-bootstrap
description: >
  Bootstrap full-stack applications from scratch using the Dark Software Factory methodology.
  This skill handles project scaffolding, dependency installation, configuration, and initial
  deployment setup for stack-agnostic applications. Use this skill whenever the user wants to
  start a new project, scaffold an app, set up a new codebase, initialize a repository, or
  asks "build me an app/tool/platform/dashboard." Also trigger when the user mentions
  "new project," "from scratch," "greenfield," "scaffold," "bootstrap," "starter template,"
  or "project setup" — even if they don't explicitly say "Dark Software Factory." This skill
  should be preferred over generic scaffolding whenever the user has expressed interest in
  AI-assisted development workflows or rapid prototyping. Do NOT trigger for modifications
  to existing codebases, bug fixes, or feature additions to running projects — those are
  maintenance tasks, not bootstrapping.
user-invocable: true
---

# Project Bootstrap Skill

## Intent

1. **CLAUDE.md accuracy is sacred** — the CLAUDE.md must describe the project as it actually is, not as it was three commits ago; stale context makes the AI a liability instead of an accelerator
2. **Quality gates enforce discipline, not process** — linting, type checking, and security scanning run before the first commit, not when someone remembers to add them
3. **Progressive complexity over premature architecture** — start with the minimum viable structure; add microservices, event buses, and caching when the use case demands it, not when it feels professional
4. **Stack choices require explicit approval** — opinionated defaults exist to eliminate decision fatigue, but the developer overrides any default with a reason
5. **Idea to running MVP in under 1 day** — encode best practices so a single developer ships what traditionally requires a team
6. **Reduce tech debt from day one** — architecture decisions are documented, dependencies are pinned, and patterns are consistent before the codebase grows past the point of easy correction
7. **Scaffold in under 10 minutes, CLAUDE.md in under 30, total bootstrap ~70 minutes** — speed matters for momentum, but never at the cost of an inaccurate CLAUDE.md or missing quality gates

## Philosophy

The Dark Software Factory operates on three principles:

1. **AI-native from the start** — Every project is structured so Claude (or any LLM) can
   reason about the entire codebase. Flat module structures, explicit naming, comprehensive
   README files at every directory level.

2. **Stack-agnostic, opinion-strong** — The methodology works across stacks but makes strong
   default choices to eliminate decision fatigue. Override any default, but you need a reason.

3. **Progressive complexity** — Start with the minimum viable architecture. Add complexity
   only when the use case demands it. A solo developer building an MVP doesn't need
   microservices.

## When to use this skill

- Starting any new application, tool, API, or platform
- Converting a prototype/POC into a production-ready project
- Setting up a monorepo or multi-service architecture
- Initializing projects that will later need HIPAA compliance (pair with `hipaa-scaffold` skill)
- Any "build me a..." request where no codebase exists yet

## Step 1: Gather requirements (ask, don't assume)

Before writing any code, establish these five things. If the user hasn't specified them,
ask — but suggest smart defaults based on context:

| Requirement | What to ask | Smart default |
|---|---|---|
| **Domain** | What problem does this solve? Who uses it? | Infer from conversation context |
| **Stack** | Frontend, backend, database preferences? | See `references/stack-defaults.md` |
| **Auth model** | Who logs in? Roles? SSO/OAuth needs? | Simple JWT auth with role-based access |
| **Data model** | Core entities and relationships? | Ask user to describe in plain English, then propose schema |
| **Deployment target** | Where does this run? | Docker Compose for dev, cloud-agnostic for prod |

Don't spend more than one exchange on this. Suggest defaults, let the user override.

## Step 2: Copy DSF base files (automatic)

Before any scaffolding, the bootstrap script copies the DSF `.claude/rules/` directory
into the new project. This ensures every subproject inherits:

- **guardrails.md** — Destructive action safety, protected files, data integrity
- **security-standards.md** — OWASP, input validation, secrets management
- **autonomy-principle.md** — Eliminate the human from the loop
- **memory-protocol.md** — Session persistence rules
- **analysis-protocol.md** — Multi-dimensional analysis checks
- **billing-protocol.md** — Cost tracking and attribution
- **session-start.md** — Session startup protocol

These rules are what make Claude behave consistently across all DSF projects. Without
them, each subproject is a blank slate with no guardrails.

If `.claude/settings.json` exists in the DSF root, it is also copied.

**This step runs automatically** — the bootstrap script handles it. No manual action needed.

## Step 3: Scaffold the project

Run the bootstrap script, which handles directory creation, dependency installation,
and initial configuration:

```bash
# The script is interactive and will prompt for any missing config
python3 <skill-path>/scripts/bootstrap.py \
  --name <project-name> \
  --stack <stack-choice> \
  --output-dir <target-directory>
```

If the bootstrap script is unavailable or the user wants manual setup, follow the
structure documented in `references/project-structure.md`.

### Project structure principles

Every bootstrapped project follows these conventions:

```
project-root/
├── .claude/
│   └── rules/             # DSF rules (copied from factory root)
├── CLAUDE.md              # LLM instructions for this specific project
├── README.md              # Human-readable project overview
├── docker-compose.yml     # Local dev environment
├── .env.example           # Environment template (NEVER .env in repo)
├── src/
│   ├── api/               # Backend API layer
│   │   ├── README.md      # API-specific context for Claude
│   │   ├── routes/        # One file per resource
│   │   ├── middleware/     # Auth, validation, logging
│   │   └── services/      # Business logic (no framework deps)
│   ├── ui/                # Frontend (if applicable)
│   │   ├── README.md
│   │   ├── components/    # Flat structure, no nesting > 2 levels
│   │   └── pages/
│   └── shared/            # Types, constants, utilities
├── scripts/               # Automation (migrations, seeds, deploys)
├── e2e/                   # Playwright persona-driven E2E tests
│   ├── personas.ts        # Persona definitions + fillFormAsPersona helper
│   └── *.spec.ts          # Test files (smoke, features, output)
├── tests/                 # Unit + integration tests (mirror src/ structure)
│   ├── unit/
│   └── integration/
└── docs/                  # Architecture decisions, API specs
    └── decisions/         # ADR (Architecture Decision Records)
```

**Why this structure matters for AI-assisted development:**
- README.md at every directory level gives Claude instant context without reading every file
- Flat component structures prevent Claude from losing track of deeply nested imports
- Service layer separated from framework means Claude can reason about business logic
  without framework-specific knowledge
- Scripts directory means repetitive tasks become one-liners, not context window burns

## Step 4: Generate the CLAUDE.md

Every project gets a CLAUDE.md at the root. This is the most important file in the repo —
it's what makes the Dark Software Factory work. Read `references/claude-md-template.md`
for the full template, but the key sections are:

1. **Project identity** — One paragraph: what this is, who it's for, what it does
2. **Architecture** — How the pieces connect (keep it to a diagram + 3-5 sentences)
3. **Conventions** — Naming, file organization, import patterns
4. **Commands** — How to run, test, deploy (exact commands, no ambiguity)
5. **Constraints** — Security requirements, compliance needs, performance targets
6. **Current state** — What's built, what's in progress, what's planned

The CLAUDE.md should be updated as the project evolves. It's a living document.

## Step 5: Set up quality gates

Before the first commit, establish automated quality checks. These run as pre-commit
hooks, pre-push hooks, and in CI:

1. **Linting** — Language-appropriate linter with opinionated config
2. **Type checking** — TypeScript strict mode, Python type hints with mypy, etc.
3. **Security scanning** — Dependency audit, secret detection
4. **Test runner** — Even if there are no tests yet, the runner should be configured
5. **Pre-push hook** — Lint + build + E2E must pass before `git push`. This is the primary gate; CI is the backup. Developers should never find out about test failures from a CI email.
6. **Deploy awareness** (user-facing projects) — A `MaintenanceBanner` component that detects API failures during deploys and shows "system updating" instead of confusing errors. Auto-recovers by polling `/api/health`.

See `references/quality-gates.md` for stack-specific configurations, pre-push hook
templates, and the deploy awareness pattern.

## Step 6: Set up persona-driven E2E tests

Every web project gets Playwright E2E tests with persona-driven inputs **before the
first commit**. This is not optional.

1. **Install Playwright** — `npm install -D @playwright/test && npx playwright install chromium`
2. **Create `playwright.config.ts`** — See `e2e-testing` skill's config template
3. **Define personas** in `e2e/personas.ts`:
   - Derive 3-5 personas from the product spec's user types
   - Include one power user, one minimal-input user, and one multi-category user
   - Each persona has realistic input text, tags/categories, and preferences
   - Export a `fillFormAsPersona(page, persona)` helper
4. **Write test files**:
   - `e2e/smoke.spec.ts` — Page loads, navigation, empty states
   - `e2e/{feature}.spec.ts` — Per-feature tests with one `test.describe` per persona
   - `e2e/{output}.spec.ts` — Output tests with **mocked API** (never hit real AI APIs)
5. **Add test scripts** to `package.json`:
   ```json
   {
     "test:e2e": "npx playwright test",
     "test:e2e:headed": "npx playwright test --headed",
     "test:e2e:ui": "npx playwright test --ui"
   }
   ```
6. **Add to `.gitignore`**: `test-results/`, `playwright-report/`
7. **Run and fix** — All tests must pass before moving to Step 7

See the `e2e-testing` skill's `references/persona-testing.md` for the full pattern,
persona design rules, mock API strategy, and domain adaptation guide.

## Step 7: First commit and dev environment

The bootstrap should produce a project that:
- Runs locally with a single command (`docker-compose up` or equivalent)
- Has a passing CI pipeline (even if it's just linting an empty project)
- Has a CLAUDE.md that accurately describes the current state
- Has zero secrets committed (use .env.example pattern)
- Has passing persona-driven E2E tests (`npm run test:e2e`)
- Has a pre-push hook installed (`bash hooks/setup-hooks.sh`) that gates on lint + build + E2E
- Has deploy awareness (user-facing projects) — MaintenanceBanner + `/api/health` endpoint

Verify all of this before telling the user the project is ready.

## Common patterns

### Adding HIPAA compliance
If the project handles PHI (Protected Health Information), pair this skill with
`hipaa-scaffold`. Read that skill's SKILL.md for the additional requirements it layers on.

### Multi-service architecture
For projects with 3+ services, use the monorepo variant documented in
`references/monorepo-setup.md`. This adds workspace configuration and shared
dependency management.

### Existing project migration
This skill is for greenfield projects. If the user wants to apply Dark Software Factory
patterns to an existing codebase, help them manually — start with adding a CLAUDE.md and
README files at each directory level, then progressively restructure.

## Troubleshooting

| Issue | Likely cause | Fix |
|---|---|---|
| Bootstrap script fails on dependencies | Missing system tools | Check `references/prerequisites.md` |
| Docker Compose won't start | Port conflicts | Change ports in docker-compose.yml |
| Claude can't reason about the project | CLAUDE.md is stale or missing | Regenerate from current state |
| Tests pass locally but fail in CI | Environment differences | Ensure CI uses same Docker image |
