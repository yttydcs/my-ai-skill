# m:docs Integration

Use this file whenever the workflow touches planning, intake, features, requirements, specs, decisions, change archives, lessons, docs roots, or docs indexes.

## Explicit Invocation Rule

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
