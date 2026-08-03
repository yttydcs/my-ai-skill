# Configuration Contract

## Project File

Store machine-readable project orchestration policy at:

```text
<project-root>/.codex/m-orchestrator.toml
```

The file is project configuration, not runtime state. Do not store credentials or mutable queue data in it.

## Required Identity

- `schema_version` may be `1` for a compatible single-repository project or `2` for an umbrella project.
- `project_id` must be a stable lowercase identifier containing only letters, digits, `.`, `_`, and `-`.
- `docs_root` may be absolute or relative to the selected project root. Relative paths must not contain traversal segments.
- `environment.namespace` must be a non-empty project-specific namespace.

Schema version 1 treats `project_root` as the one Git repository and requires one project-level `base_branch`. It keeps runtime state under that repository's Git common directory. If a schema version 1 project root is not Git, fail with an actionable schema version 2 migration message; never recommend initializing an umbrella root.

Schema version 2 treats `project_root` as an umbrella directory and requires a non-empty explicit repository catalog:

```toml
[[repositories]]
id = "service-api"
path = "repo/service-api"
base_branch = "main"
```

- Repository IDs must be unique safe identifiers.
- Repository paths must be relative, traversal-free, contained by `project_root`, unique after canonical resolution, and point to exact Git worktree roots.
- Each repository has its own non-empty base branch, which must resolve to a commit.
- The umbrella root is not Git-validated. An empty or invalid umbrella `.git` directory is irrelevant.
- Ordinary validation and status use only declared repositories; they do not recursively discover repositories.

Schema version 2 runtime state lives under `<project-root>/.codex-runtime/m-orchestrator/projects/<project_id>`. Canonical project root plus `project_id` isolate different projects, while distinct IDs isolate multiple logical projects under one umbrella.

## Command Mapping

The first version requires these exact authorities:

| Command | Required skill | Purpose |
| --- | --- | --- |
| `discuss` | `m-discuss` | discovery and requirement shaping |
| `plan` | `m-plan` | architecture and executable planning |
| `execute` | `m-execute` | implementation and lightweight validation |
| `test` | `m-test` | heavyweight validation and review |
| `archive` | `m-archive` | archive, integration, and cleanup |

Each `contexts` entry must use explicit `local:<name>` syntax. An empty list is allowed when a project has no context for that command. Unqualified and `global:` entries are rejected so a missing project environment cannot silently select unrelated global data. These rules are identical in both schema versions.

`commands.execute.require_lightweight_gate` must be `true`. `commands.test.pool` must identify a configured Tester pool. `commands.archive.pool` must identify a configured capacity-one integration pool.

## Pool Configuration

- `capacity`: integer from 1 through 64.
- `queue`: exactly `fifo` in both supported schema versions.
- `lease_timeout_seconds`: integer from 60 through 86400.
- The archive/integration pool capacity must be `1`.

An optional `[host_budget]` table may provide a numeric machine-wide ceiling:

```toml
[host_budget]
enabled = true
host_id = "local"
resource = "testers"
capacity = 3
lease_timeout_seconds = 3600
```

Every project sharing the same host/resource pair must declare the same capacity and timeout. A mismatch fails explicitly. Host runtime metadata contains only numeric capacity, opaque owner/lease IDs, and timestamps.

## Context Files

Project role knowledge belongs under the existing local `$m-context` root:

```text
<docs-root>/context/planner.md
<docs-root>/context/worker.md
<docs-root>/context/tester.md
<docs-root>/context/archive.md
```

Context files may describe commands, environments, cleanup, constraints, known failures, or authorized plaintext secrets. Load them through `$m-context`; do not parse their prose as scheduler configuration and do not copy their bodies into runtime JSON.

## Global Runtime Root

Resolve optional host-budget state in this order:

1. `M_ORCHESTRATOR_HOME`
2. `<CODEX_HOME>/m-orchestrator`
3. `~/.codex/m-orchestrator`

Project runtime state never moves into this global root. Schema version 1 uses the repository Git common directory; schema version 2 uses the project-local runtime path above.

## Task Manifest

Schema version 2 Task creation requires `task create --manifest <absolute-json-path>`. The manifest schema version is `1` and contains:

- Task ID, title, canonical plan path, acceptance checks, test points, rollback, and Planner callback identity;
- a non-empty ordered `repositories` array selecting only configured repository IDs;
- for each repository: absolute dedicated worktree, semantic branch, configured base ref, exact planning ref, worktree-root `plan.md` or `todo.md`, and relative write set.

Every selected worktree must live under `<project-root>/worktrees`, resolve to the configured repository's Git common directory, be on the declared branch, and have `HEAD` at the planning ref when the Task is created. The manifest file, plans, and normalized routing metadata may be hashed or referenced in runtime state; context bodies, diffs, test output, and credentials may not be copied there.

Schema version 1 retains `task create --task-id <id> --plan <path>` for compatibility and may also use the manifest interface.

## Validation

Run configuration validation before Planner registration, Task creation, or pool mutation. Missing files, malformed TOML, unsupported keys that affect correctness, invalid declared repositories, missing pools, wrong skill mappings, unsafe contexts, or inconsistent host budgets are blocking errors. Do not create or migrate runtime state until configuration validation succeeds. Changing schema versions never silently relocates active Tasks or leases.
