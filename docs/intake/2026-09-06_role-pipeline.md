# 2026-09-06 Role Pipeline

## Source

- Source: the current Codex discussion, following removal of `m-orchestrator` in commit `9f4e0ef` on 2026-09-05.
- Requester: the user.
- Planning was requested explicitly with `$m-plan`; this source brief was captured before execution approval. Subsequent `$m-execute` approved T1–T8, including the bounded fixture pilot and installation of only the new companion. See the active plan for implementation evidence.

## Original Request Evidence

The user initially requested manually managed role sessions and explicit session-to-session handoff, without the previous registration mechanism. They then refined the request:

> 产品经理应该执行 discuss，然后一个架构师应该进行 plan，执行者应该使用 execute，然后测试应该使用 test 之类的。

> 我希望可以手动定义一套流水线，完成和产品经理的交互之后后续全自动工作。

> 注意目前先不要移除和修改原来的 discuss-archive 这一套流程 skill，我自己还在使用，也还有一些场景需要我手动管理的。

> 理论上可以有一个自动创建整个流程需要的 session 的指令，其次一个角色可以交接给多个后续 session。

The user also requested selecting idle executors, optionally creating further execution sessions, and compacting heavily used context or continuing in a fresh session. They asked to make substantial use of `m-docs` and `m-context`, then emphasized compatibility with the existing phases' own invocation of those skills.

## Confirmed Outcomes And Constraints

- Add an optional automation companion; preserve all existing skill packages and manual invocation behavior.
- Keep `m-plan` artifacts, Task IDs, worktree boundaries, acceptance criteria, and phase gates authoritative.
- Configure roles and routing explicitly; allow existing-session bindings and one-command team creation.
- Support multiple concurrent workflow runs, idle-worker selection, bounded session creation, distinct-task fan-out, result joins, and test/repair feedback.
- After a real launch authorization at the product-manager entry, continue within its explicit scope without routine continuation questions.
- Reuse original phase implementations and their `m-docs` calls; provide context references for receivers to load through `m-context`.
- Preserve enough documents, context references, and handoff evidence to replace a session or resume a paused run without reconstructing the task from conversation memory.

## Recommendations Carried Into Planning

These are proposed implementation choices, not statements that the capability already exists:

- Package name: `m-pipeline`.
- One coordinator session per workflow; role sessions perform phase work and can be reused or replaced.
- A small local transactional runtime supports assignment and recovery. No separate project/role registration service or automatic role discovery.
- First release: fixed phase adapters, plan-bounded fan-out and joins, one level of execution children, bounded creation, manual takeover/resume, and fresh-session continuation.
- Native context compaction is an optional enhancement because the current desktop tools do not expose it or context occupancy telemetry.
- `m-archive` retains documentation, merge, and cleanup semantics. Real deployment is a separately configured, explicitly authorized operation of the release role.

## Remaining Technical Evidence

- Establish the host contract first, then verify real desktop creation readiness, message delivery, concurrent claims, exact repository/worktree continuity, and recovery in the bounded execution pilot.
- Do not infer that an idle or completed host turn means the phase passed.
- Do not infer that an App Server method can operate on the desktop's live threads from a separate server process.

## Routed Documents

- [Proposed feature](../features/m-pipeline.md)
- [Requirements](../requirements/m-pipeline.md)
- [Technical specification](../specs/m-pipeline.md)
- [Proposed decision](../decisions/2026-09-06_role-pipeline-composition.md)
- [Active implementation plan](../../plan.md)

## Publication And Phase Status

Planning documents are local to the dedicated `codex/role-pipeline` worktree. No customer pipeline, role sessions, implementation, installation, publication, or change archive was created during planning.
