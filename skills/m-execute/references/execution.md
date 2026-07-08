# Execution Rules

Use this reference for `$m-execute`, the implementation phase of `m-autoflow`.

## Phase Boundary

- Owns code, configuration, test fixture changes, and lightweight validation required by approved Task IDs.
- May update the active plan status for the touched tasks.
- Does not own plan creation, broad replanning, heavy integration testing, archive, merge, or worktree cleanup.

## Hard Rules

- Stay inside the active worktree.
- Map every changed file to a Task ID.
- Do not introduce plan-external behavior; return to planning if scope expands.
- Do not silently swallow errors.
- Do not revert user or other-agent changes unless explicitly requested.
- If a best-practice choice is uncertain, present options and ask before locking one in.

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

Run cheap, local checks in this phase when practical:

- syntax checks
- type checks
- lint checks scoped to touched files
- formatting checks scoped to touched files
- focused unit tests for changed logic
- `git diff --check`

Record any skipped lightweight check with the reason and residual risk. Reserve heavy integration, end-to-end, usability, security, and performance review for `$m-test`.
