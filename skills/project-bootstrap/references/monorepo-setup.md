# Monorepo Setup Guide

Reference for the project-bootstrap skill when projects need 3+ services.

## When to use a monorepo

- 3+ services that share types/utilities
- Frontend + backend + shared library
- Multiple microservices with shared contracts
- Team needs unified CI/CD and dependency management

## When NOT to use a monorepo

- Single service (use standard layout)
- 2 services with minimal sharing (use separate repos)
- Teams on different release cycles with no shared code

---

## Monorepo structure

```
project-name/
├── CLAUDE.md                     # Root CLAUDE.md (overall architecture)
├── README.md
├── docker-compose.yml            # All services for local dev
├── .env.example
├── .gitignore
│
├── packages/
│   ├── shared/                   # Shared types, utilities, contracts
│   │   ├── CLAUDE.md
│   │   ├── package.json          # or pyproject.toml
│   │   ├── src/
│   │   │   ├── types/
│   │   │   └── utils/
│   │   └── tests/
│   │
│   ├── api/                      # Backend service
│   │   ├── CLAUDE.md
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   ├── src/
│   │   │   ├── routes/
│   │   │   ├── middleware/
│   │   │   └── services/
│   │   └── tests/
│   │
│   ├── web/                      # Frontend application
│   │   ├── CLAUDE.md
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   └── src/
│   │
│   └── worker/                   # Background job processor
│       ├── CLAUDE.md
│       ├── package.json
│       ├── Dockerfile
│       └── src/
│
├── scripts/                      # Cross-service automation
│   ├── setup.sh                  # One-command dev setup
│   └── deploy.sh                 # Coordinated deployment
│
├── infra/                        # Infrastructure as code
│   ├── docker/                   # Dockerfiles for production
│   └── terraform/                # Cloud infrastructure
│
└── docs/
    └── decisions/
```

---

## TypeScript monorepo (npm workspaces)

### Root package.json

```json
{
  "name": "project-name",
  "private": true,
  "workspaces": ["packages/*"],
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "test": "turbo test",
    "lint": "turbo lint",
    "typecheck": "turbo typecheck"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.4.0"
  }
}
```

### turbo.json

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {},
    "typecheck": {
      "dependsOn": ["^build"]
    }
  }
}
```

### Shared package

```json
// packages/shared/package.json
{
  "name": "@project/shared",
  "version": "0.0.0",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "scripts": {
    "typecheck": "tsc --noEmit"
  }
}
```

### Consuming shared package

```json
// packages/api/package.json
{
  "name": "@project/api",
  "dependencies": {
    "@project/shared": "workspace:*"
  }
}
```

---

## Python monorepo (uv workspaces)

### Root pyproject.toml

```toml
[project]
name = "project-name"
version = "0.0.0"

[tool.uv.workspace]
members = ["packages/*"]

[tool.uv.sources]
shared = { workspace = true }
```

### Shared package

```toml
# packages/shared/pyproject.toml
[project]
name = "shared"
version = "0.0.0"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Consuming shared package

```toml
# packages/api/pyproject.toml
[project]
name = "api"
dependencies = ["shared"]

[tool.uv.sources]
shared = { workspace = true }
```

---

## Docker Compose for monorepo

```yaml
# docker-compose.yml
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

  api:
    build:
      context: .
      dockerfile: packages/api/Dockerfile
    ports: ["8000:8000"]
    depends_on: [db, redis]
    environment:
      DATABASE_URL: postgresql://dev:dev@db:5432/appname
      REDIS_URL: redis://redis:6379
    volumes:
      - ./packages/api/src:/app/src
      - ./packages/shared/src:/shared/src

  web:
    build:
      context: .
      dockerfile: packages/web/Dockerfile
    ports: ["3000:3000"]
    depends_on: [api]
    environment:
      API_URL: http://api:8000
    volumes:
      - ./packages/web/src:/app/src

  worker:
    build:
      context: .
      dockerfile: packages/worker/Dockerfile
    depends_on: [db, redis]
    environment:
      DATABASE_URL: postgresql://dev:dev@db:5432/appname
      REDIS_URL: redis://redis:6379

volumes:
  pgdata:
```

---

## CI/CD for monorepo

### GitHub Actions with path-based triggers

```yaml
# .github/workflows/api.yml
name: API CI
on:
  pull_request:
    paths:
      - 'packages/api/**'
      - 'packages/shared/**'  # Shared changes affect all consumers

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx turbo test --filter=@project/api
```

### Turborepo handles dependency-aware builds

```bash
# Only build/test packages affected by changes
npx turbo test --filter=...[origin/main]
```

---

## Key monorepo rules

1. **Shared package is a dependency, not a dump** — Only put genuinely shared code there
2. **Each package has its own CLAUDE.md** — Claude needs per-service context
3. **One docker-compose.yml at root** — Local dev starts everything with one command
4. **Version together** — Unless services are truly independent, ship them together
5. **Shared types are the contract** — API contracts live in shared, both sides import
