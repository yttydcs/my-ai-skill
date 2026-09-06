# 2026-09-06 Pipeline Project Tasks

## Problem And Result

The user reported that five AI Builder role tasks appeared outside the project after using the setup example. Inspection of the original coordinator's actual creation calls confirmed `target.type: projectless`, despite a matching saved Git project being available. The role prompts contained project paths, but prompt paths do not establish Codex project membership.

Version 0.1.1 makes project-owned creation the default, preserves explicitly chosen standalone tasks, and rejects a project creation's ready receipt when actual project membership is missing or wrong. Existing original phase skills are unchanged.

## Changes

- Correct the reusable example and entry/setup instructions to resolve the actual saved project ID before creation. No environment-specific IDs are embedded in the package.
- Support explicit project `environment: local` for non-Git saved projects and an explicitly requested direct Git checkout; reject a base ref in local mode. Existing project targets without environment retain their worktree semantics.
- Require verified `project_id` for newly accepted project creation readiness. A mismatch does not bind the receiver, free its pending creation or spawn a duplicate. Corrected evidence can reconcile the original operation.
- Keep host project membership and exact assignment repository/worktree checks separate. Multi-repository projects still use explicit code worktrees.
- Document recovery of already-created projectless teams. The current task tools have no general project-reassignment operation; changing cwd, sidebar grouping or internal databases is not a supported migration.

## Scope And Documentation

This is a focused defect correction requested after the original workflow closed; no new staged plan or implementation delegation was requested. The fix covers default configuration, creation validation, tests, documentation and companion installation. It does not create, interrupt, move or archive the user's existing role tasks, alter their active coordinator/state, or launch implementation.

- Docs root: this repository's established `docs` tree; original `$m-docs` routing reused.
- Intake impact: none — the original intake remains historical; the new bug report and observed trigger are recorded above.
- Feature impact: updated — project-owned task creation is the default.
- Requirements impact: updated — R02 clarifies project membership and explicit standalone compatibility.
- Specs impact: updated — creation environment and project readiness receipt contracts.
- Decision impact: none — existing companion/phase composition remains valid.
- Lessons impact: updated — distinguish project identity from cwd and avoid copying a disposable pilot default into project setup.
- Indexes: change entry added, lesson lookup cues updated; documentation topology is unchanged.

## Validation

- Focused pipeline regression: 32 tests, 31 passed and 1 skipped because Windows fixture symlink creation lacks privilege (WinError 1314). Includes project/default/legacy target validation, local-project configuration, missing/wrong project receipt rejection without binding or duplicate creation, corrected/idempotent receipts, and exact assignment-worktree preservation.
- Skill creator validator and existing manifest/package validator passed. The installed CLI accepted a resolved project blueprint without creating host tasks.
- Installed only `m-pipeline` version 0.1.1. All 13 source/dist/installed files match bytes; all 68 other installed m-* files and their file set remain unchanged against the pre-update snapshot.
- Scope/whitespace and 93 local Markdown links passed. Original phase sources were not edited. Full unrelated suites were not repeated for this focused correction.
- Project-target/receipt tests use deterministic host evidence. Actual host project lookup and the defective project's creation calls were inspected; this correction does not claim a new real-host project creation pilot.

## Compatibility And Recovery

Explicit projectless blueprints remain valid; old project targets keep their default worktree behavior. Existing runs and stored receipts are retained without schema migration. An unresolved new project creation now requires actual project metadata before a ready receipt can be accepted.

Updating the installed skill does not change existing task membership or an initialized run's immutable blueprint. The owning coordinator must reconcile active work before any authorized replacement, and existing creation limits/history still apply. No task recreation or user runtime mutation was performed as part of this fix.

Rollback is a scoped revert of this patch and resync of only `m-pipeline`; keep customer configurations, runtime history and tasks intact. Repository/doc changes are local-only; no push or deployment is performed.

## Related Documents

- [Original intake](../intake/2026-09-06_role-pipeline.md)
- [Feature](../features/m-pipeline.md)
- [Requirements](../requirements/m-pipeline.md)
- [Specification](../specs/m-pipeline.md)
- [Decision](../decisions/2026-09-06_role-pipeline-composition.md)
- [Lesson](../lessons/pipeline-handoff-and-closeout.md#project-membership-is-separate-from-workdir)
- [Original implementation archive](2026-09-06_m-pipeline.md)
