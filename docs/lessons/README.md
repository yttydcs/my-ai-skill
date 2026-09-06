# Lessons

## Purpose

Store reusable incident knowledge, query-friendly troubleshooting lessons, and prevention guidance that should survive individual workflows.

## How to Enter This Section

- Add or update a lesson when the same failure pattern is likely to recur.
- Start here when the question is "have we seen this before?" or "what should I check first?".
- Do not use lessons as a substitute for fixing a broken requirement or spec.

## What Belongs Here

- repeated failure patterns
- lookup hints such as symptoms, trigger conditions, keywords, and quick checks
- root-cause and prevention notes
- debugging paths worth preserving

## Naming / Maintenance Rules

- Use stable names without dates when the lesson is long-lived.
- Group by module or domain when useful.
- Capture lookup hints so someone can match the lesson from symptoms instead of re-reading change logs.
- Link lessons back to relevant intake, features, requirements, specs, decisions, and changes.

## Current Docs

- [codex-visualization-preview-limitations.md](codex-visualization-preview-limitations.md) - keywords: `$visualize:visualize`, sandboxed iframe, synthetic keyboard activation, `MutationObserver.observe`, preview host
- [dirty-worktree-review.md](dirty-worktree-review.md) - keywords: empty committed diff, staged-only change, untracked test, overlapping edits, stale review
- [orchestrator-lease-recovery.md](orchestrator-lease-recovery.md) - keywords: stale lease, orphan host lease, archive operation, owner heartbeat, `pool reclaim`, `reclaim-host`, `legacy-host-orphan`, `active_lease`, premature release, two-phase audit
- [orchestrator-multi-repository-runtime-boundaries.md](orchestrator-multi-repository-runtime-boundaries.md) - keywords: non-Git umbrella, schema v2, `[[repositories]]`, `project_instance_id`, host lease collision, manifest retry, `planning_ref`
- [pipeline-handoff-and-closeout.md](pipeline-handoff-and-closeout.md) - keywords: `shared_resource_busy`, idle receiver, uncertain dispatch, archive receipt, removed worktree, tested candidate, Windows separator, projectless, `project_mismatch`
- [python-unittest-discovery-nonpackage-tests.md](python-unittest-discovery-nonpackage-tests.md) - keywords: `ModuleNotFoundError`, `tests.test_`, `unittest discover`, missing `tests/__init__.py`, non-package tests
- [python-cache-skill-sync.md](python-cache-skill-sync.md) - keywords: `__pycache__`, `.pyc`, skill sync, extra installed file, parity mismatch, `PYTHONDONTWRITEBYTECODE`
- [searchable-lessons-capture.md](searchable-lessons-capture.md) - keywords: archive, lessons, troubleshooting, recurring investigation
- [skill-frontmatter-yaml-colon.md](skill-frontmatter-yaml-colon.md) - keywords: skill validator, YAML frontmatter, colon, description, mapping values are not allowed
- [windows-skill-parity-line-endings.md](windows-skill-parity-line-endings.md) - keywords: installed skill drift, SHA-256 mismatch, CRLF, LF, sync-skills, ignore-space-at-eol
- [windows-symlink-test-privilege.md](windows-symlink-test-privilege.md) - keywords: WinError 1314, symbolic link, symlink test skipped, Developer Mode
