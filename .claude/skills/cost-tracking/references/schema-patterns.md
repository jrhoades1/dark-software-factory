# Cost Tracking Database Schema

SQL patterns for adding cost tracking to any DSF project. Adapt the user ID
column (`clerk_user_id`) to match your auth provider.

## Tables

```sql
-- ============================================================
-- TABLE: ai_generations
-- Audit log for every AI API call. Never delete rows — this is
-- your cost accountability trail.
-- ============================================================
CREATE TABLE ai_generations (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  clerk_user_id     TEXT NOT NULL,
  application_id    UUID,                           -- FK to your domain table (nullable)

  generation_type   TEXT NOT NULL,                   -- e.g. 'job_analysis', 'resume_tailor', 'chat'
  model_used        TEXT NOT NULL,                   -- e.g. 'claude-sonnet-4-20250514'
  tokens_input      INTEGER NOT NULL DEFAULT 0,
  tokens_output     INTEGER NOT NULL DEFAULT 0,
  cost_usd          REAL NOT NULL DEFAULT 0,         -- calculated from model pricing

  input_summary     TEXT,                            -- truncated input for debugging (no PII)
  output_summary    TEXT,                            -- truncated output for debugging (no PII)
  duration_ms       INTEGER,                         -- API call duration
  error             TEXT,                            -- error message if call failed
  cached_tokens     INTEGER DEFAULT 0,              -- prompt cache hits (Anthropic)

  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ai_gen_user ON ai_generations(clerk_user_id);
CREATE INDEX idx_ai_gen_user_month ON ai_generations(clerk_user_id, created_at);
CREATE INDEX idx_ai_gen_type ON ai_generations(generation_type);

-- ============================================================
-- TABLE: expense_alerts
-- Log of threshold crossings. Tracks when users approach or
-- exceed spend limits.
-- ============================================================
CREATE TABLE expense_alerts (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  clerk_user_id     TEXT NOT NULL,

  alert_type        TEXT NOT NULL,                   -- 'monthly_cap_warning', 'monthly_cap_reached',
                                                     -- 'single_call_high', 'daily_spike',
                                                     -- 'storage_warning', 'bandwidth_warning'
  severity          TEXT NOT NULL                     -- 'low', 'medium', 'high', 'critical'
                    CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  threshold_value   REAL NOT NULL,                   -- what was the limit
  actual_value      REAL NOT NULL,                   -- what was the actual value
  message           TEXT NOT NULL,                   -- human-readable alert message

  resolved          BOOLEAN NOT NULL DEFAULT FALSE,
  resolved_at       TIMESTAMPTZ,
  resolution        TEXT,                            -- 'acknowledged', 'cap_increased', 'auto_resolved'

  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_alerts_user ON expense_alerts(clerk_user_id);
CREATE INDEX idx_alerts_unresolved ON expense_alerts(clerk_user_id, resolved) WHERE resolved = FALSE;

-- ============================================================
-- TABLE: cost_config
-- Per-user configurable spend limits and alert preferences.
-- One row per user. Created on signup or first AI usage.
-- ============================================================
CREATE TABLE cost_config (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  clerk_user_id       TEXT NOT NULL UNIQUE,

  monthly_ai_cap_usd  REAL NOT NULL DEFAULT 10.00,    -- hard cap per calendar month
  alert_threshold_pct INTEGER NOT NULL DEFAULT 80,     -- warn at this % of cap
  single_call_alert   REAL NOT NULL DEFAULT 0.50,      -- flag calls above this amount
  block_on_cap        BOOLEAN NOT NULL DEFAULT TRUE,   -- hard block vs warn-only
  email_on_high       BOOLEAN NOT NULL DEFAULT TRUE,   -- email for HIGH+ alerts

  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cost_config_user ON cost_config(clerk_user_id);
```

## Useful Queries

### Monthly spend for a user
```sql
SELECT
  COALESCE(SUM(cost_usd), 0) AS monthly_spend,
  COUNT(*) AS total_calls,
  SUM(tokens_input) AS total_input_tokens,
  SUM(tokens_output) AS total_output_tokens
FROM ai_generations
WHERE clerk_user_id = $1
  AND created_at >= DATE_TRUNC('month', NOW());
```

### Spend by generation type (current month)
```sql
SELECT
  generation_type,
  COUNT(*) AS call_count,
  SUM(cost_usd) AS total_cost,
  AVG(cost_usd) AS avg_cost,
  SUM(tokens_input + tokens_output) AS total_tokens
FROM ai_generations
WHERE clerk_user_id = $1
  AND created_at >= DATE_TRUNC('month', NOW())
GROUP BY generation_type
ORDER BY total_cost DESC;
```

### Daily spend trend (last 30 days)
```sql
SELECT
  DATE(created_at) AS day,
  SUM(cost_usd) AS daily_cost,
  COUNT(*) AS daily_calls
FROM ai_generations
WHERE clerk_user_id = $1
  AND created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY day;
```

### Monthly projection
```sql
WITH monthly AS (
  SELECT
    SUM(cost_usd) AS spend_so_far,
    EXTRACT(DAY FROM NOW()) AS days_elapsed,
    EXTRACT(DAY FROM DATE_TRUNC('month', NOW()) + INTERVAL '1 month' - INTERVAL '1 day') AS days_in_month
  FROM ai_generations
  WHERE clerk_user_id = $1
    AND created_at >= DATE_TRUNC('month', NOW())
)
SELECT
  spend_so_far,
  CASE WHEN days_elapsed > 0
    THEN ROUND((spend_so_far / days_elapsed * days_in_month)::numeric, 2)
    ELSE 0
  END AS projected_monthly
FROM monthly;
```

### Unresolved alerts
```sql
SELECT * FROM expense_alerts
WHERE clerk_user_id = $1
  AND resolved = FALSE
ORDER BY created_at DESC;
```
