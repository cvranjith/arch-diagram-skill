# OCI Architecture Diagram Workspace

## Startup Context
- Read `context/PROJECT_CONTEXT.md` first.
- Read `context/SESSION_STATE.md` next.
- Read `context/START_HERE.md` for command-level workflow.
- For diagram generation tasks, read `skill/SKILL.md` and the references it points to.

## Goal
- Generate professional Oracle OCI architecture diagrams in standalone HTML format.
- Keep outputs versioned and stored under `output/<project>/<diagram-name>-vN.html`.
- Ensure each generated HTML includes quick-edit mode for manual WYSIWYG-style updates.

## Collaboration Rules
- Ask clarifying questions before generating a new diagram.
- Summarize assumptions and wait for user confirmation when requirements are unclear.
- Never overwrite an existing diagram version.
- Update `context/SESSION_STATE.md` after major milestones so future sessions have continuity.

## Inputs And Outputs
- User-provided drafts/screenshots belong in `input/` unless the user gives another path.
- Keep Oracle source downloads in `source/oracle-downloads/`.
- Keep extracted Oracle source artifacts in `source/extracted/`.
