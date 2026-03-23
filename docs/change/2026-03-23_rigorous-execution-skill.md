# 2026-03-23 rigorous-execution-skill

## 变更背景 / 目标

本次 workflow 的目标是把用户定义的严谨 AI 实现流程固化为一个可复用的 `rigorous-execution` skill，而不是继续依赖一次性的长提示词。

使用 `$docs-governor` 完成归档前检查后的结论如下：

- Requirements impact: updated
- Specs impact: updated
- Related requirements: `docs/requirements/rigorous-execution-skill.md`
- Related specs: `docs/specs/rigorous-execution-skill.md`
- Lessons: none

## 具体变更内容

### 新增

- skill 包：
  - `skills/rigorous-execution/SKILL.md`
  - `skills/rigorous-execution/agents/openai.yaml`
  - `skills/rigorous-execution/references/initialization.md`
  - `skills/rigorous-execution/references/stages.md`
  - `skills/rigorous-execution/references/docs-governor-integration.md`
  - `skills/rigorous-execution/references/subagents.md`
  - `skills/rigorous-execution/references/templates.md`
- 安装元数据：
  - `manifests/rigorous-execution.json`
- 仓库稳定文档：
  - `docs/requirements/rigorous-execution-skill.md`
  - `docs/specs/rigorous-execution-skill.md`
- docs 索引骨架：
  - `docs/README.md`
  - `docs/requirements/README.md`
  - `docs/specs/README.md`
  - `docs/plan/README.md`
  - `docs/change/README.md`
  - `docs/lessons/README.md`

### 修改

- `plan.md`
  - 用当前 workflow 的初始化、需求、架构、任务拆分、实施记录、Review 和归档结果替换了失效的旧 plan。
- `docs/change/README.md`
  - 补充了新的归档索引项，并保持按时间倒序排列。

### 删除

- 无。

## 对应 plan.md 任务映射

- `RE-1`：补齐仓库 docs 治理骨架并新增稳定 requirement/spec，已完成。
- `RE-2`：使用官方 `init_skill.py` 初始化 `rigorous-execution` skill，已完成。
- `RE-3`：编写 skill 主体、references，并修正初始化时 `$` 被 PowerShell 吞掉的默认 prompt，已完成。
- `RE-4`：新增 manifest，完成 validate 与 copy-sync，已完成。
- `RE-5`：完成 review 与归档，已完成。

## 关键设计决策与权衡

1. 保持 `SKILL.md` 精简，把重规则拆到 `references/`。
   - 原因：触发元数据和主技能体需要保持紧凑，避免每次调用都加载完整长流程。
   - 权衡：需要通过引用文件维护更多边界，但长期更易演进。

2. 显式依赖 `$docs-governor`，而不是把其规则复制进新 skill。
   - 原因：文档治理已经有专门 skill，复制会造成双份真相和后续漂移。
   - 权衡：新 skill 的完整能力依赖 `docs-governor` 可用。

3. 在仓库级补齐 `docs/` 骨架，并为新 skill 新增稳定 `requirements/specs` 文档。
   - 原因：用户 workflow 强制要求在 `3.1` 和 `4` 做 requirement/spec impact 检查；没有稳定文档会削弱审计性。
   - 权衡：本轮不仅新增 skill，也同步引入了仓库级文档治理结构。

4. 复用已有 `validate-skills.ps1` 与 `sync-skills.ps1`，不新增新的仓库工具脚本。
   - 原因：当前仓库工具已经按 skill 名参数化，继续复用能降低维护成本。
   - 权衡：manifest 只承载轻量元数据，复杂构建逻辑仍由通用脚本承担。

## 测试与验证方式 / 结果

- docs 骨架补齐：
  - 执行：`bootstrap_docs_tree.py <worktree-root>`
  - 结果：成功创建 `docs/README.md` 及五大分类 `README.md`

- skill 结构校验：
  - 执行：`tools/validate-skills.ps1 -Skill rigorous-execution -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - 结果：通过，`quick_validate.py` 返回 `Skill is valid!`

- copy 同步验证：
  - 执行：`tools/sync-skills.ps1 -Skill rigorous-execution`
  - 结果：成功生成 `dist/codex/rigorous-execution`，并复制到 `C:\Users\HelloWorld\.codex\skills\rigorous-execution`

- 模板残留扫描：
  - 执行：使用 `rg` 扫描 `TODO`、`Structuring This Skill`、`Use -execution`
  - 结果：未发现残留模板文本

## 潜在影响

- 仓库现在拥有一个受治理的 `docs/` 入口结构，后续 skill workflow 可以在此基础上继续记录 requirements/specs/change。
- `rigorous-execution` skill 会显式依赖 `$docs-governor`，因此文档路由和归档治理需要两者协作。
- 本轮没有新增 `lessons` 文档，因为没有暴露出可复用的事故模式或排障经验。

## 回滚方案

1. 回滚当前分支中的以下内容：
   - `skills/rigorous-execution/**`
   - `manifests/rigorous-execution.json`
   - `docs/README.md`
   - `docs/requirements/**`
   - `docs/specs/**`
   - `docs/plan/**`
   - `docs/change/README.md`
   - `docs/change/2026-03-23_rigorous-execution-skill.md`
   - `docs/lessons/**`
   - `plan.md`
2. 删除安装副本：
   - `C:\Users\HelloWorld\.codex\skills\rigorous-execution`
3. 如需清理构建产物，删除：
   - `dist/codex/rigorous-execution`

## 子Agent执行轨迹

- 本次 workflow 未使用子Agent。
- 原因：当前平台策略要求先获得用户对“子 Agent / 并行代理”的显式授权，而本轮未收到该授权；同时主 Agent 已能在单工作流内完成实现、验证、Review 与归档。
