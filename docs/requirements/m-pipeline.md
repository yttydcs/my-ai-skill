# m:pipeline Requirements

## Status And Purpose

Implemented under the approved T1–T8 scope on 2026-09-06; validation and installation evidence are recorded in the [active plan](../../plan.md). Reduce the user's manual coordination of concurrent workflows while preserving the original skill family and its documents as authoritative contracts.

## Required Behavior

| ID | Requirement |
| --- | --- |
| R01 | Add one optional standalone companion; keep all pre-existing skill, manifest, and manual entry behavior unchanged. |
| R02 | Support explicit pipeline definitions, existing-session bindings, and one-command creation of a configured team. |
| R03 | Separate role, concrete host/session identity, workflow run, plan Task ID, and dispatch attempt. |
| R04 | Maintain one coordinator owner per run and one current admitted owner per assignment/session. |
| R05 | Continue automatically after an explicit launch contract: approved brief/revision, scope, repositories, environments, permitted phase actions, creation bounds, and escalation conditions. |
| R06 | Reuse the original `m-plan` artifact and gates; future plan generation is covered only by explicit user delegation within the launch contract, never invented user approval. |
| R07 | Support choose-one routing, distinct-task fan-out, required-result joins, and phase-appropriate repair/replan feedback. |
| R08 | Choose eligible idle sessions, create within configured capacity/creation limits, and otherwise wait without interrupting occupied work. |
| R09 | Bound execution children to one level in the first release; every child references existing admitted Task IDs, write sets, parent ownership, and a result destination. |
| R10 | Preserve exact repository/worktree/candidate identity, including multiple declared repositories under a non-Git project root. |
| R11 | Test the integrated required candidate; one successful branch, a completed turn, or an unverified receipt cannot complete the workflow. |
| R12 | Keep one owner of execute/test looping; do not nest an outer duplicate loop over an explicitly selected `m-go` or `m-continue` composite. |
| R13 | Preserve phase-owned `m-docs` invocation, use `m-context` composition in receivers, and directly call supporting skills only for work owned by the outer companion. |
| R14 | Persist recoverable creation/dispatch/claim/result records; reject duplicates and stale results and distinguish unknown external outcomes from failure. |
| R15 | Support status, cooperative pause, manual takeover, resume, and bounded fresh-session replacement. |
| R16 | Keep `m-archive` closeout semantics intact; optional deployment requires a separate configured procedure and actual authority for the selected environment. |
| R17 | Expose incomplete context, missing evidence, document conflicts, incompatible phase changes, and required user decisions without silent fallback. |
| R18 | Preserve user changes, selected private docs roots, secret handling, and publication boundaries. |

## Knowledge And Handoff Acceptance

- The recipient receives the actual project/docs roots, role/phase, plan paths, Task IDs, repository/worktree set, candidate revisions, authorization reference, context names/sections, required artifact references, and result destination.
- Context data is resolved by the existing loader with exact names and explicit scopes. Required-load failure blocks only dependent work and is reported.
- Original phase reports remain intact; a small separate receipt can link them for coordination. Receipt schema does not redefine phase acceptance.
- Stable documents are updated by their phase owners, indexed through `m-docs`, and distinguish proposed, implemented, tested, and released behavior.
- Concurrent edits to shared documentation follow explicit write ownership; changed plan/spec evidence invalidates affected dispatch or acceptance rather than changing it silently.
- A newly created receiver can continue the same bounded assignment without asking the user to restate known project context.

## Quality Requirements

- Use standard-library Python and local transactional persistence unless a capability finding proves another dependency necessary.
- Support Windows paths, spaces, Unicode, symlink/junction validation, and portable path handling; no invented server addresses or deployment commands.
- Keep state local to the current user/host. Coordinate shared session claims across cooperating runs with one authoritative store, not separate inconsistent lease layers.
- Do not hold database transactions across model/tool calls or use polling as the authority for ownership.
- Bound live sessions, total creation attempts, and child depth. Ordinary repair continues while evidence shows progress; escalation uses explicit out-of-scope/external causes or the documented non-progress policy.
- Never promise exactly-once external side effects from a local database alone. Reconcile ambiguous create/send/publish results before reuse or retry.
- Changes to old skill contracts during a run require compatibility review and selective revalidation. Do not freeze copied procedures inside the companion.

## Excluded From The First Execution Scope

- Native context compaction and occupancy telemetry integration beyond documenting optional capability flags.
- Background services, scheduled wakeup, or guaranteed continuation after the app or coordinator has stopped.
- Arbitrary recursive role graphs, distributed multi-host coordination, automatic project discovery, or revival of the retired registration service.
- Real user production deployment, credentials setup, remote publication, and changes to existing skills/tools.

## Related Documents

- [Feature](../features/m-pipeline.md)
- [Specification](../specs/m-pipeline.md)
- [Source request](../intake/2026-09-06_role-pipeline.md)
- [Decision](../decisions/2026-09-06_role-pipeline-composition.md)
- [Existing workflow requirements](m-autoflow-skill.md)
- [Active plan and Task mapping](../../plan.md)
