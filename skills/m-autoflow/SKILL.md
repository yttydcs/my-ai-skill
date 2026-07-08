---
name: m-autoflow
description: Umbrella collection for the m-* staged engineering workflow. Use when the user wants the whole disciplined flow without invoking each phase manually, routing to $m-discuss for discovery, $m-plan for architecture, $m-execute for implementation, $m-test for heavy validation, and $m-archive for docs/change and closeout.
---

# m:autoflow

## Overview

Use this skill as the umbrella entry for the staged `m-*` workflow. It routes the user through the phase skills and shared references without duplicating each phase's full instructions.

## Quick Start

- Invoke `$m-autoflow` when the user wants the full workflow.
- Route to phase skills:
  - `$m-discuss` for discovery, brainstorming, optional current research, and early worktree setup.
  - `$m-plan` for architecture, rejection of bad requirements, and executable `plan.md` / `todo.md` gating.
  - `$m-execute` for approved Task ID implementation and lightweight validation.
  - `$m-test` for optional heavy validation, integration testing, usability review, security review, and performance review.
  - `$m-archive` for `docs/change`, lessons, workflow-end confirmation, merge, and cleanup.
- If governed docs exist, prioritize `docs/intake`, `docs/features`, `docs/requirements`, `docs/specs`, and `docs/decisions` before relying on code-only inference.
- Read `references/initialization.md` before worktree setup.
- Read `references/stages.md` for phase order, handoffs, and blocker rules.
- Read `references/m-docs-integration.md` before editing `plan.md`, intake, features, requirements, specs, decisions, `docs/change`, or `docs/lessons`.
- Read `references/subagents.md` before any parallelism assessment or delegation.
- Read `references/templates.md` when creating `plan.md`, `docs/change`, or `docs/lessons` artifacts.

## Workflow

1. Start with `$m-discuss` unless the user explicitly enters a later phase with a valid artifact.
2. Use `$m-plan` only after the requirement is coherent enough for architecture planning.
3. Use `$m-execute` only after the plan is confirmed and the user approved implementation.
4. Use `$m-test` when heavy validation is needed, or record a justified skip.
5. Use `$m-archive` after validation to write governed archives and ask whether to end the workflow.
6. Merge and clean worktrees only after explicit workflow-end confirmation.

## Split Phase Mapping

- Discuss: use `$m-discuss` for discovery, optional research, and early workflow setup.
- Plan: use `$m-plan` for architecture and executable planning.
- Execute: use `$m-execute` for implementation and lightweight validation.
- Test: use `$m-test` for optional heavy validation and review.
- Archive: use `$m-archive` for archive and workflow-end closeout.

The phase skills are companion entry points. Keep `$m-autoflow` as the whole-workflow command.

## Guardrails

- Only one stage may be active at a time.
- Do not skip, merge, or reorder stages.
- Do not assume missing business rules, data contracts, interfaces, environment details, dependency versions, acceptance criteria, or user preferences.
- Do not write code without a dedicated worktree and confirmed `plan.md`.
- Do not treat rollback as a silent action; state the reason and update the affected docs.
- Do not dispatch sub-agents without a complete context package and an allowed phase.
- Do not treat `docs/change` as the stable source of truth for intake, features, requirements, specs, or decisions.
- Do not leave reusable lessons only in `docs/change`; promote them into `docs/lessons` when they should be queried later.
- Do not write governed private docs into a pushable code repo unless the user selected that repo as the docs root.
- Do not add docs remotes, push docs, publish docs, or choose backup targets unless the user explicitly asks.
- Do not merge or clean the worktree until the user explicitly confirms workflow end.

## References

- `references/initialization.md`
  - worktree, branch, repo, and `guide.md` prerequisites
- `references/stages.md`
  - required outputs, blockers, and transitions for discuss, plan, execute, test, and archive
- `references/m-docs-integration.md`
  - mandatory `$m-docs` usage and docs impact recording rules
- `references/subagents.md`
  - parallelism assessment, delegation gates, and audit requirements
- `references/templates.md`
  - compact templates for `plan.md`, blocker output, `docs/change`, and `docs/lessons`
- `../m-discuss/SKILL.md`
  - discussion and optional research entry point
- `../m-plan/SKILL.md`
  - planning entry point
- `../m-execute/SKILL.md`
  - execution entry point
- `../m-test/SKILL.md`
  - split validation and review entry point
- `../m-archive/SKILL.md`
  - archive and closeout entry point
