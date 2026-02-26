# Billing Protocol

Cost tracking and session attribution for DSF projects.

## Session Tracking

Sessions logged to `claude-tracking/sessions.csv`. Each project needs
`.claude/project-code.txt` for attribution and `.claude/billing.json` for expenses.

See `global/references/billing-guide.md` for the full billing.json schema, rate card,
setup instructions, and invoice commands.

## Active Project Codes

| Code | Project | Client |
|------|---------|--------|
| ALD-SERVICETITAN | ServiceTitan MCP Server | American Leak Detection |
| ALD-CALL-ANALYSIS | Call Analysis & Training | American Leak Detection |
| JOB-APPLICATIONS | Job Application System | Internal |

## Requirements Management

Each project has `requirements/` with structured specs (YAML frontmatter + markdown).
- One file per requirement: `REQ-NNN-short-slug.md`
- Claude can propose (`status: proposed`) but NOT implement without Jimmy's approval
- See `global/references/requirements-template.md` for full format and field reference
