# Lightweight Review and Evidence

Use at the end of execution, and when test, continuation or archive checks whether existing review evidence is still valid. This is a shared discipline, not a new phase or permission to change scope. Heavy-test skip decisions do not skip this review.

## Ownership

- `$m-execute` produces the lightweight review after focused validation; `$m-go` applies it to the integrated worker result.
- `$m-test` consumes a current review and investigates affected gaps alongside its risk-based heavy checks. It does not repeat an unchanged review merely because a new phase started.
- `$m-continue` checks freshness before reusing a prior pass. `$m-archive` verifies the final evidence and dispositions; it does not perform a second full review when inputs remain valid.
- The main agent remains accountable. Independent review lanes are useful when scope/risk warrants them and delegation is allowed; two sub-agents are not required for every change. Follow `subagents.md` for authorization and context.

## Review the Actual Candidate

1. Establish the repository/worktree and intended scope from the approved plan, Task IDs, AC IDs and original constraints. Inspect initial status and any recorded pre-existing dirt. Attribute changes by task and hunk; unrelated changes are context, not owned work. If ownership cannot be established, block the affected disposition rather than stage, overwrite or claim those changes.
2. Resolve the supplied or plan-recorded base to a full commit ID and record the actual comparison base once. Use the merge-base when reviewing branch changes; preserve an explicitly requested exact-commit comparison. Do not guess a base when several candidates would change scope.
3. Inspect the whole resulting worktree, including committed, staged, unstaged and untracked workflow-owned changes. Useful Git views (substitute the verified base SHA):

   ```sh
   git status --porcelain=v1 -z
   git diff --binary --full-index --no-ext-diff --no-textconv <review-base-sha> --
   git diff --cached --no-ext-diff --no-textconv --
   git diff --no-ext-diff --no-textconv --
   git ls-files --others --exclude-standard -z
   ```

   The base-to-worktree diff includes final tracked contents; index/worktree views expose staged-only or overlapping edits. Read relevant untracked files separately, including new tests/configuration. Check explicitly planned ignored files when they affect the result. Use NUL-safe parsing or tool-native file lists; do not split arbitrary filenames on spaces. Inspect binary, deletion, mode and symlink changes with suitable tools rather than treating absent textual hunks as no change.
4. `git diff <base>...HEAD` alone omits dirty work. An empty committed diff is not evidence that this execution has no changes. Do not commit, stash, stage, reset, clean or change unrelated work merely to make review possible. If there are truly no owned changes, report that explicitly and reconcile the Task status.

## Two Independent Conclusions

**Requirements**: compare the actual candidate with the original approved constraints and the plan's acceptance map. Check missing/partial requirements, incorrect behavior, and additions without an approved source. Preserve exact negation, numeric values/units, defaults, order and permissions. Do not rely solely on the executor's summary or a green test suite. Cite the AC/source and affected file/hunk for a finding; map missing requirements to their expected task/surface.

**Standards**: inspect changed code against applicable project conventions and important correctness/maintenance risks. Cite a documented rule for a hard violation. Label design smells as judgments with a concrete consequence, not automatic failures. Do not repeat lint/typecheck output or expand into unrelated refactoring.

Report each axis separately as `passed`, `failed`, `blocked` or `waived`, with evidence and actionable findings. A not-applicable check needs a reason; it is not a test that ran. Neither axis can compensate for failure on the other. Use the existing test/result table for evidence instead of duplicating reports.

## Evidence Identity and Freshness

Record enough metadata in the existing plan/result artifact to determine what was actually reviewed:

- repository/worktree, fixed comparison-base SHA and candidate HEAD SHA;
- identity of the workflow-owned staged/worktree changes and relevant untracked inputs: actual diff/content hashes, including file paths, deletions, modes and symlink targets as relevant (HEAD alone is insufficient for dirty work);
- plan definition identity and source references: approved scope, AC definitions, Task/write sets and material constraints; omit progress-only checkboxes/status/evidence fields, never substantive definitions;
- AC IDs and review axes covered, commands/checks run, evidence locations, findings and any explicit waiver with its authority/scope.

Existing exact candidate/plan identities from `$m-pipeline` may be reused; do not start a pipeline or require a checkpoint commit for manual review. Preserve that pipeline's admission/fingerprint rules. These records are evidence, not a claim of machine-enforced semantic correctness. Store evidence outside measured source inputs or explicitly exclude only report/progress metadata to avoid hashing the record into itself. Do not copy plaintext `$m-context`, secrets or unrelated file bodies into reports; include only necessary metadata.

Before accepting a result, recheck the relevant state. Code, dependency/configuration, source constraints or acceptance changes invalidate affected checks and dependent evidence. Unknown impact means the relevant verdict stays pending until assessed. A progress-only plan edit, evidence annotation or commit of identical already-reviewed content does not itself require rerunning tests: establish content/dependency equivalence and rebind the record. Unaffected evidence may remain valid with a reason. Never use a previous green result for a materially different candidate.

At closeout, check the actual integrated result. If the target branch advanced, conflicts were resolved, or integration changed behavior/dependencies, validate the affected result before cleanup; do not reuse feature-branch evidence without checking its applicability.

## Disposition

- Fix in-scope findings through the existing execution authority and refresh affected evidence. Changes to requirements or scope return to `$m-plan`; do not lower acceptance to make a result pass.
- A missing lightweight review returns to execution for that review; it does not automatically require the entire heavy-test phase.
- Explicit user review waivers name the skipped axis/checks, missing evidence and residual risk. A request to skip heavy testing alone is not a review waiver. Accepted risk permits only the existing phase gate's allowed transition and never turns unverified behavior into `passed`.
- Archive carries the AC/Task/evidence mapping, separate review conclusions, relevant identities and unresolved/waived items, or links the durable authoritative report. Preserve needed reports before worktree cleanup.
