# 2026-07-17 m-continue Loop

## Source

- Date: 2026-07-17
- Source: Codex chat
- Requester: User

## Original Request Summary

The user requested a new `m:continue` command for workflows that have already completed an `$m-execute` or `$m-test` pass. It should keep advancing the existing workflow in a loop by applying the existing execute and test behaviors, without copying their detailed instructions into a third implementation.

## Goals

- Resume an existing approved workflow after `$m-execute` or `$m-test`.
- Alternate between implementation repair and validation until acceptance passes or a blocker is explicit.
- Reuse `$m-execute` and `$m-test` as the behavioral authorities.
- Stop before archive, merge, push, or worktree cleanup.

## Non-goals

- Do not replace `$m-go`, which starts after planning and requires delegated implementation edits.
- Do not weaken plan approval, Task ID mapping, acceptance criteria, or test evidence gates.
- Do not duplicate execution or testing procedures inside `m-continue`.
- Do not authorize new scope outside the already approved Task IDs.

## Initial Interpretation

`$m-continue` should be a thin, state-driven orchestration skill. It inspects the active plan and latest execution/test result, selects the next existing phase, and repeats only while an approved Task ID remains incomplete or validation has failed:

- incomplete implementation or failed validation -> `$m-execute`
- implementation ready for validation -> `$m-test`
- test passed or was explicitly skipped -> stop and hand off to `$m-archive`
- missing plan, unmapped work, new scope, or unresolved blocker -> stop and route to `$m-plan` or report the blocker

Invocation authorizes continued edits only within the existing approved Task IDs. Delegation remains governed by `$m-execute`; unlike `$m-go`, worker sub-agents are not mandatory.

## Open Questions

- None blocking. The exact state markers and affected packaging/tests should be defined by `$m-plan` after repository inspection.

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
