# m:docs Skill

## Background

This repository needs a reusable documentation-governance skill named `m-docs` that can keep stable truth, workflow archives, and lessons aligned instead of letting knowledge drift across ad hoc files.

## Goal

Provide a reusable skill that routes documentation into the correct category and keeps recurring troubleshooting knowledge directly discoverable.

## Documentation Boundary Goal

The governed docs system must make the category split self-explanatory:

- `requirements` must explain why a capability exists, what it must do, what is in scope, and how it is accepted.
- `specs` must explain how the capability is structured technically and what contracts or guardrails it follows.
- A future editor should be able to decide where new documentation belongs without relying on chat history.

## Scope

### Must

- classify docs work across `requirements`, `specs`, `plan`, `change`, and `lessons`
- determine the canonical destination before writing or moving docs
- require requirement/spec impact checks before editing `plan` or `change`
- maintain the nearest required indexes when docs are created, moved, or renamed
- route troubleshooting and "have we seen this before?" requests to `lessons` first
- require lessons to capture lookup hints such as symptoms, trigger conditions, keywords, and quick checks
- prevent reusable troubleshooting knowledge from being buried only in `change`
- keep the `requirements` versus `specs` boundary explicit enough that the docs system is self-explanatory

### Optional

- bootstrap a governed `docs/` tree for repositories that do not have one yet
- support module buckets under `requirements`, `specs`, and `lessons`

### Out of Scope

- replacing `m-autoflow` as the workflow controller
- storing the only copy of stable requirements or specs inside `lessons`
- inventing repository-specific runtime rules that are not documented in the target repo

## Scenarios

- The user asks where a new or existing doc should live.
- A user needs to decide whether a rule belongs in `requirements` or `specs` without reading prior chat context.
- A workflow needs to record requirements/specs impact before writing `change`.
- The user wants future problem-solving to start from prior lessons instead of scanning old change logs.
- A repository lacks a governed docs tree and needs the standard layout bootstrapped.

## Functional Requirements

- The skill must read entry docs before writing leaf docs when those indexes exist.
- The skill must determine whether stable truth belongs in `requirements` or `specs`.
- The skill must define `requirements` as the home of long-lived intent, scope, scenarios, and acceptance criteria.
- The skill must define `specs` as the home of technical contracts, structures, routing rules, and implementation guardrails.
- The skill must determine whether workflow history belongs in `plan` or `change`.
- The skill must classify recurring operational knowledge into `lessons`.
- The skill must start troubleshooting lookup from `docs/lessons` when relevant.
- The skill must update the nearest README indexes when the docs topology or discoverability cues change.
- The skill must require cross-links among related requirements, specs, changes, and lessons.

## Non-functional Requirements

- Performance:
  - keep the main skill concise and defer details to references
- Readability:
  - keep routing rules explicit enough that future doc edits do not need chat-only context
- Maintainability:
  - keep source-of-truth boundaries clear so archive layers do not become accidental stable truth
- Discoverability:
  - make lessons query-friendly enough that future investigations can start from symptoms and quick checks

## Edge Cases

- A request may touch several categories and require updates in sequence.
- A repository may have partial docs coverage and need bootstrapping or repair first.
- A troubleshooting request may have no matching lesson and need fallback to `change`, `specs`, and `requirements`.
- A generated or protected docs region may exist and must not be edited manually.

## Acceptance Criteria

- `m-docs` exists as a valid reusable skill package in this repository.
- The skill can classify docs work into the governed categories and explain why.
- The stable docs explain the `requirements` versus `specs` split clearly enough that a future editor can route content without chat-only context.
- The skill can record requirement/spec impact for plan and change work.
- The skill can route reusable troubleshooting knowledge into query-friendly lessons.
- The skill can bootstrap the expected docs tree and guidance.

## Related Specs

- [../specs/m-docs-skill.md](../specs/m-docs-skill.md)

## Related Changes

- [../change/2026-03-22_docs-governor-skill.md](../change/2026-03-22_docs-governor-skill.md)
- [../change/2026-03-23_lessons-archive-lookup.md](../change/2026-03-23_lessons-archive-lookup.md)
- [../change/2026-03-24_requirements-specs-responsibility-clarity.md](../change/2026-03-24_requirements-specs-responsibility-clarity.md)
- [../change/2026-03-24_skill-prefix-rename.md](../change/2026-03-24_skill-prefix-rename.md)
