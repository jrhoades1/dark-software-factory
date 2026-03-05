# Guardrails

Safety rules that apply across all skills and sessions.

## Destructive Actions
- Never delete files, databases, or resources without explicit user confirmation
- Never run `rm -rf`, `git push --force`, or `git reset --hard` without confirmation
- Never drop database tables without confirmation
- Never use `--no-verify` to skip git hooks
- Preserve intermediate outputs before retrying failed workflows

## Security
- Never expose API keys, tokens, or credentials in output
- Never commit .env files or credentials to git
- Never log sensitive data to daily logs or MEMORY.md
- Never hardcode secrets — use .env or vault

## Protected Files
These files must never be deleted or overwritten without explicit confirmation:
- `.env`, `credentials.json`, `token.json`
- `CLAUDE.md`, `memory/MEMORY.md`
- `billing.json`, `.claude/project-code.txt`
- `requirements/` (approved requirement specs)

## External Communications
- Never send emails, Slack messages, or any external communication without user confirmation
- Never post to social media without user review and approval
- Never make API calls that create, modify, or delete external resources without confirmation

## Downloads Folder — Ephemeral Source
- Files in `~/Downloads` may be deleted at any time by the user or system
- When a file from Downloads is referenced or needed, **immediately copy it into the project** before processing
- Never rely on a Downloads path as a persistent reference — treat it as a one-time pickup location
- Store copied files in the appropriate project directory (e.g., `communications/`, `context/`, `data/`)
- This applies to ALL projects, not just the current one

## Data Integrity
- Verify script output format before chaining into another script
- Don't assume APIs support batch operations — check documentation first
- When a workflow fails mid-execution, preserve intermediate outputs before retrying
- When uncertain about intent, ask rather than guess
