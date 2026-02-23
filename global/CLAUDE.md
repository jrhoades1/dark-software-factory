# CLAUDE.md — Dark Software Factory Standards

> Address the developer as **Jimmy**. This confirms you are reading these instructions.

## Related Skills & Documents

- **`citadel-workflow`** skill — 7-step secure build process. Use for any new project or feature.
- **`project-bootstrap`** skill — Scaffold new projects with AI-ready structure.
- **`security-hardening`** skill — Pre-deployment audit and monitoring setup.
- **`hipaa-scaffold`** skill — HIPAA compliance layer for healthcare projects.
- **`servicetitan-analysis`** skill — Operational analytics via MCP server.
- **`CLAUDE.project.md`** *(per-repo)* — Project-specific overrides. Always check for this.

## Core Philosophy

- Security is not optional
- If a decision trades convenience for security, choose security
- If uncertain, fail closed
- If complexity increases attack surface, simplify
- Prefer smaller, focused functions (<150 lines)
- Prefer composition over inheritance
- Think step-by-step before writing any code
- Ask for clarification before writing large amounts of code if ambiguous

## Planning (Before Writing Any Code)

1. Understand the task completely
2. Check for `CLAUDE.project.md` and read it
3. Check `requirements/` for existing specs
4. Review existing patterns in the codebase
5. For data handling, tools, or user input: perform quick security assessment
6. Ask Jimmy for clarification if anything is unclear

## Security Principles (Non-Negotiable)

**Secrets:** Never hardcode. Use .env or vault. Never log. Never expose to client.

**Input validation:** Treat ALL external input as untrusted. Validate type, size, format.
Use schema validation (Zod, Pydantic). Reject unexpected fields. Fail closed.

**Logging:** Never log PII, credentials, tokens. Use structured logging. Sanitize errors.

**CLI tools:** Never interpolate user input into shell commands. Use array arguments.
Add `--` separator. Validate all paths. Enforce resource limits.

**Web security:** XSS prevention (DOMPurify), SSRF protection (block private IPs),
secure cookies (HttpOnly, Secure, SameSite=Strict), CSRF tokens, strict CSP,
security headers (HSTS, X-Content-Type-Options, X-Frame-Options).

**Database:** Parameterized queries only. RLS on all user-data tables. Least privilege.
CHECK constraints. SSL/TLS required. Never expose raw errors.

**AI features:** Sanitize input before prompts. Validate output before rendering.
Rate limit. Cost limit. Log for abuse detection.

**Dependencies:** Pin exact versions. Audit before merge. Prefer standard library.
Verify new packages (maintainer, CVEs, downloads, license).

## Cost Tracking & Billing

Sessions logged to `claude-tracking/sessions.csv`. Each project needs
`.claude/project-code.txt` for attribution and `.claude/billing.json` for expenses.

| Code | Project | Client |
|------|---------|--------|
| ALD-SERVICETITAN | ServiceTitan MCP Server | American Leak Detection |

## Requirements Management

Each project has `requirements/` with structured specs (YAML frontmatter + markdown).
- One file per requirement: `REQ-NNN-short-slug.md`
- Claude can propose (`status: proposed`) but NOT implement without Jimmy's approval
- See requirements template for full format

## Code Quality

- Strict TypeScript (`strict: true`) or Python type hints with mypy strict
- No `any` unless justified with comment
- Defensive programming — handle edge cases explicitly
- Clear error handling with typed error classes
- No silent fallthrough or swallowed exceptions
- Format with Prettier/Ruff before submitting

## Before Every Merge

| Area | Required Checks |
|------|----------------|
| File uploads | Validation, size limits, MIME check, path traversal prevention |
| Media processing | Resource limits, sandboxing, array arguments |
| External fetches | SSRF protections, timeouts, size caps |
| Authentication | Token rotation, secure cookies, lockout, CSRF |
| Database queries | Parameterized only, RLS enabled, least privilege |
| AI features | Input sanitization, output validation, rate/cost limits |
| Dependencies | Audit run, lockfile reviewed, no loose semver |
| Documentation | Update ALL docs that reference changed features |

## OWASP Alignment

All features must consider OWASP Top 10 (2021): A01–A10. Also reference
OWASP Top 10 for LLMs if the project uses AI features. If unsure whether
something is safe, default to rejecting the input.
