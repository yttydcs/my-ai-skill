# 2026-07-10 m-quick Fast Path

## 变更背景 / 目标

The staged `m-*` workflow was too costly for small, uncontroversial requirements and localized bugs. This change adds `$m-quick` as a guarded direct-edit path while preserving mandatory governed-doc context, focused validation, and explicit escalation for unsuitable work.

## 具体变更内容

- Added the canonical `m-quick` skill package, detailed rules, UI metadata, and manifest.
- Required `$m-docs` context reading before eligibility or implementation.
- Defined one-repo direct-edit safety, prohibited risk categories, dirty-worktree handling, focused validation, UI evidence, stable-doc impact, and direct result reporting.
- Integrated `$m-quick` into `m-autoflow` as a standalone alternate route without weakening staged worktree, plan, review, or archive gates.
- Added complete intake, feature, requirement, spec, and decision documentation plus category indexes.
- Synced and validated local installed copies of `m-quick` and `m-autoflow`.
- Archived the root execution plan and promoted the Windows line-ending parity pitfall into a reusable lesson.

## Docs root

- `D:\project\my-ai-skills\docs` after control-plane merge.
- Docs are committed locally in this repository.
- No docs remote, push, publication, or backup target was added or selected.

## Intake impact

- `Intake impact: updated`
- Added the original request record and linked this completed change.

## Feature impact

- `Feature impact: updated`
- Added a complete `$m-quick` feature dossier and clarified umbrella routing.

## Requirements impact

- `Requirements impact: updated`
- Added durable fast-path requirements and clarified the staged-workflow boundary.

## Specs impact

- `Specs impact: updated`
- Added the package, trigger, context, gate, validation, installation, and integration contracts.

## Decision impact

- `Decision impact: updated`
- Recorded the accepted choice to create a standalone command instead of weakening `$m-execute`.

## Lessons impact

- `Lessons impact: updated`
- Added a reusable Windows skill-parity lesson for CRLF/LF hash mismatches during pre-sync drift checks.

## Related plan

- [2026-07-10_m-quick-fast-path.md](../plan/2026-07-10_m-quick-fast-path.md)

## Related intake

- [2026-07-10_m-quick-fast-path.md](../intake/2026-07-10_m-quick-fast-path.md)

## Related features

- [m-quick-fast-path.md](../features/m-quick-fast-path.md)
- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related requirements

- [m-quick-fast-path.md](../requirements/m-quick-fast-path.md)
- [m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related specs

- [m-quick-skill.md](../specs/m-quick-skill.md)
- [m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related decisions

- [2026-07-10_m-quick-standalone-fast-path.md](../decisions/2026-07-10_m-quick-standalone-fast-path.md)

## Related lessons

- [windows-skill-parity-line-endings.md](../lessons/windows-skill-parity-line-endings.md)
- [skill-frontmatter-yaml-colon.md](../lessons/skill-frontmatter-yaml-colon.md)

## 对应 plan.md 任务映射

- Q1: completed; stable docs and architecture decision were added and indexed.
- Q2: completed; `m-quick` package and manifest were created.
- Q3: completed; umbrella routing and guardrails were integrated.
- Q4: completed; source validation, install sync, parity verification, and implementation commit succeeded.
- Q5: skipped; independent heavy forward-testing was optional and the user invoked `$m-archive` after the residual risk was disclosed.
- Q6: completed by this archive and the default control-plane closeout that follows this archive commit.
- Q7: not executed; no push was requested.

## 经验 / 教训摘要

- A fast workflow should remove setup and history overhead, not context recovery or validation.
- Eligibility should be risk-based rather than driven by line or file counts.
- The standalone command preserves `$m-execute` semantics better than adding a bypass mode.
- Raw file hashes are unreliable for pre-sync drift detection when Windows line-ending conversion differs between a Git worktree and installed copies.

## 可复用排查线索

- Symptoms: installed skill appears modified because SHA-256 hashes differ, but a semantic diff shows no content change.
- Trigger conditions: comparing Git working-tree files with copied Codex skill files on Windows before running `sync-skills.ps1`.
- Keywords: `m-quick`, `sync-skills`, installed skill drift, SHA-256, CRLF, LF, line endings, `--ignore-space-at-eol`.
- Quick checks: compare relative file lists excluding `.build-info.json`; run `git diff --no-index --ignore-space-at-eol`; require exact hash parity again after sync.

## 关键设计决策与权衡

- `$m-quick` is outside the staged phase chain.
- `$m-docs` reading is mandatory, while stable-doc writing is impact-based.
- The main agent performs direct edits; sub-agent overhead is excluded.
- High-risk or ambiguous work fails closed into `$m-discuss` or `$m-plan`.
- Reduced archive traceability is accepted for future quick runs, with Git and the direct result table providing the minimum evidence.

## 测试与验证方式 / 结果

- Source `m-quick` skill validation: passed.
- Source `m-autoflow` skill validation: passed.
- Installed `m-quick` and `m-autoflow` validation: passed.
- Manifest JSON parsing: passed.
- Markdown relative-link resolution: passed.
- Scenario-contract and staged-guardrail contradiction checks: passed.
- Source-to-installed SHA-256 parity after sync: passed.
- `git diff --check`: passed with expected Windows line-ending warnings only.
- Worktree status before archive: clean.
- Heavy `$m-test`: skipped after disclosure; residual risk is that realistic future prompts may reveal wording that benefits from iteration.
- UI evidence: not applicable because the repository change contains no runtime visual UI.

## 潜在影响

- Future explicit `$m-quick` requests may directly modify a selected repository after the gate passes.
- Over-broad future edits to trigger metadata could weaken selection accuracy; the dedicated feature/spec docs and validation checks should be used during revisions.
- The local installed skill is active, but no remote repository has been updated.

## 回滚方案

1. Revert the archive and implementation commits from `main`.
2. Remove `C:\Users\HelloWorld\.codex\skills\m-quick` if the command is withdrawn.
3. Rerun `tools\sync-skills.ps1 -Skill m-autoflow` from reverted source.
4. Revalidate the installed umbrella package.
5. Do not alter remotes, push targets, or backup destinations as part of rollback.

## 子Agent执行轨迹

- No sub-agents were used. `$m-execute` was selected and the host exposed no implementation sub-agent dispatch tool.

## Closeout

- Mode: default `$m-archive` closeout.
- After this archive commit, the control plane fast-forwards `main`, verifies status, removes the dedicated worktree, and deletes the merged local feature branch when safe.
- Remote state remains unchanged until an explicit `$m-gitpush` invocation.
