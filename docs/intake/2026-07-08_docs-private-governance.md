# 2026-07-08 Docs Private Governance

## Source

- Requester: user
- Source: Codex chat
- Date: 2026-07-08

## Request Text / Source-preserving Summary

- Current `specs` felt too scattered; for a feature such as personnel management, one feature document should fully describe CRUD behavior, how it works, button placement, layout, and future requirement changes.
- Original requirements should remain traceable instead of being collapsed into `change` records.
- A project may contain a `repo/` folder with multiple Git repositories, so docs governance must handle both single-repo and multi-repo capabilities.
- Governed docs should not live inside individual code repositories by default because the user does not want private work product pushed to code remotes.
- Docs may be managed in a separate Git repository, but the user decides remote targets, push policy, and backup strategy.
- The user asked to update `$m-autoflow-plan` and then continue through execution and archive.

## Context

- The affected repository is the skill repository at `D:\project\my-ai-skills`.
- The workflow used a dedicated worktree at `D:\project\my-ai-skills\worktrees\docs-private-governance`.
- Online research informed the planning stage, but the private-docs publication boundary is a user-owned project rule rather than a borrowed external convention.

## Confirmed Requirements

- Add first-class `docs_root`, `project_root`, `code_repos`, and `active_worktree` concepts.
- Add `intake` for original request evidence.
- Add `features` for complete user-visible feature dossiers.
- Add `decisions` for append-only architecture decision records.
- Keep `requirements` and `specs` as durable intent and technical contract layers.
- Keep `plan`, `change`, and `lessons` as workflow, archive, and reusable learning layers.
- Do not infer docs remotes, push targets, publication, or backup destinations.

## Open Questions

- The user has not selected a docs remote, push target, or backup destination.
- Applying the new docs model to an external project remains a future workflow that needs a named target project and docs root.

## Routed Docs

- Related requirements:
  - [../requirements/m-docs-skill.md](../requirements/m-docs-skill.md)
  - [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)
- Related specs:
  - [../specs/m-docs-skill.md](../specs/m-docs-skill.md)
  - [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)
- Related decision:
  - [../decisions/2026-07-08_private-docs-root-and-feature-first-governance.md](../decisions/2026-07-08_private-docs-root-and-feature-first-governance.md)
- Related plan:
  - [../../plan.md](../../plan.md)

## Related Changes

- [../change/2026-07-08_docs-private-governance.md](../change/2026-07-08_docs-private-governance.md)
