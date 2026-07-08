# 2026-07-08_m-plan-task-table

## 变更背景 / 目标

The user requested that after planning, `$m-plan` should show a table that briefly displays the planned tasks.

Goal: make `$m-plan` easier to review by adding a direct task summary table after creating or confirming `plan.md` / `todo.md`.

## 具体变更内容

- Updated `skills/m-plan/SKILL.md`:
  - `$m-plan` now requires a concise task summary table in the direct response.
  - The table summarizes the active `plan.md` / `todo.md` and does not replace it.
- Updated `skills/m-plan/references/planning.md`:
  - added `Direct Task Summary Table`
  - defined minimum columns: `Task ID`, `Title`, `Scope`, `Files / Modules`, `Acceptance / Tests`, and `Risk / Notes`
  - required every known task from the execution scope split to appear in the table
- Updated shared `m-autoflow` planning rules and templates:
  - `skills/m-autoflow/references/stages.md`
  - `skills/m-autoflow/references/templates.md`
- Updated `m-plan` UI metadata prompt.
- Updated stable feature, requirement, and spec docs.
- Added intake evidence for the user's requirement.
- Synced installed `m-plan` and `m-autoflow` copies.

## Docs root

`D:\project\my-ai-skills\docs`

## Intake impact

updated

## Feature impact

updated

## Requirements impact

updated

## Specs impact

updated

## Decision impact

none

## Lessons impact

none

No lesson was created because this is a direct durable workflow requirement, not a debugging incident or recurring environment pitfall. The reusable rule now lives in the skill source plus feature, requirement, and spec docs.

## Related intake

- [../intake/2026-07-08_m-plan-task-table.md](../intake/2026-07-08_m-plan-task-table.md)

## Related features

- [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related decisions

- none

## Related lessons

- none

## 对应 plan.md 任务映射

- `MPT-1`: updated `$m-plan` and shared planning rules to require a direct task summary table.
- `MPT-2`: updated stable docs and intake for the new planning output contract.
- `MPT-3`: validated, synced installed skills, archived, and closed the workflow.

## 经验 / 教训摘要

- Planning artifacts remain the detailed source of truth, but direct output should expose enough task structure for quick approval decisions.
- The task table must preserve the `Will Execute` / `Will Not Execute Now` split so it does not accidentally imply approval or expand scope.
- A compact table reduces the need to open `plan.md` for basic task review.

## 可复用排查线索

- Symptoms:
  - `$m-plan` writes or confirms `plan.md` but the chat response does not show a task overview.
  - User must open `plan.md` just to see task IDs and execution scope.
- Trigger conditions:
  - `$m-plan` creates or confirms a plan.
  - A workflow has multiple tasks, blocked tasks, or deferred tasks.
- Keywords:
  - `Plan Task Summary Table`
  - `Direct Task Summary Table`
  - `Task ID | Title | Scope`
  - `Will execute`
  - `Will not execute now`
- Quick checks:
  - Confirm `$m-plan` response includes the task table.
  - Confirm every known task appears in exactly one scope group.
  - Confirm the table does not contradict `plan.md` / `todo.md`.

## 关键设计决策与权衡

- Chose a concise table instead of duplicating full task details in chat.
- Kept `plan.md` / `todo.md` as the detailed handoff artifact.
- Required blocked/deferred tasks to appear in the table so planning output remains honest about what will not execute now.

## 测试与验证方式 / 结果

- `tools\validate-skills.ps1 -Skill m-plan`: passed.
- `tools\validate-skills.ps1 -Skill m-autoflow`: passed.
- `git diff --check`: passed with expected CRLF conversion warnings only.
- `tools\sync-skills.ps1 -Skill m-plan`: completed.
- `tools\sync-skills.ps1 -Skill m-autoflow`: completed.
- Targeted `rg` checks confirmed:
  - direct task summary table requirement exists in `$m-plan`
  - shared `m-autoflow` stage rules include the requirement
  - shared template defines the table shape
  - stable feature, requirement, and spec docs describe the behavior
- Heavy `$m-test`: skipped because this change modifies skill/docs text only and does not change application UI, runtime behavior, data, auth, storage, or external integration paths.

## 潜在影响

- Future `$m-plan` responses should include a compact task table immediately after planning.
- Users can review task IDs, execution scope, files/modules, test cues, and risks without opening markdown for the basic overview.
- Installed local skills were updated immediately. No remote push, docs publication, or backup strategy change occurred.

## 回滚方案

- Revert `feat: add m plan task summary table` and this archive commit.
- Run `tools\sync-skills.ps1 -Skill m-plan` and `tools\sync-skills.ps1 -Skill m-autoflow` from the restored source if local installed behavior must be rolled back.

## 子Agent执行轨迹

- No sub-agents used.
