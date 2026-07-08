# 2026-07-08_m-archive-default-closeout

## 变更背景 / 目标

The user corrected the workflow semantics after `$m-archive` asked for a second workflow-end confirmation. The intended behavior is that invoking `$m-archive` already means archive and end the workflow.

Goal: make `$m-archive` close workflows by default after archive completion while preserving an explicit archive-only escape hatch.

## 具体变更内容

- Updated `$m-archive` source instructions so normal invocation means archive plus closeout.
- Updated shared `$m-autoflow` stage rules so archive closes by default.
- Preserved explicit archive-only behavior for user requests such as no merge, no cleanup, pause, or archive-only.
- Kept safety checks before merge and worktree cleanup:
  - archive completion
  - worktree/repo status verification
  - unrelated dirt preservation
  - control-plane merge
- Updated stable feature, requirement, and spec docs to describe the new default closeout semantics.
- Added intake evidence for the user's correction.
- Synced installed `m-autoflow` and `m-archive` skill copies.

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

No separate lesson was created because the durable rule now lives in the feature, requirement, spec, and skill source docs. This was a direct semantics correction rather than an expensive debugging trail or reusable environment pitfall.

## Related intake

- [../intake/2026-07-08_m-archive-default-closeout.md](../intake/2026-07-08_m-archive-default-closeout.md)

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

- `MAC-1`: updated `skills/m-archive`, `skills/m-autoflow`, and shared stage/archive references.
- `MAC-2`: updated feature, requirement, spec, intake, and affected indexes.
- `MAC-3`: validated, synced installed skills, committed implementation, archived the correction, and used default closeout.

## 经验 / 教训摘要

- A command named as a terminal phase should not require a second confirmation for the same terminal intent.
- Safety checks should guard merge and cleanup, but they are separate from asking whether the user meant to end the workflow.
- Archive-only remains valuable, but it should be opt-in through explicit user wording.

## 可复用排查线索

- Symptoms:
  - `$m-archive` writes archive docs and then asks whether to end workflow.
  - User expects `$m-archive` to be equivalent to workflow end.
- Trigger conditions:
  - Terminal workflow command semantics conflict with a second confirmation prompt.
  - Skill source and stable docs both mention workflow-end confirmation.
- Keywords:
  - `workflow-end confirmation`
  - `ask whether to end`
  - `archive-only`
  - `closeout`
- Quick checks:
  - Search current skill/stable docs for `workflow-end confirmation`, `ask whether`, and `whether to end`.
  - Confirm `$m-archive` states default closeout plus explicit archive-only override.

## 关键设计决策与权衡

- Chose default closeout for `$m-archive` to match the user's command semantics.
- Rejected unconditional cleanup with no escape hatch because archive-only pauses are still useful when explicitly requested.
- Kept all merge and cleanup safety checks, so the change removes only the redundant intent confirmation, not operational safeguards.

## 测试与验证方式 / 结果

- `tools\validate-skills.ps1 -Skill m-autoflow`: passed.
- `tools\validate-skills.ps1 -Skill m-archive`: passed.
- `git diff --check`: passed with expected CRLF conversion warnings only.
- Targeted `rg` checks: no current skill or stable-doc rule still requires a second workflow-end confirmation after normal `$m-archive`.
- `tools\sync-skills.ps1 -Skill m-autoflow`: completed.
- `tools\sync-skills.ps1 -Skill m-archive`: completed.
- Heavy `$m-test`: skipped because this is a low-risk instruction/docs correction with no runtime code, data, auth, storage, or UI behavior.

## 潜在影响

- Future `$m-archive` invocations will proceed to closeout by default after archive completion.
- Users who want to keep a workflow branch/worktree after archive must explicitly say archive-only, no merge, no cleanup, or equivalent wording.
- Installed local skills were updated immediately; no remote publication occurred.

## 回滚方案

- Revert `fix: make archive close workflows by default` and this archive commit before merge, or revert the resulting commits on `main` after closeout.
- Run `tools\sync-skills.ps1 -Skill m-autoflow` and `tools\sync-skills.ps1 -Skill m-archive` from the restored source to reinstall the previous behavior locally.

## 子Agent执行轨迹

- No sub-agents used.
