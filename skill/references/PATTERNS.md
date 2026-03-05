# Architecture Diagram Layout Patterns
## Reusable patterns for OCI architecture diagrams

Claude: pick ONE pattern as the primary structure, then compose components within it.

---

## BASE CSS (include in EVERY diagram)

```css
/* Include this in every diagram's <style> block */

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: #F5F4F2;
  font-family: "Oracle Sans", "Segoe UI", Arial, Calibri, sans-serif;
  color: #312D2A;
  font-size: 12px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* Shared shell */
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

/* OCI Nav */
.oci-nav {
  height: 44px; background: #142830;
  display: flex; align-items: center; padding: 0 20px; gap: 14px;
  position: sticky; top: 0; z-index: 100;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.oci-logo {
  height: 18px;
  filter: brightness(0) invert(1);
}
.oci-nav-right { margin-left: auto; display: flex; align-items: center; gap: 8px; }
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

/* Diagram header */
.diagram-header { padding: 16px 24px 10px; border-bottom: 1px solid #DFDCD8; }
.diagram-title { font-size: 20px; font-weight: 700; color: #312D2A; margin: 0 0 3px; }
.diagram-sub { font-size: 10.5px; color: #70736E; margin: 0 0 8px; }
.badge-row { display: flex; gap: 7px; flex-wrap: wrap; }
.badge { font-size: 9.5px; font-weight: 500; padding: 2px 10px; border-radius: 10px; }
.badge-ocean  { background: #EDF4F7; color: #2C5967; border: 1px solid #b8d0d8; }
.badge-sienna { background: #FDF5F1; color: #AE562C; border: 1px solid #e8c4a8; }
.badge-green  { background: #EDF4EB; color: #4a6944; border: 1px solid #c4d8c0; }
.badge-red    { background: #FBF0EE; color: #C74634; border: 1px solid #f0c4bb; }

/* Canvas */
.diagram-canvas { padding: 20px 24px; min-height: calc(100vh - 44px - 100px - 36px); }
body.slide-layout .diagram-canvas { min-height: calc(768px - 44px - 100px - 36px); }

/* Toolbar visibility hook (top-bar toggle controls this class) */
body.toolbar-hidden .edit-toolbar { display: none; }

/* Review annotation mode (sticky notes + drawable shapes/freehand) */
.review-layer { position: absolute; inset: 0; z-index: 20; pointer-events: none; }
.review-connectors { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.review-markup { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.review-note { position: absolute; width: 230px; min-height: 94px; pointer-events: auto; }
.review-anchor { position: absolute; width: 12px; height: 12px; transform: translate(-50%, -50%); pointer-events: auto; }
.review-mark { fill: none; stroke: #C74634; stroke-width: 3; pointer-events: visiblePainted; }
.review-tools { display: none; } /* hidden unless review mode is active */
body.review-annotate-mode .review-tools { display: flex; }
body.review-annotate-mode .review-layer { pointer-events: auto; cursor: crosshair; }
body.review-annotate-mode .review-markup { pointer-events: auto; }

/* Section label */
.section-label {
  font-size: 8.5px; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: #9E9892; margin-bottom: 8px;
  display: block;
}

/* === SERVICE CARD === */
.service-card {
  background: #FFFFFF;
  border-radius: 4px;
  border: 1px solid rgba(49,45,42,0.12);
  box-shadow: 0 1px 4px rgba(49,45,42,0.10), 0 0 0 1px rgba(49,45,42,0.06);
  padding: 10px 12px 10px 16px;
  position: relative;
  transition: box-shadow 0.15s, background 0.15s;
}
.service-card:hover {
  background: #F5F4F2;
  box-shadow: 0 3px 10px rgba(49,45,42,0.14), 0 0 0 1px rgba(49,45,42,0.10);
}
.service-card::before {
  content: ''; position: absolute;
  left: 0; top: 0; bottom: 0; width: 5px; /* 5px — do not reduce */
  border-radius: 5px 0 0 5px;
  background: var(--card-accent, #2C5967);
}
.card-header { display: flex; align-items: center; gap: 9px; margin-bottom: 4px; }
.card-icon {
  width: 22px;            /* 22px minimum — do not use 18px */
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
  /* Default chip — override with chip-* class for correct category color */
  background: rgba(44,89,103,0.15);
  box-shadow: inset 0 0 0 1px rgba(44,89,103,0.25);
  flex-shrink: 0;
  color: var(--card-accent, #2C5967);
  font-size: 13px;
}
.card-icon img { width: 15px; height: 15px; }
.card-title { font-size: 13px; font-weight: 700; color: var(--card-accent, #2C5967); line-height: 1.3; }
.card-items { list-style: none; }
.card-items li { font-size: 10px; color: #312D2A; line-height: 1.65; }

/* === CATEGORY-MATCHED ICON CHIP VARIANTS ===
   MANDATORY: Apply chip-* class to .card-icon to match card accent category.
   Never use the same chip color across all categories. */
.chip-ocean  { background: rgba(44,89,103,0.15);   box-shadow: inset 0 0 0 1px rgba(44,89,103,0.25);   color: #2C5967; }
.chip-sienna { background: rgba(174,86,44,0.13);   box-shadow: inset 0 0 0 1px rgba(174,86,44,0.22);   color: #AE562C; }
.chip-red    { background: rgba(199,70,52,0.12);   box-shadow: inset 0 0 0 1px rgba(199,70,52,0.20);   color: #C74634; }
.chip-ivy    { background: rgba(117,156,108,0.13); box-shadow: inset 0 0 0 1px rgba(117,156,108,0.22); color: #759C6C; }
.chip-bark   { background: rgba(49,45,42,0.10);    box-shadow: inset 0 0 0 1px rgba(49,45,42,0.18);    color: #312D2A; }
/* Usage: <div class="card-icon chip-sienna"><i class="fa-solid fa-database"></i></div> */

/* === GROUPING BOXES === */
.group-box {
  border-radius: 4px; padding: 28px 14px 14px; position: relative;
}
.group-box > .group-label {
  position: absolute; top: 8px; left: 12px;
  font-size: 9px; font-weight: 700; color: #312D2A;
  letter-spacing: 0.05em;
}
.group-location { border: 1px solid #9E9892; background: #F5F4F2; }
.group-vcn      { border: 1px solid #9E9892; background: #DFDCD8; }
.group-ad       { border: 1px solid #9E9892; background: #FCFBFA; }
.group-compartment { border: 1px dashed #AE562C; background: transparent; }
.group-compartment > .group-label { color: #AE562C; }
.group-logical  { border: 1px dashed #312D2A; background: transparent; }
.group-onprem   { border: 1px solid #9E9892; background: #DFDCD8; }
.group-3rdparty { border: 1px dashed #A36472; background: transparent; }
.group-3rdparty > .group-label { color: #A36472; }

/* Footer */
.diagram-footer {
  padding: 8px 24px; background: #FFFFFF;
  border-top: 1px solid #DFDCD8;
  display: flex; align-items: center; gap: 20px; min-height: 36px;
}
.legend { display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
.legend-item { display: flex; align-items: center; gap: 5px; font-size: 9.5px; color: #70736E; }
.legend-dot { width: 9px; height: 9px; border-radius: 2px; flex-shrink: 0; }
.diagram-confidential { margin-left: auto; font-size: 9.5px; color: #9E9892; font-style: italic; }

/* SVG connectors */
.connector-layer {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none; overflow: visible;
}
```

Slide-view behavior:
- Keep default/full layout unscaled with full structure visible.
- In `slide-layout`, calculate a fit scale for a 16:9 frame and apply it when still legible.
- If the needed scale drops too low (around `68%` or less), switch to `slide-scroll` and allow scrolling.

---

## PATTERN 1: SIDE-PANEL (Agent / Service with Tool Sets)

**Use when:** Central service/agent with left inputs, right tools, or top channels.
This is the pattern used for the banking agent diagram.

```
┌─────────┬───────────────────────────┬──────────────┐
│  LEFT   │       CENTER CANVAS       │    RIGHT     │
│ (inputs │   [gateway] [platform]    │  (tools /    │
│  /side  │   isometric or flat       │   services)  │
│ channels│                           │              │
└─────────┴───────────────────────────┴──────────────┘
```

```html
<!-- PATTERN 1: THREE-COLUMN LAYOUT -->
<div class="layout-side-panel">

  <!-- LEFT: inputs/channels/side-channels -->
  <aside class="panel-left">
    <span class="section-label">Side Channels</span>
    <!-- .service-card items -->
  </aside>

  <!-- CENTER: main architecture -->
  <main class="panel-center">
    <!-- gateway bar, platform, etc. -->
  </main>

  <!-- RIGHT: tools/services -->
  <aside class="panel-right">
    <span class="section-label">Tools &amp; Services</span>
    <!-- .service-card items -->
  </aside>

</div>

<style>
.layout-side-panel {
  display: grid;
  grid-template-columns: 200px 1fr 280px;
  gap: 0;
  min-height: calc(100vh - 44px - 80px - 36px);
}
.panel-left, .panel-right {
  background: #FFFFFF;
  padding: 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.panel-left  { border-right: 1px solid #DFDCD8; }
.panel-right { border-left:  1px solid #DFDCD8; }
.panel-center {
  background: #F5F4F2;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
```

---

## PATTERN 2: HORIZONTAL PIPELINE

**Use when:** Sequential flow — ingestion → processing → output, or request/response chain.

```
[Stage 1] ──▶ [Stage 2] ──▶ [Stage 3] ──▶ [Stage 4]
   │               │               │               │
[sub]          [sub]           [sub]           [sub]
```

```html
<!-- PATTERN 2: PIPELINE FLOW -->
<div class="layout-pipeline">

  <div class="pipeline-stages">

    <div class="pipeline-stage">
      <div class="stage-header">
        <span class="stage-number">1</span>
        <span class="stage-title">Ingestion</span>
      </div>
      <div class="stage-body">
        <!-- service cards -->
      </div>
    </div>

    <div class="pipeline-arrow">
      <svg width="40" height="40" viewBox="0 0 40 40">
        <line x1="5" y1="20" x2="30" y2="20" stroke="#312D2A" stroke-width="1"
              marker-end="url(#arrowhead)"/>
      </svg>
    </div>

    <div class="pipeline-stage"><!-- stage 2 --></div>
    <!-- repeat for each stage -->

  </div>

</div>

<style>
.layout-pipeline { padding: 20px 24px; }
.pipeline-stages {
  display: flex;
  align-items: flex-start;
  gap: 0;
  overflow-x: auto;
  padding-bottom: 16px;
}
.pipeline-stage {
  flex: 1;
  min-width: 160px;
  max-width: 220px;
}
.pipeline-arrow {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  padding-top: 24px;
}
.stage-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 2px solid #2C5967;
}
.stage-number {
  width: 20px; height: 20px;
  background: #2C5967; color: white;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 700;
  flex-shrink: 0;
}
.stage-title {
  font-size: 11px; font-weight: 700; color: #2C5967;
}
.stage-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>
```

---

## PATTERN 3: LAYERED / SWIMLANE

**Use when:** Multiple tiers — Presentation / Application / Data, or network layers.

```
┌─────────────────────────────────────────┐
│  Presentation Layer                     │
│  [Web App]  [Mobile]  [API]             │
├─────────────────────────────────────────┤
│  Application Layer                      │
│  [Service A]  [Service B]  [Service C]  │
├─────────────────────────────────────────┤
│  Data Layer                             │
│  [DB]  [Cache]  [Object Storage]        │
└─────────────────────────────────────────┘
```

```html
<!-- PATTERN 3: SWIMLANES -->
<div class="layout-swimlanes">

  <div class="swimlane">
    <div class="swimlane-label">Presentation Layer</div>
    <div class="swimlane-content">
      <!-- service cards in a row -->
      <div class="cards-row">
        <!-- .service-card items -->
      </div>
    </div>
  </div>

  <div class="swimlane-connector">
    <!-- SVG arrows between lanes -->
  </div>

  <div class="swimlane">
    <div class="swimlane-label">Application Layer</div>
    <div class="swimlane-content">
      <div class="cards-row"><!-- cards --></div>
    </div>
  </div>

</div>

<style>
.layout-swimlanes {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.swimlane {
  border: 1px solid #9E9892;
  border-radius: 4px;
  background: #F5F4F2;
  overflow: hidden;
}
.swimlane-label {
  background: #E8E4DF;              /* slightly darker than DFDCD8 for clear separation */
  padding: 7px 14px;
  font-size: 9.5px; font-weight: 700; letter-spacing: 0.10em;
  text-transform: uppercase; color: #312D2A;
  border-bottom: 2px solid #C8C3BC;  /* 2px border for definition */
}
.swimlane-content { padding: 14px; }
.cards-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.swimlane-connector {
  display: flex;
  justify-content: center;
  height: 24px;
  align-items: center;
}
</style>
```

---

## PATTERN 4: OCI PHYSICAL (Region / VCN / Subnets)

**Use when:** Network topology, VCN design, subnet architecture, physical OCI diagram.

```html
<!-- PATTERN 4: OCI PHYSICAL TOPOLOGY -->
<div class="layout-physical">

  <!-- On-Premises / Internet -->
  <div class="group-box group-onprem" style="margin-bottom: 12px">
    <span class="group-label">On-Premises</span>
    <div class="cards-row"><!-- CPE, servers --></div>
  </div>

  <!-- OCI Region -->
  <div class="group-box group-location">
    <span class="group-label">OCI Region — ap-singapore-1</span>

    <!-- VCN -->
    <div class="group-box group-vcn" style="margin-top: 8px">
      <span class="group-label">VCN 10.0.0.0/16</span>

      <!-- Availability Domain -->
      <div class="group-box group-ad" style="margin-top: 8px">
        <span class="group-label">Availability Domain 1</span>

        <div class="subnets-row">
          <!-- Public Subnet -->
          <div class="group-box group-ad" style="flex:1">
            <span class="group-label">Public Subnet 10.0.1.0/24</span>
            <div class="cards-col"><!-- Load Balancer --></div>
          </div>
          <!-- Private Subnet -->
          <div class="group-box group-ad" style="flex:2">
            <span class="group-label">Private Subnet 10.0.2.0/24</span>
            <div class="cards-row"><!-- App servers --></div>
          </div>
        </div>
      </div>
    </div>

    <!-- OCI Services (outside VCN) -->
    <div class="oci-services-strip">
      <!-- Object Storage, IAM, etc. -->
    </div>
  </div>

</div>

<style>
.layout-physical { padding: 20px 24px; }
.subnets-row { display: flex; gap: 8px; margin-top: 8px; }
.cards-col { display: flex; flex-direction: column; gap: 6px; }
.oci-services-strip {
  margin-top: 10px;
  padding: 10px;
  border: 1px dashed #9E9892;
  border-radius: 4px;
  background: transparent;
  display: flex; gap: 8px; flex-wrap: wrap;
}
</style>
```

---

## PATTERN 5: MULTI-ENVIRONMENT (Location Canvas)

**Use when:** OCI + On-Premises + Internet + 3rd Party Cloud in one diagram.

```html
<!-- PATTERN 5: MULTI-ENVIRONMENT / LOCATION CANVAS -->
<div class="layout-location-canvas">

  <div class="location-row">
    <!-- Internet zone -->
    <div class="group-box group-logical" style="flex:1">
      <span class="group-label">Internet</span>
      <!-- Users, CDN -->
    </div>

    <!-- On-Premises -->
    <div class="group-box group-onprem" style="flex:2">
      <span class="group-label">On-Premises</span>
      <!-- Legacy systems, CPE -->
    </div>

    <!-- 3rd Party Cloud -->
    <div class="group-box group-3rdparty" style="flex:1">
      <span class="group-label">3rd Party Cloud</span>
    </div>
  </div>

  <!-- Connectivity band (VPN / FastConnect) -->
  <div class="connectivity-band">
    <!-- SVG connectors: DRG, VPN, FastConnect -->
  </div>

  <!-- OCI Region -->
  <div class="group-box group-location">
    <span class="group-label">OCI Region — ap-singapore-1</span>
    <!-- inner content -->
  </div>

</div>

<style>
.layout-location-canvas { padding: 20px 24px; display: flex; flex-direction: column; gap: 12px; }
.location-row { display: flex; gap: 12px; }
.connectivity-band {
  height: 40px; position: relative;
  border-top: 1px dashed #9E9892; border-bottom: 1px dashed #9E9892;
  background: #FCFBFA;
  display: flex; align-items: center; padding: 0 20px;
}
</style>
```

---

## PATTERN 6: GATEWAY BAR (reusable component for all patterns)

Use for API Gateway / security boundary — spans full width of center zone.

```html
<div class="gateway-bar">
  <img class="gateway-icon" src="[load-balancer-icon-uri]" alt="API Gateway">
  <div class="gateway-text">
    <div class="gateway-title">API Gateway &amp; Auth / Authz</div>
    <div class="gateway-sub">Security boundary — all requests authenticated &amp; authorized before reaching services</div>
  </div>
  <div class="gateway-tags">
    <span class="gw-tag">RBAC / ABAC</span>
    <span class="gw-tag">Rate Limits</span>
    <span class="gw-tag">Auth + Context</span>
  </div>
</div>

<style>
.gateway-bar {
  background: #1e3d47;
  border: 1.5px solid #2C5967;
  border-radius: 4px;
  padding: 9px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.14);
}
.gateway-icon { width: 26px; height: 26px; }
.gateway-text { flex: 1; }
.gateway-title { font-size: 12px; font-weight: 700; color: #FFFFFF; }
.gateway-sub { font-size: 9px; color: rgba(255,255,255,0.50); margin-top: 2px; }
.gateway-tags { display: flex; gap: 5px; flex-wrap: wrap; }
.gw-tag {
  font-size: 8.5px; color: #9BBCC8; font-family: monospace;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.18);
  padding: 2px 7px; border-radius: 3px;
}
</style>
```

---

## COMPONENT ICON BLOCK (standalone, no card box)

For use inside grouping boxes — just icon + label, no card border.

```html
<div class="icon-block">
  <img class="icon-block-img" src="[data-uri]" alt="">
  <span class="icon-block-label">Object Storage</span>
</div>

<style>
.icon-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 8px;
  border-radius: 4px;
  transition: background 0.15s;
  cursor: default;
  min-width: 70px;
}
.icon-block:hover { background: rgba(49,45,42,0.06); }
.icon-block-img { width: 32px; height: 32px; }
.icon-block-label {
  font-size: 9px; font-weight: 600; color: #312D2A;
  text-align: center; line-height: 1.3;
}
</style>
```

---

## ARROW / FLOW INDICATOR PATTERNS

### Simple dashed down-arrow (between horizontal sections)
```html
<div class="flow-arrow-down">
  <svg width="100%" height="20" viewBox="0 0 400 20" preserveAspectRatio="none">
    <line x1="33%" y1="2" x2="33%" y2="16" stroke="#312D2A" stroke-width="1"
          stroke-dasharray="3,2" marker-end="url(#arrowhead)"/>
    <line x1="50%" y1="2" x2="50%" y2="16" stroke="#312D2A" stroke-width="1"
          stroke-dasharray="3,2" marker-end="url(#arrowhead)"/>
    <line x1="67%" y1="2" x2="67%" y2="16" stroke="#312D2A" stroke-width="1"
          stroke-dasharray="3,2" marker-end="url(#arrowhead)"/>
    <defs>
      <marker id="arrowhead" viewBox="0 0 10 10" refX="9" refY="5"
              markerWidth="6" markerHeight="6" orient="auto">
        <path d="M1,1 L9,5 L1,9" fill="none" stroke="#312D2A" stroke-width="1.5"/>
      </marker>
    </defs>
  </svg>
</div>
```

### Horizontal right-arrow between pipeline stages
```html
<div class="pipeline-arrow" aria-hidden="true">
  <svg width="36" height="36" viewBox="0 0 36 36">
    <defs>
      <marker id="ph-arrow" viewBox="0 0 10 10" refX="9" refY="5"
              markerWidth="7" markerHeight="7" orient="auto">
        <path d="M1,1 L9,5 L1,9" fill="none" stroke="#312D2A" stroke-width="1.5"/>
      </marker>
    </defs>
    <line x1="4" y1="18" x2="28" y2="18" stroke="#312D2A" stroke-width="1"
          marker-end="url(#ph-arrow)"/>
  </svg>
</div>
```

---

## PATTERN 7: DATABASE SYSTEM ICON NODES (preferred for DB layers)

Use this when representing database layers in OCI/Oracle-style diagrams. Prefer OCI icon-first DB nodes with a single DB name label below (use a local icon key such as `database-system`).

```html
<div class="source-db-row">
  <div class="db-icon-node">
    <img class="db-system-icon" src="[database-system-icon-data-uri]" alt="Database System">
    <span class="db-label">OBA PDB</span>
  </div>
</div>

<style>
.source-db-row {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
}
.db-icon-node {
  min-height: 86px;
  border-radius: 6px;
  border: 1px solid #B6B1AB;
  background: #FAF9F7;
  box-shadow: 0 1px 2px rgba(49,45,42,0.10);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 6px;
}
.db-system-icon {
  width: 34px;
  height: 38px;
  object-fit: contain;
}
.db-label {
  font-size: 10px;
  font-weight: 700;
  text-align: center;
  line-height: 1.2;
  color: #312D2A;
}
</style>
```

---

## TIPS FOR GOOD DIAGRAMS

1. **Use the section-label** above every group of cards — helps scanability
2. **Left accent bar color** on cards signals category at a glance — 5px minimum width; **vary colours across groups** (see tip 17)
3. **Grouping boxes** create visual hierarchy — don't skip them for OCI-scoped content
4. **Padding inside groups**: 28px top (for label), 14px sides, 14px bottom
5. **Card gap inside groups**: 6-8px between cards
6. **Column gap between panel groups**: 0 (use border, not gap)
7. **White cards on neutral background** is the key visual contrast
8. **FA icons in chips**: always set `font-size: 13px; color: var(--card-accent)` — never inherit dark text; chip size must be 22×22px
9. **Category-matched chips**: apply `.chip-ocean`, `.chip-sienna`, `.chip-red`, `.chip-ivy`, or `.chip-bark` to every `.card-icon` — never use the same chip for all cards
10. **Never use grid auto on card widths** — set explicit `min-width` or `flex` values
11. **SVG connectors**: use a `<div style="position:relative">` wrapper on any element where you overlay an SVG connector layer
12. **Panel vs card contrast**: keep parent panels one neutral step darker than inner cards
13. **Dotted flow hints**: use short dashed arrows between adjacent stage columns when sequencing is important
14. **Primary flow arrows**: use Ocean color (#2C5967, 1.5px) for the main flow path — bark gray for all connectors is flat and hard to read
15. **Card title weight**: always 13px/700 — never below 12px or lighter than 600
16. **Swimlane headers**: use the enhanced swimlane-label style (9.5px, letter-spacing 0.10em, 2px bottom border) for full-width lane headers
17. **Accent colour variety — DEFAULT behaviour**: assign different `--card-accent` values to different swimlanes/groups so the full OCI palette is visible in each diagram. Never leave all cards at the default ocean unless the user asks for it.

    **Standard palette** (muted/professional):
    - Channels / Human-facing → `var(--sienna)` + `chip-sienna`
    - Integration / API / ESB → `var(--ocean)` + `chip-ocean`
    - Security / Risk / IAM → `var(--red)` + `chip-red`
    - Compute / Runtime → `var(--ivy)` + `chip-ivy`
    - Observability / Reporting / Audit → `var(--bark)` + `chip-bark`
    - External systems / Payment rails → `var(--bark)` + `chip-bark`
    - Data / Storage → `var(--sienna)` + `chip-sienna`

    **Vivid palette** (more colourful/energetic — use when user says diagram is too grey/muted):
    - Channels / Portal → `var(--vivid-teal)` + `chip-vivid-teal`
    - Data / Events / Messaging → `var(--vivid-orange)` + `chip-vivid-orange`
    - Integration / API / ESB → `var(--vivid-cobalt)` + `chip-vivid-cobalt`
    - Compute / Runtime → `var(--vivid-forest)` + `chip-vivid-forest`
    - Analytics / AI / ML → `var(--vivid-grape)` + `chip-vivid-grape`
    - Security / IAM → `var(--red)` + `chip-red` (unchanged — red is vivid enough)
    - Observability → `var(--bark)` + `chip-bark`

    Remember to include the `--vivid-*` CSS variables and `chip-vivid-*` classes in the diagram `<style>` block when using the vivid palette. See STYLE.md Extended Vivid Palette section.
