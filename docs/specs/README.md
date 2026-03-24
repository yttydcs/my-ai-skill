# Specs

## Purpose

Store technical contracts, integration rules, architecture constraints, and workflow-control exceptions for this skill repository.

## How to Enter This Section

- Start here after requirements when a capability needs durable technical rules.
- Use this section when the question is how the capability is structured technically, what contracts it obeys, or what implementation guardrails must remain true.
- Update specs whenever behavior-changing work alters packaging, invocation, or integration contracts.

## What Belongs Here

- skill package structure
- trigger and invocation contracts
- docs-governor integration rules
- validation and installation behavior
- sub-agent governance contracts

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

## Naming / Maintenance Rules

- Use stable names without dates.
- Keep technical contracts here instead of burying them in change logs.
- Link each spec to the requirement it supports and the change archives that implemented it.

## Current Docs

- [docs-governor-skill.md](docs-governor-skill.md)
- [rigorous-execution-skill.md](rigorous-execution-skill.md)
