# Plan - Official Interactive Skill Outputs

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `feat/visualize-skill-output`
- Base: `main` at `1360e51941aaa084564c9cc253c080f0246bb2ef`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\worktrees\visualize-skill-output\docs`
- Code Repos: `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\visualize-skill-output`
- Current Stage: `$m-test` complete; VIS-1 through VIS-4 passed and the workflow may enter `$m-archive`

## Stage Records

### Initialization

- `guide.md`: read; every repository modification must be committed with an English message following existing history.
- Project / docs / code repo confirmation: one Git repository; the versioned repository `docs/` tree is the selected governed docs root.
- Base / worktree confirmation: dedicated branch and clean worktree exist under the project `worktrees/` directory.
- Main repo boundary: the main checkout remains the control plane; planned edits happen only in this worktree.

### Discuss - Discovery And Requirements Shaping

#### Goal

Improve the `m-autoflow` skill family so selected phases can use official Codex inline interactions such as buttons, Lucide icons, local option selection, evidence navigation, and follow-up actions.

#### Scope

- Preserve the static Markdown, Mermaid, file-link, screenshot, code-comment, and Git-directive contract.
- Add an explicit decision layer for official inline interaction.
- Integrate the first rollout with `$m-discuss`, `$m-plan`, `$m-test`, and `$m-archive`.
- Add deterministic contract tests and perform real rendered interaction validation.

#### Assumptions

- The official `visualize` capability is available in supported Codex hosts but may be absent elsewhere.
- Distributed skills can invoke another skill by capability or skill name without depending on its installed version path.
- Inline actions use Codex follow-up messages; they do not directly execute repository or workflow mutations.
- Generated visualization fragments are thread-scoped runtime artifacts and do not belong in this repository.

#### Open Questions

- None blocking.
- The exact future rollout order for remaining skills is intentionally deferred until the first four phases are validated in real use.

#### Options Considered

1. Keep Markdown-only enhancement.
2. Generate inline interaction for most skill responses.
3. Use a hybrid policy that selects inline interaction only when it materially improves a decision or action.

#### Rejected Options

- Markdown-only enhancement: rejected because it does not satisfy the user's request for official buttons, icons, and inline interaction.
- Always-interactive output: rejected because it adds avoidable latency, validation cost, context usage, and visual noise to simple results.

#### Recommended Direction

Adopt the hybrid policy. Keep exact outcome and fallback data in Markdown, then use the official inline capability for high-value selection, drill-down, evidence navigation, or next-phase actions.

#### Research Summary

- No web research was needed.
- The installed official `visualize` skill was treated as the primary capability contract.
- Relevant confirmed constraints include thread-scoped fragments, `::codex-inline-vis`, semantic controls, official utility classes, sandbox-provided Lucide icons, responsive/theme-aware output, no external API calls, and `window.openai.sendFollowUpMessage` for Codex follow-up actions.

#### Worktree / Branch / Docs Root Status

- Branch: `feat/visualize-skill-output`
- Worktree: ready and clean before planning edits
- Docs root: confirmed inside the versioned repository worktree

#### Issue List

- None.

### Plan - Requirements And Architecture

#### Discussion Summary

The previous visual-output change improved static presentation but interpreted "visual components" too narrowly. The user explicitly wants the official interactive surface. The plan extends rather than removes the static contract and keeps interaction optional, bounded, and reversible.

#### Accepted / Rejected Requirements

Accepted:

- Official inline buttons, icons, selection, and follow-up actions for high-value phase results.
- A first rollout covering discuss, plan, test, and archive.
- Plain Markdown fallback and exact status preservation.
- Accessibility, responsive layout, theme awareness, secret protection, and normal phase gates.

Rejected:

- Generating an interactive result for every response.
- Direct repository mutations from presentation code.
- Hard-coded plugin-cache paths or copied official implementation instructions.
- Publishing, hosting, or bundling generated visualization files.

#### Requirements Analysis

##### Goal

Make selected workflow results easier to decide and act on without weakening correctness, authorization, or portability.

##### Scope

- Shared component-selection contract.
- Shared phase-specific interactive patterns.
- Four phase-skill integrations.
- Contract tests, skill validation, synchronization, and rendered UI evidence.

##### Use Cases

1. Compare discussion options and request planning for the selected direction.
2. Review exact plan scope and send an explicit approval follow-up containing Task IDs.
3. Inspect test status and request evidence or the correct next phase.
4. Review archive / merge / cleanup state and request additional inspection without adding a redundant archive confirmation.

##### Functional Requirements

- Decide between prose, table, Mermaid, host directive, and official inline interaction.
- Invoke the official capability by name only after the interactive trigger passes.
- Keep local presentation state inside the inline result.
- Send selected state and requested operation through a follow-up message for Codex actions.
- Re-check phase gates after every follow-up.
- Return a complete static fallback when interactive support is unavailable.

##### Non-functional Requirements

- Keep `SKILL.md` files concise through progressive disclosure.
- Preserve keyboard access, semantic controls, theme tokens, responsive layout down to 320px, and visible action labels.
- Avoid persistent dependencies, network calls, repository runtime helpers, and duplicated official instructions.
- Keep inline data free of secrets and unnecessary personal information.

##### Inputs / Outputs

- Inputs: phase result data, candidate user actions, capability availability, current workflow gate, evidence paths, and safe display values.
- Static output: outcome, exact status table or links, blocker / next command.
- Interactive output: one focused inline result with necessary labels, local selection, and bounded follow-up actions.

##### Edge Cases

- Official capability missing or disabled.
- Host bridge missing even though the visual renders.
- A button requests a phase whose entry gate is not satisfied.
- Long task labels, narrow widths, dark theme, or keyboard-only use.
- Sensitive context, credentials, or screenshots that must not enter inline data.
- Rendering succeeds but the primary interaction fails.

##### Acceptance Criteria

- The four initial phases route through the interactive pattern contract.
- Simple outputs remain static.
- No versioned plugin-cache path appears in distributed skills.
- Follow-up buttons request actions but never claim those actions already occurred.
- Markdown fallback preserves complete status and next steps.
- Contract tests and skill validation pass.
- A representative inline result renders and operates at desktop and narrow widths with screenshot evidence.

##### Risks

- Overuse could increase latency and noise.
- Interactive labels could drift from exact plan / test state.
- A visually successful button could be mistaken for completed authorization.
- Host-specific behavior may be difficult to validate outside the conversation surface.

#### Architecture Design

##### Overall Solution

Add `interactive-output-patterns.md` beside the existing shared component reference. Keep the official visualization implementation contract external and current by requiring consumers to load and obey `$visualize:visualize` when the trigger passes.

The shared decision flow is:

1. Compose the exact phase result and required Markdown fallback.
2. Determine whether a meaningful interaction improves the result.
3. If no, return the static result.
4. If yes and the capability is available, invoke `$visualize:visualize` and create one focused inline result.
5. Keep presentation state local; route Codex work through a follow-up message.
6. The receiving phase revalidates its normal entry gate.

##### Alternatives Considered

- Extend only `output-components.md`: rejected because detailed phase patterns would make the shared static reference too large.
- Copy official HTML and design-system rules into this repository: rejected because it would drift with plugin updates.
- Add a repository script or template generator: rejected because the official capability already owns rendering and runtime constraints.

##### Module Responsibilities

- `output-components.md`: choose the smallest useful output family and route interactive cases.
- `interactive-output-patterns.md`: define workflow-specific triggers, phase actions, approval boundaries, fallback, and sensitive-data rules.
- Phase `SKILL.md` files: require the shared pattern reference and name the phase-specific interactive opportunity.
- Official `$visualize:visualize`: own fragment structure, design system, icons, interaction implementation, rendering, and inline directive.
- `test_visual_output_contract.py`: prevent missing routes, unsafe actions, hard-coded version paths, and fallback regressions.

##### Data / Call Flow

`phase result -> shared output decision -> static result OR $visualize:visualize -> inline local selection -> follow-up request -> phase entry-gate validation`

##### Interface Drafts

- Discussion follow-up: selected option, recommendation context, request for `$m-plan`.
- Plan follow-up: exact approved Task IDs, request for `$m-execute` or `$m-go`.
- Test follow-up: selected failed / blocked item or request to proceed to `$m-archive` only when allowed.
- Archive follow-up: request to inspect an archive, repository state, or residual risk; normal archive invocation still closes without a second confirmation.

##### Error Handling and Safety

- Missing capability or host bridge: return Markdown only.
- Failed follow-up send: show a concise failure and retain the exact manual next command outside the inline result.
- Invalid or stale selected state: receiving phase rejects it and reports the gate failure.
- Never include secrets, raw private context, arbitrary untrusted markup, or unrelated personal data.
- Never let inline JavaScript perform Git, filesystem, merge, push, archive, cleanup, or approval actions directly.

##### Performance and Testing Strategy

- Load interactive patterns only for covered result composition.
- Avoid inline interaction for simple or single-action results.
- Add focused standard-library contract tests.
- Validate changed skill packages and run the full unit-test suite.
- Synchronize only changed skill packages and verify exact source/install parity.
- Run `$m-test` with a representative inline result, desktop and narrow screenshots, keyboard/selection checks, and primary follow-up-action evidence.

##### Extensibility Design Points

- Add future phase recipes without changing the official capability contract.
- Expand to remaining skills only after first-rollout evidence.
- Allow future hosts to retain Markdown fallback without an installed interactive capability.

#### Issue List

- None.

### Stage 3.1 - Planning

#### Project Goal and Current State

- Current state: static visual-output rules exist and validate, but official inline interaction is not routed from the workflow skills.
- Goal: add a bounded official-interaction layer for four high-value phases while preserving static behavior and safety.

#### Docs Governance Routing Decision

使用 `$m-docs` 校验计划文档路由、`docs_root`、stable-doc 影响和 lessons 查询入口。

- Docs root: `D:\project\my-ai-skills\worktrees\visualize-skill-output\docs`
- Original clarification: existing dated intake record
- Current workflow experience: existing `m-autoflow` feature dossier
- Durable capability and acceptance: existing `m-autoflow` requirements
- Technical invocation / fallback contract: existing `m-autoflow` spec
- Architecture decision: none; the hybrid policy is reversible, localized, and sufficiently captured by feature / requirement / spec truth
- Lessons: none known at planning time; archive will reassess after runtime validation

#### Related Intake / Features / Requirements / Specs / Decisions / Lessons

- Intake: `docs/intake/2026-07-15_visual-output-components.md`
- Feature: `docs/features/m-autoflow-workflow.md`
- Requirements: `docs/requirements/m-autoflow-skill.md`
- Spec: `docs/specs/m-autoflow-skill.md`
- Decisions: existing workflow decisions only; no new ADR planned
- Lessons: none currently applicable

#### Stable Docs Impact

- Intake impact: clarify
- Feature impact: clarify
- Requirements impact: clarify
- Specs impact: clarify
- Decision impact: none
- Lessons known at planning time: none

#### Executable Task List

- VIS-1: add the shared interactive-output contract and static-to-interactive routing.
- VIS-2: integrate the first four phase skills.
- VIS-3: extend contract tests, validate packages, synchronize changed skills, and verify parity.
- VIS-4: run representative official inline interaction validation through `$m-test`.
- VIS-D1: expand inline patterns to remaining skills; deferred.
- VIS-D2: publish or distribute standalone visualizations; out of scope.
- VIS-D3: add a repository runtime helper / template generator; rejected as unnecessary.

#### Execution Scope After Approval

##### Will Execute

- VIS-1
- VIS-2
- VIS-3
- VIS-4

##### Will Not Execute Now

- VIS-D1: deferred until the first rollout has real usability and maintenance evidence.
- VIS-D2: out of scope; the user requested Codex conversation output, not a hosted site or downloadable artifact.
- VIS-D3: rejected; it would duplicate official runtime responsibilities and create avoidable maintenance.

#### Task Details

##### VIS-1 - Shared Interactive Output Contract

- Owner: main agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\visualize-skill-output`
- Plan Path: `D:\project\my-ai-skills\worktrees\visualize-skill-output\plan.md`
- Goal: define when workflow results invoke official inline interaction and how they fall back safely.
- Files / Modules:
  - `skills/m-autoflow/SKILL.md`
  - `skills/m-autoflow/references/output-components.md`
  - `skills/m-autoflow/references/interactive-output-patterns.md` (new)
- Write Set: only the three paths above.
- Acceptance:
  - separates static and interactive selection clearly
  - invokes `$visualize:visualize` by name without hard-coded plugin paths
  - preserves Markdown fallback, secret protection, and phase gates
  - defines local-state versus follow-up-action boundaries
- Test Points:
  - reference exists and is linked
  - required trigger, fallback, and safety language is present
  - no `plugins/cache/.../visualize/<version>` path appears
- Rollback: revert these reference and umbrella-skill changes; re-sync the previous `m-autoflow` package.

##### VIS-2 - First Phase Integrations

- Owner: main agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\visualize-skill-output`
- Plan Path: `D:\project\my-ai-skills\worktrees\visualize-skill-output\plan.md`
- Goal: make the four selected phases consume the shared interactive patterns without changing phase semantics.
- Files / Modules:
  - `skills/m-discuss/SKILL.md`
  - `skills/m-plan/SKILL.md`
  - `skills/m-test/SKILL.md`
  - `skills/m-archive/SKILL.md`
- Write Set: only the four paths above.
- Acceptance:
  - each phase reads the shared interactive pattern reference
  - each phase names its bounded interaction opportunity
  - plan approval, test routing, and archive behavior retain their existing gates
  - `SKILL.md` files remain concise
- Test Points:
  - focused route assertions for all four skills
  - quick validation for all changed packages
- Rollback: revert the four phase-skill edits and re-sync their previous packages.

##### VIS-3 - Contract Regression And Package Synchronization

- Owner: main agent during `$m-execute`
- Worktree: `D:\project\my-ai-skills\worktrees\visualize-skill-output`
- Plan Path: `D:\project\my-ai-skills\worktrees\visualize-skill-output\plan.md`
- Goal: protect the interactive contract and make the validated source packages active locally.
- Files / Modules:
  - `tests/test_visual_output_contract.py`
  - `tools/validate-skills.ps1` (read / run only)
  - `tools/sync-skills.ps1` (read / run only)
- Write Set: `tests/test_visual_output_contract.py` only.
- Acceptance:
  - tests cover reference routing, fallback, follow-up-only actions, secrets, and path portability
  - full unit-test discovery passes, excluding only documented environment skips
  - all changed skill packages validate
  - changed packages sync and match installed copies by file set and SHA-256
  - `git diff --check` passes
- Test Points:
  - `python -m unittest discover -s tests -p 'test_*.py' -v`
  - `tools/validate-skills.ps1` for `m-autoflow`, `m-discuss`, `m-plan`, `m-test`, and `m-archive`
  - exact source/install parity excluding generated `.build-info.json`
- Rollback: restore the previous test contract and synchronize previous skill sources.

##### VIS-4 - Representative Inline Interaction Validation

- Owner: main agent during `$m-test`
- Worktree: `D:\project\my-ai-skills\worktrees\visualize-skill-output`
- Plan Path: `D:\project\my-ai-skills\worktrees\visualize-skill-output\plan.md`
- Goal: verify actual appearance and primary interaction in the Codex conversation surface.
- Files / Modules:
  - thread-scoped visualization directory only; no repository source write
- Write Set: no repository files; temporary runtime visualization and evidence files only.
- Acceptance:
  - representative output renders at desktop and narrow widths without clipping
  - buttons and Lucide icons are visible and keyboard accessible
  - local selection updates the displayed state
  - primary follow-up action sends the expected request or the test is marked blocked
  - screenshots and direct pass/fail table are reported
- Test Points:
  - official render helper or live host preview
  - desktop and narrow viewport operation
  - selection and follow-up action
- Rollback: delete temporary runtime evidence; no repository rollback required.

##### VIS-D1 - Remaining Skill Expansion

- Owner: deferred
- Worktree: not allocated
- Plan Path: this plan
- Goal: evaluate interactive patterns for `m-context`, `m-execute`, `m-go`, `m-quick`, `m-docs`, `m-gitpush`, and domain-specific skills.
- Files / Modules: deferred.
- Write Set: none in this execution.
- Acceptance: separate evidence-backed approval after first-rollout evaluation.
- Test Points: not in current scope.
- Rollback: not applicable.

##### VIS-D2 - Standalone Publication

- Owner: out of scope
- Worktree: not allocated
- Plan Path: this plan
- Goal: publish or distribute visualization files outside Codex.
- Files / Modules: none.
- Write Set: none.
- Acceptance: requires a separate user request.
- Test Points: not in current scope.
- Rollback: not applicable.

##### VIS-D3 - Repository Visualization Runtime

- Owner: rejected
- Worktree: not allocated
- Plan Path: this plan
- Goal: add a local runtime, helper script, or template generator.
- Files / Modules: none.
- Write Set: none.
- Acceptance: not applicable; official capability already owns this responsibility.
- Test Points: not in current scope.
- Rollback: not applicable.

#### Dependencies

- VIS-1 must complete before VIS-2 so phase integrations consume a stable contract.
- VIS-2 must complete before VIS-3 route assertions finalize.
- VIS-1 through VIS-3 must pass before VIS-4 heavy interaction validation.
- Archive follows only after VIS-4 passes or the user explicitly accepts a recorded blocker / residual risk.

#### Risks and Notes

- Official capability rules may evolve; invoking by name avoids a pinned-path dependency but still requires future compatibility review.
- Inline visuals are supplementary; exact Task IDs and test verdicts remain in Markdown.
- A sent follow-up message does not prove that the requested phase succeeded.
- Generated runtime files must stay outside Git source and governed docs.
- No new dependency or manifest change is planned.

#### Parallelism Assessment

- VIS-1 and VIS-2 are tightly coupled and should execute serially.
- VIS-3 depends on their final text and routes.
- VIS-4 is a later heavy-validation task.
- Parallel implementation would add coordination overhead without a safe independent write set; use one main-agent execution lane under `$m-execute`.
- If the user instead invokes `$m-go`, workers must still respect the serial dependency and bounded write sets.

#### Issue List

- None.

### Execute - Contract And Phase Integration

#### Completed Tasks

- VIS-1: added the shared interactive-output contract and static-to-interactive routing.
- VIS-2: integrated `$m-discuss`, `$m-plan`, `$m-test`, and `$m-archive` with bounded official inline interaction opportunities.
- VIS-3: extended contract coverage, validated and synchronized the five changed skill packages, and verified installed-source parity.

#### Heavy Validation Handoff

- VIS-4 was handed to `$m-test` because it required a representative official render, desktop and narrow-width evidence, keyboard and local-selection checks, and primary follow-up-action validation. The validation completed successfully in the following stage record.

#### Validation Evidence

- Full unit suite: 26 tests passed; 1 Windows symlink test skipped because the current process lacks symlink privilege (`WinError 1314`).
- Skill validation: `m-autoflow`, `m-discuss`, `m-plan`, `m-test`, and `m-archive` all passed.
- Synchronization: all five changed packages were synchronized to the local Codex skill installation.
- Exact parity: source and installed file sets and SHA-256 content matched for all five packages, excluding generated build metadata.
- Repository checks: `git diff --check` passed; no unscoped `$visualize` invocation or hard-coded versioned plugin-cache path remained in the changed contract.

#### Execution Notes

- The official capability is invoked as `$visualize:visualize`, without pinning an installed cache path or version.
- Complete Markdown outcomes remain authoritative and usable when inline rendering or the host bridge is unavailable.
- Inline controls may update local presentation state or send a follow-up request; they cannot directly approve, write files, mutate Git, merge, publish, archive, or clean up.
- Every received follow-up must pass the destination phase's normal entry gate.

#### Issue List

- None for VIS-1 through VIS-3.
- VIS-4 was pending at the end of this stage and is resolved by the `$m-test` record below.

### Test - Representative Inline Interaction Validation

#### Scope And Environment

- Task: VIS-4.
- Preview: official `$visualize:visualize` render helper output opened and operated in the Codex in-app browser.
- Source fragment: `C:\Users\HelloWorld\.codex\visualizations\2026\07\15\019f64f3-44a7-7ec3-b565-80969e1194b8\m-test-validation.html`.
- Desktop evidence: `C:\Users\HelloWorld\.codex\visualizations\2026\07\15\019f64f3-44a7-7ec3-b565-80969e1194b8\m-test-validation-desktop.png`.
- Narrow evidence: `C:\Users\HelloWorld\.codex\visualizations\2026\07\15\019f64f3-44a7-7ec3-b565-80969e1194b8\m-test-validation-narrow.png`.
- Repository source remained clean before this plan update; runtime visualization and evidence stayed outside Git source and governed docs.

#### Heavy Validation Results

| Area | Check | Status | Evidence | Notes |
| --- | --- | --- | --- | --- |
| UI | Exact 736px inner viewport | Passed | desktop screenshot and measured `viewportWidth = scrollWidth = 736` | Four controls and four Lucide icons visible; no clipping or horizontal overflow |
| UI | Exact 320px inner viewport | Passed | narrow screenshot and measured `viewportWidth = scrollWidth = 320` | Controls wrapped cleanly; all buttons remained visible |
| Interaction | Local evidence selection | Passed | operated `回传边界` control | `aria-pressed` and the selected detail changed together |
| Accessibility | Semantic controls and keyboard focus | Passed | browser accessibility snapshot | Four native labeled buttons, native tab order, focus acquisition, visible focus treatment, and pressed-state semantics confirmed |
| Integration | Follow-up action boundary | Passed | captured preview-host payload | Button called `window.openai.sendFollowUpMessage` with `$m-archive`, VIS-1 through VIS-4 context, and an explicit gate-recheck instruction |
| Safety | Direct mutation and external I/O review | Passed | fragment inspection | No file, Git, merge, archive, cleanup, `fetch`, XHR, or WebSocket action in the fragment |
| Regression | Full unit-test discovery | Passed | 26 passed, 1 environment skip | Skip remained the Windows unprivileged symlink case (`WinError 1314`) |

#### Mandatory Review Checklist

- Requirements coverage: Passed.
- Architecture reasonableness: Passed.
- Performance risks (N+1 / repeated computation / excess I/O / lock contention): Passed; the fragment is 3.3 KB and uses four bounded controls with no network or repeated I/O.
- Performance metrics / thresholds: Passed; fragment size is far below the 2 MB ceiling and no horizontal overflow occurred at either required width.
- Usability / user path: Passed.
- Readability and consistency: Passed.
- Extensibility and configuration: Passed; the repository routes by capability name and keeps official rendering rules external.
- Stability and security: Passed.
- Security boundary / permissions / data exposure: Passed.
- Test coverage: Passed.
- Whole-flow / integration validation: Passed.
- Subagent governance and audit: Passed; the serial plan required no delegation, so there was no subagent write set or result to reconcile.

#### Residual Risk

- The preview automation could focus native buttons but did not synthesize Enter / Space activation inside the sandboxed iframe. Native button semantics, focus acquisition, visible focus treatment, mouse activation, local state change, and exact follow-up payload were independently verified. A final inline rendering in the Codex conversation remains the host-level smoke check.
- The preview host logged a `MutationObserver.observe` error on reload. The fragment contains no `MutationObserver`, all required UI and actions continued to work, and the error is attributed to preview infrastructure rather than repository or fragment code.

#### Decision

- Test phase: run.
- Blocked: no.
- VIS-4: complete.
- Next phase: `$m-archive`.
- No archive, merge, cleanup, or workflow closeout was performed by `$m-test`.

## Plan Status

- Discussion: complete
- Requirements: coherent
- Architecture: complete
- Docs routing: confirmed through `$m-docs`
- Worktree: implementation and heavy validation complete for VIS-1 through VIS-4
- Requirements / architecture blockers: none
- Blocked: no
- Implementation authorization: granted through the user's `$m-execute` invocation
- Heavy validation: passed with the residual preview-environment notes recorded above
- Next action: invoke `$m-archive` to close out documentation, merge, and cleanup under its normal gates
