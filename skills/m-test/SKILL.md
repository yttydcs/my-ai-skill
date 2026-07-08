---
name: m-test
description: Optional heavy test and review phase for the m-autoflow workflow. Use after $m-execute when the change needs integration testing, end-to-end workflow validation, UI operation with screenshot evidence, manual or product usability review, security review, performance metrics, or final high-risk review before docs/change archival. Users may explicitly skip this phase and go to $m-archive, but the skip reason and residual risk must be recorded.
---

# m:test

## Overview

Use this skill for heavyweight validation and review after `$m-execute`. It is optional: the user may explicitly skip this phase and proceed to `$m-archive`, with the skip reason and residual risk recorded.

When this phase runs for UI-impacting changes, the UI must be opened, the affected path must be operated, and screenshot evidence must be reported. Missing UI evidence is a failed or blocked `$m-test`, not a pass.

## Quick Start

- Read `references/testing.md`.
- Read `../m-autoflow/references/subagents.md` before parallel validation or delegated review.
- Use the active `plan.md` or `todo.md` as the source of acceptance criteria.

## Entry Gate

Heavy testing may start only when:

- execution has produced changes mapped to Task IDs
- the active plan lists acceptance criteria and test points
- the current worktree state is understood

If implementation is incomplete or unmapped, return to `$m-execute`.

## Workflow

1. Identify changed files, Task IDs, acceptance criteria, user-facing paths, security boundaries, and performance-sensitive paths.
2. Decide whether this heavy phase is needed, unless the user explicitly chose to skip `$m-test` and proceed to `$m-archive`.
3. If skipping, record the skip reason, execution-stage checks, residual risk, and why the user accepted missing heavy validation.
4. If running, validate whole flows or integration points, not just syntax or isolated units.
5. If UI is impacted, open the actual application or page, perform the affected user operations, and capture screenshot evidence.
6. Review usability, security, and performance metrics or thresholds where applicable.
7. Perform the review checklist from `references/testing.md`.
8. Output a concise user-facing result table with pass/fail/blocked/skipped status.
9. If any review item fails, record the failing item and return to `$m-execute`.
10. If skipped or all run items pass, report that the workflow may proceed to `$m-archive`.

## Exit Gate

Output:

- whether the heavy test phase was run or skipped
- skip reason when skipped
- tests, flows, or review checks run
- pass/fail result
- uncovered risk or missing manual verification
- UI operation and screenshot evidence when UI is impacted and `$m-test` ran
- a concise pass/fail table in the direct user response
- review checklist status
- decision: return to execution or proceed to archive

Do not create archives, merge, clean worktrees, or mark the workflow ended from this phase.
