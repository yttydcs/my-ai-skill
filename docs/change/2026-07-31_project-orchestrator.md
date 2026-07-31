# 2026-07-31 Project Orchestrator

## 变更背景 / 目标

The user wanted one persistent Planner session per project that can dispatch each approved task to a temporary background Worker and immediately continue planning. Workers should reuse `$m-execute`, pass their own lightweight checks before consuming scarce test capacity, and use temporary Testers admitted through a configurable pool. Projects must remain isolated even when an optional machine-level budget limits aggregate capacity.

## 具体变更内容

- Added `$m-orchestrator` as a project-scoped companion over the existing `m-*` phases rather than a replacement for them.
- Added explicit Planner, Worker, temporary Tester, archive admission, local-context, and host-tool contracts.
- Added validated `.codex/m-orchestrator.toml` configuration with per-command skill/context mappings, project-local FIFO pools, a capacity-one archive pool, and an optional numeric host budget.
- Added a standard-library runtime for isolated project identity, Planner registration, Task state compare-and-set, Worker binding, gate-bound Tester admission, leases, heartbeat, status, stale inspection, and audited recovery.
- Enforced execution-stage gate evidence before Tester admission and result persistence before normal permit release.
- Added safe recovery for stale project leases and host-only orphan leases, including actor/reason audit records and resumable two-phase reclaim.
- Added lease-ID boundary validation, wrong-owner rejection, non-silent stale handling, host-pool initialization serialization, and Task/lease consistency checks.
- Integrated companion routing into `$m-autoflow`, added stable feature/requirement/spec/decision docs, and synchronized source, dist, and installed skill copies.

## Docs root

- Workflow docs root: `D:\project\my-ai-skills\worktrees\project-orchestrator\docs`
- Canonical docs root after merge: `D:\project\my-ai-skills\docs`
- Publication status: local-only; no remote, push, publication, or backup configuration changed.

## Intake impact

Updated. Added the original request and project-isolation constraints in [2026-07-31_project-orchestrator.md](../intake/2026-07-31_project-orchestrator.md), then linked this completed change.

## Feature impact

Updated. Added [m-project-orchestrator.md](../features/m-project-orchestrator.md) and linked the companion from the existing autoflow feature.

## Requirements impact

Updated. Added [m-project-orchestrator.md](../requirements/m-project-orchestrator.md) and aligned the existing autoflow requirements with companion routing.

## Specs impact

Updated. Added [m-project-orchestrator.md](../specs/m-project-orchestrator.md), including configuration, state, pool, recovery, safety, validation, and host-tool contracts.

## Decision impact

Updated. Added and accepted [2026-07-31_project-orchestrator.md](../decisions/2026-07-31_project-orchestrator.md).

## Lessons impact

Updated. Added [orchestrator-lease-recovery.md](../lessons/orchestrator-lease-recovery.md) because stale ownership, interrupted two-level acquisition, and crash-safe reclaim ordering are non-obvious and likely to recur in filesystem-backed schedulers.

## Related intake

- [2026-07-31_project-orchestrator.md](../intake/2026-07-31_project-orchestrator.md)

## Related features

- [m-project-orchestrator.md](../features/m-project-orchestrator.md)
- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related requirements

- [m-project-orchestrator.md](../requirements/m-project-orchestrator.md)
- [m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related specs

- [m-project-orchestrator.md](../specs/m-project-orchestrator.md)
- [m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related decisions

- [2026-07-31_project-orchestrator.md](../decisions/2026-07-31_project-orchestrator.md)

## Related lessons

- [Orchestrator lease recovery](../lessons/orchestrator-lease-recovery.md)
- [Python cache files during skill synchronization](../lessons/python-cache-skill-sync.md)
- [Windows skill parity and line endings](../lessons/windows-skill-parity-line-endings.md)
- [Windows symlink test privilege](../lessons/windows-symlink-test-privilege.md)

## 对应 plan.md 任务映射

- `ORCH-1`: created the stable feature, requirements, spec, indexes, and autoflow cross-links.
- `ORCH-2`: created the companion skill, role references, example configuration, metadata, and manifest.
- `ORCH-3`: implemented config validation, isolated runtime state, FIFO pools, project/host leases, stale reporting, and audited recovery.
- `ORCH-4`: defined Planner dispatch, `$m-execute` Worker gating, `$m-test` Tester convergence, permit release, and serialized archive admission.
- `ORCH-5`: integrated umbrella routing and added contract/runtime tests.
- `ORCH-6`: validated, synchronized, checked parity, and committed the implementation.
- `$m-continue`: hardened state/lease consistency, input validation, release ordering, host initialization, stale recovery, host-orphan recovery, and crash-resumable audit behavior.

## 经验 / 教训摘要

- A pool should represent permits, not long-lived Tester identities or shared project environments.
- Idempotent acquisition is safe only when the durable Task state and active lease still describe the same ownership.
- Lease expiry is diagnostic evidence, not authority to reclaim automatically.
- Two-level admission needs recovery for the process-crash window between host capacity acquisition and project lease persistence.
- Recovery audit must be written as a resumable state transition; otherwise a crash between Task blocking and audit completion creates another manual-repair state.
- CLI-owned identifiers used in paths must be validated even when normal values are internally generated UUIDs.

## 可复用排查线索

- Symptoms: a Task reports `TESTING` without a lease; a lease remains after the Task entered `TEST_FAILED`; host capacity stays exhausted without a project lease; a stale retry returns `Acquired`; reclaim cannot be retried after interruption.
- Trigger conditions: process termination between host/project admission steps, missing result-before-release enforcement, stale-heartbeat reuse, non-atomic pool metadata initialization, or audit persistence after destructive release.
- Keywords: `stale lease`, `orphan host lease`, `pool reclaim`, `reclaim-host`, `active_lease`, `not consistently TESTING`, `premature release`, `lease_id contains unsafe characters`, `Started`, `Completed`.
- Quick checks:
  - run `pool stale` and compare project leases, host leases, Task state, and `active_lease`;
  - confirm the lease ID is a runtime-generated lowercase UUID hex value;
  - confirm `TESTING -> TEST_FAILED|TEST_PASSED|BLOCKED` was persisted before normal release;
  - inspect project-local reclaim events before retrying recovery;
  - run the focused orchestrator tests before synchronizing the installed skill.

## 关键设计决策与权衡

- Kept orchestration above the existing phase skills so automation does not duplicate or weaken their behavior.
- Used local filesystem state and standard-library Python for deterministic Windows-compatible coordination without adding a service dependency.
- Kept project queues and environments isolated while allowing only opaque numeric host capacity to be shared.
- Chose non-blocking FIFO acquisition and explicit recovery over busy waits or automatic stale reclamation.
- Chose temporary Testers with bounded permits over reusable Tester sessions to avoid stale context and cross-project leakage.

## 测试与验证方式 / 结果

- Orchestrator-focused runtime and contract tests: 29 passed.
- Full repository unittest discovery: 69 passed, 1 existing Windows symbolic-link privilege test skipped.
- Source `m-orchestrator` and `m-autoflow` skill validation: passed.
- Installed `m-orchestrator` skill validation: passed.
- CLI smoke checks for `pool reclaim` and `pool reclaim-host`: passed.
- Source/dist/installed SHA-256 parity: 10 `m-orchestrator` files and 9 `m-autoflow` files matched, excluding generated build metadata.
- `git diff --check`: passed.
- Live Codex background Worker creation was not exercised because this repository is the skill package and has no adopting project configuration; host-tool availability remains an explicit runtime gate.

## 潜在影响

- Filesystem coordination is local-machine only and does not provide distributed consensus.
- Host-tool behavior still depends on the active Codex environment exposing project/task operations.
- Installed copies are local artifacts and remain unpushed; future source changes require another sync.
- The recurring PowerShell profile warning from an empty Conda activation command is unrelated to the implementation but remains visible in command output.

## 回滚方案

1. Revert archive commit and implementation commits `f99496f`, `cb7f1ee`, and `f5bb348` as appropriate.
2. Run `tools/sync-skills.ps1 -Skill m-orchestrator` from the restored source or remove only the installed `m-orchestrator` copy if the whole feature is reverted.
3. Re-sync `m-autoflow` if its companion routing is reverted.
4. Retain runtime state for diagnosis unless the exact project runtime root has been reviewed and explicit cleanup is desired.
5. Rerun validators, focused tests, full discovery, and parity checks.

## 子Agent执行轨迹

- None. `$m-execute` did not require worker-only delegation, the implementation write sets converged on the same runtime/contracts/tests, and stage 4 archive work is non-delegable under the workflow governance rules.

## Closeout

- Archive commit: created on `feat/project-orchestrator` before control-plane merge.
- Default closeout: merge local `main`, verify the result, remove the dedicated Worktree, and delete the merged local feature branch.
- Push status: not requested and not performed.
