#!/usr/bin/env python3
"""
assemble-diagram.py — Combine base template with diagram-specific content.

Usage:
  python3 skill/scripts/assemble-diagram.py \
    --canvas canvas.html \
    --css diagram.css \
    --output output/my-project/my-diagram-v1.html \
    [--template lean|base]   # default: lean
    [--title "Diagram Title"] \
    [--subtitle "Architecture summary"] \
    [--footer "Legend text"]

The canvas file contains only the content that goes between
CANVAS-REPLACE-START and CANVAS-REPLACE-END in the base template.

The css file (optional) contains diagram-specific styles injected
between DIAGRAM-CSS-START and DIAGRAM-CSS-END.

--template lean  (default) uses skill/templates/oci-diagram-lean.html
                 No toolbar JS, no h2canvas. Lean ~60% smaller files.
                 Includes version nav pill + "Open in Viewer" button.
--template base  uses skill/templates/oci-diagram-base.html
                 Full toolbar JS and annotation overlay embedded.
                 Use for backward compatibility or standalone review docs.

Token savings with lean: ~80% reduction in generation output.
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
CANVAS_END = "<!-- CANVAS-REPLACE-END -->"

CSS_START = "DIAGRAM-CSS-START"
CSS_END = "DIAGRAM-CSS-END"


def load(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        sys.exit(f"ERROR: file not found: {path}")
    return p.read_text(encoding="utf-8")


def inject_canvas(template: str, canvas_html: str) -> str:
    # Find the CANVAS-REPLACE-START marker; walk back to start of that comment block
    marker_idx = template.find(CANVAS_START)
    if marker_idx == -1:
        sys.exit("ERROR: CANVAS-REPLACE-START marker not found in base template.")
    # Walk back to the start of the <!-- line
    line_start = template.rfind("\n", 0, marker_idx)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1  # skip the \n
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
    # Walk back to start of the /* line
    line_start = template.rfind("\n", 0, start_idx)
    line_start = 0 if line_start == -1 else line_start + 1
    end_idx = template.find(CSS_END, start_idx)
    if end_idx == -1:
        return template.replace("</style>", css.strip() + "\n</style>", 1)
    end_idx = template.find("\n", end_idx) + 1  # include the end marker line
    replacement = (
        "/* DIAGRAM-CSS-START */\n"
        + css.strip()
        + "\n/* DIAGRAM-CSS-END */\n"
    )
    return template[:line_start] + replacement + template[end_idx:]


def set_title(template: str, title: str) -> str:
    return template.replace(
        'class="diagram-title" data-editable="true">Diagram Title</h1>',
        f'class="diagram-title" data-editable="true">{title}</h1>',
        1,
    )


def set_subtitle(template: str, subtitle: str) -> str:
    return template.replace(
        'class="diagram-sub" data-editable="true">Short architecture summary</p>',
        f'class="diagram-sub" data-editable="true">{subtitle}</p>',
        1,
    )


def set_page_title(template: str, title: str) -> str:
    return re.sub(
        r"<title>[^<]*</title>",
        f"<title>{title}</title>",
        template,
        count=1,
    )


def set_footer(template: str, footer: str) -> str:
    return template.replace(
        'data-editable="true">Legend</span>',
        f'data-editable="true">{footer}</span>',
        1,
    )


def main():
    ap = argparse.ArgumentParser(description="Assemble OCI diagram from base template + canvas content")
    ap.add_argument("--canvas", required=True, help="Path to canvas HTML fragment file")
    ap.add_argument("--css", default="", help="Path to diagram-specific CSS file (optional)")
    ap.add_argument("--output", required=True, help="Output HTML path")
    ap.add_argument("--template", default="lean", choices=["lean", "base"],
                    help="Template to use: 'lean' (default, no toolbar JS) or 'base' (full toolbar embedded)")
    ap.add_argument("--title", default="", help="Diagram title (replaces 'Diagram Title')")
    ap.add_argument("--subtitle", default="", help="Diagram subtitle")
    ap.add_argument("--footer", default="", help="Footer legend text")
    args = ap.parse_args()

    tpl_path = TEMPLATES.get(args.template)
    if not tpl_path or not tpl_path.exists():
        sys.exit(f"ERROR: template '{args.template}' not found at {tpl_path}")
    template = load(str(tpl_path))
    canvas = load(args.canvas)
    css = load(args.css) if args.css else ""

    result = inject_canvas(template, canvas)
    result = inject_css(result, css)

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
