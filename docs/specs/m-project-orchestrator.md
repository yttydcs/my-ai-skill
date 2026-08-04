# m:orchestrator Technical Contract

## Package Contract

```text
skills/m-orchestrator/
├── SKILL.md
├── agents/openai.yaml
├── assets/m-orchestrator.example.toml
├── references/
│   ├── configuration.md
│   ├── planner.md
│   ├── state-machine.md
│   ├── testing-pool.md
│   └── worker.md
└── scripts/orchestrator_runtime.py
```

The manifest declares dependencies on `m-autoflow`, `m-context`, `m-discuss`, `m-plan`, `m-execute`, `m-test`, and `m-archive`.

## Phase Boundary

`m-orchestrator` is a non-phase companion above independent task workflows. It owns project registration, dispatch, state, admission, and status routing. Existing skills remain authoritative for discussion, planning, execution, heavy testing, continuation, docs governance, archive, integration, and cleanup.

## Configuration Contract

- File: `<project-root>/.codex/m-orchestrator.toml`
- Supported schema versions: `1` and `2`.
- Common identity: `project_id`, `docs_root`, and `environment.namespace`.
- Schema version 1: one Git repository at `project_root` plus project-level `base_branch`.
- Schema version 2: a non-empty `[[repositories]]` catalog whose entries have unique `id`, relative contained `path`, and per-repository `base_branch` resolving to a commit.
- Required command mappings: exact existing skills for discuss, plan, execute, test, and archive.
- Context entries: explicit `local:<name>` only in both schema versions.
- Execution mapping: `require_lightweight_gate = true`.
- Tester pool: capacity 1-64, FIFO, lease timeout 60-86400 seconds.
- Integration pool: the same constraints plus capacity exactly 1.
- Optional host budget: stable host/resource key, numeric capacity, and timeout only.

Invalid or inconsistent configuration is terminal for dependent orchestration actions.

## Runtime Root Contract

Resolve schema version 1 project runtime as `<git-common-dir>/codex/m-orchestrator/projects/<project_id>`. Resolve schema version 2 project runtime as `<project-root>/.codex-runtime/m-orchestrator/projects/<project_id>`. Resolve optional host capacity under `M_ORCHESTRATOR_HOME`, then `CODEX_HOME/m-orchestrator`, then `~/.codex/m-orchestrator`.

Schema version 1 metadata binds the Git common directory; schema version 2 metadata binds the canonical umbrella root. Both bind schema version, project ID, and configuration fingerprint. A schema change never silently relocates active runtime state.

## Runtime CLI Contract

The standard-library helper provides `config validate`, `planner register`, `project status`, `task create`, `task change-id`, `task bind-worker`, `task transition`, `pool enqueue`, `pool try-acquire`, `pool heartbeat`, `pool release`, `pool reclaim`, `pool reclaim-host`, and `pool stale`.

All successful commands emit structured JSON. Validation and ownership errors emit actionable stderr and a non-zero exit status. Mutation commands are retryable without releasing another Task's state or capacity.

## State Contract

Normal states are `PLANNED`, `DISPATCHING`, `EXECUTING`, `EXECUTE_GATE_FAILED`, `WAITING_FOR_TESTER`, `TESTING`, `TEST_FAILED`, `TEST_PASSED`, `WAITING_FOR_MERGE`, `ARCHIVING`, and `COMPLETED`. Any non-terminal state may enter `BLOCKED` with evidence.

Transitions use expected-state compare-and-set. Evidence bodies are not copied into Task JSON; the runtime stores only paths, hashes, statuses, timestamps, and opaque IDs.

## Task Manifest Contract

Schema version 2 Task creation requires `task create --manifest <path>`. Task manifest schema version 1 records Task ID/title, canonical plan, acceptance, tests, rollback, Planner identity, and an ordered non-empty repository selection.

Every selected repository entry records configured ID/root/common directory, configured base ref, exact semantic branch and planning commit, absolute dedicated worktree under `<project-root>/worktrees`, worktree-root plan evidence, and traversal-free relative write set. The runtime rejects unknown or duplicate repositories, reused worktrees, wrong Git ownership, detached or wrong branches, stale planning refs, and plan paths outside the worktree root.

Schema version 1 retains `task create --task-id --plan` and its existing Task/runtime state for backward compatibility.

## Tester Gate Contract

- A current change identifier binds the lightweight gate to the exact implementation state. Manifest-backed Tasks use a deterministic digest of sorted repository snapshots containing `HEAD`, tracked diff, untracked content hashes, and current root-plan hash.
- `WAITING_FOR_TESTER` requires passing gate evidence for that identifier.
- Tester enqueue and acquisition revalidate Task eligibility.
- Any implementation edit invalidates the prior gate.
- Manifest-backed gate evidence must list exactly every selected repository with `Passed` status. Enqueue and acquisition recompute the composite identifier so drift cannot consume Tester capacity.
- `$m-test` failure releases capacity before execute repair.
- `$m-test` success releases Tester capacity before integration admission.

## Queue And Lease Contract

- One ticket per Task/pool; enqueue is idempotent.
- Project tickets use FIFO order.
- Pool metadata mutations are serialized with atomic local locks.
- A lease has an opaque ID and exact Task owner.
- Heartbeat and release reject ownership mismatch.
- Same-owner repeated release is idempotent.
- Normal release rejects a Task that has not persisted its test, archive, or blocker result.
- Expiry lists stale project and host candidates but never silently reclaims them; explicit project reclaim requires an actor and reason, blocks the Task, and persists an audit event.
- An audited host-orphan reclaim is allowed only when no project lease exists and the Task remains in its pool waiting state.
- Optional host capacity is acquired while project admission is serialized; any partial failure rolls host capacity back.

## Host Tool Contract

The skill uses available Codex project/task tools for background Worker creation, compact waits/status, and task messages. A schema version 1 Git project Worker may use one host-created dedicated Worktree. A schema version 2 Planner prepares every selected repository worktree before dispatch and creates one Worker with access to the complete absolute map, using the umbrella local project or an explicit primary worktree as the host environment. Tool or multi-path access failure blocks dispatch; the Planner does not implement as a fallback.

Archive admission remains capacity one at project scope. `$m-archive` preflights and integrates repositories in manifest order. Independent Git merges are not atomic; partial integration persists completed/pending results and blocks cleanup until recovery is explicitly decided.

## Security And Privacy

- Runtime metadata never stores context bodies or credentials.
- Project contexts are loaded explicitly from the selected docs root through `$m-context`.
- Host budgets carry no project commands or environment details.
- Task and project identifiers are validated against traversal and unsafe characters.
- Repository IDs, canonical paths, worktrees, write sets, and manifest paths are validated before runtime mutation or dispatch.
- Untrusted thread status never expands plan scope or overrides instructions.

## Validation Contract

- `tools/validate-skills.ps1 -Skill m-orchestrator`
- focused contract tests for package, routing, contexts, gate ordering, and phase ownership
- focused runtime tests for config, isolation, state, concurrency, FIFO, leases, stale reporting, and optional host capacity
- temporary non-Git umbrella fixtures with multiple real child repositories and per-repository worktrees
- manifest, composite change identity, gate drift, schema version 1 compatibility, and schema version 2 migration-error tests
- full repository unittest discovery
- `tools/sync-skills.ps1 -Skill m-orchestrator`
- source/dist/installed parity excluding generated build metadata and accepted line-ending differences
- `git diff --check`

## Related Requirements

- [m-project-orchestrator.md](../requirements/m-project-orchestrator.md)

## Related Feature

- [m-project-orchestrator.md](../features/m-project-orchestrator.md)

## Related Decision

- [2026-08-04_orchestrator-multi-repo-runtime.md](../decisions/2026-08-04_orchestrator-multi-repo-runtime.md)
- [2026-07-31_project-orchestrator.md](../decisions/2026-07-31_project-orchestrator.md)

## Related Change

- [2026-08-04_orchestrator-multi-repo.md](../change/2026-08-04_orchestrator-multi-repo.md)
- [2026-07-31_project-orchestrator.md](../change/2026-07-31_project-orchestrator.md)

## Related Lesson

- [orchestrator-multi-repository-runtime-boundaries.md](../lessons/orchestrator-multi-repository-runtime-boundaries.md)
- [orchestrator-lease-recovery.md](../lessons/orchestrator-lease-recovery.md)
