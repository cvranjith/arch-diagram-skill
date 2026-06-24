# OCI Architecture Diagram Skill Workspace

A local, reusable workspace for generating professional Oracle OCI architecture diagrams as standalone HTML. The focus is consistent “Redwood” visual tone, clear semantic structure, and quick-edit ergonomics for review and iteration.

## What This Workspace Provides
- **Stand‑alone HTML outputs** with embedded CSS/JS and a built‑in quick‑edit mode for WYSIWYG label changes.
- **Versioned outputs** under `output/<project>/<diagram-name>-vN.html` (never overwrite prior versions).
- **Consistent OCI styling** aligned to Oracle diagram toolkit patterns (neutral gray surfaces with restrained sienna/ocean accents).
- **Icon system and assets** extracted from official OCI packs, with OCI‑first icon usage and documented metadata.
- **Layout patterns and style rules** for cards, panels, lanes, connectors, and service grids.
- **Review tooling** in generated HTML: sticky notes, pointers, and markup (rectangle/oval/pen) that persist in saved HTML and PNG exports.
- **PNG export** support and slide‑layout toggle for 16:9 capture workflows.
- **Visual QA gate** to enforce formatting and layout quality before delivery.

## Repository Layout
- `context/` — project memory, runbook, and session handoff
- `skill/` — skill instructions, templates, references, scripts, and icon assets
- `output/` — versioned diagram HTML outputs
- `input/` — user‑provided screenshots/drafts
- `source/` — Oracle downloads and extracted source assets
- `examples/` — sample outputs and icon previews

## Typical Workflow (High Level)
1. Read `context/PROJECT_CONTEXT.md`, `context/SESSION_STATE.md`, and `context/START_HERE.md`.
2. Clarify requirements with the user.
3. Pick a layout pattern from `skill/references/PATTERNS.md`.
4. Apply OCI style rules from `skill/references/STYLE.md`.
5. Generate versioned HTML in `output/<project>/`.
6. Run the visual QA gate via `skill/scripts/visual_qa.py`.
7. Update `context/SESSION_STATE.md` with the milestone.

## Requirements
- Python 3.x for helper scripts (versioning, QA, icon extraction)

## Notes
- Manual drawing is intended for review annotations only; structural edits should be done by regenerating HTML.
- The viewer `arch-viewer.html` can extract the diagram canvas/CSS for quick review and export.

## License
No license specified. Add one if you plan to publish.
