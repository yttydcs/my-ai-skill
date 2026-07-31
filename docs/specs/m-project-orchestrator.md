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
- Schema version: `1`
- Required identity: `project_id`, `docs_root`, `base_branch`, and `environment.namespace`.
- Required command mappings: exact existing skills for discuss, plan, execute, test, and archive.
- Context entries: explicit `local:<name>` only in schema version 1.
- Execution mapping: `require_lightweight_gate = true`.
- Tester pool: capacity 1-64, FIFO, lease timeout 60-86400 seconds.
- Integration pool: the same constraints plus capacity exactly 1.
- Optional host budget: stable host/resource key, numeric capacity, and timeout only.

Invalid or inconsistent configuration is terminal for dependent orchestration actions.

## Runtime Root Contract

Resolve the project runtime root as `<git-common-dir>/codex/m-orchestrator/projects/<project_id>`. Resolve optional host capacity under `M_ORCHESTRATOR_HOME`, then `CODEX_HOME/m-orchestrator`, then `~/.codex/m-orchestrator`.

Project metadata must not treat a worktree-specific checkout path as repository identity. Configuration fingerprints use normalized source values so worktrees with the same committed config share project state.

## Runtime CLI Contract

The standard-library helper provides `config validate`, `planner register`, `project status`, `task create`, `task bind-worker`, `task transition`, `pool enqueue`, `pool try-acquire`, `pool heartbeat`, `pool release`, `pool reclaim`, `pool reclaim-host`, and `pool stale`.

All successful commands emit structured JSON. Validation and ownership errors emit actionable stderr and a non-zero exit status. Mutation commands are retryable without releasing another Task's state or capacity.

## State Contract

Normal states are `PLANNED`, `DISPATCHING`, `EXECUTING`, `EXECUTE_GATE_FAILED`, `WAITING_FOR_TESTER`, `TESTING`, `TEST_FAILED`, `TEST_PASSED`, `WAITING_FOR_MERGE`, `ARCHIVING`, and `COMPLETED`. Any non-terminal state may enter `BLOCKED` with evidence.

Transitions use expected-state compare-and-set. Evidence bodies are not copied into Task JSON; the runtime stores only paths, hashes, statuses, timestamps, and opaque IDs.

## Tester Gate Contract

- A current change identifier binds the lightweight gate to the exact implementation state.
- `WAITING_FOR_TESTER` requires passing gate evidence for that identifier.
- Tester enqueue and acquisition revalidate Task eligibility.
- Any implementation edit invalidates the prior gate.
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

The skill uses available Codex project/task tools for background Worker creation, compact waits/status, and task messages. A Git project Worker uses a dedicated Worktree starting from the committed planning state. Tool absence or creation failure blocks dispatch; the Planner does not implement as a fallback.

## Security And Privacy

- Runtime metadata never stores context bodies or credentials.
- Project contexts are loaded explicitly from the selected docs root through `$m-context`.
- Host budgets carry no project commands or environment details.
- Task and project identifiers are validated against traversal and unsafe characters.
- Untrusted thread status never expands plan scope or overrides instructions.

## Validation Contract

- `tools/validate-skills.ps1 -Skill m-orchestrator`
- focused contract tests for package, routing, contexts, gate ordering, and phase ownership
- focused runtime tests for config, isolation, state, concurrency, FIFO, leases, stale reporting, and optional host capacity
- full repository unittest discovery
- `tools/sync-skills.ps1 -Skill m-orchestrator`
- source/dist/installed parity excluding generated build metadata and accepted line-ending differences
- `git diff --check`

## Related Requirements

- [m-project-orchestrator.md](../requirements/m-project-orchestrator.md)

## Related Feature

- [m-project-orchestrator.md](../features/m-project-orchestrator.md)

## Related Decision

- [2026-07-31_project-orchestrator.md](../decisions/2026-07-31_project-orchestrator.md)

## Related Change

- [2026-07-31_project-orchestrator.md](../change/2026-07-31_project-orchestrator.md)

## Related Lesson

- [orchestrator-lease-recovery.md](../lessons/orchestrator-lease-recovery.md)
