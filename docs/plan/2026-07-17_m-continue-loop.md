# Plan - m-continue unattended convergence loop

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `feat/m-continue-loop`
- Base: `main` at `f47c38c428b113e201e2aab9d6d0e133ab18c838`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\worktrees\m-continue\docs`
- Code Repos: `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\m-continue`
- Current Stage: `$m-archive` documentation complete; ready for control-plane merge and cleanup
- Plan Path: `D:\project\my-ai-skills\worktrees\m-continue\plan.md`

## Stage Records

### Initialization

- `guide.md`: read. Every modification round must be committed automatically with an English commit message following repository history.
- Project / docs / code repo: one Git repository; its versioned `docs/` tree is the selected governed docs root.
- Dedicated worktree: confirmed under the project `worktrees/` directory.
- Main checkout: control-plane only. It has an end-of-line-only dirty state in `skills/m-autoflow/references/output-components.md`; execution and later integration must preserve it.
- Worktree state at planning start: clean on `feat/m-continue-loop` after discussion commits `14652a8` and `0bd2e81`.

### Discuss - Discovery And Requirements Shaping

#### Goal

Add `$m-continue` / `m:continue` as a thin unattended orchestrator for an already approved workflow after `$m-execute` or `$m-test`. One invocation repeatedly applies the existing execute and test behaviors without asking whether to continue.

#### Scope

Must:

- Reuse `$m-execute` and `$m-test` as the behavioral authorities instead of copying their detailed rules.
- Recover the next phase from the active plan, worktree state, and latest execution/test evidence.
- Automatically transition failed validation to execute repairs and completed implementation to test.
- Treat invocation as authorization for every in-scope execute/test iteration.
- Stop successfully only when all approved Task IDs and acceptance criteria are satisfied and test passes or records a justified skip under existing rules.
- Stop unsuccessfully only when progress genuinely requires new scope/authority/user-only input/external-state change or a non-progress loop is detected.
- Detect non-progress after three consecutive complete repair/test cycles with the same failure signature and no measurable Task, diff, or validation improvement.
- Stop before archive, merge, push, publication, or worktree cleanup.

Out of scope:

- Replacing `$m-go` or adopting its mandatory worker-only implementation boundary.
- Weakening plan, Task ID, write-set, validation, UI-evidence, or archive gates.
- Adding a persistent runtime database, state file, or executable loop script.
- Automatically invoking `$m-archive`.

#### Assumptions

- `$m-continue` is invoked against an active worktree with an approved root `plan.md` or `todo.md` and at least one prior execute/test pass.
- `$m-execute` remains authoritative for implementation and optional delegation; `$m-test` remains authoritative for heavy validation and justified skips.
- Intermediate commentary may report progress but cannot pause the loop or request continuation confirmation.
- If prior phase evidence is ambiguous, rerunning applicable validation is safer than inferring success.

#### Open Questions

- None blocking.

#### Options Considered

- Duplicate loop rules inside `$m-execute` and `$m-test`: rejected because phase transition ownership would be split and repeated.
- Extend `$m-go`: rejected because `$m-go` starts after planning and mandates worker implementation edits.
- Add a thin state-driven `$m-continue`: accepted because it preserves existing phase authorities and execution policy.

#### Recommended Direction

Create a concise companion Skill with one reference file. Keep `SKILL.md` focused on entry/exit gates and routing; keep state recovery, progress signatures, automatic transitions, and terminal rules in `references/continue.md`.

#### Research Summary

- No web research used. The design is constrained by local workflow contracts and the accepted discussion decision.

#### Worktree / Branch / Docs Root Status

- Worktree, branch, docs root, code repo, and base are confirmed.
- Discussion intake and decision records exist and are committed.

#### Issue List

- No planning blocker.
- Implementation remains blocked until the user approves MC1-MC4.

### Plan - Requirements And Architecture

#### Discussion Summary

The user clarified that `$m-continue` is not a next-step recommender. It is a single-command, unattended convergence loop. Ordinary failures are inputs to the next iteration, not reasons to stop or ask the user. Only complete acceptance or proven inability to progress terminates the command.

#### Accepted / Rejected Requirements

Accepted:

- Single invocation authorizes all approved-scope iterations.
- No continuation questions between execute and test.
- Progress-based non-progress detection with a three-cycle default threshold.
- Existing execute/test instructions remain authoritative.
- Archive remains a separate explicit phase.

Rejected:

- A fixed low total-iteration cap.
- Treating one failed test or repair attempt as terminal.
- Silent expansion into unmapped fixes or new architecture.
- Persistent state machinery that is unnecessary for a Skill-level orchestrator.

#### Requirements Analysis

##### Use Cases

- Continue immediately after `$m-execute` until required testing and repairs converge.
- Continue after a failed `$m-test` without manually invoking execute and test again.
- Resume with incomplete or ambiguous evidence by inspecting the plan/worktree and conservatively rerunning validation.
- Stop with an actionable blocker only when progress cannot be made within existing authority and scope.

##### Functional Requirements

- A valid `m-continue` source package, UI metadata, reference, and manifest exist.
- The manifest depends on `m-autoflow`, `m-execute`, and `m-test`.
- The Skill explicitly loads existing execute/test authorities and shared output/sub-agent contracts.
- The loop classifies current state as repair-needed, validation-needed, converged, or genuinely blocked.
- Each completed repair/test cycle records a normalized failure signature and measurable progress evidence.
- Three identical no-progress cycles terminate as a loop; any improvement resets the no-progress counter.
- Ordinary failure automatically transitions to the next in-scope iteration.
- Umbrella routing, stage contracts, output recipe, stable docs, and tests recognize `$m-continue`.

##### Non-functional Requirements

- Keep `SKILL.md` concise and move detailed orchestration rules to one reference file.
- Avoid executable scripts and new dependencies.
- Use explicit terminal conditions and actionable blocker output.
- Preserve backward compatibility for `$m-execute`, `$m-go`, and `$m-test`.
- Keep source/install parity through existing validation and sync tooling.

##### Inputs / Outputs

Inputs:

- Approved active plan and Task IDs.
- Current worktree/diff and task completion state.
- Latest available execute/test results, acceptance failures, and evidence.

Outputs:

- Intermediate non-blocking progress updates.
- On success: executed Task IDs, iterations, final test result, risks, and readiness for `$m-archive`.
- On failure: repeated failure signature or hard blocker, attempts/progress evidence, and required handoff.

##### Edge Cases

- First observed state is a failed test: enter execute automatically.
- First observed state is implementation-complete with no reliable test result: enter test automatically.
- Test is justifiably skipped under `$m-test`: accept only when all approved acceptance criteria are otherwise satisfied and residual risk is recorded.
- Failure changes between cycles or some checks improve: reset the same-failure counter and continue.
- A fix needs an unmapped file or new requirement: stop as outside authority and route to `$m-plan`.
- Credentials/service/UI access are unavailable: exhaust safe in-scope alternatives, then stop with explicit missing external state; never fabricate pass evidence.
- User sends a new overriding instruction: host/user direction takes precedence over unattended continuation.

##### Acceptance Criteria

- `$m-continue` can be discovered, validated, synced, and invoked as `m:continue`.
- Its contract clearly forbids continuation prompts during normal in-scope iteration.
- Its success and failure terminal states match the accepted decision.
- It does not duplicate full execute/test workflows or claim archive ownership.
- Focused tests verify manifest dependencies, authority references, automatic transitions, authorization, non-progress threshold, and terminal exclusions.
- Existing visual-output contract tests include the new workflow companion.

##### Risks

- Vague failure signatures could stop a productive loop or allow an unproductive loop to run too long.
- Wording could accidentally broaden authorization beyond approved Task IDs.
- A justified `$m-test` skip could be mistaken for unconditional success unless acceptance and residual-risk checks remain explicit.
- Main-checkout line-ending dirt on `output-components.md` must not be overwritten during later integration.

#### Architecture Design

##### Overall Solution

Add `skills/m-continue` as a thin Skill package. Its `SKILL.md` routes to the existing `$m-execute` and `$m-test` Skill/reference files and to `references/continue.md`. The reference owns only orchestration-specific state recovery, progress comparison, automatic transition, authorization, and terminal reporting.

##### Module Responsibilities

- `skills/m-continue/SKILL.md`: trigger metadata, entry gate, quick-start references, high-level loop, exit report.
- `skills/m-continue/references/continue.md`: state classification, full-cycle definition, progress signature, three-cycle non-progress rule, hard blockers, and unattended transition rules.
- `skills/m-continue/agents/openai.yaml`: `m:continue` UI metadata.
- `manifests/m-continue.json`: copy install metadata and dependencies.
- `skills/m-autoflow/**`: umbrella discovery, stage placement, delegation inheritance, and output recipe.
- `tests/test_m_continue_contract.py`: focused package and semantic contract checks.
- `tests/test_visual_output_contract.py`: shared output-reference and recipe coverage.
- Stable docs: current behavior, durable requirement, package/workflow/validation contracts.

##### Data / Call Flow

1. Validate active approved plan, worktree, prior execute/test state, and authorization boundary.
2. Inspect task status, diff, and latest evidence.
3. If implementation is incomplete or validation failed, apply `$m-execute` behavior.
4. When implementation is ready, apply `$m-test` behavior.
5. Compare the new result to the previous normalized failure/progress signature.
6. If acceptance converged, report archive readiness.
7. If failure remains but progress occurred, reset the non-progress count and repeat.
8. If the same failure has no measurable improvement for three complete cycles, or a hard out-of-scope/external blocker exists, stop with evidence.

##### Interface Drafts

- Skill name: `m-continue`
- Display name: `m:continue`
- Suggested description: continue an already approved m-autoflow execution/test workflow unattended until acceptance converges or progress is genuinely impossible.
- Manifest dependencies: `m-autoflow`, `m-execute`, `m-test`.
- Reference file: `references/continue.md`.

##### Error Handling and Safety

- Never treat missing evidence as passed.
- Never expand approved Task IDs or write sets silently.
- Never request ordinary continuation confirmation after invocation.
- Stop immediately for required new authority or destructive/external actions outside the original scope.
- Report repeated signatures, attempted cycles, missing prerequisites, and the exact handoff needed.

##### Performance and Testing Strategy

- No runtime code or dependencies; validation is textual/package-focused.
- Add deterministic Python unittest assertions for critical contract phrases and manifest relationships.
- Run skill validation for `m-continue` and every touched existing Skill.
- Run focused unittests and `git diff --check`.
- Sync `m-continue` and `m-autoflow` after validation; verify installed copies exist and match the generated distribution.

##### Extensibility Design Points

- Progress evidence categories can be extended without changing execute/test authorities.
- The three-cycle default can later become explicit configuration only through a separate requirement/decision.
- Future phase orchestrators can reuse the state-classification pattern without copying execute/test instructions.

#### Issue List

- No architecture blocker.
- User approval is required before implementation.

### Stage 3.1 - Planning

#### Project Goal and Current State

- Current state: discussion intake and decision are committed; no `m-continue` package exists.
- Goal: add and install a canonical unattended continuation Skill while preserving existing phase ownership.

#### Docs Governance Routing Decision

Using `$m-docs`:

- Original request evidence: existing `docs/intake/2026-07-17_m-continue-loop.md`.
- Current workflow behavior: clarify `docs/features/m-autoflow-workflow.md` during planning.
- Durable capability intent: clarify `docs/requirements/m-autoflow-skill.md` during planning.
- Technical package/workflow/test contract: clarify `docs/specs/m-autoflow-skill.md` during planning.
- Architecture choice: existing accepted `docs/decisions/2026-07-17_m-continue-loop.md`.
- Active control plan: this root `plan.md`; retained archive will move/copy it into `docs/plan` during `$m-archive`.
- Change and lessons: deferred to `$m-archive`; no new reusable troubleshooting lesson is known yet.

#### Related Intake / Features / Requirements / Specs / Decisions / Lessons

- Intake: `docs/intake/2026-07-17_m-continue-loop.md`
- Feature: `docs/features/m-autoflow-workflow.md`
- Requirements: `docs/requirements/m-autoflow-skill.md`
- Spec: `docs/specs/m-autoflow-skill.md`
- Decision: `docs/decisions/2026-07-17_m-continue-loop.md`
- Existing lessons: `docs/lessons/skill-frontmatter-yaml-colon.md`, `docs/lessons/windows-skill-parity-line-endings.md`

#### Stable Docs Impact

- Intake impact: clarify (completed during planning)
- Feature impact: clarify (completed during planning)
- Requirements impact: clarify (completed during planning)
- Specs impact: clarify (completed during planning)
- Decision impact: add/clarify (completed during discussion)
- Lessons impact at planning time: none; reuse existing validation and line-ending lessons

#### Executable Task List

##### Will Execute

- MC1 - Create the `m-continue` Skill package and manifest.
- MC2 - Integrate `m-continue` into umbrella routing and shared contracts.
- MC3 - Add focused continuation and output-contract tests.
- MC4 - Validate, sync, and verify source/install parity.

##### Will Not Execute Now

- MC5 - Archive, merge, and worktree cleanup; deferred to `$m-archive` after execution/test convergence.
- MC6 - Push; requires an explicit `$m-gitpush` request.

#### Task Details

##### MC1 - Create the m-continue Skill package and manifest

- Owner: main execution agent; delegatable only if later explicitly authorized and host policy permits.
- Worktree: `D:\project\my-ai-skills\worktrees\m-continue`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-continue\plan.md`
- Goal: create the canonical source package using `skill-creator` initialization/metadata conventions.
- Files / Modules:
  - `skills/m-continue/SKILL.md`
  - `skills/m-continue/references/continue.md`
  - `skills/m-continue/agents/openai.yaml`
  - `manifests/m-continue.json`
- Write Set: `skills/m-continue/**`, `manifests/m-continue.json`
- Acceptance:
  - Valid concise frontmatter and UI metadata.
  - Explicit authoritative references to execute/test and shared output/sub-agent contracts.
  - Unattended authorization, state transitions, progress reset, three-cycle no-progress rule, hard blockers, and archive exclusion are explicit.
- Test Points: `tools\validate-skills.ps1 -Skill m-continue`; focused contract unittest.
- Rollback: remove the new source package and manifest.

##### MC2 - Integrate m-continue into umbrella routing and shared contracts

- Owner: main execution agent; may be a separate bounded lane if delegation is explicitly authorized.
- Worktree: `D:\project\my-ai-skills\worktrees\m-continue`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-continue\plan.md`
- Goal: make the command discoverable and place it correctly after execute/test without changing existing phase behavior.
- Files / Modules:
  - `skills/m-autoflow/SKILL.md`
  - `skills/m-autoflow/references/stages.md`
  - `skills/m-autoflow/references/subagents.md`
  - `skills/m-autoflow/references/output-components.md`
  - `manifests/m-autoflow.json`
- Write Set: the five files above only.
- Acceptance:
  - Umbrella distinguishes `$m-continue` from `$m-go`.
  - Stage rules describe post-execute/test continuation and unattended stopping conditions.
  - Delegation inherits `$m-execute` policy and is not mandatory.
  - Output recipe summarizes iterations, Task IDs, validation, and terminal reason.
  - Umbrella manifest depends on `m-continue`.
- Test Points: `tools\validate-skills.ps1 -Skill m-autoflow`; focused text review; visual-output unittest.
- Rollback: revert only the umbrella/reference/manifest additions.

##### MC3 - Add focused continuation and output-contract tests

- Owner: main execution agent; can be drafted independently after the interface wording is fixed.
- Worktree: `D:\project\my-ai-skills\worktrees\m-continue`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-continue\plan.md`
- Goal: prevent regression of the new package and its critical unattended-loop semantics.
- Files / Modules:
  - `tests/test_m_continue_contract.py`
  - `tests/test_visual_output_contract.py`
- Write Set: the two test files above only.
- Acceptance:
  - Tests verify package files, manifest dependency/reference shape, execute/test authority links, full-loop authorization, no-confirmation rule, progress signature/reset, three-cycle threshold, hard blockers, and archive exclusion.
  - Shared output routing and recipe coverage include `m-continue`.
- Test Points: `python -m unittest discover -s tests -p "test_*contract.py"`.
- Rollback: remove the focused test and revert the visual-output test addition.

##### MC4 - Validate, sync, and verify source/install parity

- Owner: main execution agent runs and audits commands.
- Worktree: `D:\project\my-ai-skills\worktrees\m-continue`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-continue\plan.md`
- Goal: validate final sources and install discoverable local copies.
- Files / Modules:
  - Generated ignored `dist/codex/m-continue` and `dist/codex/m-autoflow`.
  - Installed `C:\Users\HelloWorld\.codex\skills\m-continue` and refreshed `m-autoflow`.
- Write Set: generated distribution/install copies only; corrective source edits must remain within MC1-MC3 write sets.
- Acceptance:
  - Skill validation passes for `m-continue` and `m-autoflow`.
  - Focused unittests and `git diff --check` pass.
  - Sync succeeds for `m-continue` and `m-autoflow`.
  - Installed package contains no extra or missing source files and manifest references resolve.
- Test Points:
  - `tools\validate-skills.ps1 -Skill m-continue`
  - `tools\validate-skills.ps1 -Skill m-autoflow`
  - `python -m unittest discover -s tests -p "test_*contract.py"`
  - `tools\sync-skills.ps1 -Skill m-continue`
  - `tools\sync-skills.ps1 -Skill m-autoflow`
  - `git diff --check`
- Rollback: revert MC1-MC3 and resync affected prior sources if installed copies must be restored.

##### MC5 - Archive, merge, and worktree cleanup

- Owner: `$m-archive`
- Scope: Will not execute now.
- Reason: closeout is outside `$m-plan`/`$m-execute` and follows successful validation.
- Expected artifacts: `docs/change/2026-07-17_m-continue-loop.md`, change index, retained plan archive, optional lesson only if reusable troubleshooting emerges.

##### MC6 - Push

- Owner: `$m-gitpush`
- Scope: Will not execute now.
- Reason: no push was requested.

#### Dependencies

- MC1 defines the canonical package contract.
- MC2 may proceed alongside MC1 once names/references are fixed; it must be reviewed against final MC1 wording.
- MC3 depends on the agreed contract but has a disjoint write set.
- MC4 is serial after MC1-MC3.
- MC5 depends on completed execution and validation.
- MC6 requires explicit user instruction.

#### Risks and Notes

- Preserve Task ID and authorization boundaries even though continuation is unattended.
- Treat repeated equal failures as terminal only when measurable progress is also absent.
- Do not create or commit generated `dist/`; it is ignored and sync-owned.
- Do not overwrite the main checkout's line-ending-only `output-components.md` dirt during later merge/cleanup.
- Do not add remotes or push.

#### Parallelism Assessment

- MC1, MC2, and MC3 have mostly disjoint write sets and can form parallel implementation lanes only if the user later explicitly authorizes sub-agent delegation and host policy permits it.
- Under ordinary `$m-execute`, the main agent may implement them serially with no loss of correctness.
- MC4 must remain serial after all source/test edits converge.

#### Issue List

- Approved: yes, through the user's explicit `$m-execute` invocation.
- Blocked: no for MC1-MC4.

### Stage 3.2 - Execution Results

#### Approved And Executed Task IDs

- MC1 - Completed. Created the canonical `m-continue` Skill package, reference, UI metadata, and manifest using the standard `skill-creator` initializer.
- MC2 - Completed. Integrated `$m-continue` into umbrella discovery, stage routing, delegation governance, output recipes, and manifest dependencies.
- MC3 - Completed. Added focused continuation contract tests and shared visual-output coverage.
- MC4 - Completed. Validated, tested, synced, and hash-verified source, distribution, and installed copies.

#### Deferred Task IDs

- MC5 - Not executed. Archive, merge, and worktree cleanup remain owned by `$m-archive`.
- MC6 - Not executed. Push remains owned by an explicit `$m-gitpush` request.

#### Parallelism Result

- MC1-MC3 had separable write sets, but the user invoked ordinary `$m-execute` without authorizing implementation sub-agents and host policy does not permit proactive delegation.
- The main agent implemented MC1-MC3 serially and ran MC4 after all source changes converged.
- No sub-agents were used.

#### Changed Files By Task ID

- MC1:
  - `skills/m-continue/SKILL.md`
  - `skills/m-continue/references/continue.md`
  - `skills/m-continue/agents/openai.yaml`
  - `manifests/m-continue.json`
- MC2:
  - `skills/m-autoflow/SKILL.md`
  - `skills/m-autoflow/references/stages.md`
  - `skills/m-autoflow/references/subagents.md`
  - `skills/m-autoflow/references/output-components.md`
  - `manifests/m-autoflow.json`
- MC3:
  - `tests/test_m_continue_contract.py`
  - `tests/test_visual_output_contract.py`
- MC4:
  - ignored generated copies under `dist/codex/m-continue` and `dist/codex/m-autoflow`
  - installed copies under `C:\Users\HelloWorld\.codex\skills\m-continue` and `C:\Users\HelloWorld\.codex\skills\m-autoflow`
  - `plan.md` execution record

#### Key Design Decisions

- Keep `SKILL.md` concise and route detailed state recovery, progress signatures, and terminal rules to `references/continue.md`.
- Treat one invocation as authorization for every in-scope execute/test iteration without broadening Task IDs, write sets, external authority, or archive ownership.
- Define progress from Task completion, relevant diff, validation results, and evidence; reset the counter for any measurable improvement or changed failure signature.
- Stop a repeated loop only after three comparable complete repair/test cycles have the same signature and no progress; use no separate small total-iteration limit.
- Preserve `$m-execute` optional delegation instead of adopting `$m-go` mandatory workers.

#### Validation Results

- `tools\validate-skills.ps1 -Skill m-continue`: passed.
- `tools\validate-skills.ps1 -Skill m-autoflow`: passed.
- `python -m unittest discover -s tests -p "test_*contract.py"`: 13 passed.
- `python -m unittest discover -s tests`: 32 passed, 1 existing platform-permission test skipped.
- `tools\sync-skills.ps1 -Skill m-continue`: passed.
- `tools\sync-skills.ps1 -Skill m-autoflow`: passed.
- Source/dist/install SHA-256 parity for both synced skills: passed, excluding generated `.build-info.json`.
- `git diff --check`: passed with expected Windows line-ending warnings only.

#### Residual Risk And Heavier Validation

- No application runtime, UI, service, data, authorization, or external integration changed; heavy UI/integration testing is not required for the execution implementation itself.
- A future real workflow invocation remains the best behavioral forward test of the Agent instructions. Independent sub-agent forward testing was skipped because no sub-agent authorization was provided.
- Main-checkout `output-components.md` remains content-equivalent dirty from line endings and was not modified from this worktree.
- `$m-test` may still perform an optional final contract review before `$m-archive`.

#### Rollback

- Revert this execution commit, remove the generated/installed `m-continue` package, and resync the prior `m-autoflow` source if rollback is required.

### Stage 4 - Archive And Closeout

#### Archive Records

- Change archive: `docs/change/2026-07-17_m-continue-loop.md`
- Retained plan target: `docs/plan/2026-07-17_m-continue-loop.md`
- Reusable lesson: `docs/lessons/python-unittest-discovery-nonpackage-tests.md`

#### Docs Impact

- Intake impact: updated; linked the completed change.
- Feature impact: updated; current `$m-continue` behavior and change link are present.
- Requirements impact: updated; durable authorization, progress, termination, and boundary requirements are present.
- Specs impact: updated; package, workflow, test, sync, and installation contracts are present.
- Decision impact: updated; accepted decision links the completed change.
- Lessons impact: updated; unittest discovery for non-package tests is now searchable.
- Root docs index impact: none; no category topology or reading order changed.
- Category indexes: change, plan, and lessons updated.

#### Validation Decision

- Heavy `$m-test`: skipped with accepted low residual risk.
- Reason: only Skill/Markdown/manifest/test contracts changed; no UI, application runtime, service, data, auth, infrastructure, or external integration path changed.
- Evidence retained: 13 focused contract tests passed; 32 full tests passed with 1 established Windows permission skip; both Skills validated and synced; source/dist/install parity and `git diff --check` passed.

#### Lessons Decision

- Added `python-unittest-discovery-nonpackage-tests.md` because the import failure occurred during this workflow, is non-obvious, and is likely to recur in future plan commands.
- Reused existing frontmatter and Windows parity lessons; no additional lesson is needed.

#### Publication And Closeout

- Docs changes are local/versioned only; no remote, push, publication, or backup action was authorized.
- Default `$m-archive` closeout is authorized by invocation.
- After committing these archive records, merge `feat/m-continue-loop` from the control-plane checkout, preserve unrelated line-ending dirt, remove/prune the worktree, and delete the local feature branch when safe.
