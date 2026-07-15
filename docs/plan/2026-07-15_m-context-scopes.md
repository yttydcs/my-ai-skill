# Plan - m-context Local And Global Scopes

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `feat/m-context-scopes`
- Base: `main` at `2aac6d5`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\worktrees\m-context-scopes\docs`
- Code Repos: `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\m-context-scopes`
- Current Stage: `4 - Archived`

## Stage Records

### Initialization

- `guide.md`: read; every repository modification must be committed with an English message consistent with history.
- Project/docs/code repo confirmation: this repository owns the source skill, loader, tests, manifests, workflow references, and governed docs.
- Base/worktree confirmation: clean `main` baseline; dedicated `feat/m-context-scopes` branch and worktree created under the project `worktrees` directory.

### Discuss - Discovery And Requirements Shaping

#### Goal

Extend `$m-context` from a single user-global store to deterministic project-local and user-global stores without making the user repeat environment details or secrets.

#### Scope

- Local context root: `<docs_root>/context`.
- Global context root: existing `M_CONTEXT_HOME`, then `<CODEX_HOME>/m-contexts`, then `~/.codex/m-contexts` resolution.
- Unqualified loads use local-first exact lookup and fall back to global only when the local context file does not exist.
- Explicit `local:` and `global:` prefixes select exactly one scope.
- Plaintext credentials and other secrets remain allowed and Agent-readable.
- No automatic `.gitignore`, `.git/info/exclude`, staging, commit, or push mutation for context files.

#### Assumptions

- `docs_root` is resolved by the selected workflow or `$m-docs` and passed explicitly to the loader. The loader will not guess a project by walking parent directories.
- A missing local root or exact local file counts as “not found” for an unqualified load. A local file that exists but cannot be resolved, validated, decoded, read, or sectioned is a local error and blocks fallback.
- When an unqualified invocation has no resolvable `docs_root`, the global scope remains usable and the result reports that local lookup was unavailable.

#### Open Questions

- None blocking. The scope order, local path, secret policy, and Git-ignore policy were explicitly confirmed.

#### Options Considered

1. Search local and global and merge both bodies.
2. Search local first, then fall back to global only when local is absent.
3. Search only one configured root and require users to switch configuration manually.

#### Rejected Options

- Merge both bodies: rejected because duplicate sections and credentials would produce ambiguous task context.
- One manually switched root: rejected because it does not provide the requested project-local/global reuse model.
- Automatic Git ignore changes: rejected by the user; the skill must not mutate repository ignore configuration.
- Loader-side parent scanning: rejected because it can bind to the wrong project or docs root.

#### Recommended Direction

Use a scoped resolver with `auto`, `local`, and `global` modes. The Agent parses `local:` / `global:` and supplies the active `docs_root`; the standard-library loader owns exact path resolution, local-first fallback, section parsing, and source diagnostics. Keep content on stdout and source/error diagnostics on stderr so metadata never contaminates loaded Markdown.

#### Research Summary

No web research is required. This change is governed by confirmed local workflow requirements and the existing repository contracts.

#### Worktree / Branch / Docs Root Status

- Branch and worktree are ready.
- The selected docs root is the worktree `docs` directory because this repository is explicitly the canonical docs owner.
- The local runtime context directory will be `<docs_root>/context`; it is not a governed-doc category and is not created during planning.

#### Issue List

- None blocking planning.

### Plan - Requirements And Architecture

#### Discussion Summary

The existing v1 loader resolves exactly one global root. The requested extension adds project-local reuse while preserving the global store and exact-name behavior. The key semantic constraint is absence-only fallback: global data may fill a missing local context, but must never mask a broken or invalid local context.

#### Accepted / Rejected Requirements

- Accepted: local/global scopes, `<docs_root>/context`, local-first fallback, strict explicit scopes, plaintext secrets, source reporting, no automatic Git mutation.
- Rejected: merged local/global content, fuzzy normal loading, encryption requirements, automatic ignore entries, and implicit project-root scanning.

#### Requirements Analysis

##### Goal

Make reusable Agent context project-aware without sacrificing deterministic lookup, path safety, backward compatibility, or intentional plaintext secret access.

##### Scope

- Extend the loader API and CLI.
- Update skill usage, storage, discovery, create/update, and composition rules.
- Reserve `docs_root/context` as non-governed runtime context data in docs governance guidance.
- Add focused tests and complete normal skill validation/synchronization after approval.

##### Use Cases

- `$m-context 测试环境` loads `docs/context/测试环境.md` when present.
- The same invocation loads global `测试环境.md` only when the local exact file is absent.
- `$m-context local:测试环境` and `$m-context global:测试环境` select one store without fallback.
- `$m-test $m-context nas配置` receives the selected context before testing starts.
- `list` and `find` expose the source scope without reading secret bodies.
- A user can save project-specific credentials locally or reusable credentials globally.

##### Functional Requirements

- Parse an optional scope prefix before the context name and optional `#section` selector.
- Derive local root only as `<explicit docs_root>/context`.
- Preserve current global root precedence.
- In `auto`, probe the local exact path first; probe global only for local absence.
- If local exists, all subsequent local errors are terminal.
- Report selected scope and path without echoing body values.
- For creation of a new name, require `local:` or `global:`. For an unqualified update, update the exact location selected by normal lookup; if neither exists, ask for scope.
- Never create or edit Git ignore configuration and never stage, commit, or push a context file as an implicit side effect.

##### Non-functional Requirements

- Standard library only; preserve Windows Unicode behavior.
- Maintain path containment independently for each root.
- Avoid reading file bodies during list/find or fallback probing.
- Keep content output distinct from diagnostics.
- Preserve the existing unqualified global behavior when no project docs root is available.

##### Inputs / Outputs

- Input name syntax: `[local:|global:]<name>[#<section>]`.
- Loader inputs: `scope`, optional explicit `docs_root`, global environment, name, and optional section.
- Load stdout: selected Markdown only.
- Load stderr/status: selected scope and resolved path, or an actionable error.
- Discovery output: scope-qualified names ordered local before global; duplicate stems remain separately visible.

##### Edge Cases

- Local and global both contain the same name.
- Local root or file is missing.
- Local file exists but is unreadable, invalid UTF-8, outside the root through a link, or lacks the requested section.
- `docs_root` is unavailable for explicit `local:`.
- Global root is missing after local absence.
- Unicode names, reserved Windows names, duplicate headings, and section fences.
- New unqualified save has no existing target.
- Context contains plaintext secrets while the surrounding workflow writes plans, docs, screenshots, or reports.

##### Acceptance Criteria

- Unqualified loading selects local when both copies exist and reports `local`.
- Unqualified loading selects global only when the local exact context is absent and reports `global`.
- Existing-but-broken local content fails without global fallback.
- Explicit scopes never cross-fallback.
- Local path resolution requires an explicit docs root and remains contained within `<docs_root>/context`.
- List/find identify scope without reading context bodies.
- New saves require an explicit scope; updates preserve unrelated content and secrets.
- No code path changes `.gitignore`, `.git/info/exclude`, Git config, index state, commits, or remotes for context data.
- Existing section extraction and global-only use cases remain passing.

##### Risks

- Treating every filesystem error as absence could hide a broken local context.
- Mixing source metadata into stdout could pollute downstream Agent context.
- Guessing docs roots could load credentials from the wrong project.
- Bulk Git operations outside this skill could still include an unignored `docs/context` file; workflow guidance must mark the directory as opt-in data rather than governed documentation.

#### Architecture Design

##### Overall Solution

Introduce a small scope-aware resolution layer around the current single-root primitives:

1. Resolve the global root with the existing precedence function.
2. Resolve the local root only from an explicit `docs_root` argument.
3. Classify an exact local candidate as absent, selected, or failed.
4. In `auto`, continue to global only for absent; otherwise return or raise the local result.
5. Load and section the selected file with the current UTF-8 and Markdown logic.
6. Return structured location metadata internally while keeping CLI body output on stdout.

##### Alternatives Considered

- Environment variable for local docs root: not the primary contract because workflow-resolved `docs_root` is more explicit; a future alias can be added separately if needed.
- Recursive project discovery: excluded to prevent cross-project selection.
- One combined virtual root: excluded because it obscures shadowing and error provenance.

##### Module Responsibilities

- `context_loader.py`: scope enum/model, root derivation, exact candidate classification, fallback, metadata, CLI flags, and existing content parsing.
- `SKILL.md`: invocation parsing, docs-root handoff, source announcement, creation/update behavior, composition, and Git side-effect prohibition.
- `context-format.md`: local/global locations, naming examples, section rules, and plaintext-secret boundary.
- `m-docs` references: classify `context/` as runtime context data outside governed-doc routing and forbid automatic Git mutations.
- Tests: resolver truth table, CLI behavior, compatibility, safety, and no-body-read discovery.
- Stable docs: preserve request traceability and define the target feature/requirement/spec contract with planned status until implementation completes.

##### Data / Call Flow

`invocation -> parse scope/name/section -> resolve docs_root if needed -> select exact local/global file -> read selected UTF-8 Markdown -> optional section extraction -> provide content to consuming skill`

##### Interface Drafts

```text
$m-context 测试环境
$m-context local:测试环境
$m-context global:测试环境
$m-context local:测试环境#启动方式
$m-context list
$m-context find nas
```

```text
context_loader.py root [--scope local|global] [--docs-root PATH]
context_loader.py list [--scope auto|local|global] [--docs-root PATH]
context_loader.py find <query> [--scope auto|local|global] [--docs-root PATH]
context_loader.py load <name> [--scope auto|local|global] [--docs-root PATH] [--section HEADING]
```

`root` without new flags remains the existing global-root query for compatibility. Auto discovery emits scope-qualified names. A successful load writes Markdown to stdout and a concise selected-source diagnostic to stderr.

##### Error Handling and Safety

- Use a dedicated not-found classification rather than string-matching generic errors.
- Only local root/file absence enables auto fallback.
- Permission, resolution, containment, file type, UTF-8, and section errors fail in their selected scope.
- Explicit local without `docs_root` fails with a request to resolve or supply it.
- Validate names before probing either root; validate containment after resolution in each root.
- Do not copy secret bodies into plan, stable docs, archives, logs, screenshots, or confirmation messages.

##### Performance and Testing Strategy

- Candidate selection performs metadata/path checks only; only the selected file body is read.
- List/find scan `*.md` filenames in at most two roots and never bodies.
- Unit tests use temporary local/global/docs roots and subprocess CLI coverage.
- Run focused unit tests, repository skill validation for `m-context` and affected governance skills, source/install synchronization, parity checks, and `git diff --check`.

##### Extensibility Design Points

- Structured scope/location results can later support more named stores without changing content parsing.
- Absence-only fallback remains a reusable resolution policy.
- Multi-source merge, encryption, remote stores, and secret managers remain outside this contract.

#### Issue List

- None blocking execution after approval.

### Stage 3.1 - Planning

#### Project Goal and Current State

The repository has an active global-only `$m-context` implementation with focused tests and installed-skill synchronization. This plan extends its resolution contract while preserving current global operation and section semantics.

#### Docs Governance Routing Decision

Using `$m-docs`: original request evidence is added to `docs/intake`; target user behavior, durable intent, and technical contracts are clarified in the existing feature, requirements, and spec documents. No architecture decision record is needed because the choice is explicit, localized, and reversible. `docs/context` is runtime context data, not a governed-doc category, and no directory or ignore entry is created by planning.

#### Related Intake / Features / Requirements / Specs / Decisions / Lessons

- Intake: `docs/intake/2026-07-13_m-context.md`, `docs/intake/2026-07-15_m-context-scopes.md`
- Feature: `docs/features/m-context.md`
- Requirements: `docs/requirements/m-context-skill.md`
- Spec: `docs/specs/m-context-skill.md`
- Decisions: none
- Lessons: `docs/lessons/windows-symlink-test-privilege.md`, `docs/lessons/windows-skill-parity-line-endings.md`

#### Stable Docs Impact

- Intake impact: add the confirmed local/global request and explicit no-ignore constraint.
- Feature impact: clarify target scope selection, fallback, save/update, and source-reporting behavior.
- Requirements impact: clarify durable local/global and Git-side-effect requirements.
- Specs impact: replace the planned single-root technical contract with a scoped resolver contract while clearly marking delivery pending.
- Decision impact: none; no ADR required.
- Lessons known at planning time: reuse Windows symlink privilege and source/install line-ending guidance; no new lesson yet.

#### Executable Task List

- `MCS-1`: implement scoped resolver and CLI contract.
- `MCS-2`: update skill, format, and docs-governance instructions.
- `MCS-3`: add focused scope, fallback, safety, and compatibility tests.
- `MCS-4`: finalize stable docs, validate, synchronize installed skills, check parity, and commit execution changes.
- `MCS-5`: do not add automatic Git-ignore or Git-state management.
- `MCS-6`: do not merge local and global context bodies.

#### Execution Scope After Approval

##### Will Execute

- `MCS-1`, `MCS-2`, `MCS-3`, `MCS-4`

##### Will Not Execute Now

- `MCS-5`: explicitly rejected by the user; context scope support must not modify ignore rules or Git state.
- `MCS-6`: out of scope; the confirmed behavior is precedence/fallback, not multi-source merging.

#### Task Details

##### MCS-1 - Implement Scoped Resolution And CLI

- Owner: main Agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\m-context-scopes`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context-scopes\plan.md`
- Goal: add `auto`, `local`, and `global` selection with absence-only fallback and source metadata.
- Files / Modules: `skills/m-context/scripts/context_loader.py`
- Write Set: scope/location types, local-root derivation, candidate classification, selection functions, CLI flags/output.
- Acceptance: truth table and interface drafts above are implemented; old unqualified global root query remains compatible.
- Test Points: unit API and subprocess CLI paths covered in `MCS-3`.
- Rollback: revert the loader change; the existing global-only code remains the baseline.

##### MCS-2 - Align Skill And Docs Governance Contracts

- Owner: main Agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\m-context-scopes`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context-scopes\plan.md`
- Goal: make scope syntax, docs-root handoff, create/update behavior, secret handling, and no-Git-side-effect rules operationally explicit.
- Files / Modules: `skills/m-context/SKILL.md`, `skills/m-context/references/context-format.md`, `skills/m-docs/references/taxonomy.md`, `skills/m-docs/references/routing-rules.md`, and affected umbrella references only if validation exposes a routing contradiction.
- Write Set: workflow instructions and non-governed `context/` classification; no runtime context data.
- Acceptance: the Agent can deterministically parse, load, save, and report either scope; docs governance does not index/archive/stage context data implicitly.
- Test Points: skill validation and contradiction search for scope, fallback, ignore, stage, and commit wording.
- Rollback: revert instruction/reference edits independently of the loader.

##### MCS-3 - Add Scoped Behavior Regression Tests

- Owner: main Agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\m-context-scopes`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context-scopes\plan.md`
- Goal: prove precedence, strict errors, path safety, discovery, and global compatibility.
- Files / Modules: `tests/test_m_context_loader.py`
- Write Set: temporary-root helpers and focused API/CLI test cases.
- Acceptance: tests cover local wins, absent-local fallback, broken-local no-fallback, explicit scope isolation, missing docs root, duplicate names in discovery, sections, Unicode, and source diagnostics.
- Test Points: `python -m unittest tests.test_m_context_loader`; retain the documented Windows symlink skip when privilege is unavailable.
- Rollback: remove new tests together with the corresponding behavior change.

##### MCS-4 - Finalize Docs, Validate, Sync, And Commit

- Owner: main Agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\m-context-scopes`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context-scopes\plan.md`
- Goal: make delivered truth and installed copies consistent and leave an auditable execution commit.
- Files / Modules: `docs/features/m-context.md`, `docs/requirements/m-context-skill.md`, `docs/specs/m-context-skill.md`, affected indexes, manifests only if validation requires metadata changes, installed skill copies through the repository sync tool.
- Write Set: remove planned-status markers after delivery, record final contract, validation/sync outputs, and English commit.
- Acceptance: unit tests and skill validation pass; installed/source parity passes with known Windows line-ending rules; `git diff --check` passes; no context data or Git ignore file is changed.
- Test Points: `tools/validate-skills.ps1` for `m-context` and affected `m-docs`/umbrella packages; `tools/sync-skills.ps1` for changed skills; parity and working-tree review.
- Rollback: revert execution commit and re-sync the previous installed versions.

##### MCS-5 - Exclude Automatic Git Ignore Or Git State Changes

- Owner: none
- Worktree: not applicable
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context-scopes\plan.md`
- Goal: record the explicit non-requirement.
- Files / Modules: `.gitignore`, `.git/info/exclude`, Git config/index/remotes.
- Write Set: none.
- Acceptance: these files/states are untouched by implementation and context operations.
- Test Points: final diff/status inspection.
- Rollback: not applicable.

##### MCS-6 - Exclude Local And Global Body Merging

- Owner: none
- Worktree: not applicable
- Plan Path: `D:\project\my-ai-skills\worktrees\m-context-scopes\plan.md`
- Goal: preserve the confirmed single-source selection model.
- Files / Modules: resolver and composition behavior.
- Write Set: none.
- Acceptance: exactly one context file supplies a normal load.
- Test Points: precedence tests assert one source only.
- Rollback: not applicable.

#### Dependencies

- `MCS-1` defines the API consumed by `MCS-2` and tested by `MCS-3`.
- `MCS-2` and `MCS-3` may proceed after the resolver interface is stable.
- `MCS-4` depends on `MCS-1` through `MCS-3` passing.

#### Risks and Notes

- No runtime or test code has been changed during planning.
- Context files may contain plaintext secrets by design. Users remain responsible for any manual Git publication decision because automatic ignore and staging policy changes are excluded.
- Planning docs describe a target contract and remain marked planned until execution completes.

#### Parallelism Assessment

The implementation is small and tightly coupled across one loader contract, one skill, and one test module. Parallel sub-agents would increase merge and semantic-drift risk, so the next execution phase should remain single-Agent unless the user explicitly requests delegation.

#### Issue List

- None blocking approval.

## Approval Gate

- Plan status: approved by the user's `$m-execute` invocation.
- Blocked: no.
- Entered execution for `MCS-1` through `MCS-4`.
- Implementation sub-agents were not used because the loader, instructions, tests, and validation share one tightly coupled contract and host policy did not authorize delegation.

## Stage 3.2 - Execution Status

- `MCS-1`: completed. Added scoped resolver models, local-root derivation, absence-only auto fallback, strict explicit scopes, source diagnostics, and scoped CLI discovery/loading.
- `MCS-2`: completed. Updated `$m-context` usage and authoring rules plus `$m-docs` taxonomy/routing boundaries for non-governed `context/` data and no automatic Git mutations.
- `MCS-3`: completed. Expanded focused coverage from 11 to 19 tests; 18 pass and the existing Windows symlink privilege case is skipped when unavailable.
- `MCS-4`: completed. Stable docs are active, `m-context` and `m-docs` source/install copies are synchronized with exact post-sync parity, focused tests and skill validators pass, and the execution diff is clean. The repository commit is recorded by the execution handoff.
- `MCS-5`: not executed as required. No Git ignore or context-data Git-state automation was added.
- `MCS-6`: not executed as required. Normal loads select exactly one source and never merge bodies.

## Stage 4 - Archive Status

- `$m-docs` routing and stable-doc impact checks: completed.
- Intake impact: updated and linked to the completed change.
- Feature impact: updated and active.
- Requirements impact: updated and active.
- Specs impact: updated and active.
- Decision impact: none; no ADR was required.
- Lessons impact: updated with `python-cache-skill-sync.md`; existing Windows parity and symlink lessons were reused.
- Change archive: `docs/change/2026-07-15_m-context-scopes.md`.
- Plan archive: `docs/plan/2026-07-15_m-context-scopes.md`.
- Indexes: change, plan, and lessons indexes updated; root topology unchanged.
- Heavy `$m-test`: skipped with accepted low residual risk because focused validation covers the standard-library, non-UI, non-service change.
- Publication: local-only; no push, remote, backup, or publication action was requested.
