---
name: m-autoflow-execute
description: Execution phase for the m-autoflow staged engineering workflow. Use only after a confirmed root plan.md/todo.md exists and the user has approved implementation. Implements mapped Task IDs inside the active worktree, performs a parallelism assessment, applies the smallest safe code changes, runs lightweight syntax/static/focused validation such as lint, typecheck, formatting, targeted unit tests, or git diff checks when practical, and reports file-level changes without archiving or closing the workflow.
---

# m:autoflow execute

## Overview

Use this skill to implement confirmed plan tasks inside the active worktree. It is the split `m-autoflow` phase for code changes and lightweight validation.

## Quick Start

- Read `references/execution.md`.
- Read `../m-autoflow/references/subagents.md` before any parallelism assessment or delegation.
- Confirm the active `plan.md` or `todo.md` is complete, current, and approved by the user.

## Entry Gate

Implementation may start only when all are true:

- requirements and architecture are unblocked
- the active worktree root has a confirmed `plan.md` or `todo.md`
- every intended change maps to a Task ID
- the user has approved moving from planning into execution

If any item is false, return to `$m-autoflow-plan`.

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

## Exit Gate

End with:

- changed files
- Task ID mapping
- key design decisions
- lightweight validation already run
- heavier validation or review still needed
- risks and rollback notes

Do not create `docs/change`, merge branches, clean worktrees, or claim workflow completion from this phase.
