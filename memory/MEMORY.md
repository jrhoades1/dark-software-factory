# Persistent Memory

> Curated long-term facts. Read at session start. Keep under ~200 lines.

## Identity
- Project: Dark Software Factory
- Framework: Dark Software Factory
- Developer: Jimmy
- Billing: Internal
- Business model: Contractor methodology (time + API costs)
- Website: https://darksoftwarefactory.com

## Active Projects
- ALD-SERVICETITAN: ServiceTitan MCP analytics for American Leak Detection
- ALD-CALL-ANALYSIS: Call analysis & CSR training for ALD
- JOB-APPLICATIONS: Job application pipeline (internal)
- HL-PILOT: Career Transformer AI for Higher Landing Inc. (client pilot, started 2026-03-05)

## Learned Behaviors
- Follow DSF architecture: Skills → Rules → Context → Args → Memory → Data
- Security is non-negotiable — fail closed when uncertain
- Check existing skills before starting any task
- Use model routing for cost efficiency (Haiku < Sonnet < Opus)
- Skills live in .claude/skills/, rules in .claude/rules/, agents in .claude/agents/
- Files in ~/Downloads are ephemeral — always copy into project immediately before processing
- Each child project gets: CLAUDE.md, .claude/project-code.txt, .claude/rules/, hooks/, memory/, context/
- Every web project gets Playwright E2E tests before delivery (e2e-testing skill)
- Hook paths in settings.local.json must be absolute — relative paths break when shell CWD changes
