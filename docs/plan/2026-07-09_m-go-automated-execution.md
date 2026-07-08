# Plan - m-go automated execution skill

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `feat/m-go-automation`
- Base: `main`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\docs`
- Code Repos: `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\m-go-automation`
- Current Stage: `3.1 - Planning`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-go-automation\plan.md`

## Stage Records

### Initialization

- `guide.md`: present. Rule: every modification round must be committed with an English commit message following prior style.
- Project/docs/code repo confirmation:
  - `project_root` is the umbrella repository `D:\project\my-ai-skills`.
  - `docs_root` is `D:\project\my-ai-skills\docs`.
  - `code_repos` is the same repository because this change updates reusable skill source packages.
  - The docs root is inside this skill-source repo for this project and is currently the selected governed docs root.
- Base/worktree confirmation:
  - Base branch is `main`.
  - Dedicated branch is `feat/m-go-automation`.
  - Dedicated worktree is `D:\project\my-ai-skills\worktrees\m-go-automation`.
  - Implementation must happen in the dedicated worktree, not in the control-plane checkout.

### Discuss - Discovery And Requirements Shaping

#### Goal

Add a new `$m-go` / `m:go` command to the `m-*` workflow family. It is similar to `$m-execute`, but it is a higher-automation executor: the main agent coordinates, audits, and accepts results, while implementation edits are made only by sub-agents. It should run safe parallel execution when task write sets allow it, then automatically run `$m-test` style heavy validation until acceptance is satisfied or a real blocker is reached.

#### Scope

Must:

- Add a canonical `$m-go` skill package.
- Keep `$m-go` gated by a confirmed `plan.md` or `todo.md`.
- Require all implementation file edits during `$m-go` to be done by worker sub-agents.
- Allow the main agent to perform orchestration, context packaging, conflict assessment, result review, command execution, validation synthesis, and final acceptance.
- Require safe parallel worker dispatch for independently acceptable Task IDs with non-conflicting write sets.
- Automatically enter `$m-test` behavior after `$m-go` implementation completes.
- If `$m-test` fails, return to delegated worker fixes and repeat until all acceptance checks pass or a blocker is explicit.
- Keep `$m-execute` as the lighter manual execution phase.
- Update stable docs, umbrella routing, governance references, validation, and local installed skill copies.

Optional:

- Improve shared templates only where needed to support `$m-go` context packages or result summaries.

Out of scope:

- Replacing `$m-execute`.
- Allowing `$m-go` to bypass `$m-plan`.
- Letting `$m-go` perform archive, merge, push, or worktree cleanup.
- Adding compatibility aliases beyond the canonical `$m-go`.
- Changing docs remotes, backup destinations, or publication behavior.

#### Assumptions

- Host sub-agent tools are available when `$m-go` runs.
- Host policy allows sub-agent delegation when the user explicitly invokes `$m-go`.
- `$m-go` can use worker sub-agents for code/docs edits and can use validation/review sub-agents only where write sets and contexts are bounded.
- The main agent may read files, run commands, review diffs, summarize results, and decide acceptance, but must not directly edit implementation files during `$m-go`.
- Plan/status updates required during `$m-go` should be delegated to a worker unless they are external status reports in chat.

#### Open Questions

- None blocking for planning.

#### Options Considered

- Extend `$m-execute` with a strict sub-agent mode.
  - Rejected because it would make the existing lightweight/manual execution entry harder to reason about.
- Add `$m-go` as an alias of `$m-execute`.
  - Rejected because `$m-go` has stronger automation, mandatory delegation, and automatic test-loop semantics.
- Add `$m-go` as a canonical companion entry point in the `m-*` family.
  - Accepted because it preserves `$m-execute` while adding a clear high-automation path.

#### Rejected Options

- Allow `$m-go` without a confirmed plan.
  - Rejected because it would weaken workflow gating and sub-agent governance.
- Let the main agent directly fix small failures during `$m-go`.
  - Rejected because it contradicts the user requirement that implementation edits go through sub-agents.
- Automatically archive from `$m-go`.
  - Rejected for this change because `$m-go` is an execution/test loop, while `$m-archive` owns closeout.

#### Recommended Direction

Create `$m-go` as a new strict automation skill that composes the existing execution, sub-agent, and test rules. It should be documented as an alternate execution entry after `$m-plan`, not as a new discovery or archive phase.

#### Research Summary

- No web research used. This is an internal workflow design based on the existing local skill contracts and current host sub-agent capability.

#### Worktree / Branch / Docs Root Status

- Worktree exists and is clean at planning start.
- Branch exists: `feat/m-go-automation`.
- Docs root exists with current `intake`, `features`, `requirements`, `specs`, `decisions`, `plan`, `change`, and `lessons` categories.

#### Issue List

- No planning blocker.
- Execution remains blocked until the user approves this plan.

### Plan - Requirements And Architecture

#### Discussion Summary

The user wants a higher-automation command named `$m-go`. Its defining rule is that the main agent does not implement. Worker sub-agents perform all modifications, the main agent schedules and audits, parallelizable execution should run in parallel, and `$m-test` should run automatically after all execution tasks complete. Failures should loop back into delegated fixes until acceptance is reached or an explicit blocker is reported.

#### Accepted / Rejected Requirements

Accepted:

- `$m-go` is a separate canonical skill package.
- `$m-go` requires an approved active plan.
- `$m-go` requires delegated implementation edits.
- `$m-go` performs parallelism assessment and dispatches parallel workers when safe.
- `$m-go` automatically runs `$m-test` behavior.
- `$m-go` loops worker fixes and tests until acceptance passes or a blocker is clear.
- `$m-go` must be included in umbrella routing, stable docs, specs, manifests, validation, and sync.

Rejected:

- Direct main-agent implementation in `$m-go`.
- Skipping plan gating.
- Folding `$m-go` into `$m-execute` as a hidden mode.
- Making `$m-go` responsible for archive/merge/cleanup.

#### Requirements Analysis

##### Goal

Add a reusable command that makes the `m-*` workflow more automated after planning while retaining auditability and phase boundaries.

##### Scope

This change touches only the `my-ai-skills` skill source repo and local installed skill copies. It does not change external application runtime logic.

##### Use Cases

- The user has an approved `plan.md` with several independent Task IDs and wants Codex to execute with minimal supervision.
- A plan contains multiple non-conflicting write sets that should be handled in parallel by worker sub-agents.
- A feature requires automatic implementation followed by heavy validation without manually invoking `$m-test`.
- A test failure needs a delegated repair loop rather than a direct main-agent patch.

##### Functional Requirements

- `skills/m-go/SKILL.md` exists with valid skill frontmatter and concise routing.
- `skills/m-go/references/go.md` defines entry gates, mandatory delegation, parallel dispatch, worker context package, integration audit, automatic `$m-test`, failure loop, and exit gate.
- `skills/m-go/agents/openai.yaml` exposes `m:go`.
- `manifests/m-go.json` defines copy install metadata and dependencies.
- `skills/m-autoflow/SKILL.md` routes to `$m-go` as the high-automation execution/test-loop entry.
- `skills/m-autoflow/references/stages.md` explains where `$m-go` fits without changing the default phase order.
- `skills/m-autoflow/references/subagents.md` distinguishes normal optional delegation from `$m-go` mandatory implementation delegation.
- Stable docs record `$m-go` as current behavior, durable requirement, and technical contract.
- Validation and sync cover `$m-go` and every affected existing skill.

##### Non-functional Requirements

- Keep `SKILL.md` frontmatter short and YAML-safe.
- Keep `$m-go` instructions concise and put detailed rules in `references/go.md`.
- Avoid duplicating the full `$m-test`, `$m-execute`, or `$m-docs` rules inside `$m-go`; reference them.
- Preserve clear phase boundaries and explicit blockers.
- Keep docs and skill source changes minimal and consistent with existing file style.

##### Inputs / Outputs

Inputs:

- Approved active `plan.md` or `todo.md`.
- Confirmed Task IDs, write sets, acceptance criteria, tests, rollback notes.
- Current host sub-agent availability and user authorization through `$m-go` invocation.

Outputs:

- New installed and source `$m-go` skill.
- Updated umbrella and governance references.
- Updated stable docs and indexes.
- Validation/sync results.
- A later `$m-test` result table when `$m-go` is actually invoked in future workflows.

##### Edge Cases

- Only one Task ID exists: `$m-go` still delegates to one worker because main-agent implementation is forbidden.
- Tasks have overlapping write sets: `$m-go` serializes worker dispatch or blocks with a conflict explanation.
- A worker fails or drifts from scope: main agent rejects the result and sends a corrected delegated task.
- Integration requires edits after worker completion: main agent delegates integration edits to a worker with a bounded write set.
- `$m-test` fails: main agent returns to delegated repair and repeats validation.
- Host sub-agent tooling is unavailable: `$m-go` blocks rather than falling back to main-agent implementation.
- User explicitly wants no heavy test: that conflicts with normal `$m-go` semantics and should be routed to `$m-execute` plus explicit `$m-test` skip handling instead.

##### Acceptance Criteria

- `$m-go` is a valid skill package and is installed locally.
- `$m-autoflow` recognizes `$m-go` as a high-automation entry.
- Stable docs mention `$m-go` in feature, requirement, and spec docs.
- Sub-agent governance explicitly covers `$m-go`.
- `$m-go` rules state that main-agent implementation edits are forbidden.
- `$m-go` rules require automatic `$m-test` after delegated execution.
- `$m-go` rules require looping delegated fixes until tests pass or blocking issues are explicit.
- Validation passes:
  - `tools\validate-skills.ps1 -Skill m-go`
  - `tools\validate-skills.ps1 -Skill m-autoflow`
  - `tools\validate-skills.ps1 -Skill m-execute`
  - `tools\validate-skills.ps1 -Skill m-test`
  - `git diff --check`
- Sync succeeds:
  - `tools\sync-skills.ps1 -Skill m-go`
  - `tools\sync-skills.ps1 -Skill m-autoflow`

##### Risks

- Over-broad `$m-go` wording could weaken plan gating.
- Ambiguous "main agent does not implement" wording could accidentally forbid review or command execution; the rule must distinguish edits from orchestration.
- Auto-test loop could become infinite; `$m-go` must define blocker conditions and iteration reporting.
- Frontmatter validation can fail if long descriptions contain YAML-sensitive punctuation.
- Sync modifies local installed skills outside the repo, so final reporting must mention source and installed copies.

#### Architecture Design

##### Overall Solution

Add `$m-go` as a companion skill package under `skills/m-go`. Keep `SKILL.md` as a short router and put operational semantics in `references/go.md`. Update `m-autoflow` shared references so the new command is discoverable, staged, and governed by the existing plan, sub-agent, test, docs, and archive model.

##### Alternatives Considered

- Modify `$m-execute` only:
  - Lower file count but blends two execution modes and raises accidental behavior risk.
- Add `$m-go` as a thin wrapper around `$m-execute`:
  - Not enough because `$m-go` changes delegation and testing semantics.
- Add `$m-go` as a first-class skill with shared-reference reuse:
  - Chosen because it is explicit, testable, and consistent with phase skills.

##### Module Responsibilities

- `skills/m-go/SKILL.md`: entry point, quick start, entry gate, workflow, exit gate.
- `skills/m-go/references/go.md`: detailed automation, delegation, integration, automatic test-loop, failure handling, and reporting rules.
- `skills/m-go/agents/openai.yaml`: UI metadata.
- `manifests/m-go.json`: install/sync metadata.
- `skills/m-autoflow/SKILL.md`: umbrella entry point list and routing.
- `skills/m-autoflow/references/stages.md`: stage mapping and default workflow treatment.
- `skills/m-autoflow/references/subagents.md`: `$m-go` mandatory delegation and main-agent non-editing rules.
- `skills/m-autoflow/references/templates.md`: add optional compact `$m-go` summary or worker result cues only if needed.
- `manifests/m-autoflow.json`: dependency update to include `m-go`.
- `docs/features/m-autoflow-workflow.md`: current user-visible behavior.
- `docs/requirements/m-autoflow-skill.md`: durable requirements and acceptance.
- `docs/specs/m-autoflow-skill.md`: package, trigger, workflow, sub-agent, validation contracts.
- `docs/decisions/2026-07-09_m-go-automated-execution.md`: decision record for the new command.
- `docs/intake/2026-07-09_m-go-automated-execution.md`: original request evidence.
- Category `README.md` files: index new intake and decision docs if created.

##### Data / Call Flow

Future `$m-go` runtime flow:

1. User invokes `$m-go` after `$m-plan`.
2. Main agent reads `$m-go`, active plan, and sub-agent/test references.
3. Main agent validates entry gates and identifies Task IDs/write sets.
4. Main agent dispatches worker sub-agents for every executable implementation task.
5. Workers edit files only inside assigned write sets and report results.
6. Main agent reviews worker output and diffs, resolves coordination by delegated follow-up workers if needed.
7. Main agent runs lightweight validation and then invokes `$m-test` behavior automatically.
8. If `$m-test` fails, main agent delegates bounded fixes and repeats validation.
9. When all acceptance checks pass, main agent reports a concise result table and says workflow may proceed to `$m-archive`.

##### Interface Drafts

Skill frontmatter:

```md
---
name: m-go
description: Automated delegated execution and test loop for confirmed m-autoflow plans.
---
```

Agent metadata:

```yaml
interface:
  display_name: "m:go"
  short_description: "Run delegated execution and testing"
  default_prompt: "Use $m-go to execute approved plan tasks with worker sub-agents and automatic testing."
```

Manifest shape:

```json
{
  "name": "m-go",
  "version": "0.1.0",
  "install_mode": "copy",
  "source_dir": "skills/m-go",
  "dist_dir": "dist/codex/m-go",
  "codex_install_root": "%USERPROFILE%/.codex/skills",
  "depends_on_skills": ["m-autoflow", "m-test"],
  "reference_files": ["references/go.md"]
}
```

##### Error Handling and Safety

- Block if no confirmed active plan exists.
- Block if host sub-agent tools are unavailable.
- Block if write sets cannot be separated or serialized safely.
- Block or route back to `$m-plan` if a required change is outside the approved plan.
- Fail explicitly when validation cannot run or UI evidence is required but unavailable.
- Never fabricate test success.
- Never use main-agent direct edits as fallback during `$m-go`.

##### Performance and Testing Strategy

- Keep source changes textual and local.
- Use repository validators for affected skills.
- Use sync script for source-to-install parity.
- Use markdown link checks only if docs links are changed enough to justify it.
- Use `git diff --check` for whitespace.
- Heavy `$m-test` after implementation should review the workflow contract, not a UI path, because this change does not affect a visual UI.

##### Extensibility Design Points

- `$m-go` can later add richer result tables without changing `$m-execute`.
- Future automation variants can reuse `references/go.md` patterns.
- Keeping `$m-go` separate preserves `$m-execute` for lower automation and explicit user-controlled testing.

#### Issue List

- No architecture blocker.
- Execution approval is still required.

### Stage 3.1 - Planning

#### Project Goal and Current State

Current state: the workflow has `$m-discuss`, `$m-plan`, `$m-execute`, `$m-test`, `$m-archive`, and `$m-autoflow` umbrella routing. Sub-agent use is currently optional in execution/test phases when safe. There is no `$m-go` command.

Goal: add `$m-go` as a strict delegated execution and automatic test-loop command.

#### Docs Governance Routing Decision

Use `$m-docs` routing:

- Original request evidence belongs in `docs/intake`.
- Current command behavior belongs in `docs/features`.
- Durable intent and acceptance belong in `docs/requirements`.
- Package and workflow contracts belong in `docs/specs`.
- The decision to add `$m-go` as a separate command belongs in `docs/decisions`.
- Workflow result belongs in `docs/change` during archive, not execution.
- No reusable troubleshooting lesson is known at planning time, but frontmatter validation lesson should be respected.

#### Related Intake / Features / Requirements / Specs / Decisions / Lessons

- Related intake:
  - To add: `docs/intake/2026-07-09_m-go-automated-execution.md`
- Related features:
  - `docs/features/m-autoflow-workflow.md`
- Related requirements:
  - `docs/requirements/m-autoflow-skill.md`
- Related specs:
  - `docs/specs/m-autoflow-skill.md`
- Related decisions:
  - Existing: `docs/decisions/2026-07-08_m-skill-phase-naming.md`
  - To add: `docs/decisions/2026-07-09_m-go-automated-execution.md`
- Related lessons:
  - `docs/lessons/skill-frontmatter-yaml-colon.md`

#### Stable Docs Impact

- Intake impact: add
- Feature impact: clarify
- Requirements impact: clarify
- Specs impact: clarify
- Decision impact: add
- Lessons known at planning time: use existing `skill-frontmatter-yaml-colon` prevention; no new lesson planned yet

#### Executable Task List

##### Will Execute

- G1 - Update stable docs for `$m-go`
- G2 - Add `$m-go` skill package and manifest
- G3 - Integrate `$m-go` into umbrella governance
- G4 - Validate and sync affected skills

##### Will Not Execute Now

- G5 - Archive and close workflow
  - Reason: belongs to `$m-archive` after execution and optional/heavy validation.
- G6 - Push branch
  - Reason: belongs to explicit `$m-gitpush` after merge/closeout or direct user request.

#### Task Details

##### G1 - Update stable docs for `$m-go`

- Owner: Delegatable documentation worker
- Worktree: `D:\project\my-ai-skills\worktrees\m-go-automation`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-go-automation\plan.md`
- Goal: Record `$m-go` in governed docs as original request evidence, current behavior, durable requirement, technical contract, and architecture decision.
- Files / Modules:
  - `docs/intake/2026-07-09_m-go-automated-execution.md`
  - `docs/intake/README.md`
  - `docs/features/m-autoflow-workflow.md`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
  - `docs/decisions/2026-07-09_m-go-automated-execution.md`
  - `docs/decisions/README.md`
- Write Set:
  - `docs/intake/**`
  - `docs/features/m-autoflow-workflow.md`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
  - `docs/decisions/**`
- Acceptance:
  - Docs clearly say `$m-go` is a separate automated delegated execution/test-loop command.
  - Docs distinguish `$m-go` from `$m-execute`, `$m-test`, and `$m-archive`.
  - Indexes include new intake and decision docs.
  - Stable docs do not rely on `docs/change` as the only current truth.
- Test Points:
  - Manual link review for added relative links.
  - `git diff --check`.
- Rollback:
  - Remove new intake/decision docs and revert edits to feature/requirement/spec/index docs.

##### G2 - Add `$m-go` skill package and manifest

- Owner: Delegatable skill-package worker
- Worktree: `D:\project\my-ai-skills\worktrees\m-go-automation`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-go-automation\plan.md`
- Goal: Create the canonical `$m-go` source package with detailed delegated execution and automatic test-loop rules.
- Files / Modules:
  - `skills/m-go/SKILL.md`
  - `skills/m-go/references/go.md`
  - `skills/m-go/agents/openai.yaml`
  - `manifests/m-go.json`
- Write Set:
  - `skills/m-go/**`
  - `manifests/m-go.json`
- Acceptance:
  - Skill frontmatter is valid and concise.
  - `SKILL.md` references `references/go.md`, `../m-autoflow/references/subagents.md`, and `../m-test/SKILL.md` or its testing reference as needed.
  - `references/go.md` defines entry gate, mandatory worker edits, parallel dispatch, test loop, blocker handling, and exit gate.
  - Manifest matches repository conventions.
- Test Points:
  - `tools\validate-skills.ps1 -Skill m-go`
  - `tools\sync-skills.ps1 -Skill m-go`
- Rollback:
  - Delete `skills/m-go` and `manifests/m-go.json`.

##### G3 - Integrate `$m-go` into umbrella governance

- Owner: Delegatable governance worker, after or alongside G2 with coordination
- Worktree: `D:\project\my-ai-skills\worktrees\m-go-automation`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-go-automation\plan.md`
- Goal: Make `$m-go` discoverable from `$m-autoflow` and align shared stage/sub-agent rules with the new automation semantics.
- Files / Modules:
  - `skills/m-autoflow/SKILL.md`
  - `skills/m-autoflow/references/stages.md`
  - `skills/m-autoflow/references/subagents.md`
  - `skills/m-autoflow/references/templates.md` if needed
  - `skills/m-autoflow/agents/openai.yaml` if default prompt should mention go
  - `manifests/m-autoflow.json`
  - Potentially `skills/m-execute/SKILL.md` or `skills/m-execute/references/execution.md` only if a cross-reference is necessary
  - Potentially `skills/m-test/SKILL.md` or `skills/m-test/references/testing.md` only if a cross-reference is necessary
- Write Set:
  - `skills/m-autoflow/**`
  - `manifests/m-autoflow.json`
  - Optional narrow edits to `skills/m-execute/**` and `skills/m-test/**`
- Acceptance:
  - `$m-autoflow` lists `$m-go` as high-automation execution after planning.
  - Default workflow remains discuss -> plan -> execute or go -> optional/automatic test -> archive.
  - `$m-go` automatic test behavior is clear without weakening the user's ability to explicitly skip `$m-test` in normal `$m-execute` flows.
  - Sub-agent governance explains mandatory `$m-go` implementation delegation and non-delegable main-agent audit responsibilities.
  - `manifests/m-autoflow.json` depends on `m-go`.
- Test Points:
  - `tools\validate-skills.ps1 -Skill m-autoflow`
  - Focused review for contradictions with `$m-execute` and `$m-test`.
- Rollback:
  - Revert umbrella/governance edits and manifest dependency.

##### G4 - Validate and sync affected skills

- Owner: Main agent may run commands and audit results; file-edit fixes must be delegated if using `$m-go` semantics in future. For this implementation workflow, fixes remain mapped to Task IDs.
- Worktree: `D:\project\my-ai-skills\worktrees\m-go-automation`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-go-automation\plan.md`
- Goal: Confirm source packages are valid and local installed copies are updated.
- Files / Modules:
  - Source validation: `skills/m-go`, `skills/m-autoflow`, and any touched existing skills.
  - Installed copies under `C:\Users\HelloWorld\.codex\skills\...` via sync script.
- Write Set:
  - Expected repository source edits from G1-G3.
  - Generated `dist/` is ignored.
  - Installed skill copies outside the repo are modified by `tools\sync-skills.ps1`.
- Acceptance:
  - `tools\validate-skills.ps1 -Skill m-go` passes.
  - `tools\validate-skills.ps1 -Skill m-autoflow` passes.
  - Any touched existing phase skill validation passes.
  - `tools\sync-skills.ps1 -Skill m-go` succeeds.
  - `tools\sync-skills.ps1 -Skill m-autoflow` succeeds.
  - Any touched existing phase skill sync succeeds when required.
  - `git diff --check` passes.
  - `git status` is understood before commit.
- Test Points:
  - Validation and sync commands above.
  - Optional markdown relative-link check if docs links changed materially.
- Rollback:
  - Revert source edits from G1-G3 and rerun sync for affected skills if installed copies must be restored.

##### G5 - Archive and close workflow

- Owner: `$m-archive`
- Worktree: `D:\project\my-ai-skills\worktrees\m-go-automation`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-go-automation\plan.md`
- Goal: Create `docs/change`, record validation, lessons impact, sub-agent trace if any, merge, and cleanup according to archive rules.
- Files / Modules:
  - `docs/change/2026-07-09_m-go-automated-execution.md`
  - `docs/change/README.md`
  - Potential `docs/lessons/**` only if a reusable lesson emerges.
- Write Set:
  - Not part of the next execution phase.
- Acceptance:
  - Archive follows `$m-archive` and `$m-docs`.
- Test Points:
  - Archive-stage verification.
- Rollback:
  - Archive-specific rollback handled by `$m-archive`.

##### G6 - Push branch

- Owner: `$m-gitpush`
- Worktree: control-plane after archive/merge or explicit user request
- Plan Path: `D:\project\my-ai-skills\worktrees\m-go-automation\plan.md`
- Goal: Push only after user explicitly invokes push workflow.
- Files / Modules:
  - None.
- Write Set:
  - Not part of the next execution phase.
- Acceptance:
  - Push succeeds or proxy fallback behavior is reported by `$m-gitpush`.
- Test Points:
  - Remote branch/status verification.
- Rollback:
  - Not applicable in execution phase.

#### Dependencies

- G2 and G1 can start independently if write sets remain disjoint.
- G3 depends conceptually on G2's `$m-go` wording but can be drafted in parallel if the interface contract is stable.
- G4 depends on G1-G3.
- G5 depends on execution and testing completion.
- G6 depends on explicit user instruction.

#### Risks and Notes

- The strongest rule to preserve is: `$m-go` forbids direct main-agent implementation edits.
- Avoid writing `$m-go` as a replacement for `$m-execute`; it is a stronger automation option after planning.
- Keep the automatic `$m-test` loop bounded by explicit failure/blocker handling.
- Validate frontmatter after every skill file change.
- Do not add docs remotes or choose backup destinations.

#### Parallelism Assessment

Parallelism is possible after user approval:

- G1 can be delegated to a docs worker.
- G2 can be delegated to a skill-package worker.
- G3 can be delegated after G2 wording is stable, or drafted in parallel with a narrow context package and reviewed carefully for consistency.
- G4 is mostly serial after edits, though validation of independent skills can be run in parallel where command output remains clear.

Suggested context package for delegated workers:

- Stage: `3.2`
- Workflow goal: Add `$m-go` as a delegated automated execution and automatic `$m-test` loop command.
- Repo: `D:\project\my-ai-skills`
- Branch: `feat/m-go-automation`
- Base branch: `main`
- Worktree: `D:\project\my-ai-skills\worktrees\m-go-automation`
- Plan path: `D:\project\my-ai-skills\worktrees\m-go-automation\plan.md`
- Requirements/spec references:
  - `docs/features/m-autoflow-workflow.md`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
  - `docs/decisions/2026-07-08_m-skill-phase-naming.md`
  - `skills/m-autoflow/references/subagents.md`
  - `skills/m-test/references/testing.md`
- Worker rules:
  - Complete only the assigned Task ID.
  - Stay inside the assigned write set.
  - Do not add plan-external changes.
  - Do not revert user or other-worker changes.
  - Report changed files, test results, risks, rollback notes, and completion status.

#### Issue List

- No unresolved requirement or architecture issue.
- Awaiting user approval before entering execution.

### Stage 3.2 - Execution Results

#### Executed Task IDs

- G1 - Completed. Stable docs now include original intake evidence, the `$m-go` architecture decision, updated current feature behavior, durable requirements, and technical contract details.
- G2 - Completed. Added the canonical `$m-go` skill package, reference rules, agent metadata, and manifest.
- G3 - Completed. Integrated `$m-go` into `$m-autoflow` routing, stage rules, sub-agent governance, manifest dependencies, and `$m-test` entry wording.
- G4 - Completed. Focused validation and source-to-install sync succeeded for affected skills.

#### Deferred Task IDs

- G5 - Not executed in this phase. Archive and closeout remain owned by `$m-archive`.
- G6 - Not executed in this phase. Push remains owned by explicit `$m-gitpush`.

#### Validation Results

- `tools\validate-skills.ps1 -Skill m-go`: passed
- `tools\validate-skills.ps1 -Skill m-autoflow`: passed
- `tools\validate-skills.ps1 -Skill m-test`: passed
- `tools\validate-skills.ps1 -Skill m-execute`: passed
- `tools\sync-skills.ps1 -Skill m-go`: passed and installed to `C:\Users\HelloWorld\.codex\skills\m-go`
- `tools\sync-skills.ps1 -Skill m-autoflow`: passed and installed to `C:\Users\HelloWorld\.codex\skills\m-autoflow`
- `tools\sync-skills.ps1 -Skill m-test`: passed and installed to `C:\Users\HelloWorld\.codex\skills\m-test`
- `git diff --check`: passed with expected Windows CRLF warnings only
- Markdown relative-link check for `docs/**/*.md`: passed
- Volatile `../../plan.md` stable-doc links: none found

#### Notes

- Sub-agents were not used during this `$m-execute` run because the user invoked `$m-execute`, not `$m-go`; host delegation rules require explicit sub-agent authorization.
- The new `$m-go` skill itself treats `$m-go` invocation as authorization for worker sub-agent execution within an approved plan scope when host policy permits delegation.
- Heavy `$m-test` remains the next optional phase for this implementation workflow unless the user proceeds directly to `$m-archive` and records the skip.
