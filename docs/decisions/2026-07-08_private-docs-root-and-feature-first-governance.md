# 2026-07-08 Private Docs Root and Feature-first Governance

## Status

Accepted

## Context

The user wants documentation to preserve original requests, keep feature behavior complete, support multi-repo projects, and avoid placing private work product inside pushable code repositories. Existing docs categories were too focused on requirements, specs, changes, and lessons, which made feature-level behavior and source evidence easy to scatter.

## Options Considered

- Keep docs inside each code repository.
- Put all durable content into `requirements` and `specs`.
- Put original requests and final truth into `change`.
- Mandate a separate docs Git repository for every project.
- Support a selected private `docs_root`, add `intake`, `features`, and `decisions`, and keep publication user-owned.

## Decision

Use a selected `docs_root` as the governed documentation root, which may be outside code repositories or may be a separate local/private Git repository. Treat code repositories as implementation carriers unless the user explicitly selects one as the docs root.

Add these first-class categories:

- `intake` for original request evidence
- `features` for current user-visible feature truth
- `decisions` for append-only architecture decision records

Keep these existing categories with clarified boundaries:

- `requirements` for durable capability intent and non-feature constraints
- `specs` for technical contracts and architecture guardrails
- `plan`, `change`, and `lessons` for workflow control, result archives, and reusable learning

Remote configuration, push targets, publication, and backup strategy remain user-owned decisions.

## Consequences

- A cross-repo capability can be documented once in private `docs/features` and link to participating repos.
- Original user requests can be preserved without turning `change` into the intake source.
- Feature CRUD, UI placement, states, permissions, and acceptance can live together in one current-truth dossier.
- Planning and archive workflows must record intake, feature, requirement, spec, decision, and lessons impact.
- Workflow code must avoid assuming that repo-local `docs/` is canonical when the user expects private docs.

## Confidence

High. The decision directly matches the user's stated privacy, traceability, and multi-repo requirements.

## Supersedes / Superseded By

- Supersedes: none
- Superseded by: none

## Related Features

- [../features/README.md](../features/README.md)

## Related Specs

- [../specs/m-docs-skill.md](../specs/m-docs-skill.md)
- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related Changes

- [../change/2026-07-08_docs-private-governance.md](../change/2026-07-08_docs-private-governance.md)
