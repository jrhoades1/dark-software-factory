/**
 * Playwright Config Template — DSF Standard
 *
 * Copy to: <app-root>/playwright.config.ts
 * Adapt: baseURL, webServer.command, webServer.url
 */
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30000,
  expect: { timeout: 10000 },
  fullyParallel: false,
  retries: 0,
  use: {
    baseURL: "http://localhost:3000", // ADAPT: match your dev server
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
    command: "npm run dev", // ADAPT: your dev server start command
    url: "http://localhost:3000", // ADAPT: match baseURL
    reuseExistingServer: true,
    timeout: 60000,
  },
});
