# Alert Thresholds & Monitoring Configuration

Reference for the security-hardening Look step. Configure these alerts before
going to production.

## Severity Definitions

| Severity | Response Time | Action | Notification |
|----------|---------------|--------|-------------|
| **CRITICAL** | Immediate (15 min) | Page on-call, start incident response | Phone + SMS + Slack |
| **HIGH** | 1 hour | Investigate immediately during business hours | Slack + email |
| **MEDIUM** | 4 hours | Investigate during business hours | Slack |
| **LOW** | 24 hours | Review in next triage | Dashboard only |

---

## Authentication Alerts

| Metric | Threshold | Severity | Description |
|--------|-----------|----------|-------------|
| Failed logins (single user) | 5 in 5 min | HIGH | Brute force attempt on account |
| Failed logins (single IP) | 20 in 5 min | HIGH | Credential stuffing from IP |
| Failed logins (global) | 100 in 5 min | CRITICAL | Large-scale credential attack |
| Admin login from new IP | Any | HIGH | Verify with admin |
| Admin login from new country | Any | CRITICAL | Likely compromised |
| Account lockouts | 10 in 15 min | HIGH | Possible targeted attack |
| Password reset spike | 5x baseline in 1 hour | MEDIUM | Possible phishing campaign |

---

## Authorization Alerts

| Metric | Threshold | Severity | Description |
|--------|-----------|----------|-------------|
| 403 responses (single user) | 10 in 5 min | HIGH | Privilege escalation attempt |
| RLS violation | Any | CRITICAL | Cross-tenant access attempt |
| Admin endpoint from non-admin | Any | HIGH | Authorization bypass attempt |
| Role change | Any | MEDIUM | Audit all role changes |

---

## API Alerts

| Metric | Threshold | Severity | Description |
|--------|-----------|----------|-------------|
| Error rate (5xx) | >5% for 5 min | HIGH | Service degradation |
| Error rate (5xx) | >20% for 2 min | CRITICAL | Service failure |
| Response time p95 | >2s for 10 min | MEDIUM | Performance degradation |
| Response time p95 | >10s for 5 min | HIGH | Service near-failure |
| Rate limit hits | >50/min for single IP | MEDIUM | Possible abuse |
| Rate limit hits (global) | >500/min | HIGH | DDoS or bot attack |
| Request size anomaly | >10MB single request | MEDIUM | Possible DoS |

---

## Data Alerts

| Metric | Threshold | Severity | Description |
|--------|-----------|----------|-------------|
| Bulk data export | >1000 records in 1 request | HIGH | Possible data exfiltration |
| Database query time | >30s | MEDIUM | Possible DoS via query |
| Storage usage spike | >20% growth in 24h | MEDIUM | Investigate cause |
| PII access volume | >100 records/hour per user | HIGH | Unusual access pattern |

---

## Infrastructure Alerts

| Metric | Threshold | Severity | Description |
|--------|-----------|----------|-------------|
| CPU usage | >80% for 15 min | MEDIUM | Scaling needed |
| CPU usage | >95% for 5 min | HIGH | Service at risk |
| Memory usage | >85% for 10 min | MEDIUM | Memory leak or scaling |
| Disk usage | >80% | MEDIUM | Provision more storage |
| Disk usage | >95% | CRITICAL | Imminent failure |
| SSL certificate expiry | <30 days | MEDIUM | Renew certificate |
| SSL certificate expiry | <7 days | CRITICAL | Renew immediately |

---

## Monitoring Stack Configuration

### Datadog

```yaml
# datadog-monitors.yaml
monitors:
  - name: "High Error Rate"
    type: metric alert
    query: "avg(last_5m):sum:http.requests.errors{env:production}.as_rate() / sum:http.requests.total{env:production}.as_rate() > 0.05"
    message: |
      Error rate exceeded 5% for 5 minutes.
      @slack-engineering @pagerduty-oncall
    tags:
      - severity:high
      - team:engineering

  - name: "Failed Auth Spike"
    type: metric alert
    query: "sum(last_5m):sum:auth.login.failed{env:production} > 100"
    message: |
      Over 100 failed logins in 5 minutes. Possible credential attack.
      @slack-security @pagerduty-oncall
    tags:
      - severity:critical
      - team:security

  - name: "Slow Responses"
    type: metric alert
    query: "avg(last_10m):avg:http.response_time.p95{env:production} > 2000"
    message: |
      P95 response time exceeded 2s for 10 minutes.
      @slack-engineering
    tags:
      - severity:medium
```

### Grafana + Prometheus

```yaml
# prometheus-rules.yaml
groups:
  - name: security
    rules:
      - alert: HighFailedLogins
        expr: sum(rate(auth_login_failed_total[5m])) > 20
        for: 2m
        labels:
          severity: high
        annotations:
          summary: "High failed login rate"
          description: "{{ $value }} failed logins/sec in last 5 minutes"

      - alert: ErrorRateSpike
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "API error rate above 5%"

      - alert: SSLCertExpiringSoon
        expr: (probe_ssl_earliest_cert_expiry - time()) / 86400 < 30
        labels:
          severity: medium
        annotations:
          summary: "SSL cert expires in {{ $value }} days"
```

### CloudWatch (AWS)

```json
{
    "MetricAlarms": [{
        "AlarmName": "HighErrorRate",
        "Namespace": "CustomApp",
        "MetricName": "5xxErrorRate",
        "Statistic": "Average",
        "Period": 300,
        "EvaluationPeriods": 1,
        "Threshold": 5.0,
        "ComparisonOperator": "GreaterThanThreshold",
        "AlarmActions": ["arn:aws:sns:us-east-1:ACCOUNT:security-alerts"]
    }]
}
```

---

## Application-Level Metrics to Emit

Add these metrics to your application code:

```python
from prometheus_client import Counter, Histogram, Gauge

# Authentication
auth_login_total = Counter("auth_login_total", "Total login attempts", ["status"])
auth_login_failed = Counter("auth_login_failed_total", "Failed login attempts", ["reason"])
auth_lockout_total = Counter("auth_lockout_total", "Account lockouts")

# API
http_request_duration = Histogram(
    "http_request_duration_seconds",
    "Request duration",
    ["method", "endpoint", "status"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# Security events
security_events = Counter(
    "security_events_total",
    "Security events",
    ["event_type"],  # rls_violation, auth_bypass_attempt, rate_limit_hit
)

# Data access
data_access_total = Counter(
    "data_access_total",
    "Data access events",
    ["resource_type", "action"],  # users/read, patients/export
)
```

---

## Dashboard Essentials

Every production app needs at minimum:

1. **Request rate** — Total requests/sec (spot traffic anomalies)
2. **Error rate** — 4xx and 5xx rates (spot attacks and failures)
3. **Response time** — p50, p95, p99 (spot degradation)
4. **Auth events** — Logins, failures, lockouts (spot credential attacks)
5. **Active users** — Concurrent sessions (spot unusual patterns)
6. **Resource usage** — CPU, memory, disk, connections (spot exhaustion)
