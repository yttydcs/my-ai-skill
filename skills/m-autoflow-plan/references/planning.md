# Planning Rules

Use this reference for the plan phase of `m-autoflow`.

## Phase Boundary

- Owns initialization, requirements analysis, architecture design, and `plan.md` / `todo.md`.
- Does not own implementation, test execution, code review, archive, merge, or worktree cleanup.
- If the user asks for coding before a confirmed plan exists, stop and produce the plan first.
- Optional web research belongs before or during planning only when the user explicitly asks for online research, current/latest external facts, or source-backed investigation. Use `$m-autoflow-research`; do not browse by default.

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
5. If explicit web research was requested, record cited findings and separate confirmed facts from inference before using them in requirements or architecture.
6. Use `$m-docs` before finalizing planning docs or declaring stable-doc impact.

## Private Docs Rules

- If the user wants private docs, do not treat code-repo `docs/` as canonical unless explicitly selected.
- If docs may be versioned in a separate Git repository, do not infer remotes, push targets, publication, or backup strategy.
- If no docs root can be identified for behavior-changing work, record a blocker before implementation.
- For multi-repo capabilities, document the feature once in the private docs root and record participating code repos in the plan.

## Required Plan Contents

- workflow goal and current state
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

## Blocking Output

When any required prerequisite is missing:

```md
问题清单
- <missing prerequisite>

阻塞：是
禁止进入执行
禁止派发实现子Agent
```
