# Stage Rules

Use this file to coordinate the `m-autoflow` phases.

## Global Rules

- `$m-orchestrator` is a project-level companion above separate task workflows. It may schedule their existing phase skills but does not become a stage or relax any per-task gate.
- Only one stage may be active at a time.
- `$m-quick` is a standalone docs-first fast path outside the stage chain; it may directly edit one selected repository only after its own low-risk gate passes.
- `$m-discuss` owns discovery, brainstorming, optional web research, and early worktree setup.
- `$m-plan` owns architecture and executable planning.
- `$m-execute` owns implementation and lightweight validation.
- `$m-go` owns delegated implementation orchestration and automatic `$m-test` looping after planning.
- `$m-continue` owns unattended state recovery and repeated reuse of `$m-execute` and `$m-test` after either phase has already run.
- `$m-test` owns optional heavy validation and review.
- `$m-archive` owns change archive, lessons, default workflow closeout, merge, and cleanup.
- Do not run web research by default; use it from `$m-discuss` only when current external facts or best practices matter.
- An orchestrated Worker uses `$m-execute` for implementation and lightweight validation. It may enter a temporary `$m-test` role only after the orchestrator verifies a passing gate for the current change state.
- A workflow may iterate or roll back, but every rollback must:
  - state the reason
  - update the affected plan or archive docs before proceeding
- If information is unclear, missing, ambiguous, or based on an unconfirmed assumption, stop and ask the user instead of guessing.
- Before unresolved issues are fixed, output `问题清单`, mark `阻塞：是`, and forbid advancing or coding.

## Standalone Fast Path - m:quick

`$m-quick` does not enter discuss, plan, implementation, test, or archive stages.

Before editing:

- read project-local instructions
- identify `project_root`, governed `docs_root`, and exactly one target code repository
- explicitly use `$m-docs` to read the minimum relevant indexes and stable leaf docs
- inspect Git status, pre-existing diffs, nearby code, and focused validation surfaces
- apply the eligibility and automatic-escalation rules from `../../m-quick/references/quick.md`

When the gate passes:

- let the main agent edit the selected current checkout directly
- do not create a quick-request branch, worktree, root plan, intake record, plan archive, or change archive by default
- run focused validation and require actual operation plus screenshot evidence for UI-impacting work
- update stable docs through `$m-docs` only when stable truth changed
- output the direct `$m-quick` result table

When the gate fails, do not silently enter or create a staged workflow. Recommend `$m-discuss` for unclear intent or conflicting truth, or `$m-plan` for clear but coordinated or high-risk work.

Project-local instructions may require a commit. Push, publication, deployment, merge, archive, and backup choices remain explicit user decisions.

## Discuss - Discovery And Requirements Shaping

Before drafting discuss output:

- identify `project_root`, `docs_root`, `code_repos`, and `active_worktree` when private docs or multi-repo boundaries matter
- if `docs/intake` exists, read relevant original request evidence when traceability matters
- if `docs/features` exists, read relevant feature docs first for user-visible behavior
- if `docs/requirements` exists, read the relevant requirement docs first
- if `docs/README.md` exists, use it as an entry point when it helps locate the right requirement doc
- treat stable docs from the selected docs root as higher-priority context than code-only inference when they are present and relevant

Required output:

- 原始请求 / 来源
- 目标
- 范围（必须 / 可选 / 不做）
- 假设
- 问题清单
- 可行方案
- 被拒绝方案与原因
- 推荐方向
- research 摘要与 citation（如使用）
- worktree / branch / docs root 状态

If anything is unclear, output `问题清单`, mark `阻塞：是`, and stop before planning.

## Plan - Architecture And Execution Planning

Before drafting plan output:

- consume the `$m-discuss` brief when it exists
- if `docs/specs` exists, read the relevant spec docs first
- if `docs/decisions` exists, read relevant decision docs when architecture choices constrain the work
- if `docs/README.md` exists, use it as an entry point when it helps locate the right spec doc
- treat stable specs and decisions as higher-priority context than code-only inference when they are present and relevant
- reject unreasonable, unsafe, contradictory, or under-specified requirements and return to `$m-discuss`

Required output:

- 使用场景
- 功能需求
- 非功能需求
- 输入输出
- 边界异常
- 验收标准
- 风险

- 总体方案（含选型理由 / 备选对比）
- 模块职责
- 数据 / 调用流
- 接口草案
- 错误与安全
- 性能与测试策略
- 可扩展性设计点
- direct task summary table with Task ID, title, execution scope, files/modules, acceptance/tests, and risk/notes

Plan artifact requirements:

- Create or update the active worktree-root `plan.md` or `todo.md`.
- Make the document handoff-ready without relying on the current chat.
- If the user already provided a complete `plan.md` or `todo.md`, confirm it instead of rewriting it.
- If the provided plan is incomplete, complete it before implementation.
- After creating or confirming the active plan, output a concise task summary table directly to the user. The table summarizes `plan.md` / `todo.md` and must preserve the `Will Execute` / `Will Not Execute Now` split.
- Include:
  - project goal and current state
  - repo, branch, base, project root, docs root, code repos, worktree absolute path, and current stage
  - related intake, features, requirements, specs, decisions, and lessons when already known
  - stable-doc impact for intake, features, requirements, specs, and decisions
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

- discuss and plan are unblocked, or direct plan invocation recorded why discuss was skipped

Execution entry choices:

- `$m-execute` is the normal implementation entry and may use sub-agents when the parallelism assessment allows it.
- `$m-go` is the high-automation implementation entry; it requires worker sub-agents for all implementation edits and automatically enters `$m-test` behavior after delegated execution converges.
- `$m-continue` is the continuation entry after an `$m-execute` or `$m-test` pass. It preserves `$m-execute` delegation policy, automatically alternates execute repairs and test evaluation, and does not ask whether to continue after ordinary failures.
- `$m-quick` is not a stage `3.2` entry and does not weaken the worktree or confirmed-plan gates in this section.

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
- In `$m-go` flows, the main agent must coordinate, inspect, run commands, and accept or reject worker results, but any implementation or integration file edit must be delegated to a worker with a bounded write set.
- Return to `3.1` if the work expands beyond the confirmed plan.
- Run lightweight implementation validation before leaving this stage when practical:
  - syntax checks
  - type checks
  - formatting checks scoped to touched files
  - lint checks scoped to touched files
  - focused unit tests for changed logic
  - `git diff --check`
- If a lightweight check is not practical, record why and carry the residual risk into stage `3.3` or the archive.

## Stage 3.3 - Code Review

First decide whether heavy testing / review is needed. This stage may be skipped when the user explicitly chooses to proceed directly to `$m-archive`, or for low-risk small changes when stage `3.2` lightweight validation is sufficient.

If skipped, record:

- skip reason
- whether the skip was an explicit user choice
- stage `3.2` checks that passed
- residual risk
- why integration, usability, security, and performance review are not required or were explicitly accepted as unrun

If not skipped, review each item and mark `通过` or `不通过`:

- 需求覆盖
- 架构合理性
- 性能风险（N+1 / 重复计算 / 多余 I/O / 锁竞争）
- 性能指标或可接受阈值
- 可用性 / 用户路径
- 可读性与一致性
- 可扩展性与配置化
- 稳定性与安全
- 安全边界 / 权限 / 输入输出暴露
- 测试覆盖情况
- 整体流程 / 联调验证
- 子Agent治理与审计（任务映射、上下文完整性、文件所有权、结果复核、冲突处理、记录完整性）

When UI is impacted and `$m-test` runs:

- open the actual application, page, preview, or story
- operate the affected user path
- capture screenshot evidence
- include a concise pass/fail table in the direct user response
- mark the test `不通过` or `阻塞` if UI evidence cannot be gathered

If any item fails, return to `3.2`.

In `$m-go` flows, failed review or test items return to delegated fixes, then the review loop runs again until all acceptance checks pass or a blocker is explicit.

In `$m-continue` flows, one invocation authorizes every iteration inside the existing approved Task IDs and write sets. Any measurable Task, diff, validation, or evidence improvement resets the non-progress count. Stop only after acceptance converges, a hard out-of-scope/external blocker is proven, or three complete repair/test cycles repeat the same failure signature without measurable progress. `$m-continue` stops before archive and reports readiness for `$m-archive` on success.

## Stage 4 - Change Archive

Requirements:

- explicitly use `$m-docs`
- Create `docs/change/YYYY-MM-DD_topic.md` in the selected docs root.
- Include:
  - 变更背景 / 目标
  - 具体变更内容
  - `Intake impact: none | updated`
  - `Feature impact: none | updated`
  - `Requirements impact: none | updated`
  - `Specs impact: none | updated`
  - `Decision impact: none | updated`
  - `Lessons impact: none | updated`
  - `Related intake: ...`
  - `Related features: ...`
  - `Related requirements: ...`
  - `Related specs: ...`
  - `Related decisions: ...`
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
- Do not add docs remotes, push docs, publish docs, or choose backup targets unless the user explicitly asks.
- Close the workflow by default after archive completion.
- Stop after archive only when the user explicitly requested archive-only handling, no merge, no cleanup, or an equivalent pause.

## Archive-only Override And Closeout

- If the user explicitly requests archive-only handling, no merge, no cleanup, or an equivalent pause:
  - stop after archive readiness
  - report retained branch/worktree state
  - continue a later round from the appropriate stage when requested
- Otherwise:
  - merge in the repo control-plane
  - move or link retained plan/change/lesson artifacts into the selected docs root when project rules require it
  - keep docs repo publication and backup decisions separate from code repo merge
  - remove and prune the worktree
