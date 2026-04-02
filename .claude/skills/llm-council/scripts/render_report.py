#!/usr/bin/env python3
"""Render an LLM Council session into a self-contained HTML report."""

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

TEMPLATE = Path(__file__).parent.parent / "references" / "report-template.html"

ADVISOR_COLORS = {
    "Contrarian": "#e74c3c",
    "First Principles": "#3498db",
    "Expansionist": "#2ecc71",
    "Outsider": "#9b59b6",
    "Executor": "#e67e22",
}

ADVISOR_ICONS = {
    "Contrarian": "&#9888;",       # warning sign
    "First Principles": "&#9881;", # gear
    "Expansionist": "&#9733;",     # star
    "Outsider": "&#128065;",       # eye
    "Executor": "&#9889;",         # lightning
}


def md_to_html(text: str) -> str:
    """Convert markdown text to HTML. Handles headings, bold, italic,
    numbered lists, bullet lists, and paragraphs."""
    escaped = html.escape(text)
    lines = escaped.split("\n")
    out: list[str] = []
    in_ul = False
    in_ol = False

    for line in lines:
        stripped = line.strip()

        # Close open lists if this line isn't a list item
        if in_ul and not stripped.startswith("- ") and not stripped.startswith("* "):
            out.append("</ul>")
            in_ul = False
        if in_ol and not re.match(r"^\d+\.\s", stripped):
            out.append("</ol>")
            in_ol = False

        # Headings
        if stripped.startswith("## "):
            out.append(f"<h2>{stripped[3:]}</h2>")
            continue
        if stripped.startswith("### "):
            out.append(f"<h3>{stripped[4:]}</h3>")
            continue

        # Bullet list
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            item = stripped[2:]
            item = _inline_formatting(item)
            out.append(f"  <li>{item}</li>")
            continue

        # Numbered list
        ol_match = re.match(r"^(\d+)\.\s(.*)", stripped)
        if ol_match:
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            item = _inline_formatting(ol_match.group(2))
            out.append(f"  <li>{item}</li>")
            continue

        # Blank line
        if not stripped:
            continue

        # Regular paragraph
        out.append(f"<p>{_inline_formatting(stripped)}</p>")

    if in_ul:
        out.append("</ul>")
    if in_ol:
        out.append("</ol>")

    return "\n".join(out)


def _inline_formatting(text: str) -> str:
    """Apply bold and italic markdown formatting."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def build_advisor_sections(advisors: dict) -> str:
    """Build collapsible advisor response sections."""
    sections = []
    for name, response in advisors.items():
        color = ADVISOR_COLORS.get(name, "#555")
        icon = ADVISOR_ICONS.get(name, "&#8226;")
        rendered = md_to_html(response)
        sections.append(f"""
        <details class="advisor-section">
            <summary style="border-left: 4px solid {color}; padding-left: 12px;">
                <span class="advisor-icon">{icon}</span>
                <strong>The {html.escape(name)}</strong>
            </summary>
            <div class="advisor-content" style="border-left: 4px solid {color}; padding-left: 12px;">
                {rendered}
            </div>
        </details>""")
    return "\n".join(sections)


def build_review_section(reviews: list, mapping: dict) -> str:
    """Build collapsible peer review section."""
    reverse_map = {v: k for k, v in mapping.items()}
    mapping_str = ", ".join(
        f"<strong>{letter}</strong> = {name}"
        for name, letter in sorted(reverse_map.items(), key=lambda x: x[1])
    )

    review_items = []
    for i, review in enumerate(reviews, 1):
        rendered = md_to_html(review)
        review_items.append(f"""
            <div class="review-item">
                <h4>Reviewer {i}</h4>
                {rendered}
            </div>""")

    return f"""
    <details class="peer-review-section">
        <summary><strong>Peer Reviews</strong> (5 anonymous cross-reviews)</summary>
        <div class="review-content">
            <p class="mapping"><em>Anonymization mapping: {mapping_str}</em></p>
            {"".join(review_items)}
        </div>
    </details>"""


def render(question: str, verdict: str, advisors: dict, reviews: list,
           mapping: dict, timestamp: str) -> str:
    """Render the full HTML report from the template."""
    template_html = TEMPLATE.read_text(encoding="utf-8")

    replacements = {
        "{{QUESTION}}": md_to_html(question),
        "{{VERDICT}}": md_to_html(verdict),
        "{{ADVISOR_SECTIONS}}": build_advisor_sections(advisors),
        "{{REVIEW_SECTION}}": build_review_section(reviews, mapping),
        "{{TIMESTAMP}}": html.escape(timestamp),
        "{{QUESTION_SHORT}}": html.escape(question[:120] + ("..." if len(question) > 120 else "")),
    }

    result = template_html
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)
    return result


def main():
    parser = argparse.ArgumentParser(description="Render LLM Council HTML report")
    parser.add_argument("--question", required=True, help="The framed council question")
    parser.add_argument("--verdict", required=True, help="Chairman verdict (markdown)")
    parser.add_argument("--advisors", required=True, help="JSON dict of advisor name -> response")
    parser.add_argument("--reviews", required=True, help="JSON list of 5 review strings")
    parser.add_argument("--mapping", required=True, help="JSON dict of letter -> advisor name")
    parser.add_argument("--output", required=True, help="Output HTML file path")

    args = parser.parse_args()

    try:
        advisors = json.loads(args.advisors)
        reviews = json.loads(args.reviews)
        mapping = json.loads(args.mapping)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON arguments: {e}", file=sys.stderr)
        sys.exit(1)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    report_html = render(
        question=args.question,
        verdict=args.verdict,
        advisors=advisors,
        reviews=reviews,
        mapping=mapping,
        timestamp=timestamp,
    )

    output_path = Path(args.output)
    output_path.write_text(report_html, encoding="utf-8")
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
