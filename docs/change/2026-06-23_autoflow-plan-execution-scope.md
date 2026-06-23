# 2026-06-23_autoflow-plan-execution-scope

## 变更背景 / 目标

用户指出 `$m-autoflow-plan` 生成的计划容易把所有任务都放在同一个 plan 里，进入 `$m-autoflow-execute` 前不够清楚哪些任务会被执行、哪些任务不会被执行。目标是让计划阶段在用户批准前明确下一执行阶段的任务边界。

## 具体变更内容

- 更新 `skills/m-autoflow-plan/SKILL.md`：
  - 要求 plan 明确区分批准后会执行的任务和下一执行阶段不会执行的任务。
  - 要求每个已知任务只出现在一个分区中。
  - 在 blocked / unblocked exit gate 中增加 execution scope 输出。
- 更新 `skills/m-autoflow-plan/references/planning.md`：
  - 将 execution scope split 纳入 Required Plan Contents。
  - 要求不执行的任务写明 blocked、out of scope、deferred、research-only 或 separate approval 等原因。
- 更新 `skills/m-autoflow/references/templates.md`：
  - 在 `plan.md` skeleton 的 Stage 3.1 Planning 中新增 `Execution Scope After Approval`。
  - 模板分为 `Will Execute` 和 `Will Not Execute Now`。
- 同步稳定文档：
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
- 同步本地安装副本，使 `C:\Users\HelloWorld\.codex\skills` 与 Git-managed source 保持一致。

## Requirements impact

updated

## Specs impact

updated

## Lessons impact

none

## Related requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related lessons

- none

## 对应 plan.md 任务映射

- `Task 1`: update `$m-autoflow-plan` planning rules so execution scope is explicit before implementation approval.
- `Task 2`: update shared `plan.md` template so generated plans contain `Will Execute` and `Will Not Execute Now` sections.
- `Task 3`: update stable requirements/specs and change archive for workflow closeout.

## 经验 / 教训摘要

- Installed skill edits under `C:\Users\HelloWorld\.codex\skills` must be synced back into `D:\project\my-ai-skills\skills` before workflow closeout.
- Plan artifacts should not rely on an agent's later interpretation of "all executable tasks"; the execution boundary must be written into the plan before approval.

## 可复用排查线索

- 症状: `$m-autoflow-execute` appears able to execute more tasks than the user intended because the plan lists all discovered tasks together.
- 触发条件: `plan.md` contains task details but lacks an explicit approval-time execution scope split.
- 关键词: `m-autoflow-plan`, `Execution Scope After Approval`, `Will Execute`, `Will Not Execute Now`, `Task ID`, `plan.md`.
- 快速检查:
  - inspect `skills/m-autoflow-plan/SKILL.md`
  - inspect `skills/m-autoflow-plan/references/planning.md`
  - inspect `skills/m-autoflow/references/templates.md`

## 关键设计决策与权衡

- Keep the rule in `$m-autoflow-plan` rather than `$m-autoflow-execute` only, because execution scope must be visible before the user approves implementation.
- Keep deferred and blocked tasks inside the plan, but require a separate "will not execute now" section so the full context remains available without blurring the next execution boundary.
- Update both phase-specific planning rules and the shared umbrella template so generated plans and direct phase usage stay aligned.

## 测试与验证方式 / 结果

- `tools/validate-skills.ps1 -Skill m-autoflow`
- `tools/validate-skills.ps1 -Skill m-autoflow-plan`
- `tools/sync-skills.ps1 -Skill m-autoflow`
- `tools/sync-skills.ps1 -Skill m-autoflow-plan`
- `git diff --check`

## 潜在影响

- Future plans will include a new required section, which may make plan artifacts slightly longer.
- Agents must now justify why any known task is not included in the immediate execution scope.

## 回滚方案

- Revert the changes in `skills/m-autoflow-plan/SKILL.md`, `skills/m-autoflow-plan/references/planning.md`, and `skills/m-autoflow/references/templates.md`.
- Revert the related requirement/spec updates and this change archive.
- Re-run validation and sync for `m-autoflow` and `m-autoflow-plan`.

## 子Agent执行轨迹

- No sub-agents were used for this workflow.
