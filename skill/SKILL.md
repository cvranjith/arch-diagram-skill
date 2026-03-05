---
name: arch-diagram
description: Create and iterate professional Oracle OCI architecture diagrams as standalone HTML with Redwood-consistent styling, OCI icon assets, versioned output naming, and built-in quick-edit mode. Use when users provide architecture ideas, sketches, screenshots, drafts, or existing HTML and want polished OCI-style diagram generation or revisions ready for architecture and technical audiences.
---

# arch-diagram Skill

## Load Before Work
1. `skill/references/STYLE.md`
2. `skill/references/PATTERNS.md`
3. `skill/assets/icons/oci_icons.json`
4. `skill/templates/oci-diagram-lean.html` ← **default template (March 2026)**

## Core Behavior
- Generate polished OCI-styled architecture diagrams as standalone HTML.
- Always save files as versioned outputs under `output/<project>/`.
- **NEVER edit or overwrite an existing `vN.html` file after it has been written.** Every change — including bug fixes, layout corrections, and visual tweaks — MUST produce a new `v(N+1).html` file. Editing an existing version in place is always wrong.
- **Default layout: slide-fit ON.** Generated HTML must initialize with slide layout active (call `setSlideLayout(true)` on page load, not `false`). The full-layout toggle is the user override. Change the JS init from `params.get("layout") === "slide"` check to default ON: `if (params.get("layout") !== "full") { setSlideLayout(true); }`
- Include quick-edit mode in every generated HTML.
- Keep a common shell across all diagrams: Oracle top bar + reusable edit/export controls.
- Use the Oracle white wordmark logo style from the base template (inline SVG image), not plain text `ORACLE`.
- Ensure output quality is presentation-ready for architects and technical stakeholders.

## Requirement Clarification (Mandatory)
Before generating a new diagram, ask targeted clarifying questions and ideate with the user. This structured discovery phase avoids costly HTML iteration later.

Ask about:
1. Diagram goal and target audience (architecture review, executive presentation, dev handoff…).
2. Scope boundaries — what is in scope, what is explicitly out of scope.
3. Required OCI services and non-OCI systems (on-prem, third-party SaaS, cloud-to-cloud).
4. Network/grouping structure (OCI Region, VCN, AD, subnet, on-prem zone, 3rd-party boundary).
5. Data flow direction, connector labels, and security/trust boundaries.
6. Required annotations (HA, DR, compliance zones, environments, protocol labels).
7. Output naming preferences (`project` slug and `diagram-name` slug, both kebab-case).

After questions, provide a **short requirement summary** and wait for explicit user confirmation.

**Then generate an ASCII wireframe** (see ASCII Wireframe section below) to validate layout before HTML.
Only after the user approves the wireframe (or explicitly says "skip wireframe / build now") should you proceed to HTML generation.

## Input Handling
Accept any of:
- Free-text architecture description.
- Pasted draft/ASCII flow.
- Screenshot/image in `input/`.
- Existing HTML version for edits.

## ASCII Wireframe (After Clarification, Before HTML)

After requirements are confirmed, generate a rough ASCII art wireframe so the user can validate the layout cheaply before HTML generation. This is the most important iteration gate — changing the wireframe costs nothing; changing HTML costs time.

### When to generate a wireframe
- **Always** for new diagrams, after requirement confirmation.
- **Skip** only when the user explicitly says "skip wireframe", "go straight to HTML", or is providing an existing HTML/screenshot for revision.

### Wireframe format rules
- Use box-drawing characters: `┌ ─ ┐ │ └ ┘ ├ ┤ ┬ ┴ ┼ ╔ ═ ╗ ║ ╚ ╝`
- Show every major container: OCI Region, VCN, subnet, swimlane, on-prem zone, 3rd-party boundary.
- Show each service/component as a named box: `[Service Name]` or `┌───────────┐ │ Service   │ └───────────┘`
- Show connectors with `→` `←` `↔` `-->` `- - ->` for flows; label important ones inline.
- Keep it schematic — proportional layout matters more than exact sizing.
- Target ~30–60 lines. Enough to see the structure; not so detailed that it defeats the purpose.
- Do not worry about colour, icons, or styling — names and positions only.

### Wireframe content checklist
1. Title / diagram name at the top.
2. All major grouping containers (rows, swimlanes, regions) with labels.
3. Every service card from the requirements — grouped in the right section.
4. Primary data flows between sections (arrows with short labels).
5. Boundary separators: on-prem vs. cloud, internal vs. external, security zone.
6. Any special nodes called out in requirements (HA replicas, DR site, audit layer…).

### Example wireframe skeleton
```
┌─────────────────── INTEGRATION LANDSCAPE ──────────────────────────┐
│                                                                     │
│  ┌──────────────────── TOP: AUXILIARY SERVICES ───────────────┐    │
│  │ [Ref Data]  [Notifications]  [FX Contracts]  [Reports]     │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌── CHANNELS ──┐  ┌──── PAYMENT HUB ──────────────┐  ┌─ EXT ──┐  │
│  │ [E-Channels] │  │  [BEST Filter] | [ESB]         │  │[I.Bus] │  │
│  │ [E-SOC]      │→ │  ┌─ Payment Hub ─────────────┐ │→ │[SWIFT] │  │
│  │ [Branch]     │  │  │         [OBPM]            │ │  │[ITMX]  │  │
│  │ [OTC]        │  │  │  TT  DD  BAHTNET          │ │  └────────┘  │
│  └──────────────┘  │  └───────────────────────────┘ │             │
│                    └────────────────────────────────┘             │
│                                                                     │
│  ┌──────────────── BOTTOM: CORE SYSTEMS ──────────────────────┐    │
│  │ [Core Banking]  [EPX]  [SSO/IAM]  [SIEM]  [HO Systems]    │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

### Wireframe iteration protocol
1. Present wireframe with: *"Does this layout match your vision? Any sections to add, remove, or rearrange before I build the HTML?"*
2. Accept free-text edits: "move X to the right lane", "add a monitoring row", "merge A and B into one box".
3. Re-generate the wireframe in-place (no file needed — ASCII only in chat).
4. Repeat until the user says the layout is correct.
5. Only then run `next_version_path.py` and generate the HTML.

**Wireframe changes are free iterations — no versioned files, no QA scripts. HTML generation begins only after explicit wireframe approval.**

## Output Naming Rules
- Project slug: `output/<project>/` using kebab-case.
- Diagram filename: `<diagram-name>-vN.html` using kebab-case.
- Version sequence must increment (`v1`, `v2`, `v3`, ...). **Never reuse an existing version number.**
- **Always run `python3 skill/scripts/next_version_path.py --project <project> --name <diagram-name>` to compute the next path before writing.** Do not guess or hardcode a version number.
- The next-version script is the single source of truth for what version to write next.

## Styling Rules
- Follow `skill/references/STYLE.md` exactly for palette, spacing, typography, card anatomy, and connector treatments.
- Follow `skill/references/PATTERNS.md` for base CSS and layout patterns.
- Use off-white page background and white service cards.
- Use OCI Redwood-aligned typography and color system only.
- **DEFAULT PALETTE: Always use the standard Oracle Redwood palette** (Ocean #2C5967, Sienna #AE562C, Bark #312D2A, Oracle Red #C74634, Ivy #759C6C). These are Oracle's official brand colours. The extended vivid palette (`--vivid-teal/orange/cobalt/forest/grape`) deviates from Oracle standard — **use vivid palette ONLY when the user explicitly says the diagram looks too grey/muted or requests more vivid/bright colours.** Do NOT use vivid colours as the default for Oracle product architecture diagrams.
- For OCI PPT-style outputs, keep neutral-gray dominant surfaces and apply sienna/ocean as restrained accents instead of heavy solid fills.
- Ensure visible contrast between background containers and foreground cards (do not use same-tone fills for both).
- Use only subtle shadows for separation; avoid heavy presentation-style effects.
- For database layers, prefer Oracle-like database-system nodes with OCI icon assets (for example `database-system`) and a single DB name label below (instead of plain text pills) when space allows.

### Layout & Overflow — NON-NEGOTIABLE RULES
Overlapping or clipped content is a hard failure. These rules prevent it.

1. **Never use `height: <Npx>` with `overflow: hidden` on section/lane/layer containers.** Fixed height + hidden overflow is the #1 cause of overlapping boxes. Always use `min-height` so containers grow with their content.
2. **Use `min-height` (not `height`) for all diagram section containers** (`.integration-layer`, `.lane`, `.layer`, `.section`, any named region box). The one exception is the slide-viewport scroll boundary which is intentional.
3. **Grid rows that contain cards must use `auto` or `minmax(min-content, Npx)`.** Never use a bare `Npx` row height — it clips content if cards grow taller. Use `minmax(min-content, 1fr)` or `minmax(min-content, 100px)` to let rows expand.
4. **Never use `overflow: hidden` on layout containers** (`.layer`, `.lane`, `.integration-layer`, `.section`, grid track wrappers). Reserve `overflow: hidden` only for UI chrome (slide viewport, review SVG layer, scrolling panels with explicit scroll fallback).
5. **After writing a diagram, mentally trace each column/row with the most cards** and verify no container has a fixed pixel height that could be shorter than its content.

### Visual Richness — NON-NEGOTIABLE RULES
These rules are mandatory on every diagram. They are what separate a polished professional diagram from a flat one.

1. **Icon chip size: 22×22px minimum.** Never use 18px chips. Small chips are invisible and unprofessional.
2. **Category-matched chip colors.** Apply `.chip-ocean`, `.chip-sienna`, `.chip-red`, `.chip-ivy`, `.chip-bark`, or vivid variant chip classes to every `.card-icon` based on the card's accent color. Never use the same chip color across all categories.
3. **Card title: 13px, font-weight 700.** Bold, clearly readable titles. Do not use 12px/600 or lighter.
4. **Left accent bar: 5px minimum width.** The bar is the category signal — thinner bars get lost.
5. **Primary flow connectors: Ocean (#2C5967), 1.5px.** Use for the main architectural flow path. Secondary hops: Bark 1px. Optional paths: dashed Neutral 4. Never make all connectors the same color.
6. **Swimlane/section headers: prominent.** Use the enhanced `.swimlane-label` style (9.5px, 0.10em spacing, 2px bottom border) for full-width lane headers.
7. **Include the chip CSS block.** Every diagram's `<style>` must include `.chip-ocean`, `.chip-sienna`, `.chip-red`, `.chip-ivy`, `.chip-bark` classes. If using vivid palette, also include `.chip-vivid-teal`, `.chip-vivid-orange`, `.chip-vivid-cobalt`, `.chip-vivid-forest`, `.chip-vivid-grape`.
8. **Vary accent bar colours across card groups — use the full OCI palette, including vivid variants.** By default every swimlane/group must receive a semantically assigned accent colour. A diagram with 6+ cards that uses only one accent colour is a quality failure. When the diagram looks "too grey" or "too muted", switch to the **vivid palette** (`--vivid-teal`, `--vivid-orange`, `--vivid-cobalt`, `--vivid-forest`, `--vivid-grape`) defined in STYLE.md Extended Vivid Palette section. Only use uniform colouring when the user explicitly requests it. Include `--vivid-*` CSS variable definitions in the `<style>` block when using vivid palette colours.

## Icon Rules
Priority:
1. OCI icon from `skill/assets/icons/oci_icons.json` (primary source)
2. Font Awesome fallback if no appropriate OCI icon is available in the local OCI assets
3. Never use emoji, Unicode symbol icons, or pictograms

Additional icon constraints:
- OCI source assets are available locally under `source/oracle-downloads/` and `source/extracted/`.
- Prefer OCI icons whenever a semantically suitable icon exists.
- For Font Awesome fallback, prefer `fa-solid` icons and apply OCI palette colors (Ocean/Sienna/Bark as appropriate).
- Keep icon style professional and consistent across the full diagram; avoid mixed visual styles.
- **Icon chips: 22×22px minimum.** Set `font-size: 13px` for FA icons inside chips; set `width/height: 15px` for OCI SVG icons inside chips.
- **Always add the category chip class** to the icon chip element: `.chip-ocean` for ocean-category cards, `.chip-sienna` for sienna-category, `.chip-red` for security/human-process, `.chip-ivy` for compute, `.chip-bark` for observability.
- Every diagram `<style>` block must define the five chip classes: `.chip-ocean`, `.chip-sienna`, `.chip-red`, `.chip-ivy`, `.chip-bark`.

### Tech Brand Icons — NEVER inline SVG path data
Technology icons (Kafka, Kubernetes, Docker, Spring, etc.) are saved in `skill/assets/icons/tech/` with hardcoded brand colors.
**Always use `<img>` tags — never embed raw SVG path data inline in generated HTML.**

```html
<!-- CORRECT — zero generation token cost for the SVG path -->
<img src="../../skill/assets/icons/tech/kafka.svg" width="14" height="14" alt="Kafka">

<!-- WRONG — inlining the full SVG path wastes ~120 tokens per icon -->
<svg viewBox="0 0 24 24"><path d="M9.71 2.136..."/></svg>
```

Relative path from `output/<project>/` to tech icons: `../../skill/assets/icons/tech/ICON.svg`
Available: `kafka.svg` (#231F20), `kubernetes.svg` (#326CE5), `docker.svg` (#2496ED), `spring.svg` (#6DB33F)
For white icons inside colored chips, add CSS: `img { filter: brightness(0) invert(1); }`

## HTML Assembly — Lean Template is Default (March 2026)
**NEVER write a complete HTML file from scratch.** Always assemble from a template using `assemble-diagram.py`.
This is the primary performance optimization: the model only generates canvas content (~150–300 lines), not the full base template (saves ~80% token output).

### Templates
| Flag | Template file | Use when |
|---|---|---|
| `--template lean` **(default)** | `skill/templates/oci-diagram-lean.html` | Default for all new diagrams |
| `--template base` | `skill/templates/oci-diagram-base.html` | Backward compat / self-contained review docs |

**Lean template** (~60% smaller output): no toolbar JS, no h2canvas embedded. Includes Oracle nav bar + "Open in Viewer" button that links to `arch-viewer.html`. Includes version nav pill (bottom-right, pure JS, no fetch). All editing/annotation/export/PNG is done in `arch-viewer.html`.

**arch-viewer.html** (project root `arch-viewer.html`): Full-featured standalone viewer. Drop a lean diagram HTML file → viewer parses and injects diagram + CSS. Contains all toolbar features: Edit, Annotate, Export PNG, Save HTML, Copy HTML, Slide Layout, Prev/Next version (File System Access API).

### Workflow
1. Write diagram-specific CSS to `skill/canvas/<project>/<name>-vN.css`
2. Write canvas HTML fragment to `skill/canvas/<project>/<name>-vN-canvas.html`
   - Canvas contains only the content between `CANVAS-REPLACE-START` and `CANVAS-REPLACE-END`
   - Do NOT include `<html>`, `<head>`, `<style>`, `<body>`, nav bar, toolbar, or `<script>`
3. Run assemble with `--template lean` (the default):
   ```
   python3 skill/scripts/assemble-diagram.py \
     --template lean \
     --canvas skill/canvas/<project>/<name>-vN-canvas.html \
     --css skill/canvas/<project>/<name>-vN.css \
     --output output/<project>/<name>-vN.html \
     --title "Diagram Title" \
     --subtitle "Architecture summary" \
     --footer "Legend text"
   ```
4. Run visual QA on the assembled output

### What the lean template provides (do NOT re-implement these)
- Oracle top nav bar with Oracle wordmark logo
- "Open in Viewer" button → links to `arch-viewer.html?file=<relative-path>`
- Version navigation pill (bottom-right): ← vN-1 | vN | vN+1 →, pure JS, file:// safe
- All diagram base CSS (palette, cards, chips, `.db-node`, footer)

### `.db-node` — Reusable Persistence Component
Use for database or event-bus nodes in a persistence layer. Defined in lean template base styles.
```html
<div class="db-node" style="--db-color: var(--oracle-red)">
  <div class="db-node-icon"><i class="fa-solid fa-database"></i></div>
  <div class="db-node-name">VAM Schema</div>
  <div class="db-node-type">Oracle DB 19c</div>
</div>

<!-- With tech brand icon (Kafka, etc.) -->
<div class="db-node" style="--db-color: #231F20">
  <div class="db-node-icon"><img src="../../skill/assets/icons/tech/kafka.svg" alt="Kafka"></div>
  <div class="db-node-name">Event Hub</div>
  <div class="db-node-type">Apache Kafka</div>
</div>
```
`--db-color` drives the icon circle color. Wrap multiple `db-node` elements in a `.persistence-layer` flex container.

The canvas file is the ONLY thing generated per diagram. Everything else is fixed and reused.

## Quick-Edit Requirement
Every generated HTML must include:
- A visible toggle for edit mode.
- `contenteditable` activation for titles, labels, and card text.
- A direct way to persist edits back to an HTML artifact (`Save HTML` via File System Access API or download fallback).
- A fast way to copy edited HTML markup (clipboard button is recommended).
- A quick PNG export option (prefer `html2canvas`) for slide-ready capture.
- A `Review Annotate` control for in-place review markup:
  - Add draggable sticky-note style comments on click.
  - Support draggable pointer targets with dotted connector lines so each comment maps to an exact point/area.
  - Include an in-toolbar review markup palette for `Sticky`, `Rectangle`, `Oval`, and `Pen` (freehand).
  - Include review style controls for drawn markup: `Solid/Dashed/Dotted`, color picker, and stroke width.
  - Allow selecting/repositioning/deleting drawn markup (`Delete Mark` button and keyboard delete).
  - Hide review markup controls when review mode is off to keep the default toolbar clean.
  - Keep annotations in the DOM so `Save HTML`, `Copy HTML`, and screenshots retain review context.
- A top-bar toggle to switch between **slide layout (default ON)** and full layout.
- **Slide layout is the default on page load.** Design all diagrams to target 16:9 fit first — use compact card sizing, tight spacing, and `min-height` (not fixed heights) so content fits. Only fall back to scroll when genuine content volume exceeds readable fit. Never clip or truncate content.
- The top-bar toggle lets users switch to full-layout (scroll) if needed, but diagrams must open in slide-fit mode.
- A top-bar toggle to show/hide the bottom edit toolbar for clean screenshots.

Use `skill/templates/oci-diagram-base.html` as the starter shell and keep its edit-mode controls.

## Revision Workflow
When user asks for changes (or when fixing any issue in a delivered diagram):
1. Run `next_version_path.py` to get the correct `v(N+1)` output path. **Do not skip this step.**
2. Read the latest output version (`vN`).
3. Apply requested changes only.
4. Write the result to the new `v(N+1)` path. **Never edit `vN` in place.**
5. Add a short HTML comment at the top listing what changed vs. the previous version.

> Rule: if a diagram file already exists on disk, it is immutable. Every change — no matter how small — creates a new version.

## Automatic Visual QA Gate (Mandatory Before Delivery)
After generating or revising any diagram HTML, run visual QA before sharing output:

1. Auto-fix + validate:
   - `python3 skill/scripts/visual_qa.py --html <output-file> --fix --require-pass --report <output-file>.visual-qa.json`
2. Optional screenshot capture (best-effort, when Playwright is available):
   - `python3 skill/scripts/visual_qa.py --html <output-file> --require-pass --screenshot <output-file>.visual-qa.png --report <output-file>.visual-qa.json`

Rules:
- Do not present final output to user unless visual QA returns pass (no errors).
- If auto-fix changed the file, re-run QA once and confirm pass.
- Keep the QA JSON report next to the output file for traceability.

## Quality Checklist
- **Requirement clarification questions were asked** before any diagram work.
- **ASCII wireframe was presented and approved** (or user explicitly skipped) before HTML generation.
- OCI nav bar present with Oracle logo and top-bar layout/tool toggles.
- Colors match OCI palette only.
- Grouping boxes follow OCI style types.
- **Primary flow connectors use Ocean (#2C5967, 1.5px); secondary use Bark (1px); optional/async use dashed Neutral 4.** NOT all connectors bark/gray.
- Icons are OCI-first, with Font Awesome only when OCI icon is unavailable.
- Major boxes/cards include semantically appropriate icons (runtime blocks, service cards, AI service cards, knowledge/source cards).
- **Icon chips are 22×22px minimum** — never 18px.
- **Icon chips use category-matched chip class** (chip-ocean / chip-sienna / chip-red / chip-ivy / chip-bark, or vivid variant) — not uniform ocean for all cards.
- **At least 3 distinct accent colours are visible** across diagrams with 6+ cards — each swimlane/group has a different colour identity using the OCI palette or vivid palette.
- **Card titles are 13px, font-weight 700** — not 12px/600.
- **Left accent bars are 5px wide** — not 3-4px.
- **Chip CSS classes defined in the `<style>` block** — standard 5 (chip-ocean/sienna/red/ivy/bark) always included; vivid chip classes (chip-vivid-teal/orange/cobalt/forest/grape) included when using vivid palette.
- **When vivid palette is used:** `--vivid-teal/orange/cobalt/forest/grape` CSS variables defined in `:root` of the HTML output.
- Database layer visuals follow Oracle-style DB nodes (OCI DB icon above, DB name below) unless the user requests a different pattern.
- No emoji or Unicode icon substitutes anywhere in the diagram.
- Foreground cards are visually distinct from their parent panels.
- Section labels / swimlane headers are prominent and scannable.
- Add dotted/dashed flow connectors when they improve process readability.
- **No section/lane/layer container uses `height: <Npx>` + `overflow: hidden`** — all use `min-height` so content never clips or overlaps.
- **All grid rows containing cards use `auto`, `minmax(min-content, Npx)`, or `1fr`** — never a bare pixel height.
- Visual QA script executed and passed (`errors=0`).
- **Template: lean used** (`--template lean`) unless backward-compat was required.
- **Lean diagram**: "Open in Viewer" button in nav bar links correctly. Version nav pill visible bottom-right.
- **arch-viewer.html** at project root: drop-zone visible; file picker works; diagram renders; toolbar functional.
- Quick-edit mode works (via arch-viewer.html).
- Save HTML / Copy HTML / Export PNG controls work in arch-viewer.html.
- Review Annotate works end-to-end in arch-viewer.html:
  - sticky notes (add/move/delete), pointer targets, dotted connectors
  - shape/freehand markup (rectangle/oval/pen), style controls (line style/color/width), mark select/move/delete
- Slide-layout toggle and toolbar show/hide work in arch-viewer.html.
- Output path and version are correct — computed by `next_version_path.py`, never manually guessed.
- Existing version files were not edited in place; all changes went to a new `v(N+1)` file.
- Diagram is presentation-quality for architecture and technical review audiences.
