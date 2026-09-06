# Sub-agent Governance

Use this file only in stages `3.2` and `3.3`.

## Phase Boundary

- Sub-agents are forbidden in stages `1`, `2`, `3.1`, and `4`.
- Exception: `$m-discuss` may use read-only research sub-agents when the user explicitly asks for web research or current external facts and host policy permits delegation.
- The research exception does not allow code edits, worktree changes, plan confirmation, implementation, validation, archive, merge, or cleanup delegation.
- `$m-go` is a strict delegated execution entry for stages `3.2` and `3.3`: implementation edits must be done by worker sub-agents, while the main agent coordinates and audits.
- `$m-continue` preserves the delegation policy of the `$m-execute` and `$m-test` behavior it applies. Invoking `$m-continue` authorizes repeated in-scope iterations, not mandatory sub-agent use.

## Mandatory Parallelism Assessment

On entry to `3.2` or `3.3`, assess whether:

- there are two or more independently acceptable Task IDs
- write sets can be split cleanly
- implementation, tests, review, or verification can run in parallel
- there is non-critical validation work that can proceed independently

If host policy permits delegation, user authorization exists when required, and any of those conditions are true, the main agent must create sub-agents unless a concrete write-set or coupling conflict makes delegation unsafe.

If sub-agents are not used, state why, such as:

- write-set conflict
- unsafe coupling
- insufficient context separation
- host policy or user-authorization limits

For `$m-discuss` research, assess whether the research can be split into independent read-only lanes. Use parallel research sub-agents only when this split is clear, and record the lanes plus synthesis responsibility.

For `$m-go`, do not skip sub-agents for implementation edits. If delegation is unavailable or unsafe, block `$m-go` instead of falling back to main-agent implementation.

For `$m-continue`, reassess parallelism when returning to execution or review, but do not infer `$m-go` worker-only authorization. Continue directly when delegation is not authorized and the applied `$m-execute` or `$m-test` rules permit main-agent work.

## Hard Preconditions

Do not delegate unless all of these are true:

- the active `plan.md` or `todo.md` is confirmed
- the delegated task has a clear Task ID
- the task has a bounded write set
- the context package is complete
- host platform policy allows delegation
- user authorization exists when the host requires it

For `$m-go`, the user's `$m-go` invocation counts as authorization for worker sub-agent execution within the approved plan scope when host policy permits delegation.

For research-only delegation, the active plan may be absent, but all of these must be true:

- the user explicitly requested web research
- each lane is read-only
- each lane has a bounded research question
- source quality expectations are specified
- the main agent will review sources and synthesize findings
- host platform policy allows delegation
- user authorization exists when the host requires it

## Non-delegable Responsibilities

The main agent must retain responsibility for:

- worktree creation
- `plan.md` or `todo.md` generation and confirmation
- requirements and architecture decisions
- research synthesis and final source trust decisions
- file ownership definition
- conflict handling
- code integration
- final acceptance
- external status reporting

For `$m-go`, if integration requires file edits, those edits must be delegated to a worker with a bounded write set. The main agent may inspect files, run commands, review diffs, and decide acceptance, but must not directly edit implementation files.

## Inheritance Rule

- Sub-agents must inherit the main agent's model and reasoning configuration.
- Do not manually downgrade or override them unless the host platform requires an exact inherited value.

## Required Context Package

Every delegated task must include:

- 阶段：`3.2` or `3.3`
- Workflow 目标
- 当前仓库
- 当前分支
- Base 分支
- Worktree 绝对路径
- 必须遵守的计划文档绝对路径
- 对应 Task ID / 标题
- 任务目标
- 验收条件
- 对应 AC ID、来源约束和验证边界；保留否定要求、数值、默认值与顺序
- 测试点
- 回滚点
- 允许修改的文件 / 目录
- 禁止修改的文件 / 目录
- 相关需求 / 架构摘要
- 关键代码 / 文档引用

## Dispatch Rules

Tell each sub-agent:

- only complete the assigned Task ID
- obey the specified plan file
- stay inside the write set
- do not add plan-external changes
- do not revert user or other agent changes
- report changed files, test results, risks, and completion status
- if working under `$m-go`, remember that other workers may be active and accommodate their changes without reverting them

## Required Sub-agent Output

Every delegated result must include:

- changed files
- key design points
- test and validation results
- acceptance IDs with evidence and unresolved/waived items, plus the reviewed candidate identity when applicable
- risks and rollback notes
- whether the assigned Task ID is fully satisfied

## Audit Rules

- The main agent remains responsible for integration and final acceptance.
- Review every sub-agent result before marking the task done.
- Record the delegation path in the final change archive.
