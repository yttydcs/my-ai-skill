# m:pipeline Role Automation

## Status

Implemented and installed as optional companion version 0.1.0 on 2026-09-06. Two disposable real-host pipelines completed planning through local release and original archive closeout. The [active plan](../../plan.md) records validation, evidence and capability limits. Existing manual skill behavior remains unchanged.

## Feature Goal

Let the user define a reusable team and pipeline, interact primarily with a product-manager session, and launch bounded automatic planning, execution, testing, archive, and optional deployment across multiple workflow runs.

## Role And Session Model

| Role | Phase authority | Result |
| --- | --- | --- |
| Product manager | `m-discuss` | Confirmed brief, unresolved business questions, launch scope |
| Architect | `m-plan` | Requirements/architecture analysis and worktree-root plans |
| Executor | `m-execute` | Task implementation and lightweight validation |
| Tester | `m-test` | Acceptance evidence and pass/fail/blocked/skip result |
| Release owner | `m-archive` and a separately configured release procedure if authorized | Archive, integration, cleanup, and optional deployment evidence |
| Workflow coordinator | New `m-pipeline` behavior | Dispatch, waiting, reconciliation, aggregation, and user status |

Roles describe responsibilities. A role can have several explicitly bound or automatically created sessions. Every workflow has one active coordinator owner. Phase sessions are independent user-visible tasks; in-phase subagents remain subject to the original phase and host policies.

## User Journey

1. Define a pipeline with project/docs/repository locations, roles, contexts, session bindings or creation policies, routing, and limits.
2. Create the configured team or bind selected existing sessions. Return the actual session references and initialization results; resume partial initialization without blindly duplicating sessions.
3. Discuss a requirement with the product manager using the original `m-discuss`.
4. Explicitly launch a run with the confirmed brief and a bounded authorization contract. Starting this implementation plan does not authorize a customer run.
5. The coordinator requests architecture through `m-plan`, validates the resulting plan against the launch contract, and dispatches only admitted Task IDs.
6. Select an eligible idle executor, create another within configured limits, or wait. Distinct independent tasks can fan out; the same task is never broadcast as multiple independent assignments.
7. Collect and integrate required execution outputs into an exact candidate before overall `m-test` acceptance. Failures return to the appropriate execution or planning owner.
8. After verified acceptance, the release role invokes `m-archive` and any separately authorized deployment procedure. Configuration defines their order according to the deployment's worktree or durable-artifact needs; deployment acts on the recorded tested version.
9. Report the overall result with plan and evidence references. Business decisions or expanded authority return to the product-manager entry rather than generating unrelated questions from every role.

## Context And Documents

- Initialization resolves `docs_root` through existing project and `m-docs` rules.
- Receivers load the configured exact context names/sections through the original `m-context`; pipeline configuration defaults to explicit project-local references.
- Phase-owned documentation work stays with the original phases. The outer coordinator does not surround every phase with duplicate `m-docs` calls.
- Pipeline setup or its own governed-document work may invoke `m-docs` directly.
- Runtime records contain references and receipts, not a second requirements specification, second task plan, context bodies, or credentials.
- Documentation is complete enough to restart a receiver, while reads are restricted to the assigned phase and task.

## Concurrency And Recovery

The coordinator waits without occupying downstream role capacity. Shared sessions process one admitted assignment at a time. Explicit shared resources, such as a release environment or integration branch, also require exclusive admission when configured; different session IDs alone do not prevent conflicting operations.

The current desktop thread tools provide observation and dispatch, not a transactional claim. Local assignment records coordinate cooperating pipelines. Manual work remains user-controlled; pause/takeover reconciles active work before an automation claim can be released.

If delivery or creation has an unknown outcome, preserve that state and reconcile actual host evidence before retrying. A timeout never grants a second owner. A fresh receiver continues from the original plan and exact repository state, with one current task owner.

## Acceptance Scenarios

- Manual and automatic use: the original `m-plan` through `m-archive` still run independently; a paused run can be continued manually and later re-adopted with verified evidence.
- Two workflows: both target a shared tester; only one assignment is admitted, the other waits, and work resumes after a verified release.
- Fan-out/join: independent Task IDs run in isolated write sets; partial branch completion cannot start full release.
- Repair: a failing integrated acceptance returns bounded work for repair and retests the changed candidate.
- Fresh context: a new receiver completes a task from document/context references and a handoff receipt without relying on full copied conversation history.
- Initialization interruption: a partially created team is reconciled by persisted operation IDs and actual host identities; unknown creation is not blindly retried.
- Docs compatibility: phase-owned documentation is not written twice and context values do not enter reports or ordinary Git write sets.
- Release identity: the recorded tested/integrated candidate is checked before publication; drift returns to relevant validation.

## First-release Boundaries

Support one desktop host, local persistent state, explicit repositories including non-Git umbrellas, bounded role capacity, one level of execution children, and resume on an active/restarted coordinator. Unattended wakeup after closing the app, arbitrary recursive teams, native compaction integration, and real production deployment are separate scopes.

## Related Documents

- [Request](../intake/2026-09-06_role-pipeline.md)
- [Requirements](../requirements/m-pipeline.md)
- [Specification](../specs/m-pipeline.md)
- [Decision](../decisions/2026-09-06_role-pipeline-composition.md)
- [Existing workflow](m-autoflow-workflow.md)
- [Existing context behavior](m-context.md)
- [Active plan](../../plan.md)
