# 2026-07-31 Project Orchestrator

## Source

- Date: 2026-07-31
- Source: Codex chat
- Requester: User

## Original Request Summary

The user wants one persistent Planner session per project. After a task is discussed and planned, the Planner should dispatch its implementation to a temporary background Worker and immediately remain available to plan the next task.

The automation layer must assist the existing `m-*` skills rather than replace their phase behavior:

- Planner work continues to use `$m-discuss` and `$m-plan`.
- Each temporary Worker uses `$m-execute`, including syntax, type, lint, formatting, focused unit, and diff validation that applies to the change.
- A Worker may enter heavyweight testing only after the execution-stage lightweight gate passes.
- Heavy testing is performed by temporary Testers admitted through a bounded Tester Pool rather than by one permanent Tester.
- Failed heavy testing returns a structured report to the owning Worker, which repairs through `$m-execute`, reruns the lightweight gate, and queues again.
- Successful heavy testing proceeds to `$m-archive` and a serialized integration/merge path.

## Project Isolation

- Every project has its own Planner identity, Task queue, Worker records, Tester Pool, merge queue, role contexts, test environment namespace, and runtime state.
- Project identity must remain stable across the project's worktrees.
- Runtime state must be shared by worktrees of the same project but isolated from other projects on the same machine.
- A machine-level resource budget may limit aggregate resource consumption, but it must contain no project commands, credentials, environment knowledge, or task state.

## Configuration And Context

- Each orchestrated command maps explicitly to an existing skill and zero or more contexts.
- Project role contexts use existing `$m-context` local storage under `<docs_root>/context`, such as `planner.md`, `worker.md`, `tester.md`, and `archive.md`.
- Project-specific automation must use explicit `local:` context selection and must not silently fall back to a global context.
- Machine-readable concurrency, routing, lease, and timeout settings belong in a validated project configuration rather than being parsed from Markdown.
- Context contents may include environment-specific facts or secrets but must not be copied into plans, reports, archives, or user-facing output unless explicitly needed.

## Non-goals

- Do not replace or weaken `$m-plan`, `$m-execute`, `$m-test`, or `$m-archive` contracts.
- Do not turn `$m-go` into the default Worker execution path.
- Do not reuse one permanent Tester session across unrelated tasks or projects.
- Do not share project test environments merely because projects run on the same machine.
- Do not hold a Tester permit while a Worker is repairing code or merely waiting in the queue.

## Open Questions

- None blocking. Pool capacities, lease timeouts, context names, and environment commands are project configuration values rather than architecture decisions.

## Stable Docs Impact

- Feature impact: add a dedicated project-orchestrator feature and link it from the autoflow workflow.
- Requirements impact: add durable project-orchestrator requirements and clarify autoflow routing.
- Specs impact: add the configuration, state, lease, dispatch, and isolation contracts.
- Decision impact: add the project-scoped orchestration architecture decision.
- Lessons impact: none known at planning time.

## Routed Docs

- [Decision](../decisions/2026-07-31_project-orchestrator.md)
- [Workflow feature](../features/m-autoflow-workflow.md)
- Planned feature: `docs/features/m-project-orchestrator.md`
- Planned requirements: `docs/requirements/m-project-orchestrator.md`
- Planned spec: `docs/specs/m-project-orchestrator.md`
