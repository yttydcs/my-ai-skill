# 2026-07-09 M Go Automated Execution

## Status

Accepted

## Context

The `m-*` workflow already has `$m-execute` for approved Task ID implementation and `$m-test` for optional heavy validation. The user wants a stronger automation command for cases where the main agent should act as coordinator and auditor only, while sub-agents perform all implementation edits and testing runs automatically after execution.

## Options Considered

- Add a strict mode inside `$m-execute`.
  - Rejected because it would blur the distinction between normal lightweight execution and fully delegated automation.
- Make `$m-go` an alias of `$m-execute`.
  - Rejected because `$m-go` requires mandatory delegated edits and an automatic `$m-test` loop.
- Add `$m-go` as a separate canonical entry point after planning.
  - Accepted because it keeps `$m-execute` simple while giving the user a clear high-automation path.

## Decision

Add `$m-go` as a separate canonical companion skill in the `m-*` workflow family.

`$m-go` is allowed only after a confirmed `$m-plan` artifact exists. It requires the main agent to delegate implementation edits to worker sub-agents. The main agent remains responsible for task splitting, context packages, result review, conflict handling, validation synthesis, and final acceptance. After delegated execution, `$m-go` automatically runs `$m-test` behavior. If validation fails, the main agent delegates bounded fixes and repeats the test loop until acceptance passes or the workflow reaches an explicit blocker.

`$m-go` does not own archive, merge, push, or worktree cleanup.

## Consequences

- `$m-execute` remains the lighter execution entry point.
- `$m-go` becomes the higher-automation execution and test-loop entry point.
- Sub-agent governance must explicitly distinguish optional delegation from `$m-go` mandatory delegated edits.
- Stable workflow docs and specs must include `$m-go` as a current entry point.
- Future archives should record `$m-go` delegation traces when it is used.

## Related Intake

- [../intake/2026-07-09_m-go-automated-execution.md](../intake/2026-07-09_m-go-automated-execution.md)

## Related Feature

- [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related Specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related Plan

- [../plan/2026-07-09_m-go-automated-execution.md](../plan/2026-07-09_m-go-automated-execution.md)

## Related Change

- [../change/2026-07-09_m-go-automated-execution.md](../change/2026-07-09_m-go-automated-execution.md)
