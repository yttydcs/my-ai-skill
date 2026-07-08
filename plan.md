# Plan - m-plan task summary table

## Workflow Information
- Repo: `D:\project\my-ai-skills`
- Branch: `refactor/m-plan-task-table`
- Base: `main` at `ac5fe4d`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\docs`
- Code Repos: `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\m-plan-task-table`
- Current Stage: `3.1 - Planning complete; ready for execution`

## Stage Records

### Initialization
- `guide.md`: requires each modification round to auto-commit with an English commit message matching prior style.
- Project/docs/code repo confirmation: this repo is both skill source repo and selected docs root for this workflow change.
- Base/worktree confirmation: dedicated worktree created under `worktrees\`; main repo remains control plane.

### Discuss - Discovery And Requirements Shaping
#### Goal
Make `$m-plan` output a concise task table directly after planning so the user can review execution scope without opening `plan.md`.

#### Scope
- Must require a direct user-facing task summary table after `$m-plan`.
- Must keep `plan.md` or `todo.md` as the source of detailed handoff truth.
- Must include enough task fields to show what will execute, what will not execute, and why.
- Must update `$m-plan`, shared `m-autoflow` stage/template rules, and stable docs.
- Must sync installed `m-plan` and `m-autoflow` after validation.
- Must not push, add remotes, publish docs, or choose backup targets.

#### Assumptions
- The user's latest message approves implementing this rule.
- "Plan 之后" means after `$m-plan` produces or confirms the plan artifact, the direct response should include the task table.
- This is a workflow output contract change, not a runtime product behavior change.

#### Open Questions
- None.

#### Options Considered
- Option A: only add a table inside `plan.md`. Rejected because the user's goal is to reduce opening markdown files.
- Option B: output the full task details in chat. Rejected because it would be noisy and duplicate `plan.md`.
- Option C: keep full details in `plan.md` and output a compact direct table. Recommended.

#### Research Summary
- No web research used; this is a direct workflow requirement from the user.

#### Worktree / Branch / Docs Root Status
- Worktree: ready.
- Branch: `refactor/m-plan-task-table`.
- Docs root: repository `docs`.

#### Issue List
- 阻塞：否

### Plan - Requirements And Architecture
#### Requirements Analysis
##### Goal
Require `$m-plan` to show a compact task summary table in the direct response after the plan is drafted or confirmed.

##### Functional Requirements
- `$m-plan` must output a concise task summary table after planning.
- The table must summarize Task ID, task title, execution scope/status, main files/modules, acceptance/test focus, and risk/notes.
- The table must include both tasks that will execute after approval and tasks that will not execute now.
- The table must not replace `plan.md`; detailed per-task acceptance, tests, and rollback remain in the active plan artifact.
- Blocked planning output may use a blocker table or issue list, but must not imply execution approval.

##### Non-functional Requirements
- Keep `SKILL.md` concise and move detailed table rules into references/templates.
- Avoid duplicating large task details in chat.
- Preserve existing docs governance and private docs guardrails.

##### Inputs / Outputs
- Input: direct user requirement in chat.
- Output: updated skill source, references, stable docs, intake, change archive, synced installed skills, and commits.

##### Edge Cases
- A plan has no executable tasks due blockers: table should show blocked/deferred tasks and the response must forbid execution.
- A plan is confirming an existing complete `plan.md`: still output the table based on the confirmed task list.
- Multi-repo planning: table should show repo/module or worktree cues in the files/modules column.

##### Acceptance Criteria
- Current `$m-plan` rules require a direct task summary table after planning.
- Shared `m-autoflow` planning rules and templates define the same table.
- Stable docs describe the new direct planning table behavior.
- Validators pass and installed skills sync.

##### Risks
- The direct table could drift from `plan.md`. Mitigation: require it to summarize the active `plan.md` / `todo.md`, not redefine scope.

#### Architecture Design
##### Overall Solution
Patch `$m-plan` source and `planning.md`, add a reusable task table template in shared templates, align shared stage rules, and update stable docs.

##### Module Responsibilities
- `skills/m-plan`: entry-level output contract.
- `skills/m-plan/references/planning.md`: detailed direct table requirements.
- `skills/m-autoflow/references/stages.md`: shared stage output requirements.
- `skills/m-autoflow/references/templates.md`: reusable table format.
- Stable docs: durable workflow behavior.

##### Error Handling and Safety
- If planning is blocked, output blockers and do not mark tasks as executable.
- The table must preserve `Will Execute` / `Will Not Execute Now` boundaries.

##### Performance and Testing Strategy
- Run targeted skill validation for `m-plan` and `m-autoflow`.
- Run `git diff --check`.
- Run sync for changed installed skills.

#### Stable Docs Impact
- Intake impact: add
- Feature impact: clarify
- Requirements impact: clarify
- Specs impact: clarify
- Decision impact: none
- Related intake: `docs/intake/2026-07-08_m-plan-task-table.md`
- Related features: `docs/features/m-autoflow-workflow.md`
- Related requirements: `docs/requirements/m-autoflow-skill.md`
- Related specs: `docs/specs/m-autoflow-skill.md`
- Related decisions: none
- Related lessons: none

#### Executable Task List
##### Will Execute
- `MPT-1`: Update `$m-plan` and shared planning rules to require a direct task summary table.
- `MPT-2`: Update stable docs and intake for the new planning output contract.
- `MPT-3`: Validate, sync installed skills, archive, merge, and clean worktree.

##### Will Not Execute Now
- Push to remote: out of scope unless separately requested.
- UI/runtime tests: out of scope because this changes skill/docs text only.
- New automation to generate the table mechanically: out of scope; the skill defines the required output contract.

#### Task Details
##### MPT-1 - Update m-plan rules
- Owner: Main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-plan-task-table`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-plan-task-table\plan.md`
- Goal: require direct task summary table after `$m-plan`.
- Files / Modules: `skills/m-plan`, `skills/m-autoflow/references/stages.md`, `skills/m-autoflow/references/templates.md`.
- Write Set: skill source and reference markdown.
- Acceptance: direct table contract exists and preserves execution scope boundaries.
- Test Points: targeted `rg`, skill validators, `git diff --check`.
- Rollback: revert commit and resync installed skills.

##### MPT-2 - Update stable docs
- Owner: Main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-plan-task-table`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-plan-task-table\plan.md`
- Goal: record planning table behavior as stable workflow truth.
- Files / Modules: `docs/features`, `docs/requirements`, `docs/specs`, `docs/intake`.
- Write Set: stable docs and indexes.
- Acceptance: docs describe direct task table after plan.
- Test Points: targeted `rg` and diff review.
- Rollback: revert docs changes.

##### MPT-3 - Validate, sync, archive, and close
- Owner: Main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-plan-task-table`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-plan-task-table\plan.md`
- Goal: validate, sync, archive, and close the workflow.
- Files / Modules: validation/sync scripts and `docs/change`.
- Write Set: installed skill copies via sync, change archive, affected indexes.
- Acceptance: validation passes, commits exist, branch merges to main, worktree removed.
- Test Points: validators, sync output, final status.
- Rollback: revert commits on main and rerun sync if needed.

#### Dependencies
- Existing validation and sync scripts.

#### Risks and Notes
- This is a skill/docs behavior change, not runtime application code.
- Heavy `$m-test` will be skipped because no application UI or runtime behavior changes.

#### Parallelism Assessment
- No sub-agents. The change is small and instruction consistency matters more than parallel throughput.

#### Issue List
- 阻塞：否
- 进入 3.2
