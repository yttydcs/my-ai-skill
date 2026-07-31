# Configuration Contract

## Project File

Store machine-readable project orchestration policy at:

```text
<project-root>/.codex/m-orchestrator.toml
```

The file is project configuration, not runtime state. Do not store credentials or mutable queue data in it.

## Required Identity

- `schema_version` must be `1`.
- `project_id` must be a stable lowercase identifier containing only letters, digits, `.`, `_`, and `-`.
- `docs_root` may be absolute or relative to the selected project root. Relative paths must not contain traversal segments.
- `base_branch` must be a non-empty branch or ref name supplied by the project.
- `environment.namespace` must be a non-empty project-specific namespace.

The runtime root is derived from the repository common Git directory and `project_id`. Different Git repositories are naturally isolated. Multiple logical projects in one repository remain isolated by distinct IDs.

## Command Mapping

The first version requires these exact authorities:

| Command | Required skill | Purpose |
| --- | --- | --- |
| `discuss` | `m-discuss` | discovery and requirement shaping |
| `plan` | `m-plan` | architecture and executable planning |
| `execute` | `m-execute` | implementation and lightweight validation |
| `test` | `m-test` | heavyweight validation and review |
| `archive` | `m-archive` | archive, integration, and cleanup |

Each `contexts` entry must use explicit `local:<name>` syntax. An empty list is allowed when a project has no context for that command. Unqualified and `global:` entries are rejected so a missing project environment cannot silently select unrelated global data.

`commands.execute.require_lightweight_gate` must be `true`. `commands.test.pool` must identify a configured Tester pool. `commands.archive.pool` must identify a configured capacity-one integration pool.

## Pool Configuration

- `capacity`: integer from 1 through 64.
- `queue`: exactly `fifo` in schema version 1.
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

Project runtime state remains under the Git common directory and never moves into this global root.

## Validation

Run configuration validation before Planner registration, Task creation, or pool mutation. Missing files, malformed TOML, unsupported keys that affect correctness, invalid paths, missing pools, wrong skill mappings, unsafe contexts, or inconsistent host budgets are blocking errors.
