# 2026-08-04 m-orchestrator Multi-repository Support

## Source

- Date: 2026-08-04
- Source: Codex chat
- Requester: User

## Original Request Summary

The user expects the new project automation layer to assist the existing `m-*` skills, including their established multi-repository behavior. A project is an umbrella directory and may contain a `repo` directory with multiple independent Git repositories. The umbrella directory itself is not necessarily a Git repository.

The immediate failure occurred while validating `D:\project\monkeys`: all four configured role contexts and the TOML syntax/fields passed, but Planner registration was blocked because the orchestrator tried to resolve Git metadata from the umbrella root. The resulting message suggested supplying one Git repository root or running `git init` in the umbrella directory.

The user rejected that interpretation because the project is intentionally multi-repository and the existing `m-*` skills already describe this topology.

## Confirmed Constraints

- Do not initialize Git in the umbrella project directory merely to satisfy orchestration.
- Treat `project_root`, `docs_root`, and implementation repositories as separate concepts.
- Validate Git only for the repositories that participate in implementation.
- Preserve one project-scoped Planner, temporary Workers, bounded temporary Tester Pools, and serialized archive admission.
- Workers use `$m-execute` and must complete cheap syntax/type/lint/format/focused-unit/diff checks before Tester admission.
- Existing phase skills remain authoritative; the automation layer only configures, dispatches, coordinates, and records their work.
- Different projects on one machine remain isolated.
- Project role contexts such as `planner.md`, `worker.md`, `tester.md`, and `archive.md` remain project-local configuration inputs loaded through `$m-context`.

## Observed Project Shape

- Umbrella: `D:\project\monkeys`
- Repository container: `D:\project\monkeys\repo`
- Multiple valid child Git repositories exist under that container.
- The umbrella root is not a valid Git repository; an empty `.git` directory does not define the project topology and must not trigger a recommendation to initialize it.

The real project is evidence for the design and later adoption. It is not in the write set of the current `my-ai-skills` workflow.

## Root Cause Summary

The wider `m-*` workflow already defines:

- `project_root` as the umbrella directory;
- `docs_root` as the governed docs location;
- `code_repos` as one or more Git implementation repositories;
- one dedicated branch, worktree, and root plan per participating repository.

`m-orchestrator` schema version 1 conflicts with that model by requiring one project-level `base_branch`, resolving one `git_common_dir` from `project_root`, and deriving project runtime state from that Git directory.

## Requested Outcome

- A non-Git umbrella root with multiple declared child repositories validates normally.
- Planner registration and project scheduling do not depend on any one child repository.
- Each Task records the exact repositories and worktrees it owns.
- Lightweight and heavy validation cover the complete participating repository set.
- Single-repository orchestrator projects remain backward compatible.
- Errors identify invalid declared repositories and never recommend changing a valid multi-repository topology.

## Stable Docs Impact

- Feature impact: update current orchestrator behavior and project isolation.
- Requirements impact: replace Git-common-dir project identity with umbrella/repository requirements.
- Specs impact: add schema v2, runtime identity, Task manifest, multi-repository evidence, and compatibility contracts.
- Decision impact: add a superseding project-runtime and repository-model decision.
- Lessons impact: reassess after implementation and migration validation.

## Routed Docs

- [Archived plan](../plan/2026-08-04_orchestrator-multi-repo.md)
- [Completed change](../change/2026-08-04_orchestrator-multi-repo.md)
- [Accepted decision](../decisions/2026-08-04_orchestrator-multi-repo-runtime.md)
- [Reusable runtime-boundary lesson](../lessons/orchestrator-multi-repository-runtime-boundaries.md)
- [Project orchestrator feature](../features/m-project-orchestrator.md)
- [Project orchestrator requirements](../requirements/m-project-orchestrator.md)
- [Project orchestrator specification](../specs/m-project-orchestrator.md)
- [Original orchestrator intake](2026-07-31_project-orchestrator.md)
