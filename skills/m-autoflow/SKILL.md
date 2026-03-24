---
name: m-autoflow
description: Enforce a staged, auditable software execution workflow with worktree-first initialization, requirements analysis, architecture design, root plan.md gating, mandatory code review, docs/change archiving, explicit blocker handling, rollback traceability, and controlled sub-agent delegation. Use this skill for work that must follow strict engineering discipline rather than ad hoc coding.
---

# m:autoflow

## Overview

Use this skill to execute implementation work under strict stage gates, explicit blockers, worktree isolation, and auditable artifacts. Treat speed as secondary to correctness, traceability, and handoff quality.

## Quick Start

- Invoke this skill explicitly as `$m-autoflow` when you want deterministic routing into this workflow.
- If `docs/requirements` or `docs/specs` exists, prioritize them during stages `1` and `2` before falling back to code-only inference.
- Read `references/initialization.md` before stage `1`.
- Read `references/stages.md` to execute stages `1` through `4` and emit the required outputs.
- Read `references/m-docs-integration.md` before editing `plan.md`, `docs/requirements`, `docs/specs`, `docs/change`, or `docs/lessons`.
- Read `references/subagents.md` before any parallelism assessment or delegation in `3.2` or `3.3`.
- Read `references/templates.md` when creating `plan.md`, `docs/change`, or `docs/lessons` artifacts.

## Workflow

1. Start with initialization, not coding:
   - confirm the task actually requires strict staged workflow execution
   - read `guide.md` if it exists
   - confirm repo, base branch, and participating modules
   - require a dedicated branch and worktree under `D:\project\MyFlowHub3\worktrees\`
   - refuse implementation in the main repo path
2. Run stage `1` requirements analysis and prioritize `docs/requirements` when it exists before relying on code or chat context alone.
3. Run stage `2` architecture analysis and prioritize `docs/specs` when it exists before relying on code or chat context alone.
4. In stage `3.1`, explicitly use `$m-docs`, record requirements/specs impact plus any already-known related lessons, and confirm the active worktree-root `plan.md` or `todo.md`.
5. In stage `3.2`, map every implementation change to a confirmed Task ID. Perform a parallelism assessment, but only use sub-agents when both the workflow rules and host platform policy allow it.
6. In stage `3.3`, review against the required checklist and return to `3.2` if any item fails.
7. In stage `4`, explicitly use `$m-docs`, archive the workflow in `docs/change/YYYY-MM-DD_topic.md`, extract reusable experience / lessons plus lookup hints, update `docs/lessons` when needed, and then ask whether the workflow should end.
8. If the user ends the workflow, perform the required merge and worktree cleanup steps. If not, restart from stage `1` for the next iteration.

## Guardrails

- Only one stage may be active at a time.
- Do not skip, merge, or reorder stages.
- Do not assume missing business rules, data contracts, interfaces, environment details, dependency versions, acceptance criteria, or user preferences.
- Do not write code without a dedicated worktree and confirmed `plan.md`.
- Do not treat rollback as a silent action; state the reason and update the affected docs.
- Do not dispatch sub-agents without a complete context package and an allowed phase.
- Do not treat `docs/change` as the stable source of truth for requirements or specs.
- Do not leave reusable lessons only in `docs/change`; promote them into `docs/lessons` when they should be queried later.
- Do not merge or clean the worktree until the user explicitly confirms workflow end.

## References

- `references/initialization.md`
  - worktree, branch, repo, and `guide.md` prerequisites
- `references/stages.md`
  - required outputs, blockers, and transitions for stages `1` through `4`
- `references/m-docs-integration.md`
  - mandatory `$m-docs` usage and docs impact recording rules
- `references/subagents.md`
  - parallelism assessment, delegation gates, and audit requirements
- `references/templates.md`
  - compact templates for `plan.md`, blocker output, `docs/change`, and `docs/lessons`
