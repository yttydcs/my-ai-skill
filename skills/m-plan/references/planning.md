# Planning Rules

Use this reference for `$m-plan`, the architecture and execution-planning phase of `m-autoflow`.

## Phase Boundary

- Owns architecture design, executable task planning, and `plan.md` / `todo.md`.
- May create or confirm the worktree when `$m-discuss` was skipped.
- Does not own implementation, test execution, code review, archive, merge, or worktree cleanup.
- If the user asks for coding before a confirmed plan exists, stop and produce the plan first.
- Discovery, brainstorming, and optional web research belong in `$m-discuss`.
- If requirements are unreasonable, unsafe, contradictory, or too vague, reject the plan request and return to `$m-discuss` with alternatives.

## Required Checks

1. Confirm the real owning repo and do not assume the wrapper root is the product repo.
2. Confirm `project_root`, `docs_root`, `code_repos`, base branch, worktree path, and participating modules.
3. Read `guide.md` from the repo root when present.
4. Prefer stable docs from the active docs root:
   - `docs/intake` for original request evidence
   - `docs/features` for current user-visible behavior
   - `docs/requirements` for durable capability intent
   - `docs/specs` for architecture and technical contracts
   - `docs/decisions` for constraining architecture choices
   - `docs/lessons` for known recurring pitfalls
5. Consume the `$m-discuss` brief when present, including research findings and rejected options.
6. Use `$m-docs` before finalizing planning docs or declaring stable-doc impact.

## Private Docs Rules

- If the user wants private docs, do not treat code-repo `docs/` as canonical unless explicitly selected.
- If docs may be versioned in a separate Git repository, do not infer remotes, push targets, publication, or backup strategy.
- If no docs root can be identified for behavior-changing work, record a blocker before implementation.
- For multi-repo capabilities, document the feature once in the private docs root and record participating code repos in the plan.
- If `$m-discuss` already created the worktree, verify rather than recreate it.

## Required Plan Contents

- workflow goal and current state
- discussion summary or a note that discussion was skipped / not needed
- repo, branch, base, project root, docs root, code repos, worktree absolute path, and phase
- related intake, features, requirements, specs, decisions, and lessons
- stable-doc impact:
  - intake impact
  - feature impact
  - requirements impact
  - specs impact
  - decision impact
  - lessons known at planning time
- task IDs and executable checklist
- execution scope split:
  - tasks to execute after user approval
  - tasks not to execute in the next execution phase, with reasons such as blocked, out of scope, deferred, research-only, or waiting for separate approval
  - every known task appears in exactly one of these two groups
- per-task goal, files/modules, write set, acceptance, tests, and rollback
- dependencies, risks, and open questions
- parallelism assessment and any allowed sub-agent context package

## Acceptance Traceability

Use the approved brief and stable docs to build a compact acceptance map in the existing plan: `AC ID | Source / exact requirement | Task IDs | Verification / evidence | Status`. Preserve existing acceptance identifiers; otherwise assign stable local IDs such as `AC-01`. Cross-repository plans may reference the same authoritative criteria rather than redefining them. Adding identifiers to an already approved plan does not require renewed approval when meaning and scope are unchanged; an admitted pipeline still follows its existing fingerprint/review rules.

- Cover every material confirmed constraint, including negative requirements, numeric values and units, defaults, ordering and permissions. Record rejected, deferred and open matters with reasons; do not turn them into executable acceptance or silently discard them.
- Check both directions: each executable requirement has an acceptance item and Task owner; each planned behavior has an approved source. A source may justify several criteria or tasks. Use `not applicable` with a reason for decisions that do not define observable behavior.
- Specify the observation boundary and an independent expected result, using existing public interfaces/test patterns when suitable. Bug fixes should normally have a failing reproduction; important new behavior benefits from small test/implementation cycles. Do not mandate TDD for documentation, low-impact styling or every task.
- Carry AC IDs and verification evidence through execution, test and archive. `pending`, `passed`, `failed`, `blocked`, `deferred` and `waived` are distinct; missing evidence and an explicit waiver are never a pass. A heavy-test skip changes verification obligations only under `$m-test` rules, not the required behavior.
- When a decision or criterion changes, record its source and invalidate affected tasks and downstream evidence. Preserve unaffected results only when their inputs and dependencies remain valid. Return for approval when meaning or scope changes; status/evidence updates alone are not new scope.

## Task Slicing

Each Task declares a user-visible or otherwise observable deliverable, its genuine `Blocked by` Task IDs, and an independent verification path. Prefer a narrow complete behavior through the necessary layers, sized to be understood and verified in a fresh agent session. File/module and write-set ownership remain mandatory; they do not define task value by themselves. Do not invent extra tasks merely to fill layers or increase parallelism.

For a wide mechanical migration that cannot land as independent behavior slices, use expand/compatibility -> migration batches -> contract/removal. State where green validation is promised. If batches require an integration branch, make the final integrate-and-verify task explicit; an intermediate batch is not standalone acceptance of the feature. Prefactoring is allowed only when directly necessary, within the approved scope and independently checked.

Show blockers and delivery/verification cues in the existing task details and summary notes; do not add a second competing task list.

## Direct Task Summary Table

After creating or confirming the active `plan.md` / `todo.md`, output a concise task summary table directly to the user.

The table is a readable summary of the active plan artifact. It must not redefine scope, omit known tasks, or conflict with `plan.md` / `todo.md`.

Link the active plan artifact with an absolute clickable path. Add a Mermaid dependency or system-flow diagram only when it materially clarifies execution order, branching, or ownership; the task table remains the source for exact scope and status.

Minimum columns:

- Task ID
- Title
- Scope (`Will execute` / `Will not execute now`)
- Files / Modules
- Acceptance / Tests
- Risk / Notes

Include every known task from the execution scope split. For tasks not executing now, put the reason in `Risk / Notes`.

Example:

```md
| Task ID | Title | Scope | Files / Modules | Acceptance / Tests | Risk / Notes |
| --- | --- | --- | --- | --- | --- |
| T1 | Add personnel list filter | Will execute | `src/features/personnel` | Filter works; focused unit test | Low risk |
| T2 | Export personnel report | Will not execute now | `api/reports` | Not in next phase | Deferred; separate approval |
```

## Blocking Output

When any required prerequisite is missing:

```md
问题清单
- <missing prerequisite>

阻塞：是
禁止进入执行
禁止派发实现子Agent
```
