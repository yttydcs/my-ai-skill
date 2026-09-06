# Intake

## Purpose

Store original request evidence before it is refined into feature, requirement, spec, decision, plan, or change documents.

## How to Enter This Section

- Start here when traceability to the user's original request matters.
- Use this section for raw request text, source-preserving summaries, request date, source, requester, and open questions.
- Link intake records to the feature, requirement, spec, decision, plan, or change docs that interpret them.

## What Belongs Here

- original user requests or source-preserving excerpts
- request context and known constraints
- unresolved questions at intake time
- links to routed stable docs and workflow archives

## Naming / Maintenance Rules

- Prefer `YYYY-MM-DD_topic.md` when the intake record comes from a dated request.
- Do not rewrite intake records into current truth; update the linked feature, requirement, spec, or decision instead.
- Keep sensitive content in the private docs root selected by the user.

## Current Docs

- [2026-09-06_acceptance-review.md](2026-09-06_acceptance-review.md) - source: Codex chat, approved acceptance traceability, behavior slices and lightweight candidate review
- [2026-09-06_role-pipeline.md](2026-09-06_role-pipeline.md) - source: Codex chat, manually configured role/session pipelines composed with the existing m-* workflow
- [2026-08-15_orchestrator-archive-queue-resume.md](2026-08-15_orchestrator-archive-queue-resume.md) - source: Codex chat, project-scoped archive FIFO waiting, automatic continuation, drift revalidation, and Windows/Linux portability
- [2026-08-04_orchestrator-multi-repo.md](2026-08-04_orchestrator-multi-repo.md) - source: Codex chat, correct `m-orchestrator` for non-Git umbrella projects with multiple child repositories
- [2026-07-31_project-orchestrator.md](2026-07-31_project-orchestrator.md) - source: Codex chat, persistent per-project Planner with temporary Workers and bounded Tester Pools
- [2026-07-20_m-discuss-grill-mode.md](2026-07-20_m-discuss-grill-mode.md) - source: Codex chat, explicitly triggered Grill Mode inside `$m-discuss`
- [2026-07-17_m-continue-loop.md](2026-07-17_m-continue-loop.md) - source: Codex chat, resume an existing execute/test workflow through a reusable convergence loop
- [2026-07-15_m-context-scopes.md](2026-07-15_m-context-scopes.md) - source: Codex chat, project-local and user-global context scopes with absence-only fallback
- [2026-07-15_visual-output-components.md](2026-07-15_visual-output-components.md) - source: Codex chat, improve skill output with useful visual components and clickable evidence
- [2026-07-13_m-context.md](2026-07-13_m-context.md) - source: Codex chat, reusable plaintext Agent context loading and skill composition
- [2026-07-10_m-quick-fast-path.md](2026-07-10_m-quick-fast-path.md) - source: Codex chat, guarded direct-edit fast path with mandatory docs context
- [2026-07-09_m-go-automated-execution.md](2026-07-09_m-go-automated-execution.md) - source: Codex chat, delegated automated execution and test-loop command
- [2026-07-09_docs-structure-sync.md](2026-07-09_docs-structure-sync.md) - source: Codex chat, docs tree synchronization request
- [2026-07-08_m-plan-task-table.md](2026-07-08_m-plan-task-table.md) - source: Codex chat, direct task summary table after planning
- [2026-07-08_m-test-ui-evidence.md](2026-07-08_m-test-ui-evidence.md) - source: Codex chat, UI test evidence and direct result table requirements
- [2026-07-08_m-archive-default-closeout.md](2026-07-08_m-archive-default-closeout.md) - source: Codex chat, archive command should imply workflow closeout
- [2026-07-08_m-skill-phase-rename.md](2026-07-08_m-skill-phase-rename.md) - source: Codex chat, phase skill rename/discuss workflow requirements
- [2026-07-08_docs-private-governance.md](2026-07-08_docs-private-governance.md) - source: Codex chat, docs governance/privacy/multi-repo requirements
