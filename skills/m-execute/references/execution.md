# Execution Rules

Use this reference for `$m-execute`, the implementation phase of `m-autoflow`.

## Phase Boundary

- Owns code, configuration, test fixture changes, lightweight validation and lightweight requirements/standards review required by approved Task IDs.
- May update the active plan status for the touched tasks.
- Does not own plan creation, broad replanning, heavy integration testing, archive, merge, or worktree cleanup.

## Hard Rules

- Stay inside the active worktree, or the exact per-repository worktree set recorded by an approved multi-repository plan/manifest.
- Map every changed file to a Task ID.
- Do not introduce plan-external behavior; return to planning if scope expands.
- Do not silently swallow errors.
- Do not revert user or other-agent changes unless explicitly requested.
- Discover facts and choose reversible in-scope implementation details using project conventions. Ask only when an unresolved decision materially affects behavior, compatibility, architecture, permissions, data, scope or acceptance, or a required prerequisite is unavailable. Do not repeat approval for the existing scope.

## Parallelism

Before editing, assess whether tasks can be split by Task ID and write set.

Use sub-agents only when:

- the active plan is confirmed
- the delegated Task ID is bounded
- write sets do not conflict
- context can be packaged completely
- host policy and user authorization allow it

If sub-agents are skipped, state the concrete reason.

## Implementation Checklist

- input validation and explicit failure paths
- error handling and observability where applicable
- safe defaults where applicable
- no avoidable O(n^2), N+1, repeated I/O, or needless copying
- clear naming and local style consistency
- no avoidable circular dependencies
- rollback point recorded in the plan

## Lightweight Validation

Run cheap, local checks in this phase when practical. For multi-repository work, apply them to every affected repository and do not report an aggregate pass while one participating repository fails:

- syntax checks
- type checks
- lint checks scoped to touched files
- formatting checks scoped to touched files
- focused unit tests for changed logic
- `git diff --check`

Use the plan's observation boundaries and independent expected results. For a bug fix, normally reproduce the failure before fixing it; for important new behavior, prefer small test/implementation/validation cycles. Do not add tests that restate the implementation, or force TDD for every reversible low-impact edit.

Record evidence against AC IDs and Task IDs; an already approved plan may use its existing acceptance labels. Record skipped checks with reasons and residual risk. Reserve heavy integration, end-to-end, usability, security, and performance review for `$m-test`.

## Lightweight Review

After focused validation, apply `../../m-autoflow/references/review.md` to the actual integrated candidate. Its scope, identity, separate requirements/standards verdicts and freshness rules are authoritative. Resolve in-scope findings before reporting readiness, or retain an explicit failed/blocked/waived disposition. Skipping heavy testing does not skip this review.
