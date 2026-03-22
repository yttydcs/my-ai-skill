# 2026-03-22 docs-governor-skill

## 变更背景 / 目标

本次 workflow 的目标是建立一个可长期积累的个人 skill 真源仓库，并在其中落地一个可复用的 `docs-governor` skill。

约束与目标如下：

- skill 真源使用 Git 管理；
- 当前先落地 Codex 可用版本；
- 安装方式使用 `copy`，不把 `~/.codex/skills` 当作真源；
- skill 需要治理文档分类与索引，覆盖：
  - `requirements`
  - `specs`
  - `plan`
  - `change`
  - `lessons`

## 具体变更内容

### 新增

- 技能仓库基础结构：
  - `skills/docs-governor/`
  - `tools/`
  - `manifests/`
- 技能主体：
  - `skills/docs-governor/SKILL.md`
  - `skills/docs-governor/agents/openai.yaml`
- 治理参考文档：
  - `skills/docs-governor/references/taxonomy.md`
  - `skills/docs-governor/references/routing-rules.md`
  - `skills/docs-governor/references/indexing-rules.md`
  - `skills/docs-governor/references/requirement-impact.md`
  - `skills/docs-governor/references/lessons-rules.md`
  - `skills/docs-governor/references/templates.md`
- 自动化脚本：
  - `skills/docs-governor/scripts/bootstrap_docs_tree.py`
  - `tools/validate-skills.ps1`
  - `tools/sync-skills.ps1`
- 安装元数据：
  - `manifests/docs-governor.json`
- 仓库忽略规则：
  - `.gitignore`

### 修改

- `plan.md`
  - 补齐了需求分析、架构设计、任务拆分、实施记录、review 结论和归档状态。

### 删除

- `docs/change/.gitkeep`
  - 目录已有真实归档文件后不再需要占位文件。

## 对应 plan.md 任务映射

- `DG-1`：初始化 skill 源布局与官方脚手架，已完成。
- `DG-2`：编写 skill 主体与治理 references，已完成。
- `DG-3`：实现 docs tree bootstrap、校验、copy 同步，已完成。
- `DG-4`：完成 review 与归档，已完成。

## 关键设计决策与权衡

1. 使用 `skills/docs-governor` 作为技能真源，而不是增加额外的 `codex/` 源包装层。
   - 原因：更贴合 `init_skill.py` 的目录模型，减少当前实现绕行。
   - 权衡：未来若做 Claude 专有包装，需要在仓库层新增额外适配，而不是直接复用源目录结构。

2. 采用 `copy` 同步，而不是链接或直接在安装目录开发。
   - 原因：安装目录和真源解耦，更利于回滚、备份和多版本管理。
   - 权衡：需要一次显式同步动作。

3. 将“文档治理”和“docs 结构初始化”放在同一个 skill 里。
   - 原因：二者属于同一领域，分成两个 skill 会重复上下文。
   - 权衡：skill 的职责比纯分类器更宽，但仍保持在同一问题域内。

4. `validate-skills.ps1` 不写死用户专属 Python 路径。
   - 原因：仓库本身应尽量减少环境耦合。
   - 处理方式：优先接受显式 `-PythonExe`，否则尝试常见位置自动发现。

## 测试与验证方式 / 结果

- Skill 结构校验：
  - 执行：`tools/validate-skills.ps1 -Skill docs-governor -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - 结果：通过，`quick_validate.py` 返回 `Skill is valid!`

- docs 树 bootstrap 冒烟：
  - 执行：`bootstrap_docs_tree.py <sample-project> --module workspace --module server`
  - 结果：成功创建 `docs/README.md`、五大分类目录及模块子目录 README。

- copy 同步验证：
  - 执行：`tools/sync-skills.ps1 -Skill docs-governor`
  - 结果：成功生成 `dist/codex/docs-governor`，并复制到 `C:\Users\HelloWorld\.codex\skills\docs-governor`

## 潜在影响

- 当前只验证了 Codex 侧安装与结构，不包含 Claude 侧包装或运行验证。
- 当前 `bootstrap_docs_tree.py` 负责创建目录与 README 骨架，但不会自动迁移历史文档。

## 回滚方案

1. 回滚当前分支中的以下内容：
   - `skills/docs-governor/**`
   - `tools/**`
   - `manifests/**`
   - `.gitignore`
   - `plan.md`
   - `docs/change/2026-03-22_docs-governor-skill.md`
2. 删除已安装副本：
   - `C:\Users\HelloWorld\.codex\skills\docs-governor`
3. 如需清理构建产物，删除：
   - `dist/codex/docs-governor`

## 子Agent执行轨迹

- 本次 workflow 未使用子Agent。
- 原因：当前会话未获得显式子Agent授权，且主Agent已完成全部实现、验证与归档。
