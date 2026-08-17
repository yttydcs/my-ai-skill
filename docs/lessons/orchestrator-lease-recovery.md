# Orchestrator Lease Recovery

## Summary

Filesystem-backed admission needs durable agreement between Task state, project leases, and optional host leases. Treat expiry as a diagnostic signal, require explicit audited reclaim, and make recovery itself resumable across process interruption.

## Lookup Hints

- Keywords: `stale lease`, `orphan host lease`, `pool reclaim`, `reclaim-host`, `active_lease`, `archive recovery hold`, `archive operation`, `owner heartbeat`, `next_ready`, `premature release`, `Started`, `Completed`.
- Quick checks: compare Task state with the exact project lease; inspect `pool stale`; check for a Tester or legacy archive host-only lease; inspect pending archive operations; verify the result transition preceded normal release; inspect `recovery_hold` and the project-local reclaim event.

## Symptoms

- A Task is in `TESTING` or `ARCHIVING` but its project lease is missing.
- A project lease still exists after the Task persisted `TEST_FAILED`, `TEST_PASSED`, or `BLOCKED`.
- Host capacity remains exhausted although no corresponding project lease exists.
- Retrying acquisition returns an old lease after its heartbeat expired or after the Task state advanced.
- Retrying recovery fails because the Task was blocked before the reclaim audit was completed.
- An `EXECUTING` Task leaves an old archive ticket at the FIFO head, or a waiting Task has a project lease without matching `active_lease`.
- Concurrent enqueue creates duplicate tickets after a long archive-candidate scan crosses the internal lock stale threshold.

## Impact

- Scarce Tester or integration capacity can remain unavailable.
- A stale owner can appear live, allowing conflicting work or misleading status.
- Manual repair may release the wrong owner or lose the reason and actor responsible for recovery.
- A queue head with inconsistent state can prevent otherwise eligible Tasks from progressing.
- An abnormal archive release can wake unrelated queued work into a partially integrated project unless readiness is held for explicit recovery.

## Trigger Conditions

- The process stops after host admission but before the project lease becomes durable.
- The process stops between archive operation, project lease, Task transition, and ticket deletion writes.
- An internal lock is reclaimed from elapsed directory age without proving that its owner exited.
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
7. Injected archive revalidation/acquisition interruptions and found stale queue heads and inconsistent pre-acquisition project leases could not converge.
8. Held a metadata lock past its stale threshold and found time-only recovery could admit two concurrent enqueue mutations.
9. Constructed a legacy archive host-only orphan and found merge inspection filtered it out because no project lease referenced its ID.

## Resolution

- Validate lease IDs against the exact generated UUID-hex format at the CLI boundary.
- Require Task state and `active_lease` to match an existing lease before treating acquisition as idempotent.
- Reject stale reuse and expose project and host stale candidates without automatic reclamation.
- Require result or blocker persistence before ordinary release.
- Provide explicit project reclaim and host-orphan reclaim with exact owner, actor, and reason.
- Block a reclaimed active Task, leave a host-orphan Task queued, and write project-local audit events.
- Use `Started` and `Completed` reclaim audit states so recovery can safely resume after interruption.
- Serialize host-pool metadata creation and validation with the same host lock used for admission.
- Restrict host leases to Tester pools; archive pools are already isolated by their project-local capacity-one lease.
- After normal archive completion, expose the next same-project queue head and persisted Worker callback as advisory readiness. After reclaim or partial integration, persist a recovery hold instead.
- Journal archive revalidation and acquisition before changing Task/lease/ticket records; reconcile the operation before later pool mutations and rerun candidate drift checks before completing acquisition.
- Keep a resumed `BLOCKED` archive owner's prior validated candidate instead of recapturing current worktree state as a skipped-test candidate.
- Treat a stale project lease with a still-waiting Task as an audited pre-acquisition orphan: remove it without creating an archive recovery hold, then retry normal admission.
- Include legacy archive host-only owners in merge stale inspection and block new archive acquisition until explicit host-orphan recovery.
- Heartbeat metadata-lock ownership and reclaim it only after safe Windows/Linux process-liveness confirmation; never use directory age alone to steal an active lock.

## Prevention / Guardrails

- Test normal, stale, inconsistent, wrong-owner, premature-release, and interrupted-recovery paths separately.
- Keep project-to-host lock ordering consistent to avoid deadlocks.
- Never infer that timeout proves an owner is dead; inspect the live Worker first.
- Do not silently reclaim capacity during status or acquisition calls.
- Keep recovery commands explicit and auditable, and make repeated calls owner-safe.
- Treat a wakeup as a retry hint rather than ownership; only a newly created project lease authorizes archive work.
- Bind every path-derived external identifier to a strict allowlist pattern before filesystem access.
- Fault-inject every durable boundary in multi-file state changes and verify that the next public mutation converges it without bypassing validation.

## Related Docs

- [Project orchestrator intake](../intake/2026-07-31_project-orchestrator.md)
- [Project orchestrator feature](../features/m-project-orchestrator.md)
- [Project orchestrator requirements](../requirements/m-project-orchestrator.md)
- [Project orchestrator specification](../specs/m-project-orchestrator.md)
- [Project orchestrator decision](../decisions/2026-07-31_project-orchestrator.md)
- [Project-scoped archive resume decision](../decisions/2026-08-15_project-scoped-archive-resume.md)
- [Project orchestrator change](../change/2026-07-31_project-orchestrator.md)
- [Project orchestrator plan](../plan/2026-07-31_project-orchestrator.md)
- [Multi-repository runtime change](../change/2026-08-04_orchestrator-multi-repo.md)
- [Multi-repository runtime boundary lesson](orchestrator-multi-repository-runtime-boundaries.md)
