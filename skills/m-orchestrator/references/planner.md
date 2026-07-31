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
- Persist the approved Task IDs, plan location, planning commit/ref, base branch, write sets, acceptance, tests, rollback, and project identity before dispatch.
- A planning ref handed to a Worker must contain the exact approved `plan.md` or `todo.md` state.

## Worker Dispatch

Before creation, confirm that the user approved the exact Task IDs and that host project/thread tools are available.

On Codex hosts, search for the current `list_projects`, `create_thread`, `wait_threads`, `read_thread`, and `send_message_to_thread` tools instead of assuming a fixed wrapper. Use `create_thread` non-blockingly; for a Git project, select its Worktree environment. Prefer compact `wait_threads` snapshots over repeated full thread reads.

Create one background project Worker for one approved task workflow. For a Git project, request a dedicated Worktree starting from the committed planning ref. The initial prompt must contain:

- role: Worker
- project ID and project root
- docs root and configuration path
- repository, base ref, and expected planning ref
- exact Task IDs and titles
- active plan path and confirmation requirement
- write sets, forbidden paths, acceptance, tests, and rollback
- required configured contexts
- runtime helper path and Task record ID
- Planner task/thread ID for status handoff
- instruction to use `$m-execute`, not `$m-go`
- instruction to stop on new scope, missing authority, invalid config, or unavailable environment

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

Passing Workers queue for the configured capacity-one archive/integration pool. Before integration, compare the Task branch with the latest base. If reconciliation changes executable content, require the appropriate lightweight gate and heavyweight validation again before `$m-archive` proceeds.
