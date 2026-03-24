# Initialization Rules

Use this file before stage `1`.

## Ownership Rule

- The main agent must perform initialization personally.
- Do not use sub-agents during initialization.

## Mandatory Checks

1. Read `guide.md` from the current repository root if it exists.
2. Confirm the participating repo or repos, modules, and base branch.
3. Ensure every participating repo has:
   - a dedicated semantic branch
   - a dedicated git worktree
4. Require worktrees under `D:\project\MyFlowHub3\worktrees\`.
5. Select one active execution worktree and keep all implementation there.

## Cross-repo Rule

- For multi-repo workflows, every participating repo must have:
  - its own dedicated branch
  - its own dedicated worktree
  - its own root `plan.md` or `todo.md`
- Record every additional worktree path, branch, dependency, and ownership boundary in the main plan.

## Branch Rules

- Allowed prefixes:
  - `feat/`
  - `fix/`
  - `refactor/`
  - `perf/`
  - `chore/`
- Do not use `flow`, `workflow`, `task`, or `experiment` in the branch name.

## Worktree Rules

- Treat the main repo path as control-plane only.
- Do not perform implementation edits in the main repo.
- Keep one `plan.md` or `todo.md` per active workflow worktree.
- For multi-repo workflows, record each worktree path, branch, dependency, and ownership boundary in the main plan.

## Main Repo Restrictions

Only allow these actions in the main repo path:

- worktree management
- merge, release, or integration validation
- workflow convergence

If any exception is necessary, require it to be explained in the final `docs/change` archive.

## Allowed Work During Initialization

- read constraints and repository state
- create branch and worktree
- confirm baseline
- create documentation skeletons

## Forbidden Work During Initialization

- writing business logic
- changing runtime behavior
- skipping directly to coding

## Blocking Output

If the worktree is missing or not ready, output:

```md
问题清单
- <missing prerequisite>

阻塞：是
禁止进入 1 / 2 / 3.1 / 3.2
```
