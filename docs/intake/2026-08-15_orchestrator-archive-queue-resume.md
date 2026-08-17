# 2026-08-15 m-orchestrator Project-scoped Archive Queue Resume

## Source

- Date: 2026-08-15
- Source: Codex chat
- Requester: User

## Request Text / Source-preserving Summary

The user asked for a concurrency review of `$m-archive`, then clarified the required scheduling behavior:

- when one archive Task owns the integration lock, later archive Tasks in the same project must wait rather than fail;
- after the owner finishes normally, the waiting archive Task must continue automatically;
- the skill and runtime may operate on both Windows and Linux;
- archive/integration is serialized within one project, while independent projects remain parallel and do not contend with each other.

The review also reproduced two concrete runtime issues:

- a manifest-backed Task whose worktree changed after `TEST_PASSED` could still acquire the merge lease and enter `ARCHIVING`;
- merge/archive acquisition incorrectly acquired the optional machine-level host lease configured for Tester capacity.

## Context

The existing orchestrator already has a project-local capacity-one merge pool, durable FIFO tickets, leases, heartbeats, explicit stale recovery, and isolated runtime roots. The missing behavior is safe continuation and archive-specific eligibility enforcement around that existing project-scoped pool.

The confirmed design does not introduce a machine-wide archive lock. Project identity remains the scheduling and isolation boundary. A configuration that shares a writable control-plane repository, target base branch, or docs root across nominally separate projects is not considered conflict-free and is outside the independent-project assumption.

## Confirmed Requirements

- Keep archive/integration capacity at one per project.
- Preserve FIFO order for Tasks waiting in `WAITING_FOR_MERGE`.
- Treat normal lock contention as waiting, not `BLOCKED`.
- After normal release, expose and wake the next eligible Task in the same project.
- Preserve a durable queue so a lost wakeup can be recovered from project status.
- Revalidate the tested change and repository base state before archive admission.
- Return drifted Tasks to execution/validation without consuming an archive lease.
- Do not acquire or hold the optional Tester host budget for archive/integration.
- Keep stale or partially completed archive recovery explicit; do not silently pass integration capacity to unrelated queued work when project recovery is unresolved.
- Use Python standard-library and filesystem behavior that is portable across local Windows and Linux environments.
- Preserve schema version 1 compatibility, schema version 2 project isolation, existing phase ownership, and standalone `$m-archive` behavior outside orchestrated admission.

## Non-goals

- Machine-wide archive serialization.
- Cross-project archive wakeups or shared archive capacity.
- Remote or multi-machine scheduling over NFS/SMB.
- Replacing `$m-archive` as the archive, merge, and cleanup authority.
- Adding deployment, publication, push, or remote-management behavior.

## Open Questions

- None blocking. Actual Linux execution evidence depends on an available Linux runner; the implementation must remain platform-neutral and include cross-process tests that can run unchanged on both operating systems.

## Routed Docs

- [Project orchestrator feature](../features/m-project-orchestrator.md)
- [Project orchestrator requirements](../requirements/m-project-orchestrator.md)
- [Project orchestrator specification](../specs/m-project-orchestrator.md)
- [Original project orchestrator decision](../decisions/2026-07-31_project-orchestrator.md)
- [Multi-repository runtime decision](../decisions/2026-08-04_orchestrator-multi-repo-runtime.md)
- [Lease recovery lesson](../lessons/orchestrator-lease-recovery.md)
- [Archived workflow plan](../plan/2026-08-15_orchestrator-archive-queue-resume.md)

## Related Changes

- [2026-08-17_orchestrator-archive-queue-resume.md](../change/2026-08-17_orchestrator-archive-queue-resume.md)
