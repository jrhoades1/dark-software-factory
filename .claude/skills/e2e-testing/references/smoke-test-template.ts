/**
 * Smoke Test Template — DSF Standard
 *
 * Copy to: <app-root>/e2e/smoke.public.spec.ts (for public pages)
 * Adapt: page titles, header text, navigation elements
 *
 * This template covers the minimum viable test suite for any web app.
 *
 * IMPORTANT: Never use waitForLoadState("networkidle") — it times out
 * with WebSocket connections (Clerk, Supabase realtime, etc.).
 * Always wait for a specific element instead.
 */
import { test, expect } from "@playwright/test";

// === TESTS ===

test.describe("Smoke tests", () => {
  test("page loads without errors", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/");
    // ADAPT: check for your app's heading
    await expect(
      page.getByRole("heading", { name: "Your App Title" })
    ).toBeVisible({ timeout: 15000 });

    expect(errors).toEqual([]);
  });

  test("CTA buttons are visible", async ({ page }) => {
    await page.goto("/");
    // ADAPT: check for your main call-to-action buttons/links
    await expect(
      page.getByRole("link", { name: "Get Started" })
    ).toBeVisible();
    await expect(
      page.getByRole("link", { name: "Sign In" })
    ).toBeVisible();
  });
});

test.describe("Auth protection", () => {
  test("protected routes redirect unauthenticated users", async ({ page }) => {
    const response = await page.goto("/dashboard"); // ADAPT: your protected route
    await page.waitForLoadState("domcontentloaded");

    const url = page.url();
    const status = response?.status() ?? 0;
    const isRedirected = !url.includes("/dashboard");
    const isBlocked = status === 401 || status === 403 || status === 404;

    expect(isRedirected || isBlocked).toBe(true);
  });
});

test.describe("Navigation", () => {
  test("all primary nav items are visible", async ({ page }) => {
    await page.goto("/");
    // ADAPT: wait for your page heading, then check nav items
    await expect(
      page.getByRole("heading", { name: "Your App Title" })
    ).toBeVisible({ timeout: 15000 });

    // ADAPT: list your navigation items
    // NOTE: Don't use exact:true if nav items have emoji/icon prefixes
    const navItems = ["Home", "About", "Settings"];
    for (const item of navItems) {
      await expect(
        page.getByRole("link", { name: item }).or(
          page.getByRole("button", { name: item })
        )
      ).toBeVisible();
    }
  });
});
