---
name: m-plan
description: Architecture and execution-planning phase for the m-autoflow workflow. Use when Codex needs to consume a $m-discuss brief or clear requirements, reject unreasonable requirements, design the technical approach, create or confirm root plan.md/todo.md, define Task IDs, acceptance, tests, rollback, and stop before implementation for user approval.
---

# m:plan

## Overview

Use this skill to convert a coherent requirement into an executable architecture and implementation plan. It deliberately stops before runtime behavior or business logic changes.

## Quick Start

- Read `references/planning.md`.
- If invoking as part of the full workflow, keep `$m-autoflow` as the umbrella context and use this skill after `$m-discuss`.
- Do not perform broad discovery here. If the requirement is unclear, unreasonable, or needs current external research, return to `$m-discuss`.
- When private docs are expected, identify `project_root`, `docs_root`, `code_repos`, and `active_worktree` before planning writes stable docs.
- Read the original canonical references only when needed:
  - `../m-autoflow/references/initialization.md` for worktree, branch, repo, and `guide.md` prerequisites.
  - `../m-autoflow/references/m-docs-integration.md` before editing `plan.md`, intake, features, requirements, specs, decisions, change, or lessons docs.
  - `../m-autoflow/references/templates.md` when creating the active `plan.md` or `todo.md`.

## Workflow

1. Confirm the task needs staged execution and identify the project root, private docs root, real owning repo or repos, base branch, modules, and working path.
2. Read `guide.md` when present and apply project-local workflow rules before generic defaults.
3. Consume the `$m-discuss` brief when present; if missing, record that discussion was skipped or not needed.
4. Ensure implementation will happen only in a dedicated branch and worktree; if missing, create or request it before planning proceeds.
5. Run requirements analysis:
   - prefer relevant `docs/intake` and `docs/features` docs when the work changes user-visible behavior
   - prefer relevant `docs/requirements` docs when they exist
   - record goal, scope, use cases, functional and non-functional requirements, inputs/outputs, edge cases, acceptance criteria, and risks
6. Run architecture analysis:
   - prefer relevant `docs/specs` docs when they exist
   - prefer relevant `docs/decisions` docs when architecture choices constrain the work
   - record solution, alternatives, module responsibilities, data/call flow, interfaces, errors, safety, performance, tests, and extension points
7. Explicitly use `$m-docs` before confirming the plan.
8. Create or confirm root `plan.md` or `todo.md` in the active worktree. Include docs root, code repos, task IDs, file/module scope, acceptance, tests, rollback points, dependencies, risks, and parallelism notes.
9. Explicitly separate tasks that will be executed after approval from tasks that will not be executed in the next execution phase. Every known task must appear in exactly one section, with the reason for any deferred, blocked, out-of-scope, or research-only task.

## Private Docs Guardrails

- Do not write governed docs into a pushable code repo when the user expects private docs.
- Do not add docs remotes, push docs, publish docs, or choose backup targets.
- If a docs root is required but unclear, stop before implementation and ask or record a blocker.
- If the requirement is unreasonable, unsafe, contradictory, or under-specified, block planning and route back to `$m-discuss` with alternatives.

## Exit Gate

Before implementation, output a clear plan status:

```md
Execution scope after approval:
- Will execute: <Task IDs>
- Will not execute now: <Task IDs and reasons>

Blocked: yes
Do not enter execution
Do not dispatch implementation sub-agents
```

After the user confirms the plan:

```md
Execution scope after approval:
- Will execute: <Task IDs>
- Will not execute now: <Task IDs and reasons>

Blocked: no
Enter execution
```

Do not edit business logic, runtime behavior, or tests before the plan is confirmed.
