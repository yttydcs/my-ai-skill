# m:context Skill

## Background

Users repeatedly provide the same environment details, paths, commands, credentials, and operational constraints to Agents. Chat-only repetition is inefficient and makes automation fragile.

## Goal

Provide a lightweight, reusable, user-local context store that Agents can load by name before performing another task.

## Scope

### Must

- provide a discoverable `$m-context` skill
- keep context data separate from the installed skill package
- use a configurable user-level context root with a deterministic fallback
- store contexts as UTF-8 Markdown
- allow arbitrary plaintext content, including passwords, tokens, private keys, and connection strings
- load contexts by exact name
- load an optional Markdown section with nested subsections
- compose with another skill in the same request and load context first
- list available contexts and find contexts by name
- fail explicitly for invalid names, missing files, unreadable content, and missing sections
- prevent path traversal outside the configured context root
- avoid unnecessary secret reproduction in user-facing summaries while still allowing the Agent to read and use all selected content

### Optional

- allow the Agent to create or update context Markdown files when the user asks
- allow `M_CONTEXT_HOME` to relocate the store
- provide nearby filename suggestions after an exact lookup failure

### Out of Scope

- encryption at rest
- OS credential vaults or external secret managers
- access-control systems beyond local filesystem permissions
- remote synchronization or publication
- automatic secret rotation, expiry, or revocation
- fuzzy loading that silently chooses a context

## Scenarios

- The user loads NAS connection details before running `$m-test`.
- The user loads deployment commands before `$m-execute` or `$m-quick`.
- The user loads only the `测试方式` section of a larger context.
- The Agent uses a plaintext password or private key found in a selected context.
- The user lists or searches saved contexts instead of remembering the exact filename.

## Functional Requirements

- `$m-context <name>` must load `<name>.md` from the resolved context root.
- `$m-context <name>#<section>` must load the matching ATX Markdown heading and content until the next heading of the same or higher level.
- `$m-context list` must enumerate context names without reading or printing their contents.
- `$m-context find <query>` must return case-insensitive filename matches without loading them.
- Co-invocation such as `$m-test $m-context nas配置` must load the selected context before the consuming skill begins task work.
- The loader must use `M_CONTEXT_HOME`, then `CODEX_HOME/m-contexts`, then `~/.codex/m-contexts` in that order.
- Normal loading must require an exact context filename stem.
- The implementation must use only bundled or standard runtime dependencies.

## Non-functional Requirements

- Keep the skill body concise and route format details to one direct reference.
- Preserve Unicode names and content on Windows.
- Produce actionable errors without swallowing filesystem or decoding failures.
- Do not scan outside the resolved context root.
- Do not print complete context contents merely to confirm that loading succeeded.
- Keep loading cost proportional to the selected file rather than reading every context body.

## Edge Cases

- `M_CONTEXT_HOME` points to a missing directory.
- The context root exists but is empty.
- A context name contains `/`, `\`, `..`, or an absolute path.
- A UTF-8 filename contains Chinese characters or spaces.
- Two headings have the same displayed text.
- A requested section contains nested headings.
- The Markdown file is empty or invalid UTF-8.
- The file contains plaintext secrets that must be used but not repeated in the final response.

## Acceptance Criteria

- The new skill passes repository skill validation.
- Unit tests cover root resolution, Unicode context names, whole-file loading, section loading, missing resources, and traversal rejection.
- The installed skill copy matches the validated source after synchronization, excluding generated build metadata where appropriate.
- A documented example demonstrates `$m-test $m-context nas配置` ordering.
- No encryption, credential-vault, or remote-sync dependency is introduced.

## Related Features

- [m-context.md](../features/m-context.md)
- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Specs

- [m-context-skill.md](../specs/m-context-skill.md)

## Related Changes

- [2026-07-13_m-context.md](../change/2026-07-13_m-context.md)
