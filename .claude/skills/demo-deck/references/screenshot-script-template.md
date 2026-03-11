# Screenshot Script Template

Save as `scripts/screenshots.mjs` in the app directory.

```javascript
import puppeteer from "puppeteer";
import { mkdir } from "fs/promises";

// Configure these for your project
const BASE = "http://localhost:3000";
const OUT = "public/screenshots";

const pages = [
  // Add your routes here
  // { name: "page-name", url: "/route", wait: 1000 },
  //
  // name: used for filename (page-name.png, page-name-viewport.png)
  // url: route to navigate to
  // wait: ms to wait after networkidle0 for JS rendering
];

await mkdir(OUT, { recursive: true });

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });

for (const p of pages) {
  console.log(`Capturing ${p.name}...`);
  await page.goto(`${BASE}${p.url}`, { waitUntil: "networkidle0" });
  await new Promise((r) => setTimeout(r, p.wait));

  // Full page (for scrollable pages like detail views)
  await page.screenshot({
    path: `${OUT}/${p.name}.png`,
    fullPage: true,
  });

  // Viewport only (for presentation — fits in a slide)
  await page.screenshot({
    path: `${OUT}/${p.name}-viewport.png`,
    fullPage: false,
  });
}

await browser.close();
console.log(`Done! ${pages.length} pages captured to ${OUT}/`);
```

## Setup

```bash
# Install puppeteer if not already present
npm install --save-dev puppeteer

# Run the script (dev server must be running)
node scripts/screenshots.mjs
```

## Tips

- Use `-viewport.png` versions in the presentation (they fit slides better)
- Use full-page versions for documentation or scrollable content
- Set `wait` higher (2000+) for pages with animations or lazy-loaded content
- Re-run the script any time the UI changes to keep screenshots fresh
