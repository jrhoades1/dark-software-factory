# Security Testing Checklist

Reference for the CITADEL Drill step. Test functionality AND security together.

## Authentication Testing

```
[ ] Login with valid credentials → success
[ ] Login with wrong password → 401, generic error message
[ ] Login with nonexistent email → 401, same generic error (no user enumeration)
[ ] Login after 5 failures → account locked for 15 minutes
[ ] Login with locked account → 423, no timing leak
[ ] Login with deactivated account → 403
[ ] JWT with expired token → 401
[ ] JWT with invalid signature → 401
[ ] JWT with "none" algorithm → 401 (algorithm confusion attack)
[ ] JWT with modified claims → 401
[ ] Missing Authorization header → 401
[ ] Malformed Authorization header → 401
[ ] Password reset with valid email → email sent, success message
[ ] Password reset with invalid email → same success message (no enumeration)
[ ] Password reset token reuse → rejected
[ ] Password reset with expired token → rejected
[ ] Session invalidation on password change → all other sessions terminated
[ ] Concurrent sessions handling → defined behavior (limit or allow)
```

## Authorization Testing

```
[ ] User A cannot access User B's resources → 404 (not 403)
[ ] User cannot access admin endpoints → 403
[ ] User cannot elevate own role via API → rejected
[ ] Deleted resource returns 404 (not leaked via error messages)
[ ] Mass assignment blocked (can't set role/admin via body)
[ ] RLS verified: direct DB query respects policies
[ ] Org-scoped data: User in Org A cannot see Org B data
[ ] API key with limited scope cannot access other scopes
```

### IDOR Testing (Insecure Direct Object Reference)
```bash
# As User A, get a resource ID
GET /api/documents/abc123  → 200

# As User B, try the same ID
GET /api/documents/abc123  → 404 (not 403)

# Try sequential IDs
GET /api/documents/1
GET /api/documents/2
GET /api/documents/3
# All should return 404 for non-owned resources
```

## Input Validation Testing

### SQL Injection
```
Input: ' OR '1'='1
Input: '; DROP TABLE users; --
Input: ' UNION SELECT password FROM users --
Input: 1; WAITFOR DELAY '00:00:05' --

All must return 400 (bad input) or be safely parameterized.
```

### XSS
```
Input: <script>alert(1)</script>
Input: <img src=x onerror=alert(1)>
Input: javascript:alert(1)
Input: "><script>alert(document.cookie)</script>

All must be encoded/escaped in output. None should execute.
```

### Path Traversal
```
Input: ../../../etc/passwd
Input: ....//....//etc/passwd
Input: %2e%2e%2f%2e%2e%2f
Input: ..%00.txt

All must be rejected or resolved within safe base directory.
```

### Command Injection
```
Input: ; ls -la
Input: | cat /etc/passwd
Input: $(whoami)
Input: `id`

All must be rejected. Never interpolate user input into shell commands.
```

## API Security Testing

```
[ ] Rate limiting works (flood endpoint, expect 429)
[ ] CORS rejects non-whitelisted origins in production
[ ] HTTP methods restricted (OPTIONS, PUT, DELETE only where intended)
[ ] Content-Type enforced (reject non-JSON on JSON endpoints)
[ ] Request body size limit enforced (default 1MB)
[ ] URL length limit enforced (default 2048 chars)
[ ] Pagination enforced (can't request 999999 items)
[ ] Slow query protection (timeout on expensive operations)
[ ] Error responses don't leak stack traces in production
[ ] Error responses don't leak database schema
[ ] API versioning works (v1 vs v2 isolation)
```

## Business Logic Testing

```
[ ] Race conditions handled (double-submit, concurrent updates)
[ ] Negative values rejected (negative price, negative quantity)
[ ] Integer overflow handled (max values for numeric fields)
[ ] State machine transitions enforced (can't skip steps)
[ ] Idempotency on critical operations (retry-safe)
[ ] Time-of-check-to-time-of-use (TOCTOU) prevented
```

### Race condition test
```bash
# Send 10 concurrent identical requests
for i in $(seq 1 10); do
    curl -X POST http://localhost:3000/api/transfer \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"amount": 100, "to": "recipient"}' &
done
wait
# Verify: exactly 1 transfer processed, not 10
```

## Security Header Testing

```bash
curl -I https://yourapp.com/

# Verify these headers exist:
# Strict-Transport-Security: max-age=31536000; includeSubDomains
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY
# Content-Security-Policy: default-src 'self'; ...
# X-XSS-Protection: 0  (disabled — CSP is the modern replacement)
# Referrer-Policy: strict-origin-when-cross-origin
# Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## Automated Security Scanning

Run these in CI on every PR:

```bash
# Dependency audit
npm audit --audit-level=high    # JS
pip-audit --strict               # Python

# Static analysis
semgrep --config=auto --error .
bandit -r src/ -f json           # Python

# Secret scanning
gitleaks detect --redact

# Container scanning (if applicable)
trivy image --severity HIGH,CRITICAL $IMAGE
```

## Test Results Template

```markdown
# Security Test Results — [Date]

## Summary
- Tests run: [N]
- Passed: [N]
- Failed: [N]
- Skipped: [N]

## Failed Tests
| Test | Expected | Actual | Severity | Fix |
|------|----------|--------|----------|-----|

## Scan Results
| Scanner | Clean? | Issues | Notes |
|---------|--------|--------|-------|
| npm audit | | | |
| semgrep | | | |
| gitleaks | | | |
| bandit | | | |
```
