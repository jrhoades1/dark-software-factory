# Incident Response Communication Templates

Pre-written templates for incident communication. Customize and send — don't
waste time wordsmithing during an active incident.

---

## Internal Alert — Initial Detection

**Subject:** [SEVERITY] Security Incident — [Brief Description]

```
SECURITY INCIDENT ALERT
Severity: [CRITICAL / HIGH / MEDIUM]
Time detected: [YYYY-MM-DD HH:MM UTC]
Detected by: [monitoring system / manual report / customer report]

Summary:
[1-2 sentences: what happened, what's affected]

Current status:
- [ ] Investigating
- [ ] Contained
- [ ] Eradicated
- [ ] Recovered

Immediate actions taken:
- [Action 1]
- [Action 2]

Impact assessment:
- Services affected: [list]
- Users affected: [estimated count]
- Data at risk: [type of data]

Next steps:
- [What's happening next]
- [Who's responsible]

Incident commander: [Name]
War room: [Slack channel / Zoom link]
Next update: [Time]
```

---

## Internal Update — Ongoing Incident

**Subject:** UPDATE [N] — [SEVERITY] Security Incident — [Brief Description]

```
INCIDENT UPDATE #[N]
Time: [YYYY-MM-DD HH:MM UTC]
Status: [Investigating / Containing / Eradicating / Recovering]

Since last update:
- [What's been done]
- [What's been discovered]

Current understanding:
- Attack vector: [known / investigating]
- Root cause: [identified / investigating]
- Scope: [contained / expanding / unknown]

Remaining actions:
- [Action 1 — Owner — ETA]
- [Action 2 — Owner — ETA]

Next update: [Time]
```

---

## Management Briefing

**Subject:** Security Incident Briefing — [Date]

```
EXECUTIVE SUMMARY

What happened:
[2-3 sentences in plain language, no jargon]

Business impact:
- Service availability: [up / degraded / down]
- Customer data exposure: [none / possible / confirmed]
- Financial impact: [estimated range]
- Regulatory obligations: [notification required? timeline?]

Timeline:
- Detected: [time]
- Contained: [time]
- Resolved: [time or ETA]

Actions taken:
- [Key actions in business terms]

Recommendations:
- [Immediate: what we're doing now]
- [Short-term: what we need to do in the next 30 days]
- [Long-term: systemic improvements needed]

Questions? Contact: [Incident commander name and channel]
```

---

## Customer Notification — Data Breach

**Use when:** Customer data has been confirmed exposed.

**Subject:** Important Security Notice — Action Required

```
Dear [Customer Name],

We are writing to inform you of a security incident that may affect
your account.

WHAT HAPPENED
On [date], we discovered [brief, honest description of what happened].
We immediately [containment actions taken].

WHAT INFORMATION WAS INVOLVED
Based on our investigation, the following information may have been
accessed:
- [List specific data types: email address, name, etc.]
- [Be specific — don't be vague to seem less bad]

WHAT WAS NOT AFFECTED
- [Passwords were NOT exposed / were hashed with bcrypt]
- [Payment information was NOT stored in the affected system]
- [Other reassurances that are TRUE]

WHAT WE ARE DOING
- [Rotated all credentials]
- [Patched the vulnerability]
- [Enhanced monitoring]
- [Engaged security firm for audit]

WHAT YOU CAN DO
- Change your password at [link]
- Enable two-factor authentication at [link]
- Monitor your accounts for suspicious activity
- [If financial data: consider credit monitoring]

CONTACT US
If you have questions, contact our security team:
- Email: security@yourdomain.com
- Phone: [number]

We take the security of your data seriously and sincerely apologize
for this incident.

[Name]
[Title]
```

---

## Regulatory Notification — HIPAA Breach

**Use when:** PHI has been confirmed exposed. Required within 60 days of discovery.

**Subject:** HIPAA Breach Notification

```
[Organization Name]
[Address]
[Date]

U.S. Department of Health and Human Services
Office for Civil Rights
[Address]

RE: Notification of Breach of Unsecured Protected Health Information

Dear Sir/Madam,

Pursuant to Section 13402(a) of the HITECH Act and 45 CFR §164.408,
[Organization Name] hereby provides notification of a breach of
unsecured protected health information.

DATE OF BREACH: [Date range]
DATE OF DISCOVERY: [Date]
NUMBER OF INDIVIDUALS AFFECTED: [Count]

DESCRIPTION OF BREACH:
[Factual description of what happened]

TYPES OF PHI INVOLVED:
[List specific PHI elements: names, dates of birth, diagnoses,
treatment records, health plan numbers, etc.]

ACTIONS TAKEN:
[Containment and remediation steps]

INDIVIDUAL NOTIFICATION:
[Individuals were / will be notified on [date] by [method]]

CONTACT INFORMATION:
[Designated contact for questions]

Respectfully submitted,
[Name, Title]
[Organization]
```

**Note:** For breaches affecting 500+ individuals, also notify:
- Prominent media outlets in the affected state(s)
- Post on organization website for 90 days

---

## Regulatory Notification — GDPR Breach

**Use when:** EU personal data has been breached. Required within 72 hours.

```
DATA BREACH NOTIFICATION — GDPR Article 33

To: [Supervisory Authority]
From: [Data Controller / DPO]
Date: [YYYY-MM-DD]

1. Nature of the breach:
   [Description of the breach, categories of data, approximate number
   of data subjects affected]

2. Contact point:
   [DPO name, email, phone]

3. Likely consequences:
   [Potential impact on data subjects]

4. Measures taken:
   [Steps taken to address the breach and mitigate effects]

5. Notification to data subjects:
   [Whether individuals have been / will be notified, and timeline]
```

---

## All-Clear Notification

**Subject:** RESOLVED — Security Incident — [Brief Description]

```
INCIDENT RESOLVED
Time: [YYYY-MM-DD HH:MM UTC]
Duration: [total incident duration]

Resolution:
[What was done to resolve the incident]

Root cause:
[Brief description — full post-mortem to follow]

Impact summary:
- Users affected: [count]
- Data exposure: [none / details]
- Downtime: [duration]

Preventive measures:
- [What's being done to prevent recurrence]

Post-mortem scheduled: [date/time]

Thank you to everyone who assisted in the response.
```
