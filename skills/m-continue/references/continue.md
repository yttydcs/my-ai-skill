# Continue Rules

Use this reference for the unattended `$m-execute` / `$m-test` convergence loop owned by `$m-continue`.

## Phase Boundary

- Own phase recovery, automatic execute/test transitions, progress comparison, and the terminal decision.
- Reuse `$m-execute` for implementation behavior and `$m-test` for validation behavior.
- Do not restate or weaken their entry gates, checks, evidence requirements, or error handling.
- Do not own planning, archive, merge, cleanup, publication, or push.

## State Recovery

Inspect all available reliable evidence:

- approved Task IDs, write sets, acceptance criteria, test points, and statuses in the active plan
- current worktree status and diff
- the latest `$m-execute` changed-file and lightweight-validation result
- the latest `$m-test` check table, evidence, failures, blockers, or justified skip

Never infer a pass from missing evidence. If implementation appears complete but validation evidence is absent or ambiguous, enter `$m-test`. If implementation is incomplete or a failed check maps to an approved Task ID, enter `$m-execute`.

Classify the state as exactly one of:

- `repair-needed`: approved implementation is incomplete or a failed check has an in-scope repair
- `validation-needed`: implementation is ready but acceptance lacks reliable test evidence
- `converged`: every approved Task ID and acceptance criterion is satisfied and `$m-test` passed or recorded a justified skip under its own rules
- `hard-blocked`: progress requires scope, authority, information, credentials, services, assets, UI access, or an external state change unavailable within the approved workflow

## Unattended Authorization

A single `$m-continue` invocation authorizes the whole in-scope convergence loop. An ordinary implementation failure, failed test, changed failure signature, or partial improvement is not a reason to ask the user whether to continue.

Continue automatically until `converged` or `hard-blocked`, or until the non-progress rule fires. A new user instruction may override the active loop, but silence never requires another confirmation.

## Complete Cycle

A complete cycle consists of:

1. Apply `$m-execute` behavior to every currently mapped repair that is needed.
2. Run its required lightweight validation.
3. Apply `$m-test` behavior to the resulting implementation state.
4. Record the test result, failure signature, and progress evidence.

When the recovered state is `validation-needed`, the first test may establish the initial signature without a preceding repair. Count non-progress only after a subsequent complete repair/test cycle has had a real opportunity to improve that signature.

## Failure Signature

Normalize the unresolved result using stable identifiers where available:

- failing Task IDs and acceptance-criterion IDs
- failing test/check names and command names
- blocker category and relevant error class
- missing evidence category, such as UI operation or screenshot evidence

Ignore volatile timestamps, temporary paths, random IDs, and harmless output ordering. Preserve enough detail to distinguish a changed failure from the same failure recurring.

## Progress Evidence

Compare at least:

- newly completed approved Task IDs or acceptance criteria
- an in-scope diff that directly addresses a failing item
- fewer failing checks or a lower-severity failure
- new valid validation or UI evidence
- removal of a blocker prerequisite within existing authority

Any measurable improvement resets the consecutive non-progress count to zero, even when the overall cycle still fails. A changed failure signature also resets the count because the workflow reached a new state.

## Non-progress Rule

Increment the consecutive non-progress count only when a complete repair/test cycle produces:

- the same normalized failure signature as the prior comparable cycle, and
- no measurable Task, diff, validation, or evidence improvement

Stop as a non-progress loop after **three consecutive complete cycles** meet both conditions. Do not impose a separate small total-iteration limit. Report the repeated signature, the three attempted cycles, why each lacked progress, and the safest required handoff.

Do not run empty or cosmetic edits merely to reset the counter. They are not progress.

## Hard Blockers

Stop without consuming three cycles when the next required action genuinely needs:

- a new or changed requirement, architecture decision, Task ID, or write set
- user-only information or credentials that cannot be derived safely
- destructive or externally mutating authority not granted by the original workflow
- an unavailable service, asset, environment, or UI that has no safe in-scope substitute
- a tooling failure that persists after relevant safe diagnostics and alternatives are exhausted

Explain the attempts already made and the exact external change, authority, or `$m-plan` update required. Do not label ordinary test failure or a repairable implementation defect as a hard blocker.

## Successful Termination

Terminate successfully only when:

- all approved Task IDs are complete
- every acceptance criterion has passed or is covered by a valid `$m-test` skip decision
- required UI or other evidence exists when `$m-test` requires it
- residual risk from any justified skip is explicit

Report readiness for `$m-archive`. Do not invoke archive automatically.

## Progress Updates

During long loops, send concise commentary at meaningful boundaries and at least as often as the host requires. State the iteration, observed change, and next automatic phase. Do not turn an update into a continuation question.

## Terminal Report

Include:

- number of execute/test cycles
- Task IDs and changed files by iteration
- validation results and evidence
- final progress vector
- `Passed` with archive readiness, or `Blocked` with the repeated signature/hard blocker and required handoff
- risks and rollback notes
