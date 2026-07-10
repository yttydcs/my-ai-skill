# m:autoflow Workflow Skill

## Background

This repository stores reusable Codex skills as Git-managed source packages. It needs a workflow family that enforces disciplined, auditable delivery while keeping phase-level commands short enough for daily use.

## Goal

Provide a reusable `m-autoflow` workflow collection with focused phase skills for discussion, planning, execution, testing, and archive, plus a guarded standalone fast path for bounded direct changes.

## Scope

### Must

- preserve `$m-autoflow` as the umbrella workflow entry point
- provide canonical phase entries named `$m-discuss`, `$m-plan`, `$m-execute`, `$m-test`, and `$m-archive`
- provide `$m-go` as a canonical high-automation execution entry after planning
- provide `$m-quick` as a canonical standalone direct-edit entry for explicit low-risk work in one repository
- keep the umbrella thin by routing to phase skills and shared references instead of duplicating phase instructions
- let `$m-discuss` own discovery, brainstorming, option comparison, requirement shaping, optional current-practice research, and early worktree setup
- let `$m-plan` own requirements consolidation, architecture design, execution planning, and approval gating
- require `$m-plan` to reject unreasonable, unsafe, contradictory, or under-specified requirements and return to discussion with alternatives
- require worktree-first staged execution before implementation, with worktree setup starting during discussion when project boundaries are clear
- require `plan.md` or `todo.md` in the active worktree before staged implementation
- require planning artifacts to explicitly separate tasks that will execute after approval from tasks that will not execute in the next execution phase, with a reason for every non-executed task
- require `$m-plan` to directly output a concise task summary table after creating or confirming the active plan
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
- require `$m-go` to keep plan gating, delegate all implementation edits to sub-agents, run safe parallel execution where write sets allow it, and automatically run `$m-test` after delegated execution
- require `$m-go` to delegate bounded fixes and repeat validation until all acceptance items pass or a blocker is explicit
- treat `$m-test` as optional heavy validation for integration, end-to-end flow, UI evidence, usability, security, and performance; allow the user to explicitly skip it and go to `$m-archive` when the reason and residual risk are recorded
- require `$m-test`, when run for UI-impacting changes, to open the affected UI, operate the affected path, and provide screenshot evidence
- require `$m-test` to directly output a concise pass/fail/blocked/skipped result table
- require `$m-quick` to use `$m-docs` for minimum relevant context before eligibility or direct edits
- require `$m-quick` to preserve existing changes, reject prohibited risk, run focused validation, and expose docs/gate/change/validation/risk results directly
- keep `$m-quick` outside the staged phase chain and forbid it from weakening normal worktree, plan, review, and archive gates

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
- The user wants a compact task summary in chat after planning without opening `plan.md` for the basic scope review.
- The user requires auditable sub-agent governance and a final `docs/change` archive.
- The user wants future troubleshooting to start from reusable lessons instead of re-reading old archives.
- The user wants private docs to be kept outside pushable code repositories while implementation happens in one or more code repos.
- The user wants a feature such as personnel management to be documented once as a complete feature dossier, even when several repos implement it.
- The user wants to run only discussion, planning, execution, testing, or archive without loading the full umbrella workflow.
- The user wants higher automation after planning, with implementation edits handled by sub-agents and testing run automatically.
- The user wants to fix an explicit bounded bug or small requirement directly in one repository without creating staged workflow artifacts, while still reading governed docs first.
- The user makes a small low-risk change where lightweight execution-stage validation is sufficient and heavyweight workflow testing should be skipped with a recorded reason.
- The user changes UI and expects visual validation evidence instead of code-only review.
- The user wants a compact test result summary in chat without opening markdown artifacts.
- The user explicitly chooses to skip `$m-test` and proceed directly to `$m-archive`.

## Functional Requirements

- `$m-autoflow` must route the user into the appropriate phase skills and shared references.
- `$m-autoflow` must expose `$m-quick` as a standalone alternate route rather than a staged phase.
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
- `$m-plan` must output a concise direct task summary table after creating or confirming the active plan.
- The `$m-plan` task table must include Task ID, title, scope, files/modules, acceptance/tests, and risk/notes.
- The `$m-plan` task table must summarize the active plan artifact and must not conflict with `plan.md` or `todo.md`.
- `$m-plan` must ask for clarification instead of assuming missing requirements.
- `$m-plan` must escalate uncertain best-practice choices instead of deciding silently.
- `$m-execute` must block if the active workflow lacks confirmed `plan.md` or `todo.md`.
- `$m-execute` must map every implementation change to a confirmed Task ID.
- `$m-execute` must report lightweight validation that passed, skipped checks with reasons, and any heavier validation still needed.
- `$m-go` must block if the active workflow lacks confirmed `plan.md` or `todo.md`.
- `$m-go` must map every delegated implementation change to a confirmed Task ID.
- `$m-go` must require worker sub-agents for implementation edits; the main agent may coordinate, inspect, run commands, review diffs, and accept results but must not directly edit implementation files.
- `$m-go` must assess Task ID and write-set parallelism, dispatch safe independent work in parallel when host policy and user authorization allow it, and serialize or block conflicting write sets.
- `$m-go` must automatically run `$m-test` behavior after delegated implementation completes.
- `$m-go` must return failed validation to delegated fixes and repeat the validation loop until acceptance passes or the blocker is explicit.
- `$m-go` must stop before `$m-archive`, merge, cleanup, or push.
- `$m-quick` must explicitly use `$m-docs` before it accepts eligibility or edits code.
- `$m-quick` must select one target Git repository, inspect current status, preserve existing work, and use a risk-based gate rather than a hard file or line limit.
- `$m-quick` must escalate conflicting docs, ambiguity, multi-repo work, architecture, public contracts, schema/migration, security, destructive data, production infrastructure, broad dependency changes, or broad validation needs.
- `$m-quick` must edit the selected current checkout directly only after its gate passes, without creating a quick-request worktree, plan, or archive by default.
- `$m-quick` must run focused validation and require actual UI operation plus screenshot evidence for UI-impacting quick changes.
- `$m-quick` must use `$m-docs` to update canonical stable docs only when stable truth changed, and must not create workflow history artifacts merely because it ran.
- `$m-quick` must output a compact direct result table and stop without automatic archive, merge, cleanup, push, publication, or deployment.
- `$m-test` must decide whether heavy validation is needed, record skip rationale when skipped, and review usability, security, and performance when it runs.
- `$m-test` must require actual UI opening, user-path operation, and screenshot evidence when it runs for UI-impacting changes.
- `$m-test` must treat missing UI evidence during a run `$m-test` as `不通过` or `阻塞`, not as a pass.
- `$m-test` must output a concise direct result table showing checks and pass/fail/blocked/skipped status.
- The workflow must allow the user to skip `$m-test` and invoke `$m-archive`, while preserving the skipped-testing reason and residual risk in archive records.
- `$m-archive` must record intake, feature, requirement, spec, decision, and lessons impact.
- `$m-archive` must capture searchable lesson cues when the workflow produced reusable debugging knowledge.
- `$m-archive` must treat normal archive invocation as a request to archive and end the workflow.
- `$m-archive` must stop after archive only when the user explicitly requests archive-only handling, no merge, no cleanup, or an equivalent pause.
- The workflow must not add docs remotes, push docs, or choose docs backup targets without explicit user instruction.
- The workflow must allow read-only parallel research lanes only from `$m-discuss` and only when host policy permits delegation.
- The workflow must keep implementation delegation gated by a confirmed plan, bounded Task IDs, complete context packages, and non-conflicting write sets.
- The workflow must treat `$m-go` invocation as explicit authorization to use worker sub-agents for the approved execution scope when host policy permits delegation.

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
- A plan may have only blocked or deferred tasks; the direct task table must not imply execution approval.
- Platform policy may forbid sub-agent use without explicit user authorization.
- Current external facts may be stale or conflicting; online research must mark uncertainty instead of treating unverified findings as stable truth.
- A lightweight execution check may be blocked by repo configuration; the workflow must record the reason and residual risk instead of hiding the gap.
- Heavy testing may be unnecessary for low-risk changes; the workflow must record why it was skipped.
- A quick request may lack matching docs; it may proceed only when local evidence keeps the work self-contained and unambiguous, and the missing context is reported.
- A quick request may encounter conflicting docs or ambiguous repo ownership; it must escalate before implementation expands.
- A quick request may reveal a prohibited risk after editing begins; it must stop broadening and report the partial state without overwriting user work.
- A UI cannot be opened due environment, auth, build, dependency, or runtime problems; if `$m-test` is running, the UI validation must be failed or blocked.
- UI responsive behavior may require both desktop and mobile screenshot evidence when affected.
- Direct `$m-plan` invocation may skip discussion only when the plan records why discussion was unnecessary or already satisfied.

## Acceptance Criteria

- `m-autoflow` exists as a valid umbrella skill package in this repository.
- `m-discuss`, `m-plan`, `m-execute`, `m-go`, `m-quick`, `m-test`, and `m-archive` exist as valid companion skill packages in this repository.
- The umbrella skill routes to the phase skills without removing the `$m-autoflow` entry point.
- The phase skills enforce discussion, planning, execution, testing, archive, and blocker rules.
- The plan artifact clearly states which Task IDs will execute after approval and which Task IDs will not execute in the next execution phase.
- `$m-plan` responses include a concise direct task summary table.
- Optional online research is controlled by discussion, supports source verification and citations, and routes stable-doc impact through `$m-docs`.
- Lightweight validation is part of execution, while heavyweight integration/UI/usability/security/performance testing is optional and separately recorded.
- `$m-go` performs delegated implementation and automatic `$m-test` looping for confirmed plans without making the main agent the implementer.
- `$m-quick` restores governed docs context, correctly gates low-risk direct work, validates the affected behavior, and escalates prohibited requests without weakening staged commands.
- UI-impacting changes tested by `$m-test` produce actual operation evidence and screenshot paths.
- `$m-test` output includes a concise direct result table.
- The archive can route reusable lessons into `docs/lessons` for later lookup.
- Planning and archive respect private docs roots and do not publish docs without the user's explicit instruction.
- All canonical skills validate and sync successfully.

## Related Features

- [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)
- [../features/m-quick-fast-path.md](../features/m-quick-fast-path.md)

## Related Specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)
- [../specs/m-quick-skill.md](../specs/m-quick-skill.md)

## Related Decisions

- [../decisions/2026-07-08_m-skill-phase-naming.md](../decisions/2026-07-08_m-skill-phase-naming.md)
- [../decisions/2026-07-09_m-go-automated-execution.md](../decisions/2026-07-09_m-go-automated-execution.md)
- [../decisions/2026-07-10_m-quick-standalone-fast-path.md](../decisions/2026-07-10_m-quick-standalone-fast-path.md)

## Related Changes

- [../change/2026-07-08_m-plan-task-table.md](../change/2026-07-08_m-plan-task-table.md)
- [../change/2026-07-08_m-test-ui-evidence.md](../change/2026-07-08_m-test-ui-evidence.md)
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
