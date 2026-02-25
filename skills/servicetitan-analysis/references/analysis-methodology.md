# Analysis Methodology: The Five-Dimension Check

> Reference: `servicetitan-analysis` skill
> Origin: ALD compensation analysis, February 2026

## The Problem

The first answer from any analytical system is almost always incomplete. It answers the question that was asked, not the question that should have been asked. Traditional BI can't recover from this — a new requirements cycle costs weeks. DSF recovers in minutes, but only if the operator pushes systematically.

---

## The Five Dimensions

Before presenting any conclusion that drives a business decision, confirm the analysis has examined all five dimensions. If any dimension is missing, flag it — don't deliver a partial answer as a final answer.

### 1. RATE — Is the unit price changing?
- Revenue per job, per unit, per hour, per transaction
- Are increases uniform across all segments or concentrated?
- Is the stated price change actually flowing through to realized revenue?

### 2. VOLUME — Is the quantity of work changing?
- Job counts, transactions, units sold, cases handled
- Trending up, down, or flat?
- Seasonal patterns vs real growth/decline?

### 3. MIX — Is the composition of work shifting?
- Are high-value vs low-value jobs redistributing?
- Is the same person doing different work than before?
- Could a "decline" in $/unit actually be a shift to more (cheaper) units?

### 4. STRUCTURE — Are compensation/cost structures uniform?
- Different commission rates, bonus tiers, salary vs hourly vs commission
- Fixed components (management fees, base pay, stipends)
- Do structural differences amplify or dampen the effect being measured?

### 5. EFFORT — Is the workload comparable?
- Hours worked, days available, capacity utilization
- Are we comparing people/teams with different time commitments?
- Does "more output" mean "more productive" or "more hours"?

### Bonus: COHORT — Who's in the analysis and why?
- Are outliers (new hires, departures, part-timers, specialists) skewing the average?
- Should they be excluded, segmented, or flagged?
- Would the conclusion change if the cohort changed?

---

## Pre-Conclusion Checklist

Before delivering a conclusion that informs a business decision:

1. Have I examined **RATE** (unit economics changing)?
2. Have I examined **VOLUME** (quantity of work changing)?
3. Have I examined **MIX** (composition of work shifting)?
4. Have I asked about **STRUCTURE** (are comp/cost models uniform)?
5. Have I asked about **EFFORT** (are workloads comparable)?
6. Have I validated the **COHORT** (who's in/out and why)?

If any dimension is unexamined, state what's missing before presenting the conclusion. Frame the answer as preliminary until all dimensions are covered.

> "Based on pricing data alone, the answer appears to be X. However, I haven't yet examined volume trends or whether workloads are comparable. Should we look at those before finalizing?"

---

## When to Apply

**Apply when:**
- The output drives a decision with real dollar impact
- Multiple stakeholders with different compensation/incentive structures are being compared
- The "obvious" framing might be missing a dimension
- Someone could reasonably ask "but what about..." after seeing the result

**Skip when:**
- Simple lookups ("what was revenue last month")
- Single-dimension queries ("show me job counts by tech")
- Exploratory questions where the user is still framing the problem

---

## The Deeper Principle

The DSF advantage is NOT getting it right the first time. The advantage is:

1. **Iteration costs minutes, not weeks.** Adding a new dimension takes one question, not a new BI project.
2. **Domain knowledge compounds in real-time.** The operator supplies context and the model adjusts immediately.
3. **The conversation IS the analysis.** No handoff between discovery and reporting.
4. **Self-correction is a feature, not a failure.** A dashboard ships the first number as final. A conversation challenges and corrects it.
