---
name: m-execute
description: Execution phase for approved m-autoflow plans. Implements mapped Task IDs in the approved worktree set, performs a parallelism assessment, applies bounded changes, validates behavior and reviews requirements and standards before handing off to optional heavy testing or archive.
---

# m:execute

## Overview

Use this skill to implement confirmed plan tasks inside the active repository worktree or exact approved multi-repository worktree set. It is the `m-autoflow` phase for code changes and lightweight validation.

## Quick Start

- Read `references/execution.md`.
- Read `../m-autoflow/references/review.md` before reviewing the execution result.
- Read `../m-autoflow/references/subagents.md` before any parallelism assessment or delegation.
- Read `../m-autoflow/references/output-components.md` before presenting the execution result.
- Confirm the active `plan.md` or `todo.md` is complete, current, and approved by the user.

## Entry Gate

Implementation may start only when all are true:

- requirements and architecture are unblocked
- every active participating repository worktree root has its confirmed `plan.md` or `todo.md`
- every intended change maps to a Task ID
- the user has approved moving from planning into execution

If any item is false, return to `$m-plan`.

## Workflow

1. Restate the approved Task IDs and write set.
2. Report a parallelism assessment before editing.
3. Give a file-level change summary and design notes before edits.
4. Implement the smallest safe changes that satisfy the task acceptance criteria.
5. Validate external inputs and fail explicitly on invalid states.
6. Preserve module boundaries, dependency direction, and existing local style.
7. Avoid unrelated refactors, broad formatting, hidden environment assumptions, and plan-external changes.
8. Run lightweight validation when practical: syntax, typecheck, focused lint, touched-file formatting, focused unit tests, or `git diff --check`.
9. Update the plan status only for the tasks actually changed.
10. Review the actual candidate against requirements and standards using the shared review contract. Record AC-to-Task evidence, separate axis conclusions and candidate/plan identity; keep failed, blocked or waived items distinct from passes.

## Exit Gate

End with:

- changed files
- Task ID mapping
- key design decisions
- lightweight validation already run
- AC-to-Task evidence and current requirements/standards review conclusions
- heavier validation or review still needed
- risks and rollback notes

Use a compact Task ID / changed-file / validation table when several mappings exist, and make changed files clickable. Emit Git components only for successful Git actions that were actually part of the authorized execution.

Do not create `docs/change`, merge branches, clean worktrees, or claim workflow completion from this phase.
