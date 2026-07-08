# Plan - docs-private-governance

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `refactor/docs-private-governance`
- Base: `main`
- Worktree: `D:\project\my-ai-skills\worktrees\docs-private-governance`
- Current Stage: `3.2 - Execution complete, awaiting review/archive`
- Planning skill: `$m-autoflow-plan`
- Docs governance skill: `$m-docs`

## Stage Records

### Initialization

- `guide.md`:
  - Present at `D:\project\my-ai-skills\guide.md`.
  - Active rule: every modification round must be committed automatically, with an English commit message following the existing history format.
- Owning repo:
  - `D:\project\my-ai-skills`
- Base branch:
  - `main`
- Dedicated branch:
  - `refactor/docs-private-governance`
- Dedicated worktree:
  - `D:\project\my-ai-skills\worktrees\docs-private-governance`
- Main repo path:
  - `D:\project\my-ai-skills`
  - Control-plane only for this workflow.
- Participating modules:
  - `skills/m-docs/**`
  - `skills/m-autoflow/**`
  - `skills/m-autoflow-plan/**`
  - `skills/m-autoflow-archive/**` if archive docs-root wording is needed during execution
  - `docs/requirements/**`
  - `docs/specs/**`
  - `docs/README.md`
  - `tools/validate-skills.ps1`
  - `tools/sync-skills.ps1`
- Initialization notes:
  - Created the dedicated worktree from `main`.
  - Added `worktrees/` to local `.git/info/exclude` in the main repo so nested worktrees do not pollute repository status. This is local Git metadata and is not part of the committed change set.
  - Replaced a stale inherited root `plan.md` in the new worktree with this workflow plan.

### Optional Research - Source-backed Planning Input

#### Research Question

How should this repository's docs governance evolve so feature-level behavior is complete and maintainable, original user requests remain traceable, and private project docs can live outside code repos in multi-repo projects?

#### Sources Used

- Atlassian PRD guidance: https://www.atlassian.com/agile/product-management/requirements
- Atlassian product requirements template: https://www.atlassian.com/software/confluence/templates/product-requirements
- Cucumber Gherkin reference: https://cucumber.io/docs/gherkin/reference/
- Diataxis documentation framework: https://diataxis.fr/
- C4 model: https://c4model.com/
- Microsoft ADR guidance: https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record

#### Confirmed Findings

- Product and feature requirements are easier to maintain when user need, scope, interaction, design context, and acceptance are grouped around the feature instead of split only by document category.
- Gherkin-style `Feature`, `Rule`, and `Scenario` structures provide a useful, lightweight pattern for acceptance criteria and CRUD workflow coverage.
- Diataxis supports organizing documentation around reader needs, but it does not by itself solve feature-level traceability; it should inform navigation, not replace feature dossiers.
- C4-style architecture views are useful for cross-repo and system/module relationships, but they should supplement feature docs rather than become the only source of feature behavior.
- ADRs should be append-only decision records for architecturally significant choices; they should not become design guides or feature specs.

#### Conflicts / Uncertainties

- No source directly covers the user's exact privacy constraint that docs must not live in pushable code repos. This is a user-owned project rule and should be treated as stable local workflow policy.
- The exact private docs location cannot be inferred globally. The skill should detect or ask for `docs_root` instead of assuming a remote or backup path.

#### Planning Implications

- Add `docs/intake/` for original request evidence.
- Add `docs/features/` as the preferred feature-level current-truth layer.
- Add optional `docs/decisions/` for ADR-style decision records.
- Keep `docs/specs/` for cross-feature technical contracts, interfaces, architecture constraints, and repo integration rules.
- Teach the workflow to distinguish `project_root`, `docs_root`, `code_repos`, and `active_worktree`.
- Make publication, remote configuration, push target, and backup strategy explicitly user-owned.

### Stage 1 - Requirements Analysis

#### Goal

Update the `m-docs` and `m-autoflow` planning model so private docs become a feature-first, traceable, multi-repo-aware source of truth that is not automatically written into or pushed with business code repositories.

#### Scope

Must:

- Add a first-class private docs-root concept:
  - `project_root`: the local umbrella project directory.
  - `docs_root`: private documentation root, possibly a standalone local/private Git repo.
  - `code_repos`: one or more implementation repositories under or near the project root.
  - `active_worktree`: the dedicated code worktree for the current implementation.
- Add `intake` for original user requests:
  - raw request text or concise source-preserving excerpts.
  - date, source, requester when known.
  - unresolved questions and links to feature/spec/change records.
- Add `features` for feature-level current truth:
  - end-to-end behavior.
  - CRUD workflows.
  - UI entry points, buttons, layout, states, and permissions.
  - acceptance scenarios.
  - cross-repo ownership map.
- Add optional `decisions` for ADR-like records:
  - append-only, stable decision entries.
  - superseding decisions link to prior decisions.
- Preserve `specs` for technical contracts:
  - API, protocol, schema, architecture, cross-repo integration, validation, and generated-doc rules.
- Keep `plan`, `change`, and `lessons` as workflow/archive/learning layers.
- Prevent governed docs from being written into a pushable code repo unless the user explicitly declares that repo as the docs root.
- Make docs Git publication user-owned:
  - do not add remotes automatically.
  - do not push docs automatically.
  - do not infer backup targets.
  - commit only when the user or local project rules require it.
- Update `$m-autoflow-plan` so planning looks for affected feature docs and intake evidence before implementation.
- Update source skill docs and stable repository docs so future edits do not rely on this chat history.

Optional:

- Update bootstrap tooling to create the expanded docs tree.
- Keep backward compatibility with existing `requirements` docs for repositories that already use them.

Out of scope:

- Creating an actual private docs repo for a user project.
- Deciding where the user should push or back up docs.
- Migrating existing external project documentation.
- Changing business/runtime behavior outside this skill repository.
- Pushing any branch or remote.

#### Use Cases

- A user has a multi-repo project under one project directory and wants one private docs truth center.
- A user wants a feature such as personnel management documented in one complete feature file, including create/read/update/delete, UI placement, permissions, and acceptance scenarios.
- A user wants original requests preserved separately from change archives.
- A user wants docs to be versioned locally but does not want them pushed with code repositories.
- A user wants cross-repo features mapped to multiple implementation repos without duplicating truth in each repo.

#### Functional Requirements

- `$m-docs` must classify docs work across `intake`, `features`, `requirements`, `specs`, `decisions`, `plan`, `change`, and `lessons`.
- `$m-docs` must prefer `features` for user-visible feature behavior and acceptance.
- `$m-docs` must prefer `intake` for original request evidence.
- `$m-docs` must keep `change` as a workflow result archive, not as the original request or feature truth.
- `$m-docs` must keep `specs` for technical contracts and architecture constraints.
- `$m-docs` must route ADR-like choices to `decisions`.
- `$m-docs` must distinguish project-level private docs from code-repo implementation docs.
- `$m-docs` must not create or update governed docs inside code repos by default.
- `$m-docs` must state that docs remote configuration, push, and backup are user-owned decisions.
- `$m-autoflow-plan` must identify `docs_root`, affected feature docs, affected specs, and affected intake records during planning.
- `$m-autoflow-plan` must block or ask when a behavior-changing request lacks a discoverable private docs root and no safe default is confirmed.
- `$m-autoflow` archive guidance must record feature/spec/intake impacts instead of writing final truth only to `change`.

#### Non-functional Requirements

- Privacy:
  - default to private local docs outside code repos.
  - never infer external publication.
- Maintainability:
  - avoid duplicating stable truth across features, specs, decisions, and changes.
  - keep skill bodies concise and put detailed routing rules in references.
- Traceability:
  - connect intake -> feature/spec/decision -> plan -> change -> lessons where relevant.
- Backward compatibility:
  - existing requirements/specs docs remain valid.
  - expanded categories should not break current validation or sync tooling.
- Discoverability:
  - root and category README files must expose the new reading order and routing rules.

#### Inputs / Outputs

Inputs:

- User request.
- Current repo and worktree state.
- Existing stable docs.
- Existing `m-docs` and `m-autoflow` skill source files.
- External research findings listed above.

Outputs:

- Updated stable repository docs.
- Updated `m-docs` source instructions and references.
- Updated `m-autoflow` / `m-autoflow-plan` planning instructions.
- Updated bootstrap/templates/indexing guidance where needed.
- Validation and sync results for affected skills.
- Local commit(s) following `guide.md`.

#### Edge Cases

- The project root may not be a Git repo.
- The private docs root may be a standalone Git repo, a plain local folder, or not created yet.
- Multiple code repos may participate in one feature.
- A feature may be fully owned by one repo but still documented in a private root due to privacy policy.
- Existing repos may already have `docs/`; the skill must not assume those are canonical when the user wants private docs.
- A docs root may have a remote, but the workflow must not push without explicit user instruction.
- A stale root `plan.md` can exist in a worktree and must be replaced by the active workflow plan.

#### Acceptance Criteria

- Future `$m-docs` usage can explain where original requests, feature behavior, technical contracts, decisions, workflow plans, changes, and lessons belong.
- Future `$m-autoflow-plan` usage can plan a multi-repo project without putting governed docs into code repos.
- Feature-level docs can represent a complete capability such as personnel management from a user-visible behavior perspective.
- Docs Git publishing and backup remain user-owned and are not inferred by the workflow.
- Affected skills validate and sync successfully.
- A local commit records the planning artifact and later implementation changes according to `guide.md`.

#### Risks

- Adding too many categories could make routing harder unless the decision tree is explicit.
- `requirements` and `features` could become competing truth layers if their boundary is not precise.
- Updating only `m-docs` without `m-autoflow-plan` would leave planning behavior inconsistent.
- Updating installed skills without source docs would create drift.

#### Issue List

- None.
- Blocked: No.
- Exit criteria met for Stage 1.

### Stage 2 - Architecture Design

#### Overall Solution

Evolve docs governance from category-first only to feature-first plus category-aware:

- `intake`: source evidence for original requests.
- `features`: current user-visible feature truth.
- `requirements`: durable capability needs and non-feature constraints; retained for backward compatibility and skill-level requirements.
- `specs`: technical contracts and architecture constraints.
- `decisions`: append-only ADR-style decisions.
- `plan`: workflow planning archive, while active root `plan.md` remains a workflow-control exception.
- `change`: completed workflow results.
- `lessons`: reusable troubleshooting and prevention knowledge.

Add a private docs-root model:

- Project-level private docs are canonical for product/feature truth.
- Code repos are implementation carriers.
- Cross-repo features are documented once in private `docs/features/` and link to code repo paths/modules.
- The workflow must not write governed docs into code repos unless the user explicitly says that code repo is the docs root.
- A docs root may be a separate Git repo, but remote/push/backup are user-owned decisions.

#### Alternatives Considered

- Keep docs under each code repo:
  - Rejected for this workflow because the user does not want private analysis and product knowledge pushed with code.
- Put everything into `requirements` and `specs`:
  - Rejected because it keeps feature behavior scattered and does not preserve original request evidence.
- Put everything into `change`:
  - Rejected because `change` is history, not current truth or raw intake.
- Make a single external docs repo mandatory:
  - Rejected because the user wants to decide backup and publication strategy; the skill should support but not impose it.

#### Module Responsibilities

- `skills/m-docs/SKILL.md`
  - Top-level classification list and guardrails.
- `skills/m-docs/references/taxonomy.md`
  - Expanded docs model and source-of-truth boundaries.
- `skills/m-docs/references/routing-rules.md`
  - Decision tree for intake/features/specs/decisions/private docs root/multi-repo cases.
- `skills/m-docs/references/templates.md`
  - Templates for intake, feature dossier, decision record, and updated indexes.
- `skills/m-docs/references/indexing-rules.md`
  - Root and category index obligations for new categories.
- `skills/m-docs/references/requirement-impact.md`
  - Impact checks expanded to feature/spec/intake/decision impacts.
- `skills/m-docs/scripts/bootstrap_docs_tree.py`
  - Optional bootstrap support for expanded private docs tree.
- `skills/m-autoflow/references/initialization.md`
  - Distinguish `project_root`, docs root, code repos, and worktrees.
- `skills/m-autoflow/references/m-docs-integration.md`
  - Record feature/intake/spec/decision impacts in planning and archive.
- `skills/m-autoflow/references/templates.md`
  - Plan/change skeletons updated with docs-root and feature-impact fields.
- `skills/m-autoflow-plan/SKILL.md`
  - Quick-start and workflow wording updated to check private docs root and affected feature docs.
- `skills/m-autoflow-plan/references/planning.md`
  - Required checks and plan contents updated for private docs root, feature dossiers, and multi-repo capabilities.
- `docs/requirements/m-docs-skill.md`
- `docs/specs/m-docs-skill.md`
- `docs/requirements/m-autoflow-skill.md`
- `docs/specs/m-autoflow-skill.md`
  - Stable repository truth for the new docs governance behavior.

#### Data / Call Flow

1. User invokes `$m-autoflow-plan` or `$m-docs`.
2. The workflow identifies the real code repo(s), current worktree, project root, and private docs root.
3. `$m-docs` reads docs indexes from the private docs root when present.
4. For behavior-changing work:
   - original request evidence routes to `intake`.
   - current feature behavior routes to `features`.
   - technical contracts route to `specs`.
   - architecturally significant decisions route to `decisions`.
5. Active root `plan.md` remains in the execution worktree as a workflow-control file.
6. Completed workflow results route to private docs `change`.
7. Reusable troubleshooting knowledge routes to private docs `lessons`.
8. Code repo commits do not publish private docs unless the user explicitly configured docs inside that repo.

#### Interface Drafts

Feature doc sections:

- Status
- Goal
- Non-goals
- Actors / permissions
- Entry points
- Layout / navigation
- Data model
- CRUD workflows
- Validation rules
- Empty / loading / error states
- API / integration contracts
- Audit / security
- Acceptance scenarios
- Cross-repo ownership
- Related intake / specs / decisions / changes / lessons

Intake doc sections:

- Source
- Date
- Raw request or source-preserving summary
- Context
- Confirmed requirements
- Open questions
- Routed feature/spec/decision/change links

Decision doc sections:

- Status
- Context
- Options considered
- Decision
- Consequences
- Supersedes / superseded by
- Related features/specs/changes

#### Error Handling and Safety

- If a request changes feature behavior and no private docs root is discoverable, ask the user or record a blocker before implementation.
- If a code repo contains `docs/` but the user has a private docs policy, do not treat repo-local docs as canonical without confirmation.
- If `features` and `requirements` compete, prefer `features` for user-visible behavior and `requirements` for broader capability constraints; update the routing rules to say this explicitly.
- If a docs root has a Git remote, do not push, add remote, or change backup configuration without explicit user instruction.
- Do not use `change` as the only home for current feature truth.

#### Performance and Testing Strategy

- Keep most behavior as instruction/reference updates; no runtime service is involved.
- Validate changed skills with:
  - `tools/validate-skills.ps1 -Skill m-docs`
  - `tools/validate-skills.ps1 -Skill m-autoflow`
  - `tools/validate-skills.ps1 -Skill m-autoflow-plan`
  - `tools/validate-skills.ps1 -Skill m-autoflow-archive` if edited
- Sync changed skills with:
  - `tools/sync-skills.ps1 -Skill <affected-skill>`
- Run `git diff --check`.
- Re-read changed references for consistency.

#### Extensibility Design Points

- New category rules live in `m-docs` references so future workflow skills can reuse them.
- Multi-repo/private-docs rules live in workflow references so execution skills can stay clear about code versus docs ownership.
- Bootstrap script can be extended without forcing every project to adopt every category immediately.

#### Issue List

- None.
- Blocked: No.
- Exit criteria met for Stage 2.

### Stage 3.1 - Planning

#### Project Goal and Current State

- Goal:
  - Plan a guarded implementation that adds private docs-root, intake, feature dossiers, decisions, and multi-repo docs routing to `m-docs` and `m-autoflow-plan`.
- Current state:
  - `m-docs` currently supports only `requirements`, `specs`, `plan`, `change`, and `lessons`.
  - `m-autoflow-plan` currently assumes docs under the owning repo and does not explicitly model a private docs root.
  - The user wants docs to be optionally versioned in a separate local/private Git repo, but publication and backup must remain user-owned.
  - A dedicated implementation worktree exists and this root `plan.md` is now the active control document.

#### Docs Governance Routing Decision

Used `$m-docs` for routing and impact review.

- Stable truth to update:
  - `docs/requirements/m-docs-skill.md`
  - `docs/specs/m-docs-skill.md`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
- Source instructions to update:
  - `skills/m-docs/**`
  - `skills/m-autoflow/**`
  - `skills/m-autoflow-plan/**`
  - `skills/m-autoflow-archive/**` only if archive phase wording must be aligned.
- Active workflow control:
  - `plan.md` at the worktree root.
- Later workflow result:
  - `docs/change/YYYY-MM-DD_docs-private-governance.md`
- Lessons:
  - No known recurring troubleshooting pattern yet.
  - Reassess during archive.
- Requirements impact: add / clarify
- Specs impact: add / clarify

#### Related Requirements / Specs / Lessons

- Related requirements:
  - `docs/requirements/m-docs-skill.md`
  - `docs/requirements/m-autoflow-skill.md`
- Related specs:
  - `docs/specs/m-docs-skill.md`
  - `docs/specs/m-autoflow-skill.md`
- Related lessons:
  - None identified yet.

#### Executable Task List

- [x] `PDG-1` Update stable docs for private docs governance.
- [x] `PDG-2` Update `m-docs` category model, routing, templates, indexes, and bootstrap support.
- [x] `PDG-3` Update `m-autoflow` and `m-autoflow-plan` to use private docs roots during planning and archive.
- [x] `PDG-4` Validate and sync affected skills.
- [x] `PDG-5` Commit approved execution changes locally.
- [ ] `PDG-6` Review and archive the workflow.
- [ ] `PDG-7` Decide docs remote, push, or backup strategy.
- [ ] `PDG-8` Create or migrate docs for any external user project.

#### Execution Scope After Approval

##### Will Execute

- `PDG-1` - required to update durable repository truth before or alongside source changes.
- `PDG-2` - required to implement the `m-docs` behavior change.
- `PDG-3` - required to align planning workflow behavior with docs governance.
- `PDG-4` - required validation and local sync for affected skills.
- `PDG-5` - required by `guide.md` after approved modifications.

##### Will Not Execute Now

- `PDG-6` - separate review/archive phase after implementation and validation.
- `PDG-7` - out of scope and user-owned; do not infer remote, push, or backup strategy.
- `PDG-8` - out of scope until the user names a target project and docs root.

#### Task Details

##### PDG-1 - Update stable docs for private docs governance

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\docs-private-governance`
- Plan Path: `D:\project\my-ai-skills\worktrees\docs-private-governance\plan.md`
- Goal:
  - Record the new long-lived requirements and specs before source behavior depends on them.
- Files / Modules:
  - `docs/requirements/m-docs-skill.md`
  - `docs/specs/m-docs-skill.md`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
  - `docs/README.md`
  - affected category indexes if topology wording changes
- Write Set:
  - `D:\project\my-ai-skills\worktrees\docs-private-governance\docs\**`
- Acceptance:
  - Stable docs describe intake, feature dossiers, private docs roots, code repo boundaries, and user-owned push/backup decisions.
  - Existing `requirements` / `specs` boundaries remain understandable.
- Test Points:
  - Re-read stable docs and indexes for consistency.
  - Confirm no stable behavior is recorded only in `change`.
- Rollback:
  - Revert the stable docs updates for this workflow.

##### PDG-2 - Update `m-docs` category model, routing, templates, indexes, and bootstrap support

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\docs-private-governance`
- Plan Path: `D:\project\my-ai-skills\worktrees\docs-private-governance\plan.md`
- Goal:
  - Make `$m-docs` able to route original requests, feature-level truth, technical specs, ADR-like decisions, workflow archives, and lessons in a private docs root.
- Files / Modules:
  - `skills/m-docs/SKILL.md`
  - `skills/m-docs/references/taxonomy.md`
  - `skills/m-docs/references/routing-rules.md`
  - `skills/m-docs/references/requirement-impact.md`
  - `skills/m-docs/references/indexing-rules.md`
  - `skills/m-docs/references/templates.md`
  - `skills/m-docs/scripts/bootstrap_docs_tree.py`
- Write Set:
  - `D:\project\my-ai-skills\worktrees\docs-private-governance\skills\m-docs\**`
- Acceptance:
  - Routing rules make `intake`, `features`, `specs`, `decisions`, `change`, and `lessons` non-overlapping.
  - Private docs root and multi-repo routing rules are explicit.
  - Bootstrap can create the expanded tree without forcing remotes or pushes.
- Test Points:
  - `tools/validate-skills.ps1 -Skill m-docs`
  - Optional dry-run of `bootstrap_docs_tree.py` if script behavior changes materially.
- Rollback:
  - Revert `skills/m-docs/**` changes.

##### PDG-3 - Update `m-autoflow` and `m-autoflow-plan` to use private docs roots

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\docs-private-governance`
- Plan Path: `D:\project\my-ai-skills\worktrees\docs-private-governance\plan.md`
- Goal:
  - Make planning and archive phases discover and respect private docs roots instead of assuming governed docs live in code repos.
- Files / Modules:
  - `skills/m-autoflow/references/initialization.md`
  - `skills/m-autoflow/references/m-docs-integration.md`
  - `skills/m-autoflow/references/templates.md`
  - `skills/m-autoflow-plan/SKILL.md`
  - `skills/m-autoflow-plan/references/planning.md`
  - `skills/m-autoflow-archive/SKILL.md` and references only if needed
- Write Set:
  - `D:\project\my-ai-skills\worktrees\docs-private-governance\skills\m-autoflow\**`
  - `D:\project\my-ai-skills\worktrees\docs-private-governance\skills\m-autoflow-plan\**`
  - optional `D:\project\my-ai-skills\worktrees\docs-private-governance\skills\m-autoflow-archive\**`
- Acceptance:
  - Planning records `project_root`, `docs_root`, `code_repos`, and `active_worktree`.
  - Behavior-changing plans check affected feature docs and intake evidence.
  - Archive guidance routes durable changes back to private docs categories.
  - Workflow never infers docs push/backup.
- Test Points:
  - `tools/validate-skills.ps1 -Skill m-autoflow`
  - `tools/validate-skills.ps1 -Skill m-autoflow-plan`
  - `tools/validate-skills.ps1 -Skill m-autoflow-archive` if edited
- Rollback:
  - Revert changed `m-autoflow*` skill files.

##### PDG-4 - Validate and sync affected skills

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\docs-private-governance`
- Plan Path: `D:\project\my-ai-skills\worktrees\docs-private-governance\plan.md`
- Goal:
  - Prove the changed skill packages are structurally valid and install the local copies used by Codex.
- Files / Modules:
  - `dist/codex/m-docs/**`
  - `dist/codex/m-autoflow/**`
  - `dist/codex/m-autoflow-plan/**`
  - optional `dist/codex/m-autoflow-archive/**`
  - `C:\Users\HelloWorld\.codex\skills\<affected-skill>`
- Write Set:
  - `D:\project\my-ai-skills\worktrees\docs-private-governance\dist\codex\**`
  - `C:\Users\HelloWorld\.codex\skills\m-docs\**`
  - `C:\Users\HelloWorld\.codex\skills\m-autoflow\**`
  - `C:\Users\HelloWorld\.codex\skills\m-autoflow-plan\**`
  - optional `C:\Users\HelloWorld\.codex\skills\m-autoflow-archive\**`
- Acceptance:
  - Affected skills validate.
  - Affected skills sync to the local install root.
  - No remote push or docs backup is performed.
- Test Points:
  - `tools/validate-skills.ps1 -Skill <affected-skill>`
  - `tools/sync-skills.ps1 -Skill <affected-skill>`
  - `git diff --check`
- Rollback:
  - Revert source and dist changes; resync previous versions if needed.

##### PDG-5 - Commit approved execution changes locally

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\docs-private-governance`
- Plan Path: `D:\project\my-ai-skills\worktrees\docs-private-governance\plan.md`
- Goal:
  - Satisfy `guide.md` by committing the approved modification round locally with an English commit message.
- Files / Modules:
  - All approved modified files from `PDG-1` through `PDG-4`.
- Write Set:
  - Git index and local branch history for `refactor/docs-private-governance`.
- Acceptance:
  - Local commit exists on the dedicated branch.
  - No push is performed.
- Test Points:
  - `git status --short`
  - `git log -1 --oneline`
- Rollback:
  - Use a follow-up revert commit if the user rejects the result after commit.

##### PDG-6 - Review and archive the workflow

- Owner: Main Agent
- Worktree: `D:\project\my-ai-skills\worktrees\docs-private-governance`
- Plan Path: `D:\project\my-ai-skills\worktrees\docs-private-governance\plan.md`
- Goal:
  - Run review, record findings, and archive the completed workflow.
- Files / Modules:
  - `plan.md`
  - `docs/change/YYYY-MM-DD_docs-private-governance.md`
  - affected docs indexes
  - possible `docs/lessons/**` if reusable troubleshooting knowledge emerges
- Write Set:
  - `D:\project\my-ai-skills\worktrees\docs-private-governance\docs\change\**`
  - optional `D:\project\my-ai-skills\worktrees\docs-private-governance\docs\lessons\**`
- Acceptance:
  - Review passes or records findings.
  - Change archive records requirements/specs/features/intake/lessons impacts.
- Test Points:
  - Archive file exists and links to changed stable docs.
  - Lessons impact is explicitly recorded.
- Rollback:
  - Revert archive docs if the workflow is abandoned before completion.

##### PDG-7 - Decide docs remote, push, or backup strategy

- Owner: User
- Worktree: N/A
- Plan Path: N/A
- Goal:
  - Decide where private docs should be pushed or backed up, if anywhere.
- Files / Modules:
  - User-managed docs repository configuration.
- Write Set:
  - None in this workflow.
- Acceptance:
  - Only the user chooses remote, push target, and backup strategy.
- Test Points:
  - Not applicable.
- Rollback:
  - Not applicable.

##### PDG-8 - Create or migrate docs for any external user project

- Owner: User / future workflow
- Worktree: future target project worktree
- Plan Path: future target workflow plan
- Goal:
  - Apply the new docs governance model to a real user project.
- Files / Modules:
  - Future target project private docs root.
- Write Set:
  - None in this workflow.
- Acceptance:
  - Requires a future named target project and docs root.
- Test Points:
  - Not applicable in this workflow.
- Rollback:
  - Not applicable.

#### Dependencies

- `PDG-1` should happen before or alongside `PDG-2` and `PDG-3` so stable truth does not lag behind source behavior.
- `PDG-2` and `PDG-3` can be worked in parallel only after the shared docs-root model is settled, but the main agent will keep ownership because the same taxonomy touches both.
- `PDG-4` depends on `PDG-2` and `PDG-3`.
- `PDG-5` depends on `PDG-1` through `PDG-4`.
- `PDG-6` depends on implementation and validation.
- `PDG-7` and `PDG-8` are outside the next execution phase.

#### Risks and Notes

- The `features` versus `requirements` boundary must be precise:
  - `features` own user-visible current behavior.
  - `requirements` remain useful for broader capability needs, constraints, and non-feature skill requirements.
- Do not create a hard-coded docs path such as `D:\private-docs`; use discovery or require confirmation.
- Do not push any code or docs branch.
- Installed skill sync writes outside the repo to `C:\Users\HelloWorld\.codex\skills`; this is local installation, not remote publication.
- The root `plan.md` is a workflow-control exception and does not replace archived `docs/plan/`.

#### Parallelism Assessment

- No implementation sub-agents are allowed in `3.1`.
- After approval, sub-agent use is not recommended for this execution because:
  - taxonomy, routing, bootstrap, and workflow wording are tightly coupled.
  - a single coherent source-of-truth boundary is more important than raw parallel speed.
  - validation/sync is small enough for the main agent.
- Main agent should execute all `PDG-1` through `PDG-5`.

#### Issue List

- None.
- Blocked: No.
- Exit criteria met for Stage 3.1.

### Stage 3.2 - Execution

#### Parallelism Assessment

- Sub-agents were not used.
- Reason:
  - `PDG-1`, `PDG-2`, and `PDG-3` share one taxonomy and source-of-truth boundary, so splitting the work would risk inconsistent wording.
  - `PDG-4` validation and sync were small local checks.
  - The main agent kept ownership of integration and acceptance.

#### PDG-1 - Stable Docs

- Completed.
- Added private-docs-root, intake, features, and decisions guidance to the repository docs entry points.
- Added category README files:
  - `docs/intake/README.md`
  - `docs/features/README.md`
  - `docs/decisions/README.md`
- Updated stable docs:
  - `docs/requirements/m-docs-skill.md`
  - `docs/specs/m-docs-skill.md`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
- Updated affected category indexes and lesson wording so current docs no longer imply that `change` or `lessons` can replace stable truth.

#### PDG-2 - m-docs Source

- Completed.
- Updated `skills/m-docs/SKILL.md` to classify `intake`, `features`, `requirements`, `specs`, `decisions`, `plan`, `change`, and `lessons`.
- Replaced the taxonomy, routing, impact, indexing, and template references with private-docs-aware rules.
- Updated lessons rules to link back to features and decisions when recurring knowledge exposes stable-doc gaps.
- Extended `bootstrap_docs_tree.py` with:
  - expanded categories
  - optional `--docs-root`
  - feature module buckets
  - private docs publication guidance

#### PDG-3 - m-autoflow / Planning / Archive Source

- Completed.
- Updated `m-autoflow` umbrella instructions, initialization rules, stage rules, docs integration, and templates to record:
  - `project_root`
  - `docs_root`
  - `code_repos`
  - `active_worktree`
  - intake/feature/requirement/spec/decision impact
- Updated `m-autoflow-plan` to require private docs-root and feature/intake checks during planning.
- Updated `m-autoflow-archive` to archive into the selected docs root and record expanded stable-doc impact.
- Kept docs remote, push, publication, and backup decisions user-owned.

#### PDG-4 - Validation And Sync

- Completed.
- Lightweight validation:
  - `python -m py_compile skills\m-docs\scripts\bootstrap_docs_tree.py`
  - `python skills\m-docs\scripts\bootstrap_docs_tree.py --docs-root tmp\docs-bootstrap-smoke --module personnel --dry-run`
  - `git diff --check`
  - `tools\validate-skills.ps1 -Skill m-docs`
  - `tools\validate-skills.ps1 -Skill m-autoflow`
  - `tools\validate-skills.ps1 -Skill m-autoflow-plan`
  - `tools\validate-skills.ps1 -Skill m-autoflow-archive`
- Local sync:
  - `tools\sync-skills.ps1 -Skill m-docs`
  - `tools\sync-skills.ps1 -Skill m-autoflow`
  - `tools\sync-skills.ps1 -Skill m-autoflow-plan`
  - `tools\sync-skills.ps1 -Skill m-autoflow-archive`
- Notes:
  - `git diff --check` produced only LF/CRLF conversion warnings and no whitespace errors.
  - No remote, push, publication, or backup action was performed.

#### PDG-5 - Local Commit

- Completed by the local commit that includes this execution record.

#### Stage 3.2 Issue List

- None.
- Blocked: No.
- Exit criteria met for Stage 3.2.

## Exit Gate

Execution scope after approval:

- Will execute: `PDG-1`, `PDG-2`, `PDG-3`, `PDG-4`, `PDG-5`
- Will not execute now:
  - `PDG-6` - separate review/archive phase after implementation and validation.
  - `PDG-7` - user-owned remote/push/backup decision.
  - `PDG-8` - future target-project migration requires separate approval.

Blocked: no
Enter execution only after the user explicitly confirms this plan.
