# Searchable Lessons Capture

## Summary

Promote reusable troubleshooting knowledge from `docs/change` into `docs/lessons` during archive so the next investigation can start from symptoms and quick checks instead of re-reading full workflow history.

## Lookup Hints

- Symptoms: the same problem keeps sending people back to old change logs or chat history
- Keywords: archive, lessons, troubleshooting, recurring investigation, quick checks
- Trigger Conditions: a workflow finishes after a costly or non-obvious investigation
- Quick Checks:
  - confirm the change archive recorded `Lessons impact`
  - check whether a related lesson path was added
  - verify `docs/lessons/README.md` exposes the lesson for lookup

## Symptoms

- A completed workflow contains useful debugging knowledge, but future users cannot find it quickly.
- The archive answers "what changed" but not "what should I check first next time?".
- Similar questions lead to repeated scans of historical change docs.

## Impact

- Troubleshooting becomes slower because the reusable path is buried in workflow history.
- Teams repeat expensive investigation steps that could have been summarized once.
- The docs system feels complete on paper but weak in day-two operations.

## Trigger Conditions

- Stage `4` archive focuses only on shipped changes and verification.
- `docs-governor` and `rigorous-execution` are both involved, but no explicit handoff exists for lesson promotion.
- The investigation revealed a structural pattern, a reusable guardrail, or a non-obvious diagnostic path.

## Root Cause

The documentation model separated `change` and `lessons`, but the archive workflow did not require a searchable handoff from one category to the other.

## Investigation Trail

- Compared `rigorous-execution` stage `4` requirements with `docs-governor` lessons rules.
- Checked repository indexes and found no direct troubleshooting entry path beyond generic lessons guidance.
- Confirmed that stable docs existed for `rigorous-execution`, but `docs-governor` lacked stable requirement/spec coverage.

## Resolution

- Made `rigorous-execution` stage `4` record lessons impact, related lessons, and query cues.
- Made `docs-governor` route troubleshooting lookup through `lessons` first.
- Added stable docs and indexes so the lessons workflow is now governed instead of informal.

## Prevention / Guardrails

- Do not leave reusable troubleshooting knowledge only inside `docs/change`.
- Capture lookup hints in every lesson: symptoms, keywords, trigger conditions, and quick checks.
- Update `docs/lessons/README.md` whenever a new lesson is created or renamed.
- Keep stable requirements/specs separate from lessons even when the lesson triggered the correction.

## Related Docs

- [../requirements/rigorous-execution-skill.md](../requirements/rigorous-execution-skill.md)
- [../specs/rigorous-execution-skill.md](../specs/rigorous-execution-skill.md)
- [../requirements/docs-governor-skill.md](../requirements/docs-governor-skill.md)
- [../specs/docs-governor-skill.md](../specs/docs-governor-skill.md)
- [../change/2026-03-23_lessons-archive-lookup.md](../change/2026-03-23_lessons-archive-lookup.md)
