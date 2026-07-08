# Testing and Review Rules

Use this reference for `$m-test`, the optional heavy validation phase of `m-autoflow`.

## Scope Boundary

- Lightweight syntax, typecheck, formatting, lint, targeted unit tests, and `git diff --check` belong in `$m-execute`.
- This phase is for heavier validation: integration, end-to-end workflow, manual product review, usability, security, and performance.
- This phase can be skipped for small low-risk changes when execution-stage validation is sufficient.
- If skipped, record why and describe residual risk.

## Skip Decision

Skip this phase when all are true:

- the change is small and low risk
- no cross-service, cross-module, permission, data migration, or user-critical workflow is affected
- execution-stage lightweight checks passed or were reasonably sufficient
- usability, security, and performance impact is trivial or unchanged

Do not skip this phase when any are true:

- the change affects end-to-end user workflows
- the change crosses frontend/backend/service boundaries
- permissions, authentication, authorization, secrets, storage, billing, or data exposure are affected
- performance-sensitive paths, large data, concurrency, background jobs, or external APIs are affected
- prior validation was blocked or inconclusive

## Heavy Validation Scope

- Run integration or end-to-end checks for the changed workflow when practical.
- Validate user-facing usability for critical flows: discoverability, error messages, loading/empty states, recovery, and regressions in common paths.
- Review security boundaries: input trust, authorization, data exposure, secret handling, injection surfaces, and unsafe defaults.
- Review performance indicators: latency-sensitive paths, repeated I/O, N+1 behavior, avoidable O(n^2), memory growth, contention, and configured thresholds where available.
- If a heavy test cannot run, record why and describe residual risk.

## Mandatory Review Checklist

Mark each item `通过` or `不通过`:

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

If all items pass:

```md
阻塞：否
进入归档
```

If skipped:

```md
测试阶段：跳过
跳过原因：<reason>
执行阶段验证：<checks>
残余风险：<risk>
阻塞：否
进入归档
```
