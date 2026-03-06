/**
 * Clerk Auth Setup Template — DSF Standard
 *
 * Copy to: <app-root>/e2e/global.setup.ts
 * Also create: <app-root>/e2e/helpers.ts (see bottom of file)
 *
 * Uses Clerk Backend API sign-in tokens to authenticate without touching the UI.
 * Works regardless of which sign-in methods are enabled (Google-only, email+password, etc.)
 *
 * Required env vars in .env.local:
 *   CLERK_SECRET_KEY=sk_test_...
 *   E2E_CLERK_USER_USERNAME=e2e-test@yourapp.dev
 *   E2E_CLERK_USER_PASSWORD=<password>
 *
 * Required Clerk setup:
 *   1. Create a test user in Clerk Dashboard > Users
 *   2. Install: npm install -D @clerk/testing dotenv
 */
import { clerkSetup, setupClerkTestingToken } from "@clerk/testing/playwright";
import { test as setup } from "@playwright/test";
import path from "path";

const authFile = path.join(__dirname, "../playwright/.clerk/user.json");

const hasClerkCreds =
  !!process.env.CLERK_SECRET_KEY &&
  !!process.env.E2E_CLERK_USER_USERNAME &&
  !!process.env.E2E_CLERK_USER_PASSWORD;

setup.describe.configure({ mode: "serial" });

setup("obtain clerk testing token", async () => {
  if (!hasClerkCreds) {
    console.log(
      "Skipping Clerk setup — missing CLERK_SECRET_KEY, E2E_CLERK_USER_USERNAME, or E2E_CLERK_USER_PASSWORD"
    );
    return;
  }
  await clerkSetup();
});

setup("authenticate test user", async ({ page }) => {
  setup.setTimeout(60000);

  if (!hasClerkCreds) {
    console.log("Skipping auth — no Clerk credentials configured");
    return;
  }

  const secretKey = process.env.CLERK_SECRET_KEY!;
  const email = process.env.E2E_CLERK_USER_USERNAME!;

  // Find the test user by email via Clerk Backend API
  const usersRes = await fetch(
    `https://api.clerk.com/v1/users?email_address=${encodeURIComponent(email)}`,
    { headers: { Authorization: `Bearer ${secretKey}` } }
  );
  const users = await usersRes.json();
  if (!users.length)
    throw new Error(`No Clerk user found with email: ${email}`);
  const userId = users[0].id;

  // Create a one-time sign-in token
  const tokenRes = await fetch("https://api.clerk.com/v1/sign_in_tokens", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${secretKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: userId,
      expires_in_seconds: 600,
    }),
  });
  if (!tokenRes.ok) {
    const err = await tokenRes.text();
    throw new Error(`Failed to create sign-in token: ${err}`);
  }
  const tokenData = await tokenRes.json();

  // Enable Clerk testing mode in the browser
  await setupClerkTestingToken({ page });

  // Pass the ticket as a query parameter — Clerk consumes it and creates a session
  await page.goto(`/sign-in?__clerk_ticket=${tokenData.token}`);
  // Wait for Clerk to process the ticket and redirect (goes to "/" typically)
  await page.waitForTimeout(5000);
  // Navigate to a protected page to verify auth works
  await page.goto("/dashboard"); // ADAPT: your first protected route
  await page.waitForURL("**/dashboard**", { timeout: 15000 });

  // Save session state for reuse across all authenticated tests
  await page.context().storageState({ path: authFile });
});

// --- helpers.ts (create as separate file) ---
//
// import { test } from "@playwright/test";
// import { setupClerkTestingToken } from "@clerk/testing/playwright";
// import type { Page } from "@playwright/test";
//
// export const hasClerkCreds =
//   !!process.env.CLERK_SECRET_KEY &&
//   !!process.env.E2E_CLERK_USER_USERNAME &&
//   !!process.env.E2E_CLERK_USER_PASSWORD;
//
// export function skipWithoutAuth() {
//   test.skip(
//     !hasClerkCreds,
//     "Skipped — add CLERK_SECRET_KEY, E2E_CLERK_USER_USERNAME, E2E_CLERK_USER_PASSWORD to .env.local"
//   );
// }
//
// /** Refresh Clerk testing token per-test to prevent session expiry mid-suite. */
// export async function refreshClerkSession(page: Page) {
//   if (hasClerkCreds) {
//     await setupClerkTestingToken({ page });
//   }
// }
//
// --- Usage in .auth.spec.ts files ---
//
// test.beforeEach(async ({ page }) => {
//   skipWithoutAuth();
//   await refreshClerkSession(page);
// });
