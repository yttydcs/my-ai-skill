# Plan - m-skill-phase-rename

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `refactor/m-skill-phase-rename`
- Base: `main`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\docs`
- Code Repos:
  - `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename`
- Current Stage: `4 - Archive complete; awaiting workflow-end confirmation`
- Planning skill: `$m-plan`
- Docs governance skill: `$m-docs`
- Discussion / optional research skill: `$m-discuss`

## Stage Records

### Initialization

- `guide.md`:
  - Present at `D:\project\my-ai-skills\guide.md`.
  - Active rule: every modification round must be committed automatically, with an English commit message following the existing history format.
- Main repo path:
  - `D:\project\my-ai-skills`
  - Control-plane only for this workflow.
- Dedicated branch:
  - `refactor/m-skill-phase-rename`
- Dedicated worktree:
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename`
- Baseline:
  - `main` at `eaa43d8 docs: archive private docs governance`
  - `main` is ahead of `origin/main` by 3 local commits from the prior completed workflow.
  - No remote push, publication, or backup action is in scope.
- Participating modules:
  - `skills/m-autoflow/**`
  - `skills/m-autoflow-plan/**`
  - `skills/m-autoflow-execute/**`
  - `skills/m-autoflow-test/**`
  - `skills/m-autoflow-archive/**`
  - `skills/m-autoflow-research/**`
  - new `skills/m-discuss/**`
  - new `skills/m-plan/**`
  - new `skills/m-execute/**`
  - new `skills/m-test/**`
  - new `skills/m-archive/**`
  - possible new `skills/m-research/**` only if retained as a public phase
  - `manifests/m-autoflow*.json`
  - new `manifests/m-*.json` for renamed phase skills
  - `docs/intake/**`
  - `docs/features/**`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
  - `docs/decisions/**`
  - `docs/change/**`
  - `tools/validate-skills.ps1`
  - `tools/sync-skills.ps1`

### Optional Research - Source-backed Planning Input

#### Research Question

How should the renamed `m-*` workflow skill set separate discussion, planning, execution, review, and archive responsibilities while allowing current-best-practice research and avoiding duplicated instructions?

#### Sources Used

- Design Council Double Diamond: https://www.designcouncil.org.uk/our-resources/framework-for-innovation/
- Atlassian product requirements guidance: https://www.atlassian.com/agile/product-management/requirements
- GitHub reusable workflows documentation: https://docs.github.com/en/actions/how-tos/sharing-automations/reusing-workflows
- Microsoft ADR guidance: https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record

#### Confirmed Findings

- The Double Diamond model supports a discover/define split before solution delivery. This maps well to a `discuss` phase that explores broadly, then narrows into a coherent requirement.
- Product requirement guidance supports collecting purpose, context, assumptions, options, acceptance, and constraints before execution planning. This maps to `discuss` producing a decision-ready brief and `plan` producing an execution-ready architecture plan.
- Reusable workflow guidance supports factoring repeated process into a shared callable unit instead of duplicating it across every caller. This maps to keeping phase skills thin and moving repeated rules into shared references.
- ADR guidance supports recording hard-to-reverse naming and workflow-structure decisions as a decision record, not burying them only in `plan.md` or `docs/change`.

#### Conflicts / Uncertainties

- External sources do not define Codex skill naming or invocation behavior; that is governed by this repository's validator, manifests, local install flow, and the user's preferred command surface.
- The user explicitly wants shorter phase names, so backward-compatible alias packages are a product decision, not an external best-practice requirement.

#### Planning Implications

- Add a first-class `m-discuss` phase before `m-plan`.
- Move worktree creation into `m-discuss` when the full workflow starts there.
- Keep `m-plan` able to create or confirm a worktree when called directly, for practical fallback.
- Rename phase skills to canonical short names:
  - `m-autoflow-plan` -> `m-plan`
  - `m-autoflow-execute` -> `m-execute`
  - `m-autoflow-test` -> `m-test`
  - `m-autoflow-archive` -> `m-archive`
  - `m-autoflow-research` -> fold into `m-discuss` unless a separate public `m-research` entry is explicitly retained.
- Keep `m-autoflow` as the umbrella collection and route through phase skills by reference, not by duplicating full instructions.
- Add an ADR for the naming and phase-boundary decision.

### Stage 1 - Requirements Analysis

#### Goal

Redefine the `m-autoflow` skill group so phase skills have short canonical names, `m-autoflow` becomes an umbrella collection, repeated instructions are centralized through references, and a new `m-discuss` phase handles product/technical discovery before architecture planning.

#### Scope

Must:

- Add canonical short phase skills:
  - `m-discuss`
  - `m-plan`
  - `m-execute`
  - `m-test`
  - `m-archive`
- Keep `m-autoflow` as the umbrella entry that lets the user invoke the whole workflow without typing each phase command.
- Remove `autoflow` from phase skill names and user-facing prompts.
- Add `m-discuss` as the first phase:
  - product-manager-like discovery with strong technical judgment
  - brainstorm options and alternatives
  - clarify vague requirements
  - challenge or reject unreasonable requirements and offer better proposals
  - optionally perform online research when current best practices, external facts, vendors, libraries, or market/product comparisons matter
  - create or confirm the dedicated worktree early in the workflow
  - produce a handoff artifact for `m-plan`
- Redefine `m-plan` as the architecture and execution-planning phase:
  - senior architect / experienced programmer posture
  - consume `m-discuss` output when present
  - reject unreasonable or unsafe requirements instead of planning blindly
  - produce the executable task plan with acceptance, tests, rollback, and execution scope
- Reduce duplication:
  - keep phase `SKILL.md` files concise
  - route repeated workflow rules through shared references
  - make `m-autoflow` list and route to phases instead of repeating phase details
- Update stable docs, manifests, references, agents metadata, validation/sync commands, and local install output.
- Preserve private docs and publication boundaries:
  - no remote changes
  - no push
  - no backup strategy decisions

Should:

- Add a feature dossier for the workflow skill set so current user-visible phase behavior is not split only across requirements/specs.
- Add an ADR for the phase renaming, `m-discuss`, and umbrella/reference model.
- Keep historical `docs/change/*autoflow*` records unchanged as historical evidence.

Out of scope:

- Pushing `main` or any branch.
- Creating or configuring external docs remotes.
- Migrating external user projects to the new workflow.
- Rewriting historical change archives only to replace old names.
- Implementing compatibility aliases for old phase skill names unless the user explicitly wants that tradeoff.

#### Use Cases

- The user invokes `$m-autoflow` and gets the complete workflow:
  - discuss -> plan -> execute -> test/review -> archive/closeout
- The user invokes `$m-discuss` to explore a vague idea, compare approaches, search current best practices when needed, and shape requirements.
- The user invokes `$m-plan` after discussion or with already-clear requirements to create an execution plan.
- The user invokes `$m-execute`, `$m-test`, or `$m-archive` for a specific confirmed phase.
- The user no longer needs to type long phase names such as `$m-autoflow-plan`.
- Future maintainers update shared phase rules once instead of copying the same stage gates into every phase skill.

#### Functional Requirements

- `m-autoflow` must remain a valid skill package and umbrella entry point.
- `m-autoflow` must depend on and reference the new short phase skills.
- `m-discuss` must be a valid skill package with manifest and installed output.
- `m-plan`, `m-execute`, `m-test`, and `m-archive` must be valid skill packages with manifests and installed output.
- Old canonical phase packages must be removed or converted according to the approved compatibility choice.
- `m-discuss` must create or confirm the dedicated branch/worktree when it starts the full workflow.
- `m-plan` must not assume discussion always happened; it must either consume a discussion artifact, create/confirm the worktree directly, or record a blocker.
- `m-discuss` must explicitly distinguish facts, assumptions, open questions, rejected ideas, viable options, and recommended direction.
- `m-discuss` must use online research only when it is useful for current external facts or best practices, and it must cite sources.
- `m-plan` must be allowed to reject unreasonable, unsafe, contradictory, or under-specified requirements and route back to `m-discuss`.
- Phase skills must reference shared instructions instead of duplicating full workflow text.
- Validation and sync tooling must work with the new canonical names.
- Installed old phase skill directories must not remain as stale canonical entries after sync unless alias support is intentionally retained.

#### Non-functional Requirements

- Maintainability:
  - shared workflow rules should have one canonical home where possible
  - phase skills should be small, loadable, and easy to audit
- Backward clarity:
  - old historical archives may mention `m-autoflow-*` because they describe past state
  - current stable docs and source must use the new canonical names
- Safety:
  - no implementation without confirmed plan
  - no merge or cleanup before archive closeout
  - no remote or backup changes
- Traceability:
  - create intake, feature, requirements, specs, decision, plan, and later change links
- Validation:
  - every new skill validates and syncs
  - old phase names are either absent or clearly documented aliases

#### Inputs / Outputs

Inputs:

- User request in this workflow.
- Existing `m-autoflow` stable docs, source packages, manifests, and local tooling.
- Prior change archives for prefix rename, phase split, execution-scope split, and private docs governance.
- External research sources listed above.

Outputs:

- Root `plan.md` in this worktree.
- Intake record for this request.
- Later implementation changes after approval:
  - updated stable docs
  - new/renamed skill packages and manifests
  - updated references and agents metadata
  - synced local installed skills
  - change archive after execution/review

#### Edge Cases

- Direct `$m-plan` invocation without prior `$m-discuss`.
- Existing users invoking `$m-autoflow-plan` after rename.
- Existing local install directories for old phase skills.
- `m-autoflow` depending on new phase skills while also hosting shared references.
- Search or research being overused by `m-discuss`.
- Requirements that are unreasonable but the user asks to plan anyway.
- Historical docs containing old names.
- This session's available skill list may still show old names until the local skill index refreshes.

#### Acceptance Criteria

- The plan explicitly states the new canonical public phase names.
- The plan defines the `m-discuss` responsibility and how it hands off to `m-plan`.
- The plan defines `m-plan` as architecture/execution planning and requires it to reject bad requirements.
- The plan defines how `m-autoflow` remains an umbrella collection without duplicating phase bodies.
- The plan includes a compatibility decision point for old phase skill names.
- The plan maps every known task to an immediate execution scope or a deferred scope.
- The next execution phase can proceed without needing chat-only context.

#### Risks

- Removing old phase skill names can break muscle memory and existing explicit invocations.
- Keeping old aliases can clutter skill discovery and undermine the user's goal of shorter names.
- Moving too much shared logic into `m-autoflow` may conflict with the user's desire for `m-autoflow` to be only a collection.
- Moving shared logic into every phase skill would create the duplication the user wants to avoid.
- Renaming package directories can leave stale installed directories if sync cleanup is incomplete.
- A too-powerful `m-discuss` could blur into planning or implementation unless its exit gate is explicit.

#### Issue List

- Compatibility with old names is a product choice:
  - default plan: remove old phase packages as canonical entries and do not retain alias packages in the next execution phase.
  - alternative: keep temporary compatibility stubs for one workflow cycle.
- Blocked: No.
- Exit criteria met for Stage 1.

### Stage 2 - Architecture Design

#### Overall Solution

Create a short-name phase architecture:

```text
m-autoflow
  umbrella / collection / router
  references shared workflow primitives

m-discuss
  discovery, brainstorming, research, requirement shaping, worktree initialization

m-plan
  architecture, task decomposition, execution plan, rejection of bad requirements

m-execute
  approved Task ID implementation and lightweight validation

m-test
  optional heavy validation, review, usability/security/performance checks

m-archive
  docs/change, lessons, workflow-end confirmation, merge and cleanup
```

Recommended canonical direction:

- `m-autoflow` remains public and stable as the whole-workflow command.
- `m-discuss`, `m-plan`, `m-execute`, `m-test`, and `m-archive` become the canonical split-phase commands.
- `m-autoflow-research` is not retained as a public canonical phase by default; its current research rules move into `m-discuss/references/research.md` or a shared reference used only by `m-discuss`.
- Historical `m-autoflow-*` phase packages are removed from source/manifests/install during execution unless the user requests compatibility aliases before approval.

#### Alternatives Considered

- Keep old `m-autoflow-*` phase names:
  - Rejected for the default plan because the user explicitly wants shorter `m-*` names.
- Rename phases but keep old alias packages:
  - Useful for compatibility, but it increases discovery noise and duplicated maintenance.
  - Deferred unless the user requests it before execution.
- Create a separate `m-core` or `m-workflow-core` shared library skill:
  - Clean separation, but adds a new abstraction and another install surface.
  - Rejected for this iteration unless `m-autoflow` cannot remain a reasonable shared-reference host.
- Keep shared references in `m-autoflow/references`:
  - Chosen for this iteration because `m-autoflow` is the collection skill and already owns common references.
  - Phase skills should reference those shared files rather than duplicate them.
- Put all research in `m-plan`:
  - Rejected because the user wants research and brainstorming before architectural planning.

#### Module Responsibilities

- `skills/m-autoflow/SKILL.md`
  - Thin umbrella entry.
  - Lists canonical phase order and references phase skill packages.
  - Avoids detailed duplicate phase instructions.
- `skills/m-autoflow/references/*.md`
  - Shared workflow primitives: initialization, docs integration, templates, sub-agent governance, stage naming, closeout basics.
  - Updated to use new canonical phase names.
- `skills/m-discuss/**`
  - New discovery phase.
  - Owns optional research, brainstorming, requirement shaping, feasibility challenge, and early worktree setup.
- `skills/m-plan/**`
  - Renamed planning phase.
  - Owns architecture, execution-scope split, task design, and rejection/reroute to discuss.
- `skills/m-execute/**`
  - Renamed execution phase.
- `skills/m-test/**`
  - Renamed heavy validation/review phase.
- `skills/m-archive/**`
  - Renamed archive/closeout phase.
- `manifests/*.json`
  - New names, dependencies, source/dist paths.
- `agents/openai.yaml`
  - New display names and default prompts.
- `docs/requirements/m-autoflow-skill.md`
  - Stable behavior requirements for umbrella and phase skills.
- `docs/specs/m-autoflow-skill.md`
  - Package, manifest, routing, validation, and install contracts.
- `docs/features/m-autoflow-workflow.md`
  - Current user-visible workflow behavior by phase.
- `docs/decisions/YYYY-MM-DD_m-skill-phase-naming.md`
  - Accepted architecture decision for names, discuss, and reference-driven umbrella.
- `docs/intake/YYYY-MM-DD_m-skill-phase-rename.md`
  - Original request evidence for this workflow.

#### Data / Call Flow

Full workflow:

1. User invokes `$m-autoflow`.
2. `m-autoflow` routes to `$m-discuss`.
3. `m-discuss`:
   - reads intake/features/requirements/specs/decisions as useful
   - creates or confirms branch/worktree
   - explores options and constraints
   - performs online research only when useful and cites sources
   - writes or updates a discussion section/artifact in the active worktree
4. User confirms direction or provides clarifications.
5. `m-plan` consumes discussion output and stable docs.
6. `m-plan` creates the executable `plan.md`.
7. After approval, `m-execute` implements mapped Task IDs.
8. `m-test` runs or records a justified skip of heavy validation.
9. `m-archive` writes `docs/change`, updates lessons if needed, asks whether to end workflow, then merges/cleans only after confirmation.

Direct phase workflow:

- `$m-discuss` can stop after discovery.
- `$m-plan` can create or confirm the worktree if `m-discuss` was skipped, but it must record that discussion was skipped or not needed.
- `$m-execute`, `$m-test`, and `$m-archive` require the relevant prior artifacts.

#### Interface Drafts

`m-discuss` output should include:

- problem / opportunity
- original request and source
- assumptions
- open questions
- user goals and non-goals
- candidate options
- rejected options and why
- feasibility / technical constraints
- research summary with citations when research was used
- recommended direction
- worktree / branch / docs root confirmation
- handoff criteria for `m-plan`

`m-plan` output should include:

- architecture decision summary
- accepted / rejected requirements
- task IDs
- execution scope split
- write sets
- acceptance
- test points
- rollback
- dependency and parallelism assessment

#### Error Handling and Safety

- If `m-discuss` cannot identify a sensible requirement, it should stop with questions rather than inventing scope.
- If `m-discuss` finds the user request unreasonable, it should reject the request clearly and propose safer alternatives.
- If `m-plan` receives an unreasonable or contradictory requirement, it should return to `m-discuss` or block rather than forcing an implementation plan.
- If `m-autoflow` cannot find a needed phase skill, it should report the missing package and stop instead of falling back silently.
- If renamed skill sync leaves old installed directories behind, execution must clean or report them explicitly.
- If backward compatibility aliases are requested, they must be thin stubs that point to canonical skills and must not duplicate rules.

#### Performance and Testing Strategy

- Use file-system rename/move operations carefully and verify every package with repo tooling.
- Validation:
  - `tools\validate-skills.ps1 -Skill m-autoflow`
  - `tools\validate-skills.ps1 -Skill m-discuss`
  - `tools\validate-skills.ps1 -Skill m-plan`
  - `tools\validate-skills.ps1 -Skill m-execute`
  - `tools\validate-skills.ps1 -Skill m-test`
  - `tools\validate-skills.ps1 -Skill m-archive`
  - optional old-alias validation only if aliases are retained
  - `git diff --check`
- Sync:
  - `tools\sync-skills.ps1 -Skill m-autoflow`
  - `tools\sync-skills.ps1 -Skill m-discuss`
  - `tools\sync-skills.ps1 -Skill m-plan`
  - `tools\sync-skills.ps1 -Skill m-execute`
  - `tools\sync-skills.ps1 -Skill m-test`
  - `tools\sync-skills.ps1 -Skill m-archive`
- Install cleanup:
  - remove stale installed directories for old phase names only after new canonical skills validate and sync.

#### Extensibility Design Points

- Keep future phase additions as new `m-*` companions rather than expanding `m-autoflow` content.
- Keep shared rules in references and load them by phase.
- Allow `m-discuss` to grow discovery tools without pushing that complexity into `m-plan`.
- Allow compatibility stubs later if real usage proves old names need a transition period.

#### Issue List

- None blocking.
- Exit criteria met for Stage 2.

### Stage 3.1 - Planning

#### Project Goal and Current State

- Goal:
  - Plan the rename and redefinition of the `m-autoflow` skill group into a short-name, reference-driven phase system with a new `m-discuss` phase.
- Current state:
  - `m-autoflow` is the umbrella.
  - Split phase skills are named `m-autoflow-plan`, `m-autoflow-execute`, `m-autoflow-test`, `m-autoflow-archive`, and `m-autoflow-research`.
  - Existing phase skills duplicate some workflow detail in `SKILL.md` descriptions and references.
  - Worktree creation currently belongs to planning/initialization; the user wants it to start during discussion when discussion is used.

#### Docs Governance Routing Decision

Used `$m-docs` to classify the planning outputs and future stable-doc impact.

- Original request evidence:
  - `docs/intake/2026-07-08_m-skill-phase-rename.md`
- Current user-visible behavior:
  - add or update `docs/features/m-autoflow-workflow.md` during execution
- Durable capability intent:
  - update `docs/requirements/m-autoflow-skill.md`
- Technical contract:
  - update `docs/specs/m-autoflow-skill.md`
- Architecture decision:
  - add `docs/decisions/2026-07-08_m-skill-phase-naming.md`
- Workflow result:
  - later create `docs/change/2026-07-08_m-skill-phase-rename.md`
- Lessons:
  - no lesson known at planning time

#### Related Intake / Features / Requirements / Specs / Decisions / Lessons

- Related intake:
  - `docs/intake/2026-07-08_m-skill-phase-rename.md`
  - `docs/intake/2026-07-08_docs-private-governance.md`
- Related features:
  - `docs/features/README.md`
  - `docs/features/m-autoflow-workflow.md`
- Related requirements:
  - `docs/requirements/m-autoflow-skill.md`
- Related specs:
  - `docs/specs/m-autoflow-skill.md`
- Related decisions:
  - `docs/decisions/2026-07-08_private-docs-root-and-feature-first-governance.md`
  - `docs/decisions/2026-07-08_m-skill-phase-naming.md`
- Related lessons:
  - `docs/lessons/skill-frontmatter-yaml-colon.md`

#### Stable Docs Impact

- Intake impact: add
- Feature impact: add
- Requirements impact: clarify
- Specs impact: clarify
- Decision impact: add
- Lessons impact: updated during archive

#### Executable Task List

- [x] `MSR-1` Update stable docs and records for the new phase model.
- [x] `MSR-2` Rename canonical phase skill packages and manifests.
- [x] `MSR-3` Add `m-discuss` and fold optional research behavior into it.
- [x] `MSR-4` Refactor `m-autoflow` into a thin umbrella/reference-driven collection.
- [x] `MSR-5` Update references, prompts, dependency names, and current docs references.
- [x] `MSR-6` Validate, sync, and clean stale installed phase skill directories.
- [x] `MSR-7` Commit approved execution changes locally.
- [x] `MSR-8` Review and archive this workflow.
- [ ] `MSR-9` Decide whether to push or publish the local branch.
- [ ] `MSR-10` Add old-name compatibility aliases.

#### Execution Scope After Approval

##### Will Execute

- `MSR-1` - required because this changes stable workflow behavior.
- `MSR-2` - required to make `m-plan`, `m-execute`, `m-test`, and `m-archive` canonical.
- `MSR-3` - required to add the new discussion/discovery phase.
- `MSR-4` - required to make `m-autoflow` the collection entry instead of a duplicate rule body.
- `MSR-5` - required to avoid stale references to old phase names in current source and stable docs.
- `MSR-6` - required to prove the new names validate/sync and to avoid stale installed old names.
- `MSR-7` - required by `guide.md`.

##### Will Not Execute Now

- `MSR-8` - separate review/archive phase after execution and validation.
- `MSR-9` - out of scope and user-owned; do not push or publish automatically.
- `MSR-10` - deferred; compatibility aliases add clutter and are not the default unless the user requests them before execution.

#### Task Details

##### MSR-1 - Update stable docs and records for the new phase model

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\plan.md`
- Goal:
  - Make durable docs describe the new canonical names, `m-discuss`, and the `m-autoflow` umbrella/reference model before source behavior depends on it.
- Files / Modules:
  - `docs/intake/2026-07-08_m-skill-phase-rename.md`
  - `docs/intake/README.md`
  - `docs/features/m-autoflow-workflow.md`
  - `docs/features/README.md`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
  - `docs/decisions/2026-07-08_m-skill-phase-naming.md`
  - `docs/decisions/README.md`
- Write Set:
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\docs\**`
- Acceptance:
  - Stable docs identify the new canonical phase names.
  - Stable docs define discuss vs plan responsibilities.
  - Stable docs record the no-duplicate reference model.
  - Historical change archives are not rewritten for cosmetic renaming.
- Test Points:
  - Re-read stable docs and indexes.
  - Confirm `docs/change` historical records are left intact except for the new archive later.
- Rollback:
  - Revert stable docs and index changes for this workflow.

##### MSR-2 - Rename canonical phase skill packages and manifests

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\plan.md`
- Goal:
  - Replace long canonical phase names with short `m-*` names.
- Files / Modules:
  - `skills/m-autoflow-plan/**` -> `skills/m-plan/**`
  - `skills/m-autoflow-execute/**` -> `skills/m-execute/**`
  - `skills/m-autoflow-test/**` -> `skills/m-test/**`
  - `skills/m-autoflow-archive/**` -> `skills/m-archive/**`
  - `skills/m-autoflow-research/**` -> fold into `skills/m-discuss/**` or remove as public phase
  - `manifests/m-autoflow-plan.json` -> `manifests/m-plan.json`
  - `manifests/m-autoflow-execute.json` -> `manifests/m-execute.json`
  - `manifests/m-autoflow-test.json` -> `manifests/m-test.json`
  - `manifests/m-autoflow-archive.json` -> `manifests/m-archive.json`
  - `manifests/m-autoflow-research.json` removed unless `m-research` is retained
- Write Set:
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\skills\m-*\**`
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\manifests\m-*.json`
- Acceptance:
  - New package names match `SKILL.md` frontmatter names, manifests, source dirs, dist dirs, and display prompts.
  - Old phase package directories are no longer canonical source packages.
- Test Points:
  - `tools\validate-skills.ps1 -Skill m-plan`
  - `tools\validate-skills.ps1 -Skill m-execute`
  - `tools\validate-skills.ps1 -Skill m-test`
  - `tools\validate-skills.ps1 -Skill m-archive`
- Rollback:
  - Revert renamed directories and manifests.

##### MSR-3 - Add `m-discuss` and fold optional research behavior into it

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\plan.md`
- Goal:
  - Add a discussion/discovery phase that can shape requirements before architecture planning.
- Files / Modules:
  - `skills/m-discuss/SKILL.md`
  - `skills/m-discuss/agents/openai.yaml`
  - `skills/m-discuss/references/discussion.md`
  - `skills/m-discuss/references/research.md` or a reference to shared research rules
  - `manifests/m-discuss.json`
- Write Set:
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\skills\m-discuss\**`
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\manifests\m-discuss.json`
- Acceptance:
  - `m-discuss` can create or confirm a worktree before plan.
  - `m-discuss` supports brainstorming, clarifying questions, option comparison, and rejection of bad requirements.
  - `m-discuss` can perform online research when useful and requires citations and uncertainty handling.
  - `m-discuss` stops before architecture execution planning and implementation.
- Test Points:
  - `tools\validate-skills.ps1 -Skill m-discuss`
  - Re-read `m-discuss` references for phase-boundary clarity.
- Rollback:
  - Remove `skills/m-discuss/**` and `manifests/m-discuss.json`.

##### MSR-4 - Refactor `m-autoflow` into a thin umbrella/reference-driven collection

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\plan.md`
- Goal:
  - Make `m-autoflow` a routing collection that points to phase skills and shared references instead of duplicating phase content.
- Files / Modules:
  - `skills/m-autoflow/SKILL.md`
  - `skills/m-autoflow/agents/openai.yaml`
  - `skills/m-autoflow/references/initialization.md`
  - `skills/m-autoflow/references/stages.md`
  - `skills/m-autoflow/references/m-docs-integration.md`
  - `skills/m-autoflow/references/subagents.md`
  - `skills/m-autoflow/references/templates.md`
  - `manifests/m-autoflow.json`
- Write Set:
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\skills\m-autoflow\**`
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\manifests\m-autoflow.json`
- Acceptance:
  - Umbrella dependency list uses new phase skills.
  - Umbrella text is concise and route-oriented.
  - Common rules live in references and are not repeated in every phase `SKILL.md`.
  - `m-autoflow` can still start the full workflow.
- Test Points:
  - `tools\validate-skills.ps1 -Skill m-autoflow`
  - `rg -n "m-autoflow-plan|m-autoflow-execute|m-autoflow-test|m-autoflow-archive|m-autoflow-research" skills manifests docs/requirements docs/specs docs/features docs/decisions`
- Rollback:
  - Revert `m-autoflow` source and manifest changes.

##### MSR-5 - Update references, prompts, dependency names, and current docs references

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\plan.md`
- Goal:
  - Remove stale current-source references to old phase names while preserving historical archive text.
- Files / Modules:
  - new phase `SKILL.md` files
  - new phase `agents/openai.yaml`
  - new phase references
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
  - `docs/features/m-autoflow-workflow.md`
  - relevant README indexes
- Write Set:
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\skills\**`
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\docs\**`
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\manifests\**`
- Acceptance:
  - Current stable docs and source use the new names.
  - Historical `docs/change` entries are not rewritten only for renaming.
  - No current manifest points to deleted package paths.
- Test Points:
  - `rg -n "m-autoflow-plan|m-autoflow-execute|m-autoflow-test|m-autoflow-archive|m-autoflow-research" skills manifests docs/requirements docs/specs docs/features docs/decisions`
  - Expected: no stale current-source references except deliberate compatibility notes if aliases are approved.
- Rollback:
  - Revert text and reference updates.

##### MSR-6 - Validate, sync, and clean stale installed phase skill directories

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\plan.md`
- Goal:
  - Prove new canonical skills are valid and installed, then remove stale old canonical phase installs.
- Files / Modules:
  - `dist/codex/m-autoflow/**`
  - `dist/codex/m-discuss/**`
  - `dist/codex/m-plan/**`
  - `dist/codex/m-execute/**`
  - `dist/codex/m-test/**`
  - `dist/codex/m-archive/**`
  - `C:\Users\HelloWorld\.codex\skills\m-autoflow\**`
  - `C:\Users\HelloWorld\.codex\skills\m-discuss\**`
  - `C:\Users\HelloWorld\.codex\skills\m-plan\**`
  - `C:\Users\HelloWorld\.codex\skills\m-execute\**`
  - `C:\Users\HelloWorld\.codex\skills\m-test\**`
  - `C:\Users\HelloWorld\.codex\skills\m-archive\**`
  - stale installed old phase directories if aliases are not retained
- Write Set:
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\dist\codex\**`
  - `C:\Users\HelloWorld\.codex\skills\m-*\**`
- Acceptance:
  - New canonical skills validate.
  - New canonical skills sync to local install.
  - Stale old phase install directories are removed or intentionally retained as aliases.
  - No remote push or docs publication is performed.
- Test Points:
  - validation and sync commands listed in Stage 2
  - `git diff --check`
  - `Get-ChildItem C:\Users\HelloWorld\.codex\skills | Where-Object Name -like "m-*"`
- Rollback:
  - Revert source/dist changes and resync previous skills if needed.

##### MSR-7 - Commit approved execution changes locally

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\plan.md`
- Goal:
  - Satisfy `guide.md` after approved modifications.
- Files / Modules:
  - All approved modified files from `MSR-1` through `MSR-6`.
- Write Set:
  - Git index and local branch history for `refactor/m-skill-phase-rename`.
- Acceptance:
  - Local commit exists.
  - No push is performed.
- Test Points:
  - `git status --short`
  - `git log -1 --oneline`
- Rollback:
  - Use a follow-up revert commit if the user rejects the result after commit.

##### MSR-8 - Review and archive this workflow

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\plan.md`
- Goal:
  - Run review, create `docs/change`, update lessons if needed, and ask whether to end the workflow.
- Files / Modules:
  - `docs/change/2026-07-08_m-skill-phase-rename.md`
  - `docs/change/README.md`
  - possible `docs/lessons/**`
- Write Set:
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\docs\change\**`
  - optional `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\docs\lessons\**`
- Acceptance:
  - Archive records intake/feature/requirement/spec/decision/lesson impact.
  - Review passes or findings are fixed/accepted.
- Test Points:
  - Re-read archive and indexes.
- Rollback:
  - Revert archive docs if workflow is abandoned before completion.

##### MSR-9 - Decide whether to push or publish the local branch

- Owner: User
- Worktree: N/A
- Plan Path: N/A
- Goal:
  - Decide remote, push, publication, or backup strategy.
- Files / Modules:
  - User-managed Git remote state.
- Write Set:
  - None in this workflow.
- Acceptance:
  - Only the user decides.
- Test Points:
  - Not applicable.
- Rollback:
  - Not applicable.

##### MSR-10 - Add old-name compatibility aliases

- Owner: User decision / future workflow
- Worktree: future or same worktree only if explicitly approved before execution
- Plan Path: this plan if amended
- Goal:
  - Keep `$m-autoflow-plan` and similar names as thin redirecting aliases.
- Files / Modules:
  - old `skills/m-autoflow-*` package names
  - old `manifests/m-autoflow-*.json`
- Write Set:
  - None in the default execution scope.
- Acceptance:
  - Only execute if the user chooses compatibility over a clean rename.
- Test Points:
  - Alias packages validate and clearly point to canonical names.
- Rollback:
  - Remove alias packages and manifests.

#### Dependencies

- `MSR-1` should happen before or alongside source changes.
- `MSR-2` and `MSR-3` should happen before `MSR-4` so umbrella dependencies can point at real packages.
- `MSR-4` depends on new phase names being decided.
- `MSR-5` depends on `MSR-2` through `MSR-4`.
- `MSR-6` depends on source and manifest completion.
- `MSR-7` depends on validation and sync.
- `MSR-8` depends on execution and review.
- `MSR-9` is user-owned and out of scope.
- `MSR-10` requires explicit user approval if desired.

#### Risks and Notes

- Default compatibility stance:
  - do not keep old phase packages unless the user asks before execution.
  - reason: the user explicitly wants shorter names and less command clutter.
- `m-autoflow` can remain both umbrella and shared reference host in this iteration.
  - If this feels too much like a rule-bearing skill rather than only a collection, create a future `m-workflow-core` or equivalent shared reference package.
- `m-discuss` should not become a loophole for implementation.
  - It may create worktrees and docs artifacts, but it must stop before code changes.
- `m-plan` should be more assertive than current planning:
  - it should reject or return bad requirements to discussion instead of producing a weak plan.
- Historical change archives should stay historically accurate.
- Local installed skills will change; this session's skill discovery list may not reflect the new names until refreshed.

#### Parallelism Assessment

- No implementation sub-agents are allowed in `3.1`.
- For execution, sub-agents are not recommended for the first pass because:
  - package renames, manifests, docs, install paths, and references are tightly coupled
  - a single consistent naming decision is more important than parallel speed
  - stale reference cleanup requires one coherent source-of-truth pass
- Main agent should execute `MSR-1` through `MSR-7`.

#### Issue List

- None.
- Blocked: No.
- Exit criteria met for Stage 3.1.

### Stage 3.2 - Execution

#### Parallelism Assessment

- Implementation sub-agents were not used.
- Reason:
  - directory renames, manifests, references, stable docs, and install cleanup all depend on one naming contract
  - splitting the edits would increase merge/conflict and stale-reference risk

#### Completed Task Mapping

- `MSR-1`:
  - Added `docs/features/m-autoflow-workflow.md`.
  - Updated `docs/features/README.md`.
  - Rewrote current `docs/requirements/m-autoflow-skill.md` around the new canonical phase names.
  - Rewrote current `docs/specs/m-autoflow-skill.md` around the new package, trigger, docs, sub-agent, validation, and cleanup contracts.
  - Added `docs/decisions/2026-07-08_m-skill-phase-naming.md`.
  - Updated `docs/decisions/README.md`.
  - Updated the intake record's planned feature/decision links to actual links.
- `MSR-2`:
  - Renamed canonical phase packages and manifests to `m-plan`, `m-execute`, `m-test`, `m-archive`, and `m-discuss`.
  - Removed old long phase source package names from the canonical source tree.
- `MSR-3`:
  - Added first-class `$m-discuss` skill behavior.
  - Folded optional online research behavior into `skills/m-discuss/references/research.md`.
  - Added discussion handoff, worktree, research, and source-quality rules.
- `MSR-4`:
  - Refactored `$m-autoflow` into an umbrella / collection entry.
  - Kept shared workflow references under `skills/m-autoflow/references`.
  - Updated umbrella manifest dependencies to the new phase skills.
- `MSR-5`:
  - Updated phase prompts, references, manifests, stable docs, and current source references to the new names.
  - Preserved old names only in source-preserving intake and historical archive contexts.
- `MSR-6`:
  - Validated and synced all six canonical skills.
  - Removed stale installed old phase skill directories from `C:\Users\HelloWorld\.codex\skills`.
- `MSR-7`:
  - This execution result is committed locally after validation as required by `guide.md`.

#### Validation Results

- Passed:
  - `tools\validate-skills.ps1 -Skill m-autoflow`
  - `tools\validate-skills.ps1 -Skill m-discuss`
  - `tools\validate-skills.ps1 -Skill m-plan`
  - `tools\validate-skills.ps1 -Skill m-execute`
  - `tools\validate-skills.ps1 -Skill m-test`
  - `tools\validate-skills.ps1 -Skill m-archive`
- Passed:
  - `tools\sync-skills.ps1 -Skill m-autoflow`
  - `tools\sync-skills.ps1 -Skill m-discuss`
  - `tools\sync-skills.ps1 -Skill m-plan`
  - `tools\sync-skills.ps1 -Skill m-execute`
  - `tools\sync-skills.ps1 -Skill m-test`
  - `tools\sync-skills.ps1 -Skill m-archive`
- Passed:
  - current-source stale-name scan across `skills`, `manifests`, `docs/requirements`, `docs/specs`, `docs/features`, and `docs/decisions`
  - `git diff --check`
- Notes:
  - `git diff --check` reported only CRLF normalization warnings from Git on Windows.
  - Installed canonical `m-*` skills now include `m-autoflow`, `m-discuss`, `m-plan`, `m-execute`, `m-test`, and `m-archive`.
  - Old installed long phase directories were removed.

#### Residual Risk

- This change affects skill invocation and local installed skill discovery. The current Codex session's displayed skill list may not refresh until a new session or skill reload.
- Heavy workflow review and `docs/change` archive are intentionally left for `MSR-8`.

#### Issue List

- None.
- Blocked: No.
- Exit criteria met for Stage 3.2.

### Stage 3.3 - Review

#### Heavy Test Decision

- Heavy `$m-test` phase: skipped.
- Skip reason:
  - The change is a skill/docs/package rename and documentation governance update.
  - No product runtime, data migration, network boundary, auth, storage, billing, or user-facing application flow changed.
  - Execution-stage validation covered skill packages, manifests, local install output, and stale-reference cleanup.

#### Review Checklist

- 需求覆盖: 通过
- 架构合理性: 通过
- 性能风险（N+1 / 重复计算 / 多余 I/O / 锁竞争）: 通过
- 性能指标 / 阈值: 通过, not applicable to this skill/docs rename
- 可用性 / 用户路径: 通过
- 可读性与一致性: 通过
- 可扩展性与配置化: 通过
- 稳定性与安全: 通过
- 安全边界 / 权限 / 数据暴露: 通过
- 测试覆盖情况: 通过
- 整体流程 / 联调验证: 通过
- 子Agent治理与审计: 通过, no sub-agents were used

#### Residual Risk

- The current Codex session may not refresh the visible skill list until a new session or skill reload.
- Users who explicitly invoke old long phase names will need to use the new names unless a future alias workflow is approved.

#### Issue List

- None.
- Blocked: No.
- Exit criteria met for Stage 3.3.

### Stage 4 - Archive

#### Docs Governance Routing Result

Used `$m-docs` to confirm archive routing, stable-doc impact, indexes, and lessons handling.

- Docs root:
  - `D:\project\my-ai-skills\worktrees\m-skill-phase-rename\docs`
- Archive:
  - `docs/change/2026-07-08_m-skill-phase-rename.md`
- Lessons:
  - `docs/lessons/skill-frontmatter-yaml-colon.md`
- Indexes updated:
  - `docs/change/README.md`
  - `docs/lessons/README.md`
- Stable-doc cross-links updated:
  - `docs/intake/2026-07-08_m-skill-phase-rename.md`
  - `docs/features/m-autoflow-workflow.md`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
  - `docs/decisions/2026-07-08_m-skill-phase-naming.md`

#### Stable Docs Impact

- Intake impact: updated
- Feature impact: updated
- Requirements impact: updated
- Specs impact: updated
- Decision impact: updated
- Lessons impact: updated

#### Validation During Archive

- Passed:
  - `tools\validate-skills.ps1 -Skill m-autoflow`
  - `tools\validate-skills.ps1 -Skill m-discuss`
  - `tools\validate-skills.ps1 -Skill m-plan`
  - `tools\validate-skills.ps1 -Skill m-execute`
  - `tools\validate-skills.ps1 -Skill m-test`
  - `tools\validate-skills.ps1 -Skill m-archive`
- Passed:
  - stale old-name scan across `skills`, `manifests`, `docs/requirements`, `docs/specs`, `docs/features`, and `docs/decisions`
  - installed canonical `m-*` skill list check
  - `git diff --check`

#### Publication / Backup

- No remote, push, docs publication, or backup target was configured.
- Branch remains local-only unless the user later chooses otherwise.

#### Issue List

- None.
- Blocked: No.
- Archive is complete.
- Workflow end still requires explicit user confirmation before merge and worktree cleanup.

## Exit Gate

Workflow status:

- Executed: `MSR-1`, `MSR-2`, `MSR-3`, `MSR-4`, `MSR-5`, `MSR-6`, `MSR-7`, `MSR-8`
- Will not execute now:
  - `MSR-9` - user-owned remote/push/publication/backup decision.
  - `MSR-10` - deferred old-name compatibility aliases, only if explicitly requested.

Blocked: no
Archive complete.
Awaiting explicit workflow-end confirmation before merge and worktree cleanup.
