---
name: m-pipeline
description: Coordinate explicitly configured role sessions through the existing m-discuss, m-plan, m-execute, m-test and m-archive skills. Use for team setup, automatic handoffs, shared worker pools, waiting, or resuming a role pipeline while retaining the original manual workflow.
---

# m:pipeline

Use one coordinator per run and the original phase skill in each receiver. This companion owns assignments and recovery; the original skills own planning, implementation, testing and closeout. Existing skills need no edits.

## Select The Entry

- **Setup/team creation:** read [configuration](references/configuration.md) and [session lifecycle](references/session-lifecycle.md). Use the user's explicit existing task bindings or requested new team. Setup does not launch implementation.
- **Start/continue a pipeline:** read [phase adapters](references/phase-adapter.md) and [handoffs](references/handoffs.md). Reuse the actual launch authority; do not ask for routine continuation approval again.
- **Receiver with an assignment:** read [phase adapters](references/phase-adapter.md). Load the named contexts first, verify exact worktree/plan identity, perform only the assigned original phase, and return its report and a receipt. Receivers do not claim another assignment or run their own outer scheduling loop.
- **Status, pause, manual takeover, resume:** read [recovery](references/recovery.md).

## Coordinator Loop

1. Resolve the explicit blueprint, project/docs roots, repository map, host task identities and one user-local state root shared by cooperating runs. Invoke `$m-docs` for setup-owned governed documents; keep phase-owned docs work with the phase.
2. Use `scripts/pipeline_runtime.py validate --input <blueprint.json>`. Runtime requests are UTF-8 JSON files: `apply --input <request.json> --state-root <local-state-root>`. See reference schemas; do not invent runtime fields or host APIs.
3. Initialize/bind the team. Record the real user launch instruction and its scope with `authorize`. An autonomous architect may review a future plan only if the user actually delegated that review; otherwise retain the original user-confirmation gate.
4. Admit the complete planned assignment set for each stage, with canonical plans, write sets and dependency references, then seal that stage. Admit downstream stages as their exact candidate becomes known. Call `next` to reserve one action transactionally.
5. Execute a returned `create` or `dispatch` action through the current host's task tools. Persist its outcome immediately. Treat returned pending creation IDs as pending, not real task IDs. Reconcile unknown outcomes before any repeat.
6. Use bounded `wait_threads` calls with cursors for the actual assigned tasks. A completed turn is only an observation. Read the phase report, verify its artifacts, candidate and Task IDs, then submit the reviewed `result`. Inspect other ready work while one receiver is occupied.
7. Continue with `next`; collect all required split results and explicitly integrate before overall tests. Repair admitted failures through `invalidate`/`retry` and the original phase. `m-go`/`m-continue`, when explicitly selected, exclusively own their internal loop.
8. After every required stage is accepted, call `finish` and report durable evidence. `m-archive` remains closeout; actual deployment uses the separate authorized release procedure.

The runtime records metadata and references, never context bodies. It performs no host calls and does not prove semantic acceptance or user authorization from a string reference: the coordinator must verify both from actual messages and evidence. Local claims coordinate cooperating runs, not arbitrary external users.

First-release operation requires an active coordinator or explicit resume. Capacity and one-level children are bounded. Fresh-session replacement is available; native token telemetry, compaction, background wakeup and distributed-host ownership are not implemented.

Before reporting results, use `../m-autoflow/references/output-components.md`; show actual task statuses and clickable plan/evidence references without exposing context values.
