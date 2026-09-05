# Recovery And Manual Control

Read `status` and actual host observations before mutating recovery state. Durable intent is not evidence that a host action was delivered or completed. Never reclaim ownership solely because time elapsed or a task looks idle.

| Action | Payload and effect |
| --- | --- |
| `pause` | `{}` stops admission; active assignments and claims remain |
| `takeover` | `{job_id,observation_ref}` after pause and verified inactive writer; frees the receiver but retains worktree/resource claims until manual evidence is accepted |
| `result` | Review manual changes against the same plan/Task IDs and submit their evidence for the surrendered operation; do not replay those tasks |
| `invalidate` | `{job_ids:[...],reason_ref}` marks affected tasks and transitive downstream evidence stale; affected active/manual writers must first be reconciled |
| `retry` | `{job_id,repositories,plans,review_ref}` refreshes reviewed candidate/plan references for failed work, increments its generation, and preserves Task IDs/write scope |
| `resume` | `{}` requires reconciled creation/delivery intents and accepted manual results; continues remaining work |
| `transfer` | `{new_coordinator:{host_id,thread_id},observation_ref}` while paused; current coordinator explicitly transfers ownership |

A fixed coordinator can resume in a later turn from the same state root/run ID. To replace it, transfer ownership while it is available and paused. If it cannot relinquish ownership safely, keep the run blocked for explicit user reconciliation rather than forging the old actor identity.

For a known host rejection before sending, submit `operation_result` with `not_delivered`; the runtime releases the reservation. After a timeout/unknown delivery, record `uncertain`. Read the intended receiver and correlate its operation marker, actual phase progress and artifact evidence. If it ran, accept its verified result. If an interrupted assignment needs manual recovery, pause, establish that the old writer stopped, and use takeover. Do not resend an uncertain instruction as a new operation merely to make progress.

Pending/uncertain creation remains counted against limits. Resolve its actual task identity and record ready, or retain the blocker. A verified creation failure can be recorded as `not_delivered`; inspect the host before doing so. Blind retry is not recovery.

When code or acceptance changes, invalidate only the affected tasks and downstream evidence. Retry reviewed work from the exact current commit and updated plan fingerprint, then resume. Progress-only plan changes need no invalidation. Skill-contract drift requires compatibility review before a retry records a new contract hash.

Ordinary in-scope repairs continue automatically. Identical failure signatures reaching `max_nonprogress` stop repetition and require a revised decision/scope. Do not reset counters to conceal non-progress. Preserve unresolved evidence and report the actionable reason.

Retiring a local session binding requires idle and no active claim. It does not archive or delete the task. Archive only specifically authorized completed workflow/test tasks with the host's archive tool. No runtime command deletes worktrees, publishes documents, sends messages to external parties, or removes context data.
