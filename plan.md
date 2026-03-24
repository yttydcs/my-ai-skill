# Plan - rigorous-execution

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `feat/lessons-archive-lookup`
- Base: `main`
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Current Stage: `4 - Change Archive (Iteration 5)`
- Scope:
  - Strengthen the coupling between `rigorous-execution` and `docs-governor` around archive and lessons handling.
  - Make stage `4` promote reusable experience into `docs/lessons` with searchable lookup hints.
  - Add stable requirements/specs coverage for `docs-governor`.
  - Make the `requirements` versus `specs` boundary self-explanatory in stable docs.
  - Reuse the repository's existing validation and copy-sync pattern for both skills.
- Non-goals:
  - Do not weaken the staged workflow gates or rollback requirements.
  - Do not invent a separate lessons-search skill outside the governed docs system.
  - Do not modify unrelated existing skills beyond required integration references.

## Stage Records

### Initialization

- `guide.md` check:
  - `D:\project\my-ai-skills\guide.md` does not exist; initialization continues without guide-specific constraints.
- Confirmed skill source repo: `D:\project\my-ai-skills`
- Confirmed base branch: `main`
- Confirmed execution branch: `feat/rigorous-execution-skill`
- Confirmed execution worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Confirmed the main repo on `main` remains control-plane only; all implementation for this workflow will occur in the dedicated worktree.

### Stage 1 - Requirements Analysis

#### Goal

- Turn the user's AI workflow into a reusable Codex skill named `rigorous-execution`.
- Make the skill enforce a strict, auditable execution sequence instead of acting like a loose prompt snippet.
- Preserve the user's explicit engineering rules for:
  - worktree-first implementation
  - plan-first coding
  - mandatory review and archive
  - explicit blocking on unclear requirements
  - controlled sub-agent usage

#### Scope

- Must:
  - Trigger when the user wants a rigorous software delivery workflow instead of ad hoc coding.
  - Enforce the pre-work initialization checks:
    - read `guide.md` if present
    - confirm repo / module / base branch
    - ensure a dedicated branch and worktree exist under `D:\project\MyFlowHub3\worktrees\`
  - Enforce phase order:
    - `1. requirements`
    - `2. architecture`
    - `3.1 plan`
    - `3.2 implementation`
    - `3.3 code review`
    - `4. change archive`
  - Force a blocking issue list when information is missing or ambiguous.
  - Force root-level `plan.md` or `todo.md` in the active worktree before coding.
  - Force explicit `docs/change/YYYY-MM-DD_topic.md` archive creation before a workflow is considered complete.
  - Force explicit `$docs-governor` use in stages `3.1` and `4`.
  - Encode the sub-agent governance rules, dispatch template, and review obligations.
- Optional:
  - Reuse existing generic tooling:
    - `tools/validate-skills.ps1`
    - `tools/sync-skills.ps1`
  - Add repository-level docs governance scaffolding so this repository has stable `requirements` and `specs` records for the new skill.
- Out of scope:
  - Replacing `docs-governor` with a copy of its rules.
  - Modifying live project code outside this skill repository.
  - Relaxing the user's blocking or stage-order rules.

#### Use Cases

- A user asks for an implementation to be carried out with strict stage gates and explicit blockers.
- A user wants the agent to create a dedicated branch and worktree before touching code.
- A user wants `plan.md` to be handoff-ready before any implementation or sub-agent delegation.
- A user wants sub-agent use to be restricted to coding or review and fully auditable.
- A user wants change archive output in `docs/change/` before the workflow is considered done.

#### Functional Requirements

- The skill must read `guide.md` at session start when the file exists.
- The skill must refuse to enter implementation when the worktree or `plan.md` is missing.
- The skill must output staged analysis artifacts for requirements and architecture before planning.
- The skill must force explicit blocking when:
  - information is unclear
  - assumptions are unconfirmed
  - task ownership is ambiguous
  - required workflow artifacts are missing
- The skill must require explicit `$docs-governor` usage:
  - before maintaining the plan in stage `3.1`
  - before archiving change notes in stage `4`
- The skill must require a parallelism assessment before `3.2` and `3.3`.
- The skill must allow sub-agents only in `3.2` and `3.3`, after a complete context package is prepared from the confirmed plan.
- The skill must ask whether to end the workflow after stage `4`.

#### Non-functional Requirements

- Performance:
  - Keep the skill body concise and move the heavier rule tables into references.
  - Prefer deterministic repository inspection over repeated broad scanning.
- Readability:
  - Keep section names aligned with the user's workflow terminology.
  - State blocking rules in explicit, auditable language.
- Extensibility:
  - Keep docs-governor integration explicit instead of duplicating its full rulebook.
  - Keep the references modular so future workflow variants can reuse subsets.
- Maintainability:
  - Use one Git-managed source of truth in this repository.
  - Keep install output under `dist/codex/` and `~/.codex/skills/` as disposable copies.

#### Inputs / Outputs

- Inputs:
  - user request
  - current repository path
  - git branch and worktree state
  - presence or absence of `guide.md`
  - current docs topology
  - task decomposition and acceptance criteria
- Outputs:
  - staged analysis artifacts
  - blocking issue list when needed
  - confirmed `plan.md`
  - skill source files and metadata
  - validation results
  - change archive document

#### Edge Cases and Exceptions

- The active repo may lack a complete governed `docs/` tree.
- A stale `plan.md` from a previous workflow may exist in the selected worktree and must be replaced.
- The main repository root may already contain valid skills, but the new workflow must not edit them unnecessarily.
- The user may provide a task that is research-only; the skill must avoid writing code unless the staged workflow reaches `3.2`.
- The task may not be safely splittable for sub-agents even though the environment supports them.

#### Acceptance Criteria

- The repository contains a usable `rigorous-execution` skill package.
- The skill correctly encodes the user's stage ordering, blocking, worktree, planning, review, archive, and workflow-end rules.
- The skill references `docs-governor` explicitly where required.
- The new skill validates cleanly with the existing repository tooling.
- The workflow is archived with review conclusions and change mapping.

#### Risks

- Over-embedding repo-specific operational detail into `SKILL.md` would make the skill too heavy.
- Duplicating `docs-governor` rules inside the new skill would create drift.
- Leaving repository docs undefined would weaken the requirement/spec impact checks required by the workflow.

#### Issue List

- None.
- Blocked: No
- Exit criteria met for Stage 1.

### Stage 2 - Architecture Design

#### Overall Solution

- Add a new skill source package at `skills/rigorous-execution`.
- Keep the main `SKILL.md` short and procedural.
- Split detailed policy into focused references:
  - initialization and worktree rules
  - stage-by-stage outputs and blockers
  - docs-governor integration
  - sub-agent governance and dispatch context
  - plan and change templates
- Reuse the repository's generic validation and sync scripts.
- Add a dedicated manifest for the new skill so installation remains copy-based and versioned.

#### Alternatives Considered

- One large `SKILL.md` containing the whole workflow:
  - Rejected because it would be long, repetitive, and harder to audit.
- Embedding docs-governor rules directly into the new skill:
  - Rejected because it would duplicate an existing specialized skill and invite drift.
- Turning the workflow into scripts instead of a skill:
  - Rejected because the workflow is primarily procedural reasoning and audit discipline, not a deterministic automation sequence.

#### Module Responsibilities

- `skills/rigorous-execution/SKILL.md`
  - Trigger metadata and the top-level workflow.
- `skills/rigorous-execution/references/initialization.md`
  - Worktree, branch, repo, and `guide.md` rules.
- `skills/rigorous-execution/references/stages.md`
  - Outputs, blockers, and transitions for stages `1` through `4`.
- `skills/rigorous-execution/references/docs-governor-integration.md`
  - Explicit moments when `$docs-governor` must be used and how to record impact checks.
- `skills/rigorous-execution/references/subagents.md`
  - Parallelism assessment, allowed phases, context package, audit requirements, and dispatch template.
- `skills/rigorous-execution/references/templates.md`
  - Compact `plan.md` and `docs/change` skeletons aligned with the workflow.
- `skills/rigorous-execution/agents/openai.yaml`
  - UI metadata for skill discovery.
- `manifests/rigorous-execution.json`
  - Install and version metadata for copy-based sync.
- `docs/requirements/*`, `docs/specs/*`, and index files
  - Stable repository-level documentation describing why this skill exists and how its packaging/integration works.

#### Data / Call Flow

1. User request triggers `rigorous-execution`.
2. The skill checks `guide.md`, repo state, branch, and worktree prerequisites.
3. The skill performs stage `1` requirements analysis and stage `2` architecture analysis in conversation.
4. Before stage `3.1`, the skill explicitly uses `$docs-governor` to:
   - determine where planning and change artifacts belong
   - check repository docs topology
   - record requirement/spec impact
5. The skill creates or updates `plan.md` in the active worktree and only then allows stage `3.2`.
6. During `3.2` and `3.3`, the skill evaluates parallelism and uses sub-agents only when the plan and context package allow it.
7. After review, the skill archives the workflow in `docs/change/` and asks whether the workflow should end.

#### Interface Drafts

- Skill trigger:
  - user asks for rigorous, staged, auditable execution
  - user asks for mandatory worktree / plan / review / archive discipline
- Docs-governor integration:
  - explicit prompt form:
    - `Use $docs-governor to route and verify plan/change docs`
- Change archive naming:
  - `docs/change/YYYY-MM-DD_主题.md`

#### Error Handling and Safety

- Treat missing worktree, missing plan, missing Task ID, or incomplete sub-agent context as hard blockers.
- Never implement in the main repo path.
- Never skip the mandatory review or archive stage.
- Record exceptions explicitly when the workflow requires a root-level active `plan.md` while repository-level docs also exist.

#### Performance and Testing Strategy

- Keep the main skill short to minimize invocation cost.
- Use reference files for low-frequency detail.
- Validate with:
  - repository structure checks
  - `quick_validate.py`
  - copy-based sync smoke test
- Prefer no new helper scripts unless deterministic behavior is actually needed.

#### Extensibility Design Points

- References are split by governance area so future lighter-weight workflows can reuse subsets.
- Explicit docs-governor dependency keeps the new skill narrower and easier to update.
- Repository docs scaffolding gives future skills a stable place to record their own requirements and specs.

#### Issue List

- None.
- Blocked: No
- Exit criteria met for Stage 2.

### Stage 3.1 - Planning

#### Project Goal and Current State

- Goal:
  - Deliver a reusable `rigorous-execution` Codex skill that operationalizes the user's staged AI workflow.
- Current state:
  - The repository already contains `docs-governor`, generic validation/sync tooling, and a dedicated execution worktree for this workflow.
  - The selected worktree currently contains a stale `plan.md` inherited from another workflow and must be replaced.
  - The repository docs topology is incomplete:
    - `docs/change/` exists
    - `docs/README.md`, `docs/requirements/`, `docs/specs/`, `docs/plan/`, and `docs/lessons/` do not yet exist

#### Docs Governance Routing Decision

- Used `$docs-governor` for routing and impact review.
- Decision:
  - The active execution plan remains `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md` because the user's workflow mandates a root-level control document in the active worktree.
  - Repository-level stable documentation will be added under `docs/requirements/` and `docs/specs/` so requirement/spec impact can be recorded explicitly.
  - Repository navigation indexes under `docs/` will be bootstrapped because the repo is now managing multiple long-lived skills and currently lacks governed entry points.
- Requirement/spec impact:
  - Requirements impact: add
  - Specs impact: add
  - Related requirements: `docs/requirements/rigorous-execution-skill.md` (to be created)
  - Related specs: `docs/specs/rigorous-execution-skill.md` (to be created)

#### Executable Task List

- [x] RE-1 - Bootstrap repository docs governance surface
- [x] RE-2 - Initialize the `rigorous-execution` skill scaffold
- [x] RE-3 - Author the skill body and reference files
- [x] RE-4 - Add manifest metadata and validate / sync the skill
- [x] RE-5 - Review, archive, and record workflow completion state

#### Task Details

##### RE-1 - Bootstrap repository docs governance surface

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - Create the minimum governed repository docs topology and add stable requirement/spec docs for the new skill.
- Files / Modules:
  - `docs/README.md`
  - `docs/requirements/README.md`
  - `docs/specs/README.md`
  - `docs/plan/README.md`
  - `docs/change/README.md`
  - `docs/lessons/README.md`
  - `docs/requirements/rigorous-execution-skill.md`
  - `docs/specs/rigorous-execution-skill.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\**`
- Acceptance:
  - Repository docs entry points exist and follow the governed taxonomy.
  - Stable requirement/spec docs exist for the new skill.
- Test Points:
  - Bootstrap output creates the expected category indexes.
  - New requirement/spec docs are linked from category indexes.
- Rollback:
  - Remove the created docs files for this workflow if the workflow is discarded.

##### RE-2 - Initialize the `rigorous-execution` skill scaffold

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - Create the base skill package with official `skill-creator` tooling and deterministic UI metadata.
- Files / Modules:
  - `skills/rigorous-execution/**`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\skills\rigorous-execution\**`
- Acceptance:
  - The skill directory exists with `SKILL.md`, `agents/openai.yaml`, and the planned references directory.
- Test Points:
  - Expected files exist after initialization.
  - Frontmatter name matches `rigorous-execution`.
- Rollback:
  - Remove the created skill directory.

##### RE-3 - Author the skill body and reference files

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - Encode the user's workflow into concise skill instructions plus auditable references.
- Files / Modules:
  - `skills/rigorous-execution/SKILL.md`
  - `skills/rigorous-execution/references/initialization.md`
  - `skills/rigorous-execution/references/stages.md`
  - `skills/rigorous-execution/references/docs-governor-integration.md`
  - `skills/rigorous-execution/references/subagents.md`
  - `skills/rigorous-execution/references/templates.md`
  - `skills/rigorous-execution/agents/openai.yaml`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\skills\rigorous-execution\**`
- Acceptance:
  - The skill captures the user's stage rules, blockers, worktree rules, docs-governor integration, and sub-agent governance.
  - `SKILL.md` remains concise and references the detailed documents instead of duplicating them.
- Test Points:
  - All referenced files exist.
  - The skill body stays coherent without embedding the full workflow verbatim.
- Rollback:
  - Revert the skill content changes.

##### RE-4 - Add manifest metadata and validate / sync the skill

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - Add install metadata for the new skill and validate/copy it with the repository tooling.
- Files / Modules:
  - `manifests/rigorous-execution.json`
  - `dist/codex/rigorous-execution/**`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\manifests\rigorous-execution.json`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\dist\codex\rigorous-execution\**`
- Acceptance:
  - Validation passes for the new skill.
  - Sync copies the built package into `C:\Users\HelloWorld\.codex\skills\rigorous-execution`.
- Test Points:
  - `tools/validate-skills.ps1 -Skill rigorous-execution` passes.
  - `tools/sync-skills.ps1 -Skill rigorous-execution` completes successfully.
- Rollback:
  - Remove the manifest and installed copy, then delete generated dist output.

##### RE-5 - Review, archive, and record workflow completion state

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - Review the implementation, record the result, and archive the workflow.
- Files / Modules:
  - `plan.md`
  - `docs/change/YYYY-MM-DD_rigorous-execution-skill.md`
  - affected docs indexes if archive navigation changes
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\change\**`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\README.md`
- Acceptance:
  - Review conclusions are recorded against the required criteria.
  - The change archive maps back to RE-1 through RE-5.
- Test Points:
  - Archive file exists with required sections.
  - Review conclusions reference actual validation steps.
- Rollback:
  - Revert the archive and review notes if the workflow is discarded.

#### Dependencies

- RE-1 precedes RE-5 and should complete before the final archive so requirements/specs are stable.
- RE-2 precedes RE-3 and RE-4.
- RE-3 precedes RE-4 because validation requires the final skill content.
- RE-5 depends on RE-1 through RE-4.

#### Risks and Notes

- The root `plan.md` location is a deliberate workflow-control exception to docs-governor's archival `docs/plan/` default.
- The new skill must reference `docs-governor` instead of copying its taxonomy wholesale.
- The existing validation and sync scripts are generic, so only new manifest data should be needed unless testing reveals a gap.

#### Parallelism Assessment

- No sub-agent delegation is allowed in `3.1`.
- Preliminary implementation split was assessed:
  - RE-1 is docs-heavy and RE-2 through RE-4 are skill-heavy, but all depend on the same newly confirmed repository/documentation model.
  - The work is currently kept with the Main Agent to avoid inconsistent policy wording across the skill and stable docs.
- A fresh parallelism assessment will be required again on entry to `3.2`.

#### Issue List

- None.
- Blocked: No
- Exit criteria met for Stage 3.1.

### Stage 3.2 - Implementation

#### RE-1 - Bootstrap repository docs governance surface

- Completed.
- Used `$docs-governor` bootstrap tooling to create repository docs indexes:
  - `docs/README.md`
  - `docs/requirements/README.md`
  - `docs/specs/README.md`
  - `docs/plan/README.md`
  - `docs/change/README.md`
  - `docs/lessons/README.md`
- Added stable repository docs for the new capability:
  - `docs/requirements/rigorous-execution-skill.md`
  - `docs/specs/rigorous-execution-skill.md`

#### RE-2 - Initialize the `rigorous-execution` skill scaffold

- Completed.
- Created the source package with the official `init_skill.py` script at:
  - `skills/rigorous-execution`
- Generated:
  - `skills/rigorous-execution/SKILL.md`
  - `skills/rigorous-execution/agents/openai.yaml`
  - `skills/rigorous-execution/references/`

#### RE-3 - Author the skill body and reference files

- Completed.
- Replaced the template skill body with a concise workflow-oriented skill.
- Added focused references:
  - `initialization.md`
  - `stages.md`
  - `docs-governor-integration.md`
  - `subagents.md`
  - `templates.md`
- Corrected generated UI metadata after discovering PowerShell stripped the literal `$` from the default prompt during scaffold creation.

#### RE-4 - Add manifest metadata and validate / sync the skill

- Completed.
- Added install metadata:
  - `manifests/rigorous-execution.json`
- Validation:
  - `tools/validate-skills.ps1 -Skill rigorous-execution -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - Result: passed, `Skill is valid!`
- Sync:
  - `tools/sync-skills.ps1 -Skill rigorous-execution`
  - Result: built `dist/codex/rigorous-execution` and copied to `C:\Users\HelloWorld\.codex\skills\rigorous-execution`
- Residual template scan:
  - `rg` check for `TODO`, `Structuring This Skill`, and the broken `Use -execution` string returned no matches.

### Stage 3.3 - Code Review

#### Review Result

- 需求覆盖：通过
  - The skill covers initialization, stage order, blockers, `plan.md`, docs-governor integration, controlled sub-agent use, review, archive, and workflow-end confirmation.
- 架构合理性：通过
  - The implementation keeps `SKILL.md` concise and pushes detailed rules into references, matching the repository's existing skill pattern.
- 性能风险（N+1 / 重复计算 / 多余 I/O / 锁竞争）：通过
  - No runtime code or extra automation layer was introduced; the skill mostly adds static guidance and reuses existing scripts.
- 可读性与一致性：通过
  - File names, rule boundaries, and terminology remain explicit and aligned with the user's workflow.
- 可扩展性与配置化：通过
  - Docs-governor integration stays modular, and future workflow variants can extend the references without rewriting the main skill.
- 稳定性与安全：通过
  - The workflow explicitly blocks on missing prerequisites, forbids implementation in the main repo, and respects host policy for sub-agent use.
- 测试覆盖情况：通过
  - Skill validation passed.
  - Copy-sync produced both `dist` and install targets.
  - Residual scaffold markers were removed.
- 子Agent治理与审计（任务映射、上下文完整性、文件所有权、结果复核、冲突处理、记录完整性）：通过
  - No sub-agents were used.
  - Reason: current host policy requires explicit user authorization before delegation, and the session did not include such authorization.
- Conclusion: Passed
  - No blocking review findings remain.

### Stage 4 - Change Archive

#### Docs Governance Check

- Used `$docs-governor` before archive completion.
- Requirements impact: updated
  - Added `docs/requirements/rigorous-execution-skill.md`
- Specs impact: updated
  - Added `docs/specs/rigorous-execution-skill.md`
- Lessons impact: none
  - No recurring failure pattern or costly investigation trail justified a lessons document in this workflow.
- Index updates required: yes
  - `docs/README.md`
  - `docs/requirements/README.md`
  - `docs/specs/README.md`
  - `docs/change/README.md`

#### Archive Result

- Change archive document created:
  - `docs/change/2026-03-23_rigorous-execution-skill.md`
- Post-archive verification fixes:
  - removed accidental patch-marker and pasted archive-body pollution from `docs/change/README.md`
- Stage 4 complete.

## Iteration 2 - Manual Invocation And Fidelity Hardening

### Initialization Refresh

- Continued in the same dedicated branch and worktree after the user requested another iteration instead of ending the workflow.
- `guide.md` remains absent in the repository root.
- Main repo is still control-plane only; implementation continues only in:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`

### Stage 1 - Requirements Analysis

#### Goal

- Tighten `rigorous-execution` so it matches the user's original workflow more exactly.
- Make the skill manual-invocation-only instead of implicitly injectable.

#### Scope

- Must:
  - disable implicit invocation for `rigorous-execution`
  - encode the missing hard rules from the original prompt, especially:
    - one stage at a time
    - rollback must state the reason and update docs
    - no unconfirmed assumptions about business, data, interface, environment, dependency version, acceptance, or preference
    - stronger `3.2` code quality gates
    - stronger sub-agent duty boundaries and mandatory-use conditions, subject to host policy
    - stronger cross-repo and control-plane constraints
- Optional:
  - clarify repository requirement/spec wording so it reflects manual invocation and the fuller governance contract
- Out of scope:
  - new runtime helper scripts
  - changing repository-wide validation tooling

#### Use Cases

- The user explicitly invokes `$rigorous-execution` for high-discipline implementation work.
- The user wants the skill to behave like an enforceable engineering protocol instead of a summarized guideline.

#### Functional Requirements

- The skill must require explicit invocation and must not auto-trigger.
- The skill must encode the missing prompt rules with hard wording instead of loose guidance.
- The skill must preserve compatibility with the existing copy-sync and validation flow.

#### Non-functional Requirements

- Performance:
  - keep `SKILL.md` concise even after hardening the rules
- Readability:
  - keep the hardest rules in focused reference files instead of duplicating them across files
- Maintainability:
  - update existing stable requirement/spec docs rather than creating competing duplicates

#### Inputs / Outputs

- Inputs:
  - current `rigorous-execution` skill source
  - original workflow constraints already captured in the conversation
- Outputs:
  - hardened skill and references
  - manual invocation policy in `agents/openai.yaml`
  - updated requirement/spec docs
  - second-round review and archive

#### Edge Cases

- Host platform policy may still prevent sub-agent dispatch even if the workflow would otherwise require it.
- The repository already has a same-day change archive for iteration 1, so iteration 2 must archive under a distinct topic name.

#### Acceptance Criteria

- `rigorous-execution` becomes manual-invocation-only.
- The main missing workflow rules from the original prompt are explicitly encoded.
- The updated skill validates and syncs successfully.

#### Risks

- Over-hardening `SKILL.md` itself could make the skill bloated; the hard rules should mostly land in references.

#### Issue List

- None.
- Blocked: No

### Stage 2 - Architecture Design

#### Overall Solution

- Keep `SKILL.md` as a concise command surface.
- Put the strict fidelity additions into the existing reference split:
  - `initialization.md`
  - `stages.md`
  - `subagents.md`
  - `docs-governor-integration.md`
- Add manual invocation control in `skills/rigorous-execution/agents/openai.yaml` via policy metadata.
- Update `docs/requirements/rigorous-execution-skill.md` and `docs/specs/rigorous-execution-skill.md` so the stable docs match the hardened behavior.

#### Alternatives Considered

- Copy the entire original prompt almost verbatim into `SKILL.md`:
  - Rejected because it would weaken progressive disclosure and make maintenance worse.
- Only change `openai.yaml` and leave the workflow wording mostly as-is:
  - Rejected because it would not satisfy the fidelity gap the user explicitly called out.

#### Module Responsibilities

- `skills/rigorous-execution/SKILL.md`
  - declare manual invocation and top-level workflow guarantees
- `skills/rigorous-execution/references/initialization.md`
  - own initialization, repo/worktree, and control-plane rules
- `skills/rigorous-execution/references/stages.md`
  - own hard stage transitions, rollback, and implementation/review/archive detail
- `skills/rigorous-execution/references/subagents.md`
  - own mandatory delegation conditions, forbidden outsourcing, inheritance, and audit rules
- `skills/rigorous-execution/agents/openai.yaml`
  - disable implicit invocation
- `docs/requirements/rigorous-execution-skill.md`
  - describe the durable user-facing need and boundaries
- `docs/specs/rigorous-execution-skill.md`
  - describe the technical contract, including manual invocation policy

#### Data / Call Flow

1. The user explicitly invokes `$rigorous-execution`.
2. The skill reads initialization rules and checks worktree prerequisites.
3. The skill enforces staged execution with stronger blocker and rollback language.
4. The skill uses `$docs-governor` explicitly in `3.1` and `4`.
5. Validation and sync remain unchanged.

#### Interface Drafts

- `agents/openai.yaml`
  - add:
    - `policy.allow_implicit_invocation: false`
- `SKILL.md`
  - state manual invocation explicitly

#### Error Handling and Safety

- If a stronger rule conflicts with host policy, the skill must obey host policy and record the reason.
- The skill must not silently degrade mandatory workflow rules into suggestions.

#### Performance and Testing Strategy

- Validate structure again with `tools/validate-skills.ps1`.
- Re-sync the installed copy after policy and content updates.
- Scan for stale wording that still suggests implicit triggering or looser behavior.

#### Extensibility Design Points

- A manual-only policy lets this remain a specialist protocol skill instead of a generally injected one.
- The stricter rule split still keeps future edits localized by governance area.

#### Issue List

- None.
- Blocked: No

### Stage 3.1 - Planning

#### Project Goal And Current State

- Goal:
  - harden `rigorous-execution` to align more closely with the original workflow prompt and require manual invocation
- Current state:
  - iteration 1 completed and produced a valid installable skill
  - remaining work is policy tightening and fidelity hardening

#### Docs Governance Routing Decision

- Used `$docs-governor` for routing and impact review for iteration 2.
- Decision:
  - update the existing stable docs rather than creating new requirement/spec leaf docs
  - create a new change archive for iteration 2 under a distinct same-day topic
- Requirement/spec impact:
  - Requirements impact: clarify
  - Specs impact: clarify
  - Related requirements: `docs/requirements/rigorous-execution-skill.md`
  - Related specs: `docs/specs/rigorous-execution-skill.md`

#### Executable Task List

- [x] RF-1 - Harden the stable requirement/spec contract
- [x] RF-2 - Harden skill sources and disable implicit invocation
- [x] RF-3 - Validate and re-sync the manual-only skill
- [x] RF-4 - Review and archive iteration 2

#### Task Details

##### RF-1 - Harden the stable requirement/spec contract

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - update the stable requirement/spec docs to reflect manual invocation and the fuller governance contract
- Files / Modules:
  - `docs/requirements/rigorous-execution-skill.md`
  - `docs/specs/rigorous-execution-skill.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\requirements\rigorous-execution-skill.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\specs\rigorous-execution-skill.md`
- Acceptance:
  - stable docs explicitly describe manual invocation and the tightened contract
- Test Points:
  - stable docs stay consistent with the skill sources after edits
- Rollback:
  - revert the stable docs to the iteration 1 version

##### RF-2 - Harden skill sources and disable implicit invocation

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - add the missing hard workflow rules and disable implicit invocation
- Files / Modules:
  - `skills/rigorous-execution/SKILL.md`
  - `skills/rigorous-execution/references/initialization.md`
  - `skills/rigorous-execution/references/stages.md`
  - `skills/rigorous-execution/references/docs-governor-integration.md`
  - `skills/rigorous-execution/references/subagents.md`
  - `skills/rigorous-execution/references/templates.md`
  - `skills/rigorous-execution/agents/openai.yaml`
  - `manifests/rigorous-execution.json`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\skills\rigorous-execution\**`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\manifests\rigorous-execution.json`
- Acceptance:
  - implicit invocation is disabled
  - missing hard workflow rules are explicitly encoded
- Test Points:
  - no stale wording suggests implicit triggering
  - policy metadata exists in `agents/openai.yaml`
- Rollback:
  - revert the skill source changes

##### RF-3 - Validate and re-sync the manual-only skill

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - verify the hardened skill and update the installed copy
- Files / Modules:
  - `dist/codex/rigorous-execution/**`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\dist\codex\rigorous-execution\**`
- Acceptance:
  - validation passes
  - sync updates the installed copy
- Test Points:
  - validator passes
  - install tree reflects the new `openai.yaml` policy
- Rollback:
  - remove regenerated dist/install copy and revert source edits

##### RF-4 - Review and archive iteration 2

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - review the second iteration and archive the hardening work
- Files / Modules:
  - `plan.md`
  - `docs/change/2026-03-23_rigorous-execution-alignment.md`
  - `docs/change/README.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\change\2026-03-23_rigorous-execution-alignment.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\change\README.md`
- Acceptance:
  - review conclusions and archive record the manual-only hardening
- Test Points:
  - archive exists and maps back to RF-1 through RF-4
- Rollback:
  - revert the iteration 2 archive if the round is discarded

#### Dependencies

- RF-1 and RF-2 precede RF-3.
- RF-4 depends on RF-1 through RF-3.

#### Risks And Notes

- The main fidelity risk is leaving any original hard rule as a soft suggestion.
- Manual invocation must be enforced through `openai.yaml` policy, not just wording.

#### Parallelism Assessment

- No sub-agent delegation is allowed in `3.1`.
- RF-1 and RF-2 touch overlapping contract language and should remain with the Main Agent for consistency.

#### Issue List

- None.
- Blocked: No
- Exit criteria met for Iteration 2 Stage 3.1.

### Iteration 2 - Stage 3.2 - Implementation

#### RF-1 - Harden the stable requirement/spec contract

- Completed.
- Updated `docs/requirements/rigorous-execution-skill.md` to require:
  - explicit manual invocation
  - one active stage at a time
  - rollback reason recording and document synchronization
  - no silent assumptions
  - escalation when best practice is uncertain
- Updated `docs/specs/rigorous-execution-skill.md` to encode:
  - `policy.allow_implicit_invocation: false`
  - stronger stage, rollback, and sub-agent contract wording

#### RF-2 - Harden skill sources and disable implicit invocation

- Completed.
- Updated `skills/rigorous-execution/SKILL.md` to state manual invocation explicitly and strengthen guardrails.
- Updated references:
  - `initialization.md`
  - `stages.md`
  - `docs-governor-integration.md`
  - `subagents.md`
  - `templates.md`
- Updated `skills/rigorous-execution/agents/openai.yaml`:
  - added `policy.allow_implicit_invocation: false`
- Updated `manifests/rigorous-execution.json`:
  - added `manual_invocation_only: true`

#### RF-3 - Validate and re-sync the manual-only skill

- Completed.
- Validation:
  - `tools/validate-skills.ps1 -Skill rigorous-execution -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - Result: passed
- Sync:
  - `tools/sync-skills.ps1 -Skill rigorous-execution`
  - Result: updated both `dist/codex/rigorous-execution` and `C:\Users\HelloWorld\.codex\skills\rigorous-execution`
- Manual-trigger verification:
  - source and installed `agents/openai.yaml` now both contain `policy.allow_implicit_invocation: false`

### Iteration 2 - Stage 3.3 - Code Review

#### Review Result

- 需求覆盖：通过
  - Iteration 2 closes the largest gaps previously identified: manual invocation, stronger rollback rules, stronger no-assumption wording, stronger implementation quality gates, and fuller sub-agent governance.
- 架构合理性：通过
  - The skill remains progressively disclosed instead of collapsing into one oversized file, which preserves maintainability while increasing fidelity.
- 性能风险（N+1 / 重复计算 / 多余 I/O / 锁竞争）：通过
  - The hardening remains static documentation and metadata only; no new runtime path or extra repository tooling was introduced.
- 可读性与一致性：通过
  - The stricter rules were added to the most relevant reference files without scattering overlapping truth.
- 可扩展性与配置化：通过
  - Manual-only invocation is implemented as policy metadata, and the stricter contract remains localized by concern.
- 稳定性与安全：通过
  - The installed skill now requires explicit invocation and preserves host-policy constraints around delegation.
- 测试覆盖情况：通过
  - Validation passed after the hardening round.
  - Sync updated the installed copy successfully.
  - The installed `openai.yaml` was verified to contain `allow_implicit_invocation: false`.
- 子Agent治理与审计（任务映射、上下文完整性、文件所有权、结果复核、冲突处理、记录完整性）：通过
  - Iteration 2 strengthens the delegation contract materially even though this workflow still did not dispatch sub-agents because host policy did not provide explicit user authorization.
- Conclusion: Passed
  - No blocking review findings remain for iteration 2.

### Iteration 2 - Stage 4 - Change Archive

#### Docs Governance Check

- Used `$docs-governor` before archive completion.
- Requirements impact: updated
  - clarified `docs/requirements/rigorous-execution-skill.md`
- Specs impact: updated
  - clarified `docs/specs/rigorous-execution-skill.md`
- Lessons impact: none
  - this round tightened policy wording but did not reveal a reusable incident pattern that warrants a lessons entry
- Index updates required: yes
  - `docs/change/README.md`

#### Archive Result

- Change archive document created:
  - `docs/change/2026-03-23_rigorous-execution-alignment.md`
- Iteration 2 Stage 4 complete.

## Iteration 3 - Docs Priority In Stage 1 And 2

### Initialization Refresh

- Continued in the same dedicated branch and worktree after the user requested another iteration instead of ending the workflow.
- `guide.md` remains absent in the repository root.
- Main repo remains control-plane only.

### Stage 1 - Requirements Analysis

#### Goal

- Ensure that when `$rigorous-execution` is explicitly invoked, stages `1` and `2` prioritize stable docs under `docs/requirements` and `docs/specs`.

#### Scope

- Must:
  - make stage `1` explicitly check `docs/requirements` first when the directory exists
  - make stage `2` explicitly check `docs/specs` first when the directory exists
  - clarify that stable docs should be preferred over ad hoc code-only inference when relevant docs exist
  - update the stable requirement/spec docs and archive the behavior change
- Optional:
  - mention the repository `docs/README.md` entry path if it helps orient the reader before checking category docs
- Out of scope:
  - new helper scripts
  - broader changes to docs-governor behavior

#### Use Cases

- The user explicitly invokes `$rigorous-execution` on a repository that already has governed docs.
- The user wants stage `1` and `2` to anchor on written requirements/specs instead of reconstructing everything from code.

#### Functional Requirements

- Stage `1` must prioritize `docs/requirements` when available.
- Stage `2` must prioritize `docs/specs` when available.
- The skill must still stop and ask if the stable docs are missing, conflicting, or insufficient for a behavior-changing request.

#### Non-functional Requirements

- Performance:
  - read the nearest stable docs first instead of scanning the repo broadly
- Readability:
  - keep the early-docs rule explicit and easy to notice
- Maintainability:
  - update existing stable docs rather than creating duplicates

#### Inputs / Outputs

- Inputs:
  - the explicit `$rigorous-execution` invocation
  - repository docs structure
  - relevant requirement/spec docs
- Outputs:
  - updated skill behavior
  - updated stable docs
  - validation, sync, and archive records

#### Edge Cases

- `docs/requirements` or `docs/specs` may exist but not contain a relevant leaf doc.
- Stable docs may conflict with the user request, requiring a blocker.

#### Acceptance Criteria

- The skill explicitly tells stage `1` to prioritize `docs/requirements`.
- The skill explicitly tells stage `2` to prioritize `docs/specs`.
- The updated skill validates and syncs successfully.

#### Risks

- If the wording is too weak, the reader may still treat the docs read as optional.

#### Issue List

- None.
- Blocked: No

### Stage 2 - Architecture Design

#### Overall Solution

- Update the top-level skill workflow to mention early stable-doc checks.
- Update `references/stages.md` to make those checks part of stage `1` and `2` entry behavior.
- Update the stable requirement and spec docs so the contract reflects the new priority rule.

#### Alternatives Considered

- Put the rule only in `SKILL.md`:
  - Rejected because stage-specific behavior belongs in `references/stages.md`.
- Put the rule only in stable docs:
  - Rejected because the skill body and stage rules also need to enforce it procedurally.

#### Module Responsibilities

- `skills/rigorous-execution/SKILL.md`
  - surface the new early-docs expectation prominently
- `skills/rigorous-execution/references/stages.md`
  - make stage `1`/`2` stable-doc reads explicit
- `docs/requirements/rigorous-execution-skill.md`
  - record the durable user-facing requirement
- `docs/specs/rigorous-execution-skill.md`
  - record the technical contract for early docs reads

#### Data / Call Flow

1. User explicitly invokes `$rigorous-execution`.
2. The skill checks initialization prerequisites.
3. Before stage `1` output, the skill checks `docs/requirements` first when available.
4. Before stage `2` output, the skill checks `docs/specs` first when available.
5. Later planning and archive behavior stays unchanged.

#### Interface Drafts

- `SKILL.md`
  - add an early-docs rule in quick start or workflow
- `references/stages.md`
  - add stage-specific doc-priority bullets

#### Error Handling and Safety

- If stable docs exist but conflict with the request, stop and ask.
- Do not silently skip stable docs when they are present and relevant.

#### Performance and Testing Strategy

- Revalidate and resync the skill after edits.
- Scan the updated files for the new `docs/requirements` and `docs/specs` priority wording.

#### Extensibility Design Points

- Keeping the rule in stage references lets future workflows add different stage-entry reads without bloating `SKILL.md`.

#### Issue List

- None.
- Blocked: No

### Stage 3.1 - Planning

#### Project Goal And Current State

- Goal:
  - add stable-doc priority to stages `1` and `2`
- Current state:
  - the skill already enforces manual invocation and stronger workflow rules
  - stage `1`/`2` doc-priority wording is not yet explicit enough

#### Docs Governance Routing Decision

- Used `$docs-governor` for routing and impact review for iteration 3.
- Decision:
  - update the existing stable requirement/spec docs
  - create a new same-day change archive for iteration 3
- Requirement/spec impact:
  - Requirements impact: clarify
  - Specs impact: clarify
  - Related requirements: `docs/requirements/rigorous-execution-skill.md`
  - Related specs: `docs/specs/rigorous-execution-skill.md`

#### Executable Task List

- [ ] RP-1 - Clarify stable docs for stage 1/2 priority reads
- [ ] RP-2 - Update skill workflow and stage references
- [ ] RP-3 - Validate and resync the skill
- [ ] RP-4 - Review and archive iteration 3

#### Task Details

##### RP-1 - Clarify stable docs for stage 1/2 priority reads

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - clarify in stable docs that stages `1` and `2` prioritize requirement/spec reads
- Files / Modules:
  - `docs/requirements/rigorous-execution-skill.md`
  - `docs/specs/rigorous-execution-skill.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\requirements\rigorous-execution-skill.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\specs\rigorous-execution-skill.md`
- Acceptance:
  - stable docs mention the stage `1`/`2` doc-priority contract
- Test Points:
  - stable docs and source files remain consistent
- Rollback:
  - revert the stable docs to the iteration 2 wording

##### RP-2 - Update skill workflow and stage references

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - make the early-docs behavior explicit in the skill and stage rules
- Files / Modules:
  - `skills/rigorous-execution/SKILL.md`
  - `skills/rigorous-execution/references/stages.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\skills\rigorous-execution\SKILL.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\skills\rigorous-execution\references\stages.md`
- Acceptance:
  - stage `1`/`2` doc-priority is explicit and easy to see
- Test Points:
  - no ambiguity remains about reading `docs/requirements` and `docs/specs`
- Rollback:
  - revert the source wording

##### RP-3 - Validate and resync the skill

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - verify the new wording and update the installed copy
- Files / Modules:
  - `dist/codex/rigorous-execution/**`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\dist\codex\rigorous-execution\**`
- Acceptance:
  - validation passes and install copy is refreshed
- Test Points:
  - validator passes
  - source and installed copy both contain the new stage `1`/`2` priority wording
- Rollback:
  - remove regenerated dist/install copy and revert source edits

##### RP-4 - Review and archive iteration 3

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
- Goal:
  - review the stage `1`/`2` docs-priority iteration and archive it
- Files / Modules:
  - `plan.md`
  - `docs/change/2026-03-23_rigorous-execution-doc-priority.md`
  - `docs/change/README.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\plan.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\change\2026-03-23_rigorous-execution-doc-priority.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-rigorous-execution-skill\docs\change\README.md`
- Acceptance:
  - review and archive capture the new docs-priority behavior
- Test Points:
  - archive exists and maps back to RP-1 through RP-4
- Rollback:
  - revert the iteration 3 archive if the round is discarded

#### Dependencies

- RP-1 and RP-2 precede RP-3.
- RP-4 depends on RP-1 through RP-3.

#### Risks And Notes

- The biggest risk is wording that still sounds optional instead of prioritized.

#### Parallelism Assessment

- No sub-agent delegation is allowed in `3.1`.
- RP-1 and RP-2 share the same contract language and stay with the Main Agent.

#### Issue List

- None.
- Blocked: No
- Exit criteria met for Iteration 3 Stage 3.1.

### Iteration 3 - Stage 3.2 - Implementation

#### RP-1 - Clarify stable docs for stage 1/2 priority reads

- Completed.
- Updated `docs/requirements/rigorous-execution-skill.md` to require stage `1` to prioritize `docs/requirements`.
- Updated `docs/specs/rigorous-execution-skill.md` to require stage `1` and `2` to prioritize stable requirement/spec docs when present.

#### RP-2 - Update skill workflow and stage references

- Completed.
- Updated `skills/rigorous-execution/SKILL.md`:
  - quick start now calls out stage `1`/`2` stable-doc priority
  - workflow now states that stage `1` prioritizes `docs/requirements`
  - workflow now states that stage `2` prioritizes `docs/specs`
- Updated `skills/rigorous-execution/references/stages.md`:
  - stage `1` now explicitly reads `docs/requirements` first when available
  - stage `2` now explicitly reads `docs/specs` first when available
  - both stages now treat stable docs as higher-priority context than code-only inference

#### RP-3 - Validate and resync the skill

- Completed.
- Validation:
  - `tools/validate-skills.ps1 -Skill rigorous-execution -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - Result: passed
- Sync:
  - `tools/sync-skills.ps1 -Skill rigorous-execution`
  - Result: updated `dist/codex/rigorous-execution` and `C:\Users\HelloWorld\.codex\skills\rigorous-execution`
- Install verification:
  - installed `SKILL.md` contains the new stage `1`/`2` docs-priority wording
  - installed `references/stages.md` contains the new stable-doc entry behavior

### Iteration 3 - Stage 3.3 - Code Review

#### Review Result

- 需求覆盖：通过
  - The requested behavior is now explicit in both the top-level skill and the stage rules.
- 架构合理性：通过
  - The docs-priority behavior lives in the stage-specific reference instead of being buried only in stable docs.
- 性能风险（N+1 / 重复计算 / 多余 I/O / 锁竞争）：通过
  - The change improves context acquisition order without adding runtime tooling or extra repository automation.
- 可读性与一致性：通过
  - The wording is short, visible, and consistent across source, stable docs, and installed copy.
- 可扩展性与配置化：通过
  - Stage-entry read order remains a reference-level rule that can evolve without destabilizing the rest of the skill.
- 稳定性与安全：通过
  - The skill now prefers written stable docs before code-only inference, reducing the chance of inventing behavior when docs exist.
- 测试覆盖情况：通过
  - Validation passed.
  - Installed copy was refreshed and spot-checked.
- 子Agent治理与审计（任务映射、上下文完整性、文件所有权、结果复核、冲突处理、记录完整性）：通过
  - No sub-agents were used in this iteration.
- Conclusion: Passed
  - No blocking review findings remain for iteration 3.

### Iteration 3 - Stage 4 - Change Archive

#### Docs Governance Check

- Used `$docs-governor` before archive completion.
- Requirements impact: updated
  - clarified `docs/requirements/rigorous-execution-skill.md`
- Specs impact: updated
  - clarified `docs/specs/rigorous-execution-skill.md`
- Lessons impact: none
  - this iteration refined reading order but did not reveal a reusable incident pattern
- Index updates required: yes
  - `docs/change/README.md`

#### Archive Result

- Change archive document created:
  - `docs/change/2026-03-23_rigorous-execution-doc-priority.md`
- Iteration 3 Stage 4 complete.

## Iteration 4 - Searchable Lessons Capture

### Initialization Refresh

- `guide.md` check:
  - `D:\project\my-ai-skills\guide.md` exists.
  - Constraint captured: every modification round must end with an automatic commit, and the commit message must use the existing English-style format.
- Confirmed skill source repo: `D:\project\my-ai-skills`
- Confirmed base branch: `main`
- Confirmed execution branch: `feat/lessons-archive-lookup`
- Confirmed execution worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Confirmed the main repo on `main` remains control-plane only; all implementation for this workflow occurs in the dedicated worktree.

### Iteration 4 - Stage 1 - Requirements Analysis

#### Goal

- Improve how `rigorous-execution` and `docs-governor` collaborate around archive, lessons, and later troubleshooting lookup.

#### Scope

- Must:
  - make stage `4` capture reusable lessons and searchable lookup hints
  - route future troubleshooting requests through `docs/lessons`
  - keep `requirements`, `specs`, `change`, and `lessons` responsibilities explicit
  - add stable requirements/specs docs for `docs-governor`
- Optional:
  - add a reusable lesson example that demonstrates the intended format
- Out of scope:
  - adding separate tooling beyond the current docs tree and skill scripts
  - relaxing any staged workflow gate

#### Use Cases

- A workflow finishes after a costly investigation and should preserve the key lesson.
- A future request asks "have we seen this before?" and should start from `docs/lessons`.
- A docs governance change now affects both the workflow controller and the docs router.

#### Functional Requirements

- `rigorous-execution` stage `4` must record `Lessons impact`, `Related lessons`, and query cues.
- `rigorous-execution` must promote reusable lessons into `docs/lessons` instead of leaving them only in `docs/change`.
- `docs-governor` must classify troubleshooting lookup as a `lessons`-first path.
- `docs-governor` lessons rules and templates must require symptoms, keywords, trigger conditions, and quick checks.
- Repository stable docs and indexes must reflect the new lessons flow.

#### Non-functional Requirements

- Keep the skill bodies concise and push detail into references.
- Keep the docs chain query-friendly without duplicating stable truth into `lessons`.
- Prefer the smallest consistent doc and script changes that make the workflow enforceable.

#### Inputs / Outputs

- Inputs:
  - current `rigorous-execution` and `docs-governor` source packages
  - existing repository docs tree
  - user direction about improving lessons capture and lookup
- Outputs:
  - updated skill source and references
  - updated stable docs and README indexes
  - one reusable lesson doc
  - one change archive for this workflow

#### Edge Cases

- `docs-governor` currently has no stable requirement/spec docs, so they must be created instead of inferred later from change history.
- A workflow may improve lessons guidance without a concrete production incident; the lesson still needs a reusable pattern rather than an invented outage.
- `change` and `lessons` must cross-link without turning `lessons` into the only source of truth.

#### Acceptance Criteria

- Both skills explicitly describe the lessons-capture and lookup behavior.
- Stable docs and indexes expose the new docs-governor and lessons contracts.
- A reusable lesson exists and is discoverable from `docs/lessons/README.md`.
- Validation and sync pass for both skills.

#### Risks

- The main risk is updating only narrative text without changing templates, index rules, and bootstrap output.

#### Issue List

- None.

### Iteration 4 - Stage 2 - Architecture Design

#### Overall Solution

- Strengthen the contract in three layers:
  - workflow layer: `rigorous-execution` stage `4`
  - docs governance layer: `docs-governor` routing, lessons rules, indexing, and templates
  - repository truth layer: stable docs, README indexes, lesson example, and archive

#### Alternatives Considered

- Alternative: create a third skill dedicated to lessons lookup.
  - Rejected because the gap is in archive governance and docs routing, not in missing skill count.
- Alternative: update only `rigorous-execution`.
  - Rejected because `docs-governor` owns the destination rules, templates, and lesson discoverability.

#### Module Responsibilities

- `skills/rigorous-execution/**`
  - enforce stage `4` capture and handoff rules
- `skills/docs-governor/**`
  - own lessons lookup, templates, indexes, and bootstrap guidance
- `docs/**`
  - hold stable truth, indexes, reusable lesson, and change archive

#### Data / Call Flow

- Workflow reaches stage `4`.
- `rigorous-execution` invokes `$docs-governor`.
- `docs-governor` decides whether lessons must be created or updated and what indexes must change.
- Archive writes `docs/change/...` and promotes reusable knowledge into `docs/lessons/...`.
- Future troubleshooting starts from `docs/lessons/README.md`, then the leaf lesson, then `docs/change` if needed.

#### Interface Drafts

- Archive fields:
  - `Lessons impact`
  - `Related lessons`
  - `经验 / 教训摘要`
  - `可复用排查线索`
- Lesson fields:
  - summary
  - lookup hints
  - symptoms
  - root cause
  - resolution
  - prevention / guardrails

#### Error Handling and Safety

- Do not treat `change` as the only home of reusable troubleshooting knowledge.
- Do not write stable behavior only into lessons; requirements/specs still carry durable truth.
- Do not leave docs-governor without stable docs once its behavior changes.

#### Performance and Testing Strategy

- Validate both skills structurally.
- Sync both installed copies.
- Run a bootstrap smoke test to confirm generated docs now expose troubleshooting guidance.

#### Extensibility Design Points

- The query-cue structure is reference-driven, so future repos can reuse it without changing the main skill bodies.
- The reusable lesson example acts as a pattern for future lessons docs.

#### Issue List

- None.

### Iteration 4 - Stage 3.1 - Planning

#### Project Goal and Current State

- Current state:
  - `rigorous-execution` checks whether a lesson may be needed, but stage `4` does not require a structured lessons handoff
  - `docs-governor` already has a `lessons` category, but direct troubleshooting lookup is not first-class in the workflow
  - `docs-governor` lacks stable requirements/specs docs in this repo
- Goal:
  - make lessons capture and later lookup explicit, query-friendly, and governed end to end

#### Docs Governance Routing Decision

- Stable capability changes:
  - `docs/requirements/`
  - `docs/specs/`
- Workflow result:
  - `docs/change/2026-03-23_lessons-archive-lookup.md`
- Reusable operational knowledge:
  - `docs/lessons/searchable-lessons-capture.md`

#### Related Requirements / Specs / Lessons

- Related requirements:
  - `docs/requirements/rigorous-execution-skill.md`
  - `docs/requirements/docs-governor-skill.md`
- Related specs:
  - `docs/specs/rigorous-execution-skill.md`
  - `docs/specs/docs-governor-skill.md`
- Related lessons:
  - `docs/lessons/searchable-lessons-capture.md`

#### Executable Task List

- [x] `LA-1` update `rigorous-execution` lessons-capture rules and templates
- [x] `LA-2` update `docs-governor` lessons routing, lookup, indexing, and bootstrap guidance
- [x] `LA-3` update stable docs, README indexes, and add the reusable lesson example
- [x] `LA-4` validate and sync both skills, then run a bootstrap smoke test
- [x] `LA-5` review and archive the workflow

#### Task Details

##### LA-1 - Update rigorous-execution archive and lessons contracts

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\plan.md`
- Goal:
  - make stage `4` enforce structured lessons capture and `docs/lessons` promotion
- Files / Modules:
  - `skills/rigorous-execution/SKILL.md`
  - `skills/rigorous-execution/references/docs-governor-integration.md`
  - `skills/rigorous-execution/references/stages.md`
  - `skills/rigorous-execution/references/templates.md`
  - `docs/requirements/rigorous-execution-skill.md`
  - `docs/specs/rigorous-execution-skill.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\rigorous-execution\SKILL.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\rigorous-execution\references\docs-governor-integration.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\rigorous-execution\references\stages.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\rigorous-execution\references\templates.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\requirements\rigorous-execution-skill.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\specs\rigorous-execution-skill.md`
- Acceptance:
  - stage `4` explicitly captures lessons impact, related lessons, and query cues
- Test Points:
  - wording is consistent across skill source, references, and stable docs
- Rollback:
  - revert the stage `4` lessons changes if the workflow is discarded

##### LA-2 - Update docs-governor lessons routing and bootstrap behavior

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\plan.md`
- Goal:
  - make troubleshooting requests start from `lessons` and make bootstrap output teach the same rule
- Files / Modules:
  - `skills/docs-governor/SKILL.md`
  - `skills/docs-governor/references/indexing-rules.md`
  - `skills/docs-governor/references/lessons-rules.md`
  - `skills/docs-governor/references/requirement-impact.md`
  - `skills/docs-governor/references/routing-rules.md`
  - `skills/docs-governor/references/taxonomy.md`
  - `skills/docs-governor/references/templates.md`
  - `skills/docs-governor/scripts/bootstrap_docs_tree.py`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\docs-governor\SKILL.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\docs-governor\references\indexing-rules.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\docs-governor\references\lessons-rules.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\docs-governor\references\requirement-impact.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\docs-governor\references\routing-rules.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\docs-governor\references\taxonomy.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\docs-governor\references\templates.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\skills\docs-governor\scripts\bootstrap_docs_tree.py`
- Acceptance:
  - docs-governor treats lessons lookup as a first-class route and bootstrap output reflects it
- Test Points:
  - routing, templates, index rules, and generated README guidance are aligned
- Rollback:
  - revert the docs-governor lessons-routing changes

##### LA-3 - Add stable docs, indexes, and reusable lessons entry

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\plan.md`
- Goal:
  - make the new lessons flow visible in repository truth and navigation
- Files / Modules:
  - `docs/README.md`
  - `docs/change/README.md`
  - `docs/lessons/README.md`
  - `docs/requirements/README.md`
  - `docs/specs/README.md`
  - `docs/requirements/docs-governor-skill.md`
  - `docs/specs/docs-governor-skill.md`
  - `docs/lessons/searchable-lessons-capture.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\README.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\change\README.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\lessons\README.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\requirements\README.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\specs\README.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\requirements\docs-governor-skill.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\specs\docs-governor-skill.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\lessons\searchable-lessons-capture.md`
- Acceptance:
  - stable docs and indexes explain the lessons-query path and include docs-governor coverage
- Test Points:
  - indexes link to the new docs
  - the lesson is discoverable from `docs/lessons/README.md`
- Rollback:
  - remove the new stable docs and lesson entry and revert the index changes

##### LA-4 - Validate, sync, and smoke test

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\plan.md`
- Goal:
  - confirm the source edits remain valid and the generated/read-installed copies reflect them
- Files / Modules:
  - `dist/codex/rigorous-execution/**`
  - `dist/codex/docs-governor/**`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\dist\codex\rigorous-execution\**`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\dist\codex\docs-governor\**`
- Acceptance:
  - validation passes for both skills
  - installed copies are refreshed
  - bootstrap smoke output contains the new troubleshooting guidance
- Test Points:
  - `tools/validate-skills.ps1 -Skill rigorous-execution`
  - `tools/validate-skills.ps1 -Skill docs-governor`
  - `tools/sync-skills.ps1 -Skill rigorous-execution`
  - `tools/sync-skills.ps1 -Skill docs-governor`
  - bootstrap smoke test with a temporary target directory
- Rollback:
  - remove regenerated dist/install copies and revert source edits if needed

##### LA-5 - Review and archive iteration 4

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\plan.md`
- Goal:
  - review the new lessons contract and archive the completed workflow
- Files / Modules:
  - `plan.md`
  - `docs/change/2026-03-23_lessons-archive-lookup.md`
  - `docs/change/README.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\plan.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\change\2026-03-23_lessons-archive-lookup.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\change\README.md`
- Acceptance:
  - review and archive capture the lessons-query behavior and related docs changes
- Test Points:
  - archive exists and maps back to `LA-1` through `LA-5`
- Rollback:
  - revert the iteration `4` archive if the round is discarded

#### Dependencies

- `LA-1`, `LA-2`, and `LA-3` precede `LA-4`.
- `LA-5` depends on `LA-1` through `LA-4`.

#### Risks and Notes

- The highest risk is inconsistent wording between the two skills and the repository truth layer.

#### Parallelism Assessment

- No sub-agent delegation is allowed in `3.1`.
- The write set overlaps across both skills and the shared docs indexes, so the Main Agent keeps ownership.

#### Issue List

- None.
- Blocked: No
- Exit criteria met for Iteration 4 Stage 3.1.

### Iteration 4 - Stage 3.2 - Implementation

#### LA-1 - Update rigorous-execution archive and lessons contracts

- Completed.
- Updated `skills/rigorous-execution/SKILL.md` to bring `docs/lessons` into the explicit stage `4` archive contract.
- Updated `skills/rigorous-execution/references/stages.md`, `docs-governor-integration.md`, and `templates.md` so archive output now records lessons impact, related lessons, and reusable lookup cues.
- Updated stable docs for `rigorous-execution` so the new stage `4` behavior is part of repository truth.

#### LA-2 - Update docs-governor lessons routing and bootstrap behavior

- Completed.
- Updated `skills/docs-governor/SKILL.md` and references so troubleshooting lookup starts from `lessons`.
- Updated lessons rules, routing rules, taxonomy, indexing rules, requirement-impact guidance, and templates to make lessons query-friendly and discoverable.
- Updated `skills/docs-governor/scripts/bootstrap_docs_tree.py` so generated docs now teach the troubleshooting-first path.

#### LA-3 - Add stable docs, indexes, and reusable lessons entry

- Completed.
- Added stable requirements/specs docs for `docs-governor`.
- Updated root and category README indexes to expose the new troubleshooting path and docs-governor docs.
- Added `docs/lessons/searchable-lessons-capture.md` as the reusable lesson example for this pattern.

#### LA-4 - Validate, sync, and smoke test

- Completed.
- Validation:
  - `tools/validate-skills.ps1 -Skill rigorous-execution -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
  - `tools/validate-skills.ps1 -Skill docs-governor -PythonExe C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe`
- Sync:
  - `tools/sync-skills.ps1 -Skill rigorous-execution`
  - `tools/sync-skills.ps1 -Skill docs-governor`
- Bootstrap smoke test:
  - `C:\Users\HelloWorld\.conda\envs\ai_envs\python.exe skills/docs-governor/scripts/bootstrap_docs_tree.py tmp\docs-governor-smoke --module api --force`

### Iteration 4 - Stage 3.3 - Code Review

#### Review Result

- 需求覆盖：通过
  - The workflow now captures reusable lessons in stage `4` and makes later lookup explicit.
- 架构合理性：通过
  - Responsibilities remain split cleanly between workflow control, docs governance, and repository truth.
- 性能风险（N+1 / 重复计算 / 多余 I/O / 锁竞争）：通过
  - The changes are doc and script level only and do not add avoidable repeated work beyond required archive capture.
- 可读性与一致性：通过
  - The new lessons language is aligned across skill source, references, stable docs, and indexes.
- 可扩展性与配置化：通过
  - Lessons lookup remains reference-driven and reusable across repositories bootstrapped by docs-governor.
- 稳定性与安全：通过
  - The docs chain now makes it harder to lose reusable troubleshooting knowledge in change archives alone.
- 测试覆盖情况：通过
  - Both skills validated and synced successfully.
  - The bootstrap smoke test confirmed the generated guidance.
- 子Agent治理与审计（任务映射、上下文完整性、文件所有权、结果复核、冲突处理、记录完整性）：通过
  - No sub-agents were used in this iteration.
- Conclusion: Passed
  - No blocking review findings remain for iteration 4.

### Iteration 4 - Stage 4 - Change Archive

#### Docs Governance Check

- Used `$docs-governor` before archive completion.
- Requirements impact: updated
  - updated `docs/requirements/rigorous-execution-skill.md`
  - added `docs/requirements/docs-governor-skill.md`
- Specs impact: updated
  - updated `docs/specs/rigorous-execution-skill.md`
  - added `docs/specs/docs-governor-skill.md`
- Lessons impact: updated
  - added `docs/lessons/searchable-lessons-capture.md`
  - updated `docs/lessons/README.md`
- Index updates required: yes
  - `docs/README.md`
  - `docs/change/README.md`
  - `docs/lessons/README.md`
  - `docs/requirements/README.md`
  - `docs/specs/README.md`

#### Archive Result

- Change archive document created:
  - `docs/change/2026-03-23_lessons-archive-lookup.md`
- Iteration 4 Stage 4 complete.

## Iteration 5 - Requirements And Specs Responsibility Clarity

### Initialization Refresh

- `guide.md` check:
  - `D:\project\my-ai-skills\guide.md` exists.
  - Constraint remains active: each modification round must end with an automatic commit using the established English commit-message format.
- Confirmed skill source repo: `D:\project\my-ai-skills`
- Confirmed base branch: `main`
- Confirmed execution branch: `feat/lessons-archive-lookup`
- Confirmed execution worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Confirmed the main repo on `main` remains control-plane only; documentation edits for this round stay in the dedicated worktree.

### Iteration 5 - Stage 1 - Requirements Analysis

#### Goal

- Make the `requirements` and `specs` responsibility split explicit enough in stable docs that the documentation system remains self-explanatory.

#### Scope

- Must:
  - explain what `requirements` own
  - explain what `specs` own
  - explain the update order when both change
  - place the durable rule in stable requirement/spec docs, not only in indexes or chat context
- Optional:
  - tighten category README wording to match the stable docs
- Out of scope:
  - changing skill source or routing references unless the stable docs prove insufficient
  - changing the lessons workflow from iteration 4

#### Use Cases

- A future editor needs to decide whether a new document belongs in `requirements` or `specs`.
- A workflow needs to record requirement/spec impact without relying on prior conversation context.
- A reader wants to understand the category split from the stable docs alone.

#### Functional Requirements

- The repository docs must define `requirements` as the home of long-lived intent, scope, scenarios, and acceptance criteria.
- The repository docs must define `specs` as the home of technical contracts, structures, constraints, and guardrails.
- The docs must explain that when both change, `requirements` update first and `specs` follow.
- The docs must make clear that `plan`, `change`, and `lessons` do not replace stable truth.

#### Non-functional Requirements

- Readability:
  - a reader should understand the split without needing taxonomy or chat history first
- Maintainability:
  - the same responsibility rule should not drift across README and stable docs
- Minimality:
  - prefer stable-doc clarification over skill-source changes

#### Inputs / Outputs

- Inputs:
  - current `docs/requirements/README.md`
  - current `docs/specs/README.md`
  - current `docs/requirements/docs-governor-skill.md`
  - current `docs/specs/docs-governor-skill.md`
- Outputs:
  - clarified README guidance
  - clarified stable requirement/spec docs
  - one change archive entry for this iteration

#### Edge Cases

- README files can summarize the split, but must not become the only durable source of the rule.
- The stable docs must stay aligned with the existing taxonomy and requirement-impact rules.

#### Acceptance Criteria

- The category README files explain the quick decision boundary.
- The `docs-governor` stable requirement/spec docs explain the durable responsibility split and update order.
- A future editor can route a document correctly by reading the stable docs without chat-only context.

#### Risks

- The main risk is over-relying on README wording while leaving the stable docs too thin.

#### Issue List

- None.

### Iteration 5 - Stage 2 - Architecture Design

#### Overall Solution

- Keep the change at the repository truth layer:
  - category README files give the quick classifier
  - `docs-governor` requirement doc states the need for self-explanatory boundaries
  - `docs-governor` spec doc states the durable technical contract for the split

#### Alternatives Considered

- Alternative: update only README files.
  - Rejected because README is navigation, not enough as the only durable truth.
- Alternative: update only the spec doc.
  - Rejected because the need for self-explanation is itself a long-lived requirement, not just a technical contract.

#### Module Responsibilities

- `docs/requirements/README.md`
  - quick entry guidance for `requirements`
- `docs/specs/README.md`
  - quick entry guidance for `specs`
- `docs/requirements/docs-governor-skill.md`
  - stable requirement that the docs system remains self-explanatory
- `docs/specs/docs-governor-skill.md`
  - stable contract for the `requirements` versus `specs` split

#### Data / Call Flow

- Reader starts with category README or stable docs.
- README gives the short classifier.
- Stable requirement/spec docs provide the durable explanation and sequencing rule.
- Future impact checks use those stable docs instead of chat memory.

#### Interface Drafts

- `requirements` shorthand:
  - `why / what / scope / acceptance`
- `specs` shorthand:
  - `how / contract / constraints / guardrails`

#### Error Handling and Safety

- Do not move the only copy of the boundary into README files.
- Do not redefine the split in a way that conflicts with taxonomy or requirement-impact guidance.

#### Performance and Testing Strategy

- Use doc consistency checks only.
- No skill validation run is required if no skill source package changes.

#### Extensibility Design Points

- Future taxonomy changes can now update a small, explicit set of stable docs instead of leaving the rule implicit.

#### Issue List

- None.

### Iteration 5 - Stage 3.1 - Planning

#### Project Goal and Current State

- Current state:
  - category README files explain the split only briefly
  - `docs-governor` stable requirement/spec docs mention routing responsibilities but do not fully spell out the `requirements` versus `specs` boundary
- Goal:
  - make the durable docs themselves explain the boundary and update order

#### Docs Governance Routing Decision

- Stable truth:
  - `docs/requirements/README.md`
  - `docs/specs/README.md`
  - `docs/requirements/docs-governor-skill.md`
  - `docs/specs/docs-governor-skill.md`
- Workflow result:
  - `docs/change/2026-03-24_requirements-specs-responsibility-clarity.md`

#### Related Requirements / Specs / Lessons

- Related requirements:
  - `docs/requirements/docs-governor-skill.md`
- Related specs:
  - `docs/specs/docs-governor-skill.md`
- Related lessons:
  - none

#### Executable Task List

- [x] `RS-1` clarify `requirements` responsibility in stable docs
- [x] `RS-2` clarify `specs` responsibility in stable docs
- [x] `RS-3` review and archive the iteration

#### Task Details

##### RS-1 - Clarify requirements responsibility and boundary

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\plan.md`
- Goal:
  - explain what belongs in `requirements` and why that rule is durable
- Files / Modules:
  - `docs/requirements/README.md`
  - `docs/requirements/docs-governor-skill.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\requirements\README.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\requirements\docs-governor-skill.md`
- Acceptance:
  - the docs define `requirements` as long-lived intent, scope, scenarios, and acceptance
- Test Points:
  - the short README guidance and stable requirement doc do not conflict
- Rollback:
  - revert the `requirements` clarification changes

##### RS-2 - Clarify specs responsibility and boundary

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\plan.md`
- Goal:
  - explain what belongs in `specs`, how it differs from `requirements`, and what update order applies
- Files / Modules:
  - `docs/specs/README.md`
  - `docs/specs/docs-governor-skill.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\specs\README.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\specs\docs-governor-skill.md`
- Acceptance:
  - the docs define `specs` as long-lived technical contract and explain sequencing when both categories change
- Test Points:
  - the short README guidance and stable spec doc do not conflict
- Rollback:
  - revert the `specs` clarification changes

##### RS-3 - Review and archive iteration 5

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup`
- Plan Path: `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\plan.md`
- Goal:
  - review the clarification round and archive it
- Files / Modules:
  - `plan.md`
  - `docs/change/README.md`
  - `docs/change/2026-03-24_requirements-specs-responsibility-clarity.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\plan.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\change\README.md`
  - `D:\project\MyFlowHub3\worktrees\my-ai-skills_feat-lessons-archive-lookup\docs\change\2026-03-24_requirements-specs-responsibility-clarity.md`
- Acceptance:
  - archive explains the new self-explanatory boundary and maps back to `RS-1` through `RS-3`
- Test Points:
  - archive exists and the reverse-chronological change index is updated
- Rollback:
  - revert the iteration 5 archive if the round is discarded

#### Dependencies

- `RS-1` and `RS-2` precede `RS-3`.

#### Risks and Notes

- The highest risk is leaving the stable docs too abstract while the README wording becomes the only practical explanation.

#### Parallelism Assessment

- No sub-agent delegation is allowed in `3.1`.
- The write set is small and tightly coupled, so the Main Agent keeps ownership.

#### Issue List

- None.
- Blocked: No
- Exit criteria met for Iteration 5 Stage 3.1.

### Iteration 5 - Stage 3.2 - Implementation

#### RS-1 - Clarify requirements responsibility and boundary

- Completed.
- Updated `docs/requirements/README.md` with a quick classifier for when `requirements` should be used and how it differs from `specs`.
- Updated `docs/requirements/docs-governor-skill.md` so self-explanatory category boundaries are now a stable requirement.

#### RS-2 - Clarify specs responsibility and boundary

- Completed.
- Updated `docs/specs/README.md` with a quick classifier for when `specs` should be used and how it differs from `requirements`.
- Updated `docs/specs/docs-governor-skill.md` so the `requirements` versus `specs` split and update order are now explicit technical contracts.

### Iteration 5 - Stage 3.3 - Code Review

#### Review Result

- 需求覆盖：通过
  - The stable docs now state both the user-facing need for self-explanation and the technical contract for the split.
- 架构合理性：通过
  - The change stays at the stable-doc layer and does not expand unnecessarily into skill source.
- 性能风险（N+1 / 重复计算 / 多余 I/O / 锁竞争）：通过
  - This round is documentation-only and adds no runtime or tool overhead.
- 可读性与一致性：通过
  - README files and stable docs now use the same `why / what` versus `how / contract` framing.
- 可扩展性与配置化：通过
  - Future taxonomy changes now have a clear stable-doc surface to update.
- 稳定性与安全：通过
  - The category split is less likely to drift into chat-only context or archives.
- 测试覆盖情况：通过
  - `git diff --check` passed.
  - The changed docs were re-read to confirm alignment.
- 子Agent治理与审计（任务映射、上下文完整性、文件所有权、结果复核、冲突处理、记录完整性）：通过
  - No sub-agents were used in this iteration.
- Conclusion: Passed
  - No blocking review findings remain for iteration 5.

### Iteration 5 - Stage 4 - Change Archive

#### Docs Governance Check

- Used `$docs-governor` before archive completion.
- Requirements impact: updated
  - updated `docs/requirements/README.md`
  - updated `docs/requirements/docs-governor-skill.md`
- Specs impact: updated
  - updated `docs/specs/README.md`
  - updated `docs/specs/docs-governor-skill.md`
- Lessons impact: none
  - this iteration clarified stable category boundaries but did not introduce a new reusable troubleshooting pattern
- Index updates required: yes
  - `docs/change/README.md`

#### Archive Result

- Change archive document created:
  - `docs/change/2026-03-24_requirements-specs-responsibility-clarity.md`
- Iteration 5 Stage 4 complete.
