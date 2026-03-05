# Start Here

## Typical Flow Per Diagram
1. Add any screenshots/drafts to `input/`.
2. Ideate and clarify requirements before drawing.
3. Choose project slug and diagram name.
4. Compute next output path:
   - `python3 skill/scripts/next_version_path.py --project <project> --name <diagram-name> --mkdir`
5. Build HTML using:
   - `skill/templates/oci-diagram-base.html`
   - `skill/references/STYLE.md`
   - `skill/references/PATTERNS.md`
   - For OCI slide-like visuals, keep neutral-gray dominant surfaces and use sienna/ocean only as restrained accents.
   - Keep panel/card contrast clear, apply semantically appropriate icons, and add dotted flow connectors only where they improve readability.
   - Use the default legibility treatment for service cards: slightly larger/brighter icon chips with clear contrast.
   - Keep the shared shell intact (Oracle top bar, edit toolbar, slide/full toggle, toolbar show/hide, Save/Copy/Export PNG controls, and `Review Annotate` controls for sticky notes + shape/freehand markup).
   - In `Slide Layout`, prefer fit-to-16:9 behavior for single-screen capture; use scroll fallback only when content cannot fit legibly.
   - Keep manual drawing scoped to review mode only (sticky/rectangle/oval/pen); structural/layout changes should still be done via LLM-driven regeneration.
6. Save to the returned `output/<project>/<diagram-name>-vN.html` path.
7. Run visual QA gate (mandatory before delivery):
   - `python3 skill/scripts/visual_qa.py --html <output-file> --fix --require-pass --report <output-file>.visual-qa.json`
8. Update `context/SESSION_STATE.md` with what changed.

## OCI Icon Asset Notes
- Embedded icon map: `skill/assets/icons/oci_icons.json`
- Icon metadata: `skill/assets/icons/oci_meta.json`
- Re-extract from Oracle PPTX when needed:
  - `python3 skill/scripts/extract_icons.py --pptx source/oracle-downloads/OCI_Icons.pptx`
