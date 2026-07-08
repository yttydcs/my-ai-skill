# Initialization Rules

Use this file before stage `1`.

## Ownership Rule

- The main agent must perform initialization personally.
- Do not use sub-agents during initialization.

## Mandatory Checks

1. Read `guide.md` from the current repository root if it exists.
2. Confirm the project root, docs root, participating repo or repos, modules, and base branch.
3. Ensure every participating repo has:
   - a dedicated semantic branch
   - a dedicated git worktree
4. Require worktrees under the current project root's own `worktrees\` directory (`<project-root>\worktrees\`).
5. Select one active execution worktree and keep all implementation there.

## Project / Docs Root Rule

- `project_root` is the local umbrella directory for the work.
- `docs_root` is the governed documentation root. It may be a local folder or a separate local/private Git repository.
- `code_repos` are implementation repositories. Do not assume their `docs/` folders are canonical when the user has a private docs root.
- `active_worktree` is the dedicated worktree where implementation happens.
- Record `project_root`, `docs_root`, `code_repos`, and `active_worktree` in the plan when they are relevant.
- If a private docs root is expected but cannot be identified, stop before implementation and ask or record a blocker.

## Cross-repo Rule

- For multi-repo workflows, every participating repo must have:
  - its own dedicated branch
  - its own dedicated worktree
  - its own root `plan.md` or `todo.md`
- Record every additional worktree path, branch, dependency, and ownership boundary in the main plan.
- Cross-repo product or feature truth belongs in the private docs root, not duplicated across code repos.

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
- Do not write governed private docs into a pushable code repo unless the user explicitly selected that repo as the docs root.

## Docs Git Rule

- A docs root may have its own Git repository.
- Do not add remotes, change remotes, push, publish, or choose backup targets unless the user explicitly asks.
- Keep docs repo commits separate from code repo commits when both are involved.

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
