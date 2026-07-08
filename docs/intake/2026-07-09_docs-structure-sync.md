# 2026-07-09 Docs Structure Sync

## Source

- Requester: user
- Source: Codex chat
- Date: 2026-07-09

## Request Text / Source-preserving Summary

The user invoked `$m-docs` and asked to check and synchronize the current project's `docs` tree to the new documentation structure.

## Context

- Project root: `D:\project\my-ai-skills`
- Docs root: `D:\project\my-ai-skills\docs`
- The docs tree already contained the new top-level categories.
- `docs/plan` had no retained planning documents, while the repository root still contained a completed workflow `plan.md`.
- Some historical intake/change entries linked to `../../plan.md`, which is an active-control-file path and can drift when later workflows replace the root plan.

## Confirmed Requirements

- Keep the governed docs tree aligned with the current `m-docs` category model.
- Preserve root `plan.md` as an active workflow control exception only, not as the long-lived archive location.
- Keep historical workflow traces navigable without pointing historical docs at a volatile root plan path.

## Open Questions

- None for this repository sync.

## Routed Docs

- Related plan archive: [../plan/2026-07-08_m-plan-task-table.md](../plan/2026-07-08_m-plan-task-table.md)
- Related change archive: [../change/2026-07-09_docs-structure-sync.md](../change/2026-07-09_docs-structure-sync.md)
