# Testing and Review Rules

Use this reference for `$m-test`, the optional heavy validation phase of `m-autoflow`.

## Scope Boundary

- Lightweight syntax, typecheck, formatting, lint, targeted unit tests, and `git diff --check` belong in `$m-execute`.
- This phase is for heavier validation: integration, end-to-end workflow, manual product review, usability, security, and performance.
- This phase can be skipped for small low-risk changes when execution-stage validation is sufficient.
- The user may also explicitly skip this phase and proceed directly to `$m-archive`.
- If skipped, record why, who accepted the skip when relevant, and describe residual risk.
- Lightweight requirements/standards review belongs to execution and remains required unless explicitly waived. Apply `../../m-autoflow/references/review.md` for candidate coverage, identity and evidence reuse; a heavy-test skip is not a review waiver.

## Skip Decision

Skip this phase when all are true:

- the change is small and low risk
- no cross-service, cross-module, permission, data migration, or user-critical workflow is affected
- execution-stage lightweight checks passed or were reasonably sufficient
- usability, security, and performance impact is trivial or unchanged

Do not skip this phase when any are true:

- the change affects end-to-end user workflows
- the change affects UI and the user did not explicitly choose to skip `$m-test`
- the change crosses frontend/backend/service boundaries
- permissions, authentication, authorization, secrets, storage, billing, or data exposure are affected
- performance-sensitive paths, large data, concurrency, background jobs, or external APIs are affected
- prior validation was blocked or inconclusive

If the user explicitly chooses to skip `$m-test`, do not run its heavy checks. Proceed to `$m-archive` when the existing acceptance and lightweight-review gates permit it; otherwise return for the missing in-scope review/repair. Record the skip, missing evidence and residual risk. Do not fabricate test results or mark an unverified AC passed.

## Heavy Validation Scope

- Run integration or end-to-end checks for the changed workflow when practical.
- For an approved multi-repository workflow, validate the complete persisted worktree set and the affected cross-repository path; do not substitute unrelated default checkouts for Task worktrees.
- Validate user-facing usability for critical flows: discoverability, error messages, loading/empty states, recovery, and regressions in common paths.
- Review security boundaries: input trust, authorization, data exposure, secret handling, injection surfaces, and unsafe defaults.
- Review performance indicators: latency-sensitive paths, repeated I/O, N+1 behavior, avoidable O(n^2), memory growth, contention, and configured thresholds where available.
- If a heavy test cannot run, record why and describe residual risk.
- Report repository-specific evidence plus the aggregate verdict when failures or skips differ between participating repositories.
- Attach results to the plan's AC IDs and Task IDs. Recheck only evidence affected by code, dependency, source or acceptance changes; preserve current results with their identity instead of rerunning them at each stage.

## UI Validation Evidence

When `$m-test` runs and the change affects UI, visible layout, components, styles, routes, interaction, forms, dialogs, state display, or responsive behavior:

- open the actual application, page, preview, or story that exercises the changed UI
- perform the affected user operations, not only load the initial page
- capture screenshot evidence for the validated state
- include desktop viewport evidence at minimum
- include mobile viewport evidence when responsive behavior or mobile layout may be affected
- record the URL, viewport, operation path, screenshot path, findings, and conclusion
- embed one or two representative screenshots in the direct response with concise alt text, then link additional evidence

If the UI cannot be opened or operated because of environment, auth, dependency, build, or runtime issues, mark the UI validation as `不通过` or `阻塞`. Do not count it as a skipped pass.

If the user explicitly skips `$m-test`, UI screenshots are not required during this phase because the phase did not run. The missing UI evidence and residual risk must be carried into `$m-archive`; this does not skip lightweight requirements/standards review.

## Direct Result Table

Always include a concise table in the direct user response so the user can see the verdict without opening markdown files.

Minimum columns:

- Area
- Check
- Status (`通过` / `不通过` / `阻塞` / `跳过`)
- Evidence
- Notes

For UI-impacting changes where `$m-test` runs, include at least one row for actual UI operation and screenshot evidence. Use an absolute clickable path in the row and embed representative evidence below the table.

Example:

```md
| Area | Check | Status | Evidence | Notes |
| --- | --- | --- | --- | --- |
| UI | Open affected page and operate key path | 通过 | [desktop evidence](/absolute/worktree/artifacts/ui/personnel-edit-desktop.png) | Desktop path verified |
| UI | Mobile responsive state | 跳过 | none | Not affected by this change |
| Security | Permission boundary | 通过 | review | No auth surface changed |
```

## Mandatory Review Checklist

For applicable heavy checks, record `通过`, `不通过`, `阻塞` or `跳过`; explain non-applicable items instead of claiming a check ran. Reuse the separate requirements/standards results from the shared review contract rather than conflating them with heavy checks:

- 需求覆盖
- 架构合理性
- 性能风险（N+1 / 重复计算 / 多余 I/O / 锁竞争）
- 性能指标 / 阈值
- 可用性 / 用户路径
- 可读性与一致性
- 可扩展性与配置化
- 稳定性与安全
- 安全边界 / 权限 / 数据暴露
- 测试覆盖情况
- 整体流程 / 联调验证
- 子Agent治理与审计（任务映射、上下文完整性、文件所有权、结果复核、冲突处理、记录完整性）

## Failure Handling

If any item is `不通过`:

```md
问题清单
- <failed item and reason>

阻塞：是
返回执行
禁止进入归档
```

If all required items pass, current lightweight review permits progression, and any unrun items have an allowed explicit disposition:

```md
阻塞：否
进入归档
```

If heavy testing is skipped and the independent lightweight-review/acceptance gates permit archive (otherwise return for the affected review or repair):

```md
测试阶段：跳过
跳过原因：<reason, including explicit user choice when applicable>
执行阶段验证：<checks>
残余风险：<risk>
阻塞：否
进入归档
```
