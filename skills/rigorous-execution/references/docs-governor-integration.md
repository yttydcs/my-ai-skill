# Docs Governor Integration

Use this file whenever the workflow touches planning, requirements, specs, change archives, lessons, or docs indexes.

## Explicit Invocation Rule

Do not rely on implicit skill triggering. State the invocation explicitly, for example:

```text
使用 $docs-governor 校验计划文档路由和 requirements/specs 影响。
```

## Stage 3.1 Requirements

Before confirming `plan.md`:

1. Use `$docs-governor`.
2. Check whether the repository docs tree needs bootstrapping or repair.
3. Check whether the relationship between plan, requirements, specs, change, and lessons is clear.
3. Decide the canonical destination for:
   - stable truth -> `requirements` or `specs`
   - workflow results -> `change`
4. If the relationship is unclear, stop before entering `3.2`.
5. Record:
   - `Requirements impact: none | clarify | add | deprecate`
   - `Specs impact: none | clarify | add | deprecate`
   - related requirements paths
   - related specs paths

## Root Plan Exception

This workflow keeps the active control document at the worktree root as `plan.md` or `todo.md`.

- Treat this as a control-plane exception required by the workflow.
- Do not let it replace `docs/plan/` as the archive category for retained planning records.

## Stage 4 Requirements

Before treating the archive as complete:

1. Use `$docs-governor`.
2. Confirm whether `requirements` changed.
3. Confirm whether `specs` changed.
4. Confirm whether a `lessons` document is needed.
5. Confirm whether `docs/README.md` or category indexes need updates.
6. Do not mark stage `4` complete until those checks are recorded.

## Escalation Conditions

Stop and ask for clarification when:

- the requested behavior conflicts with written requirements or specs
- multiple docs compete as the source of truth
- stable documentation is required but missing and cannot be inferred from the confirmed workflow
