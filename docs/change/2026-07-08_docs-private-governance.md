# 2026-07-08_docs-private-governance

## 变更背景 / 目标

The docs model needed to become feature-first, source-traceable, multi-repo aware, and private-docs aware. The user specifically wanted original requests separated from change archives, feature behavior documented end to end, and docs publication or backup left under user control.

## 具体变更内容

- Added `docs/intake`, `docs/features`, and `docs/decisions` categories with README indexes.
- Updated stable requirements and specs for `m-docs` and `m-autoflow`.
- Updated `$m-docs` taxonomy, routing rules, impact checks, templates, indexing rules, lessons rules, and bootstrap support.
- Updated `$m-autoflow`, `$m-autoflow-plan`, and `$m-autoflow-archive` to identify `project_root`, `docs_root`, `code_repos`, and `active_worktree`.
- Added archive-phase handling for intake, feature, requirement, spec, decision, and lessons impact.
- Review found that `bootstrap_docs_tree.py --module` should validate external path input. The script now rejects absolute, drive-qualified, or path-traversing module names before any directory action.
- Synced affected skills into the local Codex skill install root.

## Docs root

- `D:\project\my-ai-skills\worktrees\docs-private-governance\docs`
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

none

No reusable troubleshooting lesson was promoted. The review finding was a straightforward external-input validation issue, and the validation command is recorded below for future checks.

## Related intake

- [../intake/2026-07-08_docs-private-governance.md](../intake/2026-07-08_docs-private-governance.md)

## Related features

- [../features/README.md](../features/README.md)

## Related requirements

- [../requirements/m-docs-skill.md](../requirements/m-docs-skill.md)
- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related specs

- [../specs/m-docs-skill.md](../specs/m-docs-skill.md)
- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related decisions

- [../decisions/2026-07-08_private-docs-root-and-feature-first-governance.md](../decisions/2026-07-08_private-docs-root-and-feature-first-governance.md)

## Related lessons

- None.

## 对应 plan.md 任务映射

- `PDG-1`: completed stable docs updates.
- `PDG-2`: completed `$m-docs` taxonomy, routing, templates, indexes, and bootstrap updates.
- `PDG-3`: completed `$m-autoflow`, `$m-autoflow-plan`, and `$m-autoflow-archive` alignment.
- `PDG-4`: completed validation and local skill sync.
- `PDG-5`: committed approved execution changes locally.
- `PDG-6`: reviewed, fixed the bootstrap module-input guardrail, and archived the workflow.
- `PDG-7`: not executed; user-owned remote, push, and backup strategy.
- `PDG-8`: not executed; future target-project migration.

## 经验 / 教训摘要

- Feature behavior needs a current-truth dossier instead of being scattered across specs and change logs.
- Original request evidence should be recorded separately from the interpreted current truth.
- Multi-repo capabilities need one private docs truth center with links to implementation repos.
- Archive review should include command-line input validation when a workflow touches scripts.

## 可复用排查线索

- Symptoms:
  - `bootstrap_docs_tree.py --module` accepts a value that could escape the intended docs root.
- Trigger conditions:
  - A caller passes `..`, an absolute path, or a drive-qualified path as a module bucket.
- Keywords:
  - `bootstrap_docs_tree.py`, `--module`, `docs_root`, path traversal, module bucket
- Quick check:
  - `python skills\m-docs\scripts\bootstrap_docs_tree.py --docs-root tmp\docs-bootstrap-smoke --module ..\escape --dry-run`
  - Expected result: `exit=2` before any mkdir/write actions.

## 关键设计决策与权衡

- Chose feature-first docs plus category-aware routing instead of continuing to split user-visible behavior across specs and requirements.
- Chose a selected private `docs_root` model instead of assuming docs belong to every code repo.
- Chose user-owned remotes, push targets, and backup strategy instead of automating docs publication.
- Kept `requirements` and `specs` for durable intent and technical contracts to avoid turning feature dossiers into API references.

## 测试与验证方式 / 结果

- `python -m py_compile skills\m-docs\scripts\bootstrap_docs_tree.py`
- `python skills\m-docs\scripts\bootstrap_docs_tree.py --docs-root tmp\docs-bootstrap-smoke --module personnel --dry-run`
- `python skills\m-docs\scripts\bootstrap_docs_tree.py --docs-root tmp\docs-bootstrap-smoke --module ..\escape --dry-run`
  - result: `exit=2`
- `git diff --check`
- `tools\validate-skills.ps1 -Skill m-docs`
- `tools\validate-skills.ps1 -Skill m-autoflow`
- `tools\validate-skills.ps1 -Skill m-autoflow-plan`
- `tools\validate-skills.ps1 -Skill m-autoflow-archive`
- `tools\sync-skills.ps1 -Skill m-docs`
- `tools\sync-skills.ps1 -Skill m-autoflow`
- `tools\sync-skills.ps1 -Skill m-autoflow-plan`
- `tools\sync-skills.ps1 -Skill m-autoflow-archive`

All listed checks passed. `git diff --check` produced no whitespace errors.

## 潜在影响

- Future `$m-docs` usage will prefer private docs roots and feature dossiers when those are the user's chosen governance model.
- Future `$m-autoflow-plan` workflows will ask for or record `docs_root` boundaries before behavior-changing implementation.
- Existing docs remain compatible, but new category README files and routing rules may change where future docs are written.
- Local Codex-installed skills were updated; no remote repository was changed.

## 回滚方案

- Revert the local commits for this workflow from branch `refactor/docs-private-governance`.
- If installed skills need to return to the previous version, resync the previous source state through `tools\sync-skills.ps1`.
- Because no remote push or docs backup was performed, rollback is local-only unless the user later publishes this branch.

## 子Agent执行轨迹

- No sub-agents were used.
