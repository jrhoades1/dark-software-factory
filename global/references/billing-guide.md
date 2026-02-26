# Cost Tracking & Billing Guide

## How Session Tracking Works

Every Claude Code CLI session is automatically logged to
`C:\Users\Tracy\Projects\claude-tracking\sessions.csv` via a global Stop hook
in `~/.claude/settings.json`. Each project must have `.claude/project-code.txt`
for accurate attribution.

## Setup for a New Billable Project

1. Create `.claude/project-code.txt` in the project root with one line: the project code
2. Create `.claude/billing.json` for expense tracking (see schema below)
3. (Optional) Add a project-specific `ANTHROPIC_API_KEY` to `.env` for exact API cost tracking
4. Add the project code to the active codes table in `global/CLAUDE.md`

## Active Project Codes

| Code | Project | Client | Billing Method |
|------|---------|--------|----------------|
| ALD-SERVICETITAN | ServiceTitan MCP Server | American Leak Detection | Retainer |
| ALD-CALL-ANALYSIS | Call Analysis & Training | American Leak Detection | Retainer |
| JOB-APPLICATIONS | Job Application System | Internal | Internal |

## Rate Card

- **Retainer / internal projects:** Included in monthly fee — log tokens for internal allocation
- **Billable API work:** Check Anthropic Console (filter by project API key) for exact USD
- **Billable subscription work:** Session count x your internal hourly/session rate

## Per-Project Expense Tracking (billing.json)

Create `.claude/billing.json` in the project root to track hosting, domains,
API costs, software licenses, and one-time purchases. These merge into the
monthly report alongside token usage automatically.

### Recurring expense schema

```json
{
  "version": 1,
  "expenses": [
    {
      "id": "unique-slug",
      "description": "Human-readable name",
      "category": "hosting|domain|api|software|license|one-time",
      "amount": 20.00,
      "type": "recurring",
      "frequency": "monthly|quarterly|yearly",
      "start_date": "YYYY-MM-DD",
      "end_date": null,
      "notes": ""
    }
  ]
}
```

### One-time expense schema

For one-time expenses, use `"type": "one-time"` and `"date": "YYYY-MM-DD"`
instead of `frequency`/`start_date`/`end_date`.

```json
{
  "id": "domain-registration",
  "description": "Domain registration for example.com",
  "category": "domain",
  "amount": 12.00,
  "type": "one-time",
  "date": "2026-02-15",
  "notes": "Registered via Cloudflare"
}
```

## Month Attribution

- **Monthly** = every month while active
- **Quarterly** = every 3 months from start_date
- **Yearly** = anniversary month only
- **One-time** = month of purchase only

## Generating a Monthly Invoice

```bash
python C:\Users\Tracy\Projects\claude-tracking\report.py --month YYYY-MM
```

Output lists sessions, tokens, and expenses by project. For API-billed projects,
cross-reference the Anthropic Console filtered by the project's API key for exact USD cost.
