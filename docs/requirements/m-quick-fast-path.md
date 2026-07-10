# m:quick Fast Path Requirements

## Background

The staged `m-autoflow` workflow provides strong planning, isolation, validation, and archival controls, but that overhead is disproportionate for small changes with obvious intent, bounded impact, and simple rollback. A separate fast path is needed without giving up governed project context.

## Goal

Provide a direct one-command path for low-risk work that always reads relevant docs before editing, preserves current repository work, validates the affected behavior, and escalates unsuitable requests before scope expands.

## Scope

### Must

- provide `$m-quick` as a canonical standalone command in the `m-*` family
- require explicit fast/direct intent
- use `$m-docs` to restore the minimum relevant context before eligibility or edits
- select exactly one target Git repository
- allow direct current-checkout edits without a quick-request worktree or plan
- keep the main agent responsible for implementation
- preserve user changes and honor project-local instructions
- use a risk-based eligibility gate rather than a hard file/line limit
- reject ambiguous, cross-repo, architectural, public-contract, schema, migration, security, destructive-data, infrastructure, or broad dependency work
- run focused validation and report honest evidence
- require actual UI operation and screenshots for UI-impacting quick changes
- update stable docs only when stable truth changes
- provide a compact direct result table
- avoid automatic archive, merge, cleanup, push, publication, or deployment

### Optional

- update a clearly owned stable feature, requirement, or spec through `$m-docs`
- commit when the target project's local instructions require it or the user explicitly asks
- continue when docs are absent only if local evidence keeps the change self-contained and unambiguous

### Out Of Scope

- replacing staged workflow governance for higher-risk work
- creating workflow history artifacts for every quick request
- choosing docs remotes, backup destinations, push targets, or deployment environments
- using implementation sub-agents or automatic `$m-test` loops

## Scenarios

- A localized bug must be restored to behavior already described by feature docs.
- A small behavior adjustment has clear acceptance and no wider contract impact.
- A dirty working tree contains unrelated user changes that can be preserved.
- A request appears small but reveals a schema, security, architecture, or cross-repo boundary and must be escalated.
- A UI tweak can be exercised through a bounded actual-user-path smoke test.

## Functional Requirements

- Resolve project/docs/repo boundaries before editing.
- Read project-local instructions before generic defaults.
- Read `docs/README.md`, the relevant category index, and matching stable docs through `$m-docs`.
- Prefer `lessons` before `change` for recurring bugs and symptoms.
- Fail the gate when docs conflict or target-repo ownership is ambiguous.
- Inspect Git status and pre-existing diffs before modifying files.
- Apply the smallest safe change in the current checkout after the gate passes.
- Stop broadening when new risk invalidates eligibility.
- Run focused checks and distinguish pre-existing failures.
- Perform stable-doc impact routing after validation.
- Return gate, context, changes, validation, docs impact, and residual risk directly to the user.

## Non-functional Requirements

- Performance: read only the minimum relevant docs and avoid unnecessary workflow setup.
- Safety: fail closed on prohibited risk, ambiguity, overlap, or unavailable required evidence.
- Maintainability: reference `$m-docs` instead of copying its taxonomy.
- Traceability: expose the docs read and checks run in the final table even when no archive is created.
- Extensibility: keep detailed classification rules in one reference file.

## Edge Cases

- No governed docs root exists.
- A docs root exists but the affected feature has no dossier.
- Several repositories match the request.
- The current checkout is dirty in target files.
- The implementation is generated but its source is unclear.
- A focused test is blocked by unrelated repository configuration.
- UI evidence cannot be gathered.
- A local change unexpectedly needs a new architecture decision.

## Acceptance Criteria

- Eligible cases can be completed without a workflow worktree, plan, or archive.
- Context reading through `$m-docs` always happens before implementation eligibility is accepted.
- Ineligible cases are routed before the agent silently expands implementation.
- Stable behavior changes update canonical docs; behavior-restoring bug fixes do not create unnecessary docs churn.
- UI changes cannot pass without actual operation and screenshot evidence.
- The result table gives enough evidence that the user does not need to open a generated archive.
- The skill validates and syncs through repository tooling.

## Related Features

- [m-quick-fast-path.md](../features/m-quick-fast-path.md)
- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Specs

- [m-quick-skill.md](../specs/m-quick-skill.md)

## Related Changes

- To be added during archive.
