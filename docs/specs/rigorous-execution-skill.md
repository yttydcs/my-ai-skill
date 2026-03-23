# Rigorous Execution Skill Spec

## Architecture Overview

The skill is packaged as `skills/rigorous-execution` and kept intentionally small. Detailed operational rules live in `references/` so the main `SKILL.md` remains trigger-friendly and efficient.

## Package Contract

- Source package: `skills/rigorous-execution`
- UI metadata: `skills/rigorous-execution/agents/openai.yaml`
- Install metadata: `manifests/rigorous-execution.json`
- Install flow:
  - source -> `dist/codex/rigorous-execution` -> `C:\Users\HelloWorld\.codex\skills\rigorous-execution`

## Trigger Contract

The skill is manual-invocation-only.

- Invoke it explicitly as `$rigorous-execution`.
- `skills/rigorous-execution/agents/openai.yaml` must set:
  - `policy.allow_implicit_invocation: false`

## Workflow Contract

- Initialization precedes stage `1`.
- Stage order is fixed:
  - `1. requirements`
  - `2. architecture`
  - `3.1 plan`
  - `3.2 implementation`
  - `3.3 review`
  - `4. archive`
- Only one stage may be active at a time.
- Any rollback must state the reason and update the affected documents.
- Stage `1` prioritizes relevant docs under `docs/requirements` when they exist.
- Stage `2` prioritizes relevant docs under `docs/specs` when they exist.
- Active workflow control stays in the worktree root as `plan.md` or `todo.md`.
- `docs/change/YYYY-MM-DD_topic.md` is required before a workflow counts as complete.
- After stage `4`, the workflow must ask whether to end.
- If the user confirms workflow end, merge and worktree cleanup happen from the repo control-plane only.
- Merge and worktree cleanup are forbidden until the user confirms workflow end.

## Docs Integration Contract

- Stage `3.1` must explicitly use `$docs-governor`.
- Stage `4` must explicitly use `$docs-governor`.
- Requirement/spec impact must be recorded in planning and archive artifacts.
- The root-level active `plan.md` is a workflow-control exception and does not replace `docs/plan/` as an archive category.

## Sub-agent Contract

- Sub-agents are allowed only in `3.2` and `3.3`.
- A parallelism assessment is required on entry to `3.2` and `3.3`.
- When host policy permits and the split is safe, sub-agents should be created for qualifying parallel work.
- Delegation requires a confirmed plan and a complete context package.
- Worktree creation, plan confirmation, requirements decisions, architecture decisions, conflict handling, integration, and final acceptance remain with the main agent.
- Host platform policy still applies; if the platform requires explicit user authorization for sub-agents, the skill must honor it.

## Validation Contract

- The skill must pass `tools/validate-skills.ps1 -Skill rigorous-execution`.
- The skill must sync through `tools/sync-skills.ps1 -Skill rigorous-execution`.
- Validation must happen after the final skill content is written.

## Safety and Stability

- Do not implement in the main repo path.
- Do not proceed past a blocked stage.
- Do not allow plan-external code changes without returning to `3.1`.
- Do not treat change docs as stable truth for requirements or specs.
- Do not silently choose among uncertain best-practice options.

## Performance Considerations

- Keep `SKILL.md` concise.
- Load references selectively.
- Avoid redundant scans when repository state is already known.

## Extension Points

- Add new references for lighter or heavier workflow variants without rewriting the main skill.
- Add future platform wrappers without changing the core references model.

## Related Requirements

- [../requirements/rigorous-execution-skill.md](../requirements/rigorous-execution-skill.md)

## Related Changes

- [../change/2026-03-23_rigorous-execution-skill.md](../change/2026-03-23_rigorous-execution-skill.md)
- [../change/2026-03-23_rigorous-execution-alignment.md](../change/2026-03-23_rigorous-execution-alignment.md)
- [../change/2026-03-23_rigorous-execution-doc-priority.md](../change/2026-03-23_rigorous-execution-doc-priority.md)
