# Incident Response Playbook

5-phase incident response process. Every live application needs this documented
and tested BEFORE an incident occurs.

## Phase 1: Detection (0–15 minutes)

### Automated detection triggers

| Signal | Source | Severity |
|--------|--------|----------|
| 10+ failed logins from same IP in 5 min | Auth logs | HIGH |
| Admin account login from new IP/country | Auth logs | CRITICAL |
| 5x spike in API error rate | Monitoring | HIGH |
| Database query to user table without app context | DB audit logs | CRITICAL |
| Secret detected in git push | Pre-commit/CI | CRITICAL |
| Dependency with known CVE deployed | Container scan | HIGH |
| Unusual data export volume | Application logs | HIGH |
| RLS policy violation attempt | Database logs | CRITICAL |

### Manual detection indicators

- Customer reports seeing another customer's data
- Unexpected password reset emails
- API responses containing data from wrong tenant
- Unexplained resource usage spike
- New admin account that nobody created

### Severity classification

| Level | Description | Response time | Example |
|-------|-------------|---------------|---------|
| **CRITICAL** | Active breach, data exposure | Immediate (15 min) | Unauthorized DB access, leaked credentials |
| **HIGH** | Likely breach, needs investigation | 1 hour | Brute force success, suspicious admin activity |
| **MEDIUM** | Potential vulnerability exploited | 4 hours | Rate limit bypass, unusual traffic patterns |
| **LOW** | Security misconfiguration found | 24 hours | Missing headers, verbose error messages |

---

## Phase 2: Containment (15–60 minutes)

### Immediate containment (first 15 minutes)

```
[ ] Identify compromised accounts/systems
[ ] Revoke compromised credentials immediately
[ ] Block attacker IP(s) at WAF/firewall level
[ ] Disable compromised API keys
[ ] Force password reset on affected accounts
[ ] Enable enhanced logging on affected systems
```

### Short-term containment (15–60 minutes)

```
[ ] Isolate affected services (network segmentation)
[ ] Rotate all secrets that may be compromised
[ ] Deploy emergency patches if vulnerability is known
[ ] Take forensic snapshots BEFORE making changes
[ ] Preserve all log files (copy to secure, immutable storage)
[ ] Notify incident response team
```

### Evidence preservation

```bash
# Snapshot current state before containment changes
pg_dump $DATABASE_URL > incident_$(date +%Y%m%d_%H%M%S).sql

# Copy application logs
cp -r /var/log/app/ /secure-storage/incident-$(date +%Y%m%d)/

# Capture network state
ss -tlnp > /secure-storage/incident-$(date +%Y%m%d)/network_state.txt

# Docker container state
docker ps -a > /secure-storage/incident-$(date +%Y%m%d)/containers.txt
docker logs $(docker ps -q) > /secure-storage/incident-$(date +%Y%m%d)/docker_logs.txt
```

---

## Phase 3: Eradication (1–24 hours)

### Root cause analysis

```
[ ] How did the attacker get in? (attack vector)
[ ] What vulnerability was exploited?
[ ] How long has the attacker had access? (dwell time)
[ ] What data was accessed/exfiltrated?
[ ] Are there other compromised accounts/systems?
[ ] Were any backdoors installed?
```

### Eradication steps

```
[ ] Patch the vulnerability that was exploited
[ ] Remove any backdoors or unauthorized access
[ ] Rotate ALL credentials (not just compromised ones)
[ ] Update and patch all affected systems
[ ] Re-deploy from known-good source (not from compromised server)
[ ] Verify fix with security testing
```

### Credential rotation checklist

```
[ ] Database passwords
[ ] API keys (all third-party services)
[ ] JWT signing secrets
[ ] OAuth client secrets
[ ] SSH keys
[ ] Service account credentials
[ ] Encryption keys (if compromised, re-encrypt data)
[ ] Session tokens (force all users to re-authenticate)
```

---

## Phase 4: Recovery (1–48 hours)

### Service restoration

```
[ ] Deploy patched/clean version
[ ] Verify all security controls are active
[ ] Run full security scan before going live
[ ] Monitor closely for 48 hours post-recovery
[ ] Enable enhanced logging temporarily
[ ] Verify data integrity
```

### Verification checklist

```
[ ] All known vulnerabilities patched
[ ] All credentials rotated
[ ] RLS policies verified
[ ] Auth flows tested
[ ] Rate limiting active
[ ] Monitoring and alerting active
[ ] No unauthorized accounts exist
[ ] No unauthorized API keys exist
```

### Communication timeline

| When | Who | What |
|------|-----|------|
| 0–1 hour | Internal team | Initial alert, severity, containment status |
| 1–4 hours | Management | Impact assessment, recovery estimate |
| 4–24 hours | Affected users | If data was exposed (see ir-templates.md) |
| 24–72 hours | Regulators | If required (HIPAA: 60 days, GDPR: 72 hours) |
| 1–2 weeks | Public | If warranted (public-facing breach) |

---

## Phase 5: Post-Incident (1–2 weeks after)

### Post-mortem (blameless)

Schedule within 48 hours of recovery. Document:

```markdown
## Incident Post-Mortem — [Date]

### Timeline
- [Time] First detection signal
- [Time] Incident confirmed
- [Time] Containment started
- [Time] Root cause identified
- [Time] Eradication complete
- [Time] Service restored
- [Time] All-clear declared

### Root Cause
[What vulnerability was exploited and how]

### Impact
- Users affected: [N]
- Data exposed: [description]
- Downtime: [duration]
- Financial impact: [estimate]

### What Went Well
- [List what worked in the response]

### What Needs Improvement
- [List what didn't work or was too slow]

### Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|

### Lessons Learned
- [Key takeaways that should change process/technology]
```

### Hardening actions

```
[ ] Vulnerability class addressed (not just the specific instance)
[ ] Additional monitoring for the attack vector
[ ] Updated runbooks/playbooks with lessons learned
[ ] Team training on the incident type
[ ] Penetration test scheduled to verify fix
[ ] Insurance/legal notified if applicable
```

---

## On-Call Basics

Even for solo developers, establish:

1. **Alerting channel** — PagerDuty, Opsgenie, or phone notifications
2. **Runbook location** — This playbook, accessible offline
3. **Emergency contacts** — Cloud provider support, legal counsel, PR
4. **Break-glass access** — How to access systems in an emergency
5. **Communication channel** — Where the team coordinates (Slack, Signal)
