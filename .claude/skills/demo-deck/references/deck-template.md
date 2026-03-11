# Demo Deck HTML Template

Copy and customize this template for each project. Replace placeholder values marked with `{{BRACKETS}}`.

## Full Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{PROJECT_NAME}} — MVP Demo</title>
<style>
  :root {
    --primary: {{PRIMARY_COLOR}};       /* e.g., #1e3a5f */
    --primary-light: {{PRIMARY_LIGHT}}; /* e.g., #2d5a8e */
    --accent: {{ACCENT_COLOR}};         /* e.g., #c49a3c */
    --bg: #fafafa;
    --surface: #ffffff;
    --text: #171717;
    --muted: #6b7280;
    --border: #e5e7eb;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow: hidden;
    height: 100vh;
  }
  .deck { height: 100vh; scroll-snap-type: y mandatory; overflow-y: auto; }
  .slide {
    min-height: 100vh;
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 3.5rem 6rem;
    position: relative;
  }
  .slide-number {
    position: absolute;
    bottom: 2rem;
    right: 3rem;
    font-size: 0.75rem;
    color: var(--muted);
  }
  .nav-hint {
    position: fixed;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.7rem;
    color: var(--muted);
    opacity: 0.6;
    z-index: 10;
  }

  /* Title slide */
  .slide-title { background: var(--primary); color: white; text-align: center; }
  .slide-title h1 { font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem; }
  .slide-title .subtitle { font-size: 1.25rem; color: rgba(255,255,255,0.7); margin-bottom: 2rem; }
  .slide-title .meta { font-size: 0.9rem; color: rgba(255,255,255,0.5); }
  .slide-title .accent { color: var(--accent); }
  .logo {
    display: inline-flex; align-items: center; justify-content: center;
    width: 64px; height: 64px; background: rgba(255,255,255,0.15);
    border-radius: 16px; font-size: 1.5rem; font-weight: 800; margin-bottom: 1.5rem;
  }

  /* Section slides */
  .slide h2 { font-size: 2rem; font-weight: 700; color: var(--primary); margin-bottom: 0.5rem; }
  .slide .lead { font-size: 1.05rem; color: var(--muted); margin-bottom: 1.5rem; max-width: 700px; line-height: 1.6; }

  /* Cards */
  .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; margin-top: 1rem; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }
  .card-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); margin-bottom: 0.25rem; }
  .card-value { font-size: 1.75rem; font-weight: 700; color: var(--primary); }
  .card-sub { font-size: 0.8rem; color: var(--muted); margin-top: 0.25rem; }
  .card-accent .card-value { color: var(--accent); }

  /* Lists */
  .feature-list { list-style: none; margin-top: 0.75rem; }
  .feature-list li {
    padding: 0.6rem 0; border-bottom: 1px solid var(--border);
    display: flex; align-items: flex-start; gap: 0.75rem;
    font-size: 0.95rem; line-height: 1.5;
  }
  .feature-list li:last-child { border: none; }
  .check { color: #059669; font-weight: 700; flex-shrink: 0; }
  .dot { color: var(--accent); font-weight: 700; flex-shrink: 0; }

  /* Divider slide */
  .slide-divider {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: white; text-align: center;
  }
  .slide-divider h2 { color: white; font-size: 2.5rem; }
  .slide-divider .lead { color: rgba(255,255,255,0.7); margin: 0 auto; }

  /* CTA slide */
  .slide-cta { background: var(--primary); color: white; text-align: center; }
  .slide-cta h2 { color: white; font-size: 2.25rem; margin-bottom: 1rem; }
  .slide-cta .lead { color: rgba(255,255,255,0.7); margin: 0 auto 2rem auto; }
  .cta-items { display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap; }
  .cta-item { text-align: center; }
  .cta-item .num { font-size: 2rem; font-weight: 800; color: var(--accent); }
  .cta-item .label { font-size: 0.85rem; color: rgba(255,255,255,0.6); }

  /* Screenshots */
  .screenshot-frame {
    margin-top: 1.5rem; border-radius: 12px; overflow: hidden;
    border: 1px solid var(--border); box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    background: var(--surface);
  }
  .screenshot-frame img { width: 100%; display: block; }
  .screenshot-bar {
    background: #f1f3f5; padding: 0.5rem 1rem;
    display: flex; align-items: center; gap: 0.5rem;
    border-bottom: 1px solid var(--border);
  }
  .screenshot-dot { width: 10px; height: 10px; border-radius: 50%; }
  .screenshot-url {
    flex: 1; background: white; border-radius: 4px;
    padding: 0.2rem 0.75rem; font-size: 0.7rem; color: var(--muted);
    font-family: monospace; margin-left: 0.5rem;
  }
  .screenshot-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; margin-top: 1.5rem; }
  .screenshot-grid .screenshot-frame { margin-top: 0; }
  .screenshot-caption { text-align: center; font-size: 0.8rem; color: var(--muted); margin-top: 0.5rem; font-weight: 500; }

  .slide-with-screenshot { padding-top: 2.5rem; padding-bottom: 2.5rem; }
  .slide-with-screenshot h2 { margin-bottom: 0.25rem; }
  .slide-with-screenshot .lead { margin-bottom: 1rem; }
</style>
</head>
<body>
<div class="deck">

<!-- SLIDE: Title -->
<div class="slide slide-title">
  <div>
    <div class="logo">{{LOGO_TEXT}}</div>
    <h1>{{PROJECT_TITLE}} <span class="accent">{{HIGHLIGHT}}</span></h1>
    <p class="subtitle">MVP Demo — {{CLIENT_NAME}}</p>
    <p class="meta">Prepared for {{AUDIENCE}} &middot; {{DATE}}</p>
  </div>
</div>

<!-- SLIDE: What We Built (customize cards) -->
<div class="slide">
  <h2>What We Built</h2>
  <p class="lead">{{PROJECT_SUMMARY}}</p>
  <div class="cards">
    <div class="card">
      <div class="card-label">{{STAT_1_LABEL}}</div>
      <div class="card-value">{{STAT_1_VALUE}}</div>
      <div class="card-sub">{{STAT_1_SUB}}</div>
    </div>
    <!-- Add more cards as needed -->
  </div>
</div>

<!-- SLIDE: Screenshot (full width) -->
<div class="slide slide-with-screenshot">
  <h2>{{SECTION_TITLE}}</h2>
  <p class="lead">{{SECTION_DESCRIPTION}}</p>
  <div class="screenshot-frame">
    <div class="screenshot-bar">
      <div class="screenshot-dot" style="background:#ff5f57"></div>
      <div class="screenshot-dot" style="background:#febc2e"></div>
      <div class="screenshot-dot" style="background:#28c840"></div>
      <div class="screenshot-url">{{URL}}</div>
    </div>
    <img src="screenshots/{{SCREENSHOT_NAME}}-viewport.png" alt="{{ALT_TEXT}}">
  </div>
</div>

<!-- SLIDE: Side-by-side screenshots -->
<div class="slide slide-with-screenshot">
  <h2>{{COMPARISON_TITLE}}</h2>
  <p class="lead">{{COMPARISON_DESCRIPTION}}</p>
  <div class="screenshot-grid">
    <div>
      <div class="screenshot-frame">
        <div class="screenshot-bar">
          <div class="screenshot-dot" style="background:#ff5f57"></div>
          <div class="screenshot-dot" style="background:#febc2e"></div>
          <div class="screenshot-dot" style="background:#28c840"></div>
          <div class="screenshot-url">{{LEFT_URL}}</div>
        </div>
        <img src="screenshots/{{LEFT_SCREENSHOT}}-viewport.png" alt="{{LEFT_ALT}}">
      </div>
      <p class="screenshot-caption">{{LEFT_CAPTION}}</p>
    </div>
    <div>
      <div class="screenshot-frame">
        <div class="screenshot-bar">
          <div class="screenshot-dot" style="background:#ff5f57"></div>
          <div class="screenshot-dot" style="background:#febc2e"></div>
          <div class="screenshot-dot" style="background:#28c840"></div>
          <div class="screenshot-url">{{RIGHT_URL}}</div>
        </div>
        <img src="screenshots/{{RIGHT_SCREENSHOT}}-viewport.png" alt="{{RIGHT_ALT}}">
      </div>
      <p class="screenshot-caption">{{RIGHT_CAPTION}}</p>
    </div>
  </div>
</div>

<!-- SLIDE: Feature list + screenshot (split layout) -->
<div class="slide slide-with-screenshot">
  <div style="display:flex;gap:3rem;align-items:flex-start">
    <div style="flex:1">
      <h2>{{FEATURE_TITLE}}</h2>
      <p class="lead">{{FEATURE_LEAD}}</p>
      <ul class="feature-list">
        <li><span class="check">&#10003;</span> {{FEATURE_1}}</li>
        <!-- Add more features -->
      </ul>
    </div>
    <div style="flex:1">
      <div class="screenshot-frame">
        <div class="screenshot-bar">
          <div class="screenshot-dot" style="background:#ff5f57"></div>
          <div class="screenshot-dot" style="background:#febc2e"></div>
          <div class="screenshot-dot" style="background:#28c840"></div>
          <div class="screenshot-url">{{FEATURE_URL}}</div>
        </div>
        <img src="screenshots/{{FEATURE_SCREENSHOT}}-viewport.png" alt="{{FEATURE_ALT}}">
      </div>
    </div>
  </div>
</div>

<!-- SLIDE: Section divider -->
<div class="slide slide-divider">
  <div>
    <h2>{{DIVIDER_TITLE}}</h2>
    <p class="lead">{{DIVIDER_SUBTITLE}}</p>
  </div>
</div>

<!-- SLIDE: What's Next -->
<div class="slide">
  <h2>What's Next</h2>
  <p class="lead">Priorities for the next phase.</p>
  <ul class="feature-list">
    <li><span class="check">&#10003;</span> <strong>Done:</strong> {{DONE_ITEMS}}</li>
    <li><span class="dot">&#9679;</span> <strong>Priority 1:</strong> {{P1}}</li>
    <li><span class="dot">&#9679;</span> <strong>Priority 2:</strong> {{P2}}</li>
    <li><span class="dot">&#9679;</span> <strong>Priority 3:</strong> {{P3}}</li>
  </ul>
</div>

<!-- SLIDE: Close -->
<div class="slide slide-cta">
  <div>
    <div class="logo" style="margin: 0 auto 1.5rem auto;">{{LOGO_TEXT}}</div>
    <h2>Ready for Feedback</h2>
    <p class="lead">{{CLOSING_MESSAGE}}</p>
    <div class="cta-items">
      <div class="cta-item">
        <div class="num">{{CTA_1_NUM}}</div>
        <div class="label">{{CTA_1_LABEL}}</div>
      </div>
      <!-- Add more CTA items -->
    </div>
  </div>
</div>

</div>
<div class="nav-hint">Scroll to navigate slides</div>
</body>
</html>
```

## Slide Types Quick Reference

| Type | Class | Use For |
|---|---|---|
| Title | `slide-title` | Opening slide, dark background |
| Content | `slide` | Stats, features, text content |
| Content + Screenshot | `slide slide-with-screenshot` | Tighter padding for image slides |
| Divider | `slide slide-divider` | Section transitions, gradient background |
| Close/CTA | `slide slide-cta` | Final slide, dark background, summary stats |

## Screenshot Frame Snippet

```html
<div class="screenshot-frame">
  <div class="screenshot-bar">
    <div class="screenshot-dot" style="background:#ff5f57"></div>
    <div class="screenshot-dot" style="background:#febc2e"></div>
    <div class="screenshot-dot" style="background:#28c840"></div>
    <div class="screenshot-url">localhost:3000/route</div>
  </div>
  <img src="screenshots/name-viewport.png" alt="Description">
</div>
```
