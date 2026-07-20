# 2026-07-20 m-discuss Grill Mode

## Source

- Date: 2026-07-20
- Source: Codex chat
- Requester: User

## Original Request Summary

The user asked for a detailed investigation of the public `grill-me` skill and whether its behavior could be integrated into the repository's existing `$m-discuss` skill. After reviewing the current upstream source, related documentation, history, license, and reported failure modes, the user invoked `$m-plan` to plan the recommended integration.

## Confirmed Requirements

- Keep `$m-discuss` as the owning discovery and requirement-shaping phase.
- Add a Grill Mode that is enabled only when the user explicitly asks to be grilled, pressure-test a plan, or resolve decisions one at a time.
- Reuse the useful `grilling` behaviors without creating a runtime dependency on the external `grill-me` wrapper.
- Look up discoverable facts before asking the user.
- Ask exactly one decision question per turn, include a recommended answer and rationale, and wait for feedback.
- Resolve dependent decisions depth-first and keep confirmed, rejected, deferred, and open decisions distinguishable.
- Preserve the existing `$m-discuss` brief, docs routing, worktree status, and `$m-plan` handoff.
- Never enter planning or implementation automatically when the interview ends.
- Allow the user to stop and request a summary without imposing a fixed question count.

## Non-goals

- Do not install `mattpocock/skills` as a project dependency.
- Do not add a separate public `$m-grill` skill.
- Do not force one-question-at-a-time interviewing for ordinary `$m-discuss` requests.
- Do not copy the upstream skill verbatim or track all future upstream changes automatically.
- Do not alter `$m-plan`, `$m-execute`, or `$m-archive` phase ownership.

## Research Summary

- The current upstream [`grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) is a small user-invoked wrapper around the reusable [`grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) primitive.
- The reusable primitive requires a depth-first decision interview, one question at a time, a recommended answer per question, self-service lookup of facts, and explicit user confirmation before action.
- The upstream repository is MIT licensed, but this workflow will adapt the behavioral ideas and retain source attribution instead of copying the wrapper as a dependency.
- Upstream issues document three risks that the local contract must address: bundled questions, excessive/redundant questioning, and jumping directly to implementation after the interview.

## Open Questions

- None blocking. Exact wording and test assertions may be refined during execution without changing the confirmed behavior.

## Stable Docs Impact

- Feature impact: clarify `docs/features/m-autoflow-workflow.md` after implementation.
- Requirements impact: clarify `docs/requirements/m-autoflow-skill.md` during execution.
- Specs impact: clarify `docs/specs/m-autoflow-skill.md` during execution.
- Decision impact: add `docs/decisions/2026-07-20_m-discuss-grill-mode.md` during planning.
- Lessons impact: none known at planning time.

## Routed Docs

- [Decision](../decisions/2026-07-20_m-discuss-grill-mode.md)
- [Workflow feature](../features/m-autoflow-workflow.md)
- [Workflow requirements](../requirements/m-autoflow-skill.md)
- [Workflow spec](../specs/m-autoflow-skill.md)

## Related Changes

- To be added by `$m-archive` after implementation and validation.
