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

Ask whether to end the workflow after archive completion.

Only after explicit confirmation:

1. verify worktree and repo status
2. preserve unrelated dirt
3. commit or merge only workflow-owned product changes
4. move/archive worktree plan and change docs into the governed docs tree when project rules require it
5. merge from the control-plane repo path
6. remove junctions or path-scoped processes when needed for Windows worktree cleanup
7. remove/prune the worktree and delete the local feature branch when safe
8. report whether the result is local-only or pushed
