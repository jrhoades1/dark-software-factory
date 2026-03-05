/**
 * Smoke Test Template — DSF Standard
 *
 * Copy to: <app-root>/e2e/smoke.spec.ts
 * Adapt: page titles, header text, navigation elements
 *
 * This template covers the minimum viable test suite for any web app.
 */
import { test, expect } from "@playwright/test";

// === HELPERS ===

// Adapt: add seed/clear functions if the app uses localStorage or needs test data
async function seedData(page: import("@playwright/test").Page) {
  await page.goto("/");
  await page.waitForLoadState("networkidle");
  await page.evaluate(() => {
    // @ts-ignore — seedTestData attached to window by the app
    if (typeof window.seedTestData === "function") {
      window.seedTestData();
    }
  });
  await page.reload();
  await page.waitForLoadState("networkidle");
}

async function clearData(page: import("@playwright/test").Page) {
  await page.goto("/");
  await page.waitForLoadState("networkidle");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.waitForLoadState("networkidle");
}

// === TESTS ===

test.describe("Smoke tests", () => {
  test("page loads without errors", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // ADAPT: check for your app's header/title
    await expect(page.locator("header")).toBeVisible();

    expect(errors).toEqual([]);
  });

  test("main content area renders", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("main")).toBeVisible();
  });
});

test.describe("Navigation", () => {
  test("all primary nav items are visible", async ({ page }) => {
    await page.goto("/");

    // ADAPT: list your navigation items
    const navItems = ["Home", "About", "Settings"];
    for (const item of navItems) {
      await expect(page.getByRole("link", { name: item }).or(page.getByRole("button", { name: item }))).toBeVisible();
    }
  });
});

test.describe("Forms and inputs", () => {
  test("primary input accepts text", async ({ page }) => {
    await clearData(page);

    // ADAPT: target your main input element
    const input = page.locator("textarea, input[type='text']").first();
    if (await input.isVisible()) {
      await input.fill("Test input value");
      await expect(input).toHaveValue("Test input value");
    }
  });
});

test.describe("Persistence", () => {
  test("data survives page reload", async ({ page }) => {
    await clearData(page);

    const input = page.locator("textarea, input[type='text']").first();
    if (await input.isVisible()) {
      await input.fill("Persistence check");
      await page.waitForTimeout(1000); // wait for auto-save
      await page.reload();
      await page.waitForLoadState("networkidle");
      await expect(page.locator("textarea, input[type='text']").first()).toHaveValue("Persistence check");
    }
  });
});
