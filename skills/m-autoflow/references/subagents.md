# Sub-agent Governance

Use this file only in stages `3.2` and `3.3`.

## Phase Boundary

- Sub-agents are forbidden in stages `1`, `2`, `3.1`, and `4`.

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

## Hard Preconditions

Do not delegate unless all of these are true:

- the active `plan.md` or `todo.md` is confirmed
- the delegated task has a clear Task ID
- the task has a bounded write set
- the context package is complete
- host platform policy allows delegation
- user authorization exists when the host requires it

## Non-delegable Responsibilities

The main agent must retain responsibility for:

- worktree creation
- `plan.md` or `todo.md` generation and confirmation
- requirements and architecture decisions
- file ownership definition
- conflict handling
- code integration
- final acceptance
- external status reporting

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

## Required Sub-agent Output

Every delegated result must include:

- changed files
- key design points
- test and validation results
- risks and rollback notes
- whether the assigned Task ID is fully satisfied

## Audit Rules

- The main agent remains responsible for integration and final acceptance.
- Review every sub-agent result before marking the task done.
- Record the delegation path in the final change archive.
