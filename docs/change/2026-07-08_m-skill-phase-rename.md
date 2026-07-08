# 2026-07-08_m-skill-phase-rename

## 变更背景 / 目标

The user wanted the `m-autoflow` phase skills renamed to shorter daily-use commands, with `m-autoflow` kept as the umbrella collection. The workflow also needed a first-class `discuss` phase for product discovery, technical brainstorming, optional current-practice research, and early worktree setup before architecture planning.

## 具体变更内容

- Renamed canonical phase skills from long `m-autoflow-*` names to short `m-*` names:
  - `m-plan`
  - `m-execute`
  - `m-test`
  - `m-archive`
  - `m-discuss`
- Refactored `m-autoflow` into a route-oriented umbrella and shared reference host.
- Added `$m-discuss` as the discovery, brainstorming, optional research, and early worktree setup phase.
- Folded optional research behavior into `$m-discuss`.
- Updated `$m-plan` so it consumes discussion output, owns architecture/execution planning, and rejects unreasonable or under-specified requirements.
- Updated manifests, phase prompts, shared references, and local installed skills.
- Removed stale installed old long-name phase directories from `C:\Users\HelloWorld\.codex\skills`.
- Added current feature, requirement, spec, and decision docs for the new workflow model.

## Docs root

- `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\docs`
- Publication status: local branch only; no remote, push, publication, or backup action was performed.

## Intake impact

updated

## Feature impact

updated

## Requirements impact

updated

## Specs impact

updated

## Decision impact

updated

## Lessons impact

updated

A reusable validator lesson was promoted because the workflow found a repeatable YAML frontmatter failure mode: unquoted or unescaped colon-like syntax in a skill description can make `quick_validate.py` fail with a YAML mapping error.

## Related intake

- [../intake/2026-07-08_m-skill-phase-rename.md](../intake/2026-07-08_m-skill-phase-rename.md)
- [../intake/2026-07-08_docs-private-governance.md](../intake/2026-07-08_docs-private-governance.md)

## Related features

- [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related decisions

- [../decisions/2026-07-08_m-skill-phase-naming.md](../decisions/2026-07-08_m-skill-phase-naming.md)
- [../decisions/2026-07-08_private-docs-root-and-feature-first-governance.md](../decisions/2026-07-08_private-docs-root-and-feature-first-governance.md)

## Related lessons

- [../lessons/skill-frontmatter-yaml-colon.md](../lessons/skill-frontmatter-yaml-colon.md)

## Related plan

- Not retained as a stable `docs/plan` archive for this historical workflow; the task mapping below remains the retained planning trace.

## 对应 plan.md 任务映射

- `MSR-1`: completed stable docs and records for the new phase model.
- `MSR-2`: completed canonical phase package and manifest renames.
- `MSR-3`: added `m-discuss` and moved optional research behavior into it.
- `MSR-4`: refactored `m-autoflow` into the umbrella / shared reference host.
- `MSR-5`: updated prompts, references, dependencies, and current docs references.
- `MSR-6`: validated, synced, and cleaned stale installed phase skill directories.
- `MSR-7`: committed approved execution changes locally.
- `MSR-8`: reviewed and archived this workflow.
- `MSR-9`: not executed; user-owned remote, push, publication, and backup decision.
- `MSR-10`: not executed; old-name compatibility aliases remain deferred.

## 经验 / 教训摘要

- Short phase commands reduce daily invocation friction, but stable docs must still record the full phase boundary.
- A first-class discussion phase keeps product discovery and current-practice research out of architecture planning.
- `m-autoflow` can remain the collection entry point while shared references prevent duplicated stage rules.
- Historical `docs/change` records may keep old names as evidence; current source, manifests, requirements, specs, features, and decisions should use canonical names.
- Skill frontmatter descriptions should avoid unquoted YAML-sensitive punctuation, especially colon patterns.

## 可复用排查线索

- Symptoms:
  - `tools\validate-skills.ps1 -Skill <name>` prints `Invalid YAML in frontmatter`.
  - YAML parser reports `mapping values are not allowed`.
- Trigger conditions:
  - A skill `description` line contains colon-like syntax that YAML reads as a mapping boundary.
  - Long frontmatter descriptions are edited by hand.
- Keywords:
  - `Invalid YAML in frontmatter`, `mapping values are not allowed`, `description`, `SKILL.md`, `quick_validate.py`
- Quick check:
  - run `tools\validate-skills.ps1 -Skill <skill-name>`
  - inspect the top `---` frontmatter block in `skills/<skill-name>/SKILL.md`
  - remove the colon pattern or quote the scalar before rerunning validation

## 关键设计决策与权衡

- Chose canonical short phase names over old long names because the user explicitly wanted less command friction.
- Deferred compatibility aliases because they would add packages, validation surface, sync behavior, and stale-instruction risk.
- Kept shared references under `m-autoflow` for this iteration instead of adding a separate core package.
- Chose `m-discuss` as the owner of optional web research, rather than keeping a separate public research phase.
- Kept docs remote, push, publication, and backup decisions user-owned.

## 测试与验证方式 / 结果

- `tools\validate-skills.ps1 -Skill m-autoflow`
- `tools\validate-skills.ps1 -Skill m-discuss`
- `tools\validate-skills.ps1 -Skill m-plan`
- `tools\validate-skills.ps1 -Skill m-execute`
- `tools\validate-skills.ps1 -Skill m-test`
- `tools\validate-skills.ps1 -Skill m-archive`
- `tools\sync-skills.ps1 -Skill m-autoflow`
- `tools\sync-skills.ps1 -Skill m-discuss`
- `tools\sync-skills.ps1 -Skill m-plan`
- `tools\sync-skills.ps1 -Skill m-execute`
- `tools\sync-skills.ps1 -Skill m-test`
- `tools\sync-skills.ps1 -Skill m-archive`
- `rg -n "m-autoflow-plan|m-autoflow-execute|m-autoflow-test|m-autoflow-archive|m-autoflow-research" skills manifests docs\requirements docs\specs docs\features docs\decisions`
  - result: no current-source or stable-doc matches
- `Get-ChildItem C:\Users\HelloWorld\.codex\skills -Directory | Where-Object { $_.Name -like 'm-*' }`
  - result: canonical new names are installed; old long phase install directories were removed
- `git diff --check`

All listed checks passed. On Windows, Git reported CRLF normalization warnings during some checks; no whitespace errors were reported.

## Review

Heavy `$m-test` phase: skipped.

Skip reason:

- The change is a skill/docs/package rename and documentation governance update.
- No product runtime, data migration, network boundary, auth, storage, billing, or user-facing application flow changed.
- Execution-stage validation covered the affected skill packages, manifests, local install output, and stale-reference cleanup.

Review checklist:

- 需求覆盖: 通过
- 架构合理性: 通过
- 性能风险（N+1 / 重复计算 / 多余 I/O / 锁竞争）: 通过
- 性能指标 / 阈值: 通过, not applicable to this skill/docs rename
- 可用性 / 用户路径: 通过
- 可读性与一致性: 通过
- 可扩展性与配置化: 通过
- 稳定性与安全: 通过
- 安全边界 / 权限 / 数据暴露: 通过
- 测试覆盖情况: 通过
- 整体流程 / 联调验证: 通过
- 子Agent治理与审计: 通过, no sub-agents were used

Residual risk:

- The current Codex session may not refresh the visible skill list until a new session or skill reload.
- Users who explicitly invoke old long phase names will need to use the new names unless a future alias workflow is approved.

## 潜在影响

- Future workflows should prefer `$m-discuss`, `$m-plan`, `$m-execute`, `$m-test`, and `$m-archive`.
- `$m-autoflow` remains the whole-workflow entry point.
- Old local installed long-name phase directories were removed and are no longer canonical.
- Historical archives remain historically accurate and may still mention old phase names.

## 回滚方案

- Revert local commits on branch `refactor/m-skill-phase-rename`.
- Resync the previous skill source through `tools\sync-skills.ps1` if installed skills need to return to old names.
- Recreate old local install directories only by resyncing a previous source state or by an explicit future alias change.
- Because no remote push, docs publication, or backup action was performed, rollback is local-only unless the user later publishes this branch.

## 子Agent执行轨迹

- No sub-agents were used.
