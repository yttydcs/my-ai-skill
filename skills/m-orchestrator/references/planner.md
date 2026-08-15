# Planner Contract

## Ownership

One registered Planner task owns project-level discussion, architecture, approval, dispatch, status synthesis, and integration decisions. It does not implement work that has been dispatched to a Worker.

## Registration

1. Validate project configuration.
2. Register the current Codex task/thread ID in project runtime state.
3. If another Planner is registered, inspect its host status before replacement.
4. Replace a live Planner only after explicit user direction. A stale or missing task may be replaced with the reason recorded.

## Planning And Handoff

- Use configured Planner contexts before `$m-discuss` or `$m-plan`.
- Follow the normal dedicated branch/worktree and confirmed root-plan gates.
- Persist the approved Task IDs, canonical plan, participating repository IDs, per-repository planning refs, base refs, branches, worktrees, root plans, write sets, acceptance, tests, rollback, and project identity before dispatch.
- Every participating repository has its own dedicated branch, worktree, and root `plan.md` or `todo.md`. A planning ref handed to a Worker must identify that repository's exact committed planning state.
- Create the validated Task manifest before host dispatch. An undeclared repository or later worktree-set expansion requires a return to planning.

## Worker Dispatch

Before creation, confirm that the user approved the exact Task IDs and that host project/thread tools are available.

On Codex hosts, search for the current `list_projects`, `create_thread`, `wait_threads`, `read_thread`, and `send_message_to_thread` tools instead of assuming a fixed wrapper. Use `create_thread` non-blockingly; for a Git project, select its Worktree environment. Prefer compact `wait_threads` snapshots over repeated full thread reads.

Create one background project Worker for one approved task workflow. For a schema version 1 Git-root project, the host may create the dedicated Worktree from the committed planning ref. For a schema version 2 project, prepare every participating repository worktree first, then create the Worker in the umbrella local project or an explicitly designated primary worktree and pass the complete absolute worktree map. Do not assume one host-created worktree represents a multi-repository Task.

The initial prompt must contain:

- role: Worker
- project ID and project root
- docs root and configuration path
- ordered repository IDs and, for each repository, its root, base ref, branch, expected planning ref, worktree, root plan, and write set
- exact Task IDs and titles
- active plan path and confirmation requirement
- write sets, forbidden paths, acceptance, tests, and rollback
- required configured contexts
- runtime helper path and Task record ID
- Planner task/thread ID for status handoff
- instruction to use `$m-execute`, not `$m-go`
- instruction to stop on new scope, missing authority, invalid config, or unavailable environment

The Worker must be able to access every listed worktree before binding succeeds. Missing host multi-path access blocks dispatch instead of silently dropping a participating repository.

Task creation is non-blocking. Bind the returned Worker task/thread and host IDs to the `DISPATCHING` Task record before reporting successful dispatch. Worker binding atomically enters `EXECUTING` and is idempotent only for the same IDs. If creation succeeds but binding fails, preserve the returned IDs and report a reconciliation blocker rather than creating a duplicate Worker.

## Continuing Planning

After dispatch is recorded, return control to the user immediately. Do not wait for the Worker merely to keep the Planner turn open. The Planner may discuss and plan another task in a separate planning worktree while background work continues.

Use compact wait/status snapshots only when:

- the user asks for status;
- a Worker reports completion or needs attention;
- stale lease recovery requires live-owner inspection;
- integration admission depends on current Worker state.

Do not repeatedly poll unchanged tasks or narrate unchanged snapshots.

## Integration Coordination

Passing Workers queue for their project's configured capacity-one archive/integration pool. Ordinary contention stays `WAITING_FOR_MERGE`; it is not a blocker. Project release/status may return `next_ready` with the persisted Worker callback. Send that Worker a targeted retry message, but do not describe the wakeup as ownership: only successful acquisition authorizes archive. A missed wakeup is recoverable from project status.

Before integration, revalidate the recorded composite change identifier and every selected repository's recorded base head. Drift removes the stale archive ticket, returns the Task to execution, and requires the appropriate lightweight gate and heavyweight validation again before `$m-archive` proceeds. Archive pools remain project-local and never consume the optional Tester host budget, so independent projects may archive concurrently.

Cross-repository integration uses complete preflight plus the manifest repository order. It is not atomic: if a later repository cannot integrate, persist the completed and pending repository results, block the Task, and require an explicit recovery decision. `$m-archive` remains the authority for commits, control-plane merges, docs handling, and cleanup.

After stale ownership, reclaim, or partial integration, do not wake or admit an unrelated queued Task while the project reports an archive recovery hold. Resume the affected owner only after the explicit recovery decision is recorded.
