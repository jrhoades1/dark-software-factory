# Persona-Driven E2E Testing

Every DSF web project ships with persona-driven E2E tests. Personas represent real user
archetypes derived from the product spec, and they drive test inputs, tone, and expected
behaviors. This pattern ensures tests exercise the app the way actual users will.

## Why Personas

Generic E2E tests use throwaway inputs like "test text" or "Lorem ipsum." Persona tests
use realistic inputs from actual user archetypes, which:

- Catch edge cases from real usage patterns (long text, multi-tag selection, minimal input)
- Make test failures meaningful ("Priya the IT Leader can't submit her vent" vs "test 14 failed")
- Serve as living documentation of who your users are
- Cover the full spectrum from power users to minimal-effort users

## Persona Structure

```typescript
// e2e/personas.ts

import { test as base, type Page } from "@playwright/test";

/** Each persona represents a real user archetype from the product spec */
export interface Persona {
  name: string;          // "Marcus — Frustrated Dev"
  description: string;   // "Senior engineer who hits bugs in tools daily"
  // App-specific fields below — adapt to your domain
  inputText: string;     // Realistic input for this persona
  tags: string[];        // Categories they'd select
  context: string;       // Additional context they'd provide
  preferences: Record<string, string>;  // Tone, length, etc.
}

export const PERSONAS: Record<string, Persona> = {
  powerUser: {
    name: "Power User Name",
    description: "Description of behavior and motivation",
    inputText: "Realistic input that this person would actually type...",
    tags: ["relevant-tag"],
    context: "Realistic context",
    preferences: { tone: "professional", length: "long" },
  },
  minimalUser: {
    name: "Minimal Input User",
    description: "User who does the bare minimum",
    inputText: "Short input.",
    tags: [],
    context: "",
    preferences: {},
  },
  // Add 3-5 personas total, covering the spectrum from your product spec
};
```

## Persona Design Rules

1. **Derive from the product spec** — Every persona should map to a user type described
   in the requirements or user stories. Don't invent personas that don't represent real users.

2. **Cover the input spectrum:**
   - One power user (fills everything, long text, multiple tags)
   - One minimal user (shortest possible valid input, no optional fields)
   - One multi-category user (selects multiple options, cross-cutting concerns)
   - One or two domain-specific users (unique to your app's problem space)

3. **Use realistic text** — The input text should read like something a real person would
   actually type or say. This makes test output meaningful and catches character-limit issues.

4. **Name them** — "Marcus the Frustrated Dev" is more memorable than "persona1." Tests
   read like stories: "Marcus fills the form and generates a thread."

5. **Include edge-case personas** — At minimum, always include a "minimal input" persona
   that tests the happy path with the least possible effort.

## Helper Pattern

Create a `fillFormAsPersona()` helper that fills your app's form using a persona's data.
This is reused across all test files:

```typescript
/** Fill the main form as a specific persona */
export async function fillFormAsPersona(page: Page, persona: Persona) {
  // Fill primary input
  const mainInput = page.locator("textarea").first();
  await mainInput.fill(persona.inputText);

  // Select tags/categories
  for (const tag of persona.tags) {
    await page.getByText(tag, { exact: true }).click();
  }

  // Fill optional fields only if persona provides them
  if (persona.context) {
    await page.getByPlaceholder(/context/i).fill(persona.context);
  }

  // Set preferences (dropdowns, sliders, toggles)
  for (const [key, value] of Object.entries(persona.preferences)) {
    await page.getByText(value, { exact: false }).first().click();
  }
}
```

## Extended Test Fixture

Export an extended `test` from personas.ts so any spec file can access personas:

```typescript
export const test = base.extend<{ persona: Persona }>({
  persona: async ({}, use) => {
    await use(PERSONAS.powerUser); // default persona
  },
});

export { expect } from "@playwright/test";
```

## Test File Structure

### Smoke + Navigation (smoke.spec.ts)
Standard smoke tests — not persona-specific. Tests that every page loads, nav works,
empty states render correctly.

### Form/Input Tests (per feature)
One `test.describe` block per persona, testing that they can fill the form correctly:

```typescript
test.describe("Feature — Persona: Power User (Marcus)", () => {
  const persona = PERSONAS.powerUser;

  test("fills form completely and validates inputs", async ({ page }) => {
    await page.goto("/");
    await fillFormAsPersona(page, persona);

    // Assert form state matches persona's input
    await expect(page.locator("textarea").first()).toHaveValue(persona.inputText);
    await expect(page.getByRole("button", { name: /submit/i })).toBeEnabled();
  });
});
```

### Output/Result Tests (per feature)
Test the output using a **mocked API** — never hit real AI APIs in E2E tests:

```typescript
async function mockAPI(page: Page) {
  await page.route("**/api/generate", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ /* realistic mock response */ }),
    });
  });
}

test.describe("All personas can complete the flow", () => {
  for (const [key, persona] of Object.entries(PERSONAS)) {
    test(`${persona.name} completes the full flow`, async ({ page }) => {
      await mockAPI(page);
      await page.goto("/");
      await fillFormAsPersona(page, persona);
      await page.getByRole("button", { name: /submit/i }).click();
      // Assert output renders correctly
    });
  }
});
```

## Mock API Pattern

**Never call real AI APIs in E2E tests.** Use `page.route()` to intercept API calls:

- Return realistic mock data that matches your API's response shape
- Include enough data to test the full output UI (5+ items, realistic text)
- Mock both success and error responses

```typescript
const MOCK_RESPONSE = {
  result: {
    items: [
      { id: "1", text: "Realistic output text that matches production shape" },
      // ... enough items to test the full UI
    ],
    summary: "One sentence summary",
  },
};

async function mockAPI(page: Page) {
  await page.route("**/api/your-endpoint", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(MOCK_RESPONSE),
    });
  });
}
```

## Minimum Test Coverage Per Persona

| Test | What it covers | Required |
|------|---------------|----------|
| Form fill | Persona can fill all relevant fields | Yes |
| Input validation | Form state is correct after fill | Yes |
| Full flow (mocked) | Persona can trigger submission and see output | Yes |
| Edge case | Persona-specific boundary (e.g., minimal user with no tags) | Yes for minimal persona |

## Adapting to Your Domain

The persona pattern works for any app. Replace the VentThread-specific fields with
your domain's equivalents:

| VentThread | E-commerce | Dashboard | SaaS |
|-----------|-----------|-----------|------|
| ventText | searchQuery | dateRange | projectName |
| tags | categories | filters | teamMembers |
| tone | sortOrder | groupBy | planTier |
| context | priceRange | department | integrations |

The structure stays the same — only the persona fields and `fillFormAsPersona()` logic change.
