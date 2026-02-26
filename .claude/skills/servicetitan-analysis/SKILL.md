---
name: servicetitan-analysis
description: >
  Operational analytics and reporting via the ServiceTitan MCP server. Query
  technician performance, job costing, revenue metrics, dispatch optimization,
  and customer analytics for home services businesses. Use this skill when the
  user mentions ServiceTitan, technician KPIs, job profitability, dispatch
  efficiency, membership retention, revenue per truck, average ticket, or any
  operational metric for plumbing, HVAC, electrical, or leak detection businesses.
  Also trigger for "ALD analytics," "American Leak Detection," or any reference
  to the ServiceTitan MCP server. Requires the ServiceTitan MCP server to be
  running and configured with valid API credentials.
user-invokable: true
---

# ServiceTitan Analysis Skill

## Intent

1. **Five-Dimension completeness before any conclusion** — rate, volume, mix, structure, effort, and cohort must all be examined before delivering a finding that drives a business decision; an incomplete analysis is worse than no analysis
2. **Cohort validation is mandatory** — who is in the dataset and why; outliers skew averages and create false narratives
3. **State confidence level explicitly** — "preliminary" is not a weakness; presenting uncertain findings as definitive is how bad decisions get made
4. **Business expert reviews conclusions before action** — the data says what it says, but the operations manager knows context the numbers cannot capture
5. **Enable data-driven operational decisions** — the goal is giving business owners answers they cannot get from ServiceTitan's native reporting
6. **Identify high-margin patterns worth replicating** — analysis should surface what works, not just what happened
7. **Per-month query under 2 minutes; full 6-month analysis under 15 minutes** — speed matters for responsiveness, but never at the cost of skipping a dimension or misattributing data

## Prerequisites

- ServiceTitan MCP server running and configured
- Valid ServiceTitan API credentials (app key + tenant ID)
- API access to the required endpoints (jobs, invoices, technicians, etc.)

## Five-Dimension Analysis Check (Required)

**Before delivering any conclusion that drives a business decision**, confirm the analysis covers all dimensions. See `references/analysis-methodology.md` for full detail.

| Dimension | Question | Common miss |
|-----------|----------|-------------|
| **Rate** | Is the unit price changing? | Assuming price increases flow through uniformly |
| **Volume** | Is the quantity of work changing? | Ignoring job count trends that compound rate changes |
| **Mix** | Is the composition of work shifting? | Averaging across different job types |
| **Structure** | Are comp/cost structures uniform? | Ignoring varied commission rates or fixed fees |
| **Effort** | Is the workload comparable? | Comparing raw percentages without hours context |
| **Cohort** | Who's in the analysis and why? | Letting outliers (new hires, part-timers) skew averages |

If any dimension is unexamined, state what's missing. Frame the answer as preliminary.

## Available Analysis Types

### Technician Performance
- Revenue per technician (daily, weekly, monthly)
- Average ticket size by technician
- Conversion rate (opportunities -> sold jobs)
- Callback rate (warranty returns)
- Membership sales per technician

### Job Costing & Profitability
- Revenue vs cost per job
- Material cost analysis
- Labor cost per job hour
- Profitability by job type (repair, install, maintenance)
- Profitability by business unit

### Revenue Analytics
- Revenue by business unit (plumbing, HVAC, leak detection)
- Revenue by service type
- Revenue trends (week-over-week, month-over-month)
- Average invoice value
- Membership revenue vs one-time revenue

### Dispatch Optimization
- Jobs per day per technician
- Drive time analysis
- Capacity utilization
- Dispatch efficiency (scheduled vs completed)
- Cancellation and reschedule rates

### Customer Metrics
- Customer acquisition cost
- Membership retention rate
- Customer lifetime value
- Repeat customer rate
- NPS / satisfaction scores

## Common Query Patterns

### Technician Compensation Analysis
The validated pattern from ALD production work. See `references/case-study-ald-comp.md`.

1. **Period comparison** — Pull technician data for two comparable periods (e.g., Jun-Dec YoY)
2. **Per-tech breakdown** — Jobs, revenue, $/job for each technician individually
3. **Commission modeling** — Apply actual commission rates (they vary per tech) to see dollar impact
4. **Monthly granularity** — Pull month-by-month data for trend analysis (1 API call per month x all techs)
5. **Annualize** — Convert raw deltas to annual percentages for comparability
6. **Five-Dimension sweep** — Rate, Volume, Mix, Structure, Effort, Cohort before concluding

### Weekly Revenue Rollup
1. Query completed jobs for the trailing 7 days by business unit
2. Compare to same week prior year (seasonality) and prior week (trend)
3. Break out by revenue type: service, install, maintenance, membership

### Technician Scorecard
1. Pull individual tech metrics for the scoring period
2. Metrics: revenue, job count, avg ticket, conversion rate, callback rate, membership sales
3. Rank against team averages and prior period self-comparison

### Job Profitability Report
1. Query jobs with revenue and cost data for the target period
2. Calculate margin by job type and business unit
3. Flag jobs below margin threshold
4. Identify high-margin patterns worth replicating

## Report Output Patterns

### Tabular Comparison
Best for tech-vs-tech or period-vs-period analysis:

| Technician | Jobs | Revenue | $/Job | vs Prior | Commission Est |
|-----------|------|---------|-------|----------|---------------|
| Tech A | 45 | $X | $Y | +Z% | $W |

### Trend Table
Best for month-over-month or longitudinal analysis:

| Month | Tech A $/Job | Tech B $/Job | Team Avg |
|-------|-------------|-------------|----------|
| 2024-06 | $X | $Y | $Z |

### Decision Summary
Always conclude business-decision analyses with:
- Initial finding (what the first pass showed)
- Revised finding (after all dimensions examined)
- What changed and why
- Recommended action with confidence level

## MCP Server Integration

### Required Environment Variables
- `SERVICETITAN_APP_KEY` — API application key
- `SERVICETITAN_TENANT_ID` — Tenant identifier
- `SERVICETITAN_CLIENT_ID` — OAuth client ID
- `SERVICETITAN_CLIENT_SECRET` — OAuth client secret

### Rate Limiting
- ServiceTitan API has per-minute and daily rate limits
- For multi-month analyses, sequential calls (1/month) stay within limits
- Batch operations: check API docs before assuming batch support is available
- If 429 errors occur: back off, reduce concurrency, consider caching responses

### Data Refresh
- ServiceTitan data is near-real-time for completed jobs
- In-progress jobs may have partial data
- For historical analysis, data is stable — cache aggressively

## References

- `references/analysis-methodology.md` — Five-Dimension Check methodology and when to apply it
- `references/case-study-ald-comp.md` — ALD compensation analysis case study (validated pattern)

## Billing

Project code: `ALD-SERVICETITAN`
Client: American Leak Detection
