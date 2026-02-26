# Security Standards

Non-negotiable security principles for all DSF projects.

## Security Principles

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
