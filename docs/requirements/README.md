# Requirements

## Purpose

Store long-lived capability intent, boundaries, scenarios, and acceptance criteria for this skill repository.

## How to Enter This Section

- Start here when a workflow introduces or changes a persistent capability.
- Use this section when the question is why the capability exists, what it must do, what is in scope, or how success is accepted.
- Update this section before or alongside `docs/change/` when the underlying requirement changes.

## What Belongs Here

- why a skill exists
- who or what it serves
- core actors and scenarios
- required behavior and boundaries
- acceptance criteria that should outlive one workflow

## Boundary With Specs

- `requirements` answer `why / what`:
  - why the capability exists
  - what behavior is required
  - what is in scope or out of scope
  - how the result is accepted
- `specs` answer `how / contract`:
  - package structure
  - technical constraints
  - interface and routing rules
  - validation or bootstrap contracts
- If a change affects both, update `requirements` first, then update `specs`.

## Naming / Maintenance Rules

- Use stable names without dates.
- Keep acceptance criteria here, not only in change logs.
- Link each requirement doc to its related spec and major change records.

## Current Docs

- [m-docs-skill.md](m-docs-skill.md)
- [m-autoflow-skill.md](m-autoflow-skill.md)
- [m-thesis-aigc-revision-skill.md](m-thesis-aigc-revision-skill.md)
