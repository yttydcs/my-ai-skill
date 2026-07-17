# 2026-07-17 m-continue Loop

## Status

Accepted

## Context

The workflow already provides `$m-execute` for approved implementation and lightweight validation, `$m-test` for optional heavy validation, and `$m-go` for a fully delegated execute/test loop that starts after planning. A workflow that has already returned from `$m-execute` or `$m-test` still needs a concise way to resume and converge without restating either phase or adopting `$m-go`'s mandatory delegation model.

## Options Considered

- Add loop instructions independently to both `$m-execute` and `$m-test`.
  - Rejected because phase ownership would become less clear and the same transition rules would be duplicated.
- Extend `$m-go` to resume any execution or test result.
  - Rejected because `$m-go` has a distinct entry gate and requires all implementation edits to be delegated.
- Add `$m-continue` as a thin state-driven orchestrator over `$m-execute` and `$m-test`.
  - Accepted because it preserves the existing phase authorities and supports continuation without imposing a new execution model.

## Decision

Add `$m-continue` as a canonical companion skill for an already approved workflow after at least one `$m-execute` or `$m-test` pass.

The skill must inspect the active plan and latest phase evidence before choosing the next phase. It invokes existing `$m-execute` behavior for incomplete implementation or failed validation, then existing `$m-test` behavior when implementation is ready for validation. It repeats until acceptance passes, testing is explicitly skipped under the existing test rules, the user changes direction, or a blocker is explicit.

`$m-continue` must reference the authoritative execute and test instructions instead of restating their detailed procedures. Its own instructions should contain only entry gates, state transitions, loop termination, authorization boundaries, and orchestration output.

Invoking `$m-continue` authorizes continuation only within the already approved Task IDs and write sets. New requirements, unmapped fixes, or architecture changes return to `$m-plan`. Delegation follows `$m-execute` rules and is optional when permitted; `$m-continue` does not acquire `$m-go`'s mandatory worker-only editing boundary.

The skill stops before `$m-archive`, merge, push, publication, or worktree cleanup.

## Consequences

- Users can resume a partially converged workflow with one command after either execution or testing.
- `$m-execute` and `$m-test` remain the single sources of truth for phase behavior.
- `$m-go` remains the separate post-plan, mandatory-delegation automation path.
- Packaging, manifests, workflow routing, stable docs, and focused contract tests must recognize `m-continue`.
- The implementation must avoid ambiguous phase recovery by defining which plan/result evidence determines the next transition.

## Confidence

High. The boundary follows existing phase ownership and addresses a continuation use case not covered by `$m-go` without duplicating phase logic.

## Supersedes / Superseded By

- Supersedes: none.
- Superseded by: none.

## Related Intake

- [2026-07-17_m-continue-loop.md](../intake/2026-07-17_m-continue-loop.md)

## Related Features

- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Specs

- [m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related Changes

- No implementation or change archive exists yet.
