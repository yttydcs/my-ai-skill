# 2026-08-04 m-orchestrator Multi-repository Runtime

## 变更背景 / 目标

The project orchestrator initially treated `project_root` as one Git repository. That blocked intentional umbrella projects such as `D:\project\monkeys`, whose `repo` directory contains multiple independent repositories. The workflow corrected the project/repository boundary while preserving the existing persistent Planner, temporary Workers, bounded Tester pools, and authoritative `m-*` phases.

## 具体变更内容

- Added backward-compatible configuration schema version 2 with an explicit repository catalog and per-repository base branches.
- Made the schema v2 runtime project-local and independent of umbrella Git metadata; schema v1 keeps its existing single-repository runtime.
- Added validated Task manifests containing the exact repository subset, worktrees, branches, refs, plans, write sets, acceptance, tests, rollback, and Planner callback.
- Added deterministic composite change IDs so drift in any participating repository invalidates Tester admission evidence.
- Propagated the complete repository/worktree set through Planner, Worker, Tester, continue, and archive contracts without duplicating phase-skill behavior.
- Replaced ambiguous global host-lease ownership with opaque project-instance and Task ownership digests.
- Made exact manifest Task creation idempotent after Worker commits while retaining strict validation for first creation and different manifests.
- Added multi-repository, compatibility, concurrency, lease, manifest, gate-drift, installed-runtime, and end-to-end regression coverage.
- Synchronized the validated `m-orchestrator` source into distribution and the local installed skill.

## Docs root

- Workflow docs root: `D:\project\my-ai-skills\worktrees\orchestrator-multi-repo\docs`
- Canonical docs root after merge: `D:\project\my-ai-skills\docs`
- Publication status: local-only; no remote, push, publication, or backup configuration changed.
- `D:\project\monkeys` was read-only acceptance evidence and was not modified or initialized as Git.

## Intake impact

Updated. [2026-08-04_orchestrator-multi-repo.md](../intake/2026-08-04_orchestrator-multi-repo.md) preserves the user's umbrella/multiple-child-repository requirement and now links the completed workflow.

## Feature impact

Updated. [m-project-orchestrator.md](../features/m-project-orchestrator.md) now describes schema v2 umbrella projects, exact Task repository sets, aggregate gates, and non-atomic archive coordination.

## Requirements impact

Updated. [m-project-orchestrator.md](../requirements/m-project-orchestrator.md) now requires non-Git umbrella support, explicit repository validation, v1 compatibility, cross-project isolation, and source/dist/install parity.

## Specs impact

Updated. [m-project-orchestrator.md](../specs/m-project-orchestrator.md) now defines schema adapters, runtime identity, Task manifests, composite evidence, worktree-set propagation, security boundaries, and validation.

## Decision impact

Updated. [2026-08-04_orchestrator-multi-repo-runtime.md](../decisions/2026-08-04_orchestrator-multi-repo-runtime.md) is accepted and implemented and supersedes the single-Git-root portions of the original decision.

## Lessons impact

Updated. Added [orchestrator-multi-repository-runtime-boundaries.md](../lessons/orchestrator-multi-repository-runtime-boundaries.md) because the topology, global-owner identity, and immutable-idempotency failures are structural, non-obvious, and likely to recur in local orchestrators.

## Related intake

- [2026-08-04_orchestrator-multi-repo.md](../intake/2026-08-04_orchestrator-multi-repo.md)
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

- [2026-08-04_orchestrator-multi-repo-runtime.md](../decisions/2026-08-04_orchestrator-multi-repo-runtime.md)
- [2026-07-31_project-orchestrator.md](../decisions/2026-07-31_project-orchestrator.md)

## Related lessons

- [Orchestrator multi-repository runtime boundaries](../lessons/orchestrator-multi-repository-runtime-boundaries.md)
- [Orchestrator lease recovery](../lessons/orchestrator-lease-recovery.md)
- [Python cache files during skill synchronization](../lessons/python-cache-skill-sync.md)
- [Windows skill parity and line endings](../lessons/windows-skill-parity-line-endings.md)
- [Windows symlink test privilege](../lessons/windows-symlink-test-privilege.md)

## 对应 plan.md 任务映射

- `MRO-1`: aligned the feature, requirements, specs, decisions, intake, and terminology with umbrella/repository boundaries.
- `MRO-2`: added schema v2 repository catalogs and preserved schema v1 behavior and migration diagnostics.
- `MRO-3`: decoupled schema v2 runtime identity from Git and hardened opaque host-lease project isolation.
- `MRO-4`: persisted exact Task manifests, composite change identity, gate revalidation, and post-commit creation idempotency.
- `MRO-5`: aligned Worker, Tester, continue, and archive handoffs over complete repository/worktree sets.
- `MRO-6`: added multi-repository, compatibility, same-ID isolation, legacy lease, manifest retry, and end-to-end regression tests.
- `MRO-7`: ran validators, focused/full tests, installed smoke tests, sync, parity, performance observation, diff checks, and English commits.
- `MRO-X1` and `MRO-X2`: not executed; real-project adoption and repository discovery/external allowlisting remain separate workflows.

## 经验 / 教训摘要

- An umbrella project is a scheduling and documentation boundary, not necessarily a Git boundary.
- A machine-wide pool must identify ownership with an opaque canonical project-instance identity, not reusable human labels alone.
- Idempotent creation must check an existing immutable request identity before revalidating mutable creation-time state.
- Multi-repository evidence must bind every selected worktree; a pass in one repository cannot stand in for aggregate admission.
- Independent repository merges are not atomic and must retain per-repository progress if later integration fails.

## 可复用排查线索

- Symptoms: `project_root is not a valid Git repository`; an umbrella is told to run `git init`; two projects with the same IDs share one host lease; exact `task create --manifest` fails after a Worker commit with `planning_ref must identify the current committed planning state`.
- Trigger conditions: non-Git umbrella roots, one-Git-root schemas, global owners derived only from `project_id:task_id`, or mutable worktree validation before existing-record lookup.
- Keywords: `schema_version 2`, `[[repositories]]`, `non-Git umbrella`, `host-capacity`, `project_instance_id`, `different manifest`, `planning_ref`, `manifest retry`.
- Quick checks:
  - confirm the configured schema and explicit repository catalog before inspecting umbrella `.git`;
  - compare canonical project runtime roots and opaque project-instance IDs for colliding host leases;
  - compare the submitted manifest SHA-256 with the persisted Task before revalidating worktree HEAD;
  - rerun the focused runtime/contract tests and an installed two-repository smoke flow before archive.

## 关键设计决策与权衡

- Chose explicit repository configuration over recursive discovery so unrelated nested Git metadata is never silently adopted.
- Chose project-local schema v2 runtime state over an arbitrary child-repository anchor; schema v1 state is not automatically moved.
- Chose opaque hashed host ownership so separate roots remain isolated without storing project paths, commands, or context in global state.
- Preserved exact-ID operations for legacy lease records, but new acquisition rejects ambiguous legacy ownership instead of adopting it silently.
- Chose immutable manifest identity for retries and full mutable-state validation only for first creation.

## 测试与验证方式 / 结果

- Python compilation and `git diff --check`: passed.
- Orchestrator-focused runtime and contract suite: 46 passed.
- Full repository unittest discovery: 86 passed, with 1 existing Windows symbolic-link privilege skip.
- Source and installed `m-orchestrator` validators: passed.
- Source/dist/installed SHA-256 parity: 9 files matched, excluding generated build metadata and Python cache files.
- Installed runtime smoke: Planner registration, same-ID host capacity isolation, distinct lease IDs, and post-commit manifest retry passed.
- Installed two-repository flow: complete repository set reached `TEST_PASSED` and released Tester capacity.
- Performance observation: 8 declared repositories loaded 3 times in 7.861 seconds, or 2.620 seconds per load; no formal threshold is configured and ordinary validation remains linear in declared repositories.
- Read-only `D:\project\monkeys` validation returned the expected schema v2 migration diagnostic without suggesting `git init`.
- UI evidence: not applicable because no UI code or visible layout changed.

## 潜在影响

- Configuration validation invokes Git for each declared repository and remains linear; large catalogs may benefit from later profiling or caching with explicit freshness rules.
- Legacy host lease records can be continued only through exact-ID operations; ambiguous new acquisition blocks for explicit inspection and recovery.
- Cross-repository archive integration remains ordered but non-atomic.
- The installed skill is a local copy and remains unpushed.

## 回滚方案

1. Revert archive commit and implementation commits `87ceb9e`, `6380346`, and `73ecf17` as appropriate.
2. Run `tools/sync-skills.ps1 -Skill m-orchestrator` from the restored source.
3. Do not delete project runtime state until its Tasks and leases have been inspected and converged.
4. Rerun focused/full tests, source and installed validation, parity, smoke tests, and `git diff --check`.
5. Do not initialize or otherwise mutate umbrella projects as part of rollback.

## 子Agent执行轨迹

- None. Planning and archive are non-delegable; execution/test repairs shared the same runtime/test write set; ordinary `$m-execute`, `$m-test`, and `$m-continue` did not grant `$m-go` worker-only delegation.

## Closeout

- Archive commit: created on `fix/orchestrator-multi-repo` before control-plane merge.
- Default closeout: merge local `main`, verify the result, remove the dedicated worktree, prune worktree metadata, and delete the merged local branch.
- Push status: not requested and not performed.
