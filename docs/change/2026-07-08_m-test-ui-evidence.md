# 2026-07-08_m-test-ui-evidence

## 变更背景 / 目标

The user accepted the proposed UI validation rule for `$m-test` and added two refinements:

- UI changes should be tested by actually opening the interface, operating the affected path, and providing acceptance screenshots.
- `$m-test` should output a concise table directly to the user showing which checks passed and which did not.
- `$m-test` remains optional; the user may choose to skip it and proceed directly to `$m-archive`.

Goal: make `$m-test` a stronger evidence-based validation phase when it runs, while preserving explicit user control to skip it.

## 具体变更内容

- Updated `skills/m-test/SKILL.md`:
  - UI-impacting tested changes now require actual UI open/operation/screenshot evidence.
  - Missing UI evidence during a run `$m-test` is failed or blocked, not a pass.
  - Direct user-facing result table is required.
  - User-directed skip to `$m-archive` remains allowed with residual risk recorded.
- Updated `skills/m-test/references/testing.md`:
  - added UI validation evidence rules
  - added direct result table format and minimum columns
  - clarified skip handling and archive risk carryover
- Updated `skills/m-autoflow` shared rules:
  - clarified that `$m-test` may be explicitly skipped
  - added UI evidence and direct table requirements to stage `3.3`
- Updated stable feature, requirement, and spec docs.
- Added intake evidence for the user's requirement.
- Synced installed `m-test` and `m-autoflow` copies.

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

No lesson was created because this is a direct durable workflow requirement, not an incident or recurring troubleshooting path. The reusable rule now lives in the skill source plus feature, requirement, and spec docs.

## Related intake

- [../intake/2026-07-08_m-test-ui-evidence.md](../intake/2026-07-08_m-test-ui-evidence.md)

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

- `MTU-1`: updated `$m-test` rules for UI evidence and direct result table.
- `MTU-2`: updated stable docs and intake for the new test semantics.
- `MTU-3`: validated, synced installed skills, archived, and closed the workflow.

## 经验 / 教训摘要

- UI validation should produce visual and interaction evidence when it actually runs.
- A concise direct result table reduces the need for users to open archive markdown for the basic verdict.
- Optional testing and evidence-based testing can coexist: user-directed skip is allowed, but missing validation must be recorded as residual risk.

## 可复用排查线索

- Symptoms:
  - `$m-test` reports UI review without opening or operating the UI.
  - User has to open markdown artifacts to know which checks passed.
  - Workflow treats skipped UI testing as if it passed.
- Trigger conditions:
  - UI, component, style, route, interaction, form, modal, state display, or responsive changes.
  - User explicitly skips `$m-test` and proceeds to archive.
- Keywords:
  - `UI Validation Evidence`
  - `Direct Result Table`
  - `screenshot evidence`
  - `pass/fail table`
  - `m-test skip`
- Quick checks:
  - Confirm `$m-test` output includes an `Area / Check / Status / Evidence / Notes` table.
  - For UI-impacting tested changes, confirm screenshot paths and operation steps are present.
  - If `$m-test` was skipped, confirm `$m-archive` records missing evidence and residual risk.

## 关键设计决策与权衡

- Chose to make UI evidence mandatory only when `$m-test` runs, preserving the user's explicit ability to skip testing.
- Chose a compact direct table rather than forcing users to open `docs/change` or `plan.md` for the basic pass/fail verdict.
- Chose not to add browser automation implementation details to the skill; the rule requires real UI validation but leaves tool choice to the project and host capabilities.

## 测试与验证方式 / 结果

- `tools\validate-skills.ps1 -Skill m-test`: passed.
- `tools\validate-skills.ps1 -Skill m-autoflow`: passed.
- `git diff --check`: passed with expected CRLF conversion warnings only.
- `tools\sync-skills.ps1 -Skill m-test`: completed.
- `tools\sync-skills.ps1 -Skill m-autoflow`: completed.
- Targeted `rg` checks confirmed:
  - UI evidence requirement exists in skill and stable docs.
  - direct result table requirement exists in skill and stable docs.
  - explicit user skip remains allowed with residual risk recording.
- Heavy `$m-test`: skipped for this workflow because this change modifies skill/docs text only and does not change an application UI.

## 潜在影响

- Future `$m-test` runs for UI-impacting changes should include actual UI operation and screenshot evidence.
- Future `$m-test` responses should include a concise results table.
- Users can still skip `$m-test` and call `$m-archive`; the archive must then disclose missing validation evidence and residual risk.
- Installed local skills were updated immediately. No remote push, docs publication, or backup strategy change occurred.

## 回滚方案

- Revert `feat: require UI evidence in m test` and this archive commit.
- Run `tools\sync-skills.ps1 -Skill m-test` and `tools\sync-skills.ps1 -Skill m-autoflow` from the restored source if local installed behavior must be rolled back.

## 子Agent执行轨迹

- No sub-agents used.
