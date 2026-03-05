# OCI Architecture Diagram Style Guide
## Based on Oracle Redwood Design System v24.1 (January 2024)

---

## COLOR PALETTE (Official OCI Redwood — use these exact values)

```css
:root {
  /* === PRIMARY BRAND COLORS === */
  --ocean:     #2C5967;   /* RGB: 44/89/103  — primary, icons, headings */
  --sienna:    #AE562C;   /* RGB: 174/86/44  — accent, warnings, secondary */

  /* === NEUTRAL SCALE === */
  --air:       #FCFBFA;   /* RGB: 252/251/250 — lightest bg, card interiors */
  --neutral-1: #F5F4F2;   /* RGB: 245/244/242 — page background, region fill */
  --neutral-2: #DFDCD8;   /* RGB: 223/220/216 — VCN fill, input areas */
  --neutral-3: #9E9892;   /* RGB: 158/152/146 — borders, dividers */
  --neutral-4: #70736E;   /* RGB: 112/115/110 — secondary text */
  --bark:      #312D2A;   /* RGB: 49/45/42   — ALL connector lines, body text */

  /* === ACCENT COLORS === */
  --oracle-red: #C74634;  /* RGB: 199/70/52  — errors, Oracle-On-Prem boxes */
  --ivy:        #759C6C;  /* RGB: 117/156/108 — drill-down, success states */
  --rose:       #A36472;  /* RGB: 163/100/114 — 3rd party cloud borders */

  /* === SEMANTIC ALIASES === */
  --page-bg:        var(--neutral-1);   /* #F5F4F2 */
  --card-bg:        #FFFFFF;            /* pure white — cards sit on neutral bg */
  --card-border:    var(--neutral-3);   /* #9E9892 */
  --text-primary:   var(--bark);        /* #312D2A */
  --text-secondary: var(--neutral-4);   /* #70736E */
  --connector:      var(--bark);        /* #312D2A — ALL arrows/lines */
}
```

**Color usage rules:**
- Icons: **Ocean** or **Sienna** only — never multicolor
- Connector lines: **Bark always** — no exceptions
- Page background: **Neutral 1** (off-white) — never pure white
- Cards/boxes: **White (#FFFFFF)** — contrast against Neutral 1 bg
- Primary text: **Bark** — readable dark brown, not black
- Never use colors outside this palette

### OCI Diagram Toolkit Tone (PPT-style reference look)

Use this when the target should resemble Oracle architecture slide samples:

- Keep canvas and lanes mostly in `Neutral 1` / `Neutral 2` / `Air`.
- Use **Sienna** and **Ocean** as restrained accents (labels, strips, left bars), not large saturated fills.
- Prefer subtle brown-gray borders (`Neutral 3`) and very soft warm shadows.
- Keep parent panels slightly darker than foreground cards so card boundaries remain clear.
- Use light elevation (`0 1px 2px` to `0 1px 4px`) for cards; avoid heavy blur/glow.
- For large blocks (orchestrators, KB, grouped zones), use neutral fills with a thin accent edge instead of solid color panels.
- For large database/source nodes, use OCI DB icons (for example `database-system`) with one clear DB name label below by default; avoid dark gradient barrels.
- Use dotted/dashed connectors sparingly for stage-to-stage flow cues where linear progression exists.

---

## TYPOGRAPHY

**Font stack** (in priority order):
```css
font-family: "Oracle Sans", "Segoe UI", Arial, Calibri, sans-serif;
```

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Diagram title | 18–20px | 700 | Bark |
| Section label | 8–9px uppercase, letter-spacing 0.12em | 700 | Neutral 3 / Neutral 4 |
| Grouping label | 9px | 700 | Bark or Sienna (see group type) |
| Service/component title | **13px** | **700** | Ocean or Sienna (match card accent) |
| Service detail text | 9–10px | 400 | Bark |
| Connector label | 8px | 400 | Bark |
| Badge/tag text | 9px | 500 | varies |
| Footer / confidential | 9–10px | 400 | Neutral 3 |

---

## SPACING & SIZING

```css
/* Standard spacing scale */
--space-xs:  4px;
--space-sm:  8px;
--space-md:  12px;
--space-lg:  16px;
--space-xl:  24px;
--space-2xl: 32px;

/* Component sizing */
--icon-sm:   22px;   /* inline icon chips in cards — MINIMUM 22px */
--icon-md:   28px;   /* standalone component icons */
--icon-lg:   36px;   /* hero/header icons */

--card-padding:     10px 12px 10px 15px;
--card-radius:      4px;
--card-accent-bar:  5px;   /* left accent bar width — MINIMUM 5px for visibility */
--card-shadow:      0 1px 4px rgba(49,45,42,0.10), 0 0 0 1px rgba(49,45,42,0.06);
--card-shadow-hover: 0 3px 10px rgba(49,45,42,0.14), 0 0 0 1px rgba(49,45,42,0.10);

--group-padding:   20px 16px 16px;  /* top, sides, bottom */
--group-radius:    4px;
--group-label-offset: -12px 0 0 10px;  /* label positioned top-left of border */

/* Connector sizing */
--connector-weight: 1px;
--connector-dash:   5px 3px;  /* for user-interaction / dashed lines */
```

---

## SHADOW SYSTEM

```css
/* Card shadow — subtle, warm-toned (not cold blue-grey) */
.card-shadow {
  box-shadow: 0 1px 4px rgba(49,45,42,0.10),
              0 0 0 1px rgba(49,45,42,0.06);
}

/* Card shadow on hover */
.card-shadow:hover {
  box-shadow: 0 3px 10px rgba(49,45,42,0.14),
              0 0 0 1px rgba(49,45,42,0.10);
}

/* Grouping box shadow (very light) */
.group-shadow {
  box-shadow: 0 1px 3px rgba(49,45,42,0.06);
}
```

---

## THE REFERENCE CARD COMPONENT

This is the gold standard card component. Every service card should follow this exactly:

```css
.service-card {
  background: #FFFFFF;
  border-radius: 4px;
  border: 1px solid rgba(49,45,42,0.12);
  box-shadow: 0 1px 4px rgba(49,45,42,0.10), 0 0 0 1px rgba(49,45,42,0.06);
  padding: 10px 12px 10px 15px;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 3px;
  transition: box-shadow 0.15s, background 0.15s;
}

.service-card:hover {
  background: #F5F4F2;  /* Neutral 1 on hover */
  box-shadow: 0 3px 10px rgba(49,45,42,0.14), 0 0 0 1px rgba(49,45,42,0.10);
}

/* Left accent bar — 5px minimum width for clear visual identity */
.service-card::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 5px;
  border-radius: 5px 0 0 5px;
  background: var(--accent-color);  /* set per card — must match category */
}

.service-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 2px;
}

.service-card-icon {
  width: 22px;            /* MINIMUM 22px — do not reduce */
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
  /* Use category-matched chip color — see chip table below */
  background: rgba(44,89,103,0.15);
  box-shadow: inset 0 0 0 1px rgba(44,89,103,0.25);
  flex-shrink: 0;
  color: var(--accent-color);
}

/* Font Awesome icon in card */
.service-card-icon.fa-icon {
  font-size: 13px;
  width: 22px;
  text-align: center;
}

/* OCI SVG icon in card */
.service-card-icon img {
  width: 15px;
  height: 15px;
}

.service-card-title {
  font-size: 13px;        /* 13px — do not reduce below 12px */
  font-weight: 700;       /* bold — not 600 */
  color: var(--accent-color);  /* must match card accent category */
  line-height: 1.3;
}

.service-card-items {
  list-style: none;
  padding: 0;
  margin: 0;
}

.service-card-items li {
  font-size: 10px;
  color: #312D2A;  /* Bark */
  line-height: 1.65;
  padding-left: 0;
}
```

**Card color categories — use the FULL palette, not just Ocean:**

> **DEFAULT RULE: Diagrams with 4+ cards MUST use at least 3 distinct accent colours.** Using a single accent colour across all cards is visually monotonous and must be avoided unless the user explicitly requests uniform colouring. Distribute the OCI palette colours semantically so each swimlane/group has a recognisably different colour identity.

| Category | Accent color | `--card-accent` value | Chip class |
|----------|-------------|----------------------|------------|
| Integration / API / Middleware / ESB | Ocean `#2C5967` | `var(--ocean)` | `chip-ocean` |
| Data / Storage / Database / Reference | Sienna `#AE562C` | `var(--sienna)` | `chip-sienna` |
| Security / Compliance / Risk / IAM / Fraud | Oracle Red `#C74634` | `var(--red)` | `chip-red` |
| Compute / Runtime / Processing / Orchestration | Ivy `#759C6C` | `var(--ivy)` | `chip-ivy` |
| Observability / Monitoring / Audit / Reporting / SIEM | Bark `#312D2A` | `var(--bark)` | `chip-bark` |
| Analytics / AI / ML / Intelligent services | Ocean `#2C5967` | `var(--ocean)` | `chip-ocean` |
| Human-facing / Channels / Portal / Branch | Sienna `#AE562C` | `var(--sienna)` | `chip-sienna` |
| External systems / 3rd-party / Payment rails | Bark `#312D2A` | `var(--bark)` | `chip-bark` |
| Notifications / Events / Messaging | Sienna `#AE562C` | `var(--sienna)` | `chip-sienna` |
| Network / Connectivity / Switch / Gateway | Ivy `#759C6C` | `var(--ivy)` | `chip-ivy` |

**HTML usage:** Set `style="--card-accent: var(--ocean)"` (or `--sienna`, `--red`, `--ivy`, `--bark`) directly on each `<article class="service-card">` element. The accent bar, icon chip colour, and card title colour all inherit from `--card-accent` automatically.

**MANDATORY: Icon chip must always use the category-matched chip class. Never use ocean chip for sienna/red/ivy cards.**

**MANDATORY: Vary accent colours across card groups. A diagram where all cards share one accent colour is a quality failure.**

```css
/* Category-matched icon chip CSS — include in EVERY diagram's <style> block */
.chip-ocean  { background: rgba(44,89,103,0.15);   box-shadow: inset 0 0 0 1px rgba(44,89,103,0.25);   color: #2C5967; }
.chip-sienna { background: rgba(174,86,44,0.13);   box-shadow: inset 0 0 0 1px rgba(174,86,44,0.22);   color: #AE562C; }
.chip-red    { background: rgba(199,70,52,0.12);   box-shadow: inset 0 0 0 1px rgba(199,70,52,0.20);   color: #C74634; }
.chip-ivy    { background: rgba(117,156,108,0.13); box-shadow: inset 0 0 0 1px rgba(117,156,108,0.22); color: #759C6C; }
.chip-bark   { background: rgba(49,45,42,0.10);    box-shadow: inset 0 0 0 1px rgba(49,45,42,0.18);    color: #312D2A; }
```

Apply like: `<div class="card-icon chip-sienna"><i class="fa-solid fa-database"></i></div>`

---

## EXTENDED VIVID PALETTE (accent variety)

When the standard OCI palette feels too muted (dark ocean, brown sienna, near-black bark), use these vivid variants for a more colourful, energetic diagram. All values are derived from OCI extended brand colours — still on-brand, but more saturated.

```css
:root {
  /* === EXTENDED VIVID ACCENTS === */
  --vivid-teal:   #0F8799;  /* Bright OCI teal — channel/connectivity cards */
  --vivid-orange: #E06520;  /* Warm vibrant orange — data/messaging/events */
  --vivid-cobalt: #1E5DAB;  /* Deep cobalt blue — integration/API */
  --vivid-forest: #2E8C46;  /* Rich forest green — compute/runtime */
  --vivid-grape:  #7B4FA0;  /* Purple — analytics/AI/ML */
}
```

**Vivid chip CSS classes** (add alongside the 5 standard chip classes):

```css
.chip-vivid-teal   { background: rgba(15,135,153,0.13); box-shadow: inset 0 0 0 1px rgba(15,135,153,0.25); color: #0F8799; }
.chip-vivid-orange { background: rgba(224,101,32,0.13); box-shadow: inset 0 0 0 1px rgba(224,101,32,0.25); color: #E06520; }
.chip-vivid-cobalt { background: rgba(30,93,171,0.13);  box-shadow: inset 0 0 0 1px rgba(30,93,171,0.25);  color: #1E5DAB; }
.chip-vivid-forest { background: rgba(46,140,70,0.13);  box-shadow: inset 0 0 0 1px rgba(46,140,70,0.25);  color: #2E8C46; }
.chip-vivid-grape  { background: rgba(123,79,160,0.13); box-shadow: inset 0 0 0 1px rgba(123,79,160,0.25); color: #7B4FA0; }
```

**When to use vivid palette:**
- Default diagrams with many cards (6+) — adds visual energy and makes each swimlane distinct.
- When the user says the diagram looks "too grey" or "too muted".
- When the reference design or user's colour preference calls for more vibrant/colourful accents.

**Category mapping (vivid variant):**

| Category | Vivid accent | CSS value | Chip class |
|----------|-------------|-----------|------------|
| Channels / Portal / Branch | Vivid Teal | `var(--vivid-teal)` | `chip-vivid-teal` |
| Data / Storage / Events | Vivid Orange | `var(--vivid-orange)` | `chip-vivid-orange` |
| Integration / API / ESB | Vivid Cobalt | `var(--vivid-cobalt)` | `chip-vivid-cobalt` |
| Compute / Runtime / Orchestration | Vivid Forest | `var(--vivid-forest)` | `chip-vivid-forest` |
| Analytics / AI / ML | Vivid Grape | `var(--vivid-grape)` | `chip-vivid-grape` |
| Security / IAM / Fraud | Oracle Red | `var(--oracle-red)` | `chip-red` |
| Observability / Monitoring | Bark | `var(--bark)` | `chip-bark` |
| External / 3rd-party | Sienna | `var(--sienna)` | `chip-sienna` |

**HTML usage:** Set `style="--card-accent: var(--vivid-teal)"` (or other vivid var) on each card the same way as standard palette.

---

## GROUPING BOX SPECIFICATION

From OCI official spec:

```css
/* Location Group (OCI Region, Cloud) */
.group-location {
  border: 1px solid #9E9892;  /* Neutral 3 */
  background: #F5F4F2;         /* Neutral 1 */
  border-radius: 4px;
  padding: 24px 14px 14px;
  position: relative;
}
.group-location > .group-label {
  position: absolute;
  top: -1px; left: 10px;
  font-size: 9px; font-weight: 700; color: #312D2A;
  background: #F5F4F2;
  padding: 0 4px;
}

/* VCN Group */
.group-vcn {
  border: 1px solid #9E9892;
  background: #DFDCD8;  /* Neutral 2 */
  border-radius: 4px;
  padding: 24px 14px 14px;
}

/* Availability Domain */
.group-ad {
  border: 1px solid #9E9892;
  background: #FCFBFA;  /* Air */
  border-radius: 4px;
  padding: 24px 14px 14px;
}

/* Compartment */
.group-compartment {
  border: 1px dashed #AE562C;  /* Sienna dashed */
  background: transparent;
  border-radius: 4px;
  padding: 24px 14px 14px;
}
.group-compartment > .group-label {
  color: #AE562C;  /* Sienna */
  font-weight: 700;
}

/* Other / Logical Group */
.group-logical {
  border: 1px dashed #312D2A;  /* Bark dashed */
  background: transparent;
  border-radius: 4px;
  padding: 24px 14px 14px;
}

/* On-Premises */
.group-onprem {
  border: 1px solid #9E9892;
  background: #DFDCD8;
  border-radius: 4px;
}

/* 3rd Party Cloud */
.group-3rdparty {
  border: 1px dashed #A36472;  /* Rose dashed */
  background: transparent;
  border-radius: 4px;
}
.group-3rdparty > .group-label {
  color: #A36472;  /* Rose */
}
```

---

## PAGE LAYOUT SHELL

```css
/* === FIXED PAGE STRUCTURE === */

body {
  margin: 0;
  padding: 0;
  background: #F5F4F2;  /* Neutral 1 — ALWAYS off-white, never pure white */
  font-family: "Oracle Sans", "Segoe UI", Arial, Calibri, sans-serif;
  color: #312D2A;  /* Bark */
  font-size: 12px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* OCI Top Navigation Bar */
.oci-nav {
  height: 44px;
  background: #142830;  /* extra dark ocean — matches OCI console exactly */
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 14px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.oci-logo {
  height: 18px;
  filter: brightness(0) invert(1);
}

.oci-nav-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-btn {
  border: 1px solid rgba(255,255,255,0.24);
  background: rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.95);
  border-radius: 5px;
  font-size: 11px;
  padding: 4px 8px;
  cursor: pointer;
}

.nav-btn:hover { background: rgba(255,255,255,0.16); }

.nav-btn.active {
  border-color: rgba(255,255,255,0.52);
  background: rgba(255,255,255,0.22);
}

/* Diagram Header */
.diagram-header {
  padding: 16px 24px 10px;
  background: #F5F4F2;
  border-bottom: 1px solid #DFDCD8;
}

.diagram-title {
  font-size: 20px;
  font-weight: 700;
  color: #312D2A;
  margin: 0 0 3px;
  line-height: 1.2;
}

.diagram-sub {
  font-size: 10.5px;
  color: #70736E;
  margin: 0 0 8px;
}

/* Badge row */
.badge-row {
  display: flex;
  gap: 7px;
  flex-wrap: wrap;
}

.badge {
  font-size: 9.5px;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: 10px;
  display: inline-block;
}

.badge-ocean { background: #EDF4F7; color: #2C5967; border: 1px solid #b8d0d8; }
.badge-sienna { background: #FDF5F1; color: #AE562C; border: 1px solid #e8c4a8; }
.badge-green  { background: #EDF4EB; color: #4a6944; border: 1px solid #c4d8c0; }
.badge-red    { background: #FBF0EE; color: #C74634; border: 1px solid #f0c4bb; }
.badge-neutral { background: #F5F4F2; color: #70736E; border: 1px solid #DFDCD8; }

/* Main canvas */
.diagram-canvas {
  padding: 20px 24px;
  min-height: calc(100vh - 44px - 100px - 36px);
}

/* Slide-mode framing (fit first, scroll fallback) */
.slide-viewport { min-height: 100vh; }
.slide-frame { width: 100%; }
.diagram-shell { min-height: 100vh; }

body.slide-layout { overflow: hidden; }
body.slide-layout .slide-viewport {
  min-height: 100vh;
  height: 100vh;
  padding: 8px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  overflow: hidden;
}
body.slide-layout.slide-scroll .slide-viewport { overflow: auto; }
body.slide-layout .slide-frame {
  flex: 0 0 auto;
  position: relative;
}
body.slide-layout .diagram-shell {
  width: 1366px;
  min-height: 768px;
  margin: 0;
  background: #F5F4F2;
  box-shadow: 0 0 0 1px rgba(49,45,42,0.12);
  transform-origin: top left;
}
body.slide-layout .diagram-canvas { min-height: calc(768px - 44px - 100px - 36px); }
body.toolbar-hidden .edit-toolbar { display: none; }

/* Review annotation overlay */
.review-layer {
  position: absolute;
  inset: 0;
  z-index: 20;
  pointer-events: none;
}
.review-connectors {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.review-markup {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.review-note {
  position: absolute;
  width: 230px;
  min-height: 94px;
  background: rgba(255,245,176,0.88); /* translucent sticky-note style */
  border: 1px solid rgba(157,123,42,0.58);
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(49,45,42,0.16);
}
.review-anchor {
  position: absolute;
  width: 12px;
  height: 12px;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  border: 1.5px solid #AE562C;
  background: rgba(174,86,44,0.20);
}
.review-mark {
  fill: none;
  stroke: #C74634;
  stroke-width: 3;
  vector-effect: non-scaling-stroke;
  stroke-linecap: round;
  stroke-linejoin: round;
  pointer-events: visiblePainted;
}
/* Keep review controls hidden until review mode is active */
.review-tools { display: none; }
body.review-annotate-mode .review-tools { display: flex; }
body.review-annotate-mode .review-layer { pointer-events: auto; cursor: crosshair; }
body.review-annotate-mode .review-markup { pointer-events: auto; }

/* Footer / Legend bar */
.diagram-footer {
  padding: 8px 24px;
  background: #FFFFFF;
  border-top: 1px solid #DFDCD8;
  display: flex;
  align-items: center;
  gap: 20px;
  min-height: 36px;
}

.legend {
  display: flex;
  align-items: center;
  gap: 18px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 9.5px;
  color: #70736E;
}

.legend-dot {
  width: 9px;
  height: 9px;
  border-radius: 2px;
  flex-shrink: 0;
}

.diagram-confidential {
  margin-left: auto;
  font-size: 9.5px;
  color: #9E9892;
  font-style: italic;
}

/* Section label (above a group of cards) */
.section-label {
  font-size: 8.5px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #9E9892;
  margin-bottom: 8px;
}
```

Slide behavior guidance:
- Default/full layout should render the complete structure naturally (no clipping).
- `slide-layout` should try to fit the entire diagram into a 16:9 frame for screenshot use.
- If fit scale would drop too low (about `68%` or lower), stop scaling and enable scroll instead.

---

## CONNECTOR SVG TEMPLATE

```html
<!-- Inline SVG connector layer — position: absolute, full diagram width/height -->
<svg class="connectors" xmlns="http://www.w3.org/2000/svg"
     style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:visible">
  <defs>
    <!-- Primary data flow arrowhead (Ocean — main architectural flow) -->
    <marker id="arrowhead-ocean" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto">
      <path d="M1,1 L9,5 L1,9" fill="none" stroke="#2C5967" stroke-width="1.5"
            stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <!-- Secondary / internal arrowhead (Bark) -->
    <marker id="arrowhead" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto">
      <path d="M1,1 L9,5 L1,9" fill="none" stroke="#312D2A" stroke-width="1.5"
            stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <!-- Optional / user-interaction arrowhead (Neutral 4 dashed) -->
    <marker id="arrowhead-dash" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto">
      <path d="M1,1 L9,5 L1,9" fill="none" stroke="#70736E" stroke-width="1.5"
            stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>

  <!-- PRIMARY data flow connector — Ocean color, 1.5px, use for main architectural flows -->
  <line x1="X1" y1="Y1" x2="X2" y2="Y2"
        stroke="#2C5967" stroke-width="1.5"
        marker-end="url(#arrowhead-ocean)"/>

  <!-- SECONDARY / internal connector — Bark color, 1px -->
  <line x1="X1" y1="Y1" x2="X2" y2="Y2"
        stroke="#312D2A" stroke-width="1"
        marker-end="url(#arrowhead)"/>

  <!-- OPTIONAL / user-interaction connector — dashed Neutral 4 -->
  <line x1="X1" y1="Y1" x2="X2" y2="Y2"
        stroke="#70736E" stroke-width="1"
        stroke-dasharray="5,3"
        marker-end="url(#arrowhead-dash)"/>

  <!-- Connector with label -->
  <line x1="X1" y1="Y1" x2="X2" y2="Y2" stroke="#2C5967" stroke-width="1.5"
        marker-end="url(#arrowhead-ocean)"/>
  <rect x="MX-20" y="MY-8" width="40" height="16" fill="#F5F4F2" rx="2"/>
  <text x="MX" y="MY+5" text-anchor="middle"
        font-family="Arial,sans-serif" font-size="8" fill="#312D2A">label</text>
</svg>

**Connector color rules:**
- **Ocean (#2C5967), 1.5px**: Primary architectural/data flows — e.g. API call chains, main pipeline steps
- **Bark (#312D2A), 1px**: Internal/sub-component flows, shorter hops within a panel
- **Neutral 4 dashed (#70736E)**: Optional, async, or user-triggered interactions
```

---

## ICON REFERENCE TABLE

Available OCI SVG icons (from `skill/assets/icons/oci_icons.json`):

| Key | Service |
|-----|---------|
| `oracle-logo` | Oracle logo (nav bar) |
| `user` | User / person |
| `api-gateway` | API Gateway / network |
| `enterprise-building` | Enterprise / building |
| `database` | Database / storage |
| `database-system` | Oracle Database System (drawio-derived OCI icon) |
| `object-storage` | Object Storage / cloud store |
| `compute` | Compute instance |
| `container` | Container |
| `load-balancer` | Load Balancer / platform |
| `kubernetes` | Kubernetes / OKE |
| `functions` | OCI Functions / serverless |
| `integration` | Integration / workflow |
| `devops` | DevOps |
| `monitoring` | Monitoring / analytics globe |
| `logging` | Logging / document |
| `analytics` | Analytics |
| `generative-ai` | OCI Generative AI |
| `people-group` | People / team / human loop |
| `streaming` | Streaming |
| `security-shield` | Security / shield |
| `cloud-service` | Cloud service (generic) |
| `vault-key` | Vault / key management |

**FA fallbacks for common needs:**

| Need | FA class |
|------|----------|
| Orchestrator / agent | `fa-solid fa-sitemap` |
| LLM / AI brain | `fa-solid fa-brain` |
| Message queue | `fa-solid fa-envelope-open-text` |
| Cache / Redis | `fa-solid fa-bolt` |
| Search / RAG | `fa-solid fa-magnifying-glass` |
| Rules / compliance | `fa-solid fa-scale-balanced` |
| Report / audit | `fa-solid fa-file-lines` |
| Approval / HITL | `fa-solid fa-user-check` |
| Scheduler | `fa-solid fa-clock` |
| Event / webhook | `fa-solid fa-webhook` |
| Config / settings | `fa-solid fa-sliders` |
| Network / mesh | `fa-solid fa-network-wired` |
| ML model | `fa-solid fa-microchip` |
| Vector / embeddings | `fa-solid fa-vector-square` |

---

## VISUAL RICHNESS REQUIREMENTS (MANDATORY)

These rules close the gap between a flat diagram and a polished, professional architecture visual. Apply every rule on every diagram. No exceptions.

### 1. Icon Chips — Size & Color
- **Minimum chip size: 22×22px.** Never use 18px or smaller.
- **Always match chip color to card accent category** using the `chip-*` classes defined above.
  - Ocean card → `.chip-ocean` (blue-teal tint)
  - Sienna card → `.chip-sienna` (warm orange tint)
  - Oracle Red card → `.chip-red` (red tint)
  - Ivy card → `.chip-ivy` (green tint)
  - Bark card → `.chip-bark` (neutral dark tint)
- **Never use the same chip background for all categories.** Visual differentiation at the chip level is required.

### 2. Card Titles
- **13px, font-weight 700.** Bold card titles make the diagram scannable at a glance.
- Title color must exactly match the card accent color (ocean/sienna/red/ivy/bark).

### 3. Left Accent Bar — Colour Variety
- **5px width minimum.** The left bar is the primary category signal; do not reduce it.
- Must use the card's accent color — not a generic dark or gray.
- **Vary the accent colour across swimlanes/groups.** By default use the full OCI palette so each section has a distinct colour identity. Override only if the user explicitly requests a specific uniform colour.
- Aim for at least 3 different accent colours visible across any diagram with 6+ cards.
- Example colour distribution in a multi-zone diagram: channels → Sienna, integration hub → Ocean, security → Red, observability → Bark, compute → Ivy.

### 4. Connector Color Variation
- **Use Ocean-colored connectors (1.5px) for primary architectural flows** between major components or zones. This creates a strong visual narrative.
- Use Bark (1px) for internal or secondary hops within a panel.
- Use dashed Neutral 4 for optional or async paths.
- Do NOT make all connectors bark/gray — flat connector color flattens the diagram.

### 5. Panel / Group Background Contrast
- Keep parent panel backgrounds one shade darker than inner card backgrounds.
  - Outer zone: `Neutral 1 (#F5F4F2)` or `Neutral 2 (#DFDCD8)`
  - Inner cards: white (`#FFFFFF`)
- For panels with a strong category identity (e.g. left sidebar = "DE Channels"), a subtle warm tint is acceptable: `rgba(49,45,42,0.04)` over white panels.

### 6. Section Labels
- Section labels above card groups must be uppercase, 8.5px, letter-spacing 0.12em, `Neutral 3` color.
- For **swimlane headers** (full-width row headers), use a slightly darker background strip:
  ```css
  .swimlane-label {
    background: #E8E4DF;
    padding: 7px 14px;
    font-size: 9.5px; font-weight: 700; letter-spacing: 0.10em;
    text-transform: uppercase; color: #312D2A;
    border-bottom: 2px solid #C8C3BC;
  }
  ```

### 7. Gateway / Header Bars
- Full-width header bars (e.g. API Gateway) must use the dark Ocean: `#1e3d47` or `#142830`.
- Text: white title 12px/700, secondary text `rgba(255,255,255,0.55)`.
- Tags: monospace, `rgba(255,255,255,0.08)` background, `rgba(255,255,255,0.18)` border.

### 8. What NOT to do
- Do NOT use 18px icon chips (too small, gets lost in card).
- Do NOT use font-weight 500 or 600 for card titles (too light).
- Do NOT use bark/gray for all connectors (creates flat, undifferentiated look).
- Do NOT use same `rgba(44,89,103,0.12)` chip for all categories (ignores category identity).
- Do NOT use 3px or 4px accent bars (too thin to register at small sizes).
