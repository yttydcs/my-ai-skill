# 2026-07-15 Visual Output Components

## Change Goal

Make skill results easier to scan, open, verify, and act on by adopting current Codex visual components without turning simple answers into decorative dashboards.

## Changes

- Added one shared output-component reference for the `m-*` workflow family.
- Added component selection rules for compact tables, Mermaid, absolute clickable file links, embedded visual evidence, line-specific code comments, and successful Git actions.
- Added phase recipes so each skill uses only the components appropriate to its output shape.
- Updated UI validation guidance to embed representative screenshots and link additional evidence.
- Added a standalone compact output contract for thesis AIGC revision work.
- Added regression coverage for shared-reference routing and component safety rules.

## Docs Impact

- Intake impact: updated
- Feature impact: updated
- Requirements impact: updated
- Specs impact: updated
- Decision impact: none
- Lessons impact: none

## Related Docs

- [Original request](../intake/2026-07-15_visual-output-components.md)
- [m-autoflow feature](../features/m-autoflow-workflow.md)
- [m-autoflow requirements](../requirements/m-autoflow-skill.md)
- [m-autoflow spec](../specs/m-autoflow-skill.md)
- [thesis revision requirements](../requirements/m-thesis-aigc-revision-skill.md)
- [thesis revision spec](../specs/m-thesis-aigc-revision-skill.md)

## Validation

- All 12 changed skill packages passed `quick_validate.py` through `tools/validate-skills.ps1`.
- Full Python unit-test discovery passed 15 tests; 1 existing Windows symlink-privilege case was skipped as expected.
- Source / installed-package SHA-256 parity passed for all 12 synchronized skills.
- `git diff --check` passed; line-ending warnings were informational.

## Risk And Rollback

- Risk: overly broad component use could make responses noisy; the shared contract requires the smallest useful component and readable plain-Markdown fallback.
- Risk: app directives could misrepresent state; the contract forbids directives for attempted, failed, skipped, or merely recommended actions.
- Rollback: revert this change and resynchronize the affected skill packages.

## Sub-agent Trace

- No sub-agents were used; repository policy did not request delegation and the output-contract edits were tightly related.
