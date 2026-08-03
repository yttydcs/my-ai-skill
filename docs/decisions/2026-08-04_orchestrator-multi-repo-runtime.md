# 2026-08-04 Multi-repository Project Runtime for m-orchestrator

## Status

Proposed.

## Context

The `m-*` workflow defines a project root as an umbrella directory, a docs root as an independent governed location, and code repositories as one or more participating Git repositories. Multi-repository workflows give every participating repository its own branch, worktree, and root plan.

The first `m-orchestrator` implementation instead derives project identity and runtime state from `git rev-parse --git-common-dir` executed at the umbrella root, stores one project-level base branch, and records one plan per Task. This works for a project whose root is one Git repository but blocks valid umbrella projects such as `D:\project\monkeys`.

## Options Considered

### Initialize Git at the umbrella root

Rejected. It changes project topology, can accidentally encompass child repositories and runtime data, and contradicts the existing workflow model.

### Use one child repository as the project identity anchor

Rejected. The anchor would be arbitrary, tasks may not touch it, and its relocation or deletion would incorrectly change project identity.

### Discover every nested Git repository automatically

Rejected as the persisted source of truth. Dependency trees, caches, tooling, and nested repositories make recursive discovery ambiguous and potentially expensive. A future read-only suggestion helper may be considered separately.

### Use an explicit repository catalog and project-local runtime

Proposed. It represents the real topology, keeps project-level scheduling independent of one repository, and supports deterministic task-scoped worktree sets.

## Decision

Add orchestrator configuration schema version 2.

Schema version 2 keeps `project_id` and `docs_root` at project scope and adds an explicit non-empty `[[repositories]]` catalog. Each repository declares a stable ID, a path relative to `project_root`, and its own base branch. Declared paths must be traversal-free, unique after canonical resolution, contained by the umbrella root, and valid Git repositories. The umbrella root itself is not Git-validated.

Schema version 2 project runtime resolves under:

```text
<project_root>/.codex-runtime/m-orchestrator/projects/<project_id>
```

Runtime metadata binds the state to the canonical project root, schema version, project ID, and configuration fingerprint. Optional machine-wide capacity remains in the existing global host-budget root and contains no project knowledge.

Each approved Task persists a validated dispatch manifest selecting a non-empty subset of configured repository IDs. The manifest includes each repository's base/planning ref, semantic branch, dedicated worktree, plan evidence, write set, acceptance/test/rollback data, and Planner callback metadata. A deterministic Task change identifier is computed from a sorted per-repository snapshot so a change in any participating repository invalidates the lightweight gate.

The Planner prepares or confirms every participating repository worktree before Worker dispatch. One temporary Worker receives the complete worktree map and invokes `$m-execute` within that approved set. A temporary Tester receives the same set and invokes `$m-test` only after the aggregate lightweight gate passes. `$m-archive` remains authoritative for per-repository archive, commit, control-plane merge, docs handling, and cleanup.

Cross-repository integration is not presented as atomic. Archive admission performs complete preflight, follows an explicit repository/dependency order, stops on failure, and reports completed and pending repositories for manual or planned recovery.

Schema version 1 remains supported as a single-repository compatibility adapter when `project_root` is a valid Git repository. It keeps its existing Git-common-dir runtime path so active state is not moved implicitly. A schema version 1 non-Git umbrella receives an actionable schema v2 migration error, not a suggestion to run `git init`.

## Consequences

- Project runtime identity no longer depends on an arbitrary child repository under schema v2.
- Configuration and Task records become explicit about repository participation and per-repository base/worktree/ref state.
- Existing single-repository users retain their current configuration and runtime state.
- Automatic migration of active runtime state is intentionally avoided.
- Host Worker creation must treat a multi-repository worktree set as prepared project state rather than assume one host-created Git worktree represents the whole Task.
- Status and validation remain proportional to the configured project and selected Task repositories; ordinary operations do not recursively scan the umbrella tree.
- Focused regression tests are required for Windows canonical paths, umbrella roots, child Git repositories, compatibility, evidence invalidation, and partial integration reporting.

## Confidence

High. The model matches existing `m-autoflow` contracts and the observed project topology. The exact Codex host project used to create a multi-repository Worker may vary by installation, so the dispatch contract must validate available host tools and include absolute worktree paths rather than depend on an implicit current repository.

## Supersedes / Superseded By

- Supersedes: the Git-common-directory project identity and single project-level base-branch portions of [2026-07-31_project-orchestrator.md](2026-07-31_project-orchestrator.md), after this decision is accepted and implemented.
- Superseded by: none.

## Related Intake

- [2026-08-04_orchestrator-multi-repo.md](../intake/2026-08-04_orchestrator-multi-repo.md)
- [2026-07-31_project-orchestrator.md](../intake/2026-07-31_project-orchestrator.md)

## Related Feature

- [m-project-orchestrator.md](../features/m-project-orchestrator.md)

## Related Requirements

- [m-project-orchestrator.md](../requirements/m-project-orchestrator.md)

## Related Specs

- [m-project-orchestrator.md](../specs/m-project-orchestrator.md)
- [m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related Plan

- [Active multi-repository plan](../../plan.md)
