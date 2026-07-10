# Plan - m-quick Fast Path

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `feat/m-quick`
- Base: `main` at `c597ea1`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\worktrees\m-quick\docs`
- Code Repos: `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\m-quick`
- Installed Skill Root: `C:\Users\HelloWorld\.codex\skills`
- Current Stage: `$m-archive`, archive artifacts complete and default control-plane closeout pending

## Stage Records

### Initialization

- `guide.md`: read; every repository modification must be committed automatically with an English commit message matching existing conventions.
- Project/docs/code repo confirmation: this repository is both the skill source repository and the selected governed docs repository for this workflow.
- Base/worktree confirmation: clean `main`; dedicated branch `feat/m-quick`; dedicated worktree created at the path above.
- Publication boundary: no docs remote, backup destination, or push action is selected by this plan.

### Discuss - Discovery And Requirements Shaping

#### Goal

Add a lightweight command for small, uncontroversial requirements and bug fixes. It may edit the selected repository's current checkout directly while avoiding the full discuss/plan/execute/test/archive chain, but it must read governed docs first so project context and stable constraints are not lost.

#### Scope

- Add a canonical `$m-quick` skill.
- Make `$m-quick` a standalone fast path in the `m-*` collection, not a staged `m-autoflow` phase.
- Require `$m-docs` context lookup before eligibility is decided or code is edited.
- Permit direct main-agent edits in one selected Git repository without creating a dedicated worktree or `plan.md` for the target request.
- Require a bounded eligibility gate, minimal effective validation, stable-doc impact handling, and a compact result table.
- Route unsuitable requests to `$m-discuss` or `$m-plan` before implementation expands.

#### Non-goals

- Replace `$m-autoflow`, `$m-execute`, or `$m-go` for architectural, cross-repo, high-risk, or ambiguous work.
- Remove validation, overwrite existing user changes, or fabricate successful checks.
- Create `docs/intake`, `docs/plan`, `docs/change`, a workflow worktree, or an archive for every quick request.
- Commit or push target-project changes by default when project-local instructions do not require it.
- Duplicate the `$m-docs` taxonomy and routing rules inside `$m-quick`.

#### Assumptions

- Explicit `$m-quick` invocation authorizes direct edits inside the selected target repository after the fast-path gate passes.
- Fast-path eligibility is risk-based; file count and line count are signals, not hard limits.
- A quick request normally affects one repository and one bounded module.
- Project-local instructions such as `AGENTS.md` and `guide.md` still apply and may require commits or stronger validation.
- UI changes remain eligible only when the affected UI can be opened, operated, and evidenced with screenshots in a bounded smoke test.

#### Open Questions

- None blocking. The discussion established the command name, direct-edit semantics, docs-read requirement, escalation behavior, and validation boundary.

#### Options Considered

1. Add standalone `$m-quick` with an explicit eligibility gate and `$m-docs` read step.
2. Add a quick mode to `$m-execute`.
3. Add a flag or implicit shortcut inside `$m-autoflow`.
4. Name the command `$m-fix`, `$m-patch`, or `$m-direct`.

#### Rejected Options

- Quick mode in `$m-execute`: rejected because `$m-execute` intentionally requires an approved plan and dedicated worktree; a bypass mode would weaken its contract.
- Implicit shortcut in `$m-autoflow`: rejected because risk classification would be less visible and could silently bypass staged safeguards.
- `$m-fix`: rejected because the command also covers small requirement changes.
- `$m-patch`: rejected because it overemphasizes implementation shape rather than eligibility.
- `$m-direct`: rejected because it describes mechanism without communicating the small/low-risk boundary.

#### Recommended Direction

Create `$m-quick` as a concise standalone skill with one detailed `references/quick.md`. Keep `$m-docs` authoritative for context discovery and stable-doc routing. Expose `$m-quick` from `$m-autoflow` as an alternate fast path while explicitly excluding it from the staged worktree/plan/archive contract.

#### Research Summary

No web research was needed. This is a local workflow-contract decision governed by existing repository skills and documentation rather than volatile external facts.

#### Worktree / Branch / Docs Root Status

- Worktree ready: yes
- Branch ready: yes
- Docs root identified: yes
- Code repo identified: yes

#### Issue List

- None.

### Plan - Requirements And Architecture

#### Discussion Summary

The full workflow is intentionally rigorous but disproportionate for localized, obvious changes. The new command must reduce workflow artifacts and setup while preserving the two controls that matter most for correctness: reading current project truth before editing and validating the affected behavior afterward.

#### Accepted / Rejected Requirements

Accepted:

- Direct edits to the selected repo's current checkout after eligibility passes.
- Mandatory `$m-docs` context reading before code changes.
- No target-request worktree, root plan, intake, change archive, or archive phase by default.
- Main-agent implementation without sub-agent dispatch overhead.
- Minimal effective validation and a concise direct result table.
- Actual UI operation and screenshots for eligible UI changes.
- Stable docs updated only when stable truth changes.
- Immediate escalation when risk or ambiguity exceeds the fast-path boundary.

Rejected:

- Unconditional direct editing without a risk gate.
- Treating missing or conflicting docs as irrelevant.
- Automatic commit or push regardless of target-project instructions.
- Allowing cross-repo, schema, authentication, security, destructive-data, public-contract, dependency-platform, or architecture changes through the fast path.

#### Requirements Analysis

##### Goal

Provide a one-command path that safely resolves bounded low-risk changes with minimal procedural overhead and no loss of documented context.

##### Scope

- Skill package, metadata, manifest, umbrella routing, stable docs, validation, and local installation sync.
- No runtime application feature or visual interface is changed by this repository task.

##### Use Cases

- Fix a clear null-state, validation, typo, or localized logic bug in one repo.
- Make a small, explicit behavior or UI adjustment whose acceptance result is obvious.
- Restore behavior already described by stable docs without creating workflow history artifacts.
- Reject or escalate a seemingly small request when inspection reveals wider contracts or risk.

##### Functional Requirements

- `$m-quick` must locate `project_root`, `docs_root`, and the target `code_repo` before editing.
- `$m-quick` must explicitly use `$m-docs` in read/context mode.
- Context lookup must begin with `docs/README.md`, the nearest category index, and only matching leaf docs.
- Feature work must prioritize `features`; durable boundaries must use `requirements`; technical constraints must use `specs` and relevant `decisions`; bug/history lookup must prioritize `lessons` before `change`; ambiguous original intent may consult `intake`.
- If docs conflict with the request or code, `$m-quick` must stop before implementation and route to `$m-discuss`.
- If no docs root exists, `$m-quick` may continue only for a self-contained, unambiguous repo-local change and must report the missing context; otherwise it must escalate.
- The gate must require one target repo, clear acceptance, bounded write set, simple rollback, and focused verification.
- The gate must reject cross-repo, architecture, public API/protocol, database/schema/migration, authentication/authorization/security, destructive data, production configuration, broad dependency, or ambiguous-root-cause work.
- `$m-quick` must inspect Git status and preserve unrelated or pre-existing changes.
- `$m-quick` must not create a target-request worktree, branch, `plan.md`, `todo.md`, `docs/intake`, `docs/plan`, or `docs/change` by default.
- `$m-quick` must make the smallest safe edit and run the fastest relevant validation.
- Eligible UI changes must open and operate the affected UI path and produce screenshot evidence; inability to do so must be reported as blocked or escalated.
- A bug restoring documented behavior normally has no stable-doc write impact. An intentional stable behavior or contract change must invoke `$m-docs` and update the canonical stable docs without manufacturing workflow archive files.
- The final response must include docs read, gate result, changed scope, validation, docs impact, and residual risk.
- `$m-quick` must not commit or push by default, while still honoring stricter project-local instructions.

##### Non-functional Requirements

- Keep `SKILL.md` concise and move detailed gates, routing, and examples to one reference file.
- Avoid scripts or assets because the behavior is judgment-driven and repository-specific.
- Make escalation explicit and deterministic enough that the fast path cannot become an unbounded bypass.
- Reuse `$m-docs` by reference instead of duplicating its taxonomy.
- Preserve source-to-install parity through existing validation and sync tooling.

##### Inputs / Outputs

Inputs:

- User request and explicit `$m-quick` invocation.
- Project-local instructions.
- Governed docs indexes and affected stable docs.
- Target repository status, code, and focused test surfaces.

Outputs:

- Either a completed bounded edit with evidence, or an escalation without silently expanding scope.
- A compact table containing `Docs Context`, `Fast-path Gate`, `Changes`, `Validation`, `Docs Impact`, and `Residual Risk`.

##### Edge Cases

- Several Git repositories exist under `project_root/repo` and the target is ambiguous.
- Relevant target files already contain user changes.
- Stable docs describe behavior that conflicts with the new request.
- No governed docs root or matching feature dossier exists.
- The change looks local but touches a generated file, public interface, migration, or dependency lockfile.
- Focused tests fail for pre-existing unrelated reasons.
- A UI can be changed but cannot be started, authenticated, or operated for evidence.
- Investigation reveals the root cause spans repositories or architectural boundaries.

##### Acceptance Criteria

- `$m-quick` is a valid installed skill and appears as a distinct fast path in the `m-*` family.
- Its package explicitly requires `$m-docs` context reading before eligibility and edits.
- Its rules clearly distinguish read-always from write-only-on-stable-impact.
- Its entry gate accepts bounded low-risk cases and rejects the listed high-risk categories.
- It directly edits the selected repo only after the gate passes and preserves existing work.
- It defines focused validation, UI evidence, escalation, and direct result-table behavior.
- `$m-autoflow` no longer states an unconditional worktree/plan rule that contradicts the explicit `$m-quick` exception.
- Relevant stable docs fully describe the new command from the feature point of view.
- Repository validation and source-to-install sync pass.

##### Risks

- Over-broad metadata could trigger `$m-quick` when the user did not intend to bypass staged work.
- Vague eligibility language could allow risky work through the fast path.
- Duplicating docs routing could drift from `$m-docs` over time.
- Updating umbrella guardrails could accidentally weaken the staged workflow.
- Syncing from the worktree modifies installed skills outside Git; failed validation must prevent acceptance.

#### Architecture Design

##### Overall Solution

Create a new `m-quick` skill package using progressive disclosure:

- `SKILL.md`: identity, trigger description, fast-path contract, entry gate summary, workflow outline, and exit table.
- `references/quick.md`: detailed eligibility and escalation matrix, docs context lookup, direct-repo safety, validation expectations, UI evidence, docs impact, and result format.
- `agents/openai.yaml`: concise UI metadata.
- `manifests/m-quick.json`: copy-install metadata and dependencies on the workflow collection and `$m-docs`.

Integrate it into `m-autoflow` as a standalone alternate route. The normal staged path remains `discuss -> plan -> execute|go -> optional/automatic test -> archive`; `$m-quick` sits beside that path and is entered only for a bounded fast request.

##### Alternatives Considered

- Reuse `$m-execute`: rejected due incompatible entry gates.
- Put all rules in `m-autoflow`: rejected due duplication and context cost.
- Add deterministic eligibility script: rejected because project risk classification requires engineering judgment; a script would produce false confidence.
- Modify `$m-docs` to add a new taxonomy: rejected because existing read/routing behavior already supports this use case.

##### Module Responsibilities

- `skills/m-quick`: own fast-path eligibility, direct edit behavior, validation, escalation, and reporting.
- `skills/m-docs`: remain canonical for docs-root discovery, contextual reading, and stable-doc routing.
- `skills/m-autoflow`: expose the alternate route and preserve staged-flow guardrails.
- `manifests`: describe install dependencies and reference files.
- `docs/features/m-quick-fast-path.md`: hold complete current user-visible command behavior.
- `docs/requirements/m-quick-fast-path.md`: hold durable intent, safety boundaries, and acceptance.
- `docs/specs/m-quick-skill.md`: hold package, trigger, gate, docs lookup, validation, and install contracts.
- `docs/decisions`: record why a separate command was selected instead of weakening `$m-execute`.

##### Data / Call Flow

1. User invokes `$m-quick` with a bounded request.
2. Main agent reads project-local instructions and locates project/docs/repo boundaries.
3. Main agent explicitly invokes `$m-docs` for minimum relevant context.
4. Main agent inspects Git status and enough code to evaluate risk and acceptance.
5. If the gate fails, stop before expanding edits and route to `$m-discuss` or `$m-plan` with reasons.
6. If the gate passes, main agent directly edits the selected current checkout.
7. Main agent runs focused validation; UI paths receive actual operation and screenshot evidence.
8. Main agent invokes `$m-docs` impact handling only when stable behavior or contracts changed.
9. Main agent returns the compact result table and does not start archive, merge, cleanup, or push automatically.

##### Interface Drafts

Proposed frontmatter intent:

```md
---
name: m-quick
description: Fast direct implementation path for explicit, bounded, low-risk fixes or small requirements in one repository. Use when the user invokes $m-quick or explicitly asks for a minimal direct patch without the full staged workflow; read governed docs through $m-docs first, validate the affected behavior, and escalate ambiguous, cross-repo, contractual, architectural, security-sensitive, or otherwise high-risk work.
---
```

Proposed result shape:

```md
| Item | Result |
| --- | --- |
| Docs Context | <paths read or missing-context note> |
| Fast-path Gate | Passed / Escalated / Blocked |
| Changes | <repo and files> |
| Validation | <checks and evidence> |
| Docs Impact | None / Updated paths |
| Residual Risk | <none or concise risk> |
```

##### Error Handling and Safety

- Fail closed on target-repo ambiguity, docs conflict, unclear acceptance, or prohibited risk categories.
- Do not overwrite existing user edits; stop when overlap cannot be resolved safely.
- Distinguish pre-existing validation failures from failures introduced by the patch.
- Never describe skipped or unavailable validation as passed.
- Do not silently create workflow artifacts to compensate for missing context.
- Do not broaden from one repo to several repos after edits begin.
- Honor project-local commit rules, but never infer push or publication permission.

##### Performance and Testing Strategy

- Read indexes plus matching leaf docs, not the entire docs tree.
- Keep detailed behavior in one reference file to reduce trigger-time context.
- Validate `m-quick` and changed umbrella skills with repository tooling.
- Parse changed manifests as JSON and check Markdown links.
- Run `git diff --check`.
- Sync changed skills into the local Codex install only after source validation succeeds.
- Review scenario matrix: eligible bug, intentional behavior tweak, docs conflict, missing docs, cross-repo change, security/schema change, dirty target file, and UI smoke evidence.
- Reserve independent forward-testing for optional `$m-test` when host sub-agent facilities are available.

##### Extensibility Design Points

- Future eligibility refinements live in `references/quick.md` without inflating `SKILL.md`.
- Additional result rows can be added without changing staged workflow contracts.
- `$m-docs` taxonomy changes flow into `$m-quick` through the explicit reference rather than copied rules.
- A future quick-fix audit mode could be added separately without changing default archive behavior.

#### Issue List

- No architecture blocker.
- Execution approval is still required.

### Stage 3.1 - Planning

#### Project Goal and Current State

Current state: the repository provides the staged `$m-autoflow` family and `$m-go`, but every implementation route assumes a confirmed plan/worktree or the heavier workflow. There is no canonical direct fast path.

Goal: add `$m-quick` as a guarded direct-edit command that always restores context from governed docs before touching code.

#### Docs Governance Routing Decision

Use `$m-docs` as follows:

- Original request evidence -> `docs/intake/2026-07-10_m-quick-fast-path.md`.
- Complete current command behavior -> `docs/features/m-quick-fast-path.md`.
- Durable fast-path intent and safety boundaries -> `docs/requirements/m-quick-fast-path.md`.
- Package, gate, context-read, validation, and install contracts -> `docs/specs/m-quick-skill.md`.
- Separate-command architecture decision -> `docs/decisions/2026-07-10_m-quick-standalone-fast-path.md`.
- Umbrella feature/requirement/spec docs receive only the links and family-level routing needed to avoid duplicate truth.
- Workflow result -> `docs/change` only during `$m-archive`.
- Existing frontmatter lesson applies; no new reusable lesson is known yet.

#### Related Intake / Features / Requirements / Specs / Decisions / Lessons

- Related intake:
  - To add: `docs/intake/2026-07-10_m-quick-fast-path.md`
- Related features:
  - To add: `docs/features/m-quick-fast-path.md`
  - Existing umbrella: `docs/features/m-autoflow-workflow.md`
- Related requirements:
  - To add: `docs/requirements/m-quick-fast-path.md`
  - Existing umbrella: `docs/requirements/m-autoflow-skill.md`
- Related specs:
  - To add: `docs/specs/m-quick-skill.md`
  - Existing umbrella: `docs/specs/m-autoflow-skill.md`
- Related decisions:
  - Existing: `docs/decisions/2026-07-08_m-skill-phase-naming.md`
  - To add: `docs/decisions/2026-07-10_m-quick-standalone-fast-path.md`
- Related lessons:
  - `docs/lessons/skill-frontmatter-yaml-colon.md`

#### Stable Docs Impact

- Intake impact: add
- Feature impact: add and clarify umbrella routing
- Requirements impact: add and clarify umbrella boundary
- Specs impact: add and clarify umbrella package/exception contract
- Decision impact: add
- Lessons known at planning time: reuse `skill-frontmatter-yaml-colon`; no new lesson planned

#### Executable Task List

##### Will Execute

- Q1 - Record `$m-quick` stable docs and architecture decision
- Q2 - Create the `$m-quick` skill package and manifest
- Q3 - Integrate `$m-quick` into umbrella routing and guardrails
- Q4 - Validate, sync, and commit the implementation

##### Will Not Execute Now

- Q5 - Run optional heavy forward-testing
  - Reason: belongs to optional `$m-test`; independent sub-agent evaluation is not required for the implementation phase and current host tools may not expose a suitable worker surface.
- Q6 - Archive and close the workflow
  - Reason: belongs to `$m-archive` after execution and validation.
- Q7 - Push the resulting branch
  - Reason: belongs to explicit `$m-gitpush` after closeout or separate user instruction.

#### Task Details

##### Q1 - Record `$m-quick` stable docs and architecture decision

- Owner: Main agent or bounded docs worker when an authorized delegated execution mode is used.
- Worktree: `D:\project\my-ai-skills\worktrees\m-quick`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-quick\plan.md`
- Goal: Preserve original request evidence and make one complete feature dossier the current source of truth, with linked durable requirements, technical contracts, and decision rationale.
- Files / Modules:
  - `docs/intake/2026-07-10_m-quick-fast-path.md`
  - `docs/intake/README.md`
  - `docs/features/m-quick-fast-path.md`
  - `docs/features/m-autoflow-workflow.md`
  - `docs/features/README.md`
  - `docs/requirements/m-quick-fast-path.md`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/requirements/README.md`
  - `docs/specs/m-quick-skill.md`
  - `docs/specs/m-autoflow-skill.md`
  - `docs/specs/README.md`
  - `docs/decisions/2026-07-10_m-quick-standalone-fast-path.md`
  - `docs/decisions/README.md`
- Write Set: the exact docs above.
- Acceptance:
  - Feature dossier describes entry, docs reading, gate, direct edits, validation, UI evidence, docs impact, escalation, and final table end to end.
  - Requirement/spec docs contain durable and technical truth without duplicating the feature dossier.
  - Umbrella docs expose `$m-quick` as an alternate route without weakening staged behavior.
  - Category indexes link every new leaf doc.
- Test Points:
  - Markdown relative-link check.
  - Search for duplicate or contradictory worktree/plan rules.
  - `git diff --check`.
- Rollback: remove new leaf docs and revert index/umbrella-doc edits.

##### Q2 - Create the `$m-quick` skill package and manifest

- Owner: Main agent or bounded skill-package worker when an authorized delegated execution mode is used.
- Worktree: `D:\project\my-ai-skills\worktrees\m-quick`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-quick\plan.md`
- Goal: Add a concise, valid skill package implementing the agreed guarded fast path.
- Files / Modules:
  - `skills/m-quick/SKILL.md`
  - `skills/m-quick/references/quick.md`
  - `skills/m-quick/agents/openai.yaml`
  - `manifests/m-quick.json`
- Write Set:
  - `skills/m-quick/**`
  - `manifests/m-quick.json`
- Acceptance:
  - Skill is initialized using the system `skill-creator` initializer and contains no unnecessary README, scripts, examples, or assets.
  - Frontmatter trigger is narrow enough to require explicit fast/direct intent.
  - `$m-docs` reading occurs before eligibility or editing.
  - Gate, prohibited categories, direct-edit behavior, dirty-worktree handling, focused validation, UI evidence, docs impact, escalation, and result table are explicit.
  - Manifest matches repository conventions and lists the single reference file.
- Test Points:
  - `tools\validate-skills.ps1 -Skill m-quick`.
  - JSON parse of `manifests/m-quick.json`.
  - Scenario matrix review against `references/quick.md`.
- Rollback: remove `skills/m-quick` and `manifests/m-quick.json`.

##### Q3 - Integrate `$m-quick` into umbrella routing and guardrails

- Owner: Main agent or bounded governance worker after Q2's interface is stable.
- Worktree: `D:\project\my-ai-skills\worktrees\m-quick`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-quick\plan.md`
- Goal: Make the new command discoverable while preserving strict staged workflow semantics.
- Files / Modules:
  - `skills/m-autoflow/SKILL.md`
  - `skills/m-autoflow/references/stages.md`
  - `skills/m-autoflow/agents/openai.yaml` only if its user-facing prompt needs the fast-path cue
  - `manifests/m-autoflow.json`
- Write Set: the exact umbrella files above.
- Acceptance:
  - `$m-autoflow` lists `$m-quick` as a standalone alternate path, not a stage.
  - Default staged order remains unchanged.
  - The worktree/plan/mandatory archive guardrails are explicitly scoped to staged execution and do not contradict `$m-quick`.
  - Umbrella dependency metadata includes `m-quick`.
  - No phase skill copies `$m-quick` rules.
- Test Points:
  - `tools\validate-skills.ps1 -Skill m-autoflow`.
  - Focused contradiction search across `skills/m-autoflow`.
  - JSON parse of `manifests/m-autoflow.json`.
- Rollback: revert umbrella routing, guardrail, metadata, and manifest edits.

##### Q4 - Validate, sync, and commit the implementation

- Owner: Main agent for command execution, audit, and repository commit; any content fixes remain mapped to Q1-Q3.
- Worktree: `D:\project\my-ai-skills\worktrees\m-quick`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-quick\plan.md`
- Goal: Prove source validity, update local installed copies, verify parity, and follow `guide.md` commit policy.
- Files / Modules:
  - Source validation: `skills/m-quick`, `skills/m-autoflow`, changed manifests, and changed docs.
  - Ignored build output: `dist/codex/m-quick`, `dist/codex/m-autoflow`.
  - Installed copies: `C:\Users\HelloWorld\.codex\skills\m-quick` and `C:\Users\HelloWorld\.codex\skills\m-autoflow`.
- Write Set:
  - No new source scope beyond Q1-Q3 and plan status updates.
  - Generated/installed copies are written only by `tools\sync-skills.ps1`.
- Acceptance:
  - `tools\validate-skills.ps1 -Skill m-quick` passes.
  - `tools\validate-skills.ps1 -Skill m-autoflow` passes.
  - Changed manifests parse as JSON.
  - Markdown relative links pass.
  - `git diff --check` passes.
  - `tools\sync-skills.ps1 -Skill m-quick` succeeds.
  - `tools\sync-skills.ps1 -Skill m-autoflow` succeeds.
  - Installed package content matches source package content, excluding generated `.build-info.json`.
  - Repository changes are committed with an English conventional-style message.
- Test Points:
  - Commands above plus clean/understood `git status`.
- Rollback:
  - Revert Q1-Q3 source commits if requested and rerun sync for affected skills to restore installed copies.

##### Q5 - Run optional heavy forward-testing

- Owner: `$m-test`.
- Worktree: `D:\project\my-ai-skills\worktrees\m-quick`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-quick\plan.md`
- Goal: Independently exercise realistic eligible and ineligible prompts against the completed skill.
- Files / Modules: no planned source writes; fixes discovered by testing require a return to execution with bounded scope.
- Write Set: Will not execute now.
- Acceptance: independent scenarios classify correctly and preserve docs/context/validation rules.
- Test Points: eligible bug, missing docs, docs conflict, cross-repo request, schema/security request, dirty files, and UI evidence requirement.
- Rollback: not applicable to the test-only task.

##### Q6 - Archive and close the workflow

- Owner: `$m-archive`.
- Worktree: `D:\project\my-ai-skills\worktrees\m-quick`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-quick\plan.md`
- Goal: Create `docs/change`, assess lessons, merge, and clean the worktree.
- Files / Modules:
  - `docs/change/2026-07-10_m-quick-fast-path.md`
  - `docs/change/README.md`
  - Potential `docs/lessons/**` only if reusable troubleshooting knowledge emerges.
- Write Set: Will not execute now.
- Acceptance: archive follows `$m-archive` and `$m-docs`.
- Test Points: archive-stage verification.
- Rollback: archive-specific rollback is owned by `$m-archive`.

##### Q7 - Push the resulting branch

- Owner: `$m-gitpush`.
- Worktree: control-plane after archive/merge or explicit user request.
- Plan Path: `D:\project\my-ai-skills\worktrees\m-quick\plan.md`
- Goal: Push only after explicit invocation.
- Files / Modules: none.
- Write Set: Will not execute now.
- Acceptance: push succeeds or fallback behavior is reported.
- Test Points: remote status verification.
- Rollback: not applicable in execution planning.

#### Dependencies

- Q1 and Q2 have disjoint write sets and may run in parallel under an authorized delegated execution mode.
- Q3 depends on Q2's final interface wording but can begin once the entry/exit contract is fixed.
- Q4 depends on Q1-Q3.
- Q5 depends on Q4 and is optional.
- Q6 depends on completed implementation and the chosen validation path.
- Q7 depends on explicit user instruction and normally follows closeout.

#### Risks and Notes

- Preserve the core distinction: `$m-quick` is a bounded standalone exception; staged commands remain strict.
- Mandatory docs reading must be explicit, while docs writing remains impact-based.
- Do not make file-count thresholds the primary safety gate.
- Do not modify `$m-docs` unless execution proves an actual missing capability; current routing already supports context lookup.
- The current repository requires commits after modifications, but `$m-quick` itself must defer commit behavior to each target project's local instructions.
- Installed copies are local generated outputs and must be synced only after source validation.

#### Parallelism Assessment

- Safe parallel lanes after approval: Q1 docs and Q2 skill package.
- Coordination boundary: Q3 should consume Q2's final names and semantics to prevent wording drift.
- Serial convergence: Q4 validation, sync, parity review, and commit.
- If the user invokes `$m-execute`, the main agent may implement directly and may choose serial execution to reduce coordination overhead.
- If the user invokes `$m-go`, Q1 and Q2 are suitable bounded worker tasks; Q3 follows after interface convergence, and Q4 remains a main-agent audit/command lane with delegated content fixes.

#### Issue List

- None unresolved.
- Execution was approved by the user's explicit `$m-execute` invocation.

### Stage 3.2 - Execution Results

#### Executed Task IDs

- Q1 - Completed. Added original intake evidence, a complete feature dossier, dedicated durable requirements, a technical specification, an architecture decision, category-index entries, and narrow umbrella-doc links.
- Q2 - Completed. Created the canonical `m-quick` skill package with one detailed reference, generated UI metadata, and install manifest.
- Q3 - Completed. Added `$m-quick` to umbrella routing, stage governance, dependency metadata, and the explicit staged-workflow exception without weakening other phase gates.
- Q4 - Completed. Validated source packages and manifests, checked docs links and scenario coverage, synced `m-quick` and `m-autoflow`, and verified installed-source parity.

#### Deferred Task IDs

- Q5 - Not executed. Independent heavy forward-testing remains optional under `$m-test`.
- Q6 - Completed by `$m-archive`; archive artifacts are committed before the control-plane merge and cleanup sequence.
- Q7 - Not executed. Push remains owned by explicit `$m-gitpush`.

#### Changed Files By Task

Q1:

- `docs/intake/2026-07-10_m-quick-fast-path.md`
- `docs/intake/README.md`
- `docs/features/m-quick-fast-path.md`
- `docs/features/m-autoflow-workflow.md`
- `docs/features/README.md`
- `docs/requirements/m-quick-fast-path.md`
- `docs/requirements/m-autoflow-skill.md`
- `docs/requirements/README.md`
- `docs/specs/m-quick-skill.md`
- `docs/specs/m-autoflow-skill.md`
- `docs/specs/README.md`
- `docs/decisions/2026-07-10_m-quick-standalone-fast-path.md`
- `docs/decisions/README.md`

Q2:

- `skills/m-quick/SKILL.md`
- `skills/m-quick/references/quick.md`
- `skills/m-quick/agents/openai.yaml`
- `manifests/m-quick.json`

Q3:

- `skills/m-autoflow/SKILL.md`
- `skills/m-autoflow/references/stages.md`
- `manifests/m-autoflow.json`

Q4:

- `plan.md`
- Ignored/generated `dist/codex/m-quick` and `dist/codex/m-autoflow`
- Installed `C:\Users\HelloWorld\.codex\skills\m-quick`
- Installed `C:\Users\HelloWorld\.codex\skills\m-autoflow`

#### Key Design Decisions

- `$m-quick` is a standalone alternate route, not a shortened staged phase.
- Governed docs reading is mandatory before eligibility and implementation; stable-doc writing is impact-based.
- One detailed reference owns risk classification and execution details so `SKILL.md` remains concise.
- The main agent edits directly after the gate passes; implementation sub-agents, quick-request worktrees, plans, and archives are excluded by default.
- A dedicated feature dossier owns complete current behavior, while requirement/spec/decision docs retain their narrower canonical responsibilities.

#### Lightweight Validation Results

- `tools\validate-skills.ps1 -Skill m-quick -PythonExe C:\ProgramData\anaconda3\python.exe`: passed.
- `tools\validate-skills.ps1 -Skill m-autoflow -PythonExe C:\ProgramData\anaconda3\python.exe`: passed.
- `manifests/m-quick.json` and `manifests/m-autoflow.json` PowerShell JSON parsing: passed.
- Markdown relative-link resolution across `docs/**/*.md`: passed.
- New stable docs contain no volatile `../../plan.md` links: passed.
- Required scenario-contract token check for docs context, one-repo gate, prohibited risk, UI evidence, validation, commit policy, and escalation: passed.
- Contradiction search for staged worktree/plan rules versus the `$m-quick` exception: passed.
- `tools\sync-skills.ps1 -Skill m-quick`: passed.
- `tools\sync-skills.ps1 -Skill m-autoflow`: passed.
- Installed-source SHA-256 parity for both synced skills, excluding generated `.build-info.json`: passed.
- `git diff --check`: passed with expected Windows line-ending warnings only.

#### Heavy Validation Still Needed

- Q5 independent forward-testing was not run in `$m-execute`.
- No runtime application UI changed, so UI operation and screenshot validation are not applicable to this repository implementation.
- Residual risk: realistic future prompts may expose eligibility wording that benefits from iteration; static eligible/ineligible scenario coverage is present now.

#### Rollback Notes

- Revert the Q1-Q3 implementation commit.
- Remove the installed `m-quick` package if the command is withdrawn.
- Rerun `tools\sync-skills.ps1 -Skill m-autoflow` from the reverted source to restore the installed umbrella package.
- Do not alter docs remotes, backup destinations, or push state as part of rollback.

#### Sub-agent Trace

- No sub-agents were used. The host exposed no implementation sub-agent dispatch tool, and the user invoked `$m-execute`, which permits direct main-agent implementation.

### Stage 4 - Archive And Closeout

#### Archive Artifacts

- Plan archive: `docs/plan/2026-07-10_m-quick-fast-path.md`
- Change archive: `docs/change/2026-07-10_m-quick-fast-path.md`
- Promoted lesson: `docs/lessons/windows-skill-parity-line-endings.md`

#### Stable Docs Impact

- Intake impact: updated
- Feature impact: updated
- Requirements impact: updated
- Specs impact: updated
- Decision impact: updated
- Lessons impact: updated

#### Validation Decision

- Implementation and installed-skill validation passed.
- Optional independent heavy forward-testing was skipped after its residual risk was disclosed.
- The user's explicit `$m-archive` invocation accepted closeout on that basis.
- UI evidence was not applicable because no runtime visual UI changed.

#### Closeout Mode

- Default archive-and-end semantics apply.
- After the archive commit, the control plane fast-forwards `main`, verifies status, removes the dedicated worktree, and deletes the merged local feature branch.
- No remote push, docs publication, deployment, or backup action is included.

#### Lessons Decision

- Added `windows-skill-parity-line-endings.md` because line-ending-only hash mismatches are a reusable Windows environment pitfall likely to recur during replace-style skill sync checks.
