# m:docs Integration

Use this file whenever the workflow touches planning, intake, features, requirements, specs, decisions, change archives, lessons, docs roots, or docs indexes.

## Storage authority

Resolve the project's explicit Agent Memory binding before applying file paths below. A binding declared in AGENTS or project-scoped M_MEMORY_BINDING selects `../../m-memory/SKILL.md` and its relevant adapter. Record the binding path and library IDs once in local workflow state and carry them across worktrees; never infer a library from a directory name. With that authority, current specs/requirements and durable archive facts are service objects, and the category/impact checks below still apply. File bootstrap, README indexes and docs/plan archival do not apply: local plan/todo, execution traces and routine tests remain local and are not summarized into memory. Commit only actual durable changes at phase boundaries. No service connection means an explicit memory failure, not permission to read/write old docs. Without a binding, the existing file workflow remains in force.

## Explicit Invocation Rule

Invocation means applying `$m-docs`, not reloading its unchanged instructions on every phase. Reuse confirmed routing and still-current source content under `context-budget.md`; reassess affected categories against the current change. Required impact fields may share one table or sentence (for example, `Intake / Requirements / Specs / Decisions: none`) as long as every category has an explicit disposition. Write searchable lesson cues only when a lesson is needed.

Do not rely on implicit skill triggering. State the invocation explicitly, for example:

```text
使用 $m-docs 校验计划文档路由、docs_root、stable-doc 影响和 lessons 查询入口。
```

## Stage 3.1 Requirements

Before confirming `plan.md`:

1. Use `$m-docs`.
2. Identify the active `docs_root` and whether it is separate from the code repo.
3. Check whether the docs tree needs bootstrapping or repair.
4. Check whether the relationship between plan, intake, features, requirements, specs, decisions, change, and lessons is clear.
5. Decide the canonical destination for:
   - original request evidence -> `intake`
   - current user-visible feature truth -> `features`
   - durable capability intent -> `requirements`
   - technical contracts -> `specs`
   - architecture decisions -> `decisions`
   - workflow results -> `change`
   - reusable troubleshooting knowledge -> `lessons`
6. If the relationship is unclear, stop before entering `3.2`.
7. Record:
   - `Docs root: <path or unresolved>`
   - `Intake impact: none | clarify | add`
   - `Feature impact: none | clarify | add | deprecate`
   - `Requirements impact: none | clarify | add | deprecate`
   - `Specs impact: none | clarify | add | deprecate`
   - `Decision impact: none | add | supersede`
   - related intake paths
   - related feature paths
   - related requirements paths
   - related specs paths
   - related decision paths
   - related lessons paths when already relevant

## Root Plan Exception

This workflow keeps the active control document at the worktree root as `plan.md` or `todo.md`.

- Treat this as a control-plane exception required by the workflow.
- Do not let it replace `docs/plan/` as the archive category for retained planning records.

## Stage 4 Requirements

Before treating the archive as complete:

1. Use `$m-docs`.
2. Confirm the archive target docs root.
3. Confirm whether `intake` changed.
4. Confirm whether `features` changed.
5. Confirm whether `requirements` changed.
6. Confirm whether `specs` changed.
7. Confirm whether `decisions` changed.
8. Confirm whether a `lessons` document is needed and record why.
9. If a lesson is needed, create or update `docs/lessons` and record the related lesson paths.
10. Capture searchable lesson cues:
    - symptoms
    - trigger conditions
    - keywords or error text
    - quick checks
11. Confirm whether `docs/README.md` or category indexes need updates.
12. Do not mark stage `4` complete until those checks are recorded.

## Private Publication Rule

- Do not add docs remotes, change docs remotes, push docs, publish docs, or choose backup targets unless the user explicitly asks.
- If a docs root is a Git repository, record whether changes are local-only.

## Escalation Conditions

Stop and ask for clarification when:

- the requested behavior conflicts with written stable docs
- multiple docs compete as the source of truth
- stable documentation is required but missing and cannot be inferred from the confirmed workflow
- a private docs root is required but cannot be identified
- the only candidate docs location is inside a pushable code repo and the user expects private docs
