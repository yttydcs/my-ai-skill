# 2026-07-17 m-continue Unattended Convergence Loop

## 变更背景 / 目标

The user requested a new `$m-continue` command that can resume an already approved workflow after `$m-execute` or `$m-test`, then alternate those existing behaviors without asking whether to continue. It should stop only after acceptance fully converges or further in-scope progress is genuinely impossible.

## 具体变更内容

- Added the canonical `m-continue` Skill package, UI metadata, orchestration reference, and install manifest.
- Kept `$m-execute` and `$m-test` as the behavioral authorities instead of duplicating their detailed instructions.
- Defined state recovery from the active plan, worktree/diff, and reliable phase evidence.
- Defined one-invocation authorization for every iteration inside existing approved Task IDs and write sets.
- Added progress evidence and failure-signature comparison, with reset on any measurable improvement or changed signature.
- Added a non-progress stop after three comparable complete repair/test cycles repeat the same failure without improvement; no separate small total-iteration cap is used.
- Preserved `$m-execute` optional delegation instead of adopting `$m-go` mandatory worker edits.
- Integrated the command into `$m-autoflow` discovery, stage routing, sub-agent governance, output recipes, and manifest dependencies.
- Added focused semantic/package tests and installed synchronized local copies.

## Docs root

- `D:\project\my-ai-skills\docs` after control-plane merge.
- The governed docs root is versioned in the same local repository as the Skill source.
- No remote, push, publication, or backup action was requested or performed.

## Intake impact

- Intake impact: updated.
- The original request and unattended-loop clarification are preserved in the related intake record and now link this completed change.

## Feature impact

- Feature impact: updated.
- The current workflow feature describes `$m-continue` as a post-execute/test unattended convergence entry distinct from `$m-go`.

## Requirements impact

- Requirements impact: updated.
- Durable requirements cover single-invocation authorization, scope preservation, automatic retries, measurable progress, three-cycle non-progress detection, and archive exclusion.

## Specs impact

- Specs impact: updated.
- The technical contract covers package/manifest structure, authority references, state classification, progress signatures, test expectations, synchronization, and installation.

## Decision impact

- Decision impact: updated.
- Added and clarified the accepted decision to create a thin `$m-continue` orchestrator rather than duplicate phase rules or extend `$m-go`.

## Lessons impact

- Lessons impact: updated.
- Added a reusable lesson explaining that this repository's `tests/` directory is not a Python package and contract tests should be run with unittest discovery rather than dotted `tests.*` module names.

## Related intake

- [m-continue request](../intake/2026-07-17_m-continue-loop.md)

## Related features

- [m-autoflow workflow](../features/m-autoflow-workflow.md)

## Related requirements

- [m-autoflow workflow Skill](../requirements/m-autoflow-skill.md)

## Related specs

- [m-autoflow workflow Skill spec](../specs/m-autoflow-skill.md)

## Related decisions

- [m-continue loop decision](../decisions/2026-07-17_m-continue-loop.md)

## Related lessons

- [Python unittest discovery for non-package tests](../lessons/python-unittest-discovery-nonpackage-tests.md)
- [Windows Skill parity and line endings](../lessons/windows-skill-parity-line-endings.md)
- [Skill frontmatter YAML colon](../lessons/skill-frontmatter-yaml-colon.md)

## 对应 plan.md 任务映射

- `MC1`: completed; created `skills/m-continue`, its reference, UI metadata, and manifest.
- `MC2`: completed; integrated umbrella routing, stages, delegation policy, output recipe, and dependency metadata.
- `MC3`: completed; added focused continuation tests and shared output-contract coverage.
- `MC4`: completed; validated, ran all tests, synchronized, and hash-verified source/dist/install parity.
- `MC5`: completed by this archive phase through retained plan/change/lesson records, followed by default control-plane merge and cleanup.
- `MC6`: not executed; push requires an explicit `$m-gitpush` request.
- [Archived plan](../plan/2026-07-17_m-continue-loop.md)

## 经验 / 教训摘要

- An unattended command still needs a narrow authorization boundary; repeated confirmation can be removed without authorizing new scope or external mutation.
- A loop should distinguish ordinary failure, changed failure, measurable progress, persistent non-progress, and hard external blockers.
- A changed failure signature or any Task/diff/test/evidence improvement must reset non-progress counting.
- Skill orchestration remains maintainable when the new command references phase authorities and owns only transitions and termination.
- Test commands must match repository package topology; `unittest discover` is the reliable entry for this non-package `tests/` directory.

## 可复用排查线索

- Symptoms: `$m-continue` stops after one failure, asks whether to continue, loops despite no improvement, or expands outside approved Task IDs; unittest reports `ModuleNotFoundError: No module named 'tests.test_...'`.
- Trigger conditions: post-execute/test continuation, repeated identical validation failures, ambiguous previous evidence, or dotted unittest module invocation against this repository.
- Keywords / errors: `$m-continue`, failure signature, three consecutive complete cycles, no measurable progress, `ModuleNotFoundError`, `unittest discover`, `tests.test_m_continue_contract`.
- Quick checks: confirm the active plan is approved; compare failing IDs and progress evidence; verify the counter resets on improvement; run `python -m unittest discover -s tests`; inspect Skill authority references; run both Skill validators and source/install parity checks.

## 关键设计决策与权衡

- Chose a separate `$m-continue` Skill so continuation can start after execute or test without changing `$m-go` mandatory delegation semantics.
- Kept `SKILL.md` concise and moved orchestration detail into one progressive-disclosure reference.
- Used evidence-based non-progress detection rather than an arbitrary total-iteration cap.
- Reused existing PowerShell validation/sync tooling and introduced no new runtime dependency or state file.
- Kept archive explicit: `$m-continue` reports readiness but never archives, merges, cleans, publishes, or pushes.

## 测试与验证方式 / 结果

- `tools\validate-skills.ps1 -Skill m-continue`: passed.
- `tools\validate-skills.ps1 -Skill m-autoflow`: passed.
- Focused contract discovery: 13 tests passed.
- Full unittest discovery: 32 tests passed; 1 existing Windows symlink-privilege test skipped by its established condition.
- `tools\sync-skills.ps1 -Skill m-continue`: passed.
- `tools\sync-skills.ps1 -Skill m-autoflow`: passed.
- Source/dist/install SHA-256 file parity: passed for both packages, excluding generated `.build-info.json`.
- Explicit manifest JSON and Skill-reference checks: passed.
- `git diff --check`: passed.
- Heavy `$m-test`: skipped with accepted low residual risk because the change affects only Skill/Markdown/manifest/test contracts and has no UI, application runtime, service, data, auth, infrastructure, or external integration path.

## 潜在影响

- Agent instructions are ultimately behaviorally validated by real future invocations; focused contract tests prevent textual regression but cannot prove every model execution path.
- The three-cycle threshold is a fixed current contract; changing it to configuration requires a separate requirement and decision.
- Local installed copies were replaced through the repository sync tool after exact source validation.

## 回滚方案

- Revert implementation commit `c283856`, planning commit `eadf2c4`, and discussion commits `0bd2e81` / `14652a8` as appropriate.
- Remove `C:\Users\HelloWorld\.codex\skills\m-continue` and resynchronize `m-autoflow` from the restored source revision.
- Revert the archive commit separately if removing retained workflow history and the new lesson.

## 子Agent执行轨迹

- No sub-agents were used. The user invoked ordinary `$m-execute`, not `$m-go`, and did not grant implementation sub-agent authorization.
- Independent Skill forward testing was therefore not run; focused contract tests, full repository tests, validation, sync, and hash parity were used instead.
