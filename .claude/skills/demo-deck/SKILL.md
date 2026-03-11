---
name: demo-deck
description: >
  Generate a client-ready MVP demo presentation with automated screenshots.
  Use this skill when the user wants to create a demo deck, presentation,
  show-and-tell materials, or client walkthrough. Also trigger when the user
  mentions "demo," "presentation," "show Jackie," "show the client,"
  "MVP deck," "screenshot presentation," or "demo prep."
  This skill captures screenshots of key app routes via Puppeteer and
  assembles them into a scrollable HTML slide deck with consistent
  DSF branding.
user-invokable: true
---

# Demo Deck Generator

## Intent

- Every DSF project should be presentable to the client at any time
- Screenshots make abstract progress tangible for non-technical stakeholders
- A consistent deck format builds trust and professionalism across engagements
- Automate the boring parts (screenshots, layout) so the developer focuses on narrative
- The deck should work offline — a single HTML file with embedded or local images

## When to Use

- Client show-and-tell or demo meeting is coming up
- MVP gate passes and the project is ready to present
- User says "make a presentation," "demo deck," "show the client"
- End of a sprint or milestone — need to communicate progress
- Any time visual proof of work is needed

## Process

### Step 1: Identify Key Routes

Determine the routes to screenshot. At minimum, capture:
- The main user-facing page(s)
- Any admin/dashboard pages
- Key workflows (onboarding, detail views, etc.)

Ask the user if unclear, or infer from the app's route structure.

### Step 2: Ensure Puppeteer is Available

```bash
cd <app-dir> && npm ls puppeteer 2>/dev/null || npm install --save-dev puppeteer
```

### Step 3: Create Screenshot Script

Create `scripts/screenshots.mjs` in the app directory:

```javascript
import puppeteer from "puppeteer";
import { mkdir } from "fs/promises";

const BASE = "http://localhost:<PORT>";
const OUT = "public/screenshots";

const pages = [
  // { name: "page-name", url: "/route", wait: 1000 },
];

await mkdir(OUT, { recursive: true });

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });

for (const p of pages) {
  console.log(`Capturing ${p.name}...`);
  await page.goto(`${BASE}${p.url}`, { waitUntil: "networkidle0" });
  await new Promise((r) => setTimeout(r, p.wait));
  await page.screenshot({ path: `${OUT}/${p.name}.png`, fullPage: true });
  await page.screenshot({ path: `${OUT}/${p.name}-viewport.png`, fullPage: false });
}

await browser.close();
console.log("Done! Screenshots saved to public/screenshots/");
```

Customize the `pages` array for the project. Use `fullPage: true` for detail pages, viewport-only for dashboard overviews.

### Step 4: Run Screenshot Capture

```bash
cd <app-dir> && node scripts/screenshots.mjs
```

Verify screenshots are non-empty and visually correct by reading one or two with the Read tool.

### Step 5: Generate the HTML Deck

Create `public/demo.html` using the standard slide template. See `references/deck-template.md` for the full HTML template.

**Required slides (in order):**

1. **Title** — Project name, client name, date. Dark primary background.
2. **What We Built** — Summary stats in cards (features, questions, cost).
3. **Two Sides** — Side-by-side screenshots if there are multiple user roles (e.g., student vs admin).
4. **Section Divider** — For each major section of the app.
5. **Feature + Screenshot** — Left column: bullet list. Right column: screenshot.
6. **Side-by-Side Screenshots** — Compare views (e.g., different user states).
7. **Live Demo Divider** — Transition point to switch to the actual app.
8. **Economics/Costs** — Platform costs, per-user costs, scale projections.
9. **What's Next** — Prioritized roadmap.
10. **Close/CTA** — Summary stats, "ready for feedback."

Not all slides are required — adapt to the project. The template handles styling.

### Step 6: Embed Screenshots

Use this pattern for browser-chrome-framed screenshots:

```html
<div class="screenshot-frame">
  <div class="screenshot-bar">
    <div class="screenshot-dot" style="background:#ff5f57"></div>
    <div class="screenshot-dot" style="background:#febc2e"></div>
    <div class="screenshot-dot" style="background:#28c840"></div>
    <div class="screenshot-url">localhost:3000/route</div>
  </div>
  <img src="screenshots/page-name-viewport.png" alt="Description">
</div>
```

For side-by-side comparisons:

```html
<div class="screenshot-grid">
  <div>
    <div class="screenshot-frame">...</div>
    <p class="screenshot-caption">Caption text</p>
  </div>
  <div>
    <div class="screenshot-frame">...</div>
    <p class="screenshot-caption">Caption text</p>
  </div>
</div>
```

### Step 7: Test the Deck

Open `http://localhost:<PORT>/demo.html` in the browser. Verify:
- All screenshots load
- Scroll-snap navigation works
- Text is readable and slides aren't overcrowded
- The "Live Demo" slide is positioned correctly for the presentation flow

## Rules

- Never hardcode client-sensitive data in the deck — use generic descriptions
- Screenshots must be captured fresh each time (don't reuse stale screenshots)
- The deck must work as a standalone HTML file (no external CDN dependencies)
- Keep slides focused — one idea per slide, max 5-6 bullet points
- Always include a "What's Next" slide — clients want to see the roadmap
- Always include cost/economics if AI features are involved
- Use the project's color scheme for the deck (pull from CSS variables)
- The live demo divider should come AFTER showing screenshots, not before

## Relationships to Other Skills

| Skill | Relationship |
|---|---|
| `mvp-gate` | Demo deck is typically created after MVP gate passes |
| `cost-tracking` | Cost data from tracking feeds into the Economics slide |
| `client-follow-up` | Deck URL can be included in follow-up communications |
| `project-bootstrap` | New projects should have puppeteer in devDeps from the start |
