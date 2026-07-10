# 2026-07-10 m-quick Fast Path

## Source

- Date: 2026-07-10
- Source: Codex chat
- Requester: User

## Request Text / Source-preserving Summary

The existing `m-*` workflow is too heavy for small, uncontroversial requirements and minor bugs. Add a command that can modify code directly inside repositories under the project's repo area while minimizing redundant workflow steps.

The command must still use `$m-docs` to read relevant project documentation before changing code so that feature context, durable boundaries, technical constraints, decisions, and previous lessons are not lost.

## Context

- The full workflow remains appropriate for ambiguous, architectural, cross-repo, or high-risk work.
- The fast path should avoid mandatory worktree creation, planning artifacts, archive records, and sub-agent coordination.
- UI-impacting changes still require actual operation and screenshot evidence.
- Docs reading is mandatory; stable-doc writing is required only when current truth changes.

## Confirmed Requirements

- Canonical command name: `$m-quick`.
- Explicit invocation authorizes direct editing only after a low-risk eligibility gate passes.
- Operate on one selected Git repository's current checkout.
- Use `$m-docs` before deciding eligibility or editing.
- Preserve existing user changes and run focused validation.
- Escalate unsuitable work to `$m-discuss` or `$m-plan`.
- Do not create workflow history artifacts, commit, or push by default.

## Open Questions

- None at planning completion.

## Routed Docs

- [Feature dossier](../features/m-quick-fast-path.md)
- [Durable requirements](../requirements/m-quick-fast-path.md)
- [Technical specification](../specs/m-quick-skill.md)
- [Architecture decision](../decisions/2026-07-10_m-quick-standalone-fast-path.md)

## Related Changes

- To be added during `$m-archive` after implementation and validation.
