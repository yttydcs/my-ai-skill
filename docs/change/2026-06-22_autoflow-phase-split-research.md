# 2026-06-22_autoflow-phase-split-research

## 变更背景 / 目标

用户希望在保留原 `$m-autoflow` 的前提下，将严格工程 workflow 拆分为可单独调用的计划、执行、测试、归档阶段，并新增一个仅在明确要求时才执行的联网调研能力。用户随后进一步明确：轻量语法/静态/局部验证应属于执行阶段，测试阶段应是可跳过的重型联调、可用性、安全和性能 review。

## 具体变更内容

- 保留 `skills/m-autoflow` 作为 umbrella 入口，并增加 split phase routing。
- 新增 companion skill 包：
  - `skills/m-autoflow-plan`
  - `skills/m-autoflow-execute`
  - `skills/m-autoflow-test`
  - `skills/m-autoflow-archive`
  - `skills/m-autoflow-research`
- 新增对应 manifest：
  - `manifests/m-autoflow-plan.json`
  - `manifests/m-autoflow-execute.json`
  - `manifests/m-autoflow-test.json`
  - `manifests/m-autoflow-archive.json`
  - `manifests/m-autoflow-research.json`
- 更新 `manifests/m-autoflow.json`，声明 umbrella skill 对 companion skills 的依赖。
- 更新 `m-autoflow` stage rules：
  - optional research 只在用户明确要求联网调研时触发。
  - stage `3.2` 包含轻量本地验证。
  - stage `3.3` 改为可跳过的重型测试 / review。
- 更新 sub-agent governance：
  - research 阶段允许只读 research sub-agent 例外。
  - research exception 不允许代码编辑、worktree 改动、plan 确认、实现、验证、归档、merge 或 cleanup。
- 将稳定需求和技术契约同步到 `docs/requirements/m-autoflow-skill.md` 与 `docs/specs/m-autoflow-skill.md`。

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

- `Task 1`: split `$m-autoflow` into phase-specific companion skills while preserving the original umbrella skill.
- `Task 2`: move lightweight validation into execute and define heavy optional test/review behavior.
- `Task 3`: add explicit-request-only online research with read-only parallel research sub-agent governance.
- `Task 4`: sync installed skill changes back into Git-managed source, docs, manifests, dist, and install output.

## 经验 / 教训摘要

- Installed skills under `C:\Users\HelloWorld\.codex\skills` are not a Git source of truth; workflow closeout must sync changes back to `D:\project\my-ai-skills\skills`.
- When syncing installed copies back to source, preserve newer source-only rules. In this workflow, the source repo had already changed the worktree location rule to `<project-root>\worktrees\`; blindly copying the installed umbrella skill would have regressed it to an older hard-coded path.
- Split-phase skills should remain companion entry points. The original `$m-autoflow` must continue to work as the full workflow entry.

## 可复用排查线索

- 症状: installed skill behaves correctly but repository `git status` is clean.
- 触发条件: direct edits under `%USERPROFILE%\.codex\skills` without syncing to `skills/`.
- 关键词: `m-autoflow`, companion skills, installed skill, source package, sync-skills, phase split, research sub-agent.
- 快速检查:
  - compare `%USERPROFILE%\.codex\skills\<skill>` with `skills/<skill>`
  - run `tools/validate-skills.ps1 -Skill <skill>`
  - run `tools/sync-skills.ps1 -Skill <skill>`
  - check `manifests/<skill>.json`

## 关键设计决策与权衡

- Keep `$m-autoflow` as an umbrella entry to avoid breaking existing explicit invocations.
- Create companion skills instead of replacing the original skill so agents can load only the relevant phase when the user asks for plan, execute, test, archive, or research.
- Make online research explicit-request-only to avoid unnecessary browsing during normal repo-grounded planning.
- Allow parallel research sub-agents only as a read-only exception because research lanes can be independent, while implementation remains gated by confirmed Task IDs and write-set ownership.
- Treat heavy test/review as optional to avoid unnecessary workflow overhead for small low-risk changes, while still requiring skip rationale and residual-risk reporting.

## 测试与验证方式 / 结果

- `tools/validate-skills.ps1 -Skill m-autoflow`
- `tools/validate-skills.ps1 -Skill m-autoflow-plan`
- `tools/validate-skills.ps1 -Skill m-autoflow-execute`
- `tools/validate-skills.ps1 -Skill m-autoflow-test`
- `tools/validate-skills.ps1 -Skill m-autoflow-archive`
- `tools/validate-skills.ps1 -Skill m-autoflow-research`
- `tools/sync-skills.ps1 -Skill ...` for every affected skill
- `git diff --check`

## 潜在影响

- Agents may now choose smaller phase-specific skills instead of loading the whole umbrella skill.
- Workflows that expect a mandatory `3.3` review must account for the new skip path and its required rationale.
- Online research may introduce source freshness and citation obligations when explicitly requested.

## 回滚方案

- Remove the companion skill directories and manifests.
- Revert `skills/m-autoflow` references to the previous single-skill stage model.
- Re-run validation and sync for `m-autoflow`.
- Revert requirement/spec updates if the split-phase contract is no longer desired.

## 子Agent执行轨迹

- No sub-agents were used for this skill evolution.
