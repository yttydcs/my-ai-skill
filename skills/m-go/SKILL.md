---
name: m-go
description: Automated delegated execution and test loop for confirmed m-autoflow plans.
---

# m:go

## Overview

Use this skill after `$m-plan` when the user wants high-automation execution. `$m-go` is stricter than `$m-execute`: the main agent coordinates and audits, while worker sub-agents perform all implementation edits. After delegated implementation completes, `$m-go` automatically runs `$m-test` behavior and loops delegated fixes until acceptance passes or a blocker is explicit.

## Quick Start

- Read `references/go.md`.
- Read `../m-autoflow/references/subagents.md` before dispatching workers.
- Read `../m-test/references/testing.md` before the automatic validation loop.
- Read `../m-autoflow/references/output-components.md` before presenting orchestration or validation results.
- Confirm the active worktree root has an approved `plan.md` or `todo.md`.
- Treat `$m-go` invocation as user authorization to use worker sub-agents for the approved execution scope when host policy permits delegation.

## Entry Gate

`$m-go` may start only when all are true:

- requirements and architecture are unblocked
- the active worktree root has a confirmed `plan.md` or `todo.md`
- every intended change maps to an approved Task ID
- Task IDs have bounded write sets and acceptance criteria
- host sub-agent tools are available and delegation is permitted
- the user has invoked `$m-go` or otherwise explicitly approved delegated execution

If any item is false, return to `$m-plan` or `$m-execute` with a blocker instead of falling back to main-agent implementation.

## Main Agent Boundary

During `$m-go`, the main agent may schedule, package context, inspect files, run commands, review diffs, resolve coordination, synthesize validation, and accept or reject results.

The main agent must not directly edit implementation files. If integration, repair, docs, plan-status, or validation-fix edits are required, dispatch a worker with a bounded Task ID and write set.

## Workflow

1. Restate the approved Task IDs, write sets, acceptance criteria, and automatic test obligations.
2. Assess parallelism by Task ID, write set, dependency order, and risk.
3. Dispatch worker sub-agents for every implementation edit; use parallel workers for independent non-conflicting write sets.
4. Give each worker the complete context package from `references/go.md`.
5. Review every worker result, changed file list, validation output, risks, and rollback note.
6. Reject or re-dispatch any result that drifts from the plan, touches forbidden files, or leaves acceptance incomplete.
7. Run lightweight validation after delegated implementation converges.
8. Automatically run `$m-test` behavior using `../m-test/references/testing.md`.
9. If validation fails, delegate bounded fixes and repeat validation.
10. Stop only when all acceptance checks pass, the user changes direction, or a blocker is explicit.

## Exit Gate

End with:

- changed files by Task ID and worker
- worker dispatch summary and parallelism decisions
- validation and `$m-test` result table
- failed or blocked items, if any
- risks and rollback notes
- decision to return to delegated execution or proceed to `$m-archive`

Use clickable changed-file links and compact worker / Task ID / validation tables. Embed representative visual evidence when UI acceptance was exercised; use Mermaid only when worker dependencies or execution lanes are otherwise unclear.

Do not create `docs/change`, merge branches, clean worktrees, push, or claim workflow completion from this phase.
