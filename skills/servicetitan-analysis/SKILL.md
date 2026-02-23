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
---

# ServiceTitan Analysis Skill

> **Status:** Stub — needs formalization from ALD (American Leak Detection) work.
> Core query patterns and report structures to be migrated from production use.

Operational analytics for home services businesses via the ServiceTitan API.

## Prerequisites

- ServiceTitan MCP server running and configured
- Valid ServiceTitan API credentials (app key + tenant ID)
- API access to the required endpoints (jobs, invoices, technicians, etc.)

## Available Analysis Types

### Technician Performance
- Revenue per technician (daily, weekly, monthly)
- Average ticket size by technician
- Conversion rate (opportunities → sold jobs)
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

```
TODO: Migrate query patterns from production ALD work:
- Technician scorecard query
- Weekly revenue rollup
- Job profitability report
- Dispatch efficiency report
- Membership retention analysis
- Customer cohort analysis
```

## Report Templates

```
TODO: Migrate report templates:
- Weekly flash report (executive summary)
- Technician scorecard (individual performance)
- Business unit P&L
- Dispatch optimization recommendations
- Customer health dashboard
```

## MCP Server Integration

```
TODO: Document MCP server configuration:
- Required environment variables
- Available tools/functions
- Rate limiting considerations
- Data refresh frequency
```

## Billing

Project code: `ALD-SERVICETITAN`
Client: American Leak Detection
