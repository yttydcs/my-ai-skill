# Role Pipeline Through Existing Skill Composition

## Status

Accepted on 2026-09-06 through the user's approval of T1–T8 with `$m-execute`. Implemented as a new companion; `m-orchestrator` remains removed.

## Context

The user wants automatic role/session handoffs after a product discussion while retaining manual use of the existing `m-*` family. Later requirements add concurrent executors, bounded session creation, fresh-context continuation, and strong use of existing documents and context loaders.

The original phases already define their gates, outputs, worktree ownership, document handling, and execution/testing loops. Copying those rules into a new scheduler would create competing authorities. Conversely, text instructions alone cannot coordinate concurrent claims or reconcile interrupted external calls.

## Options

| Option | Consequence | Decision |
| --- | --- | --- |
| Prompt-only role handoffs | Simple start; weak concurrent ownership and interrupted-delivery recovery | Reject as the reliability basis |
| Companion skill plus small transactional runtime | Reuses phase authority and adds auditable assignment/recovery | Accepted |
| General recursive agent framework | Broad flexibility; large lifecycle, permission, and resource-management scope | Defer |

## Decision

1. Add `m-pipeline` as a standalone package. Existing skill packages, manifests, and shared references remain untouched in this scope.
2. Use one coordinator per workflow and explicit role/session mappings. A role's current session can change without losing workflow identity.
3. Keep pipeline definition, dispatch records, and phase artifacts separate. The original plan remains the source for tasks and acceptance.
4. Use a local SQLite store for short transactional claims and operation records; host tools perform actual session actions outside transactions. Store metadata and references, not loaded context bodies.
5. Handle unknown create/send outcomes explicitly. Do not emulate exactly-once external execution with blind retries or time-based claim expiration.
6. Retain original documentation ownership. Receivers load `m-context` references and invoke their phase; the phase uses `m-docs` where required. The outer layer invokes `m-docs` only for its own setup/document work.
7. Support bounded one-level execution fan-out and fresh-session continuation before native context compaction or multi-host work.
8. Keep truthful launch delegation separate from reviewed-plan approval. No `approved: true` flag or message from another role can substitute for real user authority.
9. Implement callbacks through the current host's task tools only after capability validation. Independent role sessions are user-visible tasks, not a way to evade phase restrictions on in-phase subagents.

## Tradeoffs And Limits

- Small durable runtime support is still required even though role bindings are manually configured or created by a setup command.
- Shared session/resource serialization requires cooperating participants using the same local store. Manual takeover requires reconciliation.
- The coordinator must remain active for unattended progress in the first release. Persistent state permits recovery but does not itself provide a wakeup service.
- Native App Server compaction is documented, but access to the desktop's actual live threads is not established by that documentation.
- `m-archive` can remove worktrees, so required evidence and exact integrated revisions must be retained before closeout and optional deployment.

## Related Documents

- [Request](../intake/2026-09-06_role-pipeline.md)
- [Feature](../features/m-pipeline.md)
- [Requirements](../requirements/m-pipeline.md)
- [Specification](../specs/m-pipeline.md)
- [Archived implementation plan](../plan/2026-09-06_role-pipeline.md)
- [Existing continuation decision](2026-07-17_m-continue-loop.md)

- [Completed change record](../change/2026-09-06_m-pipeline.md)
