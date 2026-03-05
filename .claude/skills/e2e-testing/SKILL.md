---
name: e2e-testing
description: >
  Set up and run Playwright E2E tests for any web application. Use this skill when bootstrapping
  a new project that has a web UI, when a project is ready for verification before delivery,
  or when the user asks to "test everything," "verify buttons work," "automated testing,"
  or "make sure it works before you give it to me." Also trigger when adding new features
  that need regression protection.
model: sonnet
user-invokable: true
---

# E2E Testing Skill

## Intent

Every DSF web project ships with automated end-to-end tests. No exceptions. A human should
be able to run one command and know if the app works. This skill handles setup, test creation,
and execution using Playwright.

## When to Use

- After bootstrapping any web application (pair with `project-bootstrap`)
- Before delivering a feature or milestone to a client
- When the user asks for automated testing or verification
- When adding new interactive features that need regression coverage
- When debugging a UI issue (add a failing test first, then fix)

## Stack

**Playwright** is the default E2E framework for all DSF projects. Reasons:
- Cross-browser (Chromium, Firefox, WebKit)
- Auto-waits for elements (fewer flaky tests)
- Built-in test runner with parallel execution
- Screenshot on failure for debugging
- Works with any web framework (Next.js, React, Vue, etc.)

## Process

### Step 1: Install Playwright

```bash
cd <app-directory>
npm install -D @playwright/test
npx playwright install chromium
```

Add test scripts to `package.json`:
```json
{
  "scripts": {
    "test": "npx playwright test",
    "test:ui": "npx playwright test --ui",
    "test:headed": "npx playwright test --headed"
  }
}
```

### Step 2: Create Playwright Config

Create `playwright.config.ts` in the app root:

```typescript
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30000,
  expect: { timeout: 10000 },
  fullyParallel: false,
  retries: 0,
  use: {
    baseURL: "http://localhost:3000",
    headless: true,
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { browserName: "chromium" },
    },
  ],
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000",
    reuseExistingServer: true,
    timeout: 60000,
  },
});
```

Adapt `baseURL` and `webServer.command` to match the project.

### Step 3: Create Test Structure

```
app/
  e2e/
    smoke.spec.ts       # Basic load + render tests
    navigation.spec.ts  # Route and sidebar/menu tests
    forms.spec.ts       # Input, submission, validation tests
    persistence.spec.ts # Data save/load/clear tests
    [feature].spec.ts   # Feature-specific tests
  playwright.config.ts
```

For smaller projects, a single `e2e/app.spec.ts` is fine.

### Step 4: Write Tests

Follow these patterns:

#### Test Categories (minimum coverage)

| Category | What to test | Priority |
|----------|-------------|----------|
| **Smoke** | Page loads, header visible, no console errors | Must have |
| **Navigation** | All links/buttons route correctly | Must have |
| **Forms** | Inputs render, accept data, validate | Must have |
| **Persistence** | Data survives reload (localStorage, DB) | Must have |
| **Feature** | Core business logic works end-to-end | Must have |
| **Edge cases** | Empty states, error states, boundary values | Nice to have |

#### Selector Priority

Use selectors in this order (most stable to least):
1. `getByRole("button", { name: "Submit", exact: true })` — accessible, stable
2. `getByRole("heading", { name: /title/i })` — semantic
3. `getByText("exact text").first()` — when text is unique
4. `page.locator("[data-testid='foo']")` — explicit test IDs
5. `page.locator("textarea").first()` — element type (last resort)

**IMPORTANT:** Use `exact: true` for common words like "Next", "Submit", "Save" to avoid
matching framework elements (e.g., Next.js Dev Tools button matches `/next/i`).

#### Seed Data Pattern

For apps with localStorage or DB persistence, create a seed script:

```typescript
async function seedData(page: Page) {
  await page.goto("/");
  await page.waitForLoadState("networkidle");
  await page.evaluate(() => {
    // @ts-ignore
    window.seedTestData();
  });
  await page.reload();
  await page.waitForLoadState("networkidle");
}

async function clearData(page: Page) {
  await page.goto("/");  // Must navigate FIRST — localStorage blocked on about:blank
  await page.waitForLoadState("networkidle");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.waitForLoadState("networkidle");
}
```

**Key gotcha:** You MUST `page.goto("/")` before calling `localStorage` — Playwright starts
on `about:blank` where localStorage throws `SecurityError`.

### Step 5: Run and Fix

```bash
npm test              # Headless, fast
npm run test:headed   # Watch the browser
npm run test:ui       # Interactive Playwright UI
```

Fix failures iteratively. Common issues:
- **Strict mode violation:** Selector matches multiple elements. Use `.first()`, `exact: true`, or more specific selector.
- **Timeout:** Element not rendered yet. Add `waitForLoadState("networkidle")` or `waitForTimeout()`.
- **SecurityError on localStorage:** Didn't navigate to a page first. Always `goto("/")` before `evaluate()`.

### Step 6: Add to CI (when project has CI)

```yaml
# GitHub Actions example
- name: Run E2E tests
  run: |
    npx playwright install chromium
    npm test
```

## Rules

- Every web project gets Playwright tests before delivery
- Tests must pass before telling the user "it's ready"
- Screenshot-on-failure is always enabled for debugging
- Seed data scripts are exported to `window` for manual console use too
- Never skip tests to ship faster — fix the test or fix the code
- Add `test-results/` and `playwright-report/` to `.gitignore`

## Learned Patterns (from production)

These patterns were discovered building the Higher Landing Career Transformer:

1. **Next.js Dev Tools button** matches `/next/i` — always use `{ name: "Next", exact: true }`
2. **Session titles appear in both sidebar and heading** — use `getByRole("button", ...)` for sidebar, `getByRole("heading", ...)` for content
3. **localStorage not available on `about:blank`** — always navigate before calling evaluate
4. **Hooks with relative paths break when CWD changes** — use absolute paths in settings.local.json
5. **Seed data needs `window` attachment** — export functions AND attach to window at module scope for console use
