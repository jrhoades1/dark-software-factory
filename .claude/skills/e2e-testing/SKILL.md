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

For Clerk-authenticated apps, also install:
```bash
npm install -D @clerk/testing dotenv
```

Add test scripts to `package.json`:
```json
{
  "scripts": {
    "test:e2e": "npx playwright test",
    "test:e2e:ui": "npx playwright test --ui",
    "test:e2e:headed": "npx playwright test --headed"
  }
}
```

### Step 2: Create Playwright Config

See `references/playwright-config-template.ts` for the base config.

For apps with auth, use the multi-project config in `references/playwright-config-auth.ts`
which separates setup, public, and authenticated test suites.

### Step 3: Create Test Structure

```
app/
  e2e/
    global.setup.ts       # Auth setup (if using Clerk/Auth0/etc.)
    helpers.ts             # Skip helpers, shared utilities
    smoke.public.spec.ts   # Public page tests (no auth)
    dashboard.auth.spec.ts # Authenticated dashboard tests
    [page].auth.spec.ts    # Per-page authenticated tests
  playwright.config.ts
```

### Step 4: Write Tests

Follow these patterns:

#### Test Categories (minimum coverage)

| Category | What to test | Priority |
|----------|-------------|----------|
| **Smoke** | Page loads, header visible, no console errors | Must have |
| **Navigation** | All links/buttons route correctly | Must have |
| **Forms** | Inputs render, accept data, validate | Must have |
| **Auth protection** | Protected routes redirect unauthenticated users | Must have |
| **Persistence** | Data survives reload (localStorage, DB) | Must have |
| **Feature** | Core business logic works end-to-end | Must have |
| **Edge cases** | Empty states, error states, boundary values | Nice to have |

#### Selector Priority

Use selectors in this order (most stable to least):
1. `getByRole("button", { name: "Submit" })` — accessible, stable
2. `getByRole("heading", { name: /title/i })` — semantic
3. `getByText("exact text").first()` — when text is unique
4. `page.locator("[data-testid='foo']")` — explicit test IDs
5. `page.locator("textarea").first()` — element type (last resort)

**IMPORTANT:** Nav items with emojis/icons (e.g. "📊 Dashboard") — do NOT use `exact: true`
on `getByRole("link", ...)` because the accessible name includes the icon text.

#### Wait Strategy

**NEVER use `waitForLoadState("networkidle")`** for apps with WebSocket connections
(Clerk, Supabase realtime, etc.). It will timeout because the connection never goes idle.

Instead, wait for a specific element:
```typescript
// BAD — will timeout with Clerk/WebSocket apps
await page.waitForLoadState("networkidle");

// GOOD — wait for the page's heading to appear
await page.getByRole("heading", { name: "Dashboard" }).waitFor({ timeout: 15000 });
```

#### Seed Data Pattern

For apps with localStorage or DB persistence, create a seed script:

```typescript
async function seedData(page: Page) {
  await page.goto("/");
  await page.waitForLoadState("domcontentloaded");
  await page.evaluate(() => {
    // @ts-ignore
    window.seedTestData();
  });
  await page.reload();
}
```

**Key gotcha:** You MUST `page.goto("/")` before calling `localStorage` — Playwright starts
on `about:blank` where localStorage throws `SecurityError`.

### Step 5: Clerk Authentication Setup

For Clerk-authenticated apps, use the **Backend API sign-in token** approach.
This bypasses the UI entirely — no need for email/password fields or OAuth.

See `references/clerk-auth-setup.ts` for the full implementation.

**Required env vars** (in `.env.local`):
```
CLERK_SECRET_KEY=sk_test_...
E2E_CLERK_USER_USERNAME=e2e-test@yourapp.dev
E2E_CLERK_USER_PASSWORD=<password>
```

**Required Clerk setup:**
1. Create an e2e test user in Clerk Dashboard > Users
2. The sign-in token approach works regardless of which sign-in methods
   are enabled (Google-only, email+password, etc.)

### Step 6: Vitest Coexistence

If the project uses Vitest for unit tests, **exclude the e2e directory**:

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    exclude: ["e2e/**", "node_modules/**"],
  },
});
```

Playwright and Vitest both use `test()` — Vitest will try to load Playwright files
and crash with "test.beforeEach() not expected here."

### Step 7: Run and Fix

```bash
npm run test:e2e              # Headless, fast
npm run test:e2e:headed       # Watch the browser
npm run test:e2e:ui           # Interactive Playwright UI
```

Fix failures iteratively. Common issues:
- **Strict mode violation:** Selector matches multiple elements. Use `.first()`, `{ exact: true }`, or more specific selector.
- **Timeout on networkidle:** WebSocket keeps connections open. Use element-based waits instead.
- **SecurityError on localStorage:** Didn't navigate to a page first. Always `goto("/")` before `evaluate()`.
- **Clerk rate limiting:** Too many sign-in token requests. Reuse `storageState` across tests.

### Step 8: Add to CI (when project has CI)

```yaml
# GitHub Actions example
- name: Run E2E tests
  run: |
    npx playwright install chromium
    npm run test:e2e
```

## Rules

- Every web project gets Playwright tests before delivery
- Tests must pass before telling the user "it's ready"
- Screenshot-on-failure is always enabled for debugging
- Seed data scripts are exported to `window` for manual console use too
- Never skip tests to ship faster — fix the test or fix the code
- Add `test-results/`, `playwright-report/`, and auth state dirs to `.gitignore`
- If using Vitest + Playwright, always exclude `e2e/` from Vitest config

## Learned Patterns (from production)

These patterns were discovered building DSF projects:

1. **Next.js Dev Tools button** matches `/next/i` — always use `{ name: "Next", exact: true }`
2. **Session titles appear in both sidebar and heading** — use `getByRole("button", ...)` for sidebar, `getByRole("heading", ...)` for content
3. **localStorage not available on `about:blank`** — always navigate before calling evaluate
4. **Hooks with relative paths break when CWD changes** — use absolute paths in settings.local.json
5. **Seed data needs `window` attachment** — export functions AND attach to window at module scope for console use
6. **Clerk WebSocket blocks networkidle** — never use `waitForLoadState("networkidle")` with Clerk auth. Wait for specific elements instead.
7. **Clerk sign-in tokens bypass UI** — Use Backend API `/v1/sign_in_tokens` to authenticate without needing email/password UI. Works even when only OAuth is enabled.
8. **Clerk ticket as query param** — Pass `__clerk_ticket=TOKEN` as a query parameter to `/sign-in`. Clerk consumes it and redirects to `/`. Then navigate to the protected page.
9. **Nav items with emojis** — `getByRole("link", { name: "Dashboard", exact: true })` fails when the link text is "📊 Dashboard". Drop `exact: true` for nav items with icons.
10. **`.or()` strict mode** — Playwright's `.or()` can match multiple elements causing strict mode violations. When the page is working correctly (showing both heading AND content), just assert the heading.
11. **First-load compilation delay** — Next.js dev server compiles pages on first visit. Set `test.setTimeout(60000)` for tests that are first to hit a page.
