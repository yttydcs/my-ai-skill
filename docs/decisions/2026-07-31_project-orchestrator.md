# 2026-07-31 Project-scoped m Orchestrator

## Status

Accepted and implemented.

## Context

The `m-*` family already owns disciplined discussion, planning, implementation, lightweight validation, heavy testing, continuation, and archive behavior. It does not currently provide a project-level control plane that lets one persistent Planner dispatch several independent task workflows in the background while bounding expensive Testers.

The desired automation must preserve the phase skills as the sources of truth, keep every project isolated, prevent obviously broken execution output from consuming scarce Tester capacity, and allow multiple projects to coexist on one machine.

## Options Considered

- Extend `$m-go` into the project-level orchestrator.
  - Rejected because `$m-go` requires delegated implementation edits and owns one confirmed plan's automatic execute/test loop. The requested Worker should normally use `$m-execute`, and the project Planner must manage several task workflows concurrently.
- Reuse a fixed set of permanent Tester sessions.
  - Rejected because long-lived Testers accumulate unrelated task context, bind awkwardly to worktrees, and increase the chance of cross-project environment leakage.
- Add a project-scoped companion orchestrator over the existing phase skills.
  - Accepted because it preserves phase ownership, supports a persistent Planner and temporary task roles, and localizes scheduling, isolation, context mapping, and resource admission.

## Decision

Add `$m-orchestrator` as a non-phase companion skill above the existing `m-autoflow` task workflow.

Each configured project owns one registered Planner session and any number of temporary background Worker tasks. Each Worker consumes an approved plan, runs `$m-execute`, and must produce a passing lightweight-gate record before it can queue for heavyweight testing.

Heavy testing uses temporary Tester agents scoped to the owning Worker worktree. A project-local FIFO Tester Pool limits how many Testers may run concurrently. The pool manages permits rather than reusable Tester identities. Test failure releases the permit and returns a structured report to the owning Worker. Repair work uses `$m-execute`, then reruns the complete lightweight gate before re-entry.

Each project has a stable `project_id`, explicit docs root, command-to-context mapping, environment namespace, runtime root, Task state, Tester queue, leases, and merge queue. Worktrees of the same project share runtime state through the repository common Git directory plus `project_id`. Different repositories are naturally isolated; distinct logical projects within one repository remain isolated by `project_id`.

Project-specific contexts must be selected explicitly from `<docs_root>/context` with `local:` scope. An absent configured local context blocks the dependent command instead of falling back globally. Machine-level state may enforce aggregate numeric resource budgets only; it must not contain project contexts, commands, secrets, environment details, or task state.

Final integration is serialized per project. A task waiting for integration must reconcile with the latest base and rerun the required validation when that reconciliation changes executable content. Archive, merge, and cleanup remain owned by `$m-archive`; the orchestrator controls admission and sequencing but does not redefine their behavior.

## Consequences

- The new skill needs deterministic configuration validation and a standard-library runtime helper for Task state, queue tickets, leases, heartbeats, status, and safe release.
- The runtime helper must use atomic filesystem operations and must not silently reclaim a stale lease without an explicit safety decision.
- The Planner must dispatch Worker tasks through available Codex project/thread tools and provide a self-contained context package. If those tools are unavailable, dispatch blocks rather than executing in the Planner session.
- `$m-autoflow` gains a routing reference to the new project-level companion, while the existing phase skills remain authoritative and backward compatible.
- Focused contract and runtime tests are required for project isolation, gate enforcement, FIFO admission, capacity, release, stale-lease reporting, and invalid configuration.

## Confidence

High for the skill and local runtime contracts. Live background-task creation still depends on the active Codex host exposing project/thread tools, so the skill must treat tool availability as an explicit runtime gate.

## Supersedes / Superseded By

- Supersedes: none.
- Superseded by: none.

## Related Intake

- [2026-07-31_project-orchestrator.md](../intake/2026-07-31_project-orchestrator.md)

## Related Features

- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)
- [m-project-orchestrator.md](../features/m-project-orchestrator.md)

## Related Requirements

- [m-project-orchestrator.md](../requirements/m-project-orchestrator.md)

## Related Specs

- [m-project-orchestrator.md](../specs/m-project-orchestrator.md)

## Related Change

- [2026-07-31_project-orchestrator.md](../change/2026-07-31_project-orchestrator.md)

## Related Lesson

- [orchestrator-lease-recovery.md](../lessons/orchestrator-lease-recovery.md)
