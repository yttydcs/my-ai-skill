# 2026-07-08_m-test-ui-evidence

## Source

- Source: Codex chat
- Date: 2026-07-08
- Requester: user

## Original Request Evidence

The user accepted the proposed UI validation rule and added two requirements:

- UI changes should be tested by actually opening the interface, operating it, and providing acceptance screenshots.
- `$m-test` should output a concise table directly to the user showing which checks passed and which did not, reducing the need to open markdown files.
- `$m-test` remains optional; the user may choose to skip testing and go directly to `$m-archive`.

## Interpreted Requirement

- When `$m-test` runs for UI-impacting changes, actual UI operation and screenshot evidence are required.
- Missing UI evidence during a run `$m-test` is a failure or blocker.
- `$m-test` must summarize results in a direct pass/fail table.
- Explicit user skip remains valid, but `$m-archive` must record missing evidence and residual risk.

## Routed Docs

- Feature: [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)
- Requirements: [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)
- Specs: [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)
- Change archive: [../change/2026-07-08_m-test-ui-evidence.md](../change/2026-07-08_m-test-ui-evidence.md)

## Open Questions

- None.
