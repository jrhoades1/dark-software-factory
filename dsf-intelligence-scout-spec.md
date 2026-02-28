# DSF Skill: `intelligence-scout`

## Purpose

Automated daily reconnaissance of X and YouTube for content that impacts DSF — new techniques to adopt, anti-patterns to avoid, model capability changes, competitive signals, and emerging best practices in agentic development. Produces a structured daily briefing tied directly to DSF skills and components.

This is DSF eating its own cooking: a multi-agent workflow that uses the orchestration layer to crawl, filter, analyze, and present findings.

---

## Why This Matters

The Claude Code article you just read? That was published and immediately relevant to DSF's architecture. But you found it manually. The agentic development space moves fast — Simon Willison, the Claude Code team, LangChain, CrewAI, OpenAI's agent SDK, indie builders on X — are all shipping ideas daily. Some validate your approach, some challenge it, some reveal gaps. You need a systematic way to catch these signals instead of relying on your feed algorithm.

The "bad" findings matter as much as the "good." When someone publishes a multi-agent orchestration failure post-mortem, that's a test case for your compliance-gate design. When CrewAI ships a feature that overlaps with your intent-resolver, that's competitive intelligence.

---

## Architecture

### Data Sources

**X (Twitter)**
- **Reality check:** X API is expensive ($100/mo for Basic, $5000/mo for Pro). Free tier is read-only and heavily rate-limited (17 reads/15min on v2). For a daily scout, we have options:
  - **Option A: API (Basic tier, $100/mo)** — 10,000 reads/mo, enough for daily monitoring of ~50 accounts + keyword searches. Most reliable but has cost.
  - **Option B: RSS bridges** — Services like Nitter (when operational), RSSHub, or Twstalker that expose X content as RSS. Free but fragile — these break regularly as X blocks them.
  - **Option C: Web scraping via headless browser** — Puppeteer/Playwright to load feeds. Against X ToS, brittle, not recommended for a production skill.
  - **Option D: Curated list + manual trigger** — Instead of automated crawl, maintain a list of accounts and use web search to find their recent posts. Lower fidelity but zero API cost.
  - **Recommended: Start with Option D (web search), graduate to Option A when DSF revenue justifies $100/mo.**

**YouTube**
- **YouTube Data API v3** — Free tier gives 10,000 quota units/day. Search costs 100 units, so ~100 searches/day. More than enough.
- Search by channel (subscribe to key creators) and by keyword
- Pull video metadata, descriptions, and — critically — auto-generated transcripts via `youtube-transcript-api` (Python, free, no API key needed)
- Transcripts are where the real value is: a 20-minute video from the Claude team contains more signal than 50 tweets

**Supplementary Sources (Phase 2)**
- Hacker News API (free, well-structured)
- GitHub trending repos (free API)
- ArXiv RSS feeds for agent/LLM papers
- Anthropic's blog and changelog (web fetch)
- Substack RSS from key authors

### Monitored Accounts & Channels

**X Accounts (starter list):**
```yaml
tier_1_must_watch:
  - "@AnthropicAI"        # Official announcements, model releases
  - "@alexalbert__"       # Head of Claude Relations, product direction  
  - "@siloraptor"         # Romain Huet, Claude Code engineering insights
  - "@RLanceMartin"       # LangChain, agent architecture patterns
  - "@simonw"             # Simon Willison, AI-assisted dev levels (your L5 reference)
  - "@swyx"               # AI engineering patterns, latent space
  - "@karpathy"           # Model capabilities, training insights
  - "@mcaborern"          # Boris Power, agent design at Anthropic
  - "@ClaudeCode"         # Claude Code official updates

tier_2_signal:
  - "@LangChainAI"        # Competitor framework signals
  - "@CrewAIInc"          # Multi-agent competitor
  - "@OpenAI"             # Competitive model capabilities
  - "@GoogleDeepMind"     # Research that affects model capabilities
  - "@e2aborern"          # Devin/Cognition, competing agent products
  - "@lataborenntspace"   # AI engineering podcast, industry trends

tier_3_indie_builders:
  - # Populated dynamically as scout discovers relevant builders
  - # Scout recommends additions based on engagement patterns
```

**YouTube Channels:**
```yaml
channels:
  - "Anthropic"                 # Official demos, feature deep-dives
  - "AI Engineer"               # Conference talks, practitioner content
  - "Latent Space"              # Deep technical interviews
  - "Fireship"                  # Fast takes on new releases (early signal)
  - "ArXiv Papers"              # Paper explanations
  - "Matt Wolfe"                # AI tool landscape coverage
  - "David Shapiro"             # Agent architecture thinking
```

**Keyword Searches:**
```yaml
x_keywords:
  - "claude code skills"
  - "agentic development"
  - "multi-agent orchestration"
  - "AI assisted development"
  - "HIPAA AI"
  - "healthcare LLM"
  - "progressive disclosure agents"
  - "tool design LLM"
  - "intent-driven development"
  - "MCP server"
  - "claude code tips"

youtube_keywords:
  - "claude code tutorial"
  - "building AI agents"
  - "multi-agent systems"
  - "agentic coding"
  - "LLM tool design"
  - "healthcare AI development"
  - "AI development framework"
```

---

## Scout Pipeline (Daily Workflow)

### Stage 1: Crawl
**Agent:** Data Collection Agent

```
Schedule: Daily at 6:00 AM EST (before your morning review)

X crawl (via web search fallback):
  - Search "[account name] + [keyword]" for each tier_1 account
  - Search each keyword independently  
  - Filter: last 24 hours
  - Capture: post text, engagement metrics, links, thread context

YouTube crawl (via API):
  - Search each keyword, filter: last 24 hours, sort by relevance
  - Check each monitored channel for new uploads
  - For relevant videos: pull transcript via youtube-transcript-api
  - Capture: title, description, transcript, view count, channel

Output: raw_feed.json — all discovered content, unfiltered
```

### Stage 2: Filter & Relevance Score
**Agent:** Analysis Agent

```
Input: raw_feed.json
Process:
  - Score each item 1-10 on DSF relevance using criteria:
    - Direct mention of techniques DSF uses (skills, intent blocks, orchestration)
    - New model capabilities that affect DSF architecture
    - Competitive framework features or limitations
    - Healthcare/compliance AI patterns
    - Multi-agent coordination patterns
    - Tool design principles
    - Failure modes or anti-patterns in agentic development
  
  - Classify each item:
    - "adopt"      → Technique/pattern DSF should incorporate
    - "validate"   → Confirms a DSF design decision
    - "challenge"  → Contradicts a DSF assumption (important!)
    - "compete"    → Competitive product/framework signal
    - "capability" → New model capability that changes what's possible
    - "warning"    → Anti-pattern or failure mode to avoid
    - "noise"      → Not relevant enough (score < 4), discard
  
  - Map to DSF component:
    - Which skill does this affect? (e.g., "agent-orchestrator", "compliance-gate")
    - Is this about a skill we have, or a skill we need?
    - Does this affect the business positioning (IntentStack/Rhoades AI)?

Output: scored_feed.json — filtered, scored, classified, mapped
```

### Stage 3: Synthesize & Brief
**Agent:** Briefing Agent

```
Input: scored_feed.json
Output: daily_brief.md — structured briefing document

Format (see template below)
```

---

## Daily Briefing Template

```markdown
# DSF Intelligence Brief — [DATE]

## Priority Signal (score 8-10)
Items requiring your attention today. Each includes source, classification, 
and specific DSF impact.

### [TITLE / SUMMARY]
- **Source:** [link] | **Type:** [adopt/challenge/warning/etc.] | **Score:** [N/10]
- **What it says:** [2-3 sentence summary]
- **DSF Impact:** [Which skill/component this affects and how]
- **Recommended Action:** [Specific next step — update a skill, add to roadmap, investigate further, etc.]

---

## Validation Signals (things we're doing right)
Brief list of content that confirms DSF design decisions. Good for 
confidence and for marketing content.

- [Source]: [What it validates about DSF]

## Competitive Landscape
New features, products, or positioning from competing frameworks.

- [Framework/Product]: [What they shipped/announced] → [DSF response needed?]

## Emerging Patterns
Recurring themes across multiple sources that suggest a trend.

- [Pattern]: [Evidence from N sources] → [Implication for DSF]

## Anti-Patterns & Warnings
Things going wrong for others that DSF should learn from.

- [Source]: [What went wrong] → [How DSF's design avoids/addresses this]

## Watch List Updates
- **New accounts to follow:** [if scout discovered relevant new voices]
- **Keywords to add:** [if new terminology or concepts emerged]
- **Sources going stale:** [accounts that haven't posted relevant content in 2+ weeks]

## Raw Stats
- Items crawled: [N]
- Items after relevance filter: [N]  
- Sources checked: [N accounts, N channels, N keyword searches]
```

---

## Implementation

### Phase 1: MVP (manual trigger, web search only)
**What:** A Claude Code skill you invoke manually that:
1. Uses web search to check tier_1 accounts and keywords
2. Fetches and analyzes YouTube transcripts for new relevant videos
3. Produces the daily briefing markdown

**Stack:**
- Claude Code skill (`/skills/intelligence-scout/SKILL.md`)
- Web search for X content (no API cost)
- `youtube-transcript-api` (Python) for transcripts
- YouTube Data API v3 for search/discovery (free tier)
- Output: markdown file in your project

**Invoke:** `claude "Run the intelligence scout"` or slash command

**Why start here:** Zero cost, validates the filtering/analysis pipeline, produces usable briefings immediately. You're testing whether the *analysis* is good before investing in *automation*.

### Phase 2: Automated daily run
**What:** Cron-triggered execution that runs the scout at 6 AM and delivers the briefing.

**Options for automation:**
- **GitHub Actions** — Free for public repos, 2000 min/mo for private. Schedule a workflow that runs the scout script and commits the briefing to a repo, or sends it via email/Slack.
- **Local cron + Claude Code** — If you have a persistent machine, `crontab` that invokes Claude Code with the scout skill.
- **Cloud function (AWS Lambda / Vercel)** — Serverless execution on schedule. Low cost at daily frequency.

**Delivery:**
- Markdown committed to a `dsf-intelligence` repo (searchable history)
- Email summary via SendGrid/SES (optional)
- Slack webhook to a `#dsf-intel` channel (optional)

### Phase 3: Full API integration + trend analysis
**What:** X API (Basic tier), expanded YouTube analysis, and weekly/monthly trend reports.

**Additions:**
- X API for reliable, structured data instead of web search
- Engagement-weighted scoring (highly-engaged posts get boosted)
- Weekly trend report: "This week's top 3 patterns across all sources"
- Monthly strategic report: "How DSF should evolve based on 30 days of signals"
- Automated watch list management (scout recommends new accounts based on who tier_1 accounts engage with)
- Backlink to the orchestration spec: scout findings auto-generate suggested task-graph updates

---

## Integration with DSF Orchestration

This skill is itself a multi-agent workflow that validates the orchestration layer:

```
Orchestrator
  ├── Data Collection Agent (crawl)
  │     ├── X search subtask
  │     └── YouTube search + transcript subtask
  │
  ├── Analysis Agent (filter & score)
  │     ├── Relevance scoring
  │     ├── Classification
  │     └── DSF component mapping
  │
  └── Briefing Agent (synthesize)
        ├── Priority signal extraction
        ├── Trend detection (across multiple items)
        └── Brief generation
```

The handoff documents between these agents use the same `agent-handoff` skill from the orchestration spec. The Analysis Agent receives a handoff from the Data Collection Agent with raw content and source metadata. The Briefing Agent receives scored/classified items and must synthesize across them.

This means the intelligence scout is both a **product** (it delivers value to you daily) and a **test harness** (it exercises the orchestration skills in a real workflow every day).

---

## Content You'd Have Caught This Week

To validate this concept, here's what the scout *would* have surfaced recently if it were running:

1. **The Claude Code action space article** (the one you just read)
   - Classification: `adopt` + `validate`
   - DSF Impact: Validates progressive disclosure pattern, suggests task-graph evolution
   - Score: 9/10

2. **Claude Code Tasks feature launch**
   - Classification: `capability`
   - DSF Impact: Directly affects `agent-orchestrator` and `task-graph` skills
   - Score: 10/10

3. **Any CrewAI or LangGraph multi-agent updates**
   - Classification: `compete`
   - DSF Impact: Feature comparison for IntentStack positioning
   - Score: 7/10

4. **Simon Willison posts on AI-assisted development patterns**
   - Classification: `validate` or `challenge`
   - DSF Impact: Level 5 framework alignment
   - Score: 8/10

---

## Business Value

**For you personally:** Stop missing signals. The agentic dev space is moving too fast for manual monitoring. One article (like today's) can reshape your architecture. A systematic scout means you catch these within 24 hours instead of whenever your feed algorithm decides to show it to you.

**For DSF validation:** Every daily run exercises the orchestration pipeline. Bugs, context issues, and handoff failures surface in a low-stakes workflow before they hit a client project.

**For IntentStack/Rhoades AI marketing:** The daily brief generates content ideas. When the scout classifies something as "validate," that's a potential case study or LinkedIn post: "Here's what Anthropic's team learned about X — and how DSF already handles it." When it classifies something as "challenge," that's thought leadership: "Here's a common approach that doesn't work in regulated environments, and here's why."

**For clients (future):** A customized version of this scout — monitoring their specific domain (healthcare regs, competitor product launches, relevant research) — is a standalone product. The intelligence-scout skill is domain-agnostic by design.
