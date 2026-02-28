---
name: cost-tracking
description: >
  Layer expense monitoring and cost controls onto any DSF project that uses paid APIs
  or hosted services. Adds AI usage tracking tables, cost calculation middleware,
  spend cap enforcement, alert thresholds, and admin dashboard components. Use this
  skill when the project calls Anthropic, OpenAI, or any pay-per-use API, or when
  deploying to paid tiers of Vercel, Supabase, AWS, or similar platforms. Also trigger
  when the user mentions "cost tracking," "expense monitoring," "spend caps," "budget
  alerts," "API costs," "token usage," or "billing dashboard." This skill layers ON TOP
  of an existing project — if no project exists yet, use project-bootstrap first.
user-invokable: true
---

# Cost Tracking Skill

## Intent

1. **No surprise bills** — every pay-per-use API call is logged with token counts and cost before the response leaves the server
2. **Spend caps are enforced, not advisory** — when the monthly budget is hit, AI requests are rejected with a clear error, not silently allowed to continue
3. **Cost visibility is a feature, not an afterthought** — the admin dashboard shows current spend, projections, and alerts from day one
4. **Provider pricing changes are centralized** — update one reference file, not scattered constants across the codebase
5. **Alert thresholds follow the security-hardening pattern** — severity levels, response actions, and notification channels are defined upfront

## When this skill applies

Any DSF project that:
- Calls AI APIs (Anthropic Claude, OpenAI, Google AI, etc.) on a pay-per-use basis
- Deploys to platforms with usage-based billing (Vercel, Supabase, AWS, etc.)
- Needs visibility into operational costs for budgeting or client billing
- Has configurable spend limits per user or organization

## What this skill adds

### 1. Database Schema

Add these tables to your migration. See `references/schema-patterns.md` for complete SQL.

**`ai_generations`** — Audit log for every AI API call:
- `generation_type` (job_analysis, resume_tailor, cover_letter, chat, etc.)
- `model_used` (claude-sonnet-4-20250514, gpt-4o, etc.)
- `tokens_input`, `tokens_output` — from API response usage metadata
- `cost_usd` — calculated from model pricing at time of call
- `clerk_user_id` / `user_id` — who triggered the call

**`expense_alerts`** — Log of threshold crossings:
- `alert_type` (monthly_cap_warning, monthly_cap_reached, single_call_high, storage_warning)
- `threshold_value`, `actual_value` — what was the limit vs what was observed
- `resolved` — whether the alert has been acknowledged

**`cost_config`** — Per-user or global configurable limits:
- `monthly_ai_cap_usd` (default: $10.00)
- `alert_threshold_pct` (default: 80 — warn at 80% of cap)
- `single_call_alert_usd` (default: $0.50)

### 2. Cost Calculation Middleware

Wrap your AI client with a cost-tracking layer. The middleware:

1. **Pre-request:** Queries `ai_generations` for current month's total spend. If `>= monthly_ai_cap_usd`, rejects the request with HTTP 429 and a clear message.
2. **Post-request:** Extracts `usage.input_tokens` and `usage.output_tokens` from the API response, looks up the model's pricing from `references/provider-pricing.md`, calculates cost, and inserts into `ai_generations`.
3. **Alert check:** If the new monthly total crosses the alert threshold, inserts into `expense_alerts`.

**Pattern (TypeScript / Anthropic):**
```typescript
import Anthropic from '@anthropic-ai/sdk';

export async function createTrackedMessage(
  params: Anthropic.MessageCreateParams,
  userId: string,
  generationType: string,
) {
  // 1. Check spend cap
  const monthlySpend = await getMonthlySpend(userId);
  const config = await getCostConfig(userId);
  if (monthlySpend >= config.monthly_ai_cap_usd) {
    throw new SpendCapExceededError(monthlySpend, config.monthly_ai_cap_usd);
  }

  // 2. Make the API call
  const response = await anthropic.messages.create(params);

  // 3. Log usage
  const cost = calculateCost(params.model, response.usage);
  await logAIGeneration({
    clerk_user_id: userId,
    generation_type: generationType,
    model_used: params.model,
    tokens_input: response.usage.input_tokens,
    tokens_output: response.usage.output_tokens,
    cost_usd: cost,
  });

  // 4. Check alert thresholds
  const newTotal = monthlySpend + cost;
  await checkAlertThresholds(userId, newTotal, config);

  return response;
}
```

### 3. Alert Thresholds

See `references/cost-thresholds.md` for the complete threshold table. Key alerts:

| Metric | Default Threshold | Severity | Action |
|--------|-------------------|----------|--------|
| Monthly AI spend | 80% of cap | MEDIUM | In-app warning banner |
| Monthly AI spend | 100% of cap | HIGH | Block AI requests |
| Single AI call | >$0.50 | LOW | Flag in audit log |
| Supabase DB size | 80% of tier limit | MEDIUM | Dashboard warning |
| Vercel serverless | 80% of tier limit | MEDIUM | Dashboard warning |

### 4. Admin Dashboard Components

See `references/dashboard-patterns.md` for component patterns:

- **CostSummaryCard** — Current month spend, daily average, projected month-end
- **AIUsageChart** — Calls by type over time (line chart)
- **SpendAlertBanner** — Dismissible warning when approaching limits
- **CostBreakdownTable** — Itemized AI calls with model, tokens, cost, timestamp

### 5. External Service Monitoring

For services that don't have in-app API metering:

| Service | Monitoring Method | Setup |
|---------|------------------|-------|
| **Vercel** | Spend Management (dashboard) | Settings → Billing → set budget cap |
| **Supabase** | Management API | Query project stats for DB size, bandwidth |
| **Clerk** | Dashboard only | 10K MAU free tier — check monthly |
| **AWS** | Cost Explorer + Budgets API | Set budget alerts via AWS Budgets |

## Step-by-step integration

1. Add the tables from `references/schema-patterns.md` to your migration
2. Wrap your AI client using the middleware pattern above
3. Create an admin API route that aggregates `ai_generations` data
4. Add the dashboard components from `references/dashboard-patterns.md`
5. Configure Vercel Spend Management if on a paid tier
6. Set initial cost config values in `cost_config` table

## Updating pricing

When AI provider pricing changes, update `references/provider-pricing.md`. The middleware reads pricing from a centralized lookup, so no code changes are needed — just update the reference file and redeploy the pricing constants.

## Projects using this skill

| Project | Path | Integration date |
|---------|------|-----------------|
| job-app-assistant | `C:\Users\Tracy\Projects\job-app-assistant` | 2026-02-27 |

When updating schema or middleware patterns, check these projects for compatibility.
