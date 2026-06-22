---
name: m-autoflow-archive
description: Archive and closeout phase for the m-autoflow staged engineering workflow. Use after tests and review pass to explicitly invoke $m-docs, create docs/change records, promote reusable lessons into docs/lessons, update indexes, ask whether to end the workflow, and only after explicit confirmation merge branches and clean worktrees.
---

# m:autoflow archive

## Overview

Use this skill to preserve the workflow result as governed documentation and, only after explicit user confirmation, close the workflow through merge and worktree cleanup.

## Quick Start

- Read `references/archive.md`.
- Read `../m-autoflow/references/m-docs-integration.md` before treating archive work as complete.
- Read `../m-autoflow/references/templates.md` when creating `docs/change` or `docs/lessons` artifacts.
- Explicitly invoke `$m-docs` for documentation routing, impact checks, lessons, and indexes.

## Entry Gate

Archive may start only when:

- execution is complete
- validation and code review passed or residual risks are explicitly accepted
- changed files and Task IDs are known
- the active plan is current

If any item is false, return to `$m-autoflow-test` or `$m-autoflow-execute`.

## Workflow

1. Use `$m-docs` to check requirements/specs impact and docs routing.
2. Create `docs/change/YYYY-MM-DD_topic.md` in the appropriate docs tree.
3. Record task mapping, decisions, tests, impact, rollback, and sub-agent trace.
4. Promote reusable troubleshooting or workflow knowledge into `docs/lessons` when it is likely to recur.
5. Update affected indexes.
6. Ask whether to end the workflow.
7. If the user does not explicitly confirm workflow end, stop after archive readiness.
8. If the user confirms workflow end, perform merge and worktree cleanup from the repo control plane, preserving unrelated dirt and reporting final local/remote state honestly.

## Exit Gate

End with:

- archive paths
- requirements/specs/lessons impact
- validation summary
- merge and cleanup status when workflow end was confirmed
- remaining local state, including unpushed commits or unrelated dirt

Do not merge or remove worktrees before explicit workflow-end confirmation.
