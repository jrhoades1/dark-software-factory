# CLAUDE.md Template

Copy this template to the root of every new project and fill in the sections.
This is the most important file for AI-assisted development — it's what Claude
reads first.

---

```markdown
# [Project Name]

[One paragraph: what this is, who it's for, what it does. Be specific.]

## Architecture

<!-- Diagram or description of how the pieces connect -->

### Key components
- **API**: [What it does, where it lives] (`src/api/`)
- **UI**: [What it does, where it lives] (`src/app/` or `src/ui/`)
- **Shared**: [Common types, utilities] (`src/shared/`)
- **Database**: [PostgreSQL, tables, key relationships]

### Data flow
<!-- How data moves: User → UI → API → DB → API → UI -->

## Conventions

### Naming
- Files: kebab-case (`user-service.ts`, `auth_middleware.py`)
- Components: PascalCase (`UserProfile.tsx`)
- Database tables: snake_case, plural (`user_profiles`)
- API endpoints: `/api/v1/resource-name`
- Environment variables: SCREAMING_SNAKE_CASE

### File organization
- One module per file
- Maximum directory nesting: 2 levels from src/
- Every directory with 3+ files gets a README.md
- Tests mirror the src/ directory structure

### Import patterns
<!-- Project-specific import conventions -->

## Commands

### Development
```bash
[exact command to start dev server]
```

### Testing
```bash
[exact command to run tests]
```

### Linting / Type checking
```bash
[exact lint and type check commands]
```

### Database migrations
```bash
[exact migration commands]
```

### Deployment
```bash
[exact deployment steps]
```

## Constraints

### Security (non-negotiable)
- No secrets in code — use environment variables
- All API endpoints require authentication (except health check)
- Input validation on every endpoint (Pydantic/Zod)
- Parameterized queries only
- RLS enabled on all user-data tables

### Performance
- API response time < 200ms p95
- No N+1 queries
- Pagination on all list endpoints (max 100 items)

### Compliance
<!-- HIPAA, GDPR, SOC 2 — list what applies -->

## Current State

### Built and working
- [List what's complete and functional]

### In progress
- [List current work items]

### Planned
- [List upcoming features]

### Known issues
- [List known bugs or tech debt]

## Environment Variables

| Variable | Purpose | Required | Default |
|---|---|---|---|
| DATABASE_URL | PostgreSQL connection string | Yes | — |
| JWT_SECRET | Token signing key | Yes | — |
| APP_ENV | Environment | No | development |
| LOG_LEVEL | Logging verbosity | No | info |

## Dependencies

### Key packages and why
| Package | Purpose | Version |
|---|---|---|
<!-- List the important ones, not every transitive dependency -->

## Testing Strategy

### Unit tests
- [Where they live, what they cover]

### Integration tests
- [Where they live, what they cover]

### E2E tests
- [Where they live, what they cover]

---

*Last updated: [date]*
*Maintained by: [team/person]*
```

---

## Tips for effective CLAUDE.md files

1. **Be specific** — "Run `npm run dev`" not "start the dev server"
2. **Keep it current** — Stale CLAUDE.md is worse than no CLAUDE.md
3. **Focus on what's non-obvious** — Don't document standard framework behavior
4. **Include constraints** — Claude needs to know what NOT to do
5. **List current state** — Claude needs to know what exists before proposing changes
6. **Update after every major change** — Part of the definition of done
