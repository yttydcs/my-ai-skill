# 2026-09-06 m-pipeline

## 变更背景 / 目标

Add optional `m-pipeline` version 0.1.0 so the user can configure role sessions and automate a bounded workflow after product discussion. Preserve the original `m-discuss`, `m-plan`, `m-execute`, `m-test`, `m-archive`, supporting skills, and manual workflow. The retired orchestrator stays removed.

The user approved T1–T8 with `$m-execute`, then invoked `$m-archive` for this implementation's normal documentation, local merge and worktree cleanup. No customer workflow or production deployment is authorized by this implementation closeout.

## 具体变更内容

- New companion entry, five focused references, portable blueprint, Python standard-library runtime and copy manifest. Runtime configuration, persistence and workflow transitions remain separate; host actions are performed by the coordinator outside database transactions.
- Explicit role/session bindings, bounded team creation, idle receiver selection, distinct-task fan-out, integration joins, shared claims, durable operation receipts, pause/takeover/resume and fresh-session replacement.
- Original phase adapters read the actual installed skill contracts. Receivers load exact `m-context` references; original phases retain their `m-docs` ownership. Existing `m-go` / `m-continue` can exclusively own an explicitly selected composite loop.
- Preserve the immutable tested candidate through archive metadata commits and worktree cleanup. Optional release has a configured order and evidence contract; it is separate from `m-archive`.
- New focused regression tests and disposable host-pilot helpers. Existing source skills, manifests, tools and tests remain unchanged against baseline `9f4e0efc533eebbf194c3917e033a443de1fd3ef`.
- Installed only [m-pipeline](C:/Users/HelloWorld/.codex/skills/m-pipeline/SKILL.md). Implementation and installation evidence was committed through `e840ccb6db78d6b1a8fa8193cc8b0bf03d45ca9d` before this documentation closeout.

## Docs root

Explicitly invoked original `$m-docs`. The selected root during implementation is `D:\project\my-ai-skills\worktrees\role-pipeline\docs`; after local convergence its durable location is `D:\project\my-ai-skills\docs`. No separate docs repository, remote, publication or backup target is introduced.

The completed root plan is retained at [docs/plan/2026-09-06_role-pipeline.md](../plan/2026-09-06_role-pipeline.md), with its original task definitions and execution checkpoints. Its historical absolute worktree paths are provenance, not current dispatch targets.

## Stable-document impact

These impacts describe the whole completed workflow; the archive step changes links and evidence routing, not product behavior.

- Intake impact: updated — captured source requests, execution approval and closeout reference.
- Feature impact: updated — optional companion behavior, installed status and first-release limits.
- Requirements impact: updated — R01–R18 and compatibility/acceptance boundaries.
- Specs impact: updated — phase composition, local ownership, receipts, capability gates and candidate continuity.
- Decision impact: updated — accepted companion with transactional runtime and original phase ownership.
- Lessons impact: updated — promote recurring handoff, uncertain-action and closeout diagnosis.
- Indexes: intake/features/requirements/specs/decisions entries were added during implementation; plan/change/lessons entries are added at archive. Root index topology and reading order remain valid.

## Related documents

- Related intake: [Source discussion](../intake/2026-09-06_role-pipeline.md).
- Related features: [m-pipeline](../features/m-pipeline.md).
- Related requirements: [R01–R18](../requirements/m-pipeline.md).
- Related specs: [Technical contract](../specs/m-pipeline.md).
- Related decisions: [Role pipeline composition](../decisions/2026-09-06_role-pipeline-composition.md).
- Related lessons: [Handoff and closeout](../lessons/pipeline-handoff-and-closeout.md), [Windows symlink privilege](../lessons/windows-symlink-test-privilege.md), [Installed line-ending parity](../lessons/windows-skill-parity-line-endings.md).

## 对应 plan.md 任务映射

| Task | Delivered scope | Acceptance |
| --- | --- | --- |
| T1 | Actual host and original phase capability contract | Passed; mode-specific host gaps remain explicit |
| T2 | Companion entry, roles, blueprint and adapters | Passed; original skills remain authoritative |
| T3 | Configuration and transactional coordination | Passed; contention, atomic resource acquisition, duplicate/stale receipts |
| T4 | Session lifecycle and bounded recovery | Passed within real-host and deterministic coverage below |
| T5 | Routing, split/join and exact integrated candidate | Passed; both real pipelines completed all required outputs |
| T6 | Context/docs composition and manual recovery | Passed; original loaders, pause/resume and fresh receiver |
| T7 | New manifest, tests and compatibility checks | Passed with stated Windows test skips |
| T8 | Two bounded host pipelines and companion-only installation | Passed; 8 created and archived tasks, zero remaining claims |

D1 native compaction/telemetry, D2 background wakeup, D3 distributed hosts/arbitrary recursion and D4 production deployment/publication remain excluded. No task was silently dropped from T1–T8.

## 关键设计决策与权衡

One coordinator owns a run, with explicit role/session mappings and one local SQLite store shared by cooperating runs. This supplies transactional ownership without reviving project registration. It cannot lock out unrelated human activity or another independent store.

Original plans, Task IDs and phase evidence remain canonical. Runtime metadata and an `actor` field do not prove user authorization; the coordinator must verify the actual launch instruction and any delegated future-plan review. Only different admitted write sets may execute concurrently, and overall testing follows explicit integration.

Host calls cannot be made exactly once by SQLite alone. Persist intent before dispatch; reconcile ambiguous results without releasing claims on elapsed time or treating an idle task as accepted work. Cleanup must preserve tested identity and durable evidence rather than depend on a removed checkout.

## 测试与验证方式 / 结果

| Area | Result | Evidence and limits |
| --- | --- | --- |
| Full regression | 68 tests: 66 passed, 2 skipped | `python -m unittest discover -s tests -v` after final code fixes; Windows fixture symlink creation lacks privilege, WinError 1314 |
| New tests | 28 tests: 27 passed, 1 skipped | The skip is included in the full-suite count |
| Package | Passed | Existing manifest validator, skill validator, installed CLI blueprint validation; version 0.1.0 |
| Source compatibility | Passed | Baseline diff contains no modification to any existing source package, manifest, tool or test |
| Installation compatibility | Passed | 13 new source/dist/installed files match bytes; 67 pre-existing installed files and their file set unchanged; 31 original dependency text comparisons pass after newline/BOM normalization |
| Real-host pilot | Passed | Two independent fixture repositories, split execution, integration, original test, harmless release marker and original archive/merge/cleanup |
| Recovery and contention | Passed within coverage | Real shared architect/closer/release-resource waits, sequential tester reuse, pause/resume, fresh receiver; deterministic unknown-outcome/retry tests |
| Archive validation | Passed | 182 local links, whitespace and new-source scope checked; 13 installed new files match and 67 existing installed files remain unchanged. Only documentation changed after the full regression |

Real pilot used projectless host tasks with explicit, independently verified code-worktree assignments. Saved-project worktree creation and pending-ID reconciliation have schema/deterministic evidence, not a live pilot pass; those paths remain gated on actual identity and checkout readiness. There is no throughput or latency SLO or production-scale benchmark claim.

### Retained host evidence

The local disposable evidence root is `C:\Users\HelloWorld\AppData\Local\Temp\m-pipeline-host-pilot-8tf9krl9`. It is outside the implementation checkout and is preserved by this closeout. This archive and the retained plan carry the durable result summary; temporary fixture files are supplementary local evidence, not the only record.

| Run | Tested / released commit | Local merge | Final metadata-only main |
| --- | --- | --- | --- |
| A | `35d2061eddee77be0df6881ac1d616c70c282c9f` | `d58952c8d89e7beb95346ec1f939249b3456006b` | `258df2535a4cd12d61d9cd7cd1cc34e1877c2485` |
| B | `238bc992e43941e08a81dce6a0f942dc562f63aa` | `841ae368d74b118ad863e29f0264c4c4f839eae7` | `a82f2fdb32969c80ea6b6ed163c67939180b5fa7` |

A's original test reviewed 31 fixture checks and 12 review items; B reviewed 17 checks and 12 review items. The independent audit checked exact product/release-marker bytes, candidate reachability, clean final main, preserved other fixture worktrees and metadata-only context records. Each run passed all seven fixture Task IDs (P1, A1, B1, I1, V1, R1, C1).

The [final run audit](C:/Users/HelloWorld/AppData/Local/Temp/m-pipeline-host-pilot-8tf9krl9/final-audit.json) records two complete runs, 8 created tasks, maximum observed live count 6, zero remaining claims and zero uncertain operations. The [host task audit](C:/Users/HelloWorld/AppData/Local/Temp/m-pipeline-host-pilot-8tf9krl9/final-host-tasks.json) records all 8 archived. Fixture integration worktrees were removed by their own original archive; other fixture trees remain available.

## 经验 / 教训摘要与可复用排查线索

- A receiver may be idle while its shared resource is still claimed: inspect the current assignment and reviewed receipt before dispatching a second writer.
- Archive can legitimately remove the original checkout or change documentation-only HEAD: compare immutable tested commits and preserved plan evidence, not checkout existence alone.
- A report failure after a successful merge does not justify repeating that merge. Pilot A hit a Windows path-separator mismatch in a report-only allowlist; normalizing the comparison repaired the report without replaying Git actions.
- See the [lesson](../lessons/pipeline-handoff-and-closeout.md) for symptom/keyword lookup, quick checks, root causes and prevention.

## 潜在影响与回滚方案

The installed companion is optional and requires explicit configuration and actual launch authority. Context occupancy/compaction tools are unavailable; replacement uses a bounded fresh task at a safe boundary. Automatic continuation requires an active coordinator or explicit resume. Real deployment, secrets and remote publication remain outside this implementation.

To roll back, first pause any later customer run using the companion and reconcile active assignments. Restore/remove only the new companion source, manifest and tests through scoped Git reverts, and uninstall only the verified `m-pipeline` installation. Preserve user blueprints, runtime databases, claims, context and evidence until reconciled. Existing phase packages do not need restoration because they were unchanged. Keep the archive as history and update stable capability status if the feature is withdrawn; do not reset unrelated history or delete unrelated tasks/worktrees.

## 子Agent执行轨迹

Implementation, review and this archive were performed by the workflow owner; no implementation subagents were used. T8 alone used the explicitly approved independent host role tasks below. These were bounded disposable test fixtures, not customer workflows.

| Role | Actual task ID | Final state |
| --- | --- | --- |
| Architect | `01a072f4-76b5-70e0-8536-9e99abbf925e` | Archived |
| Executor 1 | `01a072f5-78aa-73e1-993b-f35f58273c24` | Archived |
| Executor 2 | `01a072f5-8601-7270-8336-6ae1b2639675` | Archived |
| Tester | `01a072f5-9573-7180-bd33-37355387f2e7` | Archived |
| Closer | `01a072f5-a3ed-7521-aa83-bd6250631dab` | Archived |
| Fresh executor | `01a0730e-3daa-73c1-864a-589d4b88e93d` | Archived |
| Publisher A | `01a07319-d53e-7213-8b18-998003f1f4f9` | Archived |
| Publisher B | `01a0731f-75a9-7050-b472-a1244cd3ccbc` | Archived |

## Closeout

- Archive commit: `d54adb6af2fe5552fd606358a1069f382f485e21`, created after execution commit `e840ccb6db78d6b1a8fa8193cc8b0bf03d45ca9d`.
- Local merge: fast-forwarded `main` from `9f4e0efc533eebbf194c3917e033a443de1fd3ef` to the archive commit from `D:\project\my-ai-skills`. The resulting tree exactly matched the reviewed branch; skills, manifests, tools and tests also matched the completed execution commit.
- Cleanup: verified the exact resolved implementation path, clean status, branch identity, absence of reparse points and the 28 known generated ignored files. Removed only `D:\project\my-ai-skills\worktrees\role-pipeline` with `git worktree remove`, then deleted merged `codex/role-pipeline` with `git branch -d`. The control-plane checkout is the only remaining registered worktree.
- Preservation: the installed companion, all 67 pre-existing installed files, independent pilot evidence/store and other fixture worktrees remain intact. Generated distribution and bytecode inside the removed implementation checkout were disposable.
- Post-merge verification: 182 local documentation links pass from the durable main checkout; the source scope still contains no changes to pre-existing packages. Main checkout uses Git's CRLF conversion, so all 13 installed companion files match source text after newline normalization (1 is byte-identical in this checkout). The earlier 13-file source/dist/install byte comparison was made before cleanup; this line-ending difference does not represent a new skill change.
- This final closeout receipt and the retained plan status are committed as a documentation-only follow-up on local `main`; Git history records that receipt commit. Main was clean after merge and cleanup.
- Push/publication: not requested and not performed; all repository/document changes remain local.
