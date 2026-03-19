# Quality Gates — Automated Checks

Reference for the project-bootstrap skill. Configure these before the first commit.

## Pre-commit Hooks

### Setup

```bash
pip install pre-commit   # Python projects
npm install husky --save-dev  # JS projects

# Initialize
pre-commit install       # Python
npx husky init           # JS
```

### .pre-commit-config.yaml (Python projects)

```yaml
repos:
  # Secret detection (CRITICAL — catches leaked keys before commit)
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  # General hygiene
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: detect-private-key
      - id: check-merge-conflict

  # Python linting + formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### Husky + lint-staged (JS/TS projects)

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged
npx gitleaks detect --staged
```

---

## Pre-push Hook (E2E gate)

Pre-commit hooks catch formatting and secrets. Pre-push hooks catch broken builds and
failing E2E tests **before they reach CI**. This is non-negotiable for any project with
real users — a developer should never find out about test failures from a CI email.

### Setup

Create `hooks/pre-push` in the project root (tracked in git):

```bash
#!/bin/bash
# Pre-push hook: lint, build, and E2E must pass before pushing.
# Skip with: git push --no-verify (only when you know what you're doing)
set -e

echo "Pre-push: running lint + build + E2E..."

cd app  # adjust to your project's app directory

npm run lint || { echo "Lint failed. Fix errors before pushing."; exit 1; }
npm run build || { echo "Build failed. Fix errors before pushing."; exit 1; }
npx playwright test || { echo "E2E tests failed. Fix before pushing."; exit 1; }

echo "All checks passed. Pushing."
```

Create `hooks/setup-hooks.sh` to install:

```bash
#!/bin/bash
# Run once after cloning: bash hooks/setup-hooks.sh
HOOKS_DIR="$(cd "$(dirname "$0")" && pwd)"
GIT_HOOKS_DIR="$(git rev-parse --show-toplevel)/.git/hooks"

echo "Installing git hooks..."
for hook in pre-push; do
  if [ -f "$HOOKS_DIR/$hook" ]; then
    cp "$HOOKS_DIR/$hook" "$GIT_HOOKS_DIR/$hook"
    chmod +x "$GIT_HOOKS_DIR/$hook"
    echo "  installed $hook"
  fi
done
echo "Done."
```

Add to project README / CLAUDE.md under setup: `bash hooks/setup-hooks.sh`

**Why pre-push instead of pre-commit for E2E?** Pre-commit runs on every commit — E2E
suites take minutes, which kills flow. Pre-push runs once before sharing, which is the
right gate. CI is the backup, not the primary check.

---

## Deploy Awareness (user-facing projects)

Any project with real users must include a deploy-awareness system so users never see
raw "couldn't connect" errors during Vercel/Netlify/etc deployments.

**Pattern:**
1. Add a `MaintenanceBanner` component that listens for API failures
2. On failure, show "System is updating — hang tight" with auto-recovery polling
3. Poll `/api/health` every 3s until healthy, then auto-dismiss
4. Wire all API catch blocks to signal the banner via a custom event

This was learned the hard way: a client reported a "broken" coaching tool that was
actually just a 60-second deploy window. Users don't know what a deploy is.

---

## Linting Configuration

### Ruff (Python) — replaces Black, isort, flake8, and more

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "W",    # pycodestyle warnings
    "UP",   # pyupgrade
    "S",    # bandit (security)
    "B",    # bugbear
    "A",    # builtins
    "C4",   # comprehensions
    "DTZ",  # datetime (timezone-aware)
    "T10",  # debugger
    "ISC",  # implicit string concatenation
    "ICN",  # import conventions
    "PIE",  # misc lints
    "PT",   # pytest style
    "RSE",  # raise
    "RET",  # return
    "SLF",  # self
    "SIM",  # simplify
    "TID",  # tidy imports
    "TCH",  # type checking
    "ARG",  # unused arguments
    "PTH",  # pathlib
    "ERA",  # commented-out code
]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]  # Allow assert in tests
```

### ESLint (TypeScript)

```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/strict-type-checked",
    "plugin:@typescript-eslint/stylistic-type-checked",
    "next/core-web-vitals",
    "prettier"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": "error",
    "no-console": "warn"
  }
}
```

---

## Type Checking

### mypy (Python)

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
check_untyped_defs = true
no_implicit_optional = true
```

### TypeScript

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "exactOptionalPropertyTypes": true
  }
}
```

---

## Security Scanning

### Dependency audit

```bash
# Python
pip-audit --strict --desc

# JavaScript
npm audit --audit-level=high
```

### Static analysis (security-focused)

```bash
# Python — bandit (included in Ruff S rules)
bandit -r src/ -f json -o bandit-report.json

# Multi-language
semgrep --config=auto --error .
```

### Secret scanning

```bash
# Pre-commit (catches before commit)
gitleaks detect --staged

# Full repo scan
gitleaks detect --source . --report-format json --report-path gitleaks.json

# CI pipeline
trufflehog filesystem . --only-verified
```

---

## CI Pipeline Template

### GitHub Actions (Python)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint
        run: ruff check .

      - name: Format check
        run: ruff format --check .

      - name: Type check
        run: mypy src/

      - name: Security scan
        run: |
          pip-audit --strict
          bandit -r src/ -f json

      - name: Secret scan
        run: |
          pip install gitleaks || true
          gitleaks detect --source . --no-git

      - name: Test
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

### GitHub Actions (TypeScript)

```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - run: npm ci
      - run: npx eslint .
      - run: npx prettier --check .
      - run: npx tsc --noEmit
      - run: npm audit --audit-level=high
      - run: npx vitest run --coverage
```

---

## Definition of Done — Quality Checklist

Before any PR is merged:

```
[ ] All lint rules pass (zero warnings)
[ ] Type checking passes
[ ] All tests pass
[ ] Coverage not decreased
[ ] Dependency audit clean
[ ] Secret scan clean
[ ] CLAUDE.md updated (if architecture changed)
[ ] README updated (if user-facing behavior changed)
```
