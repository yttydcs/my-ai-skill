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
WAITING_FOR_MERGE -> EXECUTING (archive candidate needs revalidation)
```

Any non-terminal state may enter `BLOCKED` with evidence. Leaving `BLOCKED` requires the exact prior state or approved resume target plus a recorded resolution. Resuming an interrupted archive owner to `WAITING_FOR_MERGE` preserves its prior validated archive candidate; enqueue/acquisition revalidates that candidate and returns drift to `EXECUTING` instead of recapturing untested state. `COMPLETED` is terminal.

## Evidence Invariants

- `WAITING_FOR_TESTER` requires a passing gate file and a non-empty change identifier.
- A manifest-backed Task gate must cover exactly every selected repository and its change identifier must match the current composite worktree-set snapshot. Any repository or plan drift makes Tester enqueue/acquisition ineligible.
- `TESTING` requires an active project Tester lease for the same Task.
- `TEST_FAILED` and `TEST_PASSED` require a persisted `$m-test` result.
- `WAITING_FOR_MERGE` requires `TEST_PASSED` or a separately recorded justified heavy-test skip allowed by the existing workflow.
- A manifest-backed `WAITING_FOR_MERGE` Task records its validated composite change identifier and selected repository base heads. Missing or drifted candidate data returns it to `EXECUTING` without an archive lease.
- `ARCHIVING` requires an active capacity-one integration lease.
- `COMPLETED` requires `$m-archive` completion evidence.
- Multi-repository archive evidence must record an ordered result for every selected repository. A partial integration enters `BLOCKED`; it is not `COMPLETED`.

The runtime stores evidence paths, hashes, statuses, timestamps, and opaque identifiers. It never copies evidence bodies or loaded contexts into Task state. Project-local archive operation records make the Task/lease/ticket mutations retryable after process interruption; reconciliation cannot bypass archive-candidate revalidation.

Ordinary archive capacity/FIFO contention stays `WAITING_FOR_MERGE`; `BLOCKED` is reserved for explicit recovery or external handoff. Archive recovery holds prevent unrelated queue progress after stale ownership or partial integration.

## Compare-and-set

Every transition names the expected current state. A mismatch fails instead of overwriting newer Worker or Tester progress. Task mutation uses a project-local metadata lock and atomic file replacement.
