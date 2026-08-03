# m:orchestrator Project Automation

## Background

The staged `m-*` workflow automates one task well but requires manual management when a user wants to plan the next task while prior approved work continues. Expensive heavyweight testing also needs bounded concurrency without sharing project environments or long-lived Tester context.

## Goal

Provide a project-scoped automation companion that coordinates persistent planning, temporary background execution, execution quality gates, bounded temporary testing, repair loops, and serialized archive admission while reusing existing phase skills.

## Must

- keep one registered Planner task per configured project;
- dispatch approved work to temporary background project Workers;
- keep the Planner available after dispatch;
- use `$m-execute` as the normal Worker implementation authority;
- require a passing current lightweight gate before Tester admission;
- use temporary Testers invoking `$m-test` rather than permanent reusable Tester identities;
- enforce configurable per-project FIFO Tester capacity;
- release permits before repair, archive, blocking waits, or unrelated work;
- return failed Tester evidence to the owning Worker for execute repair and complete gate rerun;
- serialize project archive/integration admission at capacity one;
- use `$m-archive` as the archive, merge, and cleanup authority;
- support a non-Git umbrella project root with one or more explicitly declared Git implementation repositories;
- keep per-repository IDs, paths, base branches, Task branches, worktrees, planning refs, plans, and write sets explicit;
- isolate schema version 2 projects by canonical umbrella root plus stable `project_id`, while preserving schema version 1 Git-common-directory compatibility;
- map every command to its existing skill and explicit local contexts;
- fail explicitly for missing required context, invalid config, unavailable host task tools, wrong lease ownership, or invalid state transitions;
- preserve existing `m-*` behavior and backward compatibility;
- support an optional machine-level numeric resource ceiling without project knowledge.

## Should

- make enqueue, release, registration, and status operations safely retryable;
- provide non-blocking acquisition and compact project status output;
- detect stale leases without silently reclaiming them;
- keep runtime metadata free of context bodies, credentials, plans, diffs, and test output;
- use standard-library runtime dependencies only.

## Out Of Scope

- remote or multi-machine task scheduling;
- graphical dashboards;
- test-environment provisioning engines;
- CI replacement;
- secret encryption or vault management;
- automatic publication, deployment, push, or remote creation;
- sharing one project test environment with another project.

## Functional Requirements

- Configuration validation must occur before runtime mutation.
- Planner registration must prevent silent replacement of a live Planner.
- Worker dispatch must persist exact project, plan, Task, Worktree/ref, context, acceptance, test, rollback, and callback data.
- A multi-repository Task must persist a non-empty exact subset of configured repositories and reject undeclared, duplicate, aliased, traversal, or out-of-project repository/worktree paths.
- A composite change identifier must cover every selected repository's commit, tracked diff, untracked content, and root plan; drift in any selected repository must invalidate Tester admission.
- Task transitions must use expected-state compare-and-set semantics.
- `WAITING_FOR_TESTER` must require passing gate evidence and a non-empty change identifier.
- Tester acquisition must require an eligible queue-head Task and must never exceed project or enabled host capacity.
- Lease heartbeat and release must require exact Task and lease ownership.
- Repeated enqueue and same-owner release must be idempotent.
- Stale lease listing must not reclaim automatically.
- Integration admission must use a configured capacity-one pool.
- Base reconciliation that changes executable content must invalidate earlier validation as appropriate.
- Multi-repository integration must preflight every selected repository, use recorded dependency order, and report partial completion as blocked rather than atomic success.

## Non-functional Requirements

- Project status and pool inspection must scale with the selected project's entries rather than scanning unrelated repositories.
- Configuration validation and status must inspect only declared repositories and must not recursively discover project repositories.
- Runtime mutations must use atomic filesystem operations and explicit error messages.
- The system must avoid busy waits and long silent blocking calls.
- Config, state, and evidence boundaries must be deterministic and testable on Windows.
- Context selection must be explicit and must not silently fall back from local project data to global data.
- The skill package must remain concise and route detailed contracts to direct references.

## Acceptance Criteria

- Concurrent tests prove project capacity is never exceeded and FIFO order is preserved.
- Two project IDs in one repository resolve to different runtime roots.
- Separate repositories with the same project ID remain isolated.
- A non-Git umbrella with multiple declared child repositories validates and registers a Planner even when the umbrella contains an empty `.git` directory.
- Existing schema version 1 single-repository projects keep their current runtime roots and Task creation interface.
- A schema version 1 non-Git umbrella receives a schema version 2 migration error and is never instructed to initialize Git at the umbrella root.
- Invalid config, path traversal, context scope, ownership, and state transitions fail explicitly.
- A Worker without a current passing gate cannot enqueue or acquire the Tester pool.
- Failure releases project and host capacity before repair.
- Existing workflow contract tests continue passing.
- Source, distribution, and installed package copies match after validation and sync.

## Related Features

- [m-project-orchestrator.md](../features/m-project-orchestrator.md)
- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Specs

- [m-project-orchestrator.md](../specs/m-project-orchestrator.md)

## Related Decisions

- [2026-08-04_orchestrator-multi-repo-runtime.md](../decisions/2026-08-04_orchestrator-multi-repo-runtime.md)
- [2026-07-31_project-orchestrator.md](../decisions/2026-07-31_project-orchestrator.md)

## Related Changes

- [2026-07-31_project-orchestrator.md](../change/2026-07-31_project-orchestrator.md)

## Related Lessons

- [orchestrator-lease-recovery.md](../lessons/orchestrator-lease-recovery.md)
