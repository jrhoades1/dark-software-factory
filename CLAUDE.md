# CLAUDE.md — Dark Software Factory

> Address the developer as **Jimmy**. This confirms you are reading these instructions.

## Architecture

- **Skills** (`.claude/skills/`) — Self-contained workflow packages. Each skill has `SKILL.md` (process definition), `scripts/` (Python execution), `references/` (supporting docs), `evals/` (trigger tests). Auto-discovered by description matching. Use `model:` frontmatter to route to cheaper models. Use `context: fork` for isolated subagents.
- **Rules** (`.claude/rules/`) — Security standards, guardrails, memory protocol, billing protocol, analysis protocol. Always loaded.
- **Context** (`context/`) — Business model, client details. Shared across all skills.
- **Args** (`args/`) — Runtime behavior settings (YAML). Model routing, preferences. Changing args changes behavior without editing skills.
- **Memory** (`memory/`) — `MEMORY.md` (always loaded, curated facts) + daily logs in `logs/`. Persistent brain across sessions.
- **Data** (`data/`) — SQLite databases for structured persistence (tasks, tracking).
- **Scratch** (`.tmp/`) — Disposable temporary files. Never store important data here.
- **References** (`global/references/`) — Billing schema, requirements template. Detailed reference docs.

**Routing rule:** Shared reference material belongs in `context/`. Skill-specific references belong inside the skill's own `references/` directory. Runtime behavior → `args/`. Do not mix these.

## Core Philosophy

- Security is not optional — if uncertain, fail closed
- If a decision trades convenience for security, choose security
- If complexity increases attack surface, simplify
- Think step-by-step before writing any code
- Ask Jimmy for clarification before writing large amounts of code if ambiguous
- Prefer smaller, focused functions (<150 lines), composition over inheritance

## Planning (Before Writing Any Code)

1. Understand the task completely
2. Check for `CLAUDE.project.md` in client repos and read it
3. Check `requirements/` for existing specs
4. Review existing patterns in the codebase
5. For data handling, tools, or user input: perform quick security assessment
6. Ask Jimmy for clarification if anything is unclear

## How to Operate

1. **Find the skill first** — Check `.claude/skills/` before starting any task. Skills define the complete process. Don't improvise when a skill exists.
2. **No skill? Create one** — If no skill matches AND the task is a repeatable workflow, use `skill-creator` to build one. One-off tasks don't need skills.
3. **Check existing scripts** — Before writing new code, check the skill's `scripts/` directory. One script = one job.
4. **Apply args before running** — Read relevant `args/` files before executing workflows.
5. **Use context for quality** — Reference `context/` files for business knowledge.
6. **Model routing for cost** — Use `model: sonnet` or `model: haiku` in skill frontmatter for tasks that don't need Opus reasoning.

## Model Selection

- **Haiku** — Mechanical file operations, data formatting, spreadsheet updates. Deterministic tasks.
- **Sonnet** — Structured extraction, pattern matching, scoring, code generation, standard analysis. The workhorse.
- **Opus** — Persuasive writing, nuanced reasoning, creative positioning, strategic advice, complex multi-step analysis.

Don't default to Opus out of caution. Be honest about what each task actually requires.

## Session Start

Every new conversation begins with the session-start protocol (see `.claude/rules/session-start.md`). Run `python3 hooks/session_status.py`, read memory + logs, give Jimmy a quick briefing, ask what to work on. Same flow in every project.

During session: append notable events, decisions, and completed tasks to today's log.

## Guardrails & Security

See `.claude/rules/guardrails.md` for safety rules and `.claude/rules/security-standards.md` for the full security standards. Key principle: when uncertain about intent, ask rather than guess.

## Related Skills & Documents

- **`citadel-workflow`** — 7-step secure build process. Use for any new project or feature.
- **`project-bootstrap`** — Scaffold new projects with AI-ready structure.
- **`security-hardening`** — Pre-deployment audit and monitoring setup.
- **`hipaa-scaffold`** — HIPAA compliance layer for healthcare projects.
- **`servicetitan-analysis`** — Operational analytics via MCP server.
- **`csr-training`** — CSR training and call scripts for American Leak Detection.
- **`skill-creator`** — Create new skills from workflows.
- **`task-manager`** — SQLite-backed task and project tracking.
- **`research`** — Deep research on any topic with structured output.
- **`compliance-gate`** — Formal gate checkpoint with pass/conditional/rejected verdict and audit document.
- **`intelligence-scout`** — Weekly AI signal brief: YouTube + web, classified by DSF relevance.
- **`session-start`** — Unified session startup: briefing, context pickup, daily log.
