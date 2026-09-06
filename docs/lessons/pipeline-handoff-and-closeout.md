# Pipeline Handoff And Closeout

## Summary

Host task status, assignment acceptance, and tested product identity are different facts. A reliable handoff retains ownership until reviewed acceptance and preserves the tested candidate before the original archive removes its worktree.

## Lookup Hints

- Keywords: `shared_resource_busy`, idle receiver, unreleased claim, uncertain dispatch, duplicate merge, candidate drift, removed worktree, archive receipt, Windows separator, allowlist, projectless, missing project membership, `project_mismatch`.
- Quick checks: inspect the current assignment generation and operation receipt; compare actual Git history with the recorded tested commit; check whether the report alone failed after successful external work; normalize path keys before comparing allowlists.
- Environment: cooperating pipelines sharing one local SQLite store, especially around release, original `m-archive`, or Windows report generation.

## Symptoms

- A downstream run waits although the previous receiver's host turn is complete.
- Archive acceptance fails because the original checkout no longer exists or final HEAD includes archive/progress metadata.
- A retry is proposed after a timeout or report error even though the merge or release marker already exists.
- Equivalent Windows paths fail a report-only comparison because one uses backslashes and the other forward slashes.

## Impact

Premature claim release can admit two writers to a shared environment. Replaying a completed external action can duplicate effects. Treating every new archive HEAD as tested can attach acceptance to the wrong product version; requiring a removed worktree can reject legitimate closeout.

## Trigger Conditions

The host finishes before the coordinator reviews the phase result; a shared resource spans multiple receivers; cleanup happens before receipt validation; or Git/filesystem paths cross APIs with different textual separators.

## Root Cause

A host observation describes a turn, not semantic completion. Git HEAD and worktree existence describe mutable checkout state, not immutable tested identity. Local transactions cannot guarantee an external action happened exactly once. Text path keys can differ while identifying the same path.

## Investigation Trail

1. The real m-pipeline pilot observed B waiting on A's shared release resource after A's receiver was already idle. The current accepted-result state showed that the wait was correct.
2. Compatibility review found archive handoffs still needed to accept retained tested identity after metadata changes and worktree deletion. Focused regression tests and both real closeouts verified the correction.
3. Pilot A merged successfully, then its report helper rejected a Windows separator difference. Independent Git and artifact checks established that the effect already existed; only report comparison needed repair.

## Resolution

- Persist a reviewed result verdict before releasing assignment/session/resource claims. Refresh host observation after dispatch, but do not use idle status alone as acceptance.
- Preserve exact tested commits, selected plan identity, original reports and durable artifact references before cleanup. Post-archive release consumes accepted archive lineage and immutable evidence; ordinary live execution/test/release still checks exact clean HEAD.
- Reconcile intent and actual artifacts before retrying uncertain external actions. Repair a missing report without replaying completed work when evidence establishes success.
- Normalize comparison keys consistently at path boundaries. Preserve actual paths for filesystem operations and retain resolved containment checks; separator normalization alone is not a containment guarantee.

## Prevention / Guardrails

- Keep real authority, phase evidence and assignment generation checks at admission and acceptance; receipt fields are not independent proof.
- Reserve all required shared resources atomically. An occupied resource should cause waiting, not unnecessary creation of another receiver.
- Test archive-before-release, release-before-archive, stale plan identity, post-cleanup retry and unknown outcome recovery separately.
- Report real-host and deterministic coverage separately. Native compaction, pending creation readiness and unrelated human activity need their own verified host contracts.
- Keep stable technical rules in the [specification](../specs/m-pipeline.md); this lesson is a troubleshooting entry, not a second workflow definition.

## Related Intake / Features / Requirements / Specs / Decisions / Changes

- [Project task ownership correction](../change/2026-09-06_pipeline-project-tasks.md)
- [Intake](../intake/2026-09-06_role-pipeline.md)
- [Feature](../features/m-pipeline.md)
- [Requirements](../requirements/m-pipeline.md)
- [Specification](../specs/m-pipeline.md)
- [Decision](../decisions/2026-09-06_role-pipeline-composition.md)
- [Change](../change/2026-09-06_m-pipeline.md)

## Project Membership Is Separate From Workdir

Symptom: a role knows the correct project path but appears as a projectless task. The live project setup copied the initial example's `target.type: projectless`; all five creation calls therefore lacked `projectId`. Passing absolute paths in bootstrap prompts did not change host membership. The original disposable pilot had verified code worktree continuity, not the user's intended project grouping.

Quick check: inspect the actual `create_thread` target and the returned task's `projectId` in host listings before debugging filesystem paths. Match `list_projects` by the real project path/host, use a project target, and verify membership before accepting readiness. The updated runtime rejects missing/mismatched project readiness receipts and preserves their operation for reconciliation.

Keep explicit standalone configurations compatible. Do not use a projectless pilot example as the default for project work or silently downgrade on pending creation. A saved non-Git umbrella can own local role tasks while individual assignments use dedicated code worktrees. Existing tasks are not moved by changing configuration or cwd; reconcile the old coordinator and use supported reassignment or explicitly authorized replacement, preserving current work and operation history.
