# Orchestrator Multi-repository Runtime Boundaries

## Summary

Project automation must keep three identities separate: the umbrella project, each participating Git repository, and each immutable Task request. Binding project identity to one Git root, global leases to reusable labels, or retries to mutable worktree state creates failures that appear unrelated but share the same boundary mistake.

## Lookup Hints

- Keywords: `non-Git umbrella`, `project_root is not a valid Git repository`, `git init`, `schema_version 2`, `[[repositories]]`, `project_instance_id`, `host-capacity`, `planning_ref`, `different manifest`, `manifest retry`.
- Quick checks: inspect the configured schema/repository catalog; compare canonical runtime roots; inspect opaque host project-instance IDs and lease IDs; compare the submitted manifest SHA-256 with the persisted Task before checking current worktree HEAD.

## Symptoms

- All role contexts and configuration fields validate, but Planner registration fails because the umbrella root is not Git.
- The diagnostic recommends selecting one repository root or initializing Git in a valid multi-repository umbrella.
- Two different umbrella roots with the same `project_id` and `task_id` both report acquisition of the same host lease despite capacity one.
- Retrying the exact Task manifest after a Worker commit fails because `planning_ref` no longer equals the current worktree HEAD.

## Impact

- Valid projects cannot register a Planner or schedule work.
- One project may consume or release another project's scarce host capacity.
- Safe client retries become impossible after normal Worker progress.
- Operators may be encouraged to change repository topology instead of correcting configuration/runtime boundaries.

## Trigger Conditions

- `project_root` is an umbrella containing several child repositories and is not itself Git.
- Project runtime identity is derived from one `git_common_dir`.
- Global lease ownership uses only `project_id:task_id`, which is not unique across project roots.
- Task creation performs creation-time branch/ref/worktree validation before checking whether the same immutable manifest already exists.

## Root Cause

The orchestrator reused convenient labels or mutable state as authoritative identity. An umbrella path is not a repository identity, human project/Task IDs are not globally unique, and current worktree HEAD is not the identity of an already persisted creation request.

## Investigation Trail

1. Verified the real umbrella contained many valid child Git repositories while the root's `.git` was empty and irrelevant.
2. Compared the wider `m-*` project/docs/code-repository/worktree model with schema v1's single `git_common_dir` assumption.
3. Reproduced capacity-one host admission from two roots sharing the same project and Task labels; both resolved to the same owner and lease.
4. Created a manifest Task, committed normal Worker implementation, and retried the exact manifest; validation failed before the existing Task lookup.
5. Added focused regressions and repeated the installed multi-repository flow to prove the fixes survived packaging and synchronization.

## Resolution

- Use schema version 2 with an explicit, validated repository catalog for non-Git umbrella projects.
- Bind schema v2 runtime metadata to the canonical umbrella root and configuration fingerprint, independently of child Git metadata.
- Derive host ownership from opaque hashes of canonical project runtime identity and Task ID; store only opaque project-instance metadata globally.
- Permit exact-ID continuation of legacy lease records, but never let new acquisition silently adopt ambiguous legacy ownership.
- Identify existing Tasks by immutable manifest evidence first; apply mutable worktree/ref validation only when creating the Task for the first time.
- Recheck existence under the project state lock before writing to keep concurrent creation idempotent.

## Prevention / Guardrails

- Model `project_root`, `docs_root`, repositories, and worktrees as separate configured boundaries.
- Do not recursively discover and persist repositories during ordinary validation.
- Test same human IDs across different canonical roots whenever state is shared at machine scope.
- Keep global state limited to numeric capacity and opaque ownership; never store project paths, plans, commands, context bodies, or test output there.
- Separate immutable request identity from mutable precondition validation in every retryable create operation.
- Include post-progress retries, not only immediate duplicate calls, in idempotency tests.
- Validate source, distribution, and installed copies with the same end-to-end fixture.

## Related Intake / Features / Requirements / Specs / Decisions / Changes

- [Multi-repository orchestrator intake](../intake/2026-08-04_orchestrator-multi-repo.md)
- [Project orchestrator feature](../features/m-project-orchestrator.md)
- [Project orchestrator requirements](../requirements/m-project-orchestrator.md)
- [Project orchestrator specification](../specs/m-project-orchestrator.md)
- [Multi-repository runtime decision](../decisions/2026-08-04_orchestrator-multi-repo-runtime.md)
- [Multi-repository runtime change](../change/2026-08-04_orchestrator-multi-repo.md)
- [Archived implementation plan](../plan/2026-08-04_orchestrator-multi-repo.md)
- [Orchestrator lease recovery](orchestrator-lease-recovery.md)
