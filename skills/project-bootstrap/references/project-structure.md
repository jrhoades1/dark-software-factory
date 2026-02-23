# Manual Project Structure Setup

Reference for the project-bootstrap skill when the bootstrap.py script isn't
available or the user wants to understand the structure before scaffolding.

## Standard project layout

```
project-name/
├── CLAUDE.md                  # AI instructions (most important file)
├── CLAUDE.project.md          # Project-specific overrides (optional)
├── README.md                  # Human-readable overview
├── .env.example               # Environment variable template
├── .gitignore                 # Git exclusions
├── .pre-commit-config.yaml    # Pre-commit hooks
├── docker-compose.yml         # Local dev services
│
├── src/
│   ├── api/                   # Backend API layer
│   │   ├── README.md          # API context for Claude
│   │   ├── main.py            # Application entry point
│   │   ├── routes/            # Route handlers (one file per resource)
│   │   │   ├── README.md
│   │   │   ├── users.py
│   │   │   └── health.py
│   │   ├── middleware/         # Auth, validation, logging, errors
│   │   │   ├── README.md
│   │   │   ├── auth.py
│   │   │   └── validation.py
│   │   └── services/          # Business logic (no framework deps)
│   │       ├── README.md
│   │       └── user_service.py
│   │
│   ├── models/                # Database models / ORM
│   │   ├── README.md
│   │   └── user.py
│   │
│   ├── schemas/               # Request/response schemas (Pydantic/Zod)
│   │   ├── README.md
│   │   └── user.py
│   │
│   └── shared/                # Cross-cutting concerns
│       ├── README.md
│       ├── types/             # Shared type definitions
│       └── utils/             # Utility functions
│
├── tests/                     # Mirror src/ structure
│   ├── README.md
│   ├── conftest.py            # Shared fixtures
│   ├── unit/
│   │   └── test_user_service.py
│   ├── integration/
│   │   └── test_user_api.py
│   └── e2e/
│
├── scripts/                   # Automation scripts
│   ├── README.md
│   ├── seed.py               # Database seed data
│   └── migrate.sh            # Migration helper
│
├── docs/
│   └── decisions/            # Architecture Decision Records
│       └── 001-template.md
│
└── alembic/                  # Database migrations (Python)
    ├── env.py
    └── versions/
```

## Directory rules

### Maximum nesting: 2 levels from src/

```
# Good
src/api/routes/users.py
src/api/middleware/auth.py

# Bad — too deep
src/api/v1/routes/users/handlers/create.py
```

### README.md at every directory level

Every directory with 3+ files gets a README.md explaining:
- What this directory contains
- How files are organized
- Key conventions specific to this directory

This is critical for AI-assisted development — Claude reads READMEs for context
before diving into individual files.

### One module per file

```
# Good
src/api/services/user_service.py    # All user business logic
src/api/services/order_service.py   # All order business logic

# Bad — monolith file
src/api/services/index.py           # Everything crammed in one file

# Bad — over-split
src/api/services/user/create.py
src/api/services/user/read.py
src/api/services/user/update.py
src/api/services/user/delete.py
```

### Tests mirror src/

```
src/api/services/user_service.py
→ tests/unit/test_user_service.py

src/api/routes/users.py
→ tests/integration/test_user_api.py
```

---

## Full-Stack TypeScript layout

```
project-name/
├── CLAUDE.md
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── package.json
├── tsconfig.json
│
├── src/
│   ├── app/                   # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── (auth)/           # Auth route group
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   └── api/              # API Route Handlers
│   │       ├── health/route.ts
│   │       └── users/route.ts
│   │
│   ├── components/
│   │   ├── ui/               # shadcn/ui components
│   │   ├── layout/           # Layout components
│   │   └── forms/            # Form components
│   │
│   ├── lib/                  # Utilities, API clients
│   ├── hooks/                # Custom React hooks
│   ├── types/                # TypeScript type definitions
│   └── services/             # Business logic
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── public/                   # Static assets
├── scripts/
└── docs/decisions/
```

---

## Minimal layout (scripts, CLIs, tools)

```
project-name/
├── CLAUDE.md
├── README.md
├── .gitignore
├── src/
│   ├── main.py              # Entry point
│   └── utils.py             # Helpers
├── tests/
│   └── test_main.py
└── scripts/
```

---

## Manual setup commands

### Python project

```bash
mkdir -p project-name/{src/api/{routes,middleware,services},src/models,src/schemas,src/shared/{types,utils},tests/{unit,integration,e2e},scripts,docs/decisions}

cd project-name
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn[standard] sqlalchemy[asyncio] pydantic-settings
pip install pytest pytest-asyncio pytest-cov ruff mypy pip-audit

# Create essential files
touch src/__init__.py src/api/__init__.py
cp /path/to/.env.example .env.example
cp /path/to/.gitignore .gitignore

git init
git add .
git commit -m "Initial project scaffold"
```

### TypeScript project

```bash
npx create-next-app@latest project-name \
  --typescript --tailwind --eslint --app --src-dir --import-alias '@/*'

cd project-name
npm install zod @tanstack/react-query
npm install -D vitest @testing-library/react prettier

mkdir -p tests/{unit,integration,e2e} scripts docs/decisions
```
