# Stack Defaults — Opinionated Choices

Reference for the project-bootstrap skill. These are strong defaults — override
any of them, but have a reason.

## Decision Matrix

| Need | Default Choice | Why | Override when |
|------|---------------|-----|---------------|
| **Backend framework** | FastAPI (Python) | Type safety, async, auto-docs, fast | Team is JS-native → Next.js API routes |
| **Frontend framework** | Next.js 14+ (App Router) | SSR, RSC, file-based routing | Pure API → skip frontend |
| **Database** | PostgreSQL 16 | RLS, JSONB, mature, free | Document-heavy → add MongoDB alongside |
| **ORM** | SQLAlchemy (Python) / Prisma (TS) | Type-safe, migration support | Simple CRUD → raw SQL is fine |
| **Auth** | JWT + refresh rotation | Stateless, scalable | Enterprise SSO → add SAML/OIDC |
| **Validation** | Pydantic (Python) / Zod (TS) | Runtime type checking, schema gen | — |
| **CSS** | Tailwind CSS | Utility-first, no naming debates | Design system exists → use it |
| **UI components** | shadcn/ui | Copy-paste, customizable, accessible | Existing component library → use it |
| **Testing** | pytest (Python) / Vitest (TS) | Fast, good DX, good ecosystem | — |
| **Linting** | Ruff (Python) / ESLint + Prettier (TS) | Fast, opinionated | — |
| **Type checking** | mypy strict (Python) / TS strict | Catch bugs before runtime | — |
| **Container** | Docker + docker-compose | Reproducible local dev | Cloud-native → add K8s manifests |
| **CI/CD** | GitHub Actions | Integrated with GitHub | GitLab → GitLab CI |
| **Secrets** | .env (local) / cloud vault (prod) | Simple to start, secure to scale | — |
| **Monitoring** | Structured logging → Datadog/Grafana | Start with logs, add metrics | — |

---

## Stack Profiles

### Profile: Python Backend API

Best for: Data-heavy backends, AI/ML features, microservices.

```
Framework:    FastAPI
Language:     Python 3.12+
Database:     PostgreSQL 16 via SQLAlchemy 2.0
Validation:   Pydantic v2
Auth:         python-jose (JWT) + passlib (bcrypt)
Testing:      pytest + pytest-asyncio + pytest-cov
Linting:      Ruff (replaces Black, isort, flake8)
Type check:   mypy --strict
HTTP client:  httpx
Task queue:   Celery + Redis (if needed)
Migrations:   Alembic
```

### Profile: Full-Stack TypeScript

Best for: Interactive web apps, real-time features, small teams.

```
Framework:    Next.js 14+ (App Router)
Language:     TypeScript (strict: true)
Database:     PostgreSQL 16 via Prisma
Validation:   Zod
Auth:         NextAuth.js or Clerk
Testing:      Vitest + @testing-library/react + Playwright
Linting:      ESLint + Prettier
UI:           Tailwind CSS + shadcn/ui
State:        React Server Components + Zustand (if needed)
API:          Next.js Route Handlers or tRPC
```

### Profile: Minimal / Script / Tool

Best for: CLI tools, scripts, small utilities.

```
Language:     Python 3.12+ or Node.js 20+
Testing:      pytest or Vitest
Linting:      Ruff or ESLint
Structure:    Flat (src/ + tests/ + scripts/)
No framework, no database, no auth.
```

---

## Package Selection Criteria

Before adding ANY dependency, verify:

```
[ ] Maintained? (last commit < 6 months)
[ ] Popular? (>1000 weekly downloads for niche, >10K for common)
[ ] Secure? (no open CVEs, npm audit / pip-audit clean)
[ ] Licensed? (MIT, Apache 2.0, or BSD preferred)
[ ] Necessary? (can standard library do this?)
[ ] Typed? (TypeScript types or Python type stubs available)
```

### Red flags — do not install

- Last commit >12 months ago
- Single maintainer with no succession plan
- Known unpatched CVEs
- Copyleft license in commercial project (GPL)
- Does more than you need (kitchen-sink packages)
- Requires native compilation on every platform

---

## Environment Setup

### Local development

```yaml
# docker-compose.yml (all profiles)
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: appname
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

volumes:
  pgdata:
```

### Environment variables

```bash
# .env.example — template for all projects
DATABASE_URL=postgresql://dev:dev@localhost:5432/appname
REDIS_URL=redis://localhost:6379
JWT_SECRET=change-me-in-production-use-openssl-rand-hex-32
APP_ENV=development
LOG_LEVEL=debug
```

Generate secrets properly:
```bash
# Generate a secure JWT secret
openssl rand -hex 32
```
