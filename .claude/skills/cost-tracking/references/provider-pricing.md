# AI Provider Pricing Reference

Last updated: 2026-02-27

Pricing per 1 million tokens. All prices in USD.

## Anthropic Claude

| Model | Input ($/1M) | Output ($/1M) | Context | Notes |
|-------|-------------|---------------|---------|-------|
| claude-opus-4-20250514 | $15.00 | $75.00 | 200K | Most capable, use sparingly |
| claude-sonnet-4-20250514 | $3.00 | $15.00 | 200K | Best balance of quality/cost |
| claude-haiku-4-5-20251001 | $0.25 | $1.25 | 200K | Fast + cheap, use for simple tasks |

**Prompt caching discounts:**
- Cached input: 90% discount (Sonnet: $0.30/M, Haiku: $0.025/M)
- Cache write: 25% premium over base input price

**Extended thinking:**
- Thinking tokens billed at output rate
- Budget token limit: configurable per request

## OpenAI

| Model | Input ($/1M) | Output ($/1M) | Context | Notes |
|-------|-------------|---------------|---------|-------|
| gpt-4o | $2.50 | $10.00 | 128K | General purpose |
| gpt-4o-mini | $0.15 | $0.60 | 128K | Cost-optimized |
| o1 | $15.00 | $60.00 | 200K | Reasoning model |
| o3-mini | $1.10 | $4.40 | 200K | Reasoning, cost-optimized |

## Cost Calculation Formula

```typescript
function calculateCost(
  model: string,
  usage: { input_tokens: number; output_tokens: number }
): number {
  const pricing = MODEL_PRICING[model];
  if (!pricing) throw new Error(`Unknown model: ${model}`);

  const inputCost = (usage.input_tokens / 1_000_000) * pricing.inputPerMillion;
  const outputCost = (usage.output_tokens / 1_000_000) * pricing.outputPerMillion;

  return Math.round((inputCost + outputCost) * 1_000_000) / 1_000_000; // 6 decimal places
}
```

## Hosted Service Pricing (Free Tiers)

| Service | Free Tier Limits | Upgrade Trigger |
|---------|-----------------|-----------------|
| **Vercel Hobby** | 100GB bandwidth, 6K serverless min/mo | >100 users or need preview deploys |
| **Supabase Free** | 500MB DB, 1GB storage, 2GB bandwidth | >500MB data or need backups |
| **Clerk Free** | 10,000 MAUs | >10K users |
| **Planetscale Free** | 1 DB, 1B row reads/mo, 10M row writes | Need branching or >1B reads |

## When to Update This File

- After any AI provider announces pricing changes
- When adding a new AI provider to a project
- Quarterly review to catch any missed changes
- When a hosted service tier changes limits
