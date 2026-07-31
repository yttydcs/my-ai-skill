# Specs

## Purpose

Store technical contracts, integration rules, architecture constraints, and workflow-control exceptions for this skill repository.

## How to Enter This Section

- Start here after requirements when a capability needs durable technical rules.
- Use this section when the question is how the capability is structured technically, what contracts it obeys, or what implementation guardrails must remain true.
- Update specs whenever behavior-changing work alters packaging, invocation, or integration contracts.
- For user-visible feature behavior, read `../features/` first and use specs only for the technical contracts behind that behavior.

## What Belongs Here

- skill package structure
- trigger and invocation contracts
- m-docs integration rules
- validation and installation behavior
- sub-agent governance contracts
- cross-repo interface contracts
- private docs-root discovery and safety rules

## Boundary With Requirements

- `specs` answer `how / contract`:
  - how the capability is organized
  - what interfaces, routing rules, or stage rules apply
  - what technical constraints and guarantees must hold
  - how validation, sync, or bootstrap behavior works
- `requirements` answer `why / what`:
  - why the capability exists
  - what outcomes it must provide
  - what boundaries and acceptance criteria define success
- Do not move long-lived intent or acceptance criteria into `specs` just because the implementation changed.

## Boundary With Features And Decisions

- `features` describe current product behavior and acceptance from the user's perspective.
- `specs` describe the technical contract that supports or constrains that behavior.
- `decisions` record why a significant option was chosen; they do not replace specs or feature docs.

## Naming / Maintenance Rules

- Use stable names without dates.
- Keep technical contracts here instead of burying them in change logs.
- Link each spec to the requirement it supports and the change archives that implemented it.

## Current Docs

- [m-project-orchestrator.md](m-project-orchestrator.md)
- [m-context-skill.md](m-context-skill.md)
- [m-docs-skill.md](m-docs-skill.md)
- [m-autoflow-skill.md](m-autoflow-skill.md)
- [m-quick-skill.md](m-quick-skill.md)
- [m-thesis-aigc-revision-skill.md](m-thesis-aigc-revision-skill.md)
