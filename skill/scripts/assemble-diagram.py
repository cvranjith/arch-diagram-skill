#!/usr/bin/env python3
"""
assemble-diagram.py — Combine base template with diagram-specific content.

── NEW DIAGRAM ────────────────────────────────────────────────────────────────
  python3 skill/scripts/assemble-diagram.py \
    --canvas output/<project>/canvas/<name>-vN-canvas.html \
    --css    output/<project>/canvas/<name>-vN.css \
    --output output/<project>/<name>-vN.html \
    [--template lean|base]   # default: lean
    [--title "Diagram Title"] \
    [--subtitle "Architecture summary"] \
    [--footer "Legend text"]

── REVISION (SSOT: always base on the previous assembled HTML) ────────────────
Step 1 — extract the section Claude needs to read/edit (token-efficient):
  python3 skill/scripts/assemble-diagram.py \
    --extract canvas \
    --html   output/<project>/<name>-vN.html \
    --output output/<project>/canvas/<name>-vN-canvas.html

  python3 skill/scripts/assemble-diagram.py \
    --extract css \
    --html   output/<project>/<name>-vN.html \
    --output output/<project>/canvas/<name>-vN.css

  python3 skill/scripts/assemble-diagram.py \
    --extract title \
    --html   output/<project>/<name>-vN.html   # prints to stdout

Step 2 — after editing the extracted file(s), assemble the new version:
  python3 skill/scripts/assemble-diagram.py \
    --base   output/<project>/<name>-vN.html \
    --canvas output/<project>/canvas/<name>-v(N+1)-canvas.html \
    [--css   output/<project>/canvas/<name>-v(N+1).css] \
    --output output/<project>/<name>-v(N+1).html

  --base mode copies the base HTML and substitutes only the sections provided.
  Everything else (title, subtitle, nav bar, footer) is preserved from the base.

── TEMPLATES ──────────────────────────────────────────────────────────────────
--template lean  (default) uses skill/templates/oci-diagram-lean.html
                 No toolbar JS. Includes version nav pill + "Open in Viewer".
--template base  uses skill/templates/oci-diagram-base.html
                 Full toolbar JS embedded (backward compat only).
"""
import argparse
import pathlib
import re
import sys

TEMPLATES = {
    "lean": pathlib.Path("skill/templates/oci-diagram-lean.html"),
    "base": pathlib.Path("skill/templates/oci-diagram-base.html"),
}

CANVAS_START = "CANVAS-REPLACE-START"
CANVAS_END   = "<!-- CANVAS-REPLACE-END -->"
CSS_START    = "DIAGRAM-CSS-START"
CSS_END      = "DIAGRAM-CSS-END"


def load(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        sys.exit(f"ERROR: file not found: {path}")
    return p.read_text(encoding="utf-8")


# ── Template-based injection (new diagrams) ────────────────────────────────

def inject_canvas(template: str, canvas_html: str) -> str:
    marker_idx = template.find(CANVAS_START)
    if marker_idx == -1:
        sys.exit("ERROR: CANVAS-REPLACE-START marker not found in base template.")
    # The CANVAS-REPLACE-START marker is intentionally placed inside an HTML
    # comment block in the templates. If we replace from the marker line only,
    # we can accidentally leave behind the opening "<!-- …" line without its
    # matching "-->" line, which comments out the injected canvas and makes
    # arch-viewer.html show a blank diagram.
    #
    # Fix: if the marker is inside an unclosed HTML comment, start replacement
    # from the beginning of that comment instead of the marker line.
    replace_from_idx = marker_idx
    comment_start = template.rfind("<!--", 0, marker_idx)
    if comment_start != -1:
        comment_end_before_marker = template.find("-->", comment_start, marker_idx)
        if comment_end_before_marker == -1:
            replace_from_idx = comment_start

    line_start = template.rfind("\n", 0, replace_from_idx)
    line_start = 0 if line_start == -1 else line_start + 1
    end_idx = template.find(CANVAS_END, marker_idx)
    if end_idx == -1:
        sys.exit("ERROR: CANVAS-REPLACE-END marker not found in base template.")
    end_idx += len(CANVAS_END)
    return template[:line_start] + canvas_html.strip() + "\n    " + template[end_idx:]


def inject_css(template: str, css: str) -> str:
    if not css.strip():
        return template
    start_idx = template.find(CSS_START)
    if start_idx == -1:
        return template.replace("</style>", css.strip() + "\n</style>", 1)
    line_start = template.rfind("\n", 0, start_idx)
    line_start = 0 if line_start == -1 else line_start + 1
    end_idx = template.find(CSS_END, start_idx)
    if end_idx == -1:
        return template.replace("</style>", css.strip() + "\n</style>", 1)
    end_idx = template.find("\n", end_idx) + 1
    replacement = "/* DIAGRAM-CSS-START */\n" + css.strip() + "\n/* DIAGRAM-CSS-END */\n"
    return template[:line_start] + replacement + template[end_idx:]


def set_title(template: str, title: str) -> str:
    # Works for both lean template (no data-editable) and base template (with data-editable)
    return re.sub(
        r'class="diagram-title"[^>]*>Diagram Title</h1>',
        f'class="diagram-title">{title}</h1>',
        template, count=1,
    )


def set_subtitle(template: str, subtitle: str) -> str:
    # Works for both lean template (no data-editable) and base template (with data-editable)
    return re.sub(
        r'class="diagram-sub"[^>]*>Short architecture summary</p>',
        f'class="diagram-sub">{subtitle}</p>',
        template, count=1,
    )


def set_page_title(template: str, title: str) -> str:
    return re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", template, count=1)


def set_footer(template: str, footer: str) -> str:
    # Works for both lean template (<span>Legend</span>) and base template (data-editable)
    return re.sub(
        r'(class="diagram-footer"[^>]*>.*?<span[^>]*>)Legend(</span>)',
        lambda m: m.group(1) + footer + m.group(2),
        template, count=1, flags=re.S,
    )


# ── Extract sections from an assembled HTML (for revisions) ───────────────

def extract_canvas(html: str) -> str:
    """Extract canvas content from an assembled HTML.
    Strips reviewLayer div, edit-mode attributes, and restores ../../ icon paths."""
    # The viewer/runbook historically included instructional comments that could
    # contain literal strings like "</main>", which breaks non-greedy regex
    # extraction. Strip HTML comments before extracting.
    html_wo_comments = re.sub(r"<!--[\s\S]*?-->", "", html)
    match = re.search(r'<main[^>]*id="diagramCanvas"[^>]*>([\s\S]*?)</main>', html_wo_comments)
    if not match:
        sys.exit('ERROR: <main id="diagramCanvas"> not found in HTML')
    content = match.group(1)
    # Remove the reviewLayer div (injected at runtime; not part of diagram source)
    content = re.sub(
        r'\s*<div[^>]*id="reviewLayer"[^>]*>[\s\S]*?</div>\s*', '\n', content, count=1
    )
    # Strip edit-mode artifacts added by arch-viewer's Save HTML
    content = re.sub(r'\s+contenteditable="false"', '', content)
    content = re.sub(r'\s+spellcheck="false"', '', content)
    # Restore ../../ icon paths (arch-viewer strips them on injection)
    content = content.replace(' src="skill/', ' src="../../skill/')
    content = content.replace(' href="skill/', ' href="../../skill/')
    return content.strip()


def extract_css(html: str) -> str:
    """Extract diagram-specific CSS block from an assembled HTML."""
    match = re.search(
        r'/\*\s*DIAGRAM-CSS-START\s*\*/([\s\S]*?)/\*\s*DIAGRAM-CSS-END\s*\*/', html
    )
    if not match:
        sys.exit("ERROR: DIAGRAM-CSS-START/END markers not found in HTML")
    return match.group(1).strip()


def extract_title(html: str) -> str:
    """Extract the diagram title from an assembled HTML."""
    match = re.search(r'class="diagram-title"[^>]*>([^<]+)</h1>', html)
    return match.group(1).strip() if match else ""


def extract_subtitle(html: str) -> str:
    """Extract the diagram subtitle from an assembled HTML."""
    match = re.search(r'class="diagram-sub"[^>]*>([^<]+)</p>', html)
    return match.group(1).strip() if match else ""


# ── Base-HTML-based assembly (revisions) ──────────────────────────────────

def replace_canvas_in_html(html: str, new_canvas: str) -> str:
    """Replace canvas content in an assembled HTML, preserving the reviewLayer div."""
    main_match = re.search(r'(<main[^>]*id="diagramCanvas"[^>]*>)', html)
    if not main_match:
        sys.exit('ERROR: <main id="diagramCanvas"> not found in base HTML')
    main_inner_start = main_match.end()
    main_end = html.find('</main>', main_inner_start)
    if main_end == -1:
        sys.exit("ERROR: </main> not found in base HTML")

    inner = html[main_inner_start:main_end]
    review_match = re.search(r'(<div[^>]*id="reviewLayer"[^>]*>[\s\S]*?</div>)', inner)
    if review_match:
        review_block = '\n              ' + review_match.group(1)
    else:
        review_block = ''

    return (
        html[:main_inner_start]
        + review_block
        + '\n              '
        + new_canvas.strip()
        + '\n            '
        + html[main_end:]
    )


def replace_css_in_html(html: str, new_css: str) -> str:
    """Replace the diagram CSS block in an assembled HTML."""
    start_idx = html.find(CSS_START)
    if start_idx == -1:
        sys.exit("ERROR: DIAGRAM-CSS-START not found in base HTML")
    line_start = html.rfind("\n", 0, start_idx)
    line_start = 0 if line_start == -1 else line_start + 1
    end_idx = html.find(CSS_END, start_idx)
    if end_idx == -1:
        sys.exit("ERROR: DIAGRAM-CSS-END not found in base HTML")
    end_idx = html.find("\n", end_idx) + 1
    replacement = "/* DIAGRAM-CSS-START */\n" + new_css.strip() + "\n/* DIAGRAM-CSS-END */\n"
    return html[:line_start] + replacement + html[end_idx:]


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Assemble OCI diagram HTML")
    ap.add_argument("--canvas", default="", help="Canvas HTML fragment file")
    ap.add_argument("--css",    default="", help="Diagram-specific CSS file (optional)")
    ap.add_argument("--output", default="", help="Output HTML path")

    # New diagram: use a template
    ap.add_argument("--template", default="lean", choices=["lean", "base"],
                    help="Template for new diagrams (default: lean)")
    ap.add_argument("--title",    default="", help="Diagram title")
    ap.add_argument("--subtitle", default="", help="Diagram subtitle")
    ap.add_argument("--footer",   default="", help="Footer legend text")

    # Revision: use an existing assembled HTML as base
    ap.add_argument("--base", default="",
                    help="Base assembled HTML for revision (preserves title/nav/footer)")

    # Extract a section from an assembled HTML
    ap.add_argument("--extract", choices=["canvas", "css", "title", "subtitle"],
                    help="Extract a section from --html and write to --output (or stdout)")
    ap.add_argument("--html", default="", help="Source HTML for --extract")

    args = ap.parse_args()

    # ── EXTRACT mode ──────────────────────────────────────────────────────
    if args.extract:
        if not args.html:
            sys.exit("ERROR: --extract requires --html")
        html = load(args.html)
        if args.extract == "canvas":
            content = extract_canvas(html)
        elif args.extract == "css":
            content = extract_css(html)
        elif args.extract == "title":
            content = extract_title(html)
        elif args.extract == "subtitle":
            content = extract_subtitle(html)
        else:
            sys.exit(f"ERROR: unknown extract target: {args.extract}")

        if args.output:
            out = pathlib.Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8")
            print(f"[assemble-diagram] extracted {args.extract} → {out}")
        else:
            print(content)
        return

    # ── ASSEMBLE mode: requires --output ──────────────────────────────────
    if not args.output:
        sys.exit("ERROR: --output is required for assembly")

    if args.base:
        # ── REVISION: base on existing assembled HTML ──────────────────
        result = load(args.base)
        if args.canvas:
            result = replace_canvas_in_html(result, load(args.canvas))
        if args.css:
            result = replace_css_in_html(result, load(args.css))
        # Title/subtitle overrides (optional — usually preserved from base)
        if args.title:
            result = re.sub(
                r'(class="diagram-title"[^>]*>)[^<]*(</h1>)',
                lambda m: m.group(1) + args.title + m.group(2),
                result, count=1
            )
            result = set_page_title(result, args.title)
        if args.subtitle:
            result = re.sub(
                r'(class="diagram-sub"[^>]*>)[^<]*(</p>)',
                lambda m: m.group(1) + args.subtitle + m.group(2),
                result, count=1
            )
    else:
        # ── NEW DIAGRAM: use template ──────────────────────────────────
        if not args.canvas:
            sys.exit("ERROR: --canvas is required when not using --base")
        tpl_path = TEMPLATES.get(args.template)
        if not tpl_path or not tpl_path.exists():
            sys.exit(f"ERROR: template '{args.template}' not found at {tpl_path}")
        result = load(str(tpl_path))
        result = inject_canvas(result, load(args.canvas))
        if args.css:
            result = inject_css(result, load(args.css))
        if args.title:
            result = set_title(result, args.title)
            result = set_page_title(result, args.title)
        if args.subtitle:
            result = set_subtitle(result, args.subtitle)
        if args.footer:
            result = set_footer(result, args.footer)

    out = pathlib.Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result, encoding="utf-8")
    print(f"[assemble-diagram] output={out} ({out.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
