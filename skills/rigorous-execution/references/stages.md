# Stage Rules

Use this file to execute stages `1` through `4`.

## Global Rules

- Only one stage may be active at a time.
- A workflow may iterate or roll back, but every rollback must:
  - state the reason
  - update the affected plan or archive docs before proceeding
- If information is unclear, missing, ambiguous, or based on an unconfirmed assumption, stop and ask the user instead of guessing.
- Before unresolved issues are fixed, output `问题清单`, mark `阻塞：是`, and forbid advancing or coding.

## Stage 1 - Requirements Analysis

Before drafting stage `1` output:

- if `docs/requirements` exists, read the relevant requirement docs first
- if `docs/README.md` exists, use it as an entry point when it helps locate the right requirement doc
- treat stable requirement docs as higher-priority context than code-only inference when they are present and relevant

Required output:

- 目标
- 范围（必须 / 可选 / 不做）
- 使用场景
- 功能需求
- 非功能需求
- 输入输出
- 边界异常
- 验收标准
- 风险

If anything is unclear, output `问题清单`, mark `阻塞：是`, and stop.

## Stage 2 - Architecture Design

Before drafting stage `2` output:

- if `docs/specs` exists, read the relevant spec docs first
- if `docs/README.md` exists, use it as an entry point when it helps locate the right spec doc
- treat stable spec docs as higher-priority context than code-only inference when they are present and relevant

Required output:

- 总体方案（含选型理由 / 备选对比）
- 模块职责
- 数据 / 调用流
- 接口草案
- 错误与安全
- 性能与测试策略
- 可扩展性设计点

If anything is unclear, output `问题清单`, mark `阻塞：是`, and stop.

## Stage 3.1 - Planning

Requirements:

- Create or update the active worktree-root `plan.md` or `todo.md`.
- Make the document handoff-ready without relying on the current chat.
- If the user already provided a complete `plan.md` or `todo.md`, confirm it instead of rewriting it.
- If the provided plan is incomplete, complete it before implementation.
- Include:
  - project goal and current state
  - repo, branch, base, worktree absolute path, and current stage
  - related requirements, specs, and lessons when already known
  - executable checklist
  - task IDs
  - per-task goal, files, acceptance, tests, rollback
  - dependencies, risks, and notes
- If parallel work is possible, include:
  - owner
  - worktree path
  - plan path
  - write set
  - key context references

Before the plan is confirmed:

```md
阻塞：是
禁止进入 3.2
禁止派发子Agent
```

After confirmation:

```md
阻塞：否
进入 3.2
```

## Stage 3.2 - Implementation

Entry condition:

- stages `1`, `2`, and `3.1` are all unblocked

Rules:

- Map every code change to a Task ID.
- Stay inside the active worktree.
- Perform and report a parallelism assessment before implementation.
- Give a file-level change summary and design notes before editing.
- Include input validation, error handling, logging or observability when applicable, and safe defaults when applicable.
- Enforce code quality expectations:
  - performance: avoid unnecessary I/O, repeated computation, needless copying, N+1 behavior, or avoidable contention
  - readability: clear naming, clear structure, and comments that explain why when needed
  - extensibility: clear module boundaries, low coupling, configurability, and minimal hard-coding
  - architecture: explicit dependency direction and no avoidable circular dependencies
  - maintainability: minimum necessary change surface, rollback awareness, and code-doc consistency
- If best practice is uncertain, present the viable alternatives and ask the user to choose before committing to one.
- Provide runnable validation steps or tests for key and edge paths.
- Do not introduce plan-external changes; if required, return to `3.1` and update the plan first.
- After parallel work completes, the main agent must integrate results, resolve conflicts, and run regression verification.
- Return to `3.1` if the work expands beyond the confirmed plan.

## Stage 3.3 - Code Review

Review each item and mark `通过` or `不通过`:

- 需求覆盖
- 架构合理性
- 性能风险（N+1 / 重复计算 / 多余 I/O / 锁竞争）
- 可读性与一致性
- 可扩展性与配置化
- 稳定性与安全
- 测试覆盖情况
- 子Agent治理与审计（任务映射、上下文完整性、文件所有权、结果复核、冲突处理、记录完整性）

If any item fails, return to `3.2`.

## Stage 4 - Change Archive

Requirements:

- explicitly use `$docs-governor`
- Create `docs/change/YYYY-MM-DD_topic.md`.
- Include:
  - 变更背景 / 目标
  - 具体变更内容
  - `Requirements impact: none | updated`
  - `Specs impact: none | updated`
  - `Lessons impact: none | updated`
  - `Related requirements: ...`
  - `Related specs: ...`
  - `Related lessons: ...`
  - 对应 `plan.md` 任务映射
  - 经验 / 教训摘要
  - 可复用排查线索（症状 / 触发条件 / 关键词 / 快速检查）
  - 关键设计决策与权衡
  - 测试与验证方式 / 结果
  - 潜在影响与回滚方案
  - 子Agent执行轨迹
- If the debugging path was expensive, non-obvious, likely to recur, or exposed a rule worth remembering:
  - create or update the corresponding `docs/lessons/<topic>.md`
  - update `docs/lessons/README.md` and any affected indexes
- Do not leave reusable troubleshooting knowledge only inside `docs/change`.
- Ask whether to end the workflow after the archive is complete.

## Workflow End Confirmation

- If the user says `否`:
  - continue with the next round starting from stage `1`
- If the user says `是`:
  - merge in the repo control-plane
  - merge the worktree `plan.md` into the global `plan.md`
  - move worktree `docs/change` files into the global `docs/change`
  - move worktree `docs/lessons` files and affected lesson indexes into the global docs tree
  - remove and prune the worktree
