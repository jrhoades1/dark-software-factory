# Intelligence Classification Taxonomy

Used by the intelligence-scout skill to classify every signal found during
the weekly research run.

## Classification Labels

### warning
Risks, deprecations, rate limit changes, pricing changes, or security issues.
- Affects DSF operations or client projects
- Requires action before next deployment or billing cycle
- **Always surfaces regardless of relevance score**

### capability
Claude API features, model updates, SDK changes, or Claude Code releases.
- Released or announced by Anthropic
- Changes what DSF can build or how it operates
- **Always captured regardless of relevance score**

### challenge
Contradicts an existing DSF assumption or design decision.
- Directly argues against a pattern DSF currently uses
- Source is credible (Anthropic engineering, known practitioner, published research)
- Requires review of the specific decision, not wholesale change
- **Always surfaced regardless of relevance score**

### adopt
Tool, pattern, or technique DSF should incorporate.
- Directly applicable to DSF's core workflow (skills, agents, cost tracking)
- Available now (not roadmap or beta)
- Replaces an existing pain point or adds measurable capability
- **Surfaces when relevance score >= 8**

### validate
Promising signal that needs testing before committing.
- Unconfirmed in DSF's stack (Python/SQLite/Claude SDK)
- Requires a proof-of-concept before adopting
- Single source with no cross-reference yet
- **Surfaces when relevance score >= 5**

### compete
Competing framework or tool that solves the same problem as DSF.
- Addresses AI-native development workflows or Claude Code orchestration
- Used by practitioners in similar roles
- **Tracked regardless of score — logged but not acted on urgently**

## Label Precedence

When a signal fits multiple labels, apply the highest-priority one:

1. **warning** (always first)
2. **capability** (Anthropic signals always captured)
3. **challenge** (contradictions require immediate attention)
4. **adopt** (actionable patterns)
5. **validate** (needs testing)
6. **compete** (lowest priority, tracked not acted on)

## DSF Relevance Scoring (1-10)

Score each signal against these dimensions, then normalize to 1-10.

| Dimension | Weight | Question |
|-----------|--------|----------|
| Skill impact | 3x | Does this change how skills are written or triggered? |
| Agent impact | 2x | Does this change how agents coordinate or operate? |
| Cost impact | 2x | Does this affect token costs, API pricing, or spend caps? |
| Security impact | 2x | Does this introduce or close a vulnerability class? |
| Client impact | 1x | Does this affect ALD or other client project delivery? |

**1** = no connection to DSF. **10** = directly changes an active DSF component today.

## DSF Component Mapping

Map each signal to the component it most affects:

| Component | Covers |
|-----------|--------|
| `skill-execution` | SKILL.md format, trigger phrases, frontmatter, allowed-tools |
| `agent-coordination` | Agent handoffs, context fork, subagent patterns |
| `security-layer` | citadel-workflow, security-hardening, hipaa-scaffold, compliance-gate |
| `cost-tracking` | Billing, token tracking, spend caps |
| `memory-system` | MEMORY.md, daily logs, session continuity |
| `data-layer` | SQLite schemas, task-manager, structured persistence |
| `client-ald` | ALD-SERVICETITAN, ALD-CALL-ANALYSIS deliverables |
| `dsf-meta` | DSF architecture itself, CLAUDE.md conventions |

## Per-Signal Output Format

```markdown
### [Title]
- **Label:** [warning | capability | challenge | adopt | validate | compete]
- **Score:** [1-10]
- **Component:** [component from table above]
- **Source:** [URL or channel name]
- **Summary:** [2-3 sentences]
- **Action:** [What Jimmy should do, or "Track only"]
```
