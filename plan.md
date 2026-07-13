# Plan - m-context Reusable Agent Context

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `feat/m-context`
- Base: `main` at `ab8757f14db38ca670db41abfc6ed7285699b68b`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\worktrees\m-context\docs`
- Code Repos: `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\m-context`
- Current Stage: `$m-plan`, awaiting user approval

## Stage Records

### Initialization

- `guide.md`: read; every modification must be committed automatically with an English commit message following repository history.
- Project/docs/code repo confirmation: one Git repository; governed docs are this repository's `docs` tree.
- Base/worktree confirmation: clean `main`; dedicated branch `feat/m-context`; dedicated worktree created under `D:\project\my-ai-skills\worktrees\m-context`.
- Main repo restriction: the main checkout remains control-plane only; planning and future implementation occur in the dedicated worktree.

### Discuss - Discovery And Requirements Shaping

#### Goal

Add reusable external Agent context so users can save operational information once and load it by name alongside another skill.

#### Scope

- Standalone `$m-context` skill.
- User-level plaintext Markdown storage.
- Whole-file and heading-level loading.
- Context-first composition such as `$m-test $m-context nas配置`.
- Context discovery through list and find operations.

#### Assumptions

- The local machine and selected context root are trusted by the user.
- The Agent is permitted to read and use plaintext passwords, tokens, keys, and other sensitive values in selected contexts.
- Context data changes independently from the Git-managed skill package.

#### Open Questions

- None blocking for version one.

#### Options Considered

1. Store contexts inside the skill package.
2. Store contexts as separate user-local Markdown files and use a loader skill.
3. Add encryption, OS credential storage, or a remote secret manager.

#### Rejected Options

- Skill-package storage: couples personal data and secrets to distribution and reinstall flows.
- Encryption or secret-manager integration: explicitly unnecessary for the user's trusted local Agent automation use case.
- Plan-only context fields: do not solve reusable cross-task loading.

#### Recommended Direction

Create `$m-context` as a thin loader skill. Resolve one configurable context root, keep each context in one UTF-8 Markdown file, use headings for progressive loading, and load selected content before co-invoked skills act.

#### Research Summary

Security research was considered during discussion, then excluded from the chosen design after the user clarified that plaintext Agent-readable storage is intentional. No external source constrains the implementation plan.

#### Worktree / Branch / Docs Root Status

- Worktree: ready
- Branch: ready
- Docs root: confirmed
- Stable planning docs: added in this worktree

#### Issue List

- None.

### Plan - Requirements And Architecture

#### Discussion Summary

The requirement is coherent and intentionally favors low-friction local automation over encrypted secret management. The storage directory is separate from Git-managed skill source, but its complete contents are readable by the Agent.

#### Accepted / Rejected Requirements

- Accepted: plaintext secret storage, direct Agent readability, Markdown sections, skill composition, deterministic lookup, configurable global root.
- Rejected: encryption, credential vaults, remote synchronization, silent fuzzy resolution, storing personal context inside the skill package.

#### Requirements Analysis

##### Goal

Eliminate repeated manual entry of stable operational details while preserving explicit user control over which context is loaded.

##### Scope

- New skill package, manifest, format reference, deterministic loader, tests, umbrella integration, stable docs, validation, and local installation sync.

##### Use Cases

- Load NAS connection and credential details before testing.
- Load a named subsection from a larger operational context.
- Find existing contexts by filename.
- Use plaintext keys or passwords for an authorized Agent task.

##### Functional Requirements

- Root resolution: `M_CONTEXT_HOME`, then `CODEX_HOME/m-contexts`, then `~/.codex/m-contexts`.
- Exact Unicode filename-stem loading.
- Optional exact Markdown heading extraction with nested subsections.
- List and filename-find commands that do not expose file bodies.
- Context-first composition with any co-invoked skill.
- Explicit failure on missing, ambiguous, unreadable, or unsafe inputs.

##### Non-functional Requirements

- Standard-library implementation only.
- Linear selected-file parsing.
- No scanning outside the configured root.
- Windows Unicode compatibility.
- Concise skill body with progressive disclosure.

##### Inputs / Outputs

- Inputs: context operation, name, optional section, environment-based root configuration.
- Outputs: context names for discovery or selected raw Markdown for Agent consumption; actionable errors on stderr.

##### Edge Cases

- Missing/empty root, Unicode and spaced filenames, invalid UTF-8, repeated headings, nested headings, traversal attempts, symlink/junction escape, and context files containing multiline private keys.

##### Acceptance Criteria

- Requirements and specification acceptance criteria in `docs/requirements/m-context-skill.md` and `docs/specs/m-context-skill.md` pass.
- The example `$m-test $m-context nas配置` is explicitly supported.
- Plaintext secrets reach the Agent without a redaction/encryption layer but are not unnecessarily echoed in final reporting.

##### Risks

- Plaintext contexts may be exposed by local filesystem access; this is an accepted user-owned tradeoff.
- Printing loader stdout in tool traces exposes selected content to the Agent and session; this is intentional.
- Replace-style installed-skill sync could overwrite local installed drift; pre-sync comparison is required.

#### Architecture Design

##### Overall Solution

Create a new skill using the skill-creator scaffold, add a standard-library Python loader, document the Markdown contract in one reference, register a manifest, and expose the companion skill from `m-autoflow`.

##### Alternatives Considered

- Pure instruction-only filesystem reading: simpler but inconsistent for heading extraction, path validation, and Unicode error behavior.
- Structured YAML/JSON contexts: easier parsing but less convenient for long operational notes and Markdown sections.
- Multiple project/global roots with shadowing: rejected for version one because precedence and secret duplication increase ambiguity.

##### Module Responsibilities

- `skills/m-context/SKILL.md`: trigger, operation routing, context-first composition, reporting constraints.
- `skills/m-context/references/context-format.md`: storage and authoring format.
- `skills/m-context/scripts/context_loader.py`: deterministic filesystem operations and parsing.
- `tests/test_m_context_loader.py`: focused loader regression tests.
- `skills/m-autoflow`: collection discovery and companion-skill routing.
- `manifests/m-context.json`: distribution metadata.
- Stable docs: durable behavior, intent, and technical contract.

##### Data / Call Flow

1. User invokes `$m-context` alone or beside a consuming skill.
2. Skill resolves the context root.
3. Loader validates the exact name and loads the file or requested section.
4. Agent receives raw selected Markdown as task context.
5. Consuming skill proceeds under the loaded context and higher-priority instructions.

##### Interface Drafts

```text
$m-context <name>
$m-context <name>#<section>
$m-context list
$m-context find <query>
python context_loader.py load <name> [--section <heading>]
```

##### Error Handling and Safety

- Validate all names before filesystem access.
- Keep resolved paths inside the configured root.
- Fail on duplicate headings instead of selecting silently.
- Preserve decoding and filesystem causes.
- Permit plaintext secrets by design, while avoiding unnecessary reproduction in summaries and repository artifacts.

##### Performance and Testing Strategy

- Use standard-library `unittest` with temporary directories and controlled environment variables.
- Test root precedence, listing/finding, whole-file load, nested section boundaries, duplicate/missing sections, Unicode, invalid UTF-8, and traversal/root escape.
- Validate both `m-context` and changed umbrella skills, run `git diff --check`, sync only after validation, then check source/install parity.
- Heavy `$m-test` is not planned because this change has no UI or external runtime; focused unit and packaging validation are sufficient.

##### Extensibility Design Points

- Future aliases, project-local roots, metadata/frontmatter, multiple context imports, remote synchronization, or encryption can be added without changing the basic named Markdown contract.

#### Issue List

- None.

### Stage 3.1 - Planning

#### Project Goal and Current State

The repository currently has no `$m-context` package or reusable user-local context-loading contract. Planning docs now define the new capability; no implementation files or tests have been created.

#### Docs Governance Routing Decision

Using `$m-docs`, route original request evidence to intake, user-facing workflow to features, durable capability intent to requirements, technical contracts to specs, active execution control to root `plan.md`, and completed results later to change. No ADR or lesson is required at planning time.

#### Related Intake / Features / Requirements / Specs / Decisions / Lessons

- Intake: `docs/intake/2026-07-13_m-context.md`
- Feature: `docs/features/m-context.md`
- Requirements: `docs/requirements/m-context-skill.md`
- Spec: `docs/specs/m-context-skill.md`
- Existing umbrella feature: `docs/features/m-autoflow-workflow.md`
- Existing umbrella requirements: `docs/requirements/m-autoflow-skill.md`
- Existing umbrella spec: `docs/specs/m-autoflow-skill.md`
- Decisions: none
- Lesson: `docs/lessons/windows-skill-parity-line-endings.md`

#### Stable Docs Impact

- Intake impact: add
- Feature impact: add `m-context`; clarify `m-autoflow` during integration
- Requirements impact: add `m-context`; clarify `m-autoflow` during integration
- Specs impact: add `m-context`; clarify `m-autoflow` during integration
- Decision impact: none
- Lessons known at planning time: reuse Windows installed-skill parity guidance; no new lesson yet

#### Executable Task List

- MCTX-1: Create the `m-context` skill package and manifest.
- MCTX-2: Implement and unit-test deterministic context loading.
- MCTX-3: Integrate context composition into the `m-autoflow` collection and stable docs.
- MCTX-4: Validate, synchronize, verify parity, and prepare archive handoff.
- MCTX-5: Encrypted or remotely synchronized context storage.

#### Execution Scope After Approval

##### Will Execute

- MCTX-1
- MCTX-2
- MCTX-3
- MCTX-4

##### Will Not Execute Now

- MCTX-5: explicitly out of scope; the user requires simple plaintext Agent-readable storage and does not want encryption complexity.

#### Task Details

##### MCTX-1 - Create m-context Skill Package

- Owner: main Agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\m-context`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context\plan.md`
- Goal: scaffold a valid skill, author concise routing/composition instructions, document context format, and register installation metadata.
- Files / Modules: `skills/m-context/**`, `manifests/m-context.json`
- Write Set: new `m-context` skill package and manifest only
- Acceptance: valid frontmatter and UI metadata; format and composition rules match stable docs; no context data or secrets are committed.
- Test Points: skill-creator validation, manifest inspection, reference-link inspection.
- Rollback: remove the new package and manifest before installation sync.

##### MCTX-2 - Implement Deterministic Loader And Tests

- Owner: main Agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\m-context`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context\plan.md`
- Goal: implement root resolution, list/find/load operations, heading extraction, Unicode handling, and path safety without third-party dependencies.
- Files / Modules: `skills/m-context/scripts/context_loader.py`, `tests/test_m_context_loader.py`
- Write Set: loader and its focused tests
- Acceptance: all specified success and failure paths behave deterministically with actionable errors.
- Test Points: standard-library unit suite covering environment precedence, Unicode, whole-file and section loads, duplicates, missing resources, invalid UTF-8, traversal, and resolved root escape.
- Rollback: remove loader/test files and revert SKILL instructions that call the loader.

##### MCTX-3 - Integrate With m-autoflow And Stable Docs

- Owner: main Agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\m-context`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context\plan.md`
- Goal: expose `$m-context` as a composable companion without turning it into a workflow phase.
- Files / Modules: `skills/m-autoflow/SKILL.md`, `docs/features/m-autoflow-workflow.md`, `docs/requirements/m-autoflow-skill.md`, `docs/specs/m-autoflow-skill.md`, new `m-context` stable docs and category indexes
- Write Set: umbrella discovery/integration text and governed docs
- Acceptance: umbrella routing describes context-first composition; current docs distinguish the companion loader from staged phases and the quick path; indexes remain navigable.
- Test Points: targeted text searches for command exposure, phase lists, composition order, and contradictions.
- Rollback: revert umbrella and stable-doc integration while leaving the standalone package removable.

##### MCTX-4 - Validate, Sync, Verify, And Handoff

- Owner: main Agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\m-context`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context\plan.md`
- Goal: prove the package and integration are installable and prepare honest validation evidence for archive.
- Files / Modules: `tools/validate-skills.ps1`, `tools/sync-skills.ps1`, `dist/codex/m-context/**`, installed `%USERPROFILE%/.codex/skills/m-context/**`, plan status
- Write Set: generated distribution/install copies and plan status; repository source changes only if validation exposes defects
- Acceptance: focused tests pass; skill validation passes; umbrella validation passes; sync succeeds; post-sync source/install parity passes; `git diff --check` passes; all repository modifications are committed with an English message.
- Test Points: run the commands named in the specification and record exact results; use line-ending-aware pre-sync drift checks.
- Rollback: preserve genuine installed drift before sync; remove the newly installed package if acceptance fails and no prior package existed.

##### MCTX-5 - Encrypted Or Remote Context Storage

- Owner: none in this execution phase
- Worktree: none
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context\plan.md`
- Goal: potential future encryption, credential-vault, remote sync, or multi-machine sharing.
- Files / Modules: undefined future scope
- Write Set: none
- Acceptance: not applicable in current execution.
- Test Points: not applicable.
- Rollback: not applicable.

#### Dependencies

- Existing repository validation and sync scripts.
- Skill-creator scaffold and validator available under the local Codex installation.
- A usable Python runtime for loader tests and repository skill validation.

#### Risks and Notes

- The user knowingly accepts plaintext secret storage readable by the Agent.
- The context root must not be confused with governed project docs or copied into Git artifacts.
- `sync-skills.ps1` replaces the installed destination; pre-sync drift inspection is mandatory.
- No sample file containing a real credential will be created during tests.

#### Parallelism Assessment

Do not use implementation sub-agents. The approved write sets are small and tightly coupled across skill instructions, loader behavior, tests, umbrella wording, and stable docs. Sequential main-agent implementation avoids interface drift and is required by the current host policy unless the user explicitly requests delegation.

#### Issue List

- None.

## Approval Gate

- Blocked: yes
- Do not enter execution until the user approves MCTX-1 through MCTX-4.
- Do not dispatch implementation sub-agents.
