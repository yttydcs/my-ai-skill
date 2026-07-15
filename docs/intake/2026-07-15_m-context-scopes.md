# 2026-07-15 m-context Local And Global Scopes

## Source

- Source: Codex chat
- Date: 2026-07-15

## Request Text / Source-preserving Summary

The user wants `$m-context` to distinguish project-local and user-global saved context. Project-local context must live at:

```text
<docs_root>/context
```

An unqualified invocation such as `$m-context 测试环境` should first look for the exact local context and only look in the global store when the local context does not exist. It should not combine both copies. Explicit local/global selection should also be available.

The user continues to allow plaintext passwords, tokens, keys, and similar secrets because the store exists to make Agent automation easier. The Agent must be able to read those values directly; encryption is not required.

The user explicitly rejected automatically adding `docs/context` to `.gitignore` or otherwise changing Git ignore configuration. The feature must not make unrelated Git configuration or state changes on the user's behalf.

## Confirmed Requirements

- Add local and global context scopes.
- Use `<docs_root>/context` for local contexts.
- Preserve the existing user-global store and configuration precedence.
- Use local-first, absence-only fallback for unqualified loads.
- Provide strict `local:` and `global:` selection without fallback.
- Report which scope supplied the selected context.
- Permit plaintext secrets and direct Agent use.
- Do not automatically modify `.gitignore`, `.git/info/exclude`, or other Git state.

## Open Questions

- None blocking planning.

## Routed Docs

- [Feature](../features/m-context.md)
- [Requirements](../requirements/m-context-skill.md)
- [Specification](../specs/m-context-skill.md)
- [Archived plan](../plan/2026-07-15_m-context-scopes.md)

## Related Intake

- [2026-07-13_m-context.md](2026-07-13_m-context.md)

## Related Changes

- [2026-07-15_m-context-scopes.md](../change/2026-07-15_m-context-scopes.md)
