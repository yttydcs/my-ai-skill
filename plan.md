# Plan - m-discuss Grill Mode

## Workflow Information

- Repo: `D:\project\my-ai-skills`
- Branch: `feat/m-discuss-grill-mode`
- Base: `main` at `b75bab8c8b325cd91e6d2146d69caa49836dc28b`
- Project Root: `D:\project\my-ai-skills`
- Docs Root: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode\docs`
- Code Repos: `D:\project\my-ai-skills`
- Worktree: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode`
- Current Stage: `$m-execute` complete; awaiting optional `$m-test` or `$m-archive`

## Stage Records

### Initialization

- `guide.md`: read; every repository modification must be committed automatically with an English commit message matching repository history.
- Project/docs/code repo confirmation: one repository owns the skills, manifests, tests, distribution files, and governed docs. No separate private docs root is configured or expected for this workflow.
- Base/worktree confirmation: clean `main`; dedicated branch `feat/m-discuss-grill-mode`; dedicated worktree created under the project-root `worktrees` directory.
- Main checkout remains control-plane only. Planning and future implementation occur in the dedicated worktree.

### Discuss - Discovery And Requirements Shaping

#### Goal

Integrate the useful interview discipline from the public `grill-me`/`grilling` skills into `$m-discuss` without adding an external runtime dependency or changing normal discussion behavior.

#### Scope

- Explicitly triggered Grill Mode inside `$m-discuss`.
- Local interview protocol, phase routing, manifest packaging, contract tests, stable docs, distribution sync, and installed-copy sync.

#### Assumptions

- The user accepted the recommended internal-mode direction by invoking `$m-plan` immediately after the discussion result.
- `$m-discuss` remains the single public phase entry point.
- The existing docs tree in this repository is the governed docs root for this workflow.

#### Open Questions

- None blocking. Exact trigger examples may be refined during implementation while preserving the explicit-only rule.

#### Options Considered

- External `grill-me`/`grilling` dependencies.
- Mandatory grilling for all discussions.
- Separate `$m-grill` entry point.
- Explicit internal Grill Mode.

#### Rejected Options

- External dependencies: rejected for upstream and invocation coupling.
- Mandatory mode: rejected for latency and backward-compatibility impact.
- Separate skill: rejected for overlapping phase ownership and added workflow complexity.

#### Recommended Direction

Add a conditional `references/grilling.md` protocol owned by `$m-discuss`. Keep normal discussion unchanged and always converge back to the existing discussion brief and exit gate.

#### Research Summary

- Upstream `grill-me` is a thin user-invoked wrapper: <https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md>
- The reusable behavior is in `grilling`: <https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md>
- The source repository uses the MIT License: <https://github.com/mattpocock/skills/blob/main/LICENSE>
- Relevant failure reports:
  - bundled questions: <https://github.com/mattpocock/skills/issues/221>
  - implementation starts after grilling: <https://github.com/mattpocock/skills/issues/240>
  - excessive question count and natural-language escape hatch: <https://github.com/mattpocock/skills/issues/44>

#### Worktree / Branch / Docs Root Status

- Worktree: ready and clean at creation.
- Branch: `feat/m-discuss-grill-mode` from current `main`.
- Docs root: repository `docs` tree inside the dedicated worktree.
- Plan path: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode\plan.md`.

#### Issue List

- None blocking.

### Plan - Requirements And Architecture

#### Discussion Summary

The external skill is valuable as an interaction protocol, not as a dependency. `$m-discuss` already owns research, decisions, durable handoff, docs routing, and phase boundaries, so the correct integration is a conditional internal mode.

#### Accepted / Rejected Requirements

Accepted:

- explicit-only activation;
- one decision question per turn;
- recommended answer and rationale per question;
- facts researched before decisions are asked;
- depth-first decision dependency resolution;
- user confirmation before declaring shared understanding;
- standard discussion brief after the interview;
- no automatic planning or implementation;
- natural-language stop/wrap-up without a fixed question cap;
- no external skill dependency.

Rejected:

- automatic activation for every vague request;
- batching several judgment questions into one turn;
- hard-coded question limits;
- copying the seven-line wrapper without its primitive;
- starting implementation when the interview ends.

#### Requirements Analysis

##### Goal

Give users an opt-in, high-pressure way to expose and resolve hidden decisions before planning while preserving `$m-discuss` as the authoritative discovery phase.

##### Scope

In scope:

- source skill and reference changes;
- package manifest and version;
- focused contract tests;
- stable workflow docs;
- distribution and installed-copy sync;
- focused and full repository validation.

Out of scope:

- separate public skill installation;
- direct OpenAI/Claude tool-specific question APIs;
- persistent interview state outside the current task and final brief;
- implementation of `$m-plan` or downstream phase changes;
- automatic upstream update tracking.

##### Use Cases

1. A user invokes `$m-discuss` and explicitly says “grill me” to stress-test a plan.
2. A user asks for one-at-a-time hard questions about a design with dependent choices.
3. A user answers vaguely; the current branch is narrowed before moving on.
4. A discoverable fact is needed; the agent inspects the environment rather than asking the user.
5. A user asks to wrap up early; the agent emits the standard brief with unresolved decisions clearly marked.
6. The interview reaches shared understanding; the user confirms, and `$m-discuss` reports readiness for `$m-plan` without entering it.

##### Functional Requirements

- `SKILL.md` must define explicit Grill Mode triggers and conditionally load `references/grilling.md`.
- Ordinary `$m-discuss` invocations must keep current semantics.
- Grill Mode must maintain a decision snapshot containing confirmed, rejected, deferred, and open decisions.
- Before each question, the agent must resolve discoverable facts from available project or external sources when authorized.
- Each turn must contain exactly one judgment question, its recommended answer, and a concise reason.
- Dependent branches must not be asked before their parent decision is resolved or explicitly deferred.
- The agent must wait for the user's answer before continuing.
- Repeated or vague answers must be handled by narrowing the same branch rather than silently assuming agreement.
- The user may stop or request a summary at any time.
- Completion requires explicit user confirmation of shared understanding.
- Early stop with blocking open decisions must block the `$m-plan` handoff.
- Successful completion must still produce every field required by the normal `$m-discuss` exit gate.
- The mode must never implement, enter `$m-plan`, or perform archive/merge/push/cleanup automatically.
- The reference must include upstream attribution and license links without requiring the external skill at runtime.

##### Non-functional Requirements

- Backward compatible and additive.
- Conditional reference loading to avoid unnecessary context cost.
- Host-neutral instructions with a plain-text question fallback.
- No new executable dependency or network requirement.
- Prompt contract protected by deterministic standard-library tests.
- Maintain existing naming, packaging, dist, and install conventions.

##### Inputs / Outputs

- Input: existing `$m-discuss` request plus an explicit grilling/pressure-test intent.
- Intermediate state: in-task decision snapshot; no new persistent runtime format.
- Output: the existing decision-ready `$m-discuss` brief with resolved and unresolved decisions reflected in its normal fields.

##### Edge Cases

- No meaningful open decisions remain: ask only for shared-understanding confirmation, then emit the brief.
- A fact lookup fails: report the evidence gap and ask a decision only if the user actually owns the missing choice.
- The user changes a parent decision: invalidate affected child decisions and revisit only those branches.
- The user stops early: summarize confirmed state and keep blocking questions open.
- The user asks to implement during Grill Mode: stop at the discussion boundary and route to `$m-plan`.
- The user invokes ordinary `$m-discuss` without a Grill trigger: do not apply the one-question loop.
- A host lacks a structured question control: use one plain-text question and wait.

##### Acceptance Criteria

- Explicit Grill triggers route to the new local reference.
- Vague requests alone do not activate Grill Mode.
- Contract text enforces one question, recommendation, wait, facts/decisions separation, depth-first ordering, confirmation, early wrap-up, and no implementation.
- The normal discussion brief and exit gate remain authoritative.
- Manifest, source, dist, and installed copies include the new reference and agree after sync.
- Focused and full repository tests pass.

##### Risks

- Models may still batch questions unless the contract and tests use strong unambiguous wording.
- Open-ended interviews may become repetitive; decision-state tracking and deduplication must mitigate this without a numeric cap.
- Over-broad triggers could slow normal discussions; activation must remain explicit.
- Sync replaces the exact dist/install skill directories; execution must verify targets and source state before invoking it.

#### Architecture Design

##### Overall Solution

Use `$m-discuss/SKILL.md` as a conditional router, `references/grilling.md` as the interview engine, and `references/discussion.md` as the phase/brief authority. The mode ends by returning to the normal discussion exit gate.

##### Alternatives Considered

- External dependency: less local code, but brittle invocation and upstream coupling.
- Inline all rules in `SKILL.md`: simple packaging, but bloats the always-loaded entry file.
- Separate public skill: clean primitive boundary, but duplicates discovery entry points.

##### Module Responsibilities

- `skills/m-discuss/SKILL.md`: trigger detection, conditional reference loading, workflow ordering, phase boundary.
- `skills/m-discuss/references/grilling.md`: decision snapshot, fact lookup, single-question loop, completion/early-stop rules, attribution.
- `skills/m-discuss/references/discussion.md`: required brief, planning handoff, worktree rule, compatibility with Grill Mode.
- `manifests/m-discuss.json`: package version, dependencies, reference inclusion.
- `tests/test_m_discuss_grill_contract.py`: deterministic source/manifest/docs contract.
- `docs/features/m-autoflow-workflow.md`: current user-visible workflow after implementation.
- `docs/requirements/m-autoflow-skill.md`: durable behavioral requirements.
- `docs/specs/m-autoflow-skill.md`: technical routing and validation contract.
- `dist/codex/m-discuss` and installed `m-discuss`: generated/synced copies, not hand-edited.

##### Data / Call Flow

1. User invokes `$m-discuss`.
2. Entry skill evaluates explicit Grill Mode intent.
3. Normal mode follows the existing workflow unchanged.
4. Grill Mode loads `references/grilling.md`, collects facts, and initializes the decision snapshot.
5. The highest-risk unresolved parent decision produces one recommended question.
6. The agent waits, records the answer, and updates/invalidate branches as needed.
7. The loop ends on explicit shared-understanding confirmation or user-requested wrap-up.
8. `$m-discuss` emits the standard brief and states whether `$m-plan` is allowed.

##### Interface Drafts

```text
mode = explicit_grill_intent ? GRILL : STANDARD

if mode == GRILL:
  load references/grilling.md
  inspect facts
  initialize decision snapshot
  while unresolved decision remains and user has not requested wrap-up:
    select highest-risk unresolved parent branch
    ask exactly one decision question with recommendation and reason
    wait for user
    update snapshot and dependent branches
  request explicit shared-understanding confirmation when no blocking branch remains

emit standard m-discuss brief
stop before m-plan or implementation
```

##### Error Handling and Safety

- Treat missing evidence as an explicit gap, not a guessed fact.
- Treat ambiguous user answers as unresolved.
- Never convert a recommendation into user agreement.
- Preserve unresolved blockers in the final brief.
- Preserve the existing prohibition on implementation and destructive workflow actions.

##### Performance and Testing Strategy

- Load the new reference only when the explicit trigger passes.
- Add a focused Python `unittest` module that reads source files and asserts the complete contract and manifest inclusion.
- Run skill validation, focused tests, full test discovery, whitespace checks, sync, and post-sync parity checks.
- Do not add runtime code or dependencies.

##### Extensibility Design Points

- Future modes can add separate references while keeping `$m-discuss` as the router.
- Decision snapshot vocabulary can be reused by a future documented interview mode without changing the normal brief.
- Upstream behavior can be reviewed manually without making local correctness depend on upstream changes.

#### Issue List

- None blocking.

### Stage 3.1 - Planning

#### Project Goal and Current State

Current `$m-discuss` supports broad discovery and handoff but lacks a strict one-question decision interview. The goal is an additive explicit mode that fills that gap without changing downstream phase ownership.

#### Docs Governance Routing Decision

- Original request evidence: new intake record.
- Architecturally significant choice: new decision record.
- Current user-visible workflow: update during implementation, after source behavior exists.
- Durable behavior: update requirements during implementation.
- Technical routing/validation contract: update spec during implementation.
- Active execution control: this root `plan.md`.
- Completed result: later `$m-archive` change record.
- Reusable lesson: none known yet.

#### Related Intake / Features / Requirements / Specs / Decisions / Lessons

- Intake: `docs/intake/2026-07-20_m-discuss-grill-mode.md`
- Feature: `docs/features/m-autoflow-workflow.md`
- Requirements: `docs/requirements/m-autoflow-skill.md`
- Spec: `docs/specs/m-autoflow-skill.md`
- Decision: `docs/decisions/2026-07-20_m-discuss-grill-mode.md`
- Lessons: `docs/lessons/python-unittest-discovery-nonpackage-tests.md` applies to focused test invocation.

#### Stable Docs Impact

- Intake impact: add; completed during planning.
- Feature impact: clarify during execution after behavior is implemented.
- Requirements impact: clarify during execution.
- Specs impact: clarify during execution.
- Decision impact: add; completed during planning.
- Lessons impact: none; reuse the existing non-package unittest discovery lesson.

#### Executable Task List

- `GM-1`: implement the conditional Grill Mode source contract.
- `GM-2`: add packaging/version changes and focused contract tests.
- `GM-3`: align stable workflow, requirement, and spec docs with implemented behavior.
- `GM-4`: validate, sync source to dist/installed copies, and verify parity.
- `GM-5`: archive, merge, and clean up through `$m-archive`; not part of the next execution phase.

#### Execution Scope After Approval

##### Will Execute

- `GM-1`
- `GM-2`
- `GM-3`
- `GM-4`

##### Will Not Execute Now

- `GM-5`: deferred to the separate `$m-archive` phase after implementation and validation.

#### Task Details

##### GM-1 - Implement Conditional Grill Mode

- Owner: main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode\plan.md`
- Goal: add explicit-only mode routing and the reusable local interview protocol while preserving normal discussion.
- Files / Modules:
  - `skills/m-discuss/SKILL.md`
  - `skills/m-discuss/references/discussion.md`
  - `skills/m-discuss/references/grilling.md` (new)
- Write Set: only the files above.
- Acceptance:
  - explicit trigger and conditional loading are unambiguous;
  - the full interview, confirmation, early-stop, and no-implementation contract is present;
  - normal `$m-discuss` behavior and exit brief remain authoritative.
- Test Points: source contract assertions from `GM-2`; manual contradiction search.
- Rollback: revert the three skill-source changes.

##### GM-2 - Package And Protect The Contract

- Owner: main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode\plan.md`
- Goal: include the new reference in the package and prevent prompt-contract regressions.
- Files / Modules:
  - `manifests/m-discuss.json`
  - `tests/test_m_discuss_grill_contract.py` (new)
- Write Set: only the manifest and focused test module.
- Acceptance:
  - manifest version reflects the additive capability and lists `references/grilling.md`;
  - tests cover explicit activation, normal-mode preservation, single-question sequencing, recommended answers, fact lookup, decision dependencies, wrap-up, confirmation, standard brief, and phase boundary;
  - no external skill dependency is declared.
- Test Points: `python -m unittest discover -s tests -p "test_m_discuss_grill_contract.py"`.
- Rollback: revert manifest/test changes; the source reference then remains unshipped and must also be rolled back through `GM-1`.

##### GM-3 - Align Stable Documentation

- Owner: main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode\plan.md`
- Goal: make current workflow behavior, durable requirements, and technical contracts match the implemented mode.
- Files / Modules:
  - `docs/features/m-autoflow-workflow.md`
  - `docs/requirements/m-autoflow-skill.md`
  - `docs/specs/m-autoflow-skill.md`
- Write Set: the three stable docs only; existing indexes need no update because no new stable leaf is added.
- Acceptance:
  - docs distinguish ordinary discussion from explicit Grill Mode;
  - requirements describe user-visible acceptance and phase boundaries;
  - spec describes routing, reference/package structure, contract tests, and sync requirements;
  - docs link the intake and decision where appropriate.
- Test Points: focused doc contract assertions and link/path review.
- Rollback: revert the three stable-doc changes without altering intake or the accepted planning decision.

##### GM-4 - Validate And Sync

- Owner: main agent
- Worktree: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode\plan.md`
- Goal: prove source integrity and synchronize exact generated copies.
- Files / Modules:
  - `dist/codex/m-discuss/**`
  - `C:\Users\HelloWorld\.codex\skills\m-discuss/**` (installed generated copy)
- Write Set: generated dist and installed `m-discuss` directories through the existing sync tool only.
- Acceptance:
  - `tools/validate-skills.ps1 -Skill m-discuss` passes;
  - focused and full `unittest` suites pass;
  - `git diff --check` passes;
  - `tools/sync-skills.ps1 -Skill m-discuss` succeeds after source validation;
  - source, dist, and installed copies contain the new reference and match apart from generated build metadata;
  - unrelated installed skills and repository files remain untouched.
- Test Points:
  - `python -m unittest discover -s tests -p "test_m_discuss_grill_contract.py"`
  - `python -m unittest discover -s tests -p "test_*.py"`
  - `powershell -File tools/validate-skills.ps1 -Skill m-discuss`
  - `powershell -File tools/sync-skills.ps1 -Skill m-discuss`
  - post-sync tree/parity comparison
- Rollback: restore the previous installed/dist `m-discuss` from Git/source by reverting implementation commits and rerunning the existing sync tool from the restored source.

##### GM-5 - Archive And Close Out

- Owner: main agent in a later `$m-archive` phase
- Worktree: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode`
- Plan Path: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode\plan.md`
- Goal: create the change archive, reassess lessons, merge, and clean the worktree under archive rules.
- Files / Modules: `docs/change`, optional `docs/lessons`, archived `docs/plan`, control-plane Git state.
- Write Set: intentionally excluded from the next execution phase.
- Acceptance: governed archive complete, validation evidence recorded, stable-doc impact confirmed, merge/cleanup safety checks pass.
- Test Points: defined by `$m-archive`.
- Rollback: retain branch/worktree and stop before merge if any archive or safety gate fails.

#### Dependencies

- `GM-1` precedes `GM-2` because tests assert the final source contract.
- `GM-2` precedes `GM-3` so documentation can cite the actual packaged structure and validation names.
- `GM-1` through `GM-3` must pass before `GM-4` syncs generated copies.
- `GM-5` begins only after execution and validation finish.

#### Risks and Notes

- The prompt behavior is model-mediated; tests validate instruction completeness, not every possible model response.
- The new mode must remain explicit-only to prevent normal discussion latency regressions.
- Sync is exact-directory replacement for known targets and must run only after validation.
- Upstream sources are research inputs, not runtime authorities.

#### Parallelism Assessment

- No implementation sub-agents will be used. The user did not request delegation, current host policy does not permit proactive delegation, and the tasks have sequential contract dependencies with overlapping documentation context.
- The main agent owns all requirements, architecture, edits, integration, and acceptance.

#### Issue List

- None blocking.

## Plan Confirmation Gate

- Plan status: approved by the user's `$m-execute` invocation.
- Execution status: `GM-1` through `GM-4` completed.
- Archive status: not started; `GM-5` remains outside this execution phase.

## Execution Record - 2026-07-20

### Completed Tasks

- `GM-1`: completed in `ee906f6` (`feat: add m-discuss grill mode`).
- `GM-2`: completed in `6698149` (`test: protect m-discuss grill contract`).
- `GM-3`: completed in `2174254` (`docs: define m-discuss grill mode`).
- `GM-4`: completed after source validation, exact sync, installed validation, and hash parity checks.
- `GM-5`: not executed; retained for `$m-archive`.

### Validation Evidence

- Focused contract discovery: 8 tests passed.
- Full repository discovery: 40 tests passed, 1 existing conditional test skipped.
- Source skill validation: passed for `m-discuss`.
- Installed skill validation: passed for `C:\Users\HelloWorld\.codex\skills\m-discuss`.
- `git diff --check`: passed.
- Source -> dist parity: 5 files matched by SHA-256, excluding generated `.build-info.json`.
- Source -> installed parity: 5 files matched by SHA-256, excluding generated `.build-info.json`.
- Dist and installed build metadata: version `0.2.0`.
- Dist is intentionally ignored by `.gitignore`; sync produced no repository-tracked dist change.

### Validation Note

The first dotted unittest invocation failed before loading any test because this repository's `tests/` directory is not a Python package. The existing `docs/lessons/python-unittest-discovery-nonpackage-tests.md` guidance was applied, the plan commands were corrected to discovery syntax, and the focused and full suites then passed.

### Residual Validation

- No heavy `$m-test` run occurred. The change is a prompt/package/documentation contract with deterministic tests and no runtime UI, schema, network, security-boundary, or performance behavior.
- A live conversational Grill Mode trial remains optional if model-behavior evidence is desired before archive.
