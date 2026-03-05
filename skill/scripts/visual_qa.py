#!/usr/bin/env python3
"""
Deterministic visual QA for OCI diagram HTML outputs.

This script validates and optionally auto-fixes:
- panel/card contrast
- runtime layout whitespace risks
- icon sizing and icon placement uniformity
- layout container overflow/clip (fixed height + overflow:hidden → overlapping boxes)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Finding:
    code: str
    severity: str  # info|warn|error
    message: str
    fixed: bool = False


AUTO_FIX_MARKER = "Visual QA Auto-Fix"
AUTO_FIX_BEGIN = "/* Visual QA Auto-Fix: begin */"
AUTO_FIX_END = "/* Visual QA Auto-Fix: end */"


AUTO_FIX_BLOCK = (
    AUTO_FIX_BEGIN
    + """
/* Visual QA Auto-Fix: layout + icon uniformity + contrast */
.runtime-grid {
  display: grid;
  grid-template-columns: 180px 1fr;
  grid-template-areas:
    "orchestrator capabilities"
    "orchestrator genai";
  gap: 10px;
  align-items: start;
}
.orchestrator-box { grid-area: orchestrator; }
.capability-grid { grid-area: capabilities; }
.genai-panel { grid-area: genai; }
.layer {
  background: #E8E4DF;
  border: 1px solid #C3BDB7;
}
.service-card {
  background: #FFFFFF;
  border: 1px solid #CFC9C2;
  box-shadow: 0 1px 2px rgba(49,45,42,0.09);
}
.service-head,
.ai-service-head,
.doc-head {
  display: flex;
  align-items: center;
  gap: 6px;
}
.service-icon {
  width: 22px;
  height: 22px;
  text-align: center;
  font-size: 13px;
}
.ai-service-icon {
  width: 22px;
  height: 22px;
  text-align: center;
  font-size: 13px;
}
.doc-icon {
  width: 22px;
  height: 22px;
  text-align: center;
  font-size: 13px;
}
@media (max-width: 760px) {
  .runtime-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      "orchestrator"
      "capabilities"
      "genai";
  }
  .cap-col:not(:last-child)::after,
  .cap-col:not(:last-child)::before {
    display: none;
  }
}
"""
    + AUTO_FIX_END
).strip()


def _extract_style(html: str) -> Tuple[Optional[str], Optional[int], Optional[int]]:
    match = re.search(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)
    if not match:
        return None, None, None
    return match.group(1), match.start(1), match.end(1)


def _find_rule_body(css: str, selector: str) -> Optional[str]:
    """Return the body of the LAST CSS rule block where selector appears as a
    standalone (non-descendant) member of the selector list."""
    last_body = None
    block_pattern = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
    for m in block_pattern.finditer(css):
        # Split on commas to get individual selectors; strip whitespace
        selectors = [s.strip() for s in m.group(1).split(",")]
        # Only count an exact standalone match (avoids ".foo .service-head")
        if selector in selectors:
            last_body = m.group(2)
    return last_body


def _find_prop(rule_body: Optional[str], prop: str) -> Optional[str]:
    if not rule_body:
        return None
    match = re.search(rf"{re.escape(prop)}\s*:\s*([^;]+);", rule_body, re.I)
    if not match:
        return None
    return match.group(1).strip()


def _count_class_tokens(html: str, class_name: str) -> int:
    pattern = re.compile(
        rf"""<[^>]*\bclass\s*=\s*["'][^"']*\b{re.escape(class_name)}\b[^"']*["'][^>]*>""",
        re.I,
    )
    return len(pattern.findall(html))


def _parse_hex_color(value: Optional[str]) -> Optional[Tuple[int, int, int]]:
    if not value:
        return None
    color = value.strip().lower()
    if not color.startswith("#"):
        return None
    hex_value = color[1:]
    if len(hex_value) == 3:
        hex_value = "".join(ch * 2 for ch in hex_value)
    if len(hex_value) != 6:
        return None
    try:
        r = int(hex_value[0:2], 16)
        g = int(hex_value[2:4], 16)
        b = int(hex_value[4:6], 16)
        return r, g, b
    except ValueError:
        return None


def _luminance(rgb: Tuple[int, int, int]) -> float:
    def to_linear(channel: int) -> float:
        c = channel / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * to_linear(r) + 0.7152 * to_linear(g) + 0.0722 * to_linear(b)


def _validate(css: str, html: str) -> List[Finding]:
    findings: List[Finding] = []

    # 1) Runtime whitespace risk (classic 3-column + short right panel pattern)
    has_cap = "capability-grid" in html
    has_genai = "genai-panel" in html
    runtime_rule = _find_rule_body(css, ".runtime-grid")
    runtime_cols = _find_prop(runtime_rule, "grid-template-columns") or ""
    if has_cap and has_genai and len(runtime_cols.split()) >= 3:
        findings.append(
            Finding(
                code="runtime-layout-whitespace",
                severity="error",
                message=(
                    "Runtime layout uses a 3-column grid with genai panel as a side column; "
                    "this often leaves unused whitespace under capability columns."
                ),
            )
        )

    # 2) Contrast check between panel and card surfaces
    layer_rule = _find_rule_body(css, ".layer")
    card_rule = _find_rule_body(css, ".service-card")
    layer_bg = _find_prop(layer_rule, "background")
    card_bg = _find_prop(card_rule, "background")
    layer_rgb = _parse_hex_color(layer_bg)
    card_rgb = _parse_hex_color(card_bg)
    if layer_rgb and card_rgb:
        diff = abs(_luminance(layer_rgb) - _luminance(card_rgb))
        if diff < 0.06:
            findings.append(
                Finding(
                    code="panel-card-contrast",
                    severity="error",
                    message=(
                        f"Low panel/card contrast (luminance diff={diff:.3f}). "
                        "Use clearer surface separation."
                    ),
                )
            )

    # 3) Icon placement uniformity by card type
    checks = [
        ("service-card", "service-icon", "service cards"),
        ("ai-service-card", "ai-service-icon", "AI service cards"),
        ("doc-card", "doc-icon", "document cards"),
    ]
    for card_cls, icon_cls, label in checks:
        cards = _count_class_tokens(html, card_cls)
        icons = _count_class_tokens(html, icon_cls)
        if cards == 0:
            continue
        ratio = icons / cards if cards else 1.0
        if ratio < 0.70:
            findings.append(
                Finding(
                    code=f"{card_cls}-icon-coverage",
                    severity="error",
                    message=f"Low icon coverage for {label}: {icons}/{cards}.",
                )
            )
        elif ratio < 0.95:
            findings.append(
                Finding(
                    code=f"{card_cls}-icon-coverage",
                    severity="warn",
                    message=f"Partial icon coverage for {label}: {icons}/{cards}.",
                )
            )

    # 4) Icon sizing consistency
    expected = {
        ".service-icon": {"width": "22px", "font-size": "13px"},
        ".ai-service-icon": {"width": "22px", "font-size": "13px"},
        ".doc-icon": {"width": "22px", "font-size": "13px"},
    }
    for selector, props in expected.items():
        body = _find_rule_body(css, selector)
        if body is None:
            findings.append(
                Finding(
                    code=f"{selector}-missing",
                    severity="error",
                    message=f"Missing selector rule: {selector}.",
                )
            )
            continue
        for prop, val in props.items():
            actual = _find_prop(body, prop)
            if actual != val:
                findings.append(
                    Finding(
                        code=f"{selector}-{prop}",
                        severity="warn",
                        message=f"{selector} {prop} is '{actual}', expected '{val}'.",
                    )
                )

    # 5) Head wrappers for icon/title alignment
    for selector in [".service-head", ".ai-service-head", ".doc-head"]:
        body = _find_rule_body(css, selector)
        display = _find_prop(body, "display")
        if display != "flex":
            findings.append(
                Finding(
                    code=f"{selector}-display",
                    severity="warn",
                    message=f"{selector} should use display:flex for consistent icon/title alignment.",
                )
            )

    # 6) Overlap / content-clip risk: layout containers with fixed height + overflow:hidden
    #    Scan ALL rule blocks (not just the last) so @media overrides don't hide the issue.
    #    Any section/layer/lane container using height:Npx + overflow:hidden will clip or
    #    overlap cards when content grows beyond the fixed size.
    _LAYOUT_CONTAINER_SELECTORS = [
        ".integration-layer", ".layer", ".lane", ".section",
        ".diagram-section", ".arch-section", ".region-box",
    ]
    # Use raw block scan to catch the offending rule regardless of cascade order
    _block_scan = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
    _already_flagged: set = set()
    for _m in _block_scan.finditer(css):
        _rule_selectors = [s.strip() for s in _m.group(1).split(",")]
        _body = _m.group(2)
        for sel in _LAYOUT_CONTAINER_SELECTORS:
            if sel not in _rule_selectors or sel in _already_flagged:
                continue
            # Match bare `height: Npx` but NOT `min-height` or `max-height`
            _height_m = re.search(r"(?<![a-z-])height\s*:\s*(\d+px)", _body)
            _overflow_m = re.search(r"\boverflow\s*:\s*(hidden|clip)\b", _body)
            if _height_m and _overflow_m:
                _already_flagged.add(sel)
                findings.append(
                    Finding(
                        code=f"{sel}-overflow-clip",
                        severity="error",
                        message=(
                            f"{sel} uses height:{_height_m.group(1)} with overflow:{_overflow_m.group(1)}. "
                            "This clips content and causes overlapping boxes. "
                            "Use min-height and overflow:visible instead."
                        ),
                    )
                )
            elif _height_m and not _overflow_m:
                _already_flagged.add(sel)
                findings.append(
                    Finding(
                        code=f"{sel}-fixed-height",
                        severity="warn",
                        message=(
                            f"{sel} uses a fixed height:{_height_m.group(1)}. "
                            "Prefer min-height so the container grows with its content."
                        ),
                    )
                )

    return findings


def _fix_overflow_clips(html: str) -> Tuple[str, bool]:
    """Replace fixed height + overflow:hidden on known layout containers with
    min-height + overflow:visible to prevent content clipping / overlapping boxes."""
    changed = False
    css, start, end = _extract_style(html)
    if css is None or start is None or end is None:
        return html, False

    # Regex: inside a rule body, replace `height: Npx` (not min-height) with `min-height: Npx`
    # and `overflow: hidden` with `overflow: visible`, for layout container selectors only.
    _LAYOUT_SELECTORS_RE = re.compile(
        r"(\.integration-layer|\.layer\b|\.lane\b|\.section\b|\.diagram-section|\.arch-section|\.region-box)"
        r"(\s*\{[^}]*?)"
        r"(height\s*:\s*)(\d+px)"
        r"([^}]*?\})",
        re.S,
    )

    def _patch_rule(m: re.Match) -> str:
        rule = m.group(0)
        # Replace bare height:Npx with min-height:Npx (negative lookbehind avoids min-height/max-height)
        rule = re.sub(r"(?<![a-z-])height\s*:\s*(\d+px)", r"min-height: \1", rule)
        # Replace overflow:hidden with overflow:visible in the same rule
        rule = re.sub(r"\boverflow\s*:\s*hidden\b", "overflow: visible", rule)
        return rule

    new_css = _LAYOUT_SELECTORS_RE.sub(_patch_rule, css)
    if new_css != css:
        changed = True
        html = html[:start] + new_css + html[end:]

    return html, changed


def _apply_auto_fix(html: str) -> Tuple[str, bool]:
    css, start, end = _extract_style(html)
    if css is None or start is None or end is None:
        return html, False

    updated_css = css
    if AUTO_FIX_BEGIN in css and AUTO_FIX_END in css:
        pattern = re.compile(
            rf"{re.escape(AUTO_FIX_BEGIN)}.*?{re.escape(AUTO_FIX_END)}",
            re.S,
        )
        updated_css = pattern.sub(AUTO_FIX_BLOCK, css, count=1)
    elif AUTO_FIX_MARKER in css:
        # Backward compatibility with earlier single-marker block appended at end.
        marker_index = css.find("/* Visual QA Auto-Fix:")
        if marker_index >= 0:
            updated_css = css[:marker_index].rstrip() + "\n\n" + AUTO_FIX_BLOCK + "\n"
    else:
        updated_css = css.rstrip() + "\n\n" + AUTO_FIX_BLOCK + "\n"

    if updated_css == css:
        return html, False

    updated_html = html[:start] + updated_css + html[end:]
    return updated_html, True


def _try_screenshot(html_path: Path, screenshot_path: Path) -> Tuple[bool, str]:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        return False, "playwright not available in this environment"

    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
    uri = html_path.resolve().as_uri()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1600, "height": 980})
            page.goto(uri)
            page.wait_for_timeout(500)
            page.screenshot(path=str(screenshot_path), full_page=True)
            browser.close()
        return True, f"screenshot saved: {screenshot_path}"
    except Exception as exc:
        return False, f"screenshot failed: {exc}"


def _summarize(findings: List[Finding]) -> Dict[str, int]:
    counts = {"info": 0, "warn": 0, "error": 0}
    for item in findings:
        counts[item.severity] = counts.get(item.severity, 0) + 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Visual QA for OCI architecture diagram HTML.")
    parser.add_argument("--html", required=True, help="Path to generated HTML file.")
    parser.add_argument("--fix", action="store_true", help="Apply deterministic visual fixes before validating.")
    parser.add_argument("--require-pass", action="store_true", help="Exit non-zero when validation has errors.")
    parser.add_argument("--report", help="Optional JSON report output path.")
    parser.add_argument(
        "--screenshot",
        help="Optional screenshot path. Captured only if Playwright is available.",
    )
    args = parser.parse_args()

    html_path = Path(args.html).resolve()
    if not html_path.exists():
        print(f"[visual-qa] ERROR: HTML not found: {html_path}", file=sys.stderr)
        return 2

    html = html_path.read_text(encoding="utf-8")
    findings: List[Finding] = []
    fixed_any = False

    if args.fix:
        # Fix 1: overflow-clip on layout containers (height+overflow:hidden → min-height+overflow:visible)
        html_after_clip, clip_changed = _fix_overflow_clips(html)
        if clip_changed:
            html = html_after_clip
            fixed_any = True
            findings.append(
                Finding(
                    code="overflow-clip-fixed",
                    severity="info",
                    message="Fixed layout containers: replaced fixed height+overflow:hidden with min-height+overflow:visible to prevent content overlap.",
                    fixed=True,
                )
            )

        # Fix 2: standard auto-fix block (layout, contrast, icon sizing/alignment)
        html_after_fix, changed = _apply_auto_fix(html)
        if changed:
            html = html_after_fix
            fixed_any = True
            findings.append(
                Finding(
                    code="auto-fix-applied",
                    severity="info",
                    message="Applied visual QA auto-fix block (layout, contrast, icon sizing/alignment).",
                    fixed=True,
                )
            )

        if fixed_any:
            html_path.write_text(html, encoding="utf-8")

    css, _, _ = _extract_style(html)
    if css is None:
        findings.append(Finding(code="style-block-missing", severity="error", message="No <style> block found in HTML."))
    else:
        findings.extend(_validate(css, html))

    if args.screenshot:
        ok, msg = _try_screenshot(html_path, Path(args.screenshot))
        findings.append(
            Finding(
                code="screenshot",
                severity="info" if ok else "warn",
                message=msg,
            )
        )

    counts = _summarize(findings)
    qa_pass = counts["error"] == 0

    print(f"[visual-qa] file={html_path}")
    print(f"[visual-qa] fixed={str(fixed_any).lower()} pass={str(qa_pass).lower()} errors={counts['error']} warns={counts['warn']}")
    for item in findings:
        marker = "FIXED" if item.fixed else item.severity.upper()
        print(f"[visual-qa] {marker} {item.code}: {item.message}")

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "file": str(html_path),
            "pass": qa_pass,
            "fixed": fixed_any,
            "summary": counts,
            "findings": [asdict(item) for item in findings],
        }
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if args.require_pass and not qa_pass:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
