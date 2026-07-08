# 2026-07-08 M Skill Phase Rename

## Source

- Requester: user
- Source: Codex chat
- Date: 2026-07-08

## Request Text / Source-preserving Summary

- Rename phase skills such as `m-autoflow-plan` to shorter names such as `m-plan`; apply the same idea to `m-autoflow-execute` and the related phase skills.
- Keep `m-autoflow` as the collection / umbrella for the smaller skills so the user does not need to type each phase command individually.
- Make the umbrella use references internally and avoid writing the same content repeatedly.
- Add a `discuss` phase.
- `discuss` should search the web when needed, look up current best practices, explore feasible options, support requirement refinement, and brainstorm thoroughly.
- `discuss` should behave like a senior product manager with strong technical understanding.
- `plan` should behave like a senior architect / experienced programmer and produce the execution plan.
- If a requirement is unreasonable, the workflow should reject it and provide better suggestions.
- Worktree creation should theoretically start during `discuss`.

## Context

- Existing phase skills are named:
  - `m-autoflow-plan`
  - `m-autoflow-execute`
  - `m-autoflow-test`
  - `m-autoflow-archive`
  - `m-autoflow-research`
- Existing umbrella skill is `m-autoflow`.
- Prior docs governance work added private docs root, intake, features, decisions, and explicit stable-doc impact rules.

## Confirmed Requirements

- Add `m-discuss` as a first-class phase.
- Rename canonical phase skills to shorter `m-*` names.
- Keep `m-autoflow` as umbrella/collection.
- Avoid duplicated workflow instructions by using shared references.
- Let `discuss` own discovery, brainstorming, optional research, and early worktree setup.
- Let `plan` own architecture and executable planning.
- Require rejection or rerouting when requirements are unreasonable.

## Open Questions

- Whether to keep old `m-autoflow-*` phase names as temporary compatibility aliases.
- Whether `m-autoflow` should continue to host shared references, or whether a future separate core/reference package is worth creating.

## Routed Docs

- Related feature:
  - [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)
- Related requirements:
  - [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)
- Related specs:
  - [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)
- Related decisions:
  - [../decisions/2026-07-08_m-skill-phase-naming.md](../decisions/2026-07-08_m-skill-phase-naming.md)
- Related plan:
  - [../../plan.md](../../plan.md)

## Related Changes

- Later archive:
  - planned [../change/2026-07-08_m-skill-phase-rename.md](../change/2026-07-08_m-skill-phase-rename.md)
