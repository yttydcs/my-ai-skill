# Archive and Closeout Rules

Use this reference for `$m-archive`, the archive phase of `m-autoflow`.

## Required Archive Content

Create `docs/change/YYYY-MM-DD_topic.md` in the selected docs root with:

- 变更背景 / 目标
- 具体变更内容
- Docs root
- `Intake impact: none | updated`
- `Feature impact: none | updated`
- `Requirements impact: none | updated`
- `Specs impact: none | updated`
- `Decision impact: none | updated`
- `Lessons impact: none | updated`
- Related intake
- Related features
- Related requirements
- Related specs
- Related decisions
- Related lessons
- 对应 `plan.md` 任务映射
- 经验 / 教训摘要
- 可复用排查线索（症状 / 触发条件 / 关键词 / 快速检查）
- 关键设计决策与权衡
- 测试与验证方式 / 结果
- 潜在影响与回滚方案
- 子Agent执行轨迹

## Lessons Promotion

Create or update `docs/lessons` when the debugging path was:

- expensive
- non-obvious
- likely to recur
- a reusable workflow rule
- a recurring platform or environment pitfall

Do not leave reusable knowledge only in `docs/change`.

## Private Docs Publication

- A docs root may be a separate local/private Git repository.
- Do not add remotes, change remotes, push, publish, or choose backup targets unless the user explicitly asks.
- If docs changes are local-only, say so in the archive or final status.
- Keep docs repo commits separate from code repo commits when both are involved.

## Closeout

`$m-archive` means "archive and end this workflow" by default. Do not ask for a second workflow-end confirmation after a normal archive invocation.

Stop after archive only when the user explicitly asks for archive-only handling, no merge, no cleanup, or an equivalent pause.

When an orchestrated Worker enters this phase, verify that the Task owns the active project integration lease before the first archive or integration mutation. `WAITING_FOR_MERGE`, `next_ready`, and host messages are retry signals only. Archive does not acquire Tester host capacity and does not create a global archive lock; project scheduling remains owned by `$m-orchestrator`. Direct standalone archive invocations retain the normal entry gate above.

Default closeout sequence:

1. verify worktree and repo status
2. preserve unrelated dirt
3. commit or merge only workflow-owned product changes
4. move/archive worktree plan and change docs into the governed docs tree when project rules require it
5. merge from the control-plane repo path
6. remove junctions or path-scoped processes when needed for Windows worktree cleanup
7. remove/prune the worktree and delete the local feature branch when safe
8. report whether the result is local-only or pushed

For a multi-repository workflow:

- preflight every participating repository before the first merge;
- use the dependency/integration order recorded by the approved plan or Task manifest;
- keep docs-repository commits separate from code-repository commits;
- record archive, commit, merge, validation, and cleanup status per repository;
- do not describe independent Git merges as atomic;
- if a later repository fails after earlier integration succeeded, stop, preserve all worktrees needed for recovery, report completed and pending repositories, and require an explicit recovery decision rather than claiming closeout.

## User-facing Closeout

- Lead with whether archive and closeout completed or where they stopped.
- Link archive and lessons artifacts with absolute clickable paths.
- Use a compact archive / merge / cleanup / remaining-state table when several repositories or states are involved.
- Emit supported Git components only for successful actions completed during this closeout; never emit them for planned or failed actions.
