# Project Context

## Objective
Build a reusable local skill/workspace that can produce professional Oracle OCI architecture diagrams quickly, with consistent Redwood styling and strong visual polish.
Target visual tone should match OCI diagram toolkit samples: neutral gray/light backgrounds with restrained sienna/ocean accents.

## Required Output Contract
- File format: standalone `.html`
- Output location: `output/<project>/<meaningful-file-name>-v1.html` then `-v2`, `-v3`, etc.
- Never overwrite prior versions.
- Include a quick-edit mode in each generated HTML so text and labels can be edited directly in-browser.
- Keep diagrams architecture-professional: clear layer/card contrast, semantic icons, and restrained flow connectors.

## Primary Workflow
1. Ideation and requirement clarification with the user.
2. Convert requirements into components, groups, and flows.
3. Select layout pattern from `skill/references/PATTERNS.md`.
4. Apply OCI style rules from `skill/references/STYLE.md`.
5. Generate versioned HTML output under `output/<project>/`.
6. Run visual QA gate (`skill/scripts/visual_qa.py`) and pass before delivery.
7. Iterate by reading the previous version and writing a new version.

## Current Directory Layout
- `AGENTS.md`: startup rules for this workspace.
- `context/`: persistent project memory and session handoff.
- `context/START_HERE.md`: command-level runbook for each new diagram.
- `skill/SKILL.md`: execution instructions for the architecture-diagram skill.
- `skill/references/`: style/pattern reference docs.
- `skill/templates/`: reusable HTML starter templates.
- `skill/assets/icons/`: OCI icon metadata and inlined icon registry.
- `skill/scripts/`: utility scripts (icon extraction, version path helper).
- `source/oracle-downloads/`: original Oracle downloads (zip/pptx).
- `source/extracted/`: extracted drawio/visio source assets.
- `input/`: user-provided drafts/screenshots.
- `output/`: generated diagram versions.
- `examples/`: reference sample outputs.

## Oracle Assets In Repo
- Draw.io pack: `source/oracle-downloads/OCI-Style-Guide-for-Drawio.zip`
- Visio pack: `source/oracle-downloads/OCI_Icons_Visio.zip`
- OCI icon PPTX: `source/oracle-downloads/OCI_Icons.pptx`
- Extracted drawio files: `source/extracted/drawio/OCI Style Guide for Drawio/`
- Extracted visio files: `source/extracted/visio/OCI/`
