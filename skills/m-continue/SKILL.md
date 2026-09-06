---
name: m-continue
description: Continue an already approved m-autoflow workflow after an m-execute or m-test pass. Reuse the existing execution and testing phases unattended until all acceptance criteria converge or further in-scope progress is genuinely impossible.
---

# m:continue

## Overview

Use this skill to resume an approved workflow after `$m-execute` or `$m-test`. Treat one invocation as authorization to alternate the existing execute and test behaviors without asking whether to continue after ordinary failures.

## Quick Start

- Read `references/continue.md` for state recovery, progress comparison, loop transitions, and terminal rules.
- Read `../m-execute/SKILL.md` and `../m-execute/references/execution.md` before applying execution behavior.
- Read `../m-test/SKILL.md` and `../m-test/references/testing.md` before applying test behavior.
- Read `../m-autoflow/references/review.md` before reusing previous review or acceptance evidence.
- Read `../m-autoflow/references/subagents.md` before any parallelism assessment or delegation.
- Read `../m-autoflow/references/output-components.md` before presenting progress or the terminal result.
- Use the active `plan.md` or `todo.md` as the source of approved Task IDs, write sets, acceptance criteria, and test points.

## Entry Gate

Start only when all are true:

- an approved active `plan.md` or `todo.md` exists
- the workflow has completed at least one `$m-execute` or `$m-test` pass
- intended repairs remain mapped to approved Task IDs and write sets
- current worktree state and available phase evidence can be inspected

If the plan is missing, stale, or requires new scope, stop with the exact `$m-plan` handoff instead of inventing authorization.

## Authorization Boundary

Treat invocation as authorization for every subsequent execute/test iteration inside the existing approved scope. Do not ask whether to continue between phases or after an ordinary failed pass.

Do not treat invocation as authorization for new requirements, unmapped files, destructive actions, archive, merge, cleanup, publication, push, credentials, or external state changes. Preserve `$m-execute` delegation rules; `$m-continue` does not impose `$m-go` mandatory worker-only edits.

## Workflow

1. Recover the current state from the active plan, worktree/diff, and latest reliable execute/test evidence.
2. Apply `$m-execute` behavior when implementation is incomplete or validation failed.
3. Apply `$m-test` behavior when implementation is ready for validation.
4. Compare each complete repair/test cycle with the preceding failure and progress evidence.
5. Continue automatically while acceptance is incomplete and measurable progress remains possible.
6. Stop successfully only after all approved acceptance criteria converge.
7. Stop unsuccessfully only for a hard blocker or the non-progress threshold defined in `references/continue.md`.

Intermediate commentary may summarize the current iteration and next automatic transition. It must not pause the loop or request continuation confirmation.

## Exit Gate

Report:

- terminal status: `Passed` or `Blocked`
- Task IDs and iterations executed
- final test result or justified skip
- progress evidence or repeated failure signature
- remaining risks and rollback notes
- decision: ready for `$m-archive`, or exact blocker and required handoff

Do not create `docs/change`, invoke `$m-archive`, merge, clean a worktree, publish, push, or claim full workflow closeout from this skill.
