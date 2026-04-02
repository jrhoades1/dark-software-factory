---
name: llm-council
description: >
  Run any question, idea, or decision through a council of 5 AI advisors who
  independently analyze it, peer-review each other anonymously, and synthesize
  a final verdict. Based on Karpathy's LLM Council methodology.
  MANDATORY TRIGGERS: "council this", "run the council", "war room this",
  "pressure-test this", "stress-test this", "debate this".
  STRONG TRIGGERS (use when combined with a real decision or tradeoff):
  "should I X or Y", "which option", "what would you do", "is this the right
  move", "validate this", "get multiple perspectives", "I can't decide",
  "I'm torn between".
  Do NOT trigger on simple yes/no questions, factual lookups, or casual
  "should I" without a meaningful tradeoff. DO trigger when the user presents
  a genuine decision with stakes, multiple options, and context that suggests
  they want it pressure-tested from multiple angles.
model: sonnet
context: fork
user-invokable: true
allowed-tools: Agent, Bash(python3 .claude/skills/llm-council/scripts/*), Read, Glob, Grep, Write
---

# LLM Council

Five independent advisors analyze a question from fundamentally different angles,
peer-review each other anonymously, then a chairman synthesizes a final verdict.
Adapted from Andrej Karpathy's LLM Council methodology.

## When to Use

The council is for questions where being wrong is expensive.

**Good council questions:**
- Pricing and packaging decisions
- Positioning and go-to-market angles
- Pivot or stay-the-course decisions
- Copy, messaging, or landing page critiques
- Hire vs automate tradeoffs

**Not council questions:**
- Single right answers (factual lookups)
- Creation tasks (write me a tweet)
- Processing tasks (summarize this article)

If the question has one right answer or doesn't benefit from multiple perspectives,
just answer it directly.

## The Five Advisors

Each advisor is a thinking style, not a persona. They create natural tension.

| Advisor | Lens | Role |
|---------|------|------|
| **The Contrarian** | Risk & failure | Finds what's wrong, what's missing, what will fail. Assumes a fatal flaw exists and hunts for it. |
| **The First Principles Thinker** | Fundamentals | Strips assumptions, rebuilds from ground up. Often says "you're asking the wrong question." |
| **The Expansionist** | Upside & opportunity | Finds upside everyone missed. What could be bigger? What's undervalued? Ignores risk (that's the Contrarian's job). |
| **The Outsider** | Fresh eyes | Zero context about the field or history. Catches the curse of knowledge — things obvious to you but confusing to everyone else. |
| **The Executor** | Implementation | Only cares about feasibility and speed. "What do you do Monday morning?" If no clear first step exists, says so. |

**Tension map:** Contrarian vs Expansionist (downside vs upside). First Principles vs Executor (rethink vs ship). Outsider keeps everyone honest.

## Process

### Step 1: Frame the Question (with context enrichment)

When triggered, do two things before framing:

**A. Scan for context (< 30 seconds).** Quick `Glob` + `Read` for:
- `CLAUDE.md` / `claude.md` in the workspace (business context, constraints)
- `memory/` folder (audience profiles, past decisions, business details)
- Files the user explicitly referenced
- Previous council transcripts (avoid re-counciling the same ground)
- Any files relevant to the specific question (pricing data, launch results, etc.)

Grab the 2-3 most relevant files. Don't over-research.

**B. Frame the question.** Reframe the user's raw question + enriched context as a clear, neutral prompt containing:
1. The core decision or question
2. Key context from the user's message
3. Key context from workspace files (business stage, audience, constraints, numbers)
4. What's at stake

Don't add your own opinion. Don't steer it. If the question is too vague, ask ONE clarifying question, then proceed.

Save the framed question for the transcript.

### Step 2: Convene the Council (5 sub-agents in parallel)

Spawn all 5 advisors simultaneously as sub-agents using the Agent tool. Use `model: sonnet` for all advisors. Each gets:

1. Their advisor identity and thinking style
2. The framed question
3. Instruction: respond independently, don't hedge, lean fully into your angle

**Sub-agent prompt template:**
```
You are [Advisor Name] on an LLM Council.

Your thinking style: [advisor description]

A user has brought this question to the council:

---
[framed question]
---

Respond from your perspective. Be direct and specific. Don't hedge or try to
be balanced. Lean fully into your assigned angle. The other advisors will cover
the angles you're not covering.

Keep your response between 150-300 words. No preamble. Go straight into your analysis.
```

**Target:** 150-300 words per advisor.

**Error handling:** If any advisor returns an unusable response, re-spawn that single advisor. If fewer than 4 usable responses after retry, flag to the user and proceed with what's available.

### Step 3: Peer Review (5 sub-agents in parallel)

This is the core of Karpathy's insight — what makes this more than "ask 5 times."

1. Collect all 5 advisor responses
2. **Anonymize:** Generate a random mapping of advisors to letters A-E. Record the mapping for the transcript reveal
3. Spawn 5 reviewer sub-agents in parallel (model: sonnet). Each sees all 5 anonymized responses

**Reviewer prompt template:**
```
You are reviewing the outputs of an LLM Council. Five advisors independently
answered this question:

---
[framed question]
---

Here are their anonymized responses:

**Response A:** [response]
**Response B:** [response]
**Response C:** [response]
**Response D:** [response]
**Response E:** [response]

Answer these three questions. Be specific. Reference responses by letter.

1. Which response is the strongest? Why?
2. Which response has the biggest blind spot? What is it missing?
3. What did ALL five responses miss that the council should consider?

Keep your review under 200 words. Be direct.
```

### Step 4: Chairman Synthesis

One sub-agent (model: opus) receives everything:
- The framed question
- All 5 advisor responses (de-anonymized, advisor names visible)
- All 5 peer reviews

The chairman produces the verdict using this exact structure. **IMPORTANT:** The
verdict is rendered by a markdown-to-HTML converter, so use clean markdown: `##`
headings, `**bold**` for emphasis, blank lines between paragraphs, and numbered
lists where appropriate. Do NOT dump everything into a single paragraph.

```
## Where the Council Agrees

[Points multiple advisors converged on independently. High-confidence signals.
Use numbered points if there are multiple. One paragraph per point.]

## Where the Council Clashes

[Genuine disagreements. Both sides presented. Why reasonable advisors disagree.
Separate each clash into its own paragraph with a blank line between them.]

## Blind Spots the Council Caught

[Things that only emerged through peer review. What individual advisors missed.]

## The Recommendation

[Clear, direct recommendation. Not "it depends." A real answer with reasoning.
The chairman CAN disagree with the majority if the dissenter's reasoning is strongest.]

## The One Thing to Do First

[A single concrete next step. Not a list. One thing.]
```

### Step 5: Generate the Council Report

Run the report renderer script:

```bash
python3 .claude/skills/llm-council/scripts/render_report.py \
  --question "<framed question>" \
  --verdict "<chairman verdict markdown>" \
  --advisors '<JSON: {"Contrarian": "...", "First Principles": "...", ...}>' \
  --reviews '<JSON: list of 5 review strings>' \
  --mapping '<JSON: {"A": "Contrarian", "B": "Executor", ...}>' \
  --output "council-report-$(date +%Y%m%d-%H%M%S).html"
```

Open the HTML file after generating it.

### Step 6: Save the Transcript

Write `council-transcript-[timestamp].md` in the same location. Include:
- The original question (user's raw input)
- The framed question
- All 5 advisor responses (labeled by advisor name)
- All 5 peer reviews (with anonymization mapping revealed)
- The chairman's full synthesis

This transcript is the audit artifact. Previous transcripts let the user (or a future agent) see how thinking evolved across council sessions.

## Output

Every council session produces two files:
```
council-report-YYYYMMDD-HHMMSS.html     # visual report for scanning
council-transcript-YYYYMMDD-HHMMSS.md   # full transcript for reference
```

## Cost Notes

This skill spawns 11 sub-agents total (5 advisors + 5 reviewers + 1 chairman).
Advisors and reviewers use Sonnet. Only the chairman uses Opus. This balances
quality with cost — the structured analysis work doesn't need Opus reasoning,
but the final synthesis does.

## Important Rules

- **Always spawn all 5 advisors in parallel.** Sequential spawning wastes time and lets earlier responses bleed into later ones.
- **Always anonymize for peer review.** If reviewers know which advisor said what, they defer to certain thinking styles instead of evaluating on merit.
- **The chairman can disagree with the majority.** If 4/5 say "do it" but the 1 dissenter's reasoning is strongest, side with the dissenter.
- **Don't council trivial questions.** If one right answer exists, just answer it.
- **The visual report matters.** Most users scan the report, not the transcript. Keep the HTML clean and scannable.
