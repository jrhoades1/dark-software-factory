---
name: security-hardening
description: >
  Perform security audits and apply hardening to any application. Covers the CITADEL
  Enforce and Look steps: secrets audit, dependency scanning, code security review,
  auth hardening, data protection, infrastructure security, monitoring setup, and
  incident response. Use this skill when the user says "security audit," "pre-deployment
  check," "Enforce step," "Look step," "pen test prep," "harden," "vulnerability scan,"
  "dependency audit," "incident response," or "monitoring setup." Also trigger for
  SOC 2 prep, security questionnaires, OWASP compliance checks, or any request to
  "make this production-ready" or "is this secure." This skill works on existing
  projects — it audits and hardens, not scaffolds. For building new apps securely from
  scratch, use citadel-workflow instead.
---

# Security Hardening Skill

Audit existing applications for vulnerabilities and apply production hardening.
Implements the CITADEL Enforce (E) and Look (L) steps.

## When to use this skill

- Before any deployment to production
- When preparing for SOC 2, HIPAA, or compliance audits
- After a security incident (post-mortem hardening)
- When onboarding enterprise customers who require security reviews
- Periodic security health checks on running applications
- When the citadel-workflow skill hands off the Enforce or Look steps

## Audit execution order

Run these audits in sequence. Each produces pass/fail. ALL must pass before deployment.

---

## 1. Secrets Management Audit

Run the automated scan script if available, otherwise execute manually:

```bash
# Scan for secrets in code
grep -r "sk-" . --exclude-dir=node_modules --exclude-dir=.git
grep -r "password.*=" . --exclude-dir=node_modules --exclude-dir=.git
grep -r "AKIA" . --exclude-dir=node_modules --exclude-dir=.git
grep -r "ghp_" . --exclude-dir=node_modules --exclude-dir=.git

# Scan git history
git log --all -- .env
git log --all -- credentials.json

# Automated scanning
gitleaks detect
trufflehog filesystem . --only-verified
```

### Checklist
```
[ ] No secrets in source code
[ ] No secrets in git history
[ ] .env in .gitignore (verify: cat .gitignore | grep .env)
[ ] All API keys rotatable (not hardcoded)
[ ] Secrets not in error messages or logs
[ ] Automated secret scanning in CI/CD
[ ] Each service has independent API key
```

### If secrets found in git history
Keys are BURNED. Rotate immediately, scrub with BFG Repo-Cleaner, audit access logs.

For enterprise secrets management (AWS/GCP/Azure vaults), see `references/enterprise-secrets.md`.

---

## 2. Dependency Security

```bash
npm audit                   # JavaScript
pip-audit                   # Python
npm sbom --sbom-format=cyclonedx > sbom.json  # Generate SBOM
```

```
[ ] No critical/high vulnerabilities
[ ] Lock file committed
[ ] Exact versions pinned ("1.2.3" not "^1.2.3")
[ ] Unused dependencies removed
[ ] SBOM generated
[ ] Automated update PRs configured (Dependabot/Renovate)
```

---

## 3. Code Security Review

```
[ ] Input validation on ALL endpoints
[ ] Parameterized queries everywhere
[ ] Output encoding/sanitization
[ ] HTTPS enforced
[ ] CORS whitelist (not '*' in production)
[ ] Rate limiting on public endpoints
[ ] Auth on all protected routes
[ ] Authorization checks before data access
[ ] Secure sessions (httpOnly, secure, sameSite)
[ ] No eval() or dangerous functions
[ ] File upload restrictions (type, size, quarantine)
```

---

## 4. Auth & Authorization Audit

```
[ ] Strong password requirements (8+ chars, mixed)
[ ] Account lockout (5 failures = 15 min lockout)
[ ] Short-lived tokens with refresh rotation
[ ] Authorization on ALL protected routes
[ ] RLS enabled (verify: SELECT * FROM pg_policies;)
[ ] No default/weak credentials
[ ] Secure password reset (time-limited tokens)
[ ] MFA for high-value accounts
[ ] Token rotation on privilege escalation
[ ] Secure cookie attributes (HttpOnly, Secure, SameSite=Strict)
```

---

## 5. Data Protection

```
[ ] Encryption at rest (database encryption enabled)
[ ] TLS 1.3 in transit
[ ] No PII in logs
[ ] Data retention policy defined
[ ] Backup strategy tested
[ ] Privacy policy published (if collecting user data)
```

For GDPR: data export, deletion, consent management.
For HIPAA: defer to `hipaa-scaffold` skill.

---

## 6. Security Scanning

```bash
# Static analysis
semgrep --config=auto .
bandit -r .                 # Python

# Secret scanning
gitleaks detect

# Container security
trivy image image-name

# Infrastructure as Code
checkov -d .                # Terraform/CF/K8s
```

---

## 7. Infrastructure Security

See `references/infrastructure-checklist.md` for:
- Cloud security checklist (IAM, S3, VPC, audit logging)
- Container hardening (minimal images, non-root, multi-stage builds)
- Secure Dockerfile template

---

## 8. Security Review Report Template

```markdown
# Security Review — [App Name]
Date: [YYYY-MM-DD] | Reviewer: [name]

## Vulnerabilities Found
| ID | Severity | Description | Location |

## Vulnerabilities Fixed
| ID | Fix Applied | Verified |

## Accepted Risks
| Risk | Justification | Mitigations | Review Date |

## Tools Run
| Tool | Result | Date |

## Deployment Readiness
- [ ] All critical/high resolved
- [ ] All scans clean
- [ ] Secrets audit passed
- [ ] Auth audit passed
- [ ] Monitoring configured
```

---

## 9. Monitoring Setup (Look Step)

### Metrics to track
- Failed auth attempts (by IP, by user, rate over time)
- Authorization failures
- Rate limit hits
- API error rate spikes
- Admin action audit trail
- Secret access logs

### Alert thresholds
Read `references/alert-thresholds.md` for CRITICAL/HIGH/MEDIUM definitions and
example alert configurations for Datadog, Grafana, and CloudWatch.

---

## 10. Incident Response

5-phase playbook: Detection → Containment → Eradication → Recovery → Post-Incident.
Read `references/ir-playbook.md` for the full playbook with timelines and
`references/ir-templates.md` for communication templates (internal + external breach
notification).
