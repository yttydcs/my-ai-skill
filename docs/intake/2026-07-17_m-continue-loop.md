# 2026-07-17 m-continue Loop

## Source

- Date: 2026-07-17
- Source: Codex chat
- Requester: User

## Original Request Summary

The user requested a new `m:continue` command for workflows that have already completed an `$m-execute` or `$m-test` pass. It should keep advancing the existing workflow in a loop by applying the existing execute and test behaviors, without copying their detailed instructions into a third implementation. One invocation must authorize unattended iteration: the Agent must not ask whether to continue between execute and test passes, and may stop only after the approved acceptance scope has fully converged or further progress is genuinely impossible.

## Goals

- Resume an existing approved workflow after `$m-execute` or `$m-test`.
- Alternate automatically between implementation repair and validation until acceptance fully passes or progress is genuinely impossible.
- Reuse `$m-execute` and `$m-test` as the behavioral authorities.
- Treat invocation as authorization for every in-scope execute/test iteration without repeated confirmation.
- Detect non-progress loops from evidence rather than imposing an arbitrary iteration limit.
- Stop before archive, merge, push, or worktree cleanup.

## Non-goals

- Do not replace `$m-go`, which starts after planning and requires delegated implementation edits.
- Do not weaken plan approval, Task ID mapping, acceptance criteria, or test evidence gates.
- Do not duplicate execution or testing procedures inside `m-continue`.
- Do not authorize new scope outside the already approved Task IDs.
- Do not pause merely because one execution or test pass failed.
- Do not ask the user whether to continue during a normally progressing loop.

## Initial Interpretation

`$m-continue` should be a thin, state-driven orchestration skill. It inspects the active plan and latest execution/test result, selects the next existing phase, and repeats only while an approved Task ID remains incomplete or validation has failed:

- incomplete implementation or failed validation -> automatically apply `$m-execute`
- implementation ready for validation -> automatically apply `$m-test`
- test passed or was explicitly skipped under the existing test rules, with all approved acceptance criteria satisfied -> stop successfully and hand off to `$m-archive`
- a single execute/test failure -> record progress evidence and continue automatically
- an identical failure signature persists across consecutive complete repair/test cycles with no Task status, code-diff, or validation-evidence improvement -> stop as a non-progress loop
- progress requires new scope, new authority, user-only information, or an external state change that cannot be produced in scope -> stop as genuinely unable to continue

Invocation authorizes every continued edit and validation pass within the existing approved Task IDs, so no additional continue confirmation is required. Delegation remains governed by `$m-execute`; unlike `$m-go`, worker sub-agents are not mandatory. Intermediate status updates are allowed, but they must not pause the loop or ask the user to choose whether the next in-scope iteration should run.

## Open Questions

- None blocking. `$m-plan` should define the exact progress signature and a conservative consecutive-cycle threshold for declaring a non-progress loop; the recommended default is three complete repair/test cycles with the same failure signature and no measurable improvement.

## Stable Docs Impact

- Feature impact: update `docs/features/m-autoflow-workflow.md`.
- Requirements impact: update `docs/requirements/m-autoflow-skill.md`.
- Specs impact: update `docs/specs/m-autoflow-skill.md`.
- Decision impact: add `docs/decisions/2026-07-17_m-continue-loop.md`.

## Routed Docs

- [Decision](../decisions/2026-07-17_m-continue-loop.md)
- [Workflow feature](../features/m-autoflow-workflow.md)
- [Workflow requirements](../requirements/m-autoflow-skill.md)
- [Workflow spec](../specs/m-autoflow-skill.md)

## Related Changes

- No implementation or change archive exists yet.
