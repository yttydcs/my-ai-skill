# m:autoflow Workflow Skill

## Background

This repository stores reusable Codex skills as Git-managed source packages. It needs a workflow family that enforces disciplined, auditable delivery while keeping phase-level commands short enough for daily use.

## Goal

Provide a reusable `m-autoflow` workflow collection with focused phase skills for discussion, planning, execution, testing, and archive.

## Scope

### Must

- preserve `$m-autoflow` as the umbrella workflow entry point
- provide canonical phase entries named `$m-discuss`, `$m-plan`, `$m-execute`, `$m-test`, and `$m-archive`
- keep the umbrella thin by routing to phase skills and shared references instead of duplicating phase instructions
- let `$m-discuss` own discovery, brainstorming, option comparison, requirement shaping, optional current-practice research, and early worktree setup
- let `$m-plan` own requirements consolidation, architecture design, execution planning, and approval gating
- require `$m-plan` to reject unreasonable, unsafe, contradictory, or under-specified requirements and return to discussion with alternatives
- require worktree-first execution before implementation, with worktree setup starting during discussion when project boundaries are clear
- require `plan.md` or `todo.md` in the active worktree before implementation
- require planning artifacts to explicitly separate tasks that will execute after approval from tasks that will not execute in the next execution phase, with a reason for every non-executed task
- require explicit blocker handling with `问题清单` and `阻塞：是`
- require rollback reason recording and document synchronization
- require no silent assumptions about business, data, interface, environment, dependency version, acceptance, or preference
- require explicit `$m-docs` usage when planning or archive changes governed docs
- require planning and archive phases to identify the private `docs_root` when governed docs should not live in code repositories
- require behavior-changing workflows to check affected intake, feature, requirement, spec, and decision docs before implementation
- require multi-repo capabilities to record project root, docs root, code repos, and active worktrees separately
- require docs remote, push, and backup decisions to remain user-owned
- require archive to extract reusable experience / lessons and record searchable lookup hints
- require archive to either update `docs/lessons` or record why `Lessons impact: none`
- require mandatory review decision and `docs/change` archive before workflow completion
- require controlled sub-agent usage only in allowed phases
- keep execution responsible for implementation plus lightweight local validation such as syntax checks, type checks, focused lint, touched-file formatting checks, focused unit tests, and `git diff --check`
- treat `$m-test` as optional heavy validation for integration, end-to-end flow, usability, security, and performance; allow skipping it for low-risk small changes when the reason and residual risk are recorded

### Optional

- reuse the repository's generic validation and copy-sync tooling
- keep repository-level requirements and specs so future workflows can record impact cleanly
- add temporary compatibility aliases in a later change if the user explicitly accepts the extra maintenance cost

### Out of Scope

- changing external project runtime logic
- relaxing the user's stage gates or blocker rules
- duplicating `m-docs` as a separate implementation inside this skill family
- adding docs remotes, pushing docs, or choosing backup targets

## Scenarios

- The user wants a strict implementation workflow rather than a direct code patch.
- The user wants an early discussion phase that researches current best practices only when that would improve the requirement.
- The user requires git worktree isolation before coding.
- The user requires handoff-ready `plan.md` artifacts before any coding or delegation.
- The user requires auditable sub-agent governance and a final `docs/change` archive.
- The user wants future troubleshooting to start from reusable lessons instead of re-reading old archives.
- The user wants private docs to be kept outside pushable code repositories while implementation happens in one or more code repos.
- The user wants a feature such as personnel management to be documented once as a complete feature dossier, even when several repos implement it.
- The user wants to run only discussion, planning, execution, testing, or archive without loading the full umbrella workflow.
- The user makes a small low-risk change where lightweight execution-stage validation is sufficient and heavyweight workflow testing should be skipped with a recorded reason.

## Functional Requirements

- `$m-autoflow` must route the user into the appropriate phase skills and shared references.
- `$m-autoflow` must not duplicate full phase instructions that already belong to a phase skill.
- `$m-discuss` must check project, docs, code-repo, and worktree boundaries when those affect the workflow.
- `$m-discuss` must use web research only when current external facts, best practices, source-backed comparison, or the user's explicit request make research useful.
- `$m-discuss` must verify and cite external research before feeding it into requirements, planning, or stable docs.
- `$m-discuss` must produce a handoff-ready brief covering goal, scope, assumptions, open questions, options considered, rejected options, recommended direction, and worktree/docs-root status.
- `$m-plan` must consume the discussion brief when it exists.
- `$m-plan` must check for `guide.md` before planning when the file exists.
- `$m-plan` must read relevant intake, feature, requirement, spec, and decision docs before changing stable workflow truth.
- `$m-plan` must prefer private-docs-root stable docs when the user has separated docs from code repos.
- `$m-plan` must emit requirements analysis and architecture design before the executable plan.
- `$m-plan` must create or confirm root-level `plan.md` or `todo.md` in the active worktree.
- `$m-plan` must place every known Task ID in exactly one execution-scope group: tasks to execute after approval, or tasks not to execute now with the blocking, deferral, out-of-scope, research-only, or separate-approval reason.
- `$m-plan` must ask for clarification instead of assuming missing requirements.
- `$m-plan` must escalate uncertain best-practice choices instead of deciding silently.
- `$m-execute` must block if the active workflow lacks confirmed `plan.md` or `todo.md`.
- `$m-execute` must map every implementation change to a confirmed Task ID.
- `$m-execute` must report lightweight validation that passed, skipped checks with reasons, and any heavier validation still needed.
- `$m-test` must decide whether heavy validation is needed, record skip rationale when skipped, and review usability, security, and performance when it runs.
- `$m-archive` must record intake, feature, requirement, spec, decision, and lessons impact.
- `$m-archive` must capture searchable lesson cues when the workflow produced reusable debugging knowledge.
- `$m-archive` must treat normal archive invocation as a request to archive and end the workflow.
- `$m-archive` must stop after archive only when the user explicitly requests archive-only handling, no merge, no cleanup, or an equivalent pause.
- The workflow must not add docs remotes, push docs, or choose docs backup targets without explicit user instruction.
- The workflow must allow read-only parallel research lanes only from `$m-discuss` and only when host policy permits delegation.
- The workflow must keep implementation delegation gated by a confirmed plan, bounded Task IDs, complete context packages, and non-conflicting write sets.

## Non-functional Requirements

- Performance:
  - keep each `SKILL.md` concise and load details from references only when needed
- Readability:
  - use short phase names and explicit blocker wording
- Extensibility:
  - keep `m-docs` integration explicit instead of copying its full rule set
- Maintainability:
  - keep install output disposable and Git source authoritative
  - keep historical change archives append-only even when current names change

## Edge Cases

- `guide.md` may be absent.
- The repository docs tree may be incomplete.
- A private docs root may be separate from every participating code repo.
- A code repo may contain a `docs/` directory that is not canonical for the project.
- A capability may span several repos while one private feature doc remains the source of truth.
- A stale `plan.md` from another workflow may exist and need replacement.
- Platform policy may forbid sub-agent use without explicit user authorization.
- Current external facts may be stale or conflicting; online research must mark uncertainty instead of treating unverified findings as stable truth.
- A lightweight execution check may be blocked by repo configuration; the workflow must record the reason and residual risk instead of hiding the gap.
- Heavy testing may be unnecessary for low-risk changes; the workflow must record why it was skipped.
- Direct `$m-plan` invocation may skip discussion only when the plan records why discussion was unnecessary or already satisfied.

## Acceptance Criteria

- `m-autoflow` exists as a valid umbrella skill package in this repository.
- `m-discuss`, `m-plan`, `m-execute`, `m-test`, and `m-archive` exist as valid companion skill packages in this repository.
- The umbrella skill routes to the phase skills without removing the `$m-autoflow` entry point.
- The phase skills enforce discussion, planning, execution, testing, archive, and blocker rules.
- The plan artifact clearly states which Task IDs will execute after approval and which Task IDs will not execute in the next execution phase.
- Optional online research is controlled by discussion, supports source verification and citations, and routes stable-doc impact through `$m-docs`.
- Lightweight validation is part of execution, while heavyweight integration/usability/security/performance testing is optional and separately recorded.
- The archive can route reusable lessons into `docs/lessons` for later lookup.
- Planning and archive respect private docs roots and do not publish docs without the user's explicit instruction.
- All canonical skills validate and sync successfully.

## Related Features

- [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related Decisions

- [../decisions/2026-07-08_m-skill-phase-naming.md](../decisions/2026-07-08_m-skill-phase-naming.md)

## Related Changes

- [../change/2026-07-08_m-archive-default-closeout.md](../change/2026-07-08_m-archive-default-closeout.md)
- [../change/2026-07-08_m-skill-phase-rename.md](../change/2026-07-08_m-skill-phase-rename.md)
- [../change/2026-03-23_rigorous-execution-skill.md](../change/2026-03-23_rigorous-execution-skill.md)
- [../change/2026-03-23_rigorous-execution-alignment.md](../change/2026-03-23_rigorous-execution-alignment.md)
- [../change/2026-03-23_rigorous-execution-doc-priority.md](../change/2026-03-23_rigorous-execution-doc-priority.md)
- [../change/2026-03-23_rigorous-execution-invocation-policy.md](../change/2026-03-23_rigorous-execution-invocation-policy.md)
- [../change/2026-03-23_lessons-archive-lookup.md](../change/2026-03-23_lessons-archive-lookup.md)
- [../change/2026-03-24_skill-prefix-rename.md](../change/2026-03-24_skill-prefix-rename.md)
- [../change/2026-06-22_autoflow-phase-split-research.md](../change/2026-06-22_autoflow-phase-split-research.md)
- [../change/2026-06-23_autoflow-plan-execution-scope.md](../change/2026-06-23_autoflow-plan-execution-scope.md)
