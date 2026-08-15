# Project-scoped Archive Resume

## Status

Accepted on 2026-08-15.

## Context

The orchestrator already has a capacity-one integration pool per project, but normal release did not expose the next waiting Worker, merge acquisition did not revalidate post-test worktree/base drift, and archive acquisition consumed the optional machine Tester budget. A global archive lock would fix same-project overlap by unnecessarily serializing independent projects.

## Options Considered

1. Add one machine-wide archive lock.
2. Add locks keyed by physical repositories or docs roots.
3. Strengthen the existing project-local integration pool with durable candidates, readiness, and explicit recovery holds.

## Decision

Use option 3. Each project keeps a FIFO, capacity-one integration queue. Ordinary contention remains `WAITING_FOR_MERGE`. A normal completed release and project status expose the next eligible same-project Worker callback; the host wakeup is advisory and the Worker must retry acquisition.

Manifest-backed Tasks persist a validated archive candidate containing the composite worktree identifier and configured repository base heads. Enqueue and acquisition revalidate it under the project-pool metadata lock. Drift returns the Task to execution and consumes no lease. Archive admission never acquires the optional Tester host budget.

Stale ownership or partial integration remains explicit recovery. A project-local recovery hold prevents unrelated Tasks from being advertised or admitted until the affected owner is deliberately resumed. The runtime uses only short metadata-directory locks, atomic JSON replacement, Git subprocesses, and standard-library facilities shared by Windows and Linux.

## Consequences

- Same-project archives serialize and can continue through their existing Workers after normal release.
- Independent projects can archive concurrently.
- Lost wakeups are recoverable from project status.
- Base or worktree drift cannot use stale validation to enter archive.
- There is no remote or multi-machine coordination guarantee.

## Related Docs

- [Intake](../intake/2026-08-15_orchestrator-archive-queue-resume.md)
- [Feature](../features/m-project-orchestrator.md)
- [Requirements](../requirements/m-project-orchestrator.md)
- [Specification](../specs/m-project-orchestrator.md)
- [Plan](../../plan.md)
