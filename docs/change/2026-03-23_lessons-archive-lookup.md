# 2026-03-23 lessons-archive-lookup

## 变更背景 / 目标

本次 workflow 的目标是把 `rigorous-execution` 和 `docs-governor` 之间关于归档与 lessons 的协作做实，不再只停留在“是否需要 lessons”的提醒层面。

目标如下：

- 在 `rigorous-execution` 的 stage `4` 明确要求补充可复用的经验 / 教训摘要；
- 让归档结果能够沉淀到 `docs/lessons/`，而不是只留在 `docs/change/`；
- 让后续遇到问题时，可以先按症状、关键词和快速检查项直接查询 lessons；
- 补齐 `docs-governor` 的稳定 requirements / specs 真源文档。

## 具体变更内容

### skill 与 reference

- 更新 `skills/rigorous-execution/SKILL.md`
  - 将 `docs/lessons` 纳入 stage `4` 的显式治理范围；
  - 要求归档时抽取 reusable lessons 和 lookup hints。
- 更新 `skills/rigorous-execution/references/`
  - `stages.md`
  - `docs-governor-integration.md`
  - `templates.md`
  - 增加 `Lessons impact`、`Related lessons`、经验 / 教训摘要和可复用排查线索的硬性要求。
- 更新 `skills/docs-governor/SKILL.md` 与 references
  - 明确把 troubleshooting lookup 路由到 `lessons`；
  - 要求 `lessons` 文档提供症状、关键词、触发条件和 quick checks；
  - 要求 `docs/lessons/README.md` 保持可发现性。

### 仓库稳定文档与索引

- 更新 `docs/requirements/rigorous-execution-skill.md`
- 更新 `docs/specs/rigorous-execution-skill.md`
- 新增 `docs/requirements/docs-governor-skill.md`
- 新增 `docs/specs/docs-governor-skill.md`
- 更新：
  - `docs/README.md`
  - `docs/change/README.md`
  - `docs/lessons/README.md`
  - `docs/requirements/README.md`
  - `docs/specs/README.md`

### lessons 沉淀

- 新增 `docs/lessons/searchable-lessons-capture.md`
  - 把这次 workflow 抽象成一条可复用的 lessons：
    - 为什么经验会被埋在 change 里
    - 以后应该先查什么
    - 归档时必须补哪些 query cues

### bootstrap 输出

- 更新 `skills/docs-governor/scripts/bootstrap_docs_tree.py`
  - 生成的 `docs/README.md` 现在包含 troubleshooting order；
  - 生成的 `docs/change/README.md` 会提醒把可复用排查经验提升到 `lessons`；
  - 生成的 `docs/lessons/README.md` 会要求 lookup hints。

## Requirements impact

updated

## Specs impact

updated

## Lessons impact

updated

## Related requirements

- `docs/requirements/rigorous-execution-skill.md`
- `docs/requirements/docs-governor-skill.md`

## Related specs

- `docs/specs/rigorous-execution-skill.md`
- `docs/specs/docs-governor-skill.md`

## Related lessons

- `docs/lessons/searchable-lessons-capture.md`

## 对应 plan.md 任务映射

- `LA-1`：更新 `rigorous-execution` 的 stage `4` lessons 归档契约。
- `LA-2`：更新 `docs-governor` 的 lessons 路由、查询与模板契约。
- `LA-3`：补齐稳定文档、README 索引和 reusable lesson 样例。
- `LA-4`：验证并同步两个 skill，验证 bootstrap 输出。
- `LA-5`：完成 review 与归档。

## 经验 / 教训摘要

- `change` 适合记录一次 workflow 做了什么，但不适合承担“以后先查什么”的入口职责。
- 如果 stage `4` 只判断 lessons 是否需要，而不强制抽取 query cues，经验会继续埋在 change 或对话里。
- `rigorous-execution` 和 `docs-governor` 在归档阶段必须协同演进；只改其中一个会留下制度缝隙。

## 可复用排查线索

- 症状：
  - 明明做过一次调查，后续仍然只能翻旧的 `docs/change/` 或聊天记录。
- 触发条件：
  - workflow 完成了非显然的修复、排查成本较高，或暴露了重复性问题模式。
- 关键词：
  - `archive`
  - `lessons`
  - `troubleshooting`
  - `quick checks`
  - `recurring investigation`
- 快速检查：
  - 看本次 change 是否记录了 `Lessons impact`
  - 看是否已经存在 `Related lessons`
  - 看 `docs/lessons/README.md` 是否把 lesson 暴露成可查入口

## 关键设计决策与权衡

1. 选择增强现有 docs 治理链，而不是额外发明独立的 lessons-search skill。
   - 原因：问题本质是归档治理链条不完整，不是缺一个新的技能入口。
   - 权衡：需要同时修改两个 skill 和仓库稳定文档，改动面比只改一个文件大。

2. 选择“结构化 query cues”而不是纯自由文本经验总结。
   - 原因：后续查询更依赖症状、关键词、触发条件和 quick checks。
   - 权衡：归档模板更严格，但可检索性明显更高。

3. 为 `docs-governor` 补 requirements / specs，而不是继续只靠 change archive 追溯其行为。
   - 原因：这个 skill 已经承担稳定治理职责，缺少真源文档会让后续 impact check 继续失真。
   - 权衡：仓库中的稳定文档数量增加，但职责边界更清楚。

## 测试与验证方式 / 结果

- Skill 结构校验：
  - 执行：`tools/validate-skills.ps1 -Skill rigorous-execution -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - 结果：通过
  - 执行：`tools/validate-skills.ps1 -Skill docs-governor -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - 结果：通过

- Skill 同步：
  - 执行：`tools/sync-skills.ps1 -Skill rigorous-execution`
  - 结果：成功更新 `dist/codex/rigorous-execution` 与 `C:\Users\HelloWorld\.codex\skills\rigorous-execution`
  - 执行：`tools/sync-skills.ps1 -Skill docs-governor`
  - 结果：成功更新 `dist/codex/docs-governor` 与 `C:\Users\HelloWorld\.codex\skills\docs-governor`

- bootstrap 冒烟验证：
  - 执行：`C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe skills/docs-governor/scripts/bootstrap_docs_tree.py tmp\docs-governor-smoke --module api --force`
  - 结果：生成的 `docs/README.md`、`docs/change/README.md`、`docs/lessons/README.md` 都包含新的 lessons / troubleshooting 指引，验证后已清理临时目录。

## 潜在影响

- 归档阶段的要求更严格，后续 workflow 会多一步 lessons triage 和索引维护。
- `docs-governor` 现在把 troubleshooting lookup 视为一等场景，后续若有人继续直接把经验写进 `change`，会更明显地偏离规范。

## 回滚方案

1. 回滚本次变更涉及的以下内容：
   - `skills/rigorous-execution/**`
   - `skills/docs-governor/**`
   - `docs/requirements/rigorous-execution-skill.md`
   - `docs/specs/rigorous-execution-skill.md`
   - `docs/requirements/docs-governor-skill.md`
   - `docs/specs/docs-governor-skill.md`
   - `docs/README.md`
   - `docs/change/README.md`
   - `docs/lessons/README.md`
   - `docs/requirements/README.md`
   - `docs/specs/README.md`
   - `docs/lessons/searchable-lessons-capture.md`
   - `docs/change/2026-03-23_lessons-archive-lookup.md`
   - `plan.md`
2. 如需撤销安装副本，删除：
   - `C:\Users\HelloWorld\.codex\skills\rigorous-execution`
   - `C:\Users\HelloWorld\.codex\skills\docs-governor`
3. 如需清理构建产物，删除：
   - `dist/codex/rigorous-execution`
   - `dist/codex/docs-governor`

## 子Agent执行轨迹

- 本次 workflow 未使用子Agent。
- 原因：stage `3.1` 到归档涉及同一批规则与文档，拆分写入会增加交叉修改和审计成本。
