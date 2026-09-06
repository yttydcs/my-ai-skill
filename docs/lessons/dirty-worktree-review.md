# Reviewing Dirty Worktrees

## Summary

A branch-only diff can miss implementation that has not been committed. Review the actual owned candidate and preserve its evidence identity before handoff. The [shared review reference](../../skills/m-autoflow/references/review.md) defines the workflow rule; this lesson records the reproducible failure pattern.

## Lookup Hints

- Keywords: empty committed diff, dirty worktree, staged-only change, untracked test, overlapping edits, stale review, candidate identity.
- Symptoms: an implementation is reported complete while a review sees no changes, or a newly added test is absent from review.
- Quick checks: inspect Git status, base-to-worktree diff, index diff, unstaged diff and NUL-delimited untracked paths.

## Symptoms

`git diff <base>...HEAD` omits uncommitted implementation and new untracked files. A final worktree file can also equal its baseline while its staged content differs, hiding the index change from the base-to-worktree view.

## Impact

Review may falsely claim coverage, or carry a previous pass to a different candidate. An attempted cleanup or forced commit can also disturb unrelated user work.

## Trigger Conditions

Execution hands off before commit; index and worktree contain overlapping edits; new tests remain untracked; or requirements change after an earlier pass.

## Root Cause

Git HEAD, the index, the working tree and untracked inputs are different surfaces. A single commit comparison does not describe all of them.

## Investigation Trail

1. Created temporary Git repositories with committed, staged, unstaged, deleted and untracked files, including a filename with spaces and Chinese characters.
2. Staged an overlapping edit, then restored only its working-tree contents to the baseline. The index still contained a change.
3. Executed the commands directly from the shared review reference. Their combined output covered every surface.
4. Compared HEAD, index entries, status and file bytes before and after review; the commands preserved all of them.

## Resolution

Use complementary views, read new files separately, and attribute only workflow-owned changes. The executable reproduction is retained in [test_m_acceptance_review_contract.py](../../tests/test_m_acceptance_review_contract.py).

## Prevention / Guardrails

- Do not equate an empty committed diff with no implementation.
- Record actual candidate and plan identity, including relevant dirty inputs; refresh only affected evidence when inputs change.
- Do not force a commit or clean a worktree merely to enable review.
- Keep expected behavior independent of implementation, and distinguish supplied scenario facts from checks actually run.

## Related Intake / Features / Requirements / Specs / Decisions / Changes

- [Intake](../intake/2026-09-06_acceptance-review.md)
- [Feature](../features/m-autoflow-workflow.md)
- [Requirements](../requirements/m-autoflow-skill.md)
- [Spec](../specs/m-autoflow-skill.md)
- [Change](../change/2026-09-06_acceptance-review.md)
- Architecture decision impact: none; existing phase ownership remains in place.
