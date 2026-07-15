# Python Cache Files During Skill Synchronization

## Summary

Replace-style skill synchronization can copy untracked `__pycache__` directories and `.pyc` files when tests or compilation run inside the source skill before synchronization. Remove or prevent generated caches before syncing, then require clean source/dist/install parity.

## Lookup Hints

- Keywords: `__pycache__`, `.pyc`, skill sync, `sync-skills.ps1`, extra installed file, parity mismatch, `PYTHONDONTWRITEBYTECODE`.
- Symptoms: installed skill contains Python bytecode; file-list parity reports an extra cache path; a clean source tree still has ignored generated files.
- Trigger conditions: running Python tests, importing a loader, or using `py_compile` before a recursive copy-based sync.
- Quick checks: search source skill directories for `__pycache__` and `*.pyc`; inspect ignored files; compare source, dist, and install file lists excluding only documented build metadata.

## Symptoms

- Post-sync installed directories contain `scripts/__pycache__/...pyc`.
- Source/install file-list comparison fails even though tracked source changes are correct.
- `git status` remains clean because the generated cache is ignored, making the extra package content easy to miss.

## Impact

- Installed packages include environment-specific generated artifacts.
- Exact parity checks become noisy or misleading.
- Bytecode from one Python version may be distributed unnecessarily to another environment.

## Trigger Conditions

- A Python loader is imported by unit tests from its source directory.
- `python -m py_compile` or similar compilation runs before synchronization.
- The synchronization tool recursively copies the complete source directory rather than only tracked or allowlisted files.

## Root Cause

Python writes bytecode caches beside imported modules by default. The repository ignores those files, but the replace-style synchronization script copies every filesystem entry under the source skill, including ignored and untracked generated files.

## Investigation Trail

1. Ran loader tests and syntax compilation before syncing `m-context`.
2. Synced the complete skill directory to `dist` and the installed Codex skill root.
3. A parity/file-list check found `scripts/__pycache__/context_loader...pyc` in the copied package.
4. Verified that the cache was generated during the current workflow and was not a tracked or user-authored skill file.
5. Removed only the verified worktree cache directories, re-synced, and confirmed exact source/dist/install hashes.

## Resolution

- Verify each cache path resolves inside the active worktree before deletion.
- Remove generated `__pycache__` directories and `.pyc` files from source skill paths.
- Re-run replace-style synchronization.
- Require exact file-list and SHA-256 parity after sync, excluding only documented generated metadata such as `.build-info.json`.

## Prevention / Guardrails

- Run validation with `PYTHONDONTWRITEBYTECODE=1` when practical.
- Check source skill directories for ignored generated files immediately before synchronization.
- Do not treat Git cleanliness as proof that a recursive copy source contains only distributable files.
- Exclude caches in the synchronization implementation or copy from an explicit tracked/allowlisted set in a separately planned improvement.
- Preserve genuine installed-package drift; do not delete or overwrite it until compared with the committed baseline.

## Related Docs

- [Local/global m-context intake](../intake/2026-07-15_m-context-scopes.md)
- [m-context feature](../features/m-context.md)
- [m-context requirements](../requirements/m-context-skill.md)
- [m-context specification](../specs/m-context-skill.md)
- [Local/global m-context change](../change/2026-07-15_m-context-scopes.md)
- [Windows skill parity and line endings](windows-skill-parity-line-endings.md)
