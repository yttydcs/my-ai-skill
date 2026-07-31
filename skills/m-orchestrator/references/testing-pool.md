# Testing Pool Contract

## Pool Meaning

A pool limits concurrent temporary role executions. It does not represent reusable Tester identities or shared project environments.

Every project owns independent queues and leases. An optional host budget limits aggregate numeric resource consumption across projects without sharing their context or commands.

## FIFO Admission

- Enqueue one ticket per project, pool, and Task.
- Repeated enqueue for the same waiting Task is idempotent.
- Sort tickets by durable creation time and opaque ticket ID.
- Only the head eligible Task may acquire a project slot.
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

## Release

Persist the Tester result or blocker by transitioning `TESTING` to `TEST_FAILED`, `TEST_PASSED`, or `BLOCKED` before release. Then release the optional host lease and project lease in an owner-safe retryable operation. Only after capacity is released may the Worker enter `EXECUTING`, `WAITING_FOR_MERGE`, or another non-testing state. A missing already-released lease may return `Released` only when no current lease exists for another owner.

## Stale Leases

Expiry is a diagnostic threshold, not automatic proof that a Tester is dead. List stale project and host candidates with their owner and last heartbeat. The Planner or owning Worker must inspect live task status before explicit reclaim through `pool reclaim`, supplying the exact lease ID, actor, and reason. Project reclaim rejects a fresh lease, transitions its Task to `BLOCKED`, releases host and project capacity, and writes a project-local audit event. It never resumes or expands the Task automatically.

If a process stopped after host admission but before the project lease was durable, `pool reclaim-host` may release that stale orphan only when the Task is still in the pool's waiting state and owns no project lease. The command requires the exact host lease ID, actor, and reason, writes an audit event, and leaves the Task queued for a normal retry.

Pool implementation locks may use a short internal stale threshold for crash recovery because they protect metadata operations only; they must not be confused with Tester leases.

## Waiting Behavior

Acquisition is non-blocking. A waiting Worker may retry after a bounded interval and report meaningful progress, but it must not hold a permit, busy-loop, or prevent the Planner from accepting new conversation.
