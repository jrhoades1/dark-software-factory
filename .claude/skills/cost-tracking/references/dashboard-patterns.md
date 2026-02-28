# Cost Dashboard Component Patterns

Reusable component patterns for displaying cost data. Adapt to your UI framework
(React/Next.js with shadcn/ui shown here).

## CostSummaryCard

Displays current month spend, daily average, and projection.

```typescript
// components/admin/cost-summary.tsx
interface CostSummary {
  monthlySpend: number;
  monthlyCapUsd: number;
  projectedMonthly: number;
  totalCalls: number;
  daysElapsed: number;
}

// Display:
// ┌─────────────────────────────────────┐
// │ AI Spend This Month                 │
// │ $4.23 / $10.00                      │
// │ ████████████░░░░░░░░  42%           │
// │                                     │
// │ Daily avg: $0.47  Projected: $14.10 │
// │ 87 calls this month                 │
// └─────────────────────────────────────┘
//
// - Progress bar color: green (<60%), yellow (60-80%), red (>80%)
// - If projected > cap, show warning icon
// - Use shadcn Card + Progress components
```

## SpendAlertBanner

Dismissible warning banner shown when approaching or exceeding limits.

```typescript
// components/admin/spend-alert.tsx
interface SpendAlert {
  id: string;
  alertType: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  createdAt: string;
}

// Display:
// ┌─ ⚠️ ─────────────────────────────────────────────────────┐
// │ You've used 83% of your $10.00 monthly AI budget ($8.30). │
// │ Consider reducing usage or increasing your cap.      [✕]  │
// └───────────────────────────────────────────────────────────┘
//
// Severity colors:
// - medium: yellow/amber background
// - high: orange background
// - critical: red background with bold text
// Use shadcn Alert component with variant mapping
```

## AIUsageChart

Line or bar chart showing AI usage over time.

```typescript
// components/admin/ai-usage-chart.tsx
interface DailyUsage {
  day: string;       // "2026-02-15"
  dailyCost: number;
  dailyCalls: number;
}

// Display: Line chart with recharts
// - X axis: dates (last 30 days)
// - Y axis (left): cost in USD
// - Y axis (right): call count
// - Horizontal dashed line at monthly cap / days in month (daily budget)
//
// Dependencies: recharts (npm install recharts)
// Use ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend
```

## CostBreakdownTable

Itemized view of AI calls with filtering.

```typescript
// components/admin/cost-breakdown.tsx
interface AIGeneration {
  id: string;
  generationType: string;
  modelUsed: string;
  tokensInput: number;
  tokensOutput: number;
  costUsd: number;
  createdAt: string;
}

// Display: shadcn Table with columns:
// | Time | Type | Model | Input Tokens | Output Tokens | Cost |
// |------|------|-------|-------------|--------------|------|
// | 2:34 PM | Job Analysis | sonnet-4 | 4,231 | 1,892 | $0.04 |
// | 1:15 PM | Resume Tailor | sonnet-4 | 6,102 | 2,841 | $0.06 |
//
// Features:
// - Filter by generation type
// - Sort by cost (desc) or date
// - Pagination (20 per page)
// - Total row at bottom
```

## CostConfigForm

Settings form for adjusting spend limits.

```typescript
// components/admin/cost-config.tsx
interface CostConfig {
  monthlyAiCapUsd: number;
  alertThresholdPct: number;
  singleCallAlertUsd: number;
  blockOnCap: boolean;
  emailOnHigh: boolean;
}

// Display: shadcn form with:
// - Monthly budget: Input (number, $1-$100)
// - Alert at: Slider (50%-95%)
// - Flag calls over: Input (number, $0.10-$5.00)
// - Hard block at cap: Switch
// - Email for high alerts: Switch
// - Save button
```

## SpendByTypeChart

Pie or bar chart showing spend breakdown by generation type.

```typescript
// Display: Donut chart or horizontal bar chart
// - Segments: job_analysis, resume_tailor, cover_letter, etc.
// - Show percentage and dollar amount per segment
// - Use recharts PieChart or BarChart
```

## Admin Page Layout

Compose the above components into an admin page:

```typescript
// app/dashboard/admin/page.tsx
//
// Layout:
// ┌──────────────────────────────────────────┐
// │ [SpendAlertBanner - if active]           │
// ├──────────────────┬───────────────────────┤
// │ CostSummaryCard  │ SpendByTypeChart      │
// ├──────────────────┴───────────────────────┤
// │ AIUsageChart (full width)                │
// ├──────────────────────────────────────────┤
// │ CostBreakdownTable (full width)          │
// ├──────────────────────────────────────────┤
// │ CostConfigForm                           │
// └──────────────────────────────────────────┘
```
