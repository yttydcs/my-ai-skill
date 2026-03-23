# Docs Governor Integration

Use this file whenever the workflow touches planning, requirements, specs, change archives, lessons, or docs indexes.

## Explicit Invocation Rule

Do not rely on implicit skill triggering. State the invocation explicitly, for example:

```text
使用 $docs-governor 校验计划文档路由、requirements/specs 影响和 lessons 查询入口。
```

## Stage 3.1 Requirements

Before confirming `plan.md`:

1. Use `$docs-governor`.
2. Check whether the repository docs tree needs bootstrapping or repair.
3. Check whether the relationship between plan, requirements, specs, change, and lessons is clear.
4. Decide the canonical destination for:
   - stable truth -> `requirements` or `specs`
   - workflow results -> `change`
   - reusable troubleshooting knowledge -> `lessons`
5. If the relationship is unclear, stop before entering `3.2`.
6. Record:
   - `Requirements impact: none | clarify | add | deprecate`
   - `Specs impact: none | clarify | add | deprecate`
   - related requirements paths
   - related specs paths
   - related lessons paths when already relevant

## Root Plan Exception

This workflow keeps the active control document at the worktree root as `plan.md` or `todo.md`.

- Treat this as a control-plane exception required by the workflow.
- Do not let it replace `docs/plan/` as the archive category for retained planning records.

## Stage 4 Requirements

Before treating the archive as complete:

1. Use `$docs-governor`.
2. Confirm whether `requirements` changed.
3. Confirm whether `specs` changed.
4. Confirm whether a `lessons` document is needed and record why.
5. If a lesson is needed, create or update `docs/lessons` and record the related lesson paths.
6. Capture searchable lesson cues:
   - symptoms
   - trigger conditions
   - keywords or error text
   - quick checks
7. Confirm whether `docs/README.md` or category indexes need updates.
8. Do not mark stage `4` complete until those checks are recorded.

## Escalation Conditions

Stop and ask for clarification when:

- the requested behavior conflicts with written requirements or specs
- multiple docs compete as the source of truth
- stable documentation is required but missing and cannot be inferred from the confirmed workflow
