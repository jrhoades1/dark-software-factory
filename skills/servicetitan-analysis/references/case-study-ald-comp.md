# Case Study: Technician Compensation Analysis

> Reference: `servicetitan-analysis` skill
> Client: American Leak Detection (South Florida franchise)
> Date: February 2026

## Problem Statement

Business raised service prices in 2024 and assumed technicians benefited proportionally through commission (21-25% of revenue). Office staff had received no raise in 18 months; ownership was considering a 10% office increase. Question: **is that equitable?**

No dashboard existed. Data was locked inside ServiceTitan across thousands of job records spanning 18 months.

## Traditional Cost

- Data engineer + BI analyst: 1-2 weeks, $5,000-15,000
- Assumes the right questions are asked upfront (they weren't)

## What Actually Happened

Single conversational session via ServiceTitan MCP server + Claude. ~20 minutes.

### Analysis Progression

| Step | Action | Dimension |
|------|--------|-----------|
| 1 | Jun-Dec 2024 vs 2025 tech comparison (jobs, revenue, $/job) | Rate |
| 2 | Noticed price increase wasn't uniform — some techs going backwards | Mix |
| 3 | Applied 21% commission to see per-tech dollar impact | Structure |
| 4 | Pulled 18 months of monthly data (19 API calls: 1/month x all techs) | — |
| 5 | Annualized growth rates — raw deltas to comparable annual % | — |
| 6 | Adjusted for real comp structures (varied commission rates, management fees) | Structure |
| 7 | **Initial conclusion: +3.3% annual $/job growth** | Rate + Mix |
| 8 | Added volume trends — +5.8% annual job count growth | Volume |
| 9 | Factored in effort — 64-80+ hrs/pay vs standard office hours | Effort |
| 10 | Cleaned cohort — removed part-timers, pool techs, new hires | Cohort |
| 11 | **Revised conclusion: ~9.5% effective comp growth — 10% office raise is parity** | All |

### Key Findings

| Metric | Value |
|--------|-------|
| Core techs analyzed | 5 (consistent performers, full 18mo data) |
| Annualized $/job growth | +3.3% |
| Annualized volume growth | +5.8% |
| Combined effective comp growth | ~9.5% |
| Initial estimate (rate only) | 3-4% |
| Revised estimate (all dimensions) | ~9.5% — 10% office raise is parity |

### Insights

- **Job mix shift absorbs price increases** — pricing went up but techs doing different (lower-value) work
- **Volume was the hidden multiplier** — more jobs (+5.8%) compounded the price increase effect
- **Effort disparity reframed fairness** — field techs at 64-80+ hrs vs office at standard hours
- **First-pass answer was 188% low** — 3.3% jumped to 9.5% once all dimensions examined

## API Pattern

- 19 sequential API calls (one per month x all technicians)
- Data normalized across time periods within the conversation
- Domain knowledge (commission rates, management fees, exclusions) supplied by operator mid-analysis

## Validation Points

1. **No schema design upfront** — MCP exposes primitives, Claude composes on the fly
2. **Domain expertise applied in real-time** — not spec'd in a requirements doc
3. **Self-correction in same session** — 3.3% → 9.5%, all within one conversation
4. **Decision-ready output** — defensible number for a compensation conversation

## Repeatable Pattern

Every home services company with 5-20 technicians has this blind spot. They raise prices and assume the field benefits. Nobody checks whether job mix changes absorb the increase. This is a repeatable advisory engagement: connect to ServiceTitan, run the Five-Dimension analysis, deliver the insight.
