# 2026-03-23 rigorous-execution-invocation-policy

## 变更背景 / 目标

本轮目标是移除 `rigorous-execution` 对隐式触发的显式禁用配置，并将仓库中的稳定文档与安装元数据同步到一致状态，方便后续按宿主实际行为进行测试。

使用 `$docs-governor` 进行归档检查后的结论：

- Requirements impact: updated
- Specs impact: updated
- Related requirements: `docs/requirements/rigorous-execution-skill.md`
- Related specs: `docs/specs/rigorous-execution-skill.md`
- Lessons: none

## 具体变更内容

### 新增

- 新增本轮归档文档：
  - `docs/change/2026-03-23_rigorous-execution-invocation-policy.md`

### 修改

- 触发元数据：
  - `skills/rigorous-execution/agents/openai.yaml`
    - 删除 `policy.allow_implicit_invocation: false`
- 安装元数据：
  - `manifests/rigorous-execution.json`
    - 删除 `manual_invocation_only: true`
- skill 主体：
  - `skills/rigorous-execution/SKILL.md`
    - 将“只允许手动调用”调整为“支持显式调用，但不再在元数据层禁止隐式选择”
- 稳定文档：
  - `docs/requirements/rigorous-execution-skill.md`
  - `docs/specs/rigorous-execution-skill.md`
    - 同步更新触发契约描述
- 索引：
  - `docs/change/README.md`

### 删除

- 无。

## Requirements impact

- updated

## Specs impact

- updated

## Related requirements

- `docs/requirements/rigorous-execution-skill.md`

## Related specs

- `docs/specs/rigorous-execution-skill.md`

## 对应 plan.md 任务映射

- 本轮未单独维护新的 root `plan.md` 任务编号；本次为用户定向触发策略调整。

## 关键设计决策与权衡

1. 同时删除 `openai.yaml` 和 manifest 中的 manual-only 约束，而不是只删一处。
   - 原因：避免源码、元数据、稳定文档三者互相矛盾。
   - 权衡：宿主后续是否真的会隐式选中该 skill，仍取决于会话侧 catalog 和路由策略，而不只取决于本仓库。

2. 保留 `$rigorous-execution` 的显式调用文案，但不再把它写成唯一入口。
   - 原因：显式调用仍是最可控的测试方式。
   - 权衡：文案变得稍宽，但和当前配置更一致。

## 测试与验证方式 / 结果

- 结构校验：
  - 执行：`tools/validate-skills.ps1 -Skill rigorous-execution`
  - 结果：通过，`Skill is valid!`

- 安装同步：
  - 执行：`tools/sync-skills.ps1 -Skill rigorous-execution`
  - 结果：成功更新 `dist/codex/rigorous-execution` 与 `C:\Users\HelloWorld\.codex\skills\rigorous-execution`

- 安装副本检查：
  - 执行：检查安装目录中的 `agents/openai.yaml`
  - 结果：安装副本中已不再包含 `allow_implicit_invocation` 配置

## 潜在影响

- `rigorous-execution` 不再在 skill 元数据层禁止隐式选择。
- 这不会自动保证它出现在每个会话的可用 skill 列表中；宿主侧是否收录、是否选择，仍取决于会话环境。

## 回滚方案

1. 回滚以下文件：
   - `skills/rigorous-execution/agents/openai.yaml`
   - `manifests/rigorous-execution.json`
   - `skills/rigorous-execution/SKILL.md`
   - `docs/requirements/rigorous-execution-skill.md`
   - `docs/specs/rigorous-execution-skill.md`
   - `docs/change/README.md`
   - `docs/change/2026-03-23_rigorous-execution-invocation-policy.md`
2. 删除已安装副本并重新同步旧版本：
   - `C:\Users\HelloWorld\.codex\skills\rigorous-execution`
3. 如需清理构建产物，删除：
   - `dist/codex/rigorous-execution`

## 子Agent执行轨迹

- 本轮未使用子Agent。
- 原因：本次改动范围小，主Agent可直接完成实现、校验与安装。
