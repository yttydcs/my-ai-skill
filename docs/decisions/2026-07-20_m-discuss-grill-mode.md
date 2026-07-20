# 2026-07-20 m-discuss Grill Mode

## Status

Accepted for planning

## Context

`$m-discuss` already owns discovery, research, option comparison, requirement shaping, worktree status, governed-doc routing, and the handoff brief consumed by `$m-plan`. It does not currently define a strict interactive loop for surfacing dependent judgment calls. The public `grill-me` skill provides that loop, but its current entry file is only a wrapper around a separate `grilling` primitive and its stateless output does not satisfy this repository's durable brief and phase-boundary requirements.

## Options Considered

- Add `grill-me` and `grilling` as external skill dependencies.
  - Rejected because it would introduce upstream coupling, a two-skill invocation dependency, and host-specific invocation metadata for behavior that is small enough to own locally.
- Apply the grilling protocol to every `$m-discuss` invocation.
  - Rejected because ordinary research, option comparison, and bounded clarification should not become an open-ended one-question-per-turn interview.
- Add a separate public `$m-grill` skill that hands off to `$m-discuss`.
  - Rejected because it duplicates the discovery phase boundary and makes the user compose two overlapping entry points.
- Add an explicitly triggered internal Grill Mode to `$m-discuss`.
  - Accepted because it preserves one phase owner, keeps normal behavior backward compatible, and composes the interview discipline with the existing brief and docs workflow.

## Decision

Add a conditional Grill Mode to `$m-discuss` through a dedicated local reference, tentatively `skills/m-discuss/references/grilling.md`.

`skills/m-discuss/SKILL.md` remains the router and phase owner. It loads the new reference only when the user explicitly asks to be grilled, asks for a pressure test or hard questioning, or clearly requests decisions to be resolved one at a time. Merely receiving a vague request does not activate Grill Mode.

The Grill Mode contract must:

- research discoverable facts before asking the user;
- ask exactly one judgment question per turn and wait for the response;
- attach a recommended answer and concise rationale to each question;
- resolve parent decisions before dependent branches;
- track confirmed, rejected, deferred, and open decisions without inventing user agreement;
- re-ask or narrow the current branch when the answer is too vague to support planning;
- avoid redundant questions and permit natural-language stop or wrap-up requests instead of a hard numeric limit;
- require explicit confirmation before declaring shared understanding complete;
- return to the standard `$m-discuss` brief and exit gate after the interview;
- never invoke `$m-plan`, implementation, archive, merge, push, or cleanup automatically.

If the user stops with blocking decisions unresolved, the brief must preserve those open questions and report that the workflow cannot proceed to `$m-plan`. If the user confirms shared understanding and the existing discussion exit gate passes, the brief may report that planning is ready, but the user must still invoke or approve the next phase.

The local reference should acknowledge that the interview pattern was adapted from Matt Pocock's MIT-licensed `grilling` skill and link the upstream source and license. It must not depend on the external skill being installed.

## Consequences

- `$m-discuss` gains a high-pressure interview mode without slowing ordinary discussions.
- The existing discussion brief becomes the durable artifact missing from stateless `grill-me` sessions.
- A focused contract test is needed because one-question sequencing and the no-implementation gate are prompt-level behavior that can regress silently.
- The `m-discuss` manifest, distribution tree, and installed copy must include the new reference.
- The requirements, spec, and workflow feature docs must describe the conditional mode and its compatibility boundary after implementation.

## Confidence

High. The chosen design preserves existing phase ownership and directly addresses the gaps identified in the upstream behavior and issue history.

## Supersedes / Superseded By

- Supersedes: none.
- Superseded by: none.

## Related Intake

- [2026-07-20_m-discuss-grill-mode.md](../intake/2026-07-20_m-discuss-grill-mode.md)

## Related Features

- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Specs

- [m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related Changes

- To be added by `$m-archive` after implementation and validation.
