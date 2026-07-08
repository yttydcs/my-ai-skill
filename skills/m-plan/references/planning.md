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

## Blocking Output

When any required prerequisite is missing:

```md
问题清单
- <missing prerequisite>

阻塞：是
禁止进入执行
禁止派发实现子Agent
```
