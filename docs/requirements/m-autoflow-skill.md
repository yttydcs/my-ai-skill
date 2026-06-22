# m:autoflow Skill

## Background

This repository stores reusable Codex skills as Git-managed source packages. It needs a workflow skill named `m-autoflow` that enforces disciplined delivery instead of allowing direct ad hoc coding.

## Goal

Provide a reusable skill that drives a staged, auditable engineering workflow from initialization through archive.

## Scope

### Must

- support explicit invocation via `$m-autoflow` when deterministic routing is needed
- require worktree-first initialization
- require stage order from requirements through archive
- require only one active stage at a time
- require stage `1` to prioritize `docs/requirements` when relevant stable docs exist
- require `plan.md` or `todo.md` in the active worktree before implementation
- require explicit blocker handling with `问题清单` and `阻塞：是`
- require rollback reason recording and document synchronization
- require no silent assumptions about business, data, interface, environment, dependency version, acceptance, or preference
- require explicit `$m-docs` usage in stages `3.1` and `4`
- require stage `4` to extract reusable experience / lessons and record searchable lookup hints
- require stage `4` to either update `docs/lessons` or record why `Lessons impact: none`
- require mandatory review and `docs/change` archive before completion
- require controlled sub-agent usage only in allowed phases
- preserve `$m-autoflow` as the umbrella workflow entry while allowing split-phase companion skills for research, planning, execution, testing, and archive
- support an optional online research phase only when the user explicitly asks for web search, online investigation, latest/current external information, or source-backed research
- require online research findings to be verified, cited, and routed through `$m-docs` when they change stable requirements or specs
- keep execution responsible for implementation plus lightweight local validation such as syntax checks, type checks, focused lint, touched-file formatting checks, focused unit tests, and `git diff --check`
- treat the test/review phase as optional heavy validation for integration, end-to-end flow, usability, security, and performance; allow skipping it for low-risk small changes when the reason and residual risk are recorded

### Optional

- reuse the repository's generic validation and copy-sync tooling
- keep repository-level requirements and specs so future workflows can record impact cleanly

### Out of Scope

- changing external project runtime logic
- relaxing the user's stage gates or blocker rules
- duplicating `m-docs` as a separate implementation inside this skill

## Scenarios

- The user asks for a strict implementation workflow rather than a direct code patch.
- The user requires git worktree isolation before coding.
- The user requires handoff-ready `plan.md` artifacts before any coding or delegation.
- The user requires auditable sub-agent governance and a final `docs/change` archive.
- The user wants future troubleshooting to start from reusable lessons instead of re-reading old archives.
- The user wants to run only planning, execution, testing, archive, or research without loading the full umbrella workflow.
- The user explicitly asks for online research before planning and expects current, cited external evidence.
- The user makes a small low-risk change where lightweight execution-stage validation is sufficient and heavyweight workflow testing should be skipped with a recorded reason.

## Functional Requirements

- The skill must check for `guide.md` before stage `1` when the file exists.
- The skill must block if the dedicated worktree is missing.
- The skill must block if the active workflow lacks `plan.md` or `todo.md` before `3.2`.
- The skill must read relevant requirement docs first in stage `1` when `docs/requirements` exists.
- The skill must emit stage outputs for requirements analysis and architecture design before planning.
- The skill must ask for clarification instead of assuming missing requirements.
- The skill must escalate uncertain best-practice choices instead of deciding silently.
- The skill must record `Lessons impact` and `Related lessons` in the stage `4` archive.
- The skill must capture searchable lesson cues when the workflow produced reusable debugging knowledge.
- The skill must ask whether the workflow should end after stage `4`.
- The skill must not perform web research during ordinary planning unless the user explicitly requests it.
- The skill must allow read-only parallel research sub-agents only for explicitly requested online research and only when host policy permits delegation.
- The main agent must review research sources, reconcile conflicting claims, and cite links before using research findings in planning artifacts.
- The skill must keep implementation sub-agent delegation gated by a confirmed plan, bounded Task IDs, complete context packages, and non-conflicting write sets.
- The execute phase must report lightweight validation that passed, skipped checks with reasons, and any heavier validation still needed.
- The test phase must decide whether heavy validation is needed, record skip rationale when skipped, and review usability, security, and performance when it runs.

## Non-functional Requirements

- Performance:
  - keep the skill body concise and load details from references only when needed
- Readability:
  - use the user's stage names and explicit blocker wording
- Extensibility:
  - keep m-docs integration explicit instead of copying its full rule set
- Maintainability:
  - keep install output disposable and Git source authoritative

## Edge Cases

- `guide.md` may be absent.
- The repository docs tree may be incomplete.
- A stale `plan.md` from another workflow may exist and need replacement.
- Platform policy may forbid sub-agent use without explicit user authorization.
- Current external facts may be stale or conflicting; online research must mark uncertainty instead of treating unverified findings as stable truth.
- A lightweight execution check may be blocked by repo configuration; the workflow must record the reason and residual risk instead of hiding the gap.
- Heavy testing may be unnecessary for low-risk changes; the workflow must record why it was skipped.

## Acceptance Criteria

- `m-autoflow` exists as a valid skill package in this repository.
- `m-autoflow-plan`, `m-autoflow-execute`, `m-autoflow-test`, `m-autoflow-archive`, and `m-autoflow-research` exist as valid companion skill packages in this repository.
- The skill enforces the user's staged workflow and blocker rules.
- The umbrella skill routes to the companion skills without removing the original `$m-autoflow` entry point.
- The skill integrates with `m-docs` and repository copy-sync tooling.
- Optional online research is explicit-request-only, supports read-only parallel research lanes, and requires source verification and citations.
- Lightweight validation is part of execution, while heavyweight integration/usability/security/performance testing is optional and separately recorded.
- The stage `4` archive can route reusable lessons into `docs/lessons` for later lookup.
- The skill validates and syncs successfully.

## Related Specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related Changes

- [../change/2026-03-23_rigorous-execution-skill.md](../change/2026-03-23_rigorous-execution-skill.md)
- [../change/2026-03-23_rigorous-execution-alignment.md](../change/2026-03-23_rigorous-execution-alignment.md)
- [../change/2026-03-23_rigorous-execution-doc-priority.md](../change/2026-03-23_rigorous-execution-doc-priority.md)
- [../change/2026-03-23_rigorous-execution-invocation-policy.md](../change/2026-03-23_rigorous-execution-invocation-policy.md)
- [../change/2026-03-23_lessons-archive-lookup.md](../change/2026-03-23_lessons-archive-lookup.md)
- [../change/2026-03-24_skill-prefix-rename.md](../change/2026-03-24_skill-prefix-rename.md)
- [../change/2026-06-22_autoflow-phase-split-research.md](../change/2026-06-22_autoflow-phase-split-research.md)
