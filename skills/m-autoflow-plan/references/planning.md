# Planning Rules

Use this reference for the plan phase of `m-autoflow`.

## Phase Boundary

- Owns initialization, requirements analysis, architecture design, and `plan.md` / `todo.md`.
- Does not own implementation, test execution, code review, archive, merge, or worktree cleanup.
- If the user asks for coding before a confirmed plan exists, stop and produce the plan first.
- Optional web research belongs before or during planning only when the user explicitly asks for online research, current/latest external facts, or source-backed investigation. Use `$m-autoflow-research`; do not browse by default.

## Required Checks

1. Confirm the real owning repo and do not assume the wrapper root is the product repo.
2. Read `guide.md` from the repo root when present.
3. Confirm branch, base branch, worktree path, and participating modules.
4. Prefer stable docs:
   - `docs/requirements` for requirements
   - `docs/specs` for architecture
   - `docs/lessons` for known recurring pitfalls
5. If explicit web research was requested, record cited findings and separate confirmed facts from inference before using them in requirements or architecture.
6. Use `$m-docs` before finalizing planning docs or declaring requirements/spec impact.

## Required Plan Contents

- workflow goal and current state
- repo, branch, base, worktree absolute path, and phase
- related requirements, specs, and lessons
- task IDs and executable checklist
- execution scope split:
  - tasks to execute after user approval
  - tasks not to execute in the next execution phase, with reasons such as blocked, out of scope, deferred, research-only, or waiting for separate approval
  - every known task appears in exactly one of these two groups
- per-task goal, files/modules, write set, acceptance, tests, and rollback
- dependencies, risks, and open questions
- parallelism assessment and any allowed sub-agent context package

## Blocking Output

When any required prerequisite is missing:

```md
问题清单
- <missing prerequisite>

阻塞：是
禁止进入执行
禁止派发实现子Agent
```
