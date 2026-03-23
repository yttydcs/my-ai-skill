# 2026-03-23 rigorous-execution-alignment

## 变更背景 / 目标

本轮是同一 workflow 的第二次迭代，目标是把 `rigorous-execution` 从“结构化改写版”进一步收紧为更接近原始提示词的法规版，并明确禁止隐式触发。

使用 `$docs-governor` 进行归档检查后的结论：

- Requirements impact: updated
- Specs impact: updated
- Related requirements: `docs/requirements/rigorous-execution-skill.md`
- Related specs: `docs/specs/rigorous-execution-skill.md`
- Lessons: none

## 具体变更内容

### 新增

- 新增本轮归档文档：
  - `docs/change/2026-03-23_rigorous-execution-alignment.md`

### 修改

- 稳定文档：
  - `docs/requirements/rigorous-execution-skill.md`
  - `docs/specs/rigorous-execution-skill.md`
- skill 主体与 references：
  - `skills/rigorous-execution/SKILL.md`
  - `skills/rigorous-execution/references/initialization.md`
  - `skills/rigorous-execution/references/stages.md`
  - `skills/rigorous-execution/references/docs-governor-integration.md`
  - `skills/rigorous-execution/references/subagents.md`
  - `skills/rigorous-execution/references/templates.md`
- 触发策略：
  - `skills/rigorous-execution/agents/openai.yaml`
    - 新增 `policy.allow_implicit_invocation: false`
- 安装元数据：
  - `manifests/rigorous-execution.json`
    - 新增 `manual_invocation_only: true`
- 规划与索引：
  - `plan.md`
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

- `RF-1`：补强稳定 requirement/spec 契约，已完成。
- `RF-2`：补强 skill/references 并关闭隐式触发，已完成。
- `RF-3`：重新 validate 与 sync 安装副本，已完成。
- `RF-4`：完成 review 与 iteration 2 archive，已完成。

## 关键设计决策与权衡

1. 用 `openai.yaml` policy 显式关闭隐式触发，而不是只在文案里写“请手动触发”。
   - 原因：只有 metadata policy 才是真正的触发控制。
   - 权衡：仍然保留描述文本，帮助人类和模型理解该技能的使用边界。

2. 保持 progressive disclosure，不把原始长提示词整段塞回 `SKILL.md`。
   - 原因：这样仍然能长期维护，并减少每次调用的上下文负担。
   - 权衡：结果不是“逐字复制版”，而是“语义尽量等价、结构化拆分版”。

3. 迭代 2 只更新已有 stable docs，不新增新的 requirement/spec leaf doc。
   - 原因：这一轮是澄清和收紧既有契约，而不是引入新的能力类别。
   - 权衡：变更历史需要通过新的 `docs/change` 归档来追踪，而不是通过新增 stable docs 来表达。

## 测试与验证方式 / 结果

- 结构校验：
  - 执行：`tools/validate-skills.ps1 -Skill rigorous-execution -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - 结果：通过，`Skill is valid!`

- 安装同步：
  - 执行：`tools/sync-skills.ps1 -Skill rigorous-execution`
  - 结果：成功更新 `dist/codex/rigorous-execution` 与 `C:\Users\HelloWorld\.codex\skills\rigorous-execution`

- 手动触发策略核验：
  - 执行：检查源码与安装副本中的 `agents/openai.yaml`
  - 结果：两者均包含 `policy.allow_implicit_invocation: false`

- 规则收紧核验：
  - 执行：扫描以下关键文本是否存在
    - `Manual invocation only`
    - `Only one stage may be active at a time`
    - `rollback`
    - `allow_implicit_invocation`
  - 结果：源码与稳定 docs 均已包含对应约束

## 潜在影响

- `rigorous-execution` 现在应只在显式写出 `$rigorous-execution` 时被使用，而不是被动自动注入。
- 本轮提高了对原始提示词的语义契合度，但仍保留“主 skill + references”结构，而非逐字粘贴长 prompt。

## 回滚方案

1. 回滚以下 iteration 2 变更：
   - `docs/requirements/rigorous-execution-skill.md`
   - `docs/specs/rigorous-execution-skill.md`
   - `skills/rigorous-execution/**`
   - `manifests/rigorous-execution.json`
   - `docs/change/README.md`
   - `docs/change/2026-03-23_rigorous-execution-alignment.md`
   - `plan.md`
2. 删除更新后的安装副本并重新同步 iteration 1 版本：
   - `C:\Users\HelloWorld\.codex\skills\rigorous-execution`
3. 如需清理构建产物，删除：
   - `dist/codex/rigorous-execution`

## 子Agent执行轨迹

- 本轮 iteration 2 仍未使用子Agent。
- 原因：当前宿主策略要求先获得用户对并行 agent 的显式授权，本轮未收到该授权；因此即使技能规则更严格，执行层仍需服从宿主策略。
