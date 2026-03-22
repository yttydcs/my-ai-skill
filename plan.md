# Plan - docs-governor

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `feat/docs-governor-skill`
- Base: `main`
- Worktree: `D:\project\MyFlowHub3\worktrees\docs-governor-skill`
- Current Stage: `4 - Change Archive`
- Scope:
  - Create a reusable `docs-governor` skill repository
  - Implement a Codex-focused skill with a compatibility-friendly layout for future Claude support
  - Use copy-based sync as the installation model
- Non-goals:
  - Do not modify `D:\project\MyFlowHub3` runtime code or document tree in this workflow
  - Do not install to Claude-specific runtime paths in this workflow

## Stage Records

### Initialization

- Confirmed skill source repo: `D:\project\my-ai-skills`
- Confirmed base branch: `main`
- Confirmed execution branch: `feat/docs-governor-skill`
- Confirmed execution worktree: `D:\project\MyFlowHub3\worktrees\docs-governor-skill`

### Stage 1 - Requirements Analysis

#### Goal

- Create a reusable `docs-governor` skill that governs project documentation instead of merely editing Markdown.
- Make the skill portable across projects, with Codex-first packaging and a compatibility-friendly layout for future Claude support.
- Enforce a durable documentation model centered on:
  - `requirements`
  - `specs`
  - `plan`
  - `change`
  - `lessons`

#### Scope

- Must:
  - Create a Git-managed skill source repository.
  - Create a Codex-discoverable skill package.
  - Encode document taxonomy, routing rules, indexing rules, requirement-impact checks, lessons handling, and copy-based sync guidance.
  - Include a deterministic bootstrap script that can create the recommended docs tree in a target project.
- Optional:
  - Keep the repository layout ready for future Claude-specific packaging.
  - Generate UI metadata for Codex skill discovery.
- Out of scope:
  - Modifying `D:\project\MyFlowHub3\docs` in this workflow.
  - Installing to Claude runtime directories in this workflow.
  - Migrating historical docs from existing projects.

#### Use Cases

- A user asks where a new document belongs.
- A user asks to create or repair a project's docs structure.
- A user asks to write a change note and must first verify whether requirements or specs changed.
- A user asks to add a postmortem / lesson and link it back to change history and stable docs.
- A user wants a reusable, versioned skill repository that can later support multiple AI tools.

#### Functional Requirements

- The skill must classify document work before editing.
- The skill must route content to one canonical category:
  - `requirements`: long-lived needs, boundaries, and acceptance criteria
  - `specs`: technical contracts, architecture constraints, interfaces, generated-doc guardrails
  - `plan`: workflow planning archive
  - `change`: workflow result archive
  - `lessons`: recurring problems, root causes, prevention guidance
- The skill must force a requirement/spec impact check before writing `plan` or `change`.
- The skill must define index update obligations whenever a new doc is created or renamed.
- The skill must protect generated or semi-generated docs from unsafe manual edits.
- The skill repository must support copy-based installation into `~/.codex/skills`.

#### Non-functional Requirements

- Performance:
  - Prefer index-first navigation over repository-wide ad hoc scanning.
  - Keep skill instructions concise and push detail into references.
- Readability:
  - Use stable terminology and explicit decision rules.
  - Keep templates simple and auditable.
- Extensibility:
  - Isolate shared content from platform-specific wrappers.
  - Allow future Claude packaging without rewriting core references.
- Maintainability:
  - Use a single Git source of truth.
  - Treat install directories as disposable copies.

#### Inputs / Outputs

- Inputs:
  - User doc task intent
  - Project docs topology
  - Target scope or module
  - Existing requirements/specs/change context
- Outputs:
  - Document classification
  - Target path recommendation
  - Required prerequisite reads
  - Required index updates
  - Requirement/spec impact conclusion
  - Optional bootstrap action for missing docs tree

#### Edge Cases and Exceptions

- Projects may not yet have the recommended docs tree.
- Historical docs may still use deprecated names such as `plan_archive`.
- Generated docs may contain protected regions.
- A single user request may involve both stable docs and archival docs.
- Some projects may not want Claude packaging yet; Codex must still work independently.

#### Acceptance Criteria

- The repository contains a usable `docs-governor` Codex skill package.
- The skill can explain and enforce the five-category docs model.
- The repository contains copy-based sync / install guidance and supporting scripts.
- The repository contains a bootstrap script for the recommended docs tree.
- The repository validates cleanly with the provided skill validation tooling.

#### Risks

- Overloading the skill with project-specific assumptions would reduce portability.
- Mixing long-lived truth with archive docs would make routing rules ambiguous.
- Platform-specific wrappers may drift if shared content boundaries are unclear.

#### Issue List

- None.
- Blocked: No
- Exit criteria met for Stage 1.

### Stage 2 - Architecture Design

#### Overall Solution

- Build a single Git source repository at `D:\project\my-ai-skills`.
- Create one skill named `docs-governor`.
- Package the skill as Codex-first, with `skills/docs-governor` as the source package and `dist/codex/docs-governor` as the installable Codex copy target.
- Keep the skill body and bundled resources platform-neutral where practical so a future Claude wrapper can reuse the same core content.
- Use copy-based installation:
  - source repo -> build / dist -> copy into `C:\Users\HelloWorld\.codex\skills\docs-governor`

#### Alternatives Considered

- Single monolithic `SKILL.md` with no references:
  - Rejected because it would become large, fragile, and hard to maintain.
- Two separate skills (`docs-governor` and `docs-bootstrap`):
  - Rejected for now because governance and bootstrap belong to the same domain and would duplicate context.
- Directly editing `~/.codex/skills` as the source of truth:
  - Rejected because install directories are poor long-term sources of truth.

#### Module Responsibilities

- `skills/docs-governor/SKILL.md`
  - Provide Codex trigger metadata and the core operational flow.
- `skills/docs-governor/references/*`
  - Hold taxonomy, routing, indexing, requirement-impact, lessons, and templates.
- `skills/docs-governor/scripts/*`
  - Hold deterministic helpers such as docs tree bootstrap.
- `skills/docs-governor/agents/openai.yaml`
  - Provide Codex UI metadata generated from the skill definition.
- `tools/sync-skills.ps1`
  - Build and copy the Codex package into the install directory.
- `tools/validate-skills.ps1`
  - Validate source structure and invoke provided quick validation.
- `manifests/docs-governor.json`
  - Record version/build metadata used during copy-based sync.

#### Data / Call Flow

1. Edit the skill source under Git.
2. Validate source structure and metadata.
3. Build the Codex installable package under `dist/codex/docs-governor`.
4. Copy the built package into `~/.codex/skills/docs-governor`.
5. When invoked, the skill:
   - classifies the doc task
   - identifies required prerequisite reads
   - decides the canonical destination
   - enforces requirement/spec impact checks
   - updates indexes or instructs the user to do so
   - optionally bootstraps the docs tree when absent

#### Interface Drafts

- Bootstrap script:
  - Input:
    - target project root
    - optional module buckets
    - optional overwrite / dry-run flags
  - Output:
    - created directories
    - created files
    - skipped paths
- Sync script:
  - Input:
    - skill name
    - target platform (`codex`)
    - copy mode only
  - Output:
    - built dist path
    - install target path
    - copied file summary

#### Error Handling and Safety

- Treat install directories as write-only deployment targets; never edit them manually.
- Fail fast if required source files for a package are missing.
- Refuse silent overwrites of incompatible structures unless explicitly requested.
- Preserve generated metadata and validate before copying.
- Document that generated or protected doc regions must not be edited manually.

#### Performance and Testing Strategy

- Keep the skill body small and route detailed rules into references.
- Use deterministic scripts for structure creation and package sync.
- Validate with:
  - repository structure checks
  - `quick_validate.py`
  - smoke test of copied Codex package

#### Extensibility Design Points

- Shared / platform split allows later Claude packaging without rewriting references.
- Manifest-driven metadata allows future per-skill versioning.
- Bootstrap script can later support custom module buckets or alternative docs layouts.

#### Issue List

- None.
- Blocked: No
- Exit criteria met for Stage 2.

### Stage 3.1 - Planning

#### Project Goal and Current State

- Goal:
  - Deliver a Git-managed, reusable `docs-governor` skill repository with Codex packaging, copy-based sync, and a docs-tree bootstrap script.
- Current state:
  - The repository exists and has a dedicated worktree, but no skill content has been implemented yet.

#### Executable Task List

- [ ] DG-1 - Initialize the skill source layout
- [ ] DG-2 - Author the skill content and references
- [ ] DG-3 - Implement bootstrap, validation, and copy-sync scripts
- [ ] DG-4 - Validate, review, and archive the workflow

#### Task Details

##### DG-1 - Initialize the skill source layout

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\docs-governor-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\docs-governor-skill\plan.md`
- Goal:
  - Create the repository layout and initialize the skill package using the official `skill-creator` tooling.
- Files / Modules:
  - `skills/docs-governor/**`
  - `dist/**`
  - `manifests/**`
  - `tools/**`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\skills\docs-governor\**`
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\dist\**`
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\manifests\**`
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\tools\**`
- Acceptance:
  - The repository has the intended high-level layout.
  - The skill package exists with valid Codex-facing scaffolding.
- Test Points:
  - Expected directories exist.
  - No missing required skill files.
- Rollback:
  - Remove created layout files and revert the commit.

##### DG-2 - Author the skill content and references

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\docs-governor-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\docs-governor-skill\plan.md`
- Goal:
  - Encode the docs governance rules, taxonomy, impact checks, indexing rules, and templates.
- Files / Modules:
  - `skills/docs-governor/references/**`
  - `skills/docs-governor/SKILL.md`
  - `skills/docs-governor/agents/openai.yaml`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\skills\docs-governor\references\**`
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\skills\docs-governor\SKILL.md`
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\skills\docs-governor\agents\openai.yaml`
- Acceptance:
  - The skill can route all five doc categories.
  - The skill explicitly enforces requirement/spec impact checks and lesson handling.
- Test Points:
  - Reference files cover the required categories.
  - Skill frontmatter and body remain concise and valid.
- Rollback:
  - Revert the skill content changes.

##### DG-3 - Implement bootstrap, validation, and copy-sync scripts

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\docs-governor-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\docs-governor-skill\plan.md`
- Goal:
  - Add deterministic scripts for docs tree initialization, skill validation, and copy-based Codex sync.
- Files / Modules:
  - `skills/docs-governor/scripts/**`
  - `tools/sync-skills.ps1`
  - `tools/validate-skills.ps1`
  - `manifests/docs-governor.json`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\skills\docs-governor\scripts\**`
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\tools\sync-skills.ps1`
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\tools\validate-skills.ps1`
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\manifests\docs-governor.json`
- Acceptance:
  - The docs bootstrap script can create the recommended docs tree.
  - The sync script builds and copies the Codex package to `~/.codex/skills/docs-governor`.
  - The validation script checks the repository and skill package.
- Test Points:
  - Dry-run or real-run script execution succeeds.
  - Built package exists under `dist/codex/docs-governor`.
  - Installed package appears under `C:\Users\HelloWorld\.codex\skills\docs-governor`.
- Rollback:
  - Revert scripts and generated manifests / dist output.

##### DG-4 - Validate, review, and archive the workflow

- Owner: Main Agent
- Worktree: `D:\project\MyFlowHub3\worktrees\docs-governor-skill`
- Plan Path: `D:\project\MyFlowHub3\worktrees\docs-governor-skill\plan.md`
- Goal:
  - Review the implementation, record results, and archive the workflow.
- Files / Modules:
  - `plan.md`
  - `docs/change/YYYY-MM-DD_docs-governor.md`
- Write Set:
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\plan.md`
  - `D:\project\MyFlowHub3\worktrees\docs-governor-skill\docs\change\**`
- Acceptance:
  - Review findings are recorded.
  - Change archive exists and maps back to DG-1 through DG-4.
- Test Points:
  - Archive document created with required sections.
  - Review conclusions reference actual verification steps.
- Rollback:
  - Revert archive and review notes if the workflow is discarded.

#### Dependencies

- DG-1 precedes DG-2 and DG-3.
- DG-2 must complete before final validation of DG-3.
- DG-4 depends on DG-1 through DG-3.

#### Risks and Notes

- The skill-creator scripts are external inputs and must be reused carefully instead of copied manually.
- Platform compatibility must not bloat the Codex skill body.
- Copy-based sync must not treat `~/.codex/skills` as a source of truth.
- Layout adjustment recorded during planning refinement:
  - Use `skills/docs-governor` as the source package instead of adding an extra source-time `codex/` wrapper.
  - Reason: aligns directly with `init_skill.py`, reduces indirection, and keeps the current implementation smaller without blocking future wrappers.

#### Parallelism Assessment

- Two implementation slices exist (`DG-2` content and `DG-3` tooling), but they are coupled through shared paths, packaging conventions, and validation expectations.
- Sub-agent delegation is not used in this workflow because the current session has not received explicit user authorization for sub-agent use under the active platform policy.

#### Issue List

- None.
- Blocked: No
- Exit criteria met for Stage 3.1.

### Stage 3.2 - Implementation

#### DG-1 - Initialize the skill source layout

- Completed.
- Created source package skeleton with the official `init_skill.py` script at:
  - `skills/docs-governor`
- Created repository support layout:
  - `tools/`
  - `manifests/`
  - `.gitignore`

#### DG-2 - Author the skill content and references

- Completed.
- Replaced template `SKILL.md` with a concise governance workflow.
- Added references:
  - `taxonomy.md`
  - `routing-rules.md`
  - `indexing-rules.md`
  - `requirement-impact.md`
  - `lessons-rules.md`
  - `templates.md`

#### DG-3 - Implement bootstrap, validation, and copy-sync scripts

- Completed.
- Added deterministic docs bootstrap script:
  - `skills/docs-governor/scripts/bootstrap_docs_tree.py`
- Added repository tooling:
  - `tools/validate-skills.ps1`
  - `tools/sync-skills.ps1`
- Added install/build manifest:
  - `manifests/docs-governor.json`
- Performed copy installation into:
  - `C:\Users\HelloWorld\.codex\skills\docs-governor`

### Stage 3.3 - Code Review

#### Review Result

- Requirements coverage: Passed
  - The skill covers routing, docs-tree bootstrap, index maintenance, requirement/spec impact checks, and lessons handling.
- Architecture rationality: Passed
  - The repository keeps one Git source package and one copy-installed Codex target, which matches the confirmed copy sync model.
- Performance risk: Passed
  - The skill favors index-first reads and concise references; no unnecessary heavy automation was introduced.
- Readability and consistency: Passed
  - File names, responsibilities, and templates are explicit and stable.
- Extensibility and configurability: Passed
  - The source package remains platform-neutral enough for future wrappers, and the bootstrap script supports optional module buckets.
- Stability and security: Passed
  - The sync flow is one-way from source to install target, and validation fails fast on missing required files.
- Test coverage: Passed with noted scope
  - `quick_validate.py` passed.
  - The bootstrap script created a sample docs tree successfully.
  - Copy-based sync produced an installable package under `~/.codex/skills`.
  - Scope note: no Claude-side packaging or runtime smoke test was attempted in this workflow.
- Sub-agent governance and audit: Passed
  - No sub-agents were used.
  - Reason: explicit sub-agent authorization was not present in the current session policy.
- Conclusion: Passed
  - No blocking review findings remain.

### Stage 4 - Change Archive

- Change archive document created:
  - `docs/change/2026-03-22_docs-governor-skill.md`
- Stage 4 complete.
