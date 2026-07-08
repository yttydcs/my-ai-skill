# Plan - m-test UI evidence and result table

## Workflow Information
- Repo: `D:\project\my-ai-skills`
- Branch: `refactor/m-test-ui-evidence`
- Base: `main` at `a99cdc0`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\docs`
- Code Repos: `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\m-test-ui-evidence`
- Current Stage: `3.1 - Planning complete; ready for execution`

## Stage Records

### Initialization
- `guide.md`: requires each modification round to auto-commit with an English commit message matching previous style.
- Project/docs/code repo confirmation: this repo is both skill source repo and selected docs root for this workflow change.
- Base/worktree confirmation: dedicated worktree created under `worktrees\`; main repo remains control plane.

### Discuss - Discovery And Requirements Shaping
#### Goal
Strengthen `$m-test` for UI changes and make its results easier to consume without opening markdown files.

#### Scope
- Must require actual opening, operation, and screenshot evidence when `$m-test` is executed for UI-impacting changes.
- Must make UI evidence a blocking condition inside a run `$m-test`.
- Must require a concise pass/fail table in the direct user response.
- Must preserve `$m-test` as optional: the user may explicitly skip testing and go directly to `$m-archive`.
- Must update stable feature, requirement, and spec docs because workflow behavior changes.
- Must sync installed `m-test` and affected umbrella rules after validation.
- Must not push, add remotes, or choose docs backup targets.

#### Assumptions
- The user's latest message approves implementing these requirements.
- "UI changes" includes page, component, style, layout, route, interaction, form, modal, visible state, or responsive behavior changes.
- If the user skips `$m-test`, archive should record that testing was skipped and describe residual risk instead of pretending UI evidence exists.

#### Open Questions
- None.

#### Options Considered
- Option A: only mention screenshots as recommended evidence. Rejected because the user wants actual opening/operation/screenshots as an acceptance rule.
- Option B: make `$m-test` mandatory for every UI change. Rejected because the user explicitly wants `$m-test` to remain optional and skippable by going to `$m-archive`.
- Option C: keep `$m-test` optional, but when it runs for UI changes, require actual UI operation evidence and a direct pass/fail table. Recommended.

#### Research Summary
- No web research used; this is a direct workflow policy requirement from the user.

#### Worktree / Branch / Docs Root Status
- Worktree: ready.
- Branch: `refactor/m-test-ui-evidence`.
- Docs root: repository `docs`.

#### Issue List
- 阻塞：否

### Plan - Requirements And Architecture
#### Requirements Analysis
##### Goal
Update `$m-test` so UI-impacting changes produce concrete visual and interaction evidence when tested, while preserving the user's right to skip testing and archive directly.

##### Functional Requirements
- `$m-test` must detect UI-impacting changes.
- When `$m-test` runs and UI is impacted, it must open the application or relevant page, perform affected user operations, and provide screenshot evidence.
- If UI evidence cannot be gathered during a run `$m-test`, the result must be failed or blocked.
- `$m-test` must output a concise table directly to the user showing each checked area and pass/fail/blocked/skipped status.
- The direct table must include enough context to avoid requiring the user to open markdown files for the basic verdict.
- User-directed skip remains allowed: the user may skip `$m-test` and invoke `$m-archive`, with residual testing risk recorded.

##### Non-functional Requirements
- Keep `SKILL.md` concise and place detailed rules in references.
- Keep output language simple enough for repeated operational use.
- Avoid adding runtime dependencies or hard-coded environment assumptions.

##### Inputs / Outputs
- Input: direct user clarification in chat.
- Output: updated skill source, reference docs, stable docs, intake, change archive, synced installed skills, and commits.

##### Edge Cases
- A UI cannot be launched due environment/auth/dependency issues: `$m-test` records blocked or failed, not passed.
- A non-UI change runs `$m-test`: screenshot evidence is not required, but the result table still is.
- User explicitly skips `$m-test`: proceed to archive with skip reason and residual risk.
- Responsive UI affected: include desktop and mobile screenshots when practical.

##### Acceptance Criteria
- Current `m-test` rules require UI open/operate/screenshot evidence when UI changes are tested.
- Current rules require a direct user-facing pass/fail table for `$m-test` output.
- Current rules preserve optional skip and direct `$m-archive` path.
- Relevant validators pass and installed skills sync.

##### Risks
- If "UI" is defined too narrowly, visual regressions could slip through. Mitigation: define broad UI-impacting criteria.
- If screenshots are required even when the user skips `$m-test`, optionality is lost. Mitigation: scope screenshot evidence to a run `$m-test`, and require archive risk disclosure for skip.

#### Architecture Design
##### Overall Solution
Patch `skills/m-test` and `skills/m-test/references/testing.md`, then align shared stage rules and stable docs.

##### Module Responsibilities
- `skills/m-test`: entry-level semantics and exit output requirements.
- `skills/m-test/references/testing.md`: detailed UI evidence, result table, skip, and failure rules.
- `skills/m-autoflow/references/stages.md`: shared stage summary and optional skip semantics.
- Stable docs: current truth for the workflow capability.

##### Error Handling and Safety
- UI evidence missing during a run `$m-test` blocks or fails the test phase.
- User-directed skip is explicitly recorded and does not fabricate evidence.

##### Performance and Testing Strategy
- Run targeted skill validators for `m-test` and `m-autoflow`.
- Run `git diff --check`.
- Run sync for changed installed skills.

#### Stable Docs Impact
- Intake impact: add
- Feature impact: clarify
- Requirements impact: clarify
- Specs impact: clarify
- Decision impact: none
- Related intake: `docs/intake/2026-07-08_m-test-ui-evidence.md`
- Related features: `docs/features/m-autoflow-workflow.md`
- Related requirements: `docs/requirements/m-autoflow-skill.md`
- Related specs: `docs/specs/m-autoflow-skill.md`
- Related decisions: none
- Related lessons: none

#### Executable Task List
##### Will Execute
- `MTU-1`: Update `$m-test` rules for UI evidence and direct result table.
- `MTU-2`: Update stable docs and intake for the new test semantics.
- `MTU-3`: Validate, sync installed skills, archive, merge, and clean worktree.

##### Will Not Execute Now
- Browser automation tooling implementation: out of scope; this skill records workflow rules, not a reusable test runner.
- Pushing changes: out of scope unless separately requested.
- Docs remote, backup, or publication changes: user-owned and out of scope.

#### Task Details
##### MTU-1 - Update m-test rules
- Owner: Main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-test-ui-evidence`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-test-ui-evidence\plan.md`
- Goal: require UI evidence and direct pass/fail table when `$m-test` runs.
- Files / Modules: `skills/m-test`, `skills/m-autoflow/references/stages.md`
- Write Set: skill source and reference markdown.
- Acceptance: UI-impacting tested changes require actual open/operate/screenshots; output table required; user skip preserved.
- Test Points: targeted `rg`, skill validators, `git diff --check`.
- Rollback: revert the commit and resync installed skills.

##### MTU-2 - Update stable docs
- Owner: Main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-test-ui-evidence`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-test-ui-evidence\plan.md`
- Goal: keep feature, requirement, and spec docs aligned with the new semantics.
- Files / Modules: `docs/features`, `docs/requirements`, `docs/specs`, `docs/intake`.
- Write Set: stable docs and indexes.
- Acceptance: stable docs describe UI evidence, direct result table, and optional user skip.
- Test Points: targeted `rg` and diff review.
- Rollback: revert changed docs.

##### MTU-3 - Validate, sync, archive, and close
- Owner: Main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-test-ui-evidence`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-test-ui-evidence\plan.md`
- Goal: validate, sync, archive, and close the workflow.
- Files / Modules: validation/sync scripts and `docs/change`.
- Write Set: generated installed skill copies via sync, change archive, affected indexes.
- Acceptance: validation passes, commits exist, branch merges to main, worktree removed.
- Test Points: validators, sync output, final status.
- Rollback: revert commits on main and rerun sync if needed.

#### Dependencies
- Existing `tools/validate-skills.ps1` and `tools/sync-skills.ps1`.

#### Risks and Notes
- This is a skill/docs behavior change, not runtime application code.
- Heavy `$m-test` for this workflow will be skipped because this workflow itself does not change UI.

#### Parallelism Assessment
- No sub-agents. The change is small, tightly coupled, and benefits from single-agent consistency.

#### Issue List
- 阻塞：否
- 进入 3.2
