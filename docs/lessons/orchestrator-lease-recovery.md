# Orchestrator Lease Recovery

## Summary

Filesystem-backed admission needs durable agreement between Task state, project leases, and optional host leases. Treat expiry as a diagnostic signal, require explicit audited reclaim, and make recovery itself resumable across process interruption.

## Lookup Hints

- Keywords: `stale lease`, `orphan host lease`, `pool reclaim`, `reclaim-host`, `active_lease`, `not consistently TESTING`, `premature release`, `Started`, `Completed`.
- Quick checks: compare Task state with the exact project lease; inspect `pool stale`; check for a host-only lease; verify the result transition preceded normal release; inspect the project-local reclaim event.

## Symptoms

- A Task is in `TESTING` or `ARCHIVING` but its project lease is missing.
- A project lease still exists after the Task persisted `TEST_FAILED`, `TEST_PASSED`, or `BLOCKED`.
- Host capacity remains exhausted although no corresponding project lease exists.
- Retrying acquisition returns an old lease after its heartbeat expired or after the Task state advanced.
- Retrying recovery fails because the Task was blocked before the reclaim audit was completed.

## Impact

- Scarce Tester or integration capacity can remain unavailable.
- A stale owner can appear live, allowing conflicting work or misleading status.
- Manual repair may release the wrong owner or lose the reason and actor responsible for recovery.
- A queue head with inconsistent state can prevent otherwise eligible Tasks from progressing.

## Trigger Conditions

- The process stops after host admission but before the project lease becomes durable.
- Normal release is allowed before test/archive/blocker evidence is persisted.
- Idempotent acquisition checks only for an existing lease and ignores Task state or heartbeat age.
- Reclaim mutates Task and capacity before writing a durable recovery record.
- External lease IDs are interpolated into paths without strict validation.

## Root Cause

A lease file alone is not the full ownership state. Correct ownership is the conjunction of the configured pool, exact Task and lease IDs, Task state, `active_lease`, heartbeat freshness, and any paired host lease. Recovery that updates these records in an unsafe order can create a second inconsistent state even while fixing the first.

## Investigation Trail

1. Compared the state-machine contract with the runtime transition and found that leaving `BLOCKED` did not actually require a resolution.
2. Exercised repeated acquisition after result persistence and found the old lease was returned despite incompatible Task state.
3. Aged project and host heartbeats and found stale ownership could be reused rather than surfaced for inspection.
4. Reviewed first-use host-pool creation and found metadata validation outside the shared host lock.
5. Injected the host-acquired/project-not-durable crash boundary and identified an unreportable host-only orphan.
6. Reviewed reclaim ordering and found interruption between Task blocking and audit completion was not retry-safe.

## Resolution

- Validate lease IDs against the exact generated UUID-hex format at the CLI boundary.
- Require Task state and `active_lease` to match an existing lease before treating acquisition as idempotent.
- Reject stale reuse and expose project and host stale candidates without automatic reclamation.
- Require result or blocker persistence before ordinary release.
- Provide explicit project reclaim and host-orphan reclaim with exact owner, actor, and reason.
- Block a reclaimed active Task, leave a host-orphan Task queued, and write project-local audit events.
- Use `Started` and `Completed` reclaim audit states so recovery can safely resume after interruption.
- Serialize host-pool metadata creation and validation with the same host lock used for admission.

## Prevention / Guardrails

- Test normal, stale, inconsistent, wrong-owner, premature-release, and interrupted-recovery paths separately.
- Keep project-to-host lock ordering consistent to avoid deadlocks.
- Never infer that timeout proves an owner is dead; inspect the live Worker first.
- Do not silently reclaim capacity during status or acquisition calls.
- Keep recovery commands explicit and auditable, and make repeated calls owner-safe.
- Bind every path-derived external identifier to a strict allowlist pattern before filesystem access.

## Related Docs

- [Project orchestrator intake](../intake/2026-07-31_project-orchestrator.md)
- [Project orchestrator feature](../features/m-project-orchestrator.md)
- [Project orchestrator requirements](../requirements/m-project-orchestrator.md)
- [Project orchestrator specification](../specs/m-project-orchestrator.md)
- [Project orchestrator decision](../decisions/2026-07-31_project-orchestrator.md)
- [Project orchestrator change](../change/2026-07-31_project-orchestrator.md)
- [Project orchestrator plan](../plan/2026-07-31_project-orchestrator.md)
- [Multi-repository runtime change](../change/2026-08-04_orchestrator-multi-repo.md)
- [Multi-repository runtime boundary lesson](orchestrator-multi-repository-runtime-boundaries.md)
