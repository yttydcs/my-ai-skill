# m:context Reusable Agent Context

## Status

Active with project-local and user-global scopes.

## Goal

Let a user save operational knowledge once and load it into later Agent tasks by name, including when composing it with another `m-*` skill.

## Non-goals

- Encrypt context files.
- Act as a production secret manager.
- Synchronize contexts between machines.
- Store contexts inside the `m-context` skill package.
- Automatically publish or commit context files.

## Actors / Permissions

- User: creates, updates, selects, and deletes local contexts.
- Agent: resolves and reads user-selected context files, including plaintext secrets, then uses the content for the requested work.

The context root is a trusted local boundary. Files imported from untrusted sources are not automatically treated as trusted context.

## Entry Points

```text
$m-context nas配置
$m-context local:nas配置
$m-context global:nas配置
$m-context nas配置#测试方式
$m-context list
$m-context find nas
$m-test $m-context nas配置
```

## Context Storage

- Local scope uses `<docs_root>/context` and requires the active docs root to be identified explicitly by the Agent or workflow.
- Global scope uses `M_CONTEXT_HOME` when explicitly configured.
- Otherwise global scope uses `$CODEX_HOME/m-contexts`.
- When `CODEX_HOME` is unset, global scope uses `~/.codex/m-contexts`.
- Store each context as one UTF-8 Markdown file named `<context-name>.md`.
- Context files may contain plaintext passwords, tokens, private keys, connection strings, and other sensitive operational information.
- The skill does not automatically edit `.gitignore`, `.git/info/exclude`, Git config, staging, commits, pushes, or remotes for context files.

## Loading Workflow

1. Parse an optional `local:` or `global:` prefix and an optional section selector.
2. For an unqualified name, check the exact local context first and check global only when the local root or exact file is absent.
3. For a qualified name, resolve only the selected scope and never fall back.
4. If a local file exists but cannot be resolved, validated, decoded, read, or sectioned, fail locally instead of hiding the error with global content.
5. Load the whole Markdown file, or extract the requested heading and its nested subsections.
6. When another skill is present in the same request, finish context loading before executing that skill.
7. Report the selected scope, context name, and section without reproducing sensitive values unnecessarily.

## Create And Update Workflow

- A new context must use an explicit `local:` or `global:` target.
- An unqualified update changes the exact context selected by normal local-first resolution.
- If an unqualified name exists in neither scope, ask the user to select a scope instead of guessing.
- Preserve unrelated headings and secret values during updates.
- Context operations do not implicitly stage, commit, ignore, publish, or push the affected file.

## Validation Rules

- Reject empty names, path separators, traversal segments, and resolved paths outside the selected context root.
- Resolve local paths only from an explicit docs root; do not walk parent directories to guess a project.
- Fail explicitly when the selected root, context, or requested section does not exist.
- Do not silently select a partial match for normal loading.
- `find` may return partial filename matches, but the user or Agent must choose an exact result before loading.

## Empty / Loading / Error States

- Missing explicit-local docs root: explain that `docs_root` must be resolved or supplied.
- Missing local root/file in auto mode: continue to global; all other local errors remain terminal.
- Missing selected context root: explain the expected path and how to create or configure it.
- Empty selected context root: return an empty list without fabricating defaults.
- Missing context: show exact-name failure and nearby `find` results when available.
- Missing section: list available headings.
- Invalid UTF-8 or unreadable file: fail with the affected path and cause.

## Acceptance Scenarios

### Compose With Testing

Given `nas配置.md` exists, when the user invokes `$m-test $m-context nas配置`, then the Agent loads the NAS context before applying the test workflow.

### Prefer Project-local Context

Given both local and global stores contain `测试环境.md`, when the user invokes `$m-context 测试环境`, then the Agent loads only the local copy and reports the local source.

### Fall Back Only For Absence

Given the local exact context is absent and a global copy exists, when the user invokes `$m-context 测试环境`, then the Agent loads the global copy. Given the local file exists but is unreadable or invalid, the same invocation fails without global fallback.

### Select One Scope Explicitly

Given either store contains `测试环境.md`, when the user invokes `$m-context local:测试环境` or `$m-context global:测试环境`, then only the named scope is inspected.

### Load One Section

Given a context contains `## 测试方式`, when the user invokes `$m-context nas配置#测试方式`, then the Agent loads that heading and its nested content without loading unrelated peer sections.

### Read Plaintext Secrets

Given a selected context contains a plaintext password or private key, when the Agent needs it for the authorized task, then it may read and use the value directly without an encryption or secret-store flow.

### Reject Traversal

Given a context name attempts to escape the configured root, when loading is requested, then the loader rejects it with an actionable error.

## Cross-repo Ownership

- Source skill and loader: `skills/m-context`
- Umbrella discovery and composition documentation: `skills/m-autoflow`
- Local context data: `<docs_root>/context`, outside governed-doc taxonomy even when the docs root is versioned
- Global context data: user-local `m-contexts` directory outside this repository by default

## Related Intake

- [2026-07-13_m-context.md](../intake/2026-07-13_m-context.md)
- [2026-07-15_m-context-scopes.md](../intake/2026-07-15_m-context-scopes.md)

## Related Requirements

- [m-context-skill.md](../requirements/m-context-skill.md)

## Related Specs

- [m-context-skill.md](../specs/m-context-skill.md)

## Related Decisions

- None.

## Related Changes

- [2026-07-13_m-context.md](../change/2026-07-13_m-context.md)
- [2026-07-15_m-context-scopes.md](../change/2026-07-15_m-context-scopes.md)

## Related Lessons

- [Python cache files during skill synchronization](../lessons/python-cache-skill-sync.md)
- [Windows skill parity and line endings](../lessons/windows-skill-parity-line-endings.md)
- [Windows symlink test privilege](../lessons/windows-symlink-test-privilege.md)
