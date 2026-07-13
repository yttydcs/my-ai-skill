# m:context Skill Spec

## Scope

Define the package, storage, invocation, parsing, composition, validation, and installation contracts for reusable Agent context loading.

## Package Contract

```text
skills/m-context/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── context-format.md
└── scripts/
    └── context_loader.py
```

- `SKILL.md` owns resolution and composition workflow instructions.
- `context-format.md` owns the user-authored Markdown contract and examples.
- `context_loader.py` provides deterministic root resolution, listing, searching, exact loading, and section extraction.
- `manifests/m-context.json` registers repository distribution and installation metadata.

## Context Root Resolution

Resolve exactly one root in this order:

1. `M_CONTEXT_HOME` when non-empty.
2. `<CODEX_HOME>/m-contexts` when `CODEX_HOME` is non-empty.
3. `~/.codex/m-contexts`.

The root is allowed to contain plaintext sensitive information. It is outside Git repositories by default but is not encrypted or otherwise hidden from the Agent.

## Context File Contract

- File extension: `.md`
- Encoding: UTF-8
- Canonical context identifier: exact filename stem
- Filename may contain Unicode characters and spaces.
- Context body may contain arbitrary Markdown and plaintext secrets.
- Headings use ATX syntax (`#` through `######`).
- No required YAML frontmatter is introduced in the first version.

Example:

```markdown
# NAS 配置

## 连接信息
- Host: 192.168.1.10
- Password: plaintext-value

## 测试方式
- Workdir: /volume1/test

### 清理
- Remove temporary containers after testing.
```

## Invocation Contract

```text
$m-context <name>
$m-context <name>#<section>
$m-context list
$m-context find <query>
```

- `<name>` is resolved by exact filename stem.
- `#<section>` matches heading text exactly after surrounding whitespace is trimmed.
- When a section name occurs more than once, fail as ambiguous and report matching heading levels or positions.
- Section output includes the matched heading, its body, and nested headings until the next heading of the same or higher level.
- `list` returns sorted context names only.
- `find` performs a case-insensitive substring match on filenames and returns names only.

## Composition Contract

When `$m-context` and another skill are named in one request:

1. Read both skills as required by the host.
2. Resolve and load every explicitly requested context before the consuming skill performs task actions.
3. Treat loaded content as user-provided task context.
4. Preserve higher-priority system, developer, repository, and skill instructions.
5. Announce which context names and sections were loaded, but do not echo complete sensitive contents unless needed.
6. If a required context cannot be loaded, block the consuming action rather than proceeding with guessed values.

The order is semantic rather than shell pipeline syntax. `$m-test $m-context nas配置` means context-first task execution even though both skills trigger from the same prompt.

## Loader Interface

The standard-library Python helper exposes:

```text
context_loader.py root
context_loader.py list
context_loader.py find <query>
context_loader.py load <name>
context_loader.py load <name> --section <heading>
```

Successful `load` writes selected Markdown to stdout so the Agent can consume it. Diagnostics go to stderr. Failures use a non-zero exit status and actionable messages.

## Path Safety

- Reject absolute names, drive-qualified names, path separators, `.` and `..` path components, and names ending in `.md` when the interface expects a stem.
- Resolve the candidate path and require it to remain inside the resolved context root.
- Do not recursively scan arbitrary parent directories.
- Do not follow a resolved context file outside the root through a symlink or junction.

These checks protect deterministic lookup and accidental file disclosure; they are not an encryption or authorization layer.

## Secret Handling Contract

- Plaintext secrets are explicitly permitted in context files.
- The Agent may read and use all content in a user-selected context.
- Do not redact loader output before it reaches the Agent.
- Do not automatically reproduce secrets in commentary, final responses, plans, archives, screenshots, or test reports.
- Do not copy context data into the skill package, distribution tree, or repository documentation.

## Error Handling

- Missing root: identify the resolved path and configuration variables.
- Missing context: identify the exact requested name and optionally list nearby filename matches.
- Missing section: identify the section and list available headings.
- Duplicate section: fail instead of choosing silently.
- Invalid UTF-8, unreadable file, or filesystem error: preserve the cause and affected path.
- Invalid name or root escape: reject before content loading.

## Validation Contract

- Run standard-library unit tests for loader behavior.
- Run `tools/validate-skills.ps1 -Skill m-context`.
- Run `tools/validate-skills.ps1 -Skill m-autoflow` after umbrella integration changes.
- Run `tools/sync-skills.ps1 -Skill m-context` only after validation succeeds.
- Check source/install parity after sync, excluding generated `.build-info.json` and accounting for Windows line endings during pre-sync drift checks.
- Run `git diff --check` before acceptance.

## Performance Constraints

- `load` reads only the selected context file.
- `list` and `find` inspect filenames without reading file bodies.
- Section extraction is linear in the selected file size.
- No third-party runtime dependency is required.

## Related Features

- [m-context.md](../features/m-context.md)
- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Requirements

- [m-context-skill.md](../requirements/m-context-skill.md)

## Related Decisions

- None.

## Related Changes

- [2026-07-13_m-context.md](../change/2026-07-13_m-context.md)
