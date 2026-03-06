/**
 * Playwright Config Template (with Auth) — DSF Standard
 *
 * Copy to: <app-root>/playwright.config.ts
 * Adapt: baseURL, port, webServer.command
 *
 * Three test projects:
 *   1. setup    — Authenticates via Clerk sign-in token
 *   2. public   — Tests that don't need auth (landing page, sign-in)
 *   3. authenticated — Tests that need a logged-in session
 */
import { defineConfig } from "@playwright/test";
import dotenv from "dotenv";
import path from "path";

// Load .env.local for Clerk keys and test user credentials
dotenv.config({ path: path.resolve(__dirname, ".env.local") });

const PORT = 3000; // ADAPT: your dev server port

const hasClerkCreds =
  !!process.env.CLERK_SECRET_KEY &&
  !!process.env.E2E_CLERK_USER_USERNAME &&
  !!process.env.E2E_CLERK_USER_PASSWORD;

export default defineConfig({
  testDir: "./e2e",
  timeout: 30000,
  expect: { timeout: 10000 },
  fullyParallel: false,
  retries: 0,
  use: {
    baseURL: `http://localhost:${PORT}`,
    headless: true,
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "setup",
      testMatch: /global\.setup\.ts/,
    },
    {
      name: "public",
      testMatch: /.*\.public\.spec\.ts/,
      use: { browserName: "chromium" },
    },
    {
      name: "authenticated",
      testMatch: /.*\.auth\.spec\.ts/,
      dependencies: ["setup"],
      use: {
        browserName: "chromium",
        storageState: hasClerkCreds
          ? "playwright/.clerk/user.json"
          : undefined,
      },
    },
  ],
  webServer: {
    command: `npm run dev -- --port ${PORT}`, // ADAPT: your dev server command
    url: `http://localhost:${PORT}`,
    reuseExistingServer: true,
    timeout: 60000,
  },
});
