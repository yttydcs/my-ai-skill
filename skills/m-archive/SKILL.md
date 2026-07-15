---
name: m-archive
description: Archive and closeout phase for the m-autoflow workflow. Use after $m-execute and optional $m-test pass, to explicitly invoke $m-docs, create docs/change records in the selected docs root, record intake/feature/requirement/spec/decision impact, promote reusable lessons, update indexes, and by default finish the workflow through control-plane merge and worktree cleanup unless the user explicitly requested archive-only handling.
---

# m:archive

## Overview

Use this skill to preserve the workflow result as governed documentation and close the workflow through merge and worktree cleanup by default.

Invoking `$m-archive` means "archive and end this workflow". Stop after archive only when the user explicitly asks for archive-only handling, no merge, no cleanup, or an equivalent pause.

## Quick Start

- Read `references/archive.md`.
- Read `../m-autoflow/references/m-docs-integration.md` before treating archive work as complete.
- Read `../m-autoflow/references/templates.md` when creating `docs/change` or `docs/lessons` artifacts.
- Read `../m-autoflow/references/output-components.md` before presenting archive and closeout status.
- Explicitly invoke `$m-docs` for documentation routing, impact checks, lessons, and indexes.
- Do not infer docs remote, push, publication, or backup strategy.

## Entry Gate

Archive may start only when:

- execution is complete
- validation and code review passed or residual risks are explicitly accepted
- changed files and Task IDs are known
- the active plan is current

If any item is false, return to `$m-test` or `$m-execute`.

## Workflow

1. Use `$m-docs` to check stable-doc impact and docs routing.
2. Create `docs/change/YYYY-MM-DD_topic.md` in the selected docs root.
3. Record task mapping, decisions, tests, intake/feature/requirement/spec/decision impact, rollback, and sub-agent trace.
4. Promote reusable troubleshooting or workflow knowledge into `docs/lessons` when it is likely to recur.
5. Update affected indexes.
6. If the user explicitly requested archive-only handling, stop after archive readiness and report the retained branch/worktree state.
7. Otherwise, perform merge and worktree cleanup from the repo control plane, preserving unrelated dirt and reporting final local/remote state honestly.

## Exit Gate

End with:

- archive paths
- intake/features/requirements/specs/decisions/lessons impact
- validation summary
- merge and cleanup status, or retained branch/worktree status when archive-only handling was explicitly requested
- remaining local state, including unpushed commits or unrelated dirt

Link archive artifacts with absolute clickable paths and summarize archive / merge / cleanup / remaining state in a compact table when several states must be compared. Emit Git components only for successful actions completed during closeout.

Do not merge or remove worktrees before archive completion, status verification, and unrelated-dirt preservation checks.
