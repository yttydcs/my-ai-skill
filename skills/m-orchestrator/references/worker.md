# Worker Contract

## Entry Gate

A Worker starts only with a validated project configuration, an approved plan, exact Task IDs, a dedicated worktree for every participating repository, a persisted Task manifest, and a complete dispatch package.

Confirm every repository's root plan and planning ref before implementation. A missing, stale, or mismatched worktree, plan, repository, or ref blocks execution and returns an actionable status to the Planner.

## Execution

1. Load every configured `local:` Worker context.
2. Apply `$m-execute` to only the approved Task IDs, participating repository worktrees, and per-repository write sets.
3. Preserve its input validation, error handling, file ownership, rollback, and lightweight-validation rules.
4. Compute the runtime composite change identifier over the sorted participating repository snapshots: current commits, tracked diffs, untracked file content, and root-plan hashes.
5. Write a lightweight-gate evidence file with overall `Passed` status, the composite change identifier, and one `Passed` repository entry per selected repository. Include commands, exit statuses, and applicability/skips, but no context secrets.

## Lightweight Gate

Run every applicable cheap check in each affected repository before Tester admission:

- syntax or compilation
- type checking
- focused lint and formatting checks
- focused unit tests for changed logic
- unresolved conflict-marker inspection
- import/module-resolution checks when applicable
- `git diff --check`

An inapplicable check may be marked `Skipped` with a reason and residual risk. A failed applicable check keeps the Task in execution. Do not enqueue, reserve, or create a Tester until every applicable check passes for the current change identifier.

Any implementation or plan edit in any participating repository after gate creation invalidates the aggregate gate. Enqueue and Tester acquisition re-check the current composite identifier. Repair work must produce a new identifier and rerun the complete gate across the worktree set.

## Tester Admission

1. Transition the Task to `WAITING_FOR_TESTER` with the passing gate evidence and change identifier.
2. Enqueue once in the configured project Tester pool.
3. Use non-blocking acquisition; remain queued when capacity is unavailable.
4. After a lease is issued, create one temporary Tester sub-agent with access to the complete Worker worktree set and the complete stage `3.3` context package.
5. Load configured `local:` Tester contexts before invoking `$m-test`.
6. Heartbeat the lease during long validation and release it immediately after the Tester result is persisted.

## Failure And Repair

A failed Tester result must identify Task IDs, acceptance checks, reproduction commands, evidence locations, and whether the failure remains inside the approved scope.

Release project and host permits before repair. Transition to `TEST_FAILED`, then return to `EXECUTING` and apply `$m-execute` behavior. After repair, recompute the change identifier, rerun the full lightweight gate, and requeue.

Use the existing `$m-continue` only when the user explicitly invokes that companion for an already-started execute/test workflow. The orchestrator does not silently replace its own state and pool contract with `$m-continue`.

## Success

Persist the passing `$m-test` result for the complete repository set, release Tester capacity, transition through `TEST_PASSED` to `WAITING_FOR_MERGE`, and enqueue the capacity-one integration pool. After admission, invoke `$m-archive` as the archive, per-repository merge, and cleanup authority. Report partial integration as blocked; never claim cross-repository atomicity.

## Blockers

Block and notify the Planner when progress requires new Task IDs, a larger write set, architecture changes, credentials, destructive actions, deployment/publication authority, unavailable external state, or a context/environment decision only the user can supply.
