# Go Rules

Use this reference for `$m-go`, the delegated execution and automatic test-loop entry in the `m-autoflow` workflow.

## Phase Boundary

- Owns high-automation implementation orchestration after a confirmed `$m-plan`.
- Composes stage `3.2` delegated implementation and stage `3.3` heavy validation behavior.
- Requires worker sub-agents for implementation edits.
- May run commands, inspect diffs, and validate results from the main agent.
- Does not own requirements discovery, architecture replanning, archive, merge, worktree cleanup, or push.

## Hard Rules

- Stay inside the active worktree.
- Require a confirmed `plan.md` or `todo.md`.
- Map every changed file to an approved Task ID.
- Do not introduce plan-external behavior; return to `$m-plan` if scope expands.
- Do not silently swallow worker failures, validation gaps, or unavailable tooling.
- Do not fabricate `$m-test` success.
- Do not allow the main agent to directly edit implementation files during `$m-go`.
- If an edit is needed after review, delegate that edit to a worker with a bounded write set.
- If the user wants to skip heavy validation, route to `$m-execute` plus explicit `$m-test` skip handling instead of using normal `$m-go`.

## Main Agent Responsibilities

The main agent must personally own:

- entry-gate checks
- Task ID and write-set analysis
- worker context packaging
- worker dispatch ordering and parallelism decisions
- conflict detection and resolution strategy
- review of worker-reported files, tests, risks, and rollback notes
- command execution for integrated validation when useful
- `$m-test` result synthesis
- final acceptance decision and user-facing status

The main agent must not personally own implementation edits in `$m-go`.

## Parallelism

Before dispatch, classify approved Task IDs:

- independent and safe to run in parallel
- serial because of dependency order
- serial because of overlapping write sets
- blocked because context, write set, or acceptance is unclear

Use parallel workers when all are true:

- two or more Task IDs are independently acceptable
- write sets do not conflict
- context packages can be complete
- host policy permits delegation
- user authorization exists through `$m-go` invocation or another explicit statement

When only one Task ID can execute, dispatch one worker. Do not fall back to main-agent implementation.

## Required Worker Context Package

Every worker must receive:

- Stage: `3.2` for implementation or `3.3` for validation/review fixes
- Workflow goal
- Current repository
- Current branch
- Base branch
- Worktree absolute path
- Required plan path
- Task ID and title
- Task goal
- Acceptance criteria
- AC IDs, original source constraints and observation boundaries
- Test points
- Rollback point
- Allowed files and directories
- Forbidden files and directories
- Relevant requirement and architecture summary
- Key code or docs references
- Notice that other workers may be editing nearby areas
- Instruction not to revert user or other-worker changes

## Worker Dispatch Rules

Tell each worker:

- complete only the assigned Task ID
- stay inside the allowed write set
- do not add plan-external changes
- do not change unrelated formatting
- validate the changed path where practical
- report changed files, design points, validation results, risks, rollback notes, and completion status

## Integration Review

After a worker reports completion, the main agent must:

- inspect the worker's changed files and status
- confirm every file maps to the assigned Task ID
- confirm acceptance criteria are satisfied or clearly incomplete
- run or schedule relevant lightweight validation
- check for write-set conflicts with other worker output
- reject the result or dispatch follow-up work if scope drift, missing validation, or failed acceptance appears

Apply `../../m-autoflow/references/review.md` to the integrated candidate before acceptance. Worker self-reports do not replace requirements/standards review. Preserve the AC/Task/evidence map and refresh only affected results after repairs.

If integration itself needs file edits, dispatch an integration worker with a narrow write set.

## Automatic Test Loop

After delegated implementation converges:

1. Run lightweight implementation checks when practical.
2. Run `$m-test` behavior using `../m-test/references/testing.md`.
3. Produce the direct `$m-test` result table.
4. If every check passes, report that the workflow may proceed to `$m-archive`.
5. If any item fails, map each failure to a Task ID or create a planning blocker.
6. Delegate bounded fixes for mapped failures.
7. Repeat validation until checks pass or a blocker is explicit.

## Blocking Conditions

Block instead of continuing when:

- no confirmed plan exists
- sub-agent tools are unavailable
- host policy forbids delegation
- the approved plan lacks Task IDs, write sets, acceptance, or tests
- a required fix is outside the approved plan
- worker outputs conflict and cannot be resolved within existing Task IDs
- validation requires credentials, services, assets, or UI access that are unavailable
- repeated fix attempts expose an unresolved requirement or architecture issue

Use:

```md
问题清单
- <blocking issue>

阻塞：是
返回计划或等待用户输入
禁止进入归档
```

## Exit Report

When `$m-go` finishes or blocks, report:

- Task IDs executed
- workers used and parallelism decisions
- changed files by worker
- validation commands and `$m-test` results
- direct pass/fail/blocked/skipped table
- unresolved risks
- rollback notes
- whether to return to `$m-go`, return to `$m-plan`, or proceed to `$m-archive`
