# Windows Skill Parity And Line Endings

## Summary

Raw SHA-256 comparison can report false installed-skill drift on Windows when a Git working tree uses CRLF while an installed or copied skill uses LF. Confirm semantic equality before replacing an installed package, then require exact parity after sync.

## Lookup Hints

- Keywords: installed skill drift, SHA-256 mismatch, CRLF, LF, line endings, `sync-skills.ps1`, `git diff --no-index`, `--ignore-space-at-eol`.
- Quick signal: matching file lists and an empty whitespace-tolerant diff despite different hashes.
- Quick checks:
  - exclude generated `.build-info.json`
  - compare relative file lists
  - run `git diff --no-index --ignore-space-at-eol` for mismatched files
  - after sync, compare exact file hashes again

## Symptoms

- A pre-sync safety check says the installed skill differs from repository source.
- Multiple text files have different hashes, but no meaningful line changes appear.
- Git warns that LF will be replaced by CRLF.

## Impact

Treating the mismatch as real local drift can unnecessarily block a safe sync or cause someone to preserve meaningless line-ending differences as if they were user-authored content.

## Trigger Conditions

- Windows Git checkout with line-ending conversion enabled or mixed line-ending history.
- Installed Codex skills created through direct copy from a differently normalized source tree.
- Pre-sync safeguards based only on exact hashes.

## Root Cause

Cryptographic hashes include line-ending bytes. CRLF and LF files therefore hash differently even when their parsed Markdown or YAML content is equivalent.

## Investigation Trail

1. Compared the installed `m-autoflow` package with the `main` source package before destructive sync.
2. Relative file lists matched, but several SHA-256 values differed.
3. Ran `git diff --no-index --ignore-space-at-eol` for each mismatch.
4. The diff was empty, confirming line-ending-only differences.
5. Synced the validated worktree source and then confirmed exact installed-source hashes.

## Resolution

Use a two-stage parity check:

1. Before sync, detect possible user drift with file-list comparison plus a semantic or line-ending-tolerant diff.
2. After sync, require exact hashes because the install copy should now be byte-for-byte identical to the selected source package, excluding generated metadata.

## Prevention / Guardrails

- Never classify a Windows text-file hash mismatch as user modification without inspecting the diff.
- Exclude generated `.build-info.json` from source/install parity comparisons.
- Preserve and escalate genuine content differences before running a replace-style sync script.
- Keep exact post-sync parity as the final acceptance check.

## Related Docs

- [Original intake](../intake/2026-07-10_m-quick-fast-path.md)
- [m-quick feature](../features/m-quick-fast-path.md)
- [m-quick requirements](../requirements/m-quick-fast-path.md)
- [m-quick specification](../specs/m-quick-skill.md)
- [Standalone fast-path decision](../decisions/2026-07-10_m-quick-standalone-fast-path.md)
- [Change archive](../change/2026-07-10_m-quick-fast-path.md)
