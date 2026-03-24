# 2026-03-24 skill-prefix-rename

## 变更背景 / 目标

本轮目标是给这一组 skill 加统一前缀并完成正式重命名，避免继续保留分散的旧命名。

目标如下：

- `docs-governor` 改为 `m-docs`
- `rigorous-execution` 改为 `m-autoflow`
- 调用名同步改为 `$m-docs` 和 `$m-autoflow`
- 源码目录、manifest、稳定文档、校验/同步命令和本机安装目录保持一致

## 具体变更内容

- 重命名 skill 源目录：
  - `skills/docs-governor` -> `skills/m-docs`
  - `skills/rigorous-execution` -> `skills/m-autoflow`
- 重命名 manifest：
  - `manifests/docs-governor.json` -> `manifests/m-docs.json`
  - `manifests/rigorous-execution.json` -> `manifests/m-autoflow.json`
- 重命名稳定 requirement/spec 文档：
  - `docs/requirements/docs-governor-skill.md` -> `docs/requirements/m-docs-skill.md`
  - `docs/specs/docs-governor-skill.md` -> `docs/specs/m-docs-skill.md`
  - `docs/requirements/rigorous-execution-skill.md` -> `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/rigorous-execution-skill.md` -> `docs/specs/m-autoflow-skill.md`
- 更新当前技能定义与显示名：
  - `name: m-docs`
  - `name: m-autoflow`
  - `display_name: m:docs`
  - `display_name: m:autoflow`
- 更新依赖与引用：
  - `m-autoflow` 现在显式依赖 `m-docs`
  - `docs-governor-integration.md` 重命名为 `m-docs-integration.md`
- 更新工具默认值：
  - `tools/validate-skills.ps1`
  - `tools/sync-skills.ps1`
  - 默认 skill 改为 `m-docs`

## Requirements impact

updated

## Specs impact

updated

## Lessons impact

updated

## Related requirements

- `docs/requirements/m-docs-skill.md`
- `docs/requirements/m-autoflow-skill.md`

## Related specs

- `docs/specs/m-docs-skill.md`
- `docs/specs/m-autoflow-skill.md`

## Related lessons

- `docs/lessons/searchable-lessons-capture.md`

## 对应 plan.md 任务映射

- `RN-1`：重命名 skill 源目录、manifest 和稳定文档文件名。
- `RN-2`：更新 skill frontmatter、display name、依赖、调用名和说明文档。
- `RN-3`：验证并同步新名字到本机安装目录，清理旧安装目录。
- `RN-4`：review 与 archive。

## 经验 / 教训摘要

- 这套 skill 机制的真实名称受两层约束：
  - validator 只允许 hyphen-case
  - Windows 文件系统不允许 `:` 出现在目录名和文件名里
- 所以 `m:docs` / `m:autoflow` 只能作为显示名，真实 skill 名必须用 `m-docs` / `m-autoflow`。
- 重命名 skill 不只是改 `SKILL.md` 的 `name`，还必须同时处理目录、manifest、引用文档、校验/同步脚本和本机安装副本。

## 可复用排查线索

- 症状：
  - 想给 skill 加前缀，但改名后校验、同步或安装路径不一致。
- 触发条件：
  - skill 名需要重命名，且仓库同时维护 source、manifest、stable docs 和本机安装副本。
- 关键词：
  - `skill rename`
  - `hyphen-case`
  - `windows colon`
  - `m-docs`
  - `m-autoflow`
- 快速检查：
  - 查看 `SKILL.md` frontmatter 的 `name`
  - 查看 `agents/openai.yaml` 的 `display_name` 和 `default_prompt`
  - 查看 manifest 的 `name`、`source_dir`、`dist_dir`、`depends_on_skills`
  - 查看 `tools/validate-skills.ps1` / `tools/sync-skills.ps1`
  - 查看 `C:\Users\HelloWorld\.codex\skills\` 是否只剩新目录名

## 关键设计决策与权衡

1. 真实 skill 名采用 `m-docs` / `m-autoflow`，显示名采用 `m:docs` / `m:autoflow`。
   - 原因：这是同时满足 validator 和 Windows 文件系统约束的最接近目标方案。
   - 权衡：实际调用是 `$m-docs` / `$m-autoflow`，不是带冒号的名字。

2. 保留历史 change archive 文件名不变。
   - 原因：这些文件记录的是当时的变更主题，不需要为了当前命名强行重写文件名。
   - 权衡：历史 archive 文件名仍会出现旧名字，但当前稳定文档和安装链路都以新名字为准。

3. 保留历史 change archive 的正文语义，不按现名回写旧轮次内容。
   - 原因：archive 的职责是保留当时发生了什么，而不是追溯性改写历史事实。
   - 权衡：旧 archive 正文中会继续出现旧 skill 名，但这比把过去的实现路径伪装成当前名字更可靠。

## 测试与验证方式 / 结果

- Skill 结构校验：
  - 执行：`tools/validate-skills.ps1 -Skill m-docs -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - 结果：通过
  - 执行：`tools/validate-skills.ps1 -Skill m-autoflow -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - 结果：通过

- Skill 同步：
  - 执行：`tools/sync-skills.ps1 -Skill m-docs`
  - 结果：成功更新 `dist/codex/m-docs` 与 `C:\Users\HelloWorld\.codex\skills\m-docs`
  - 执行：`tools/sync-skills.ps1 -Skill m-autoflow`
  - 结果：成功更新 `dist/codex/m-autoflow` 与 `C:\Users\HelloWorld\.codex\skills\m-autoflow`

- 本机安装清理验证：
  - 删除：
    - `C:\Users\HelloWorld\.codex\skills\docs-governor`
    - `C:\Users\HelloWorld\.codex\skills\rigorous-execution`
  - 结果：本机 install root 中仅保留新名字：
    - `m-docs`
    - `m-autoflow`

## 潜在影响

- 现有使用者如果仍然调用 `$docs-governor` 或 `$rigorous-execution`，需要迁移到 `$m-docs` 和 `$m-autoflow`。
- 历史 archive 文件名没有跟着改，后续阅读时需要把它们理解为重命名前的历史记录。

## 回滚方案

1. 回滚以下内容：
   - `skills/m-docs/**`
   - `skills/m-autoflow/**`
   - `manifests/m-docs.json`
   - `manifests/m-autoflow.json`
   - `docs/requirements/m-docs-skill.md`
   - `docs/specs/m-docs-skill.md`
   - `docs/requirements/m-autoflow-skill.md`
   - `docs/specs/m-autoflow-skill.md`
   - `tools/validate-skills.ps1`
   - `tools/sync-skills.ps1`
   - `docs/change/2026-03-24_skill-prefix-rename.md`
   - `plan.md`
2. 删除新安装目录：
   - `C:\Users\HelloWorld\.codex\skills\m-docs`
   - `C:\Users\HelloWorld\.codex\skills\m-autoflow`
3. 如需恢复旧目录名，再同步旧版 skill。

## 子Agent执行轨迹

- 本次 workflow 未使用子Agent。
- 原因：重命名涉及同一组目录、文档与安装链路，拆分写入会增加交叉修改和审计成本。
