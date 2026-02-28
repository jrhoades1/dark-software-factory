---
name: intelligence-scout
description: >
  Run the weekly DSF intelligence brief. Searches YouTube channels and the web
  for AI development signals relevant to the Dark Software Factory. Classifies
  findings as adopt, validate, challenge, compete, capability, or warning.
  Use when the user says "run the weekly brief," "intelligence scout," "what
  happened in AI this week," "weekly AI update," "scout for signals," or
  "what should DSF adopt." Output: .tmp/intelligence/weekly-brief-YYYY-MM-DD.md
model: sonnet
context: fork
user-invokable: true
allowed-tools: Bash(python3 .claude/skills/intelligence-scout/scripts/*)
---

# Intelligence Scout

Weekly reconnaissance of YouTube and the web for content that impacts DSF —
new techniques to adopt, anti-patterns to avoid, model capability changes,
competitive signals, and emerging best practices in agentic development.

## Intent

1. **Weekly cadence enforces signal quality over volume** — daily scanning produces noise; weekly synthesis produces decisions
2. **YouTube is the primary source, web search is secondary** — practitioners publish working knowledge on YouTube before it appears in docs or blogs; transcripts contain dense signal
3. **Every signal gets a classification label and a DSF relevance score** — raw information without classification is just reading; the taxonomy makes it actionable (see `references/classification-taxonomy.md`)
4. **The brief is for Jimmy, not for completeness** — 10 high-relevance signals with clear actions beats 50 signals with no guidance; cap at 15 signals max
5. **Python scripts only pull transcripts** — Claude natively searches the web and fetches pages; the script does the one thing Claude cannot: extract YouTube transcripts
6. **Output is a file, not a conversation** — `.tmp/intelligence/weekly-brief-YYYY-MM-DD.md` persists for review, linking, and quarterly rollups
7. **Phase 1 is manual-trigger only** — automation comes after the format is validated through real usage

## Prerequisites

```bash
# youtube-transcript-api must be installed
pip install youtube-transcript-api

# Verify:
python3 -c "from youtube_transcript_api import YouTubeTranscriptApi; print('ok')"
```

## Workflow

### Step 1 — Set Up Run

- Date: current date (`YYYY-MM-DD`)
- Output path: `.tmp/intelligence/weekly-brief-[date].md`
- Create `.tmp/intelligence/` if it doesn't exist

### Step 2 — YouTube Video Discovery

Read `references/scout-channels.md` for monitored channels. For each channel,
use WebSearch to find videos published in the last 7 days:

```
site:youtube.com "@[channel-handle]" [focus keyword]
```

Collect video URLs. Cap at 3-5 videos per channel, 15 total max.

### Step 3 — Pull Transcripts

Pass discovered video URLs to the transcript script:

```bash
python3 .claude/skills/intelligence-scout/scripts/youtube_transcripts.py \
  --video-ids "VIDEO_ID_1,VIDEO_ID_2,VIDEO_ID_3" \
  --output .tmp/intelligence/transcripts-[date].json
```

Read the output JSON. Note any failures (transcripts disabled, video unavailable).

### Step 4 — Web Intelligence

Use WebSearch natively for each keyword group from `references/scout-channels.md`:

- Anthropic / Claude queries
- Agent pattern queries
- Healthcare AI queries (if relevant to current projects)
- Competitive queries

Also check web sources directly via WebFetch:
- `https://www.anthropic.com/news` — scan for new posts in last 7 days
- `https://hn.algolia.com/api/v1/search?query=claude+code&tags=story&numericFilters=created_at_i>[unix_timestamp_7_days_ago]` — HN stories

### Step 5 — Classify Signals

Read `references/classification-taxonomy.md`. For each signal found across
YouTube transcripts and web results:

1. Assign a classification label (warning, capability, challenge, adopt, validate, compete)
2. Score 1-10 on DSF relevance using the weighted dimensions
3. Map to a DSF component
4. Write a 2-3 sentence summary
5. Determine action (specific next step or "Track only")

### Step 6 — Filter

Keep only:
- Signals with score >= 5
- All `warning` signals regardless of score
- All `capability` signals regardless of score
- All `challenge` signals regardless of score

Cap at 15 total. If more qualify, take highest-scoring.

### Step 7 — Compose Weekly Brief

Write the brief to `.tmp/intelligence/weekly-brief-[date].md` using this template:

```markdown
# DSF Intelligence Brief — [YYYY-MM-DD]

**Run date:** [date]
**Sources:** [N] YouTube videos, [N] web sources
**Signals found:** [N] — [breakdown by label]

---

## Warnings (Action Required)

[warning-label signals — or "None this week"]

## Capability Updates

[capability-label signals from Anthropic]

## Adopt Recommendations

[adopt-label signals, sorted by score descending]

## Validate (Needs Testing)

[validate-label signals]

## Challenges to Review

[challenge-label signals — contradictions to DSF assumptions]

## Competitor Watch

[compete-label signals]

---

## Sources

### YouTube
| Channel | Video | Transcript | Score |
|---------|-------|------------|-------|
| [channel] | [title + URL] | [yes/no] | [score] |

### Web
| Source | Article | Score |
|--------|---------|-------|
| [source] | [title + URL] | [score] |

---

*Generated by intelligence-scout skill*
*Taxonomy: .claude/skills/intelligence-scout/references/classification-taxonomy.md*
```

### Step 8 — Present Summary

Tell Jimmy:
- Top 3 signals (title + label + score)
- Count by label
- Path to the full brief file
- Any `warning` or `challenge` signals that need immediate attention

## Rules

- Never include signals with score < 5 unless they are `warning`, `capability`, or `challenge`
- Cap the brief at 15 signals total
- Do not pull transcripts for videos longer than 30 minutes — skip and note in sources
- If the transcript script fails for a video, skip it gracefully — note the failure in the sources table
- Never make action recommendations beyond the `Action` field in each signal — Jimmy decides what to act on
- Always write the output file before presenting the summary — the file is the deliverable
- If run more than once in a week, write a new timestamped file — never overwrite prior briefs

## Edge Cases

- **No YouTube results for a channel:** Skip, note "no new videos" in sources
- **Transcript unavailable:** Skip the video, note title in sources table with "no transcript"
- **WebSearch returns nothing for a keyword:** Note "no results" — don't fabricate signals
- **All videos fail transcript pull:** Proceed with web-only scout; note in brief header
- **youtube-transcript-api not installed:** Tell Jimmy to run `pip install youtube-transcript-api`; proceed with web-only scout

## Related Skills

- `research` — for deep dives on specific signals surfaced by the scout
- `compliance-gate` — if a `warning` signal implies a gate review is needed
- `task-manager` — to log `adopt` recommendations as tasks for follow-up
