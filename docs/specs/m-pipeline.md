# m:pipeline Specification

## Status And Authority

Implemented on 2026-09-06. The [active plan](../../plan.md) records admitted implementation tasks, validation and installation status. The original phase skills remain authoritative for their own prerequisites, work, evidence, and closeout.

## Package And Responsibilities

The standalone `skills/m-pipeline/` package contains:

- `SKILL.md` and `agents/openai.yaml`: entry routing and coordinator duties.
- `references/configuration.md`: explicit blueprint, launch contract, and limits.
- `references/phase-adapter.md`: composition with the installed original skills.
- `references/session-lifecycle.md`: creation, reservation, waiting, and replacement.
- `references/handoffs.md`: input envelopes, output receipts, and candidate identity.
- `references/recovery.md`: pause, takeover, reconciliation, and resume.
- `assets/pipeline.example.json`: portable, nonsecret example requiring actual user bindings.
- `scripts/pipeline_runtime.py`: command boundary, validation errors, and structured output.
- `scripts/pipeline_lib/{__init__,config,store,workflow}.py`: configuration validation, transactional state, and transition decisions.

The Python runtime uses the standard library and SQLite. It validates and records decisions; the coordinator invokes host task tools. Do not introduce an independent network service, project registration API, hidden session discovery, or copied phase implementation. The existing manifest-driven packaging tools should accept one new copy manifest without modification.

## User Entry Points

The skill supports natural-language requests corresponding to these operations. These are skill operations, not new native Codex slash commands:

| Operation | Meaning |
| --- | --- |
| Setup | Validate a blueprint and bind explicitly named existing tasks; create the configured team only when the user requests creation. |
| Start | Record the real launch instruction and start a run from the confirmed brief or an existing approved plan. |
| Status | Show current phase, assigned tasks, waiting reason, outstanding evidence, and next action. |
| Pause | Stop admitting new assignments and request a cooperative stop at a safe boundary. |
| Resume | Reconcile host activity and artifacts, then continue eligible pending work. |
| Take over | Transfer an explicitly identified assignment to manual management after reconciling its current writer. |

Setup is not launch approval. Existing-session binding is not permission to interrupt its current task. The first release requires an active coordinator for unattended progress; resume works from durable state after interruption. Background wakeup is outside this release.

## Explicit Blueprint

The user-owned JSON blueprint has a version and these validated groups:

| Group | Required contract |
| --- | --- |
| Project and documents | Explicit project root, selected docs root, and context scopes; a project root need not be a Git repository. |
| Repositories | Stable repository keys mapped to actual repository paths, configured base refs, and allowed worktree roots. Validate each repository separately. |
| Roles | Role name, original phase skill or permitted composite, context references, and eligible existing sessions or an authorized creation policy. |
| Session policy | Initial capacity, maximum live sessions, maximum total creation attempts per run, fresh-session policy, and one-level child limit. |
| Routing | Declared phase dependencies; `any` selects one receiver, `split` assigns distinct admitted Task IDs, and `join` requires all selected predecessor results. |
| Resource keys | Explicit shared integration/document/release resources that cooperating runs must serialize, even when their sessions differ. |
| Launch policy | Scope and brief revision, repositories, permitted actions and environments, plan-review delegation if any, creation limits, and escalation conditions. |

Reject unknown fields, invalid enums, duplicate identities, dangling edges, unsupported cycles, inconsistent limits, unresolved required paths, and overlapping assignments without an integration owner. Support the fixed phase progression, optional configured phases, bounded execution fan-out, and explicit repair/replan edges. Arbitrary graph recursion is not supported.

Resolve relative paths against the blueprint's location; runtime paths passed to tools are absolute. Canonicalize actual filesystem identity, including Windows case behavior and junction/symlink targets, before testing write boundaries. Do not resolve an umbrella root as the only repository or silently substitute a default checkout. Explicit context scopes follow the existing `m-context` loader's rules.

## Identities And Persistence

Keep these identities distinct: pipeline definition revision, run ID, role ID, host/session ID, repository/worktree ID, plan Task ID, assignment attempt, and external operation ID. A role can have multiple sessions; replacing one session does not replace the run or admitted task.

Use one configurable, user-local state root per cooperating host. An explicit state-root option wins; a default can be derived from the real `CODEX_HOME` when available. Fail with a configuration instruction if no safe location resolves. Do not hard-code a username or put the database inside a repository that might be published.

One SQLite database is authoritative for run/coordinator ownership, session and resource claims, assignments, external operation intents/receipts, and transition history. A second lock/lease registry must not compete with it. Session claim uniqueness spans all cooperating runs using this store. Warn explicitly if a configured shared session is managed outside that coordination boundary; never claim cross-host or noncooperating exclusivity.

Persist only metadata, hashes/revisions, reference paths, small structured results, and necessary task identity. Do not copy full context documents, messages containing credentials, or secret environment values into blueprints, receipts, logs, or fixtures. Authorization references must identify the actual user instruction and its bounded scope; fabricated booleans are not evidence.

## Transition And Claim Rules

Run states are `draft`, `ready`, `running`, `waiting`, `paused`, `needs_input`, `complete`, and `cancelled`. Assignments separately track `pending`, `reserved`, `dispatched`, `running`, `result_pending`, `passed`, `failed`, and `uncertain`. Host turn status is an observation, not an assignment verdict.

1. Check prerequisites, plan revision, permitted scope, and candidate identity before admission.
2. Atomically reserve an eligible session, assignment attempt, and all required shared resources. If any is unavailable, reserve none and enter a documented wait.
3. Persist an immutable operation intent before a host call. Leave the transaction before context preparation or any model/tool/network call.
4. Record the returned real identity and receipt, using compare-and-set checks against the current assignment generation. Repeated known receipts are idempotent; mismatched or stale results are rejected.
5. Accept completion only after reconciling the stage evidence, expected Task IDs, authorized plan revision, and exact candidate. Persist the verdict before releasing the claim.
6. Never hold a downstream session while waiting only for upstream work. A controller admits new work only while it owns the run.

An idle host status does not prove that an assignment has completed. A clock timeout does not authorize claim reclamation. Cooperative pause and takeover retain claims until the old writer is known inactive and ownership is transferred explicitly. Acquire shared resources atomically to avoid partial-acquisition deadlocks; use a stable queue order for competing eligible assignments.

Unknown create, send, or release outcomes become `uncertain`: inspect operation markers, host identity, and actual artifacts before deciding whether to acknowledge or retry. When observation cannot establish the outcome, expose that blocker. Do not blindly retry a potentially delivered instruction, create duplicate sessions, or promise exactly-once external effects.

## Host Capability Gate

The initial implementation task must verify the installed host's actual tools and record supported, unsupported, and unproven capabilities. Required checks include:

- Existing-session lookup and stable host/thread identities.
- Creation from an explicitly configured project and starting Git state; actual destination checkout verification.
- Asynchronous creation that may return only `clientThreadId` initially. Do not use it as a real `threadId`; reconcile readiness first.
- Message delivery and bounded waiting with cursors; final or needs-attention status must still undergo phase acceptance.
- Recovery from a tool timeout whose external action may have succeeded.
- One coordinator's ability to continue waiting and dispatching while active.

There is no documented atomic host reservation in the current exposed task tools. Local claims coordinate cooperating users of this runtime; recheck host observations immediately before dispatch. An external user can still operate a task outside this protocol, which requires reconciliation rather than a stronger guarantee.

The current exposed task tools do not provide native context occupancy or compaction. App Server documents `thread/compact/start`, asynchronous compaction events, and token-usage events, but availability in another interface does not establish access to this desktop's live tasks. Do not launch a separate server and assume shared ownership. Native compaction remains optional and deferred; first-release correctness depends on explicit fresh-session replacement.

Capability references: [App Server](https://learn.chatgpt.com/docs/app-server#trigger-thread-compaction) and [CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli). Revalidate against the actual host before future integration. If exact checkout creation or another required capability is unavailable, mark the affected mode unsupported and surface it; do not silently downgrade its semantics.

## Launch Authority And Original Phase Composition

Default role mapping is product manager → `m-discuss`, architect → `m-plan`, executor → `m-execute`, tester → `m-test`, and release owner → `m-archive`. Roles are configuration, not five new skill packages. A session may retain one role across runs but can own only one admitted assignment at a time.

A launch instruction must explicitly authorize subsequent work within its recorded scope. For autonomous planning, it must also delegate review of generated plans within that scope to the designated role. Record that review as delegated acceptance, never as a plan personally reviewed by the user. Without such delegation, the original user-confirmation gate still applies. No sibling message can grant authority that the user did not give. Scope expansion or an unresolved product choice returns to the product manager/user.

Read the actual original skills and referenced contracts at stage entry. Record their relevant revisions/hashes for drift detection without vendoring copies. Each stage uses the existing initialization, dedicated worktree, root plan, Task IDs, acceptance, evidence, and closeout rules. Independent role sessions must not be used to bypass restrictions on subagents inside a phase.

The default coordinator owns transitions between execute and test, admitting only plan-authorized repair work. If a blueprint explicitly uses `m-go` or `m-continue`, that composite exclusively owns its internal loop. `m-continue` retains its prerequisite of an existing execute/test pass. The outer layer waits for the composite result and does not run another nested repair loop.

Repeated work should advance on evidence. Distinguish actionable test failures from unresolved infrastructure, conflicting artifacts, and non-progress. Apply a documented bounded non-progress policy to prevent endless retries; ordinary successful progress needs no repeated continuation approval.

## Handoff Envelope And Result Receipt

The envelope carries:

- Run, role/phase, assignment/attempt and operation IDs, plus reply destination.
- Absolute project/docs roots, actual repository and worktree mappings, base/candidate revisions, and ownership boundaries.
- Canonical root plan path and revision, admitted Task IDs, expected evidence, dependencies, and relevant stable document references.
- Actual launch-authority reference and restrictions.
- Context names/sections with explicit scopes and prerequisite load failures, if any.

Receivers use the original phase's report format. A separate structured receipt links that report and its evidence, including completed/blocked Task IDs, candidate identity, remaining work, and result generation. The receipt coordinates execution; it cannot redefine phase acceptance or convert a generic final message into a pass.

Persist external evidence needed for resume before a worktree is removed. After archive, retain verified commit identities and the archive's durable paths; invalidate disposable paths rather than continuing to read them.

## Fan-Out, Integration, And Replacement

`any` waits for or selects one eligible receiver. `split` distributes different admitted Task IDs with disjoint write sets into isolated validated worktrees. Group children have a parent assignment and a result destination; children cannot spawn another level in this release. Run-wide live and total-creation limits include replacement and child sessions. Session/worktree/resource claims are shared across cooperating runs in the same store; limits do not describe unrelated host tasks.

A designated integration owner assembles all required outputs into the planned candidate, resolving conflicts within admitted scope. Candidate assembly must be explicitly planned and is not an early release merge into the base branch. The join checks the complete required set and then validates the exact integrated revision across participating repositories. If integration changes that revision, affected tests become stale. Never accept a single child pass as overall completion.

Fresh-session replacement is permitted only after the prior writer is known inactive and its progress is durable. Reuse the same assignment context and exact candidate; do not replay completed Task IDs. If supported host creation cannot recover the exact checkout/state, require reconciliation. A fork copies history and is not a substitute for a fresh context.

Without token telemetry, do not invent a context percentage. Use explicit user replacement, observable context problems, or a configured completed-assignment reuse bound at safe boundaries. Replacement may wait when creation capacity is exhausted.

## Documentation And Context Composition

| Owner | Required use |
| --- | --- |
| Outer setup/coordinator | Invoke `m-docs` for its own stable setup/document changes; establish canonical roots and route/index those documents once. |
| Stage receiver | Co-invoke `m-context` for required role/project context before invoking the phase; resolve exact references using the existing loader. |
| Architect / `m-plan` | Let the existing phase invoke `m-docs` and maintain the canonical plan and governed design documents. |
| Release owner / `m-archive` | Let the existing phase invoke `m-docs` and perform its existing archive/merge/cleanup contract. |
| Runtime | Store references, ownership and receipts; do not create a second requirement, plan, or document-governance system. |

Required context failures block dependent work with a useful error. Shared document writes require an owner/resource claim. Referenced document and plan revisions are checked on admission and result acceptance. Record the admitted task-definition/scope revision separately from execution-progress updates: a changed acceptance criterion or write set can invalidate work, while appending a progress receipt must not invalidate the assignment that produced it. Material changes invalidate affected pending work or test evidence and require selective revalidation, not unconditional restart of every stage.

Manual takeover uses the same plan, Task IDs, worktrees, context references, and evidence. Resume observes those artifacts before scheduling remaining work. No private docs, secrets, or user-global context are copied into a public code repository for convenience.

## Closeout And Optional Release

`m-archive` remains document/archive/merge/cleanup work. A deployment step requires an explicitly configured procedure, target environment, authorized action, durable candidate, acceptance evidence, and rollback reference. The blueprint must state whether that procedure consumes a tested worktree before cleanup or a durable artifact/commit afterward; there is no assumed universal deployment order.

Claims on a shared environment remain held while an external release outcome is uncertain. Implementation validation uses a harmless fixture release that writes a local marker; actual production deployment, credentials, pushes, and infrastructure provisioning are outside this plan.

## Verification Contract

Focused tests must cover malformed configuration; Windows/Unicode paths; multi-repository roots; two-process claim contention; resource acquisition rollback; duplicate/stale/out-of-order receipts; interrupted creation/dispatch; pause/takeover/resume; capacity limits; required join results; exact integrated candidate validation; context-load failures; delegation boundaries; and loop ownership.

Host integration uses a fake adapter for deterministic faults and a bounded disposable real-host pilot for supported behavior. Compare pre-existing source skills, manifests, tools, and tests against the planning baseline. Validate and sync only the new manifest. Report capability gaps and any skipped platform checks explicitly; a mocked pass is not a real-host pass.

## Related Documents

- [Feature](../features/m-pipeline.md)
- [Requirements](../requirements/m-pipeline.md)
- [Decision](../decisions/2026-09-06_role-pipeline-composition.md)
- [Original request](../intake/2026-09-06_role-pipeline.md)
- [Existing phase contract](m-autoflow-skill.md)
- [Context contract](m-context-skill.md)
- [Documentation contract](m-docs-skill.md)
