# Resume .docx Formatting Specification

## Page setup
- **Paper size:** Letter (8.5" × 11")
- **Margins:** 0.75" all sides
- **Target length:** 1 page preferred, 2 pages maximum

## Typography

### Name / Header
- **Font:** Calibri Bold, 16pt
- **Color:** Dark navy (#1F2937)
- **Alignment:** Left
- **Below name:** Contact line in Calibri 10pt, regular weight
  - Format: `City, ST | email@domain.com | (555) 123-4567 | linkedin.com/in/handle`
  - Separated by pipes with spaces

### Section headers
- **Font:** Calibri Bold, 12pt
- **Color:** Dark navy (#1F2937)
- **Border:** 1pt bottom border in navy, with 4pt spacing below
- **Spacing:** 12pt before, 4pt after

### Job titles / Role headers
- **Format:** `Role Title — Company Name` in Calibri Bold 11pt
- **Dates:** Right-aligned on the same line, Calibri Regular 10pt
- **Location:** Below the title line, Calibri Italic 10pt (if included)

### Body text
- **Font:** Calibri Regular, 10.5pt
- **Color:** Dark gray (#374151)
- **Line spacing:** 1.15
- **Bullet character:** • (bullet, not dash)
- **Bullet indent:** 0.25" from left margin
- **Paragraph spacing:** 2pt after each bullet

### Skills section
- **Format:** Category labels in bold, items in regular weight
- **Example:** **Languages:** Python, Java, C#, NodeJS
- **Layout:** Compact, using pipes or commas to save vertical space

## Section order (default)

1. Name + Contact
2. Professional Summary (3-4 lines max)
3. Experience (reverse chronological unless using Relevant/Additional split)
4. Technical Skills
5. Education

The order may shift for heavy tailoring (e.g., Technical Skills moved up if the
job is heavily tool-focused).

## Fitting to One Page

When the content is too long for a single page, apply these formatting levers in order.
Each one reclaims space; stop as soon as the content fits.

**Level 1 — Content compression (do this first):**
- Reduce oldest/least relevant roles to 2 bullets each
- Combine Education into a single line: "MBA, Shorter University | BS MIS, UAB"
- Use compact skills format with pipes: "Python | Java | C# | NodeJS"

**Level 2 — Spacing reduction:**
- Reduce section header spacing.before from 240 to 160 (DXA)
- Reduce role header spacing.before from 160 to 100
- Reduce bullet spacing.after from 40 to 20
- Reduce summary paragraph spacing

**Level 3 — Font and margin adjustments:**
- Reduce body text from 10.5pt to 10pt (size: 20 in DXA half-points)
- Reduce left/right margins from 0.75" (1080 DXA) to 0.5" (720 DXA)
- Reduce top/bottom margins from 0.5" to 0.4" (576 DXA)

**Level 4 — Accept two pages (last resort):**
- If the candidate has 15+ years and the user hasn't objected to two pages, it's
  acceptable. Ensure the page break falls between roles, not mid-role. Skills and
  Education should be on the same page as the final role.

**Never do these:**
- Don't go below 10pt body text — becomes hard to read
- Don't reduce margins below 0.4" — looks cramped
- Don't remove roles entirely to fit — employment gaps raise questions

## PDF conversion

After creating the .docx, convert to PDF. Use LibreOffice if available:
```bash
libreoffice --headless --convert-to pdf resume.docx --outdir .
```

If LibreOffice isn't available, use python-docx to create the .docx and note
that PDF conversion will need to be done manually. Don't skip the .docx to
produce only a PDF — the user needs the editable version.
