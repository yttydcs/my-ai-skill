# m:docs Skill

## Background

This repository needs a reusable documentation-governance skill named `m-docs` that can keep stable truth, original request evidence, workflow archives, and lessons aligned instead of letting knowledge drift across ad hoc files.

## Goal

Provide a reusable skill that routes documentation into the correct category, supports private docs roots outside pushable code repositories, keeps feature-level truth complete, and keeps recurring troubleshooting knowledge directly discoverable.

## Documentation Boundary Goal

The governed docs system must make source-of-truth boundaries self-explanatory:

- `intake` preserves original request evidence.
- `features` describe current user-visible feature behavior, workflows, UI placement, permissions, and acceptance.
- `requirements` describe durable capability intent, boundaries, and non-feature constraints.
- `specs` describe technical contracts, architecture constraints, and implementation guardrails.
- `decisions` preserve architecturally significant choices.
- `plan`, `change`, and `lessons` remain workflow, archive, and reusable learning layers.
- A future editor should be able to decide where new documentation belongs without relying on chat history.

## Scope

### Must

- classify docs work across `intake`, `features`, `requirements`, `specs`, `decisions`, `plan`, `change`, and `lessons`
- support a private `docs_root` that may be outside any pushable code repository
- preserve original user requests in `intake` instead of treating `change` as the request source
- route user-visible feature behavior to `features`
- determine the canonical destination before writing or moving docs
- require feature/requirement/spec/decision impact checks before editing `plan` or `change`
- maintain the nearest required indexes when docs are created, moved, renamed, or when topology changes
- route troubleshooting and "have we seen this before?" requests to `lessons` first
- require lessons to capture lookup hints such as symptoms, trigger conditions, keywords, and quick checks
- prevent reusable troubleshooting knowledge from being buried only in `change`
- keep category boundaries explicit enough that the docs system is self-explanatory
- treat docs remote configuration, push targets, and backup strategy as user-owned decisions

### Optional

- bootstrap a governed `docs/` tree for repositories or private docs roots that do not have one yet
- support module buckets under `features`, `requirements`, `specs`, and `lessons`

### Out of Scope

- replacing `m-autoflow` as the workflow controller
- storing the only copy of stable feature behavior, requirements, specs, or decisions inside `lessons`
- inventing repository-specific runtime rules that are not documented in the target repo
- deciding where the user's private docs should be pushed or backed up

## Scenarios

- The user asks where a new or existing doc should live.
- The user wants original requests preserved before they are refined into current truth.
- The user wants one feature file to describe a complete capability such as personnel management.
- The user has multiple code repositories but wants private docs kept outside pushable repos.
- A user needs to decide whether a rule belongs in `features`, `requirements`, `specs`, or `decisions` without reading prior chat context.
- A workflow needs to record feature/requirement/spec/decision impact before writing `change`.
- The user wants future problem-solving to start from prior lessons instead of scanning old change logs.
- A repository or private docs root lacks a governed docs tree and needs the standard layout bootstrapped.

## Functional Requirements

- The skill must read entry docs before writing leaf docs when those indexes exist.
- The skill must identify the intended `docs_root` before writing governed docs.
- The skill must not write governed docs into a pushable code repository by default when a private docs root is expected.
- The skill must define `intake` as the home of original request evidence.
- The skill must define `features` as the home of current user-visible feature truth.
- The skill must define `requirements` as the home of durable capability intent, scope, and non-feature acceptance criteria.
- The skill must define `specs` as the home of technical contracts, structures, routing rules, and implementation guardrails.
- The skill must define `decisions` as the home of append-only ADR-style records.
- The skill must determine whether workflow history belongs in `plan` or `change`.
- The skill must classify recurring operational knowledge into `lessons`.
- The skill must start troubleshooting lookup from `docs/lessons` when relevant.
- The skill must update the nearest README indexes when the docs topology or discoverability cues change.
- The skill must require cross-links among related intake, features, requirements, specs, decisions, changes, and lessons.
- The skill must never add remotes, push, or choose backup locations for a docs repository unless the user explicitly requests it.

## Non-functional Requirements

- Performance:
  - keep the main skill concise and defer details to references
- Readability:
  - keep routing rules explicit enough that future doc edits do not need chat-only context
- Maintainability:
  - keep source-of-truth boundaries clear so archive layers do not become accidental stable truth
- Privacy:
  - keep private docs publication and backup under user control
- Discoverability:
  - make lessons query-friendly enough that future investigations can start from symptoms and quick checks

## Edge Cases

- A request may touch several categories and require updates in sequence.
- A feature can span multiple code repositories while its docs live in one private docs root.
- A code repository can contain a `docs/` folder that is not canonical for the project.
- A docs root can have its own Git repository and remote, but publication remains user-owned.
- A repository may have partial docs coverage and need bootstrapping or repair first.
- A troubleshooting request may have no matching lesson and need fallback to `change`, `features`, `specs`, and `requirements`.
- A generated or protected docs region may exist and must not be edited manually.

## Acceptance Criteria

- `m-docs` exists as a valid reusable skill package in this repository.
- The skill can classify docs work into intake, feature, requirement, spec, decision, plan, change, and lesson categories and explain why.
- The stable docs explain private docs roots and category boundaries clearly enough that a future editor can route content without chat-only context.
- The skill can record feature/requirement/spec/decision impact for plan and change work.
- The skill can route reusable troubleshooting knowledge into query-friendly lessons.
- The skill can bootstrap the expected docs tree and guidance.

## Related Specs

- [../specs/m-docs-skill.md](../specs/m-docs-skill.md)

## Related Changes

- [../change/2026-03-22_docs-governor-skill.md](../change/2026-03-22_docs-governor-skill.md)
- [../change/2026-03-23_lessons-archive-lookup.md](../change/2026-03-23_lessons-archive-lookup.md)
- [../change/2026-03-24_requirements-specs-responsibility-clarity.md](../change/2026-03-24_requirements-specs-responsibility-clarity.md)
- [../change/2026-03-24_skill-prefix-rename.md](../change/2026-03-24_skill-prefix-rename.md)
