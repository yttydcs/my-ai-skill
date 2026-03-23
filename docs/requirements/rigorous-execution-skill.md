# Rigorous Execution Skill

## Background

This repository stores reusable Codex skills as Git-managed source packages. It needs a workflow skill that enforces disciplined delivery instead of allowing direct ad hoc coding.

## Goal

Provide a reusable skill that drives a staged, auditable engineering workflow from initialization through archive.

## Scope

### Must

- require explicit manual invocation via `$rigorous-execution`
- require worktree-first initialization
- require stage order from requirements through archive
- require only one active stage at a time
- require stage `1` to prioritize `docs/requirements` when relevant stable docs exist
- require `plan.md` or `todo.md` in the active worktree before implementation
- require explicit blocker handling with `问题清单` and `阻塞：是`
- require rollback reason recording and document synchronization
- require no silent assumptions about business, data, interface, environment, dependency version, acceptance, or preference
- require explicit `$docs-governor` usage in stages `3.1` and `4`
- require mandatory review and `docs/change` archive before completion
- require controlled sub-agent usage only in allowed phases

### Optional

- reuse the repository's generic validation and copy-sync tooling
- keep repository-level requirements and specs so future workflows can record impact cleanly

### Out of Scope

- changing external project runtime logic
- relaxing the user's stage gates or blocker rules
- duplicating `docs-governor` as a separate implementation inside this skill

## Scenarios

- The user asks for a strict implementation workflow rather than a direct code patch.
- The user requires git worktree isolation before coding.
- The user requires handoff-ready `plan.md` artifacts before any coding or delegation.
- The user requires auditable sub-agent governance and a final `docs/change` archive.

## Functional Requirements

- The skill must check for `guide.md` before stage `1` when the file exists.
- The skill must block if the dedicated worktree is missing.
- The skill must block if the active workflow lacks `plan.md` or `todo.md` before `3.2`.
- The skill must read relevant requirement docs first in stage `1` when `docs/requirements` exists.
- The skill must emit stage outputs for requirements analysis and architecture design before planning.
- The skill must ask for clarification instead of assuming missing requirements.
- The skill must escalate uncertain best-practice choices instead of deciding silently.
- The skill must ask whether the workflow should end after stage `4`.

## Non-functional Requirements

- Performance:
  - keep the skill body concise and load details from references only when needed
- Readability:
  - use the user's stage names and explicit blocker wording
- Extensibility:
  - keep docs-governor integration explicit instead of copying its full rule set
- Maintainability:
  - keep install output disposable and Git source authoritative

## Edge Cases

- `guide.md` may be absent.
- The repository docs tree may be incomplete.
- A stale `plan.md` from another workflow may exist and need replacement.
- Platform policy may forbid sub-agent use without explicit user authorization.

## Acceptance Criteria

- `rigorous-execution` exists as a valid skill package in this repository.
- The skill enforces the user's staged workflow and blocker rules.
- The skill integrates with `docs-governor` and repository copy-sync tooling.
- The skill validates and syncs successfully.

## Related Specs

- [../specs/rigorous-execution-skill.md](../specs/rigorous-execution-skill.md)

## Related Changes

- [../change/2026-03-23_rigorous-execution-skill.md](../change/2026-03-23_rigorous-execution-skill.md)
- [../change/2026-03-23_rigorous-execution-alignment.md](../change/2026-03-23_rigorous-execution-alignment.md)
- [../change/2026-03-23_rigorous-execution-doc-priority.md](../change/2026-03-23_rigorous-execution-doc-priority.md)
