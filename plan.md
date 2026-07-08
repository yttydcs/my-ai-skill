# Plan - m-archive default closeout

## Workflow Information
- Repo: `D:\project\my-ai-skills`
- Branch: `refactor/m-archive-default-closeout`
- Base: `main` at `a13d504`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\docs`
- Code Repos: `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\m-archive-default-closeout`
- Current Stage: `4 - Archive complete; default closeout pending`

## Stage Records

### Initialization
- `guide.md`: requires every modification round to auto-commit with an English commit message matching prior style.
- Project/docs/code repo confirmation: this repository is both source package repo and selected governed docs root for this skill change.
- Base/worktree confirmation: dedicated worktree created under `worktrees\`; main repo remains control plane.

### Discuss - Discovery And Requirements Shaping
#### Goal
Align `$m-archive` semantics with the user's clarification: invoking archive should mean "archive and end workflow" by default.

#### Scope
- Must update skill rules that still require a second workflow-end confirmation after `$m-archive`.
- Must preserve an explicit escape hatch for "archive only, do not merge/clean" when the user says so.
- Must update stable feature, requirement, and spec docs because the workflow behavior changes.
- Must add a dated change archive for this correction.
- Must sync installed skill copies after validation.
- Must not push, add remotes, or choose docs backup targets.

#### Assumptions
- The user's latest statement is a direct requirement correction and implementation approval for this narrow behavior fix.
- Existing historical `docs/change` entries remain append-only and may keep older wording as history.
- Heavy integration testing is unnecessary because this is a skill/docs behavior correction with no runtime logic.

#### Open Questions
- None.

#### Options Considered
- Option A: keep explicit second confirmation. Rejected because it conflicts with the user's desired command semantics.
- Option B: make `$m-archive` always merge and clean immediately. Rejected because users still need a safe "archive only" escape hatch.
- Option C: make `$m-archive` default to closeout, but stop when the user explicitly requests archive-only. Recommended.

#### Research Summary
- No web research used; this is a local workflow semantics correction based on direct user feedback.

#### Worktree / Branch / Docs Root Status
- Worktree: ready.
- Branch: `refactor/m-archive-default-closeout`.
- Docs root: repository `docs`.

#### Issue List
- 阻塞：否

### Plan - Requirements And Architecture
#### Requirements Analysis
##### Goal
Make `$m-archive` equivalent to ending the workflow by default, including archive, merge, and cleanup.

##### Functional Requirements
- `$m-archive` must create/update archive docs and then proceed to closeout by default.
- `$m-archive` must not ask "whether to end workflow" after a normal archive invocation.
- `$m-archive` must stop after archive only when the user explicitly requests not to merge or clean up.
- `$m-autoflow` umbrella and shared stage rules must describe the same behavior.
- Stable docs must describe the new default closeout semantics.

##### Non-functional Requirements
- Keep instructions concise and avoid duplicating phase details.
- Preserve private docs remote/push/backup guardrails.
- Keep historical archives append-only except for indexes that list the new change.

##### Inputs / Outputs
- Input: direct user correction in the current chat.
- Output: updated skill source, stable docs, change archive, synced installed skills, and a local commit.

##### Edge Cases
- User says "只归档", "不要合并", or "不要清理": archive stops after docs and reports retained worktree state.
- Worktree is dirty at closeout: archive must preserve unrelated dirt and block or report instead of deleting.
- Docs root is separate from code repo in another project: archive must not infer push/backup decisions.

##### Acceptance Criteria
- No current source or stable docs claim that normal `$m-archive` must ask for a second workflow-end confirmation.
- `$m-archive` docs clearly state default closeout and explicit archive-only override.
- Relevant validators pass.
- Installed copies for changed skills are synced.
- Worktree is merged and removed after archive because default closeout now applies.

##### Risks
- Over-broad search/replace could rewrite historical change records. Mitigation: change only current skill and stable docs, not old archives except new archive/index.

#### Architecture Design
##### Overall Solution
Patch the source-of-truth instructions in `skills/m-archive`, `skills/m-autoflow`, and shared references, then align `docs/features`, `docs/requirements`, and `docs/specs`.

##### Module Responsibilities
- `skills/m-archive`: phase-specific closeout behavior.
- `skills/m-autoflow`: umbrella routing behavior.
- `skills/m-autoflow/references/stages.md`: shared phase sequencing and closeout rules.
- Stable docs: current product truth for future planning and impact checks.

##### Error Handling and Safety
- Keep closeout gated by clean-status verification, control-plane merge, and explicit preservation of unrelated dirt.
- Keep "archive only" available via explicit user instruction.

##### Performance and Testing Strategy
- Run targeted skill validation for `m-autoflow` and `m-archive`.
- Run `git diff --check`.
- Run sync for changed installed skills after validation.

#### Stable Docs Impact
- Intake impact: add
- Feature impact: clarify
- Requirements impact: clarify
- Specs impact: clarify
- Decision impact: none
- Related intake: `docs/intake/2026-07-08_m-archive-default-closeout.md`
- Related features: `docs/features/m-autoflow-workflow.md`
- Related requirements: `docs/requirements/m-autoflow-skill.md`
- Related specs: `docs/specs/m-autoflow-skill.md`
- Related decisions: none
- Related lessons: none

#### Executable Task List
##### Will Execute
- `MAC-1`: Update archive and umbrella skill rules.
- `MAC-2`: Update stable docs and indexes for default closeout semantics.
- `MAC-3`: Validate, sync installed skills, commit, archive, merge, and clean worktree.

##### Will Not Execute Now
- Compatibility aliases for old skill names: out of scope.
- Docs remote, push, backup, or publication: user-owned and out of scope.

#### Task Details
##### MAC-1 - Update skill rules
- Owner: Main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-archive-default-closeout`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-archive-default-closeout\plan.md`
- Goal: make `$m-archive` default to closeout and remove second-confirmation wording.
- Files / Modules: `skills/m-archive`, `skills/m-autoflow`, shared references.
- Write Set: skill source and reference markdown files.
- Acceptance: no current rules require asking whether to end after archive.
- Test Points: validator and targeted `rg`.
- Rollback: revert commit before merge, or revert merge commit after closeout.

##### MAC-2 - Update stable docs
- Owner: Main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-archive-default-closeout`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-archive-default-closeout\plan.md`
- Goal: keep feature, requirement, and spec docs aligned with the new semantics.
- Files / Modules: `docs/features`, `docs/requirements`, `docs/specs`, `docs/intake`.
- Write Set: stable docs and indexes.
- Acceptance: current stable docs describe archive as default closeout with archive-only override.
- Test Points: targeted `rg` and markdown diff review.
- Rollback: revert changed docs.

##### MAC-3 - Validate, sync, archive, and close
- Owner: Main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-archive-default-closeout`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-archive-default-closeout\plan.md`
- Goal: validate, sync installed skills, commit, create change archive, then close workflow by default.
- Files / Modules: validation tooling, sync tooling, `docs/change`.
- Write Set: `dist` and installed skill copies from sync if generated by the existing tool; `docs/change` archive and indexes.
- Acceptance: validation passes, commit exists, branch merges to main, worktree removed.
- Test Points: `tools/validate-skills.ps1`, `tools/sync-skills.ps1`, `git diff --check`, final `git status`.
- Rollback: revert source commit or restore from main before merge.

#### Dependencies
- Existing validation and sync scripts.

#### Risks and Notes
- This is a low-risk instruction and documentation update.
- Heavy `$m-test` will be skipped with rationale in the archive if targeted validation passes.

#### Parallelism Assessment
- No sub-agents. The write set is small and tightly coupled, so parallel editing would add coordination overhead.

#### Issue List
- 阻塞：否
- 进入 3.2

### Stage 3.2 - Implementation
- `MAC-1`: completed. Updated archive and umbrella skill rules to make `$m-archive` default to closeout with explicit archive-only override.
- `MAC-2`: completed. Updated stable feature, requirement, and spec docs; added intake evidence and index entry.
- `MAC-3`: partially completed. Validation and install sync completed before archive.
- Lightweight validation:
  - `tools\validate-skills.ps1 -Skill m-autoflow`: passed.
  - `tools\validate-skills.ps1 -Skill m-archive`: passed.
  - `git diff --check`: passed with expected CRLF conversion warnings only.
  - `tools\sync-skills.ps1 -Skill m-autoflow`: completed.
  - `tools\sync-skills.ps1 -Skill m-archive`: completed.
- Implementation commit: `7e3dfc1 fix: make archive close workflows by default`
- 阻塞：否

### Stage 3.3 - Review Decision
- Heavy `$m-test`: skipped.
- Skip reason: low-risk instruction/docs correction with no runtime code, data, auth, storage, or UI behavior.
- Residual risk: wording mismatch could recur if future docs reintroduce second-confirmation language; mitigated by targeted `rg` checks and stable-doc updates.
- 阻塞：否

### Stage 4 - Change Archive
- `$m-docs` usage: applied to route intake, stable-doc impact, change archive, and index updates.
- Change archive: `docs/change/2026-07-08_m-archive-default-closeout.md`
- Intake impact: updated
- Feature impact: updated
- Requirements impact: updated
- Specs impact: updated
- Decision impact: none
- Lessons impact: none
- Related intake: `docs/intake/2026-07-08_m-archive-default-closeout.md`
- Related features: `docs/features/m-autoflow-workflow.md`
- Related requirements: `docs/requirements/m-autoflow-skill.md`
- Related specs: `docs/specs/m-autoflow-skill.md`
- Related decisions: none
- Related lessons: none
- Default closeout: enabled by the corrected `$m-archive` semantics.
