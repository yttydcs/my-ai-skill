# Host Session Lifecycle

Discover the current host's `list_projects`, `create_thread`, `list_threads`, `read_thread`, `send_message_to_thread` and `wait_threads` tools. Native compaction and context-usage telemetry are not assumed. Do not call a separate App Server and infer access to this desktop's live tasks.

## Existing Sessions

Resolve the user's named task with host metadata, then bind its actual host/thread ID and cwd. `bind` initializes unknown readiness. Use `observe` only after a real host observation. A task can be used by several configured roles/runs, but a global session claim admits only one assignment at a time. Do not dispatch to an active, needs-input, unknown or claimed task.

An idle observation never releases an assignment. A phase result and coordinator review do that. External manual activity can race with the local runtime; recheck the host immediately before sending. If it became busy before any send, record known `not_delivered`. If send may have occurred, retain `uncertain` and reconcile.

## One-Command Team Creation

Resolve project ownership before `bootstrap`: call `list_projects`, match the user's saved project by actual path and host, and populate `target.projectId` with the returned ID. For a multi-repository umbrella, keep role tasks under that saved umbrella project unless the user explicitly chose individual repository projects. Writing `project_root` in a prompt or running `cd` does not put a task in a Codex project. Missing or ambiguous matches require resolution; they do not authorize projectless creation.

`bootstrap` uses an actual user request to create the configured initial role capacity. Loop over returned actions until each configured role is bound; no implementation is launched by setup. `next` can also request a new receiver on demand within launch bounds.

For each returned `create`:

1. Preserve its operation ID before calling the host. Put that exact ID in the new task's bootstrap prompt for recovery correlation, and use a short descriptive task title.
2. For `project`, verify the returned project ID/path/host and `isGitRepository`. Pass `create_thread` a target containing `type: "project"`, that `projectId`, and `environment`. A Git project defaults to `{type: "worktree", startingState: {type: "branch", branchName: <configured base_ref>}}`; a non-Git project uses `{type: "local"}`. Use local for Git only when the user explicitly requested the saved checkout directly. Omitted blueprint environment means worktree for compatibility. Do not invent a ref or set `onMissing: create-branch` without a user request for that branch.
3. For explicitly selected `projectless` work, create the requested projectless task. Add a short operation suffix to its directory name to distinguish intentional fresh receivers. It will have no Codex project membership. The later envelope gives its exact code worktree; default cwd is not permission to work elsewhere. Never substitute this target after a project creation error or while setup is pending.
4. The bootstrap prompt identifies the role, project/docs roots, source skill path, context references, operation ID and coordinator. Ask it to inspect its role/context, report its actual cwd/readiness and stop before phase work. A product-manager task can then receive the user's discussion separately.
5. Record `operation_result`: `{operation_id,outcome:"pending",client_thread_id,observation_ref}` for queued setup, or `{operation_id,outcome:"ready",session:{host_id,thread_id},cwd,observation_ref}` only for verified real identity. For project creation also require `project_id` from actual task metadata, matching the requested `projectId`. Use `list_threads` for project membership if `read_thread` omits it. The runtime rejects missing/mismatched project membership before binding; a reported cwd alone is insufficient.
6. When creation is pending, inspect host task listings and read the matching ready task to correlate the operation marker and cwd. Do not pass `clientThreadId` to a tool requiring `threadId`. If identity remains uncertain, preserve that state; do not create a replacement blindly.
7. Observe bootstrap completion before marking idle. Creating a task does not mean it is ready for assignment.

Emit the host-required created-task directive with actual real or pending identity when presenting newly created tasks. Do not override models or reasoning settings without an explicit request.

Validation boundary (2026-09-06): the disposable live pilot exercised projectless task creation with separately verified Git worktrees, explicit shared bindings and fresh receivers. Saved-project worktree creation and pending-ID recovery have schema/deterministic-test coverage only. At setup, verify the actual host's project metadata, ready identity and checkout before enabling either mode for a run; unknown readiness remains pending and cannot receive code work.

## Existing Projectless Teams

An installed skill update does not change existing task membership or an initialized run's immutable blueprint. Inspect the original coordinator, bindings and active claims before recovery. Do not claim that sidebar grouping, changing cwd or `handoff_thread` reassigns `projectId`; the currently exposed tools provide no general project-reassignment action. If no supported reassignment is available, present bounded project-task replacement to the user, obtain actual creation/old-task archival authority when absent, and let the owning coordinator reconcile the old run before establishing corrected bindings. Preserve operation history and do not edit live SQLite rows or the app's internal task database to simulate a move.

## Dispatch And Waiting

`next` returns a dispatch intent with operation ID and envelope. Send one readable instruction containing the role/phase, Task IDs, exact worktrees/commits, plan references, contexts, authority and reply destination. Refer to an envelope file when long; keep bodies of private contexts out of it.

Record `{operation_id,outcome:"delivered",observation_ref}` only after a known successful send. `not_delivered` is allowed only when no send occurred or rejection proves nondelivery. Use `uncertain` for timeouts/unclear results. A delayed phase result may reconcile uncertainty, but arbitrary retries cannot.

Use one bounded `wait_threads` call for up to eight assigned tasks, with each latest cursor as `afterCursor`. Wait at most 60 seconds per blocking call; communicate meaningful changes without repeating unchanged snapshots. Read the phase output when a task finishes or needs attention. Record observations before result acceptance.

## Fresh Receivers

At an inactive boundary, checkpoint progress in canonical artifacts and exact commits. After `reuse_after` completed assignments, the old session is no longer eligible. If live capacity is full, explicitly retire its local binding after verifying idle, then permit a new creation. Local retirement is not deletion or archival of a user task.

For an unfinished assignment, use pause/takeover and accept a verified failed/checkpoint report before retrying in a fresh receiver. Preserve Task IDs and repositories; change only reviewed candidate/progress references. Forking copies completed history and is not a fresh-context reset. Do not invent occupancy percentages. Capacity exhaustion waits; it does not interrupt busy work or silently increase limits.
