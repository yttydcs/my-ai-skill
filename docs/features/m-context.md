# m:context Reusable Agent Context

## Status

Active.

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
$m-context nas配置#测试方式
$m-context list
$m-context find nas
$m-test $m-context nas配置
```

## Context Storage

- Use `M_CONTEXT_HOME` when explicitly configured.
- Otherwise use `$CODEX_HOME/m-contexts`.
- When `CODEX_HOME` is unset, use `~/.codex/m-contexts`.
- Store each context as one UTF-8 Markdown file named `<context-name>.md`.
- Context files may contain plaintext passwords, tokens, private keys, connection strings, and other sensitive operational information.

## Loading Workflow

1. Resolve the configured context root.
2. Resolve the requested context by exact filename stem.
3. Load the whole Markdown file, or extract the requested heading and its nested subsections.
4. When another skill is present in the same request, finish context loading before executing that skill.
5. Report the loaded context name and section without reproducing sensitive values unnecessarily.

## Validation Rules

- Reject empty names, path separators, traversal segments, and resolved paths outside the context root.
- Fail explicitly when the root, context, or requested section does not exist.
- Do not silently select a partial match for normal loading.
- `find` may return partial filename matches, but the user or Agent must choose an exact result before loading.

## Empty / Loading / Error States

- Missing context root: explain the expected path and how to create or override it.
- Empty context root: return an empty list without fabricating defaults.
- Missing context: show exact-name failure and nearby `find` results when available.
- Missing section: list available headings.
- Invalid UTF-8 or unreadable file: fail with the affected path and cause.

## Acceptance Scenarios

### Compose With Testing

Given `nas配置.md` exists, when the user invokes `$m-test $m-context nas配置`, then the Agent loads the NAS context before applying the test workflow.

### Load One Section

Given a context contains `## 测试方式`, when the user invokes `$m-context nas配置#测试方式`, then the Agent loads that heading and its nested content without loading unrelated peer sections.

### Read Plaintext Secrets

Given a selected context contains a plaintext password or private key, when the Agent needs it for the authorized task, then it may read and use the value directly without an encryption or secret-store flow.

### Reject Traversal

Given a context name attempts to escape the configured root, when loading is requested, then the loader rejects it with an actionable error.

## Cross-repo Ownership

- Source skill and loader: `skills/m-context`
- Umbrella discovery and composition documentation: `skills/m-autoflow`
- Context data: user-local `m-contexts` directory outside this repository by default

## Related Intake

- [2026-07-13_m-context.md](../intake/2026-07-13_m-context.md)

## Related Requirements

- [m-context-skill.md](../requirements/m-context-skill.md)

## Related Specs

- [m-context-skill.md](../specs/m-context-skill.md)

## Related Decisions

- None.

## Related Changes

- [2026-07-13_m-context.md](../change/2026-07-13_m-context.md)

## Related Lessons

- [Windows skill parity and line endings](../lessons/windows-skill-parity-line-endings.md)
- [Windows symlink test privilege](../lessons/windows-symlink-test-privilege.md)
