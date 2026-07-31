# Task State Machine

## States

| State | Meaning |
| --- | --- |
| `PLANNED` | approved plan persisted; no Worker recorded yet |
| `DISPATCHING` | background Worker creation is in progress |
| `EXECUTING` | Worker is implementing or running the lightweight gate |
| `EXECUTE_GATE_FAILED` | at least one applicable lightweight check failed |
| `WAITING_FOR_TESTER` | current change has a passing gate and is queued |
| `TESTING` | a valid Tester lease is active |
| `TEST_FAILED` | heavyweight validation failed and its result is persisted |
| `TEST_PASSED` | heavyweight validation passed and its result is persisted |
| `WAITING_FOR_MERGE` | task is queued for capacity-one archive/integration admission |
| `ARCHIVING` | integration permit is active and `$m-archive` owns closeout |
| `COMPLETED` | archive and required closeout completed |
| `BLOCKED` | progress requires an explicit external or user handoff |

## Allowed Normal Transitions

```text
PLANNED -> DISPATCHING -> EXECUTING
EXECUTING -> EXECUTE_GATE_FAILED -> EXECUTING
EXECUTING -> WAITING_FOR_TESTER -> TESTING
TESTING -> TEST_FAILED -> EXECUTING
TESTING -> TEST_PASSED -> WAITING_FOR_MERGE
WAITING_FOR_MERGE -> ARCHIVING -> COMPLETED
```

Any non-terminal state may enter `BLOCKED` with evidence. Leaving `BLOCKED` requires the exact prior state or approved resume target plus a recorded resolution. `COMPLETED` is terminal.

## Evidence Invariants

- `WAITING_FOR_TESTER` requires a passing gate file and a non-empty change identifier.
- `TESTING` requires an active project Tester lease for the same Task.
- `TEST_FAILED` and `TEST_PASSED` require a persisted `$m-test` result.
- `WAITING_FOR_MERGE` requires `TEST_PASSED` or a separately recorded justified heavy-test skip allowed by the existing workflow.
- `ARCHIVING` requires an active capacity-one integration lease.
- `COMPLETED` requires `$m-archive` completion evidence.

The runtime stores evidence paths, hashes, statuses, timestamps, and opaque identifiers. It never copies evidence bodies or loaded contexts into Task state.

## Compare-and-set

Every transition names the expected current state. A mismatch fails instead of overwriting newer Worker or Tester progress. Task mutation uses a project-local metadata lock and atomic file replacement.
