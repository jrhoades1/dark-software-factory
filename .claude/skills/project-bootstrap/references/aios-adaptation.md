# AIOS Adaptation Pattern

When bootstrapping a new client project, pull reusable infrastructure from AIOS (`C:\Users\Tracy\Projects\AIOS`). This eliminates setup time for hooks, memory, skills, and guardrails.

## What to Pull from AIOS

### Always (every project)

| Component | Source | Adapt |
|-----------|--------|-------|
| Guardrail hook | `hooks/guardrail_check.py` | Add project-specific protected files |
| Memory capture hook | `hooks/memory_capture.py` | Works as-is |
| Output validation hook | `hooks/validate_output.py` | Works as-is |
| Settings template | `.claude/settings.local.json.example` | Add project-specific permissions |
| Memory protocol | `.claude/rules/memory-protocol.md` | Works as-is |
| Guardrails rules | `.claude/rules/guardrails.md` | Add project-specific rules |

### When Applicable

| Component | Source | When |
|-----------|--------|------|
| Skill patterns | `.claude/skills/skill-creator/references/patterns.md` | Project needs custom skills |
| Agent definitions | `.claude/agents/` | Project needs specialized subagents |
| Context structure | `context/my-voice.md`, `context/my-business.md` | Client-facing projects |
| Session status script | Adapt from HL `hooks/session_status.py` | Projects with daily log + task tracking |
| Preferences config | `args/preferences.yaml` | Projects needing runtime behavior tuning |
| E2E test setup | `.claude/skills/e2e-testing/references/` | Any project with a web UI |

## Adaptation Checklist

1. Copy hooks into `hooks/` directory
2. Create `.claude/settings.local.json` wiring hooks to lifecycle events
3. Create `memory/` and `memory/logs/` directories
4. Create `context/` with project-specific context files
5. Create `.claude/rules/` with guardrails + memory protocol
6. If project needs skills: create `.claude/skills/{name}/SKILL.md` using patterns from AIOS skill-creator
7. If project needs voice consistency: create `context/[domain]-voice.md`

## Proven in Production

- **Higher Landing (HL-PILOT)**: Full adaptation — hooks, skills (coaching-session, brand-synthesis), voice guide, context files, memory system
- Pattern: ~30 min to adapt AIOS infra to new project vs. building from scratch
