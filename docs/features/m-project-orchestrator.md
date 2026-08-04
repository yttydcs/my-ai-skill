# m:orchestrator Project Automation

## Status

Active.

## Feature Goal

Let one persistent Planner task per project continue discussing and planning while approved task workflows execute in isolated background Workers, pass an execution-stage quality gate, use bounded temporary Testers, and enter serialized archive/integration.

## Actors

- User: approves plans, project configuration, environment authority, and scope expansion.
- Project Planner: owns discussion, architecture, Task dispatch, status synthesis, and integration decisions.
- Temporary Worker: owns one approved plan and its exact participating repository/worktree set and invokes `$m-execute`.
- Temporary Tester: validates one eligible aggregate change through `$m-test` while holding a project Tester permit.
- Archive integrator: invokes `$m-archive` after capacity-one integration admission.

## Entry Point

```text
$m-orchestrator
```

The project supplies `.codex/m-orchestrator.toml`. Schema version 1 supports a compatible single Git-root project. Schema version 2 supports a non-Git umbrella root with an explicit catalog of child Git repositories and per-repository base branches. Role knowledge is loaded through explicit local `$m-context` files such as `planner`, `worker`, `tester`, and `archive` under the selected docs root.

## User Workflow

1. The project Planner uses `$m-discuss` and `$m-plan` with configured Planner context.
2. After exact Task approval, it persists a Task manifest, prepares one branch/worktree/root plan per participating repository, creates a background project Worker from those committed planning states, and returns immediately to conversation.
3. The Worker loads project context and runs `$m-execute`.
4. Failed syntax, compile, type, lint, format, focused unit, conflict, import, or diff checks in any participating repository remain in execution and never consume Tester capacity.
5. A passing aggregate change enters the project FIFO Tester queue with per-repository gate evidence bound to a composite change identifier.
6. A temporary Tester loads the project's local Tester context and runs `$m-test` while holding project and optional host permits.
7. Test failure releases permits and returns structured evidence to the Worker for repair and full gate rerun.
8. Test success releases Tester capacity and enters the capacity-one archive/integration queue.
9. `$m-archive` remains responsible for archive, merge, and cleanup behavior.

## Project Isolation

- Each project has a stable `project_id`, Planner registration, Task records, Worker mappings, queues, leases, environment namespace, contexts, and integration state.
- Schema version 2 runtime state is bound to the canonical umbrella root and `project_id`, independently of any one child repository. Schema version 1 retains Git-common-directory identity for compatibility.
- Different logical projects inside one umbrella or repository require different IDs and environment namespaces.
- Tasks select only configured repositories; ordinary validation and status never recursively scan or silently adopt child repositories.
- A machine-level host budget shares only numeric capacity and opaque lease ownership. It never stores project commands, secrets, plans, diffs, or test results.

## Configuration And Context

- Machine-readable routing, pool, timeout, and namespace settings live in `.codex/m-orchestrator.toml`.
- Project knowledge lives in `<docs_root>/context/*.md` and is loaded through `$m-context`.
- Configured contexts use explicit `local:` scope. Missing local context blocks the dependent action rather than falling back globally.
- Context bodies are not copied into runtime state, plans, reports, archives, screenshots, or user-facing summaries.

## Status And Error States

- Invalid config: block before Planner registration or Task creation.
- Missing host task tools: block background dispatch; never implement silently in the Planner.
- Lightweight gate failed: remain in Worker execution.
- Waiting for Tester: keep a FIFO ticket without holding capacity.
- Stale Tester lease: report owner and heartbeat; inspect the Worker before explicit recovery.
- New scope or authority: block and return to the Planner/user.
- Integration drift: reconcile with the latest base and rerun affected validation before archive.
- Partial multi-repository integration: stop, preserve recovery worktrees, and report completed and pending repositories; independent Git merges are not atomic.

## Acceptance Scenarios

### Planner Remains Available

Given an approved Task is dispatchable, when the Planner creates its background Worker, then the Worker ID is persisted and the Planner returns without waiting for implementation completion.

### Reject Broken Work Before Tester

Given an applicable execution-stage check fails, when the Worker evaluates Tester admission, then no queue ticket or Tester lease is created and the Worker repairs through `$m-execute`.

### Bound Tester Concurrency

Given more eligible Tasks than the configured capacity, when they request Tester admission concurrently, then capacity is not exceeded and remaining Tasks wait in FIFO order without permits.

### Keep Projects Separate

Given two configured projects on one machine, when both run Workers and Testers, then their contexts, environments, Task records, queues, and project leases remain separate even if an optional host budget limits aggregate concurrency.

### Support A Non-Git Umbrella

Given a schema version 2 project root that is not Git and declares multiple valid child repositories, when configuration is validated and its Planner is registered, then orchestration succeeds without inspecting or initializing Git at the umbrella root.

### Invalidate Aggregate Gate On Any Repository Drift

Given a Task whose lightweight gate covers several repositories, when any participating worktree or root plan changes, then Tester enqueue or acquisition rejects the stale composite identifier and returns the Task to execution.

### Repair And Requeue

Given `$m-test` fails, when the result is persisted, then all Tester permits are released before `$m-execute` repairs the Task, and the repaired change must pass a new gate before requeue.

## Related Intake

- [2026-08-04_orchestrator-multi-repo.md](../intake/2026-08-04_orchestrator-multi-repo.md)
- [2026-07-31_project-orchestrator.md](../intake/2026-07-31_project-orchestrator.md)

## Related Requirements

- [m-project-orchestrator.md](../requirements/m-project-orchestrator.md)

## Related Specs

- [m-project-orchestrator.md](../specs/m-project-orchestrator.md)

## Related Decisions

- [2026-08-04_orchestrator-multi-repo-runtime.md](../decisions/2026-08-04_orchestrator-multi-repo-runtime.md)
- [2026-07-31_project-orchestrator.md](../decisions/2026-07-31_project-orchestrator.md)

## Related Changes

- [2026-08-04_orchestrator-multi-repo.md](../change/2026-08-04_orchestrator-multi-repo.md)
- [2026-07-31_project-orchestrator.md](../change/2026-07-31_project-orchestrator.md)

## Related Lessons

- [orchestrator-multi-repository-runtime-boundaries.md](../lessons/orchestrator-multi-repository-runtime-boundaries.md)
- [orchestrator-lease-recovery.md](../lessons/orchestrator-lease-recovery.md)
