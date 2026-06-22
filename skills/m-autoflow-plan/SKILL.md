---
name: m-autoflow-plan
description: Plan phase for the m-autoflow staged engineering workflow. Use when Codex needs to initialize a dedicated worktree, analyze requirements, design architecture, create or confirm root plan.md/todo.md, check docs governance with $m-docs, and stop before implementation for user review. Use for planning-first requests, plan.md creation, or the planning portion of strict staged implementation work. If the user explicitly asks for web research or current external information, invoke $m-autoflow-research as an optional read-only planning aid before finalizing requirements or architecture.
---

# m:autoflow plan

## Overview

Use this skill to run the planning side of `m-autoflow`: initialization, requirements analysis, architecture design, and the gated implementation plan. It deliberately stops before runtime behavior or business logic changes.

## Quick Start

- Read `references/planning.md`.
- If invoking as part of the original full workflow, keep `$m-autoflow` as the umbrella context and use this skill for stages `0` through `3.1`.
- Do not perform web research by default. If the user explicitly asks for online research, current/latest external facts, or source-backed investigation, read `../m-autoflow-research/SKILL.md` and run it before finalizing requirements or architecture.
- Read the original canonical references only when needed:
  - `../m-autoflow/references/initialization.md` for worktree, branch, repo, and `guide.md` prerequisites.
  - `../m-autoflow/references/m-docs-integration.md` before editing `plan.md`, requirements, specs, change, or lessons docs.
  - `../m-autoflow/references/templates.md` when creating the active `plan.md` or `todo.md`.

## Workflow

1. Confirm the task needs staged execution and identify the real owning repo, base branch, modules, and working path.
2. Read `guide.md` when present and apply project-local workflow rules before generic defaults.
3. Ensure implementation will happen only in a dedicated branch and worktree; if missing, create or request it before planning proceeds.
4. If explicit web research was requested, run `$m-autoflow-research` and keep only verified, cited findings.
5. Run requirements analysis:
   - prefer relevant `docs/requirements` docs when they exist
   - record goal, scope, use cases, functional and non-functional requirements, inputs/outputs, edge cases, acceptance criteria, and risks
6. Run architecture analysis:
   - prefer relevant `docs/specs` docs when they exist
   - record solution, alternatives, module responsibilities, data/call flow, interfaces, errors, safety, performance, tests, and extension points
7. Explicitly use `$m-docs` before confirming the plan.
8. Create or confirm root `plan.md` or `todo.md` in the active worktree. Include task IDs, file/module scope, acceptance, tests, rollback points, dependencies, risks, and parallelism notes.

## Exit Gate

Before implementation, output a clear plan status:

```md
Blocked: yes
Do not enter execution
Do not dispatch implementation sub-agents
```

After the user confirms the plan:

```md
Blocked: no
Enter execution
```

Do not edit business logic, runtime behavior, or tests before the plan is confirmed.
