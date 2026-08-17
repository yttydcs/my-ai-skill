# Testing Pool Contract

## Pool Meaning

A pool limits concurrent temporary role executions. It does not represent reusable Tester identities or shared project environments.

Every project owns independent queues and leases. An optional host budget limits aggregate temporary Tester consumption across projects without sharing their context or commands. Archive/integration pools never acquire host capacity.

A Tester lease belongs to one Task, not one repository. For a multi-repository Task, the temporary Tester receives the exact persisted repository/worktree set and validates the affected cross-repository flow while holding one project permit (and one optional host permit).

## FIFO Admission

- Enqueue one ticket per project, pool, and Task.
- Repeated enqueue for the same waiting Task is idempotent.
- Sort tickets by durable creation time and opaque ticket ID.
- Only the head eligible Task may acquire a project slot.
- Revalidate a manifest-backed Task's composite change identifier before enqueue and again before acquisition. Repository drift keeps the Task in Worker execution and must not consume Tester capacity.
- Do not remove a ticket until all required project and host capacity is acquired and the lease record is durable.

## Lease Ownership

Each lease records only:

- project ID
- pool name
- Task ID
- opaque lease ID
- optional host lease ID
- acquired and heartbeat timestamps
- configured expiry threshold

Heartbeat, release, and reclaim require the exact Task and runtime-generated lease IDs. Wrong-owner operations fail. Malformed lease IDs also fail. Repeated release by the same owner is idempotent and cannot affect another Task.

## Acquisition Ordering

Use one consistent order:

1. lock the project pool;
2. confirm queue head, Task eligibility, and project capacity;
3. acquire optional host capacity;
4. write the project lease;
5. remove the queue ticket;
6. unlock the project pool.

If any step after host acquisition fails, release the host lease before returning. Never keep partial capacity while reporting `Waiting` or `Failed`.

For archive/integration pools, omit step 3 entirely. Before steps 4-5, persist a project-local operation record; then write the lease, compare-and-set the Task to `ARCHIVING`, remove the ticket, and complete the operation. A later pool mutation reconciles an interrupted operation before new admission and revalidates the archive candidate again before completing a partial acquisition. Capacity one is enforced only inside that project's runtime root, so independent projects can hold archive leases concurrently.

## Release

Persist the Tester result or blocker by transitioning `TESTING` to `TEST_FAILED`, `TEST_PASSED`, or `BLOCKED` before release. Then release the optional host lease and project lease in an owner-safe retryable operation. Only after capacity is released may the Worker enter `EXECUTING`, `WAITING_FOR_MERGE`, or another non-testing state. A missing already-released lease may return `Released` only when no current lease exists for another owner.

## Stale Leases

Expiry is a diagnostic threshold, not automatic proof that a Tester is dead. List stale project and host candidates with their owner and last heartbeat. The Planner or owning Worker must inspect live task status before explicit reclaim through `pool reclaim`, supplying the exact lease ID, actor, and reason. Reclaim of a lease paired with an active Task transitions that Task to `BLOCKED`, releases capacity, and writes a project-local audit event. A stale project lease left before Task acquisition is recorded as an orphan admission, removed without blocking the still-waiting Task, and remains retryable and audited.

If a process stopped after host admission but before the project lease was durable, `pool stale` reports the host-only orphan for either the Tester or legacy archive owner. `pool reclaim-host` may release it only when the Task is still in that pool's waiting state and owns no project lease. The command requires the exact host lease ID, actor, and reason, writes an audit event, and leaves the Task queued for a normal retry.

Pool implementation locks carry an owner token, process ID, and heartbeat. A contender waits for normal release and may recover an expired internal lock only after the recorded process is confirmed exited; elapsed time alone never authorizes stealing a live lock. This uses portable directory metadata plus safe process-liveness checks on Windows and Linux, not platform-specific file-lock APIs. Internal locks must not be confused with Tester leases.

## Waiting Behavior

Acquisition is non-blocking. A waiting Worker may retry after a bounded interval and report meaningful progress, but it must not hold a permit, busy-loop, or prevent the Planner from accepting new conversation.

For a normal completed archive release, return `next_ready` for the eligible same-project queue head and its persisted Worker callback. Project status returns the same value so the Planner can recover a missed wakeup. The callback is a retry hint, not a lease. Explicit archive reclaim or partial integration creates a project-local recovery hold; unrelated queued Tasks remain waiting until the affected owner is deliberately resumed.
