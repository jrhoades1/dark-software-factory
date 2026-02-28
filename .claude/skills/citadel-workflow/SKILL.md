---
name: citadel-workflow
description: >
  Execute the CITADEL secure development methodology for building production applications.
  CITADEL is a 7-step process: Conceive, Inventory, Tie, Assemble, Drill, Enforce, Look.
  Use this skill whenever starting a new application, major feature, or full build cycle.
  Trigger on phrases like "build an app," "new project," "CITADEL," "let's build," "start
  building," "create an application," "develop a platform," or any request that involves
  going from idea to deployed software. Also trigger when the user says "follow the workflow"
  or "secure build process." Pair with project-bootstrap for scaffolding, security-hardening
  for the Enforce/Look steps, and hipaa-scaffold for healthcare projects. Do NOT trigger for
  single bug fixes, small feature additions, or code review — those don't need the full
  CITADEL process.
user-invokable: true
---

# CITADEL Workflow — Secure-by-Default Application Development

## Intent

1. **Threat modeling requires human judgment** — automated scanners find known patterns, but identifying what could go wrong for THIS specific application requires a person who understands the domain
2. **Enforce step is mandatory, never skippable** — if time is short, reduce scope in Assemble; never skip the security audit to meet a deadline
3. **Testing completeness before deployment** — functional, security, and integration tests all pass; shipping untested code is shipping unknown risk
4. **Incident response ownership is defined before go-live** — "who gets paged" is answered before the first user hits production, not after the first outage
5. **Ship production-ready software that reduces rework** — the CITADEL process exists to build it right once, not to build it fast and fix it later
6. **Meet regulatory requirements systematically** — HIPAA, SOC 2, and compliance needs are addressed during design, not discovered during audit
7. **Maintain development velocity without sacrificing security** — Conceive in under 1 hour, Inventory in under 4 hours, total MVP in under 25 hours

> **Prerequisites:** Read `dev-standards` skill (or project's CLAUDE.md) for code quality
> and security rules that apply during every step of this workflow.

## CITADEL Overview

| Step | Phase | Purpose | Pairs with |
|------|-------|---------|------------|
| **C** | Conceive | Problem, users, threats, billing | — |
| **I** | Inventory | Data schema, security architecture, stack | `project-bootstrap` |
| **T** | Tie | Validate connections, secrets, config | — |
| **A** | Assemble | Build with layered security | `dev-standards` |
| **D** | Drill | Functional + security testing | — |
| **E** | Enforce | Pre-deployment security audit | `security-hardening` |
| **L** | Look | Monitoring, alerting, incident response | `security-hardening` |

**Key principle:** Never skip steps. The Enforce step is mandatory before any deployment.
If time-constrained, reduce scope in Assemble — don't skip Enforce.

---

## C — Conceive

**Purpose:** Know exactly what you're building AND how to secure it before touching code.

### Check Requirements First

Before starting any new feature, check `requirements/` for existing specs:
- Are there `proposed` or `approved` requirements that cover this work?
- If yes, reference the REQ ID and implement against that spec
- If no, create a new requirement file using the requirements template

### Seven Questions (all mandatory)

1. **What problem does this solve?** — One sentence. If you can't say it simply, you don't
   understand it yet.
2. **Who is this for?** — Specific user. "Sales team" or "Medicare plan admins." Not "everyone."
3. **What does success look like?** — Measurable outcome. "Dashboard loads in <2s with live
   metrics" not "it works."
4. **What are the constraints?** — Budget, timeline, tech stack, billing attribution.
5. **What sensitive data is involved?** 🔒 — Credentials, PII, payment data, API keys, PHI,
   AI prompts/responses.
6. **Who should NOT have access?** 🔒 — Unauthenticated users? Other tenants? Public internet?
7. **What could go wrong?** 🔒 — Data breach, unauthorized access, compliance violations,
   prompt injection.

### Security Requirements Checklist
```
[ ] All sensitive data types identified
[ ] Access control requirements defined (who sees/edits what)
[ ] Authentication method chosen (email/password, OAuth, SSO)
[ ] Compliance requirements listed (GDPR, HIPAA, SOC2)
[ ] Attack vectors identified (SQLi, XSS, SSRF, prompt injection)
[ ] Data retention policy defined
[ ] Audit logging needs determined
[ ] AI security planned (if building AI features)
```

### Output: App Brief

```markdown
## App Brief
- **Problem:** [One sentence]
- **User:** [Who specifically]
- **Success:** [Measurable outcome]
- **Constraints:** [List]
- **Sensitive Data:** [What needs protection]
- **Access Control:** [Who can access what]
- **Threat Model:** [Key attack vectors]
- **Compliance:** [Regulatory requirements]
- **AI Usage:** [If applicable — what for, what risks]
- **Project Code:** [Billing code for .claude/project-code.txt]
```

---

## I — Inventory

**Purpose:** Design security BEFORE building. This is where most insecure apps fail.

### Data Schema

Define your source of truth WITH security constraints. See `references/schema-patterns.md`
for secure schema examples with:
- Row Level Security (RLS) on all user-data tables
- CHECK constraints for validation at database level
- Length limits to prevent DoS
- Proper foreign key relationships with CASCADE rules
- Email/format regex validation
- Non-negative value constraints

### Security Architecture

For every project, fill in this table:

| Component | Mechanism | Implementation |
|-----------|-----------|----------------|
| Authentication | [method] | [specific tool] |
| Authorization | [method] | [RLS, RBAC, ABAC] |
| API Security | [method] | [keys, CORS, rate limits] |
| Input Validation | [method] | [Zod, Joi, Pydantic] |
| Data Encryption | [at rest + transit] | [TLS 1.3 + DB encryption] |
| Rate Limiting | [strategy] | [per-IP, per-user thresholds] |
| Error Handling | [strategy] | [generic user msgs, detailed server logs] |
| Secrets Management | [method] | [.env, vault, cloud secrets] |
| Zero-Trust | [approach] | [auth + authz on every request] |

### Zero-Trust Model

Read `references/zero-trust-patterns.md` for implementation patterns including:
- Middleware examples (JWT verification + account status + permission check + audit log)
- mTLS between internal services
- Field-level encryption for PII

### Integrations Map

List every external connection with: Service, Purpose, Auth Type, Key Storage, Rotation
Policy, MCP availability. See `references/integration-security.md` for the template and
security requirements.

### Technology Stack

Propose stack based on requirements. Refer to `project-bootstrap` skill's
`references/stack-defaults.md` for opinionated defaults. User approves before proceeding.

### Edge Cases + Attack Scenarios

Document both operational edge cases (API limits, token expiry, timeouts) and security
attack scenarios. See `references/attack-scenarios.md` for the standard threat catalog
(SQLi, XSS, CSRF, brute force, session hijack, privilege escalation, prompt injection,
supply chain).

---

## T — Tie

**Purpose:** Validate all connections SECURELY before building.

### Repository Security Inspection
Before running `claude` on any cloned or forked repository, inspect for supply-chain risks:
```
[ ] Read .claude/ directory contents — check CLAUDE.md, settings.json, commands/ for
    unexpected shell commands, hook overrides, or permission escalations
[ ] Verify settings.json does not grant blanket Bash permissions or disable hooks
[ ] Check for post-checkout / pre-commit hooks that download or execute remote code
[ ] If .claude/ contains anything suspicious, remove it and configure from scratch
```
> **Why:** CVE-2025-59536 and CVE-2026-21852 demonstrated RCE via malicious `.claude/`
> directories in cloned repos. Never trust upstream AI config without inspection.

### Connection Validation
```
[ ] Database connection tested
[ ] All API keys verified AND stored in .env
[ ] .env file in .gitignore (CRITICAL — verify before first commit)
[ ] MCP servers responding
[ ] OAuth flows working end-to-end
[ ] Environment variables set correctly
[ ] Rate limits understood and documented
[ ] HTTPS endpoints verified (no HTTP)
```

### Secret Management Validation
```
[ ] Every secret in .env (not in code)
[ ] .env in .gitignore
[ ] No secrets in git history (grep -r "sk-" . --exclude-dir=node_modules)
[ ] Each service has its own API key (independent rotation)
[ ] Test key rotation process before going live
```

For enterprise secrets management (AWS Secrets Manager, GCP Secret Manager, Azure Key
Vault), see `references/enterprise-secrets.md`.

### Output
- All connections validated and documented
- Secrets securely stored and verified
- No leaked credentials in code or git history

---

## A — Assemble

**Purpose:** Build with layered security. Follow the `dev-standards` skill (or CLAUDE.md)
for all code quality and security rules during this phase.

### Architecture Layers

Build in this order — each layer adds security:

1. **Database** — Schema with RLS, constraints, encryption
2. **API/Backend** — Input validation, auth middleware, parameterized queries
3. **Business Logic** — Authorization checks, rate limiting, audit logging
4. **Frontend** — XSS prevention, CSP, secure session handling
5. **Integration** — SSRF protection, timeout handling, certificate validation

### Build Order (Security First)
```
1. Database schema + RLS policies + seed data
2. Authentication flow (signup → login → session → refresh → logout)
3. Authorization middleware (role checks on every route)
4. Core API endpoints with input validation
5. Frontend pages with secure data fetching
6. Integration connections with error handling
7. AI features with input/output security (if applicable)
```

### API Security Hardening

For API-heavy applications, read `references/api-security.md` for:
- API versioning strategy
- Request signing
- GraphQL-specific security (depth limiting, query complexity)
- Webhook security (signature verification)
- Rate limiting tiers

### AI Feature Security

If building AI-powered features, read `references/ai-security.md` for:
- Prompt injection defense
- Input sanitization before AI processing
- Output validation after AI generation
- Cost controls and rate limiting
- Abuse detection patterns

---

## D — Drill

**Purpose:** Test functionality AND security.

### Testing Layers
1. **Functional** — Does it work? Happy path + error handling
2. **Security** — Can it be broken? Injection, auth bypass, privilege escalation
3. **Integration** — Do the pieces work together?
4. **Edge cases** — What happens with bad input, timeouts, concurrent access?

### Security Testing Checklist
Read `references/security-testing.md` for the complete checklist covering:
- Authentication testing (brute force, session fixation, token manipulation)
- Authorization testing (horizontal/vertical privilege escalation, IDOR)
- Input validation testing (SQLi, XSS, path traversal, command injection)
- API security testing (rate limits, CORS, missing auth)
- Business logic testing (race conditions, parameter tampering)

### Performance vs Security

Read `references/perf-security-balance.md` for guidance on:
- When to cache auth checks (and when NOT to)
- Rate limiting without degrading UX
- Encryption overhead management
- CDN security considerations

---

## E — Enforce (Mandatory Pre-Deployment)

**⚠️ DO NOT DEPLOY until this passes.**

Hand off to the `security-hardening` skill for the full audit. At minimum:

```
[ ] Secrets audit — no secrets in code or git history
[ ] Dependency audit — no critical/high vulnerabilities
[ ] Code security review — input validation, parameterized queries, output encoding
[ ] Auth audit — strong passwords, lockout, secure sessions, RLS
[ ] Data protection — encryption at rest + transit, no PII in logs
[ ] Security scanning — npm audit/pip-audit, gitleaks, semgrep
[ ] Infrastructure — if cloud: IaC scanning, least privilege IAM, no public buckets
```

### Output: Security Review Document
Generate the security review report. See `security-hardening` skill for the template.

---

## L — Look (Mandatory for Live Apps)

Hand off to the `security-hardening` skill for monitoring setup and incident response.
At minimum:

```
[ ] Failed auth attempts tracked and alerted
[ ] Rate limit hits monitored
[ ] API error rate baseline established
[ ] Admin action audit trail active
[ ] Incident response playbook documented
[ ] On-call rotation established (even if it's just you)
```

---

## Anti-Patterns

These mistakes lead to breaches:

**Development:** Building before designing. Skipping connection validation. No data modeling.
No testing. Hardcoding secrets.

**Security:** "We'll add security later." Using `*` CORS in production. Storing passwords
in plaintext. Trusting client-side validation. Logging sensitive data. Using HTTP in
production. Skipping the Enforce step. No monitoring. Default credentials. Disabling
security features to "make it work."

---

## Related Skills

- `project-bootstrap` — Scaffolding and project structure
- `dev-standards` — Code quality and security rules (or use CLAUDE.md)
- `security-hardening` — Enforce + Look steps, security audit
- `hipaa-scaffold` — HIPAA compliance layer for healthcare
- `servicetitan-analysis` — Operational analytics via MCP
