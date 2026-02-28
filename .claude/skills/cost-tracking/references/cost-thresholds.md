# Cost Alert Thresholds

Configurable alert thresholds for expense monitoring. Follows the same severity
model as `security-hardening/references/alert-thresholds.md`.

## Severity Definitions (Cost Context)

| Severity | Response | Action | Notification |
|----------|----------|--------|-------------|
| **CRITICAL** | Immediate | Hard block on API requests | Email + in-app banner |
| **HIGH** | 1 hour | Warn user, prepare to block | Email + in-app banner |
| **MEDIUM** | Next session | Display warning in dashboard | In-app banner only |
| **LOW** | Informational | Log for review | Dashboard metric only |

---

## AI API Cost Alerts

| Metric | Default Threshold | Severity | Action |
|--------|-------------------|----------|--------|
| Monthly AI spend per user | 80% of `monthly_ai_cap_usd` | MEDIUM | Show warning banner on dashboard |
| Monthly AI spend per user | 95% of `monthly_ai_cap_usd` | HIGH | Show persistent banner + email notification |
| Monthly AI spend per user | 100% of `monthly_ai_cap_usd` | CRITICAL | Block AI requests, return HTTP 429 |
| Single AI call cost | > `single_call_alert_usd` (default $0.50) | LOW | Flag in `ai_generations` audit log |
| Daily AI spend | > 30% of monthly cap in one day | HIGH | Possible runaway usage |
| AI error rate | > 20% of calls failing in 1 hour | MEDIUM | Wasting money on failed calls |

---

## Hosted Service Alerts

| Service | Metric | Default Threshold | Severity | Action |
|---------|--------|-------------------|----------|--------|
| Supabase | DB size | 80% of tier limit (400MB free) | MEDIUM | Dashboard warning |
| Supabase | DB size | 95% of tier limit (475MB free) | HIGH | Email + dashboard warning |
| Supabase | Bandwidth | 80% of tier limit | MEDIUM | Dashboard warning |
| Supabase | Storage | 80% of tier limit (800MB free) | MEDIUM | Dashboard warning |
| Vercel | Serverless minutes | 80% of tier limit | MEDIUM | Dashboard warning |
| Vercel | Bandwidth | 80% of tier limit | MEDIUM | Dashboard warning |
| Clerk | MAU count | 80% of tier limit | LOW | Dashboard metric |

---

## Default Configuration

```sql
-- Insert default cost config for new users
INSERT INTO cost_config (clerk_user_id, monthly_ai_cap_usd, alert_threshold_pct, single_call_alert_usd)
VALUES ($1, 10.00, 80, 0.50);
```

| Setting | Default | Description |
|---------|---------|-------------|
| `monthly_ai_cap_usd` | $10.00 | Hard cap on AI API spend per calendar month |
| `alert_threshold_pct` | 80 | Percentage of cap that triggers warning |
| `single_call_alert_usd` | $0.50 | Flag individual calls above this amount |
| `block_on_cap` | true | Whether to hard-block or just warn at cap |
| `email_on_high` | true | Send email for HIGH severity alerts |

---

## Customization

Users should be able to adjust these thresholds via the admin dashboard:

- **Monthly cap:** Slider or input, $1-$100 range, default $10
- **Alert threshold:** 50%-95% range, default 80%
- **Single call alert:** $0.10-$5.00 range, default $0.50
- **Block behavior:** Toggle between hard block and warn-only

---

## Alert Resolution

Alerts in `expense_alerts` should be resolvable:

| Resolution | Meaning |
|-----------|---------|
| `acknowledged` | User saw the alert and chose to continue |
| `cap_increased` | User raised their monthly cap |
| `auto_resolved` | New billing period started |
| `investigated` | Admin reviewed the usage pattern |
