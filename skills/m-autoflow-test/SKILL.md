---
name: m-autoflow-test
description: Optional heavy test and review phase for the m-autoflow staged engineering workflow. Use after execution when the change needs integration testing, end-to-end workflow validation, manual or product usability review, security review, performance metrics, or final high-risk review before docs/change archival. Small low-risk changes may skip this phase when execution-stage lightweight validation is sufficient and the skip reason is recorded.
---

# m:autoflow test

## Overview

Use this skill for heavyweight validation and review after `$m-autoflow-execute`. It is optional: skip it for low-risk small changes when execution-stage checks already cover the change.

## Quick Start

- Read `references/testing.md`.
- Read `../m-autoflow/references/subagents.md` before parallel validation or delegated review.
- Use the active `plan.md` or `todo.md` as the source of acceptance criteria.

## Entry Gate

Heavy testing may start only when:

- execution has produced changes mapped to Task IDs
- the active plan lists acceptance criteria and test points
- the current worktree state is understood

If implementation is incomplete or unmapped, return to `$m-autoflow-execute`.

## Workflow

1. Identify changed files, Task IDs, acceptance criteria, user-facing paths, security boundaries, and performance-sensitive paths.
2. Decide whether this heavy phase is needed.
3. If skipping, record the skip reason, execution-stage checks, residual risk, and why usability/security/performance/integration review is unnecessary.
4. If running, validate whole flows or integration points, not just syntax or isolated units.
5. Review usability, security, and performance metrics or thresholds where applicable.
6. Perform the review checklist from `references/testing.md`.
7. If any review item fails, record the failing item and return to `$m-autoflow-execute`.
8. If skipped or all run items pass, report that the workflow may proceed to `$m-autoflow-archive`.

## Exit Gate

Output:

- whether the heavy test phase was run or skipped
- skip reason when skipped
- tests, flows, or review checks run
- pass/fail result
- uncovered risk or missing manual verification
- review checklist status
- decision: return to execution or proceed to archive

Do not create archives, merge, clean worktrees, or mark the workflow ended from this phase.
