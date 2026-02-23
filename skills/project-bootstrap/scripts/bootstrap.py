#!/usr/bin/env python3
"""
Dark Software Factory — Project Bootstrap Script

Scaffolds a new project with opinionated defaults, quality gates,
and AI-ready structure (README files at every level, CLAUDE.md template).

Usage:
    python3 bootstrap.py --name my-project --stack nextjs --output-dir ./
    python3 bootstrap.py --name my-api --stack fastapi --output-dir ./
    python3 bootstrap.py --interactive
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# ─── Stack Configurations ────────────────────────────────────────────────────

STACKS = {
    "nextjs": {
        "label": "Next.js (Full-Stack TypeScript)",
        "dirs": [
            "src/app/(auth)", "src/app/api", "src/app/dashboard",
            "src/components/ui", "src/components/layout", "src/components/forms",
            "src/lib", "src/hooks", "src/types", "src/services",
            "tests/unit", "tests/integration", "tests/e2e",
            "scripts", "docs/decisions", "public"
        ],
        "init_cmd": "npx create-next-app@latest {name} --typescript --tailwind --eslint --app --src-dir --import-alias '@/*' --no-git",
        "deps": [],
        "dev_deps": ["vitest", "@testing-library/react", "prettier"],
        "dev_cmd": "npm run dev",
        "test_cmd": "npx vitest run",
        "lint_cmd": "npx eslint . --ext .ts,.tsx",
    },
    "fastapi": {
        "label": "FastAPI (Python Backend)",
        "dirs": [
            "src/api/routes", "src/api/middleware", "src/api/services",
            "src/models", "src/schemas", "src/shared/types", "src/shared/utils",
            "tests/unit", "tests/integration", "tests/e2e",
            "scripts", "docs/decisions", "alembic/versions"
        ],
        "init_cmd": None,
        "deps": ["fastapi", "uvicorn[standard]", "sqlalchemy[asyncio]", "alembic",
                 "pydantic-settings", "python-jose[cryptography]", "passlib[bcrypt]",
                 "httpx", "psycopg2-binary"],
        "dev_deps": ["pytest", "pytest-asyncio", "pytest-cov", "ruff", "mypy",
                     "pip-audit", "pre-commit"],
        "dev_cmd": "uvicorn src.api.main:app --reload",
        "test_cmd": "pytest --cov=src --cov-report=term-missing",
        "lint_cmd": "ruff check . && mypy src/",
    },
    "minimal": {
        "label": "Minimal (structure only, no framework)",
        "dirs": [
            "src", "tests", "scripts", "docs/decisions"
        ],
        "init_cmd": None,
        "deps": [],
        "dev_deps": [],
        "dev_cmd": "echo 'No dev server configured'",
        "test_cmd": "echo 'No test runner configured'",
        "lint_cmd": "echo 'No linter configured'",
    }
}

# ─── Templates ───────────────────────────────────────────────────────────────

CLAUDE_MD_TEMPLATE = """# {name}

{description}

## Architecture

<!-- TODO: Add architecture diagram -->

### Key components
- **API**: Backend service (`src/api/`)
- **UI**: Frontend application (`src/ui/` or `src/app/`)
- **Shared**: Common types and utilities (`src/shared/`)

### Data flow
<!-- TODO: Describe how data moves through the system -->

## Conventions

### Naming
- Files: kebab-case
- Components: PascalCase
- Database tables: snake_case, plural
- API endpoints: /api/v1/resource-name
- Environment variables: SCREAMING_SNAKE_CASE

### File organization
- One module per file
- Maximum directory nesting: 2 levels
- Every directory with 3+ files gets a README.md
- Tests mirror the src/ directory structure

## Commands

### Development
```bash
{dev_cmd}
```

### Testing
```bash
{test_cmd}
```

### Linting
```bash
{lint_cmd}
```

## Constraints

### Security
- No secrets in code — use environment variables
- All API endpoints require authentication (except health check)
- Input validation on every endpoint

### Performance
- API response time < 200ms p95
- No N+1 queries

## Current State

### Built and working
- Project scaffolding with quality gates
- Development environment configuration

### In progress
- <!-- TODO: Add current work items -->

### Planned
- <!-- TODO: Add planned features -->

## Environment Variables
| Variable | Purpose | Required | Default |
|---|---|---|---|
| DATABASE_URL | PostgreSQL connection string | Yes | — |
| JWT_SECRET | Token signing key | Yes | — |
| NODE_ENV / PYTHON_ENV | Environment | No | development |
"""

ENV_EXAMPLE_TEMPLATE = """# {name} Environment Variables
# Copy this to .env and fill in values
# NEVER commit .env to version control

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/{name_snake}

# Auth
JWT_SECRET=change-me-in-production
JWT_EXPIRY=3600

# App
APP_ENV=development
APP_PORT=3000
LOG_LEVEL=debug
"""

DOCKER_COMPOSE_TEMPLATE = """version: '3.8'

services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: {name_snake}
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d {name_snake}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
"""

GITIGNORE_TEMPLATE = """# Environment
.env
.env.local
.env.*.local

# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# Build
dist/
build/
.next/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.coverage
htmlcov/

# Logs
*.log
logs/
"""

PRE_COMMIT_CONFIG = """repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: detect-private-key
"""

# ─── Core Logic ──────────────────────────────────────────────────────────────

def create_project(name: str, stack: str, output_dir: str, description: str = ""):
    """Scaffold a complete Dark Software Factory project."""
    
    config = STACKS[stack]
    project_path = Path(output_dir) / name
    name_snake = name.replace("-", "_")
    
    print(f"\n🏭 Dark Software Factory — Bootstrapping '{name}' ({config['label']})")
    print(f"   Target: {project_path.resolve()}\n")
    
    # Create project root
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Create directory structure
    print("📁 Creating directory structure...")
    for dir_path in config["dirs"]:
        (project_path / dir_path).mkdir(parents=True, exist_ok=True)
    
    # Generate README files at every directory level
    print("📝 Generating README files...")
    generate_readmes(project_path)
    
    # Generate root files
    print("📄 Generating root configuration files...")
    
    # CLAUDE.md
    desc = description or f"A {config['label']} application bootstrapped with the Dark Software Factory."
    (project_path / "CLAUDE.md").write_text(
        CLAUDE_MD_TEMPLATE.format(
            name=name,
            description=desc,
            dev_cmd=config["dev_cmd"],
            test_cmd=config["test_cmd"],
            lint_cmd=config["lint_cmd"],
        )
    )
    
    # README.md
    (project_path / "README.md").write_text(
        f"# {name}\n\n{desc}\n\n"
        f"## Quick Start\n\n"
        f"```bash\n"
        f"cp .env.example .env\n"
        f"docker-compose up -d\n"
        f"{config['dev_cmd']}\n"
        f"```\n\n"
        f"## Development\n\n"
        f"See [CLAUDE.md](./CLAUDE.md) for detailed development instructions.\n"
    )
    
    # .env.example
    (project_path / ".env.example").write_text(
        ENV_EXAMPLE_TEMPLATE.format(name=name, name_snake=name_snake)
    )
    
    # docker-compose.yml
    (project_path / "docker-compose.yml").write_text(
        DOCKER_COMPOSE_TEMPLATE.format(name_snake=name_snake)
    )
    
    # .gitignore
    (project_path / ".gitignore").write_text(GITIGNORE_TEMPLATE)
    
    # .pre-commit-config.yaml
    (project_path / ".pre-commit-config.yaml").write_text(PRE_COMMIT_CONFIG)
    
    # Stack-specific initialization
    if stack == "fastapi":
        generate_fastapi_files(project_path, name, name_snake)
    elif stack == "nextjs":
        generate_nextjs_markers(project_path, name)
    
    # Generate ADR template
    print("📋 Creating Architecture Decision Record template...")
    generate_adr_template(project_path)
    
    # Initialize git
    print("🔧 Initializing git repository...")
    subprocess.run(["git", "init"], cwd=project_path, capture_output=True)
    
    # Summary
    print(f"\n✅ Project '{name}' bootstrapped successfully!")
    print(f"\n   Next steps:")
    print(f"   1. cd {project_path}")
    print(f"   2. cp .env.example .env  (and fill in values)")
    print(f"   3. docker-compose up -d  (start database)")
    print(f"   4. {config['dev_cmd']}")
    print(f"   5. Update CLAUDE.md with your specific project details")
    print()
    
    return project_path


def generate_readmes(project_path: Path):
    """Create README.md files at every directory level for AI context."""
    for dirpath, dirnames, filenames in os.walk(project_path):
        # Skip hidden dirs and node_modules
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
        
        rel_path = Path(dirpath).relative_to(project_path)
        if str(rel_path) == '.':
            continue
        
        readme_path = Path(dirpath) / "README.md"
        if not readme_path.exists():
            dir_name = Path(dirpath).name
            purpose = infer_directory_purpose(str(rel_path))
            readme_path.write_text(f"# {dir_name}\n\n{purpose}\n")


def infer_directory_purpose(rel_path: str) -> str:
    """Infer the purpose of a directory from its path for README generation."""
    purposes = {
        "src": "Application source code.",
        "src/api": "Backend API layer — routes, middleware, and business logic services.",
        "src/api/routes": "API route handlers. One file per resource (e.g., `users.py`, `orders.py`).",
        "src/api/middleware": "Express/FastAPI middleware — authentication, validation, logging, error handling.",
        "src/api/services": "Business logic layer. Framework-agnostic — no HTTP concepts here.",
        "src/models": "Database models / ORM definitions.",
        "src/schemas": "Pydantic models / request-response schemas for API validation.",
        "src/shared": "Code shared across the application — types, constants, utilities.",
        "src/shared/types": "TypeScript types / Python type definitions shared across modules.",
        "src/shared/utils": "Utility functions used across the application.",
        "src/ui": "Frontend application code.",
        "src/ui/components": "Reusable UI components. Flat structure — avoid nesting beyond 2 levels.",
        "src/ui/pages": "Page-level components / route views.",
        "src/app": "Next.js App Router pages and layouts.",
        "src/components": "Reusable UI components.",
        "src/hooks": "Custom React hooks.",
        "src/lib": "Library code, API clients, and third-party integrations.",
        "src/services": "Business logic and data access services.",
        "src/types": "TypeScript type definitions.",
        "tests": "Test suite — mirrors src/ directory structure.",
        "tests/unit": "Unit tests — isolated function and module tests.",
        "tests/integration": "Integration tests — tests that involve multiple modules or external services.",
        "tests/e2e": "End-to-end tests — full user flow tests.",
        "scripts": "Automation scripts — migrations, seeds, deployments, data processing.",
        "docs": "Project documentation.",
        "docs/decisions": "Architecture Decision Records (ADRs). See `001-template.md`.",
        "alembic": "Database migration configuration (SQLAlchemy/Alembic).",
        "alembic/versions": "Database migration files. Generated by `alembic revision`.",
        "public": "Static assets served directly (images, fonts, etc.).",
    }
    return purposes.get(rel_path, "TODO: Describe the purpose of this directory.")


def generate_fastapi_files(project_path: Path, name: str, name_snake: str):
    """Generate FastAPI-specific starter files."""
    
    # Main application
    (project_path / "src" / "api" / "main.py").write_text(f'''"""
{name} — Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="{name}",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {{"status": "healthy", "service": "{name}"}}
''')
    
    # pyproject.toml
    (project_path / "pyproject.toml").write_text(f'''[project]
name = "{name}"
version = "0.1.0"
requires-python = ">=3.11"

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "UP", "S", "B", "A", "C4", "DTZ", "T10",
          "ISC", "ICN", "PIE", "PT", "RSE", "RET", "SLF", "SIM", "TID", "TCH",
          "ARG", "PTH", "ERA"]

[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "--cov=src --cov-report=term-missing"
''')
    
    # requirements.txt
    deps = STACKS["fastapi"]["deps"] + STACKS["fastapi"]["dev_deps"]
    (project_path / "requirements.txt").write_text("\n".join(deps) + "\n")
    
    # __init__.py files
    for init_dir in ["src", "src/api", "src/api/routes", "src/api/middleware",
                     "src/api/services", "src/models", "src/schemas",
                     "src/shared", "src/shared/types", "src/shared/utils",
                     "tests", "tests/unit", "tests/integration"]:
        init_path = project_path / init_dir / "__init__.py"
        if init_path.parent.exists():
            init_path.touch()


def generate_nextjs_markers(project_path: Path, name: str):
    """Generate marker files for Next.js projects (actual init happens via create-next-app)."""
    (project_path / "NEXT_SETUP.md").write_text(
        f"# Next.js Setup\n\n"
        f"This project was scaffolded by the Dark Software Factory.\n\n"
        f"If `create-next-app` wasn't run automatically, run:\n"
        f"```bash\n"
        f"npx create-next-app@latest {name} --typescript --tailwind --eslint "
        f"--app --src-dir --import-alias '@/*'\n"
        f"```\n\n"
        f"Then merge the generated files with this directory structure.\n"
    )


def generate_adr_template(project_path: Path):
    """Create an ADR template in docs/decisions/."""
    adr_dir = project_path / "docs" / "decisions"
    adr_dir.mkdir(parents=True, exist_ok=True)
    
    (adr_dir / "001-template.md").write_text(
        "# ADR-001: [Title]\n\n"
        "## Status\nProposed | Accepted | Deprecated | Superseded\n\n"
        "## Context\nWhat is the issue that we're seeing that is motivating this decision?\n\n"
        "## Decision\nWhat is the change that we're proposing and/or doing?\n\n"
        "## Consequences\nWhat becomes easier or more difficult to do because of this change?\n"
    )


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Dark Software Factory — Project Bootstrap"
    )
    parser.add_argument("--name", required=True, help="Project name (kebab-case)")
    parser.add_argument("--stack", choices=list(STACKS.keys()), default="fastapi",
                       help="Technology stack")
    parser.add_argument("--output-dir", default=".", help="Parent directory for the project")
    parser.add_argument("--description", default="", help="One-line project description")
    
    args = parser.parse_args()
    create_project(args.name, args.stack, args.output_dir, args.description)


if __name__ == "__main__":
    main()
