# Archived Plan - m-pipeline Implementation

This is the retained implementation plan, archived through the user's `$m-archive` invocation on 2026-09-06. Original task definitions and chronological execution checkpoints are preserved below; historical worktree paths are provenance. See the [change archive](../change/2026-09-06_m-pipeline.md) for closeout evidence.

## Archive Status

- Phase: `m-archive`; documentation prepared, local convergence pending final verification.
- Docs root after convergence: `D:\project\my-ai-skills\docs`.
- Intake impact: updated; feature impact: updated; requirements impact: updated; specs impact: updated; decision impact: updated — new companion documents are complete and their plan links now target this retained copy.
- Lessons impact: updated — [pipeline handoff and closeout](../lessons/pipeline-handoff-and-closeout.md) captures recurring ownership, immutable-candidate and report-recovery guidance.
- Plan/change/lessons indexes updated; the root documentation topology is unchanged. No publication target is inferred.

## Execution Status And Goal At Archive Entry

- Phase: `m-execute`.
- Status: T1–T8 completed, verified and accepted on 2026-09-06; only the new m-pipeline companion is installed.
- Blocked: no. This implementation branch's own archive/merge/cleanup remains a later original `m-archive` phase.
- User instruction authorizing execution: `$m-execute`, following the presented T1–T8 scope, including bounded T8 fixture-task creation and installation of only the new companion. D1–D4 remain excluded.
- Goal: add an optional role/session pipeline that continues from an explicitly authorized product discussion through the existing planning, execution, testing, and closeout phases, while preserving the user's original manual workflow.

## Initialization And Ownership

| Item | Value |
| --- | --- |
| Project root | `D:\project\my-ai-skills` |
| Owning code repository | `D:\project\my-ai-skills` — the skill repository; no other product repository participates in this implementation |
| Base | `main` at `9f4e0efc533eebbf194c3917e033a443de1fd3ef` |
| Dedicated branch | `codex/role-pipeline` |
| Active worktree | `D:\project\my-ai-skills\worktrees\role-pipeline` |
| Selected docs root | `D:\project\my-ai-skills\worktrees\role-pipeline\docs` — this repository's established documentation tree |
| Canonical active plan | `D:\project\my-ai-skills\worktrees\role-pipeline\plan.md` |
| Local guide | `guide.md`: automatically commit changes with an English commit message consistent with history |
| Implementation owner | Current workflow owner, after explicit approval; no implementation delegation is admitted in this planning turn |

The base already removed the retired orchestrator. Do not reinstate its registration service, edit its backups, or treat historical orchestrator documents as active workflow rules. Existing source skills, manifests, shared tools, and pre-existing tests are the compatibility baseline and must remain unchanged.

## Discussion And Chosen Direction

The user wants to define a pipeline manually, bind dedicated existing sessions or create a configured team with one instruction, then stop manually moving work between several workflows. The default responsibilities are product manager/discuss, architect/plan, executor/execute, tester/test, and release owner/archive with a separately configured deployment procedure.

The proposed package is `m-pipeline`. Roles map to existing skills; they are not a new collection of competing phase skills. One coordinator owns each run. A small local SQLite runtime records explicit assignments, shared session/resource claims, operation receipts, and recovery state. Host tools create and message actual sessions. This durable coordination is needed for parallel workflows, but does not reintroduce project registration or automatic discovery.

The original root plan remains authoritative. `any` chooses one eligible receiver; `split` distributes distinct admitted Task IDs; `join` requires all designated results and tests the integrated candidate. Session replacement reloads explicit context and exact worktree/commit progress. One-level execution children and creation limits bound expansion.

Use `m-context` in the receiving session before the phase. Preserve the existing phase-owned `m-docs` calls, particularly in `m-plan` and `m-archive`; the companion invokes `m-docs` directly only for documents it owns. Do not duplicate project truth or load full context bodies into runtime state.

Autonomous launch must record an actual user instruction with scope, environments, permitted actions, creation bounds, and any delegated review of future plans. It must not describe a delegated review as the user having personally approved an unseen plan. When delegation is absent, the original plan-confirmation gate remains. Required product decisions and scope expansion return to the user.

## Governed Document Impact

`m-docs` is used for this planning work. The selected docs root is explicit; no private external repository or publication target is inferred.

| Document category | Planned impact |
| --- | --- |
| Intake | Preserve the source discussion in [2026-09-06_role-pipeline.md](../intake/2026-09-06_role-pipeline.md). |
| Feature | Add the proposed user workflow and scenarios in [m-pipeline.md](../features/m-pipeline.md). |
| Requirements | Add R01–R18 and durable compatibility boundaries in [m-pipeline.md](../requirements/m-pipeline.md). |
| Specification | Add composition, identity, state, host, and handoff contracts in [m-pipeline.md](../specs/m-pipeline.md). |
| Decision | Record the companion/runtime choice in [2026-09-06_role-pipeline-composition.md](../decisions/2026-09-06_role-pipeline-composition.md). |
| Indexes | Add entries to the five nearest category indexes; mark unimplemented capability documents as planned. |
| Lessons | Read existing [runtime-boundary](../lessons/orchestrator-multi-repository-runtime-boundaries.md) and [recovery](../lessons/orchestrator-lease-recovery.md) lessons as history. Add a new lesson only if implementation produces a reusable finding. |
| Change and plan archive | No implementation/change claim or archived-plan copy during planning. Leave later closeout to the original `m-archive`. |

## Task Summary

All paths in this table are relative to the active worktree. Proposed files do not exist merely because they appear in the plan. Detailed write sets below are authoritative.

| Task ID | Title | Scope | Files / Modules | Acceptance / Tests | Risk / Notes |
| --- | --- | --- | --- | --- | --- |
| T1 | Verify host and phase capabilities | Will execute | New spec and capability evidence | Confirm real session identities, checkout binding, waiting, and delegation contract | Gate dependent integration; unsupported capability must be explicit |
| T2 | Define companion and phase adapters | Will execute | `skills/m-pipeline` entry, roles, configuration and phase references | Original skill calls, truthful launch authority, and one loop owner | No edits to existing phase skills |
| T3 | Implement transactional coordination | Will execute | New runtime config/store and focused tests | Cross-run claims, atomic resources, operation receipts, and recovery pass | Local cooperating-host guarantee only |
| T4 | Implement session lifecycle | Will execute | New lifecycle instructions, runtime transitions and tests | Existing/new sessions, bounded waiting, uncertain delivery, and fresh replacement | No native context compaction |
| T5 | Implement automatic phase routing | Will execute | New workflow/handoff logic and tests | Any/split/join, repair/replan, exact integrated candidate and one-level children | Scope and shared write ownership remain enforced |
| T6 | Integrate context, documents and manual recovery | Will execute | New phase/recovery references and contract tests | Fresh session resumes from canonical artifacts; manual work is not replayed | Preserve private docs and existing supporting-skill ownership |
| T7 | Package and validate compatibility | Will execute | New manifest, fixtures, contract tests and docs | New package validates; existing packages remain byte-for-byte unchanged | Mock evidence is distinguished from host evidence |
| T8 | Run bounded host pilot and install companion | Will execute | New skill installation and new-scope validation docs | Two fixture workflows share sessions safely and complete configured flow | At most 8 new test sessions total, 6 live; no real deployment |
| D1 | Native compaction and context telemetry | Will not execute now | Optional future host adapter | Verify access to actual desktop sessions before integration | Deferred: capability is not exposed in current task tools |
| D2 | Background wakeup after coordinator stops | Will not execute now | Future wakeup integration | Resume without an active coordinator | Deferred: first release has persistence and explicit resume |
| D3 | Recursive graphs and distributed hosts | Will not execute now | Future scheduler extensions | Additional depth and distributed ownership semantics | Deferred: first release is one host and one child level |
| D4 | Actual production deployment and publication | Will not execute now | Product environment and release configuration | Separate target-specific authorization and evidence | Out of scope: fixtures only; no credentials, push or production action |

## Will Execute After Approval

- [x] T1 — Verify host and phase capabilities; real creation/delivery acceptance remains assigned to T8.
- [x] T2 — Define companion and phase adapters.
- [x] T3 — Implement transactional coordination.
- [x] T4 — Implement session lifecycle.
- [x] T5 — Implement automatic phase routing; real-host scenario remains in T8.
- [x] T6 — Integrate context, documents and manual recovery; real receiver validation remains in T8.
- [x] T7 — Package and validate compatibility.
- [x] T8 — Run bounded host pilot and install only the new companion.

### T1 — Verify Host And Phase Capabilities

- Owner/root: current workflow owner; canonical plan and active worktree above.
- Goal: establish the actual host contract before implementation depends on assumed capabilities.
- Write set: `docs/specs/m-pipeline.md` for the supported contract; this root `plan.md` for task progress and capability evidence. Evidence initially distinguishes documentation inspection from real-host verification; no passing runtime evidence is fabricated. Preserve completed evidence through the original later `m-archive` routing.
- Work: inspect current task APIs and original skill entry contracts; define expected handling of pending creation IDs, exact destination worktrees, completed/needs-attention observations, unclear delivery, and user delegation. Determine the documented method to reconcile a created task's real identity and checkout. Define a disposable pilot blueprint and a fault-injection matrix for later tasks.
- Acceptance/tests: a capability table states supported/unsupported/unproven with evidence and the effect on each advertised mode. Required unsupported behavior blocks its dependent path; no default-branch substitution, fake compaction, or silent manual fallback. Later T8 must resolve the real-host items before those modes are declared supported.
- Dependencies: none. This task does not create role sessions; creation is isolated to the explicitly bounded T8 pilot.
- Risks: a required capability may not exist on the installed host. If the finding materially changes promised behavior, revise the affected plan scope and return that decision to the user before dependent implementation.
- Rollback: revert only this task's new evidence/spec changes; no host state is mutated.

### T2 — Define Companion And Phase Adapters

- Owner/root: current workflow owner; same active worktree and plan.
- Goal: specify one usable optional entry point with clear roles and phase ownership.
- Write set: `skills/m-pipeline/SKILL.md`, `agents/openai.yaml`, `references/configuration.md`, `references/phase-adapter.md`, `assets/pipeline.example.json` under the new package; relevant new feature/spec docs.
- Work: implement setup/start/status/pause/resume routing, explicit existing/create bindings, plan-review delegation, stage inputs/outputs, required context references, and selected composite-loop ownership. Keep examples portable and nonsecret. Read originals at use time and track relevant contract revisions without copying their content.
- Acceptance/tests: walkthroughs cover a manually bound team and an explicitly requested new team, delegation absent/present, scope expansion, default execute/test, and explicitly chosen `m-go`/`m-continue`. Every role invokes the actual skill and retains its prerequisites. `m-archive` is described accurately as closeout, with deployment separately configured.
- Dependencies: T1 capability contract. Behavior tests are consolidated in T7 after runtime contracts exist.
- Risks: instructions alone cannot enforce concurrency, so they must call the T3 runtime before dispatch; they must not imply stronger host guarantees.
- Rollback: remove/revert only the new package entry and examples; old skill invocation remains available.

### T3 — Implement Transactional Coordination

- Owner/root: current workflow owner; same active worktree and plan.
- Goal: make assignment ownership and recovery reliable across cooperating concurrent runs.
- Write set: new package `scripts/pipeline_runtime.py`, `scripts/pipeline_lib/{__init__,config,store}.py`; `tests/test_m_pipeline_config.py`, `tests/test_m_pipeline_store.py`.
- Work: validate explicit blueprints, paths and limits; resolve one local state store; create a versioned SQLite schema for runs, ownership, sessions/resources, assignments and operation records. Use short transactions and compare-and-set generations, structured errors, immutable operation IDs, and explicit uncertain states. Do not store context bodies or secrets.
- Acceptance/tests: valid portable configs round-trip; unknown fields/invalid roots fail clearly; Unicode/spaces and Windows junction/case behavior are handled with platform-specific skips reported. Two processes cannot claim one shared session/resource concurrently. Failed all-resource acquisition leaves no partial claim. Duplicate receipts are harmless; stale receipts cannot release a newer claim. Simulated restart preserves uncertainty and ownership; timeout alone never reclaims it.
- Dependencies: T1 and T2.
- Risks: a local store coordinates only participants using that store. Long-running transactions or a second lease layer would undermine the design and are prohibited.
- Rollback: revert new runtime/tests; retain any user runtime database until its ownership is reconciled. No automatic deletion or migration of unrelated state.

### T4 — Implement Session Lifecycle

- Owner/root: current workflow owner; same active worktree and plan.
- Goal: bind, create, wait for, and replace sessions without duplicate or interrupted work.
- Write set: new package `references/session-lifecycle.md`, `scripts/pipeline_lib/workflow.py`, necessary new-package runtime command wiring; `tests/test_m_pipeline_workflow.py` lifecycle cases.
- Work: generate durable creation/dispatch intents; reconcile pending creation IDs into real host/thread IDs; reserve before preparing context and sending work; implement capacity/total-creation accounting, eligibility checks and bounded cursor-based waiting. Reconcile uncertain delivery before retry. Allow fresh-session replacement only after the previous writer stops and progress is durable.
- Acceptance/tests: fake-host sequences cover delayed readiness, timeout after successful creation/send, duplicate callbacks, busy sessions, all capacity occupied, replacement capacity exhausted, and manual activity drift. No pending ID reaches a thread-only tool. Replacement preserves Task IDs and exact candidate identity; no invented context percentage or automatic native compaction is advertised.
- Dependencies: T3.
- Risks: external human actions can race with local admission; expose and reconcile them instead of treating local claims as host locks.
- Rollback: pause admission, reconcile live assignments, then revert new lifecycle logic. Do not kill occupied sessions or discard their evidence.

### T5 — Implement Automatic Phase Routing

- Owner/root: current workflow owner; same active worktree and plan.
- Goal: complete a bounded pipeline after authorized launch, including meaningful parallel execution.
- Write set: new package `references/handoffs.md`, `scripts/pipeline_lib/workflow.py`, runtime command wiring, and `tests/test_m_pipeline_workflow.py` routing cases.
- Work: validate handoff envelopes and receipts against the current plan/authority/candidate. Implement any/split/join, explicit repair and replan transitions, one-level admitted children, a designated integration owner, required-result accounting, candidate invalidation, and single ownership of composite execution/test loops. Serialize declared shared docs/integration/release resources.
- Acceptance/tests: two runs can share an idle pool without duplicate assignment; fan-out never gives the same admitted write set to competing writers. A missing/failed child blocks the required join. A changed integrated commit invalidates old test evidence. Ordinary in-scope repair progresses automatically, while scope expansion and bounded non-progress surface actionable decisions. Multi-repository fixtures retain separate paths and revisions. Release uses a harmless fixture only.
- Dependencies: T4; context/document behavior also requires T6 before end-to-end acceptance.
- Risks: integration is not an early release merge. All candidate assembly and conflict handling must fit admitted tasks; business completion requires original phase evidence.
- Rollback: stop new dispatch, preserve child outputs and the integrated candidate, and return remaining work to the same canonical plan for manual execution.

### T6 — Integrate Context, Documents And Manual Recovery

- Owner/root: current workflow owner; same active worktree and plan.
- Goal: give new or resumed role sessions enough canonical context without duplicating the existing workflow's document system.
- Write set: new package `references/phase-adapter.md`, `references/recovery.md`, `references/handoffs.md`, necessary new runtime transition checks; `tests/test_m_pipeline_contract.py` context/recovery cases; new feature/requirements/spec docs.
- Work: compose `m-context` before the phase using explicit names/sections and roots; let original phases own their `m-docs` calls. Define setup-owned docs governance, artifact revisions, shared document ownership, durable evidence before cleanup, cooperative pause/takeover/resume, and phase-contract drift handling.
- Acceptance/tests: a fresh session reconstructs the same assignment from references and evidence. Required context failure prevents dependent dispatch. Private context bodies never enter the runtime/fixture/public repo. Pause admits no new work, takeover waits for the old writer, and resume recognizes manually completed tasks without replay. Task-definition/scope changes trigger selective revalidation; progress-only updates do not invalidate their own assignment. Original phase reports remain truthful.
- Dependencies: T2, T3 and T5 transition shapes.
- Risks: snapshots can become stale; check revisions on admission and acceptance. Never infer a private docs root or silently fall back on context-load errors.
- Rollback: revert only companion integration; continue manually from the original artifacts and preserved evidence.

### T7 — Package And Validate Compatibility

- Owner/root: current workflow owner; same active worktree and plan.
- Goal: produce an installable companion with evidence for its new contracts and preservation of the old workflow.
- Write set: `manifests/m-pipeline.json`; new `tests/test_m_pipeline_contract.py`, focused new test files from T3–T6 and `tests/fixtures/m-pipeline/`; new package/docs refinements only. Record execution validation in this root plan and let later `m-archive` route completed results into the established `docs/change/` category.
- Work: use the established copy-manifest format and unchanged validation/sync scripts. Build deterministic fake-host fixtures, complete contract tests, run the existing regression suite once, and record required platform skips. Compare all pre-existing skills/manifests/tools/tests to the base. Review examples and state/logging for secret leakage.
- Acceptance/tests: focused tests, applicable existing regression checks, package validation and generated package inspection pass. Fault cases cover restart, duplicate/stale results, concurrency, cross-repo candidate identity, context failures and authority boundaries. No changes to old package files or behavior are needed. Mock-only capabilities remain labeled unproven until T8.
- Dependencies: T2–T6.
- Risks: a test that just mirrors implementation is insufficient; prefer observable invariants and independent process/fake-host scenarios. Do not broaden unrelated tooling work.
- Rollback: revert new manifest, tests and package refinements; existing installed skills remain unchanged.

### T8 — Run Bounded Host Pilot And Install Companion

- Owner/root: current workflow owner; implementation still uses this worktree and canonical plan. Pilot repositories use explicitly identified disposable paths, not this repository's business worktree or user product repositories.
- Goal: validate real tool composition and make only the new companion available after all acceptance gates pass.
- Write set: this root plan's execution evidence; new feature/requirements/spec statuses; generated ignored `dist/codex/m-pipeline/`; only the new user skill destination resolved by the existing sync tool. Local scratch repos and runtime state must be explicitly identified before creation/cleanup. Later closeout uses the established document categories; do not invent a new testing-docs tree.
- Creation scope on approval of T8: explicitly request up to 8 new disposable Codex tasks in total, at most 6 live at once, solely for the pilot. Reuse them between phases where appropriate; do not bind, message, rename, archive, or interrupt unrelated existing tasks. If that bound cannot validate the design, report the remaining gap rather than expand it silently.
- Work: run two fixture workflows with an explicitly shared session/resource pool, busy-session waiting, one parallel split/join, fresh-session continuation, pause/resume, and a deterministic local release marker. Confirm actual destination worktrees and evidence at every handoff. Archive only completed pilot tasks created for this test using the host tool. Validate/sync only the new manifest, following the existing scripts' documented options.
- Acceptance/tests: real-host evidence establishes the supported creation and handoff modes, exact candidate continuity and automatic in-scope progression. Busy receivers receive no conflicting assignment; fresh receivers need no repeated user explanation. Existing installed packages match their pre-install state. Any unsupported/skipped scenario is reported and its affected advertised capability remains gated. No real deployment, remote push or credentials provisioning occurs.
- Dependencies: T7. Approval of this planning phase alone does not authorize this pilot; execution approval must include T8 and its explicit creation/install scope.
- Risks: host limits or API gaps can prevent full pilot completion. Do not declare success from simulated tests; revise the supported capability claim or escalate the material scope decision.
- Rollback: stop new pilot dispatch, reconcile live tasks, retain evidence, and archive only completed test tasks. Remove/restore only the verified new skill destination if installation needs rollback; preserve other packages. Validate exact scratch paths before any recursive removal.

## Will Not Execute Now

- D1 — Native context compaction and occupancy telemetry. Official interface documentation is insufficient to prove access to the active desktop tasks; first release uses bounded fresh-session replacement. Requires a separately validated host adapter.
- D2 — Background wakeup after app/coordinator shutdown. Durable records and explicit resume are included; an always-on service or scheduled wakeup is a later project.
- D3 — Arbitrary recursive graphs, deeper execution children and distributed multi-host scheduling. The first release uses one cooperating host/store and one execution-child level.
- D4 — Actual product production deployments, secrets/environment provisioning, remote publication and Git push. Only configurable release semantics and local fixture validation are included.

## Dependencies And Parallelism

Implementation sequence: T1 → T2 → T3 → T4 → T5 → T6 → T7 → T8. Some reference drafting could be independent, but workflow/runtime files overlap, so the initial implementation uses one writer. This plan does not admit implementation subagents. Future changes to that policy require an explicit bounded assignment consistent with the original phase instructions.

Runtime role concurrency is a product feature validated by T8; it is separate from delegating this implementation. Each pilot task must receive its fixture project/docs root, role skill, exact worktree/revision, parent/run/Task IDs, write set, launch authority, evidence target, and creation limits.

## Requirement Coverage

| Requirement IDs | Owning implementation tasks |
| --- | --- |
| R01 | T2, T7, T8 |
| R02, R08, R15 | T2, T4, T6, T8 |
| R03, R04, R14 | T3, T4, T5 |
| R05, R06, R12 | T1, T2, T5, T7 |
| R07, R09, R10, R11 | T1, T4, T5, T7, T8 |
| R13, R17, R18 | T3, T6, T7 |
| R16 | T2, T5, T8 |

## Validation And Completion

During this planning turn, validate document links, task/scope completeness, requirement mapping, changed-file boundaries and whitespace only. Do not run implementation tests or claim runtime capability passes. Commit the planning documents in English per `guide.md`; do not push or merge.

Planning validation on 2026-09-06: checked the exact 11-document write set, 85 local Markdown links, all 12 unique Task IDs and their scope split, and coverage of R01–R18. Pre-existing skills, manifests, tools and tests have no changes against the base. Whitespace validation passed. No implementation tests or real-host pilot were run in this phase.

After execution approval, run focused new tests as each behavior is implemented, then the existing regression suite and unchanged package validation in T7. T8 adds bounded real-host evidence. Record mock/host/platform distinctions and unresolved capabilities. Once checks pass, do not repeat broad tests without a relevant change or concern.

Execution is complete only when every admitted task is accepted, the companion is validated and installed within the approved scope, pre-existing packages remain unchanged, and stable docs accurately describe implemented behavior. The current workflow's final archive/merge/cleanup still belongs to the original `m-archive`; no base-branch merge is part of this planning turn.

## Risks And Remaining Technical Questions

- Host creation may not expose a reliable path to the requested live checkout; T1 defines the contract and T8 supplies real evidence before claiming support.
- No per-thread context-usage/compaction tools are currently exposed. This is an explicit D1 exclusion, not an assumed fallback success.
- Autonomous generated-plan review needs a real explicit launch delegation; the wrapper cannot invent authority or modify old skills to bypass it.
- Local claims cannot lock out arbitrary external users or independent state stores. Recovery must reveal and reconcile competing activity.
- A release may depend on a worktree that archive removes. Configuration must establish the order and preserve durable evidence; T8 tests fixture semantics only.
- If T1 reveals that preserving the existing contracts cannot support an essential requested mode, stop that dependent path and present a concrete scope revision. Do not silently reduce behavior or refactor the original phase skills.

## Approval Boundary

Requested execution scope: T1–T8, including T8's bounded disposable-session creation and installation of only `m-pipeline`. D1–D4 remain excluded. The user may approve selected Task IDs; dependent tasks must remain blocked if their prerequisite is excluded.

Execution approval received through the user's `$m-execute` follow-up. This does not authorize D1–D4 or changes to existing skill packages.

## Execution Evidence

### T1 — Capability Inspection, 2026-09-06

| Capability | Evidence / status | Implementation consequence |
| --- | --- | --- |
| Saved projects | `list_projects` returned the real repository path and Git flag | Resolve actual project IDs; do not invent registration records |
| Existing task identity and working directory | `read_thread` on this task returned stable ID, host ID, status and `cwd` | Bind verified identities; send exact worktree paths in every assignment |
| New tasks | Tool schema supports projectless and project worktree creation, explicit starting state, and pending `clientThreadId` | Persist creation intent; reconcile the ready task ID before dispatch; real pilot pending T8 |
| Observe and send | `read_thread`, `send_message_to_thread`, cursor-based `wait_threads` exposed | Coordinator owns host calls; runtime records intents and claims; real pilot pending T8 |
| Exact checkout | Task metadata exposes actual cwd; shell can independently verify configured Git worktrees and revisions | Explicit assignment workdir is mandatory even if task cwd differs; no default-checkout substitution |
| Atomic host claim / exactly-once send | Not documented by exposed tools | Local SQLite coordinates cooperating runs only; ambiguous outcomes remain uncertain |
| Native compaction / context occupancy | Not exposed in current task tools | D1 deferred; use bounded fresh-session replacement |
| Background wakeup | No wakeup service in this scope | D2 deferred; active coordinator or explicit resume required |
| Original phase authority | Read installed `m-execute`, shared phase/subagent rules and `m-context`; existing `m-plan` requires real approval | Preserve original skill calls and report actual launch delegation; never invent user approval |

Read-only inspection passed. No role tasks were created during T1. Host creation and end-to-end evidence are not yet claimed.

### T2–T7 — Implementation And Local Validation, 2026-09-06

Added only `skills/m-pipeline/`, `manifests/m-pipeline.json`, new `test_m_pipeline_*` tests and their isolated fixture helper. The companion composes original phase skills; the runtime performs no host calls. It validates explicit blueprints and selected original-plan definition sections, records local SQLite claims/intents, seals stage membership, checks exact candidates and reviewed receipts, and supports bounded creation, one-level groups, manual takeover and recovery.

Validation: `python -m unittest discover -s tests -v` ran 66 tests: 64 passed, 2 skipped for Windows symlink privilege (WinError 1314). New scenarios cover independent-process claim contention, all-or-none resource acquisition, uncertain delivery across restart, manual takeover, one-level joins, distinct-branch integration requirements, required-context failure, scope/environment authority, non-Git umbrellas with two repositories, non-progress bounds, and duplicate/stale results. `tools/validate-skills.ps1 -Skill m-pipeline` and the bundled skill validator passed. `git diff --check` passed. No pre-existing source skills, manifests, tools or tests changed.

Two implementation refinements were verified: dispatch invalidates prior idle observations so a fresh host observation is required for result acceptance; occupied shared resources wait without triggering unnecessary receiver creation. Plan fingerprints normalize completion checkboxes and exclude explicitly unselected progress sections while detecting changed task definitions.

At the T7 checkpoint, T8 had not run and no installation had occurred. Local/fake-host checks alone were not claimed as host acceptance; final real-host and installation evidence appears below.

### T8 — Real-Host Pilot Checkpoints, 2026-09-06

Disposable pilot root: `C:\Users\HelloWorld\AppData\Local\Temp\m-pipeline-host-pilot-8tf9krl9`. Two independent fixture repositories use separate docs/worktree roots and one local state store. `tests/fixtures/m-pipeline/pilot.py` prepares requests and validates local artifacts; real host observations and semantic result review remain coordinator-owned.

Five authorized bootstrap tasks were created and their real IDs/cwds verified: architect `01a072f4-76b5-70e0-8536-9e99abbf925e`, executors `01a072f5-78aa-73e1-993b-f35f58273c24` / `01a072f5-8601-7270-8336-6ae1b2639675`, tester `01a072f5-9573-7180-bd33-37355387f2e7`, closer `01a072f5-a3ed-7521-aa83-bd6250631dab`. All completed bootstrap and loaded the explicit local context through the original loader. No context values were copied into coordination records.

The second run correctly waited for the shared architect while the first planning assignment owned it. Pilot A's actual `m-plan` report and root plan were reviewed and accepted at clean commit `5997de320771a66f4b69d49f03fc4bea267a3213`; its two distinct implementation assignments were then sent to separate receivers/worktrees while the architect began pilot B. This is partial evidence, not an end-to-end pass yet.

Live fixture preparation caught a configuration defect: an explicitly configured release-before-archive order was incorrectly treated as a backward edge. Fixed that case while retaining graph-cycle and backward repair restrictions. Added explicit runtime identifier validation and pinned the original skill-root path in handoff envelopes. Eight focused contract checks passed after those changes. Source and installed text for the seven core original skills match; byte hashes for all 67 pre-existing installed m-* files were recorded before installation. The new installed destination was absent.

Further compatibility review fixed immutable tested-candidate handoff across original archive cleanup, including post-archive release retry from retained evidence. This permits archive metadata/merge changes without treating the resulting HEAD as a newly tested product version. Normal execution/test/live-release handoffs still require exact clean HEAD. The post-cleanup regression also rejects changed plan identity. Final full regression after these code fixes: 68 tests, 66 passed, 2 Windows symlink-privilege skips; new package tests alone: 28 tests, 27 passed, 1 of those skips. Package validation and 96 local Markdown links passed. All pre-existing source packages remain unchanged against the baseline.

The sixth real task, fresh executor `01a0730e-3daa-73c1-864a-589d4b88e93d`, loaded the configured context and completed B1 from canonical references without a repeated user explanation. B was paused with outstanding claims; a new dispatch was rejected, completed work was reviewed without replay, and explicit resume succeeded. Both original executors were then verified idle, retired from the local pool and archived through the host after their accepted results. Two live slots remain available within the approved total-creation bound.

Both original m-test passes were reviewed and accepted: A at `35d2061eddee77be0df6881ac1d616c70c282c9f` (31 fixture checks, 12 review items), B at `238bc992e43941e08a81dce6a0f942dc562f63aa` (17 fixture checks, 12 review items). Independent coordinator byte/Git checks confirm source-to-candidate identity, clean state and unchanged reviewed plans. The shared tester was reused sequentially. B's release explicitly returned `shared_resource_busy` while A's release result remained unaccepted, even though A's receiver had finished; no new receiver was created until that claim was released by reviewed acceptance.

Publisher A `01a07319-d53e-7213-8b18-998003f1f4f9` and publisher B `01a0731f-75a9-7050-b472-a1244cd3ccbc` brought the pilot to exactly 8 created tasks and a maximum of 6 unarchived tasks. No further creation is admitted. A's local release marker was independently verified as its tested full commit plus LF; B release and both original archive closeouts remain pending at this checkpoint.

### Implementation Review Checklist

| Review item | Status | Evidence / limitation |
| --- | --- | --- |
| Requirement coverage | Passed for admitted first-release scope | R01–R18 map to T1–T8; final real-host closeout and companion-only installation passed; deferred/mode-specific limits remain explicit |
| Architecture | Passed | Config, persistence and workflow modules separate responsibilities; original phase skills remain authoritative; host calls remain outside the runtime |
| Performance risks: repeated I/O, lock contention | Passed for bounded scope | Filesystem/Git validation occurs before short SQLite transactions; independent-process contention and rollback tests passed; stage scans are bounded by admitted work |
| Performance targets / thresholds | Not specified | No throughput or latency SLO was supplied; no production-scale benchmark is claimed |
| Usability / user path | Passed for verified modes | Setup, explicit launch, wait, split/integrate, shared receiver reuse, pause/resume and fresh receiver worked on the real host; mode-specific gaps are documented |
| Readability / consistency | Passed | Small entry skill routes to focused references; JSON actions and errors use consistent contracts; English commits follow guide.md |
| Extensibility / configuration | Passed | Versioned blueprint, explicit repositories/roles/resources and bounded creation; no unnecessary external dependencies or recursive framework |
| Stability / recovery | Passed in deterministic tests | Unknown outcomes survive restart, no timeout-based ownership release, stale/duplicate receipts and failed non-progress are checked |
| Security / permissions / data exposure | Passed within cooperating-host boundary | Runtime does not prove user authority; coordinator checks actual instructions and artifact evidence. No credentials or context bodies in records/reports; path and scope checks reject invalid assignments |
| Test coverage | Passed with platform skips | Final 68-test suite: 66 passed, 2 Windows symlink-privilege skips; the latter are not claimed as passed |
| Whole-flow validation | Passed | Two real fixture pipelines completed original planning, split execution, integration, testing, local release and original archive/merge/cleanup; both runtime runs finished with no claims or uncertain operations |
| Delegation governance / audit | Passed | No implementation subagents; exactly 8 explicitly authorized pilot tasks with bounded live capacity, distinct Task IDs/write sets, canonical context/docs references and coordinator result review |

The real fixture is static and introduces no UI; screenshot/route/responsive checks are inapplicable. Saved-project worktree creation and pending-ID recovery remain gated by actual host metadata/readiness checks and have no live-pilot claim; deterministic/schema checks cover those paths. Native compaction, background wakeup, deeper/distributed teams and real production remain D1–D4.

### T8 — Completion And Installation, 2026-09-06

Both real runs finished with all seven admitted Task IDs passed. The final audit found exactly 8 created tasks, a maximum observed live count of 6, zero remaining claims and zero uncertain/pending operations. All 8 completed pilot tasks were archived through the host tool. Only each fixture's integration worktree/branch was cleaned by its original m-archive; the other fixture worktrees and durable evidence remain available for review. No production or remote effect occurred.

| Run | Immutable tested/released commit | Local merge commit | Final Progress-only main commit | Original closeout evidence |
| --- | --- | --- | --- | --- |
| A | `35d2061eddee77be0df6881ac1d616c70c282c9f` | `d58952c8d89e7beb95346ec1f939249b3456006b` | `258df2535a4cd12d61d9cd7cd1cc34e1877c2485` | [Archive](C:/Users/HelloWorld/AppData/Local/Temp/m-pipeline-host-pilot-8tf9krl9/docs/a/change/2026-09-06_pilot-a-closeout.md), [receipt](C:/Users/HelloWorld/AppData/Local/Temp/m-pipeline-host-pilot-8tf9krl9/docs/a/plan/host-archive-report.md) |
| B | `238bc992e43941e08a81dce6a0f942dc562f63aa` | `841ae368d74b118ad863e29f0264c4c4f839eae7` | `a82f2fdb32969c80ea6b6ed163c67939180b5fa7` | [Archive](C:/Users/HelloWorld/AppData/Local/Temp/m-pipeline-host-pilot-8tf9krl9/docs/b/change/2026-09-06_pilot-b-closeout.md), [receipt](C:/Users/HelloWorld/AppData/Local/Temp/m-pipeline-host-pilot-8tf9krl9/docs/b/plan/host-archive-report.md) |

Independent coordinator checks verified exact product and release-marker bytes, candidate reachability, clean final main, expected cleanup, preserved other worktrees and metadata-only context records. Each merge tree equals its tested candidate; subsequent commits change only Progress. The runtime accepted immutable tested identities after actual worktree deletion. A report-only Windows separator mismatch was repaired without replaying a completed Git action. B then waited for the shared closer until A's report was reviewed and accepted, and completed the same closeout normally.

Detailed local audit: [final-audit.json](C:/Users/HelloWorld/AppData/Local/Temp/m-pipeline-host-pilot-8tf9krl9/final-audit.json) and [final-host-tasks.json](C:/Users/HelloWorld/AppData/Local/Temp/m-pipeline-host-pilot-8tf9krl9/final-host-tasks.json). These disposable pilot paths are retained as local evidence; the runtime fixture/store is outside project and docs roots.

After those gates passed, verified the exact absolute sync destinations and absence of an existing installed companion, then ran unchanged `tools/sync-skills.ps1 -Skill m-pipeline`. Installation: [m-pipeline/SKILL.md](C:/Users/HelloWorld/.codex/skills/m-pipeline/SKILL.md); generated distribution: `dist/codex/m-pipeline`. All 13 new source files match distribution and installed bytes (excluding the generated build-info file), and all 67 pre-existing installed m-* files and their file set remain byte-identical. All 31 original dependency Markdown/Python files also match source text after newline/BOM normalization; no dependency was rewritten. The installed CLI successfully validated the real fixture blueprint.

| Area | Check | Status | Evidence | Notes |
| --- | --- | --- | --- | --- |
| Regression | Full repository suite | Passed with skips | 68 total: 66 passed, 2 skipped | Windows symlink privilege unavailable |
| Package | Manifest/skill validation and installed CLI | Passed | Unchanged validator; installed blueprint validation | Version 0.1.0, 13 matching new files |
| Compatibility | Original source and installed packages | Passed | Baseline Git comparison; 67 installed byte hashes; 31 dependency text comparisons | Existing manual phases untouched |
| Host integration | Two complete role pipelines | Passed | Original phase receipts and final audit above | 8 created/8 archived; no remaining claims |
| Recovery | Shared waiting, pause/resume, fresh receivers and uncertain outcomes | Passed within stated coverage | Real shared architect/closer/resource waiting, pause/resume and fresh receiver; deterministic fault/retry tests | Pending creation and saved-project mode lack live evidence and remain gated |

Final documentation verification passed for 103 local Markdown links, whitespace and the exact new-scope file boundary. Only documentation changed after the final regression run; no broad test rerun was needed.

T1–T8 are complete. The implementation is committed on `codex/role-pipeline`; the parent repository main remains at its original baseline. This turn does not perform the implementation workflow's own archive, base-branch merge, push or worktree cleanup.
