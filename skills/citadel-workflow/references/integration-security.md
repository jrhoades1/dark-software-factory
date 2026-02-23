# Integration Security Requirements

Reference for the CITADEL Inventory and Tie steps. Every external service connection
must be documented with its security posture.

## Integration Map Template

Fill this in during the Inventory step for every external service:

| Service | Purpose | Auth Type | Key Storage | Rotation Policy | BAA Required | MCP Available |
|---------|---------|-----------|-------------|-----------------|-------------|---------------|
| PostgreSQL | Primary DB | Password | .env | 90 days | If PHI | N/A |
| Supabase | Auth + DB | API key | .env | On demand | If PHI | Yes |
| Stripe | Payments | API key | .env | Annually | No | No |
| OpenAI/Anthropic | AI features | API key | .env | On demand | If PHI | Yes |
| SendGrid | Email | API key | .env | 90 days | If PHI content | No |
| AWS S3 | File storage | IAM role | Instance role | Auto-rotated | If PHI | No |
| GitHub | Source control | OAuth/PAT | .env | 90 days | No | Yes |

---

## Security Requirements Per Integration

### Databases

```
[ ] Connection uses SSL/TLS (sslmode=require)
[ ] Connection string in .env (never in code)
[ ] Database user has minimal permissions (no SUPERUSER)
[ ] Connection pooling configured (prevent exhaustion)
[ ] Idle connection timeout set
[ ] Query timeout configured (prevent long-running queries)
[ ] Separate read/write users where possible
```

### Third-Party APIs

```
[ ] API key stored in .env
[ ] Rate limits documented and respected
[ ] Retry logic with exponential backoff
[ ] Timeout configured on all requests (default: 30s)
[ ] Response validation (don't trust external data)
[ ] Error responses don't leak API keys in logs
[ ] Fallback behavior defined (what happens when API is down?)
```

### Webhook Receivers

```
[ ] Signature verification on all incoming webhooks
[ ] Replay protection (check timestamp, reject if >5 min old)
[ ] Idempotency handling (same webhook delivered twice)
[ ] IP allowlisting where provider publishes IP ranges
[ ] Rate limiting on webhook endpoint
[ ] Async processing (return 200 immediately, process later)
```

### OAuth Integrations

```
[ ] PKCE flow used (not implicit grant)
[ ] State parameter for CSRF protection
[ ] Token stored server-side (not in browser localStorage)
[ ] Refresh token rotation enabled
[ ] Scope limited to minimum needed
[ ] Token revocation on disconnect
```

---

## Connection Validation Checklist (Tie Step)

Run this before writing any business logic:

```bash
# Database connectivity
psql $DATABASE_URL -c "SELECT 1;"

# API key validity
curl -H "Authorization: Bearer $API_KEY" https://api.service.com/health

# OAuth flow end-to-end
# Test: login → callback → token → refresh → revoke

# Webhook delivery
# Test: trigger event → verify signature → confirm processing
```

```
[ ] Each connection tested independently
[ ] Error handling verified (what happens when it's down?)
[ ] Rate limits tested (trigger a 429, verify backoff works)
[ ] Timeout behavior verified
[ ] All secrets confirmed in .env and .gitignore
```

---

## Common Integration Security Mistakes

| Mistake | Risk | Fix |
|---------|------|-----|
| Sharing API keys across services | One compromise = all compromised | Unique key per service |
| No timeout on external calls | Hanging requests exhaust resources | Set 30s timeout |
| Logging full request/response | Secrets in logs | Redact auth headers |
| Trusting external API responses | Injection via API response | Validate all external data |
| No fallback for API downtime | Cascading failures | Circuit breaker pattern |
| Storing OAuth tokens in localStorage | XSS = token theft | Server-side storage only |

---

## MCP Server Integration

For projects using Model Context Protocol (MCP) servers:

```
[ ] MCP server runs locally or in trusted environment
[ ] Tools have explicit permission boundaries
[ ] API keys passed via environment, not in prompts
[ ] Rate limiting on MCP tool invocations
[ ] Audit logging of all MCP tool calls
[ ] Read-only tools where possible (principle of least privilege)
```
