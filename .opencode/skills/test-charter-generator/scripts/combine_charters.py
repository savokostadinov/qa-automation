#!/usr/bin/env python3
"""
combine_charters.py — Combine generated SBTM charter .md files into one styled HTML
=====================================================================================
Reads all CHR-[PLATFORM]-*.md files from the output directory, converts them to
a single styled HTML document that opens in any browser and can be printed to PDF.

Usage:
    python3 combine_charters.py --platform tablet
    python3 combine_charters.py --platform laptop
    python3 combine_charters.py --platform mobile
    python3 combine_charters.py --platform all

Output:
    docs/skill-test-charters/output/CHARTERS-TABLET.html
    docs/skill-test-charters/output/CHARTERS-LAPTOP.html
    docs/skill-test-charters/output/CHARTERS-MOBILE.html
    docs/skill-test-charters/output/CHARTERS-ALL.html
"""

import argparse
import glob
import os
import re
import sys
import webbrowser
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs", "skill-test-charters", "output")

PLATFORM_PREFIX = {
    "tablet": "CHR-TAB-",
    "laptop": "CHR-LAP-",
    "mobile": "CHR-MOB-",
    "all":    "CHR-",
}

PLATFORM_LABEL = {
    "tablet": "Tablet",
    "laptop": "Laptop",
    "mobile": "Mobile",
    "all":    "All Platforms",
}

PLATFORM_COLOR = {
    "tablet": "#4A90D9",
    "laptop": "#27AE60",
    "mobile": "#E67E22",
    "all":    "#8E44AD",
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    /* ── Base ── */
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 15px;
      line-height: 1.7;
      color: #1e2235;
      background: #eef1f6;
      margin: 0;
      padding: 0 0 64px 0;
    }}

    /* ── Cover page ── */
    .cover {{
      background: linear-gradient(135deg, {accent} 0%, {accent_dark} 100%);
      color: white;
      padding: 80px 72px 72px 72px;
      min-height: 300px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      page-break-after: always;
      position: relative;
      overflow: hidden;
    }}
    .cover::before {{
      content: '';
      position: absolute;
      top: -60px; right: -60px;
      width: 320px; height: 320px;
      border-radius: 50%;
      background: rgba(255,255,255,0.06);
    }}
    .cover::after {{
      content: '';
      position: absolute;
      bottom: -80px; left: 40px;
      width: 240px; height: 240px;
      border-radius: 50%;
      background: rgba(255,255,255,0.04);
    }}
    .cover .label {{
      font-size: 11px;
      letter-spacing: 4px;
      text-transform: uppercase;
      opacity: 0.7;
      margin-bottom: 20px;
      position: relative; z-index: 1;
    }}
    .cover h1 {{
      font-size: 42px;
      font-weight: 800;
      margin: 0 0 10px 0;
      line-height: 1.15;
      position: relative; z-index: 1;
    }}
    .cover .subtitle {{
      font-size: 16px;
      opacity: 0.8;
      margin-bottom: 40px;
      position: relative; z-index: 1;
    }}
    .cover .meta {{
      display: flex;
      gap: 48px;
      font-size: 12px;
      opacity: 0.7;
      flex-wrap: wrap;
      position: relative; z-index: 1;
      border-top: 1px solid rgba(255,255,255,0.2);
      padding-top: 24px;
    }}
    .cover .meta span {{ display: flex; flex-direction: column; gap: 2px; }}
    .cover .meta strong {{ font-size: 16px; font-weight: 700; opacity: 1; color: white; }}

    /* ── TOC ── */
    .toc {{
      background: white;
      margin: 40px auto;
      max-width: 860px;
      border-radius: 16px;
      padding: 40px 52px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.07);
      page-break-after: always;
    }}
    .toc h2 {{
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: {accent};
      margin-top: 0;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 2px solid {accent_light};
    }}
    .toc ol {{
      padding-left: 0;
      margin: 0;
      list-style: none;
      counter-reset: toc-counter;
    }}
    .toc li {{
      counter-increment: toc-counter;
      display: flex;
      align-items: baseline;
      gap: 14px;
      padding: 10px 0;
      border-bottom: 1px solid #f0f2f5;
    }}
    .toc li:last-child {{ border-bottom: none; }}
    .toc li::before {{
      content: counter(toc-counter, decimal-leading-zero);
      font-size: 11px;
      font-weight: 700;
      color: {accent};
      opacity: 0.5;
      flex-shrink: 0;
      width: 24px;
    }}
    .toc a {{
      color: #1e2235;
      text-decoration: none;
      font-weight: 500;
      font-size: 14px;
      flex: 1;
    }}
    .toc a:hover {{ color: {accent}; }}
    .toc .toc-area {{
      font-size: 10px;
      font-weight: 600;
      color: white;
      background: {accent};
      opacity: 0.7;
      border-radius: 20px;
      padding: 2px 10px;
      text-transform: uppercase;
      letter-spacing: 1px;
      flex-shrink: 0;
    }}

    /* ── Charter card ── */
    .charter {{
      background: white;
      margin: 40px auto;
      max-width: 860px;
      border-radius: 16px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.07);
      overflow: visible;
      page-break-inside: avoid;
      page-break-after: always;
      scroll-margin-top: 32px;
    }}
    .charter-header {{
      background: linear-gradient(100deg, {accent} 0%, {accent_dark} 100%);
      color: white;
      padding: 28px 40px 24px 40px;
      border-radius: 16px 16px 0 0;
      overflow: hidden;
      position: relative;
    }}
    .charter-header::after {{
      content: '';
      position: absolute;
      top: -40px; right: -40px;
      width: 180px; height: 180px;
      border-radius: 50%;
      background: rgba(255,255,255,0.07);
    }}
    .charter-id {{
      font-size: 12px;
      font-weight: 500;
      letter-spacing: 0.5px;
      opacity: 0.75;
      margin-bottom: 10px;
      position: relative; z-index: 1;
    }}
    .charter-header h2 {{
      margin: 0 0 12px 0;
      font-size: 19px;
      font-weight: 700;
      line-height: 1.4;
      position: relative; z-index: 1;
    }}
    .charter-meta {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      position: relative; z-index: 1;
    }}
    .charter-header .platform-badge {{
      display: inline-block;
      background: rgba(255,255,255,0.18);
      border: 1px solid rgba(255,255,255,0.3);
      border-radius: 20px;
      padding: 3px 14px;
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 1.5px;
      text-transform: uppercase;
    }}
    .charter-body {{
      padding: 36px 40px 40px 40px;
    }}

    /* ── Section grid layout ── */
    .sections-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0 32px;
    }}
    .section-full {{ grid-column: 1 / -1; }}

    /* ── Sub-labels (e.g. "From Reference Test Cases:") ── */
    .sub-label {{
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: {accent_dark};
      margin: 16px 0 8px 0;
      opacity: 0.7;
    }}
    .sub-label:first-child {{ margin-top: 0; }}

    /* ── References metadata block ── */
    .ref-block {{
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 6px 16px;
      font-size: 13px;
      background: #f8f9fc;
      border-radius: 8px;
      padding: 14px 18px;
    }}
    .ref-key {{
      font-weight: 600;
      color: {accent_dark};
      white-space: nowrap;
    }}
    .ref-val {{ color: #3a3f52; }}

    /* ── TC reference list (in SCOPE section) ── */
    .tc-ref-list {{
      margin: 0;
      padding-left: 0;
      list-style: none;
    }}
    .tc-ref-list li {{
      display: flex;
      align-items: baseline;
      gap: 10px;
      padding: 7px 12px;
      margin-bottom: 4px;
      border-radius: 6px;
      background: #f8f9fc;
      font-size: 13px;
      color: #3a3f52;
      line-height: 1.5;
    }}
    .tc-ref-list li .tc-id {{
      font-weight: 700;
      color: {accent_dark};
      white-space: nowrap;
      min-width: 52px;
    }}
    .tc-ref-list li .tc-title {{ flex: 1; }}

    /* ── Sections ── */
    .section {{
      margin-bottom: 32px;
    }}
    .section-title {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 2.5px;
      text-transform: uppercase;
      color: {accent};
      margin-bottom: 14px;
    }}
    .section-title::before {{
      content: '';
      display: inline-block;
      width: 3px;
      height: 14px;
      background: {accent};
      border-radius: 2px;
      flex-shrink: 0;
    }}
    .section p {{
      margin: 0 0 10px 0;
      color: #3a3f52;
      line-height: 1.7;
    }}
    .section p:last-child {{ margin-bottom: 0; }}

    /* ── Ordered lists (numbered test ideas) ── */
    .section ol {{
      margin: 0;
      padding-left: 0;
      list-style: none;
      counter-reset: idea-counter;
    }}
    .section ol li {{
      counter-increment: idea-counter;
      display: flex;
      gap: 14px;
      padding: 10px 14px;
      margin-bottom: 6px;
      border-radius: 8px;
      background: #f8f9fc;
      border-left: 3px solid {accent_light};
      line-height: 1.6;
      color: #3a3f52;
      font-size: 14px;
    }}
    .section ol li:hover {{
      background: #f0f3fa;
      border-left-color: {accent};
    }}
    .section ol li::before {{
      content: counter(idea-counter);
      display: flex;
      align-items: center;
      justify-content: center;
      min-width: 24px;
      height: 24px;
      border-radius: 50%;
      background: {accent};
      color: white;
      font-size: 11px;
      font-weight: 700;
      flex-shrink: 0;
      margin-top: 1px;
    }}

    /* ── Unordered lists (bullets) ── */
    .section ul {{
      margin: 0;
      padding-left: 0;
      list-style: none;
    }}
    .section ul li {{
      display: flex;
      gap: 10px;
      padding: 6px 0;
      border-bottom: 1px solid #f0f2f5;
      color: #3a3f52;
      font-size: 14px;
      line-height: 1.6;
      align-items: flex-start;
    }}
    .section ul li:last-child {{ border-bottom: none; }}
    .section ul li::before {{
      content: '';
      display: inline-block;
      min-width: 6px;
      height: 6px;
      border-radius: 50%;
      background: {accent};
      margin-top: 8px;
      flex-shrink: 0;
    }}

    /* ── Test case table ── */
    .tc-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      margin-top: 4px;
      border-radius: 8px;
      overflow: hidden;
    }}
    .tc-table th {{
      background: {accent_light};
      color: {accent_dark};
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      padding: 10px 14px;
      text-align: left;
    }}
    .tc-table td {{
      padding: 10px 14px;
      border-bottom: 1px solid #f0f2f5;
      vertical-align: top;
      color: #3a3f52;
    }}
    .tc-table tr:last-child td {{ border-bottom: none; }}
    .tc-table tr:hover td {{ background: #fafbfe; }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      border-radius: 6px;
      padding: 3px 10px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}
    .badge-pass {{ background: #d1fae5; color: #065f46; }}
    .badge-fail {{ background: #fee2e2; color: #991b1b; }}

    /* ── Defect table ── */
    .defect-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      margin-top: 4px;
      border-radius: 8px;
      overflow: hidden;
    }}
    .defect-table th {{
      background: #fef9ec;
      color: #92400e;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      padding: 10px 14px;
      text-align: left;
    }}
    .defect-table td {{
      padding: 10px 14px;
      border-bottom: 1px solid #f0f2f5;
      vertical-align: top;
      color: #3a3f52;
    }}
    .severity-high   {{ color: #b91c1c; font-weight: 700; }}
    .severity-major  {{ color: #b91c1c; font-weight: 700; }}
    .severity-medium {{ color: #d97706; font-weight: 600; }}
    .severity-minor  {{ color: #059669; font-weight: 600; }}
    .severity-low    {{ color: #059669; font-weight: 600; }}

    /* ── Footer ── */
    .page-footer {{
      max-width: 860px;
      margin: 0 auto 48px auto;
      text-align: center;
      font-size: 12px;
      color: #9ca3af;
      padding: 24px 36px 0 36px;
      border-top: 1px solid #e5e7eb;
    }}
    .page-footer a {{ color: #9ca3af; }}

    /* ── Print ── */
    @media print {{
      body {{ background: white; padding: 0; }}
      .charter {{ box-shadow: none; border: 1px solid #e5e7eb; margin: 20px auto; }}
      .toc {{ box-shadow: none; border: 1px solid #e5e7eb; }}
      .cover {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
      .charter-header {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
      .section ol li {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
      .toc li::before {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    }}
  </style>
</head>
<body>

{cover}

{toc}

{charters}

<div class="page-footer">
  Generated by test-charter-generator &nbsp;·&nbsp; PrestaShop Demo Shop &nbsp;·&nbsp;
  <a href="https://demo.prestashop.com/#/en/front">demo.prestashop.com</a>
  &nbsp;·&nbsp; SBTM — Bach, J. (1999)
</div>

</body>
</html>
"""


def hex_darken(hex_color: str, factor: float = 0.75) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return "#{:02x}{:02x}{:02x}".format(int(r * factor), int(g * factor), int(b * factor))


def hex_lighten(hex_color: str, alpha: float = 0.12) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r2 = int(r + (255 - r) * (1 - alpha))
    g2 = int(g + (255 - g) * (1 - alpha))
    b2 = int(b + (255 - b) * (1 - alpha))
    return "#{:02x}{:02x}{:02x}".format(r2, g2, b2)


def md_to_html_content(md: str) -> str:
    """Convert the body of a charter .md file into structured HTML sections.

    Handles two header styles:
      1. Markdown:   ## Section Title
      2. Plain-text: line of dashes followed by SECTION TITLE followed by line of dashes
                     (the format used by the charter template)
    """
    lines = md.splitlines()
    sections = []
    current_section = None
    current_lines = []

    # Skip the outer document border (===...=== wrapping the whole file)
    SKIP_SECTIONS = {"TEST CHARTER", ""}

    def flush():
        if current_section is not None and current_section not in SKIP_SECTIONS:
            sections.append((current_section, "\n".join(current_lines).strip()))

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Plain-text section pattern:
        #   previous line = "-----..." separator
        #   current line  = section title text (non-empty, no leading special chars)
        #   next line     = "-----..." separator
        prev_stripped = lines[i - 1].strip() if i > 0 else ""
        next_stripped = lines[i + 1].strip() if i + 1 < len(lines) else ""
        is_sandwiched = (
            re.match(r"^[-]{3,}$", prev_stripped) and
            re.match(r"^[-]{3,}$", next_stripped) and
            stripped and
            not re.match(r"^[=\-#]", stripped)
        )
        if is_sandwiched:
            flush()
            current_section = stripped
            current_lines = []
            i += 2  # skip the closing separator line
            continue

        # Markdown heading style
        if re.match(r"^#{1,3}\s+", stripped):
            flush()
            current_section = re.sub(r"^#{1,3}\s+", "", stripped).strip()
            current_lines = []
            i += 1
            continue

        # Skip pure separator lines (===, ---) that are not part of content
        if re.match(r"^[=\-]{3,}$", stripped):
            i += 1
            continue

        # Skip the "Charter ID / Platform / Target URL / Test Session" header block
        if re.match(r"^(Charter ID|Platform|Target URL|Test Session)\s*:", stripped, re.I):
            i += 1
            continue

        current_lines.append(line)
        i += 1

    flush()

    if not sections:
        # Fallback: render as pre-formatted text (should not happen for valid charters)
        return f"<pre style='white-space:pre-wrap;font-size:13px;'>{escape_html(md)}</pre>"

    html_parts = []
    for title, body in sections:
        if not body and not title:
            continue
        body_html = render_section_body(title, body)
        if not body_html:
            continue

        # Sections that should span full width
        FULL_WIDTH = {
            "MISSION",
            "TEST IDEAS & EXPLORATION NOTES",
            "ORACLE — HOW TO DETERMINE PASS/FAIL",
            "KNOWN DEFECTS & RISKS (FROM REFERENCE DOCS)",
            "EXPLORATORY TESTING AREAS (BEYOND REFERENCE TCS)",
        }
        extra_class = " section-full" if title.upper() in FULL_WIDTH else ""

        html_parts.append(f"""
        <div class="section{extra_class}">
          <div class="section-title">{escape_html(title)}</div>
          {body_html}
        </div>""")

    # Wrap all sections in the grid container
    grid_inner = "\n".join(html_parts)
    return f'<div class="sections-grid">{grid_inner}</div>'


def badge_inline(text: str) -> str:
    """Convert [PASS] / [FAIL] tokens inside plain text to HTML badge spans."""
    text = re.sub(r'\[PASS\]', '<span class="badge badge-pass">PASS</span>', text)
    text = re.sub(r'\[FAIL\]', '<span class="badge badge-fail">FAIL</span>', text)
    return text


def render_section_body(title: str, body: str) -> str:
    """Render a section body with proper paragraph joining, sub-labels, badge conversion,
    numbered/bullet lists, and a special REFERENCES metadata block."""
    title_lower = title.lower()
    lines = body.splitlines()
    non_empty = [l for l in lines if l.strip()]

    if not non_empty:
        return ""

    # ── REFERENCES section: render as a key/value metadata block ──
    if "references" in title_lower:
        rows = []
        for l in non_empty:
            if ":" in l:
                key, _, val = l.partition(":")
                rows.append(
                    f'<div class="ref-key">{escape_html(key.strip())}</div>'
                    f'<div class="ref-val">{badge_inline(escape_html(val.strip()))}</div>'
                )
        if rows:
            return f'<div class="ref-block">{"".join(rows)}</div>'

    # ── SCOPE COVERED: render TC reference lines as styled tc-ref-list ──
    if "what is covered" in title_lower:
        items = []
        prose_buf = []
        for l in non_empty:
            stripped = l.strip()
            # TC reference line: "  - TC_XX : Title  [PASS/FAIL]"
            m = re.match(r"[-*]?\s*(TC_\w+)\s*:\s*(.+)", stripped)
            if m:
                tc_id = m.group(1)
                rest = m.group(2).strip()
                # extract trailing badge
                rest_html = badge_inline(escape_html(rest))
                items.append(
                    f'<li><span class="tc-id">{escape_html(tc_id)}</span>'
                    f'<span class="tc-title">{rest_html}</span></li>'
                )
            else:
                if items:
                    # flush tc list then continue with prose
                    pass
                prose_buf.append(stripped)

        html_out = []
        # prose lines before TCs
        if prose_buf:
            para = " ".join(prose_buf)
            html_out.append(f"<p>{escape_html(para)}</p>")
        if items:
            html_out.append(f'<ul class="tc-ref-list">{"".join(items)}</ul>')
        return "\n".join(html_out)

    # ── Markdown table ──
    if any("|" in l for l in non_empty[:3]):
        return render_md_table(non_empty, title_lower)

    # ── Mixed content: paragraphs + sub-labels + numbered/bullet lists ──
    html_parts = []
    list_buf = []
    list_type = "ul"
    prose_buf = []   # accumulate consecutive plain-text lines into one <p>

    # Sub-label patterns: lines like "From Reference Test Cases:" or "Heuristics to apply:"
    SUB_LABEL_RE = re.compile(
        r"^(From Reference Test Cases|Exploratory Extensions.*|Heuristics to apply|"
        r"Specific areas to probe|Focus Areas)\s*:?\s*$",
        re.I
    )

    def flush_list():
        if list_buf:
            tag = list_type
            items_html = "".join(
                f"<li>{badge_inline(escape_html(t))}</li>" for t in list_buf
            )
            html_parts.append(f"<{tag}>{items_html}</{tag}>")
            list_buf.clear()

    def flush_prose():
        if prose_buf:
            para = " ".join(prose_buf)
            html_parts.append(f"<p>{escape_html(para)}</p>")
            prose_buf.clear()

    for line in lines:
        stripped = line.strip()

        if not stripped:
            flush_prose()
            flush_list()
            continue

        m_num   = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
        m_bul   = re.match(r"^\s*[-*]\s+(.+)$", line)
        m_alpha = re.match(r"^\s*[A-Z]\.\s+(.+)$", line)
        m_indent = re.match(r"^(\s{2,})(\S.*)$", line)

        if m_num:
            flush_prose()
            if list_type != "ol" and list_buf:
                flush_list()
            list_type = "ol"
            list_buf.append(m_num.group(2))
        elif m_bul:
            flush_prose()
            if list_type != "ul" and list_buf:
                flush_list()
            list_type = "ul"
            list_buf.append(m_bul.group(1))
        elif m_alpha:
            flush_prose()
            if list_type != "ul" and list_buf:
                flush_list()
            list_type = "ul"
            list_buf.append(m_alpha.group(1))
        elif m_indent and list_buf:
            list_buf[-1] += " " + stripped
        elif SUB_LABEL_RE.match(stripped):
            flush_prose()
            flush_list()
            label_text = stripped.rstrip(":")
            html_parts.append(f'<div class="sub-label">{escape_html(label_text)}</div>')
        else:
            flush_list()
            prose_buf.append(stripped)

    flush_prose()
    flush_list()
    return "\n".join(html_parts)


def render_md_table(lines: list, title_lower: str) -> str:
    rows = [l for l in lines if "|" in l and not re.match(r"^\|[-| ]+\|$", l)]
    if not rows:
        return ""

    header = [c.strip() for c in rows[0].strip("|").split("|")]
    data_rows = rows[1:]

    is_tc = any(k in title_lower for k in ("reference test", "scope", "test case", "covered"))
    is_defect = any(k in title_lower for k in ("defect", "known", "bug", "risk"))

    table_class = "tc-table" if is_tc else ("defect-table" if is_defect else "tc-table")

    th_html = "".join(f"<th>{escape_html(h)}</th>" for h in header)
    td_rows = []
    for row in data_rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        td_html = ""
        for i, cell in enumerate(cells):
            cell_html = escape_html(cell)
            # Status badge
            if cell.upper() in ("PASS", "PASSED"):
                cell_html = '<span class="badge badge-pass">PASS</span>'
            elif cell.upper() in ("FAIL", "FAILED"):
                cell_html = '<span class="badge badge-fail">FAIL</span>'
            # Severity colouring
            elif cell.lower() in ("high", "major"):
                cell_html = f'<span class="severity-high">{escape_html(cell)}</span>'
            elif cell.lower() == "medium":
                cell_html = f'<span class="severity-medium">{escape_html(cell)}</span>'
            elif cell.lower() in ("low", "minor"):
                cell_html = f'<span class="severity-low">{escape_html(cell)}</span>'
            td_html += f"<td>{cell_html}</td>"
        td_rows.append(f"<tr>{td_html}</tr>")

    return f"""<table class="{table_class}">
      <thead><tr>{th_html}</tr></thead>
      <tbody>{''.join(td_rows)}</tbody>
    </table>"""


def escape_html(text: str) -> str:
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def extract_charter_meta(md: str, filename: str) -> dict:
    """Extract charter ID, title, platform, area from the markdown content."""
    charter_id = os.path.splitext(os.path.basename(filename))[0].upper()
    title = charter_id
    platform = "Unknown"
    area = "General"

    lines = md.splitlines()
    in_mission = False
    mission_text = None

    for line in lines:
        stripped = line.strip()
        if re.match(r"^Charter ID\s*:", stripped, re.I):
            val = re.sub(r"^Charter ID\s*:\s*", "", stripped, flags=re.I).strip()
            if val:
                charter_id = val.split()[0]
        elif re.match(r"^#{1,2}\s+", stripped):
            candidate = re.sub(r"^#{1,2}\s+", "", stripped).strip()
            if candidate and candidate.upper() not in ("TEST CHARTER", "MISSION"):
                title = candidate
            if candidate.upper() == "MISSION":
                in_mission = True
        elif re.match(r"^Platform\s*:", stripped, re.I):
            platform = re.sub(r"^Platform\s*:\s*", "", stripped, flags=re.I).strip()
        elif re.match(r"^Mission Area\s*:|^Area\s*:", stripped, re.I):
            area = re.sub(r"^(Mission Area|Area)\s*:\s*", "", stripped, flags=re.I).strip()
        # Plain-text section marker (e.g. "MISSION" on its own line or under dashes)
        elif re.match(r"^MISSION\s*$", stripped):
            in_mission = True
        elif in_mission and stripped and not re.match(r"^[-=]{3,}$", stripped):
            # First substantive line of the MISSION section — use as title
            if mission_text is None and len(stripped) > 10:
                mission_text = stripped
            in_mission = False
        elif re.match(r"^[-=]{3,}$", stripped) and in_mission:
            pass  # separator line inside mission block, keep scanning

    # Use mission text as title if no # heading was found
    if title == charter_id and mission_text:
        # Truncate to a readable length
        title = mission_text[:80] + ("…" if len(mission_text) > 80 else "")

    # Derive area label from charter ID if not found in content
    area_labels = {
        "LOCALE": "Localization", "CART": "Shopping Cart", "AUTH": "Auth & Registration",
        "NAV": "Navigation & Banners", "SEARCH": "Search", "FILTER": "Filters & Sorting",
        "PROD": "Product Details", "REG": "Registration & Validation", "LAYOUT": "Layout & Responsiveness",
        "MOB": "Mobile", "TAB": "Tablet", "LAP": "Laptop",
    }
    if area == "General" and "-" in charter_id:
        parts = charter_id.split("-")
        if len(parts) >= 3:
            area_key = parts[2].upper()
            area = area_labels.get(area_key, area_key)

    # Always use the area label as the charter title — clean, short, readable in TOC and header
    title = area

    return {"id": charter_id, "title": title, "platform": platform, "area": area}


def build_html(platform: str, charter_files: list) -> str:
    accent = PLATFORM_COLOR.get(platform, "#4A90D9")
    accent_dark = hex_darken(accent)
    accent_light = hex_lighten(accent)
    label = PLATFORM_LABEL.get(platform, platform.title())
    now = datetime.now().strftime("%B %d, %Y")

    def sort_key(fpath):
        """Sort by the trailing sequence number in the filename (e.g. 001, 002)."""
        name = os.path.splitext(os.path.basename(fpath))[0]  # e.g. CHR-TAB-NAV-001
        parts = name.split("-")
        try:
            return int(parts[-1])
        except (ValueError, IndexError):
            return name  # fallback to alphabetical

    charters_data = []
    for fpath in sorted(charter_files, key=sort_key):
        with open(fpath, encoding="utf-8") as f:
            md = f.read()
        meta = extract_charter_meta(md, fpath)
        charters_data.append((meta, md))

    # Cover
    cover = f"""
    <div class="cover">
      <div class="label">Session-Based Test Management · SBTM</div>
      <h1>Test Charters<br>{label}</h1>
      <div class="subtitle">PrestaShop Demo Shop &nbsp;·&nbsp; demo.prestashop.com</div>
      <div class="meta">
        <span><strong>{len(charters_data)}</strong>Charters</span>
        <span><strong>{label}</strong>Platform</span>
        <span><strong>{now}</strong>Generated</span>
      </div>
    </div>"""

    PLATFORM_FULL = {
        "TAB": "Tablet", "LAP": "Laptop", "MOB": "Mobile",
    }
    AREA_FULL = {
        "NAV": "Navigation & Banners", "PROD": "Product Discovery",
        "LOCALE": "Localization", "FILTER": "Filters & Sorting",
        "REG": "Registration & Validation", "CART": "Shopping Cart",
        "AUTH": "Auth & Registration", "SEARCH": "Search",
        "LAYOUT": "Layout & Responsiveness",
    }

    def expand_id(charter_id: str) -> str:
        """Turn CHR-TAB-NAV-001 into  Charter · Tablet · Navigation & Banners · 001"""
        parts = charter_id.split("-")
        # parts: ['CHR', 'TAB', 'NAV', '001']  or  ['CHR', 'LAP', 'FILTER', '006']
        if len(parts) < 4:
            return charter_id
        plat = PLATFORM_FULL.get(parts[1].upper(), parts[1].title())
        area = AREA_FULL.get(parts[2].upper(), parts[2].title())
        seq  = parts[3].lstrip("0") or "1"
        return f"Charter &nbsp;·&nbsp; {plat} &nbsp;·&nbsp; {area} &nbsp;·&nbsp; #{seq}"

    # TOC
    toc_items = ""
    for i, (meta, _) in enumerate(charters_data, 1):
        toc_items += f"""
        <li>
          <a href="#{meta['id'].lower().replace(' ', '-')}">{meta['title']}</a>
          <span class="toc-area">{meta['area']}</span>
        </li>"""
    toc = f"""
    <div class="toc">
      <h2>Table of Contents</h2>
      <ol>{toc_items}</ol>
    </div>"""

    # Charter cards
    cards = []
    for meta, md in charters_data:
        anchor_id = meta['id'].lower().replace(' ', '-')
        body_html = md_to_html_content(md)
        card = f"""
    <div class="charter" id="{anchor_id}">
      <div class="charter-header">
        <div class="charter-id">{expand_id(meta['id'])}</div>
        <h2>{meta['title']}</h2>
        <div class="charter-meta">
          <span class="platform-badge">{meta['platform']}</span>
          <span class="platform-badge">{meta['area']}</span>
        </div>
      </div>
      <div class="charter-body">
        {body_html}
      </div>
    </div>"""
        cards.append(card)

    return HTML_TEMPLATE.format(
        title=f"Test Charters — {label}",
        accent=accent,
        accent_dark=accent_dark,
        accent_light=accent_light,
        cover=cover,
        toc=toc,
        charters="\n".join(cards),
    )


def main():
    parser = argparse.ArgumentParser(description="Combine charter .md files into one styled HTML.")
    parser.add_argument("--platform", required=True, choices=["tablet", "laptop", "mobile", "all"])
    parser.add_argument("--open", action="store_true", help="Open the HTML file in the browser after generating")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    platforms = ["tablet", "laptop", "mobile"] if args.platform == "all" else [args.platform]
    output_files = []

    for platform in platforms:
        prefix = PLATFORM_PREFIX[platform]
        pattern = os.path.join(OUTPUT_DIR, f"{prefix}*.md")
        files = glob.glob(pattern)

        if not files:
            print(f"[WARN] No charter .md files found for platform '{platform}' (pattern: {pattern})", file=sys.stderr)
            continue

        print(f"[INFO] Found {len(files)} charter file(s) for {platform}: {[os.path.basename(f) for f in sorted(files)]}", file=sys.stderr)

        html_content = build_html(platform, files)
        out_filename = f"CHARTERS-{platform.upper()}.html"
        out_path = os.path.join(OUTPUT_DIR, out_filename)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"[OK] Generated: {out_path}", file=sys.stderr)
        output_files.append(out_path)

    if args.platform == "all" and output_files:
        # Also generate a combined ALL file
        all_files = glob.glob(os.path.join(OUTPUT_DIR, "CHR-*.md"))
        if all_files:
            html_content = build_html("all", all_files)
            out_path = os.path.join(OUTPUT_DIR, "CHARTERS-ALL.html")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"[OK] Generated combined: {out_path}", file=sys.stderr)
            output_files.append(out_path)

    if args.open and output_files:
        for p in output_files:
            webbrowser.open(f"file://{p}")
            print(f"[INFO] Opened in browser: {p}", file=sys.stderr)

    # Print paths to stdout for the AI to reference
    for p in output_files:
        print(p)


if __name__ == "__main__":
    main()
