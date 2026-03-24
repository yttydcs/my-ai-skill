# 2026-03-24 requirements-specs-responsibility-clarity

## 变更背景 / 目标

本次 workflow 的目标是把 `requirements` 和 `specs` 的职责边界写得更明确，并且把这条边界放进稳定文档本身，保证文档在脱离当前对话后仍然自解释。

目标如下：

- 明确 `requirements` 回答什么问题；
- 明确 `specs` 回答什么问题；
- 明确两者的先后关系和边界；
- 避免这些规则只存在于 README、change archive 或聊天记录里。

## 具体变更内容

- 更新 `docs/requirements/README.md`
  - 增加 `requirements` 的进入条件、内容范围和与 `specs` 的边界说明。
- 更新 `docs/specs/README.md`
  - 增加 `specs` 的进入条件、内容范围和与 `requirements` 的边界说明。
- 更新 `docs/requirements/docs-governor-skill.md`
  - 增加 `Documentation Boundary Goal`，把 category 边界提升为稳定 requirement。
  - 明确 docs 系统需要自解释，不依赖 chat context。
- 更新 `docs/specs/docs-governor-skill.md`
  - 增加 `Requirements And Specs Responsibility Contract`。
  - 增加 `Self-Explanation Contract`。
  - 明确当两者同时变化时的更新顺序。

## Requirements impact

updated

## Specs impact

updated

## Lessons impact

none

## Related requirements

- `docs/requirements/docs-governor-skill.md`

## Related specs

- `docs/specs/docs-governor-skill.md`

## Related lessons

- none

## 对应 plan.md 任务映射

- `RS-1`：补强 `requirements` category README 和稳定 requirement 文档。
- `RS-2`：补强 `specs` category README 和稳定 spec 文档。
- `RS-3`：完成 review 与 archive。

## 经验 / 教训摘要

- 类别边界如果只写在 reference 或对话里，后续维护者仍然会回到“这条该放哪”的重复判断。
- `README` 适合做导航，但不足以承载完整的稳定边界；还需要 requirement/spec 真源文档兜底。

## 可复用排查线索

- 症状：
  - 读者知道有 `requirements` 和 `specs`，但不知道各自应该回答什么。
- 触发条件：
  - 文档需要路由新内容，或者需要做 requirement/spec impact 判断。
- 关键词：
  - `requirements`
  - `specs`
  - `boundary`
  - `why what`
  - `how contract`
- 快速检查：
  - 先看 `docs/requirements/README.md` 和 `docs/specs/README.md`
  - 再看 `docs/requirements/docs-governor-skill.md` 与 `docs/specs/docs-governor-skill.md`
  - 确认该内容是在描述长期 intent，还是在描述技术 contract

## 关键设计决策与权衡

1. 选择把边界写进稳定 requirement/spec，而不是只改 README。
   - 原因：README 是导航层，不应该成为唯一真源。
   - 权衡：需要同时维护 category README 和稳定文档两层表述。

2. 选择用 `why / what` 与 `how / contract` 作为最短判断口径。
   - 原因：便于快速分类，也和现有 taxonomy 一致。
   - 权衡：口径更短，但仍需要稳定 spec 展开详细规则。

## 测试与验证方式 / 结果

- 一致性检查：
  - 执行：`git diff --check`
  - 结果：通过
- 文档复核：
  - 逐项检查变更后的 `requirements` / `specs` README 与 `docs-governor` 稳定 requirement/spec
  - 结果：四份文档对 category 边界、问题视角和更新顺序的表述一致

## 潜在影响

- 后续 requirement/spec impact 判断会更严格，因为稳定文档现在明确了边界。
- 若未来 taxonomy 调整，这几份稳定文档也需要同步维护，而不只是改 reference。

## 回滚方案

1. 回滚以下文件：
   - `docs/requirements/README.md`
   - `docs/specs/README.md`
   - `docs/requirements/docs-governor-skill.md`
   - `docs/specs/docs-governor-skill.md`
   - `docs/change/README.md`
   - `docs/change/2026-03-24_requirements-specs-responsibility-clarity.md`
   - `plan.md`
2. 保留其他 skill 和 lessons 相关改动不变。

## 子Agent执行轨迹

- 本次 workflow 未使用子Agent。
- 原因：变更集中在同一组稳定文档，拆分执行不划算且会增加交叉修改。
