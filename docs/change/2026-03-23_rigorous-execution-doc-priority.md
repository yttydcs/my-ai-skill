# 2026-03-23 rigorous-execution-doc-priority

## 变更背景 / 目标

本轮 iteration 3 的目标是让 `$rigorous-execution` 在显式触发后，于阶段 `1` 和 `2` 优先检查稳定文档，而不是默认先从代码或对话上下文推断。

使用 `$docs-governor` 进行归档检查后的结论：

- Requirements impact: updated
- Specs impact: updated
- Related requirements: `docs/requirements/rigorous-execution-skill.md`
- Related specs: `docs/specs/rigorous-execution-skill.md`
- Lessons: none

## 具体变更内容

### 新增

- 新增本轮归档文档：
  - `docs/change/2026-03-23_rigorous-execution-doc-priority.md`

### 修改

- skill 主体：
  - `skills/rigorous-execution/SKILL.md`
    - 明确阶段 `1` 优先看 `docs/requirements`
    - 明确阶段 `2` 优先看 `docs/specs`
- 阶段规则：
  - `skills/rigorous-execution/references/stages.md`
    - 为阶段 `1` 和 `2` 增加稳定文档优先读取规则
- 稳定文档：
  - `docs/requirements/rigorous-execution-skill.md`
  - `docs/specs/rigorous-execution-skill.md`
- 归档索引：
  - `docs/change/README.md`
- 计划记录：
  - `plan.md`

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

- `RP-1`：补强 stable requirement/spec，对阶段 `1`/`2` 的 docs 优先读取做持久化约束，已完成。
- `RP-2`：更新 skill 主体和 stage references，使 docs 优先读取成为显式流程规则，已完成。
- `RP-3`：重新 validate 并 sync 安装副本，已完成。
- `RP-4`：完成 review 与 iteration 3 archive，已完成。

## 关键设计决策与权衡

1. 把“优先读 docs”同时写进 `SKILL.md` 和 `references/stages.md`。
   - 原因：前者保证入口可见，后者保证阶段执行时有明确步骤。
   - 权衡：存在少量重复，但可读性更高。

2. 让阶段 `1` 对应 `docs/requirements`，阶段 `2` 对应 `docs/specs`。
   - 原因：这与 requirements/specs 的职责边界一致，减少阶段语义混淆。
   - 权衡：当仓库只有其中一类文档时，另一阶段仍需回退到代码和用户澄清。

3. 把稳定文档视为高优先级上下文，而不是绝对真理。
   - 原因：若文档缺失、冲突或不完整，流程仍需要阻塞并提问，而不是盲从旧文档。
   - 权衡：阶段执行仍然需要做冲突判断，不能机械读取。

## 测试与验证方式 / 结果

- 结构校验：
  - 执行：`tools/validate-skills.ps1 -Skill rigorous-execution -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - 结果：通过，`Skill is valid!`

- 安装同步：
  - 执行：`tools/sync-skills.ps1 -Skill rigorous-execution`
  - 结果：成功更新 `dist/codex/rigorous-execution` 与 `C:\Users\HelloWorld\.codex\skills\rigorous-execution`

- 安装副本核验：
  - 执行：检查安装副本中的 `SKILL.md` 与 `references/stages.md`
  - 结果：已包含阶段 `1`/`2` 对 `docs/requirements`、`docs/specs` 的优先读取规则

## 潜在影响

- 以后显式调用 `$rigorous-execution` 时，如果仓库有稳定 docs，阶段 `1`/`2` 会更早锚定现有 requirements/specs。
- 这会降低仅靠代码推断需求/架构的概率，但也更依赖仓库文档质量。

## 回滚方案

1. 回滚以下 iteration 3 变更：
   - `skills/rigorous-execution/SKILL.md`
   - `skills/rigorous-execution/references/stages.md`
   - `docs/requirements/rigorous-execution-skill.md`
   - `docs/specs/rigorous-execution-skill.md`
   - `docs/change/README.md`
   - `docs/change/2026-03-23_rigorous-execution-doc-priority.md`
   - `plan.md`
2. 删除更新后的安装副本并重新同步上一版本：
   - `C:\Users\HelloWorld\.codex\skills\rigorous-execution`
3. 如需清理构建产物，删除：
   - `dist/codex/rigorous-execution`

## 子Agent执行轨迹

- 本轮 iteration 3 未使用子Agent。
- 原因：该修改范围小、写集集中，且本轮不需要并行拆分即可安全完成。
