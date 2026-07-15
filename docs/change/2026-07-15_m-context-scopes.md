# 2026-07-15 m-context Local And Global Scopes

## 变更背景 / 目标

The first `$m-context` version used one user-global plaintext store. The user requested project-local context at `<docs_root>/context`, while retaining the global store for reusable cross-project data. The goal was deterministic local-first loading without requiring repeated environment details or credentials.

## 具体变更内容

- Added `auto`, `local`, and `global` context scope models to the standard-library loader.
- Added explicit local-root derivation from `<docs_root>/context` without parent-directory project discovery.
- Implemented local-first exact lookup where only a missing local root or exact file permits global fallback.
- Kept existing-but-invalid local files terminal for path resolution, containment, file type, permission, UTF-8, and section failures.
- Added strict `local:` and `global:` invocation rules, scope-qualified discovery, and source diagnostics separated from loaded Markdown.
- Kept the existing global precedence: `M_CONTEXT_HOME`, `<CODEX_HOME>/m-contexts`, then `~/.codex/m-contexts`.
- Defined new-context creation as explicit-scope only and unqualified updates as exact auto-resolution of an existing file.
- Classified `<docs_root>/context` as non-governed runtime context data in `$m-docs` routing.
- Explicitly prohibited automatic `.gitignore`, `.git/info/exclude`, Git config, staging, commit, push, or publication changes for context files.
- Expanded focused loader/API/CLI regression coverage and synchronized the changed `m-context` and `m-docs` skills to the local Codex installation.

## Docs root

- `D:\project\my-ai-skills\docs`
- The docs are versioned in the local code repository selected by the user.
- No remote, publication, backup, or push action was performed.
- No `docs/context` directory or context data was created during the workflow.

## Intake impact

- Intake impact: updated
- Added the local/global scope request, plaintext-secret allowance, local path, fallback behavior, and explicit no-ignore constraint.

## Feature impact

- Feature impact: updated
- Activated project-local and user-global storage, strict scopes, source reporting, create/update behavior, and absence-only fallback.

## Requirements impact

- Requirements impact: updated
- Added durable scope, path, fallback, discovery, no-merge, and no-automatic-Git-mutation requirements.

## Specs impact

- Specs impact: updated
- Added the scoped resolver API/CLI, structured location results, exact fallback classification, output-channel separation, and validation contract.

## Decision impact

- Decision impact: none
- The local path, precedence behavior, plaintext policy, and Git-ignore boundary were explicit user requirements and did not require a separate ADR.

## Lessons impact

- Lessons impact: updated
- Added a reusable lesson for Python cache files being copied by replace-style skill synchronization.
- Reused the Windows line-ending parity and symlink-test privilege lessons.

## Related intake

- [Original m-context request](../intake/2026-07-13_m-context.md)
- [Local/global scope request](../intake/2026-07-15_m-context-scopes.md)

## Related features

- [m-context](../features/m-context.md)

## Related requirements

- [m-context skill](../requirements/m-context-skill.md)

## Related specs

- [m-context skill spec](../specs/m-context-skill.md)

## Related decisions

- None.

## Related lessons

- [Python cache files during skill synchronization](../lessons/python-cache-skill-sync.md)
- [Windows skill parity and line endings](../lessons/windows-skill-parity-line-endings.md)
- [Windows symlink test privilege](../lessons/windows-symlink-test-privilege.md)

## 对应 plan.md 任务映射

- `MCS-1`: completed; implemented scoped resolution, absence-only fallback, structured source metadata, and CLI behavior.
- `MCS-2`: completed; aligned `$m-context` instructions, format reference, and `$m-docs` runtime-context boundary.
- `MCS-3`: completed; expanded the focused suite from 11 to 19 tests.
- `MCS-4`: completed; activated stable docs, validated both changed skills, synchronized local installations, and verified exact parity.
- `MCS-5`: not executed as required; no automatic Git-ignore or context-data Git-state management was introduced.
- `MCS-6`: not executed as required; a normal load selects exactly one source and never merges local/global bodies.
- [Archived plan](../plan/2026-07-15_m-context-scopes.md)

## 经验 / 教训摘要

- Fallback must be controlled by a typed missing-resource condition; catching broad filesystem or content errors would hide broken project-local configuration behind global data.
- The workflow must provide `docs_root` explicitly. Loader-side parent scanning risks selecting credentials from the wrong project.
- Loaded Markdown and source metadata need separate output channels so downstream skills receive only the intended context body.
- Replace-style skill synchronization copies generated files present in the source directory; Python caches should be removed or prevented before syncing.
- A context directory under a docs root remains user-controlled runtime data, not a governed-document category or automatic Git write set.

## 可复用排查线索

- Symptoms: the global context loads unexpectedly; a broken local context appears to be ignored; `list` results lack a scope; installed skills contain `__pycache__`; source/install parity reports extra `.pyc` files.
- Trigger conditions: missing local root/file, existing invalid local file, absent `--docs-root`, tests or `py_compile` run before replace-style synchronization, Windows line-ending conversion.
- Keywords / errors: `local lookup unavailable`, `Context not found in local or global scope`, `Cannot resolve existing context`, `loaded local:`, `loaded global:`, `__pycache__`, `.pyc`, `POST_SYNC_EXACT_PARITY_OK`.
- Quick checks: run `context_loader.py root --scope local --docs-root <docs_root>`; run scoped `list`; inspect stderr source diagnostics; check the source skill for generated caches before sync; compare source, dist, and install file lists and hashes after sync.

## 关键设计决策与权衡

- Chose local-first precedence instead of body merging to keep one deterministic credential/environment source per invocation.
- Allowed fallback only for absence, not for validation or content errors, so global data cannot conceal a broken local override.
- Required explicit workflow-provided `docs_root` instead of environment or ancestor discovery to avoid cross-project ambiguity.
- Preserved global-only compatibility when no docs root is available, while reporting that local lookup was unavailable.
- Kept plaintext secrets Agent-readable and rejected encryption work because automation convenience is the explicit trust model.
- Left all Git treatment of `docs/context` to explicit user actions; the workflow neither ignored nor staged context data.

## 测试与验证方式 / 结果

- `python -m unittest tests.test_m_context_loader`: 19 tests ran; 18 passed; 1 skipped because the current Windows account cannot create the symlink fixture.
- Python syntax compilation: passed.
- `tools/validate-skills.ps1 -Skill m-context`: passed.
- `tools/validate-skills.ps1 -Skill m-docs`: passed.
- Pre-sync installed-package drift check against the committed baseline: passed after excluding generated `.build-info.json` and Python cache files.
- Exact source/dist/install SHA-256 parity for `m-context` and `m-docs`: passed after synchronization, excluding generated build metadata.
- Installed `m-context` local-root CLI smoke check: passed.
- `git diff --check`: passed.
- `.gitignore` unchanged and `docs/context` absent: confirmed.
- Heavy `$m-test`: skipped. The change has no UI, service integration, production data, authorization boundary, external dependency, or performance-critical path; focused execution validation was accepted for closeout.

## 潜在影响

- Auto discovery now returns scope-qualified names, which is intentionally more explicit than the previous global-only name list.
- Successful loads write a concise source diagnostic to stderr; consumers must treat stdout as the context body.
- Local context files may contain plaintext secrets and are not automatically ignored by Git. Publication remains the user's responsibility.
- Residual risk: the symlink/junction regression remains skipped on Windows accounts without link privilege, though containment logic is unchanged and existing local resolution errors are terminal.

## 回滚方案

- Revert product commit `53803d5` after merge.
- Re-sync `m-context` and `m-docs` from the prior repository revision.
- The global context store and user-created context files remain separate and must not be deleted automatically.
- Revert the archive commit separately only if documentation history must also be removed.

## 子Agent执行轨迹

- No sub-agents were used. The loader, instructions, tests, and validation shared one tightly coupled contract, the user invoked `$m-execute` rather than `$m-go`, and host policy did not authorize delegation.
