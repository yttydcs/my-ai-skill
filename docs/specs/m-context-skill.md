# m:context Skill Spec

## Scope

Define the package, storage, invocation, parsing, composition, validation, and installation contracts for reusable Agent context loading.

## Delivery Status

The scoped local/global contract is implemented and active.

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

- `SKILL.md` owns invocation parsing, docs-root handoff, resolution, create/update, and composition workflow instructions.
- `context-format.md` owns the user-authored Markdown contract and examples.
- `context_loader.py` provides deterministic root resolution, listing, searching, exact loading, and section extraction.
- `manifests/m-context.json` registers repository distribution and installation metadata.

## Context Root Resolution

### Local Root

- Accept `docs_root` explicitly from the Agent or active workflow.
- Derive the local root as `<docs_root>/context`.
- Do not infer `docs_root` by recursively scanning parent directories.
- An explicit local operation without `docs_root` is an actionable error.

### Global Root

Resolve the global root in this order:

1. `M_CONTEXT_HOME` when non-empty.
2. `<CODEX_HOME>/m-contexts` when `CODEX_HOME` is non-empty.
3. `~/.codex/m-contexts`.

### Auto Selection

For an unqualified exact name:

1. If `docs_root` is known, inspect `<docs_root>/context/<name>.md`.
2. If the local root or exact local file is absent, inspect the global exact path.
3. If the local exact file exists, select it and do not inspect global content.
4. If an existing local file fails resolution, containment, type, permission, UTF-8, or section validation, fail locally without fallback.
5. If `docs_root` is unavailable, use global scope and report that local lookup was unavailable.

Both roots may contain plaintext sensitive information. Neither is encrypted or hidden from the Agent. `context/` is runtime context data, not a governed-doc category merely because it is under `docs_root`.

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
$m-context local:<name>
$m-context global:<name>
$m-context <name>#<section>
$m-context list
$m-context find <query>
```

- Scope prefixes are parsed before the context name; the optional section selector remains last.
- `<name>` is resolved by exact filename stem.
- Unqualified names use auto selection; explicit names never cross scopes.
- `#<section>` matches heading text exactly after surrounding whitespace is trimmed.
- When a section name occurs more than once, fail as ambiguous and report matching heading levels or positions.
- Section output includes the matched heading, its body, and nested headings until the next heading of the same or higher level.
- Auto `list` returns scope-qualified names in local-then-global order and keeps duplicate stems visible as separate entries.
- `find` performs a case-insensitive substring match on filenames and returns scope-qualified matches without loading bodies.

## Create And Update Contract

- Creating a name that exists in neither scope requires `local:` or `global:`.
- Updating an unqualified existing name uses the same exact auto selection as loading.
- Explicit updates affect only the selected scope.
- Preserve unrelated sections and plaintext values.
- Creation/update/delete does not implicitly change ignore rules, Git configuration, staging, commits, remotes, pushes, or publication state.

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
context_loader.py root [--scope local|global] [--docs-root PATH]
context_loader.py list [--scope auto|local|global] [--docs-root PATH]
context_loader.py find <query> [--scope auto|local|global] [--docs-root PATH]
context_loader.py load <name> [--scope auto|local|global] [--docs-root PATH]
                       [--section <heading>]
```

`root` without new flags retains the existing global-root output for compatibility. Successful `load` writes only selected Markdown to stdout so the Agent can consume it. A concise selected-scope/path diagnostic goes to stderr. Failures use a non-zero exit status and actionable messages.

The Python API should return structured scope/location results rather than requiring callers to parse exception text. A dedicated absence classification controls fallback; generic `OSError`, validation, and content errors do not.

## Path Safety

- Reject absolute names, drive-qualified names, path separators, `.` and `..` path components, and names ending in `.md` when the interface expects a stem.
- Validate the name once, resolve each candidate independently, and require it to remain inside its selected root.
- Do not recursively scan arbitrary parent directories.
- Do not follow a resolved context file outside the root through a symlink or junction.

These checks protect deterministic lookup and accidental file disclosure; they are not an encryption or authorization layer.

## Secret Handling Contract

- Plaintext secrets are explicitly permitted in context files.
- The Agent may read and use all content in a user-selected context.
- Do not redact loader output before it reaches the Agent.
- Do not automatically reproduce secrets in commentary, final responses, plans, archives, screenshots, or test reports.
- Do not copy context data into the skill package, distribution tree, or repository documentation.
- Do not automatically add context paths to ignore files or alter Git state; plaintext context publication remains a user-controlled filesystem/Git decision.

## Error Handling

- Missing explicit-local docs root: request an explicit docs root.
- Missing selected root: identify the resolved path and relevant configuration source.
- Missing auto local root/context: continue to global; if global is also absent, report both attempted scopes.
- Missing explicit-scope context: identify the exact requested scope and name and optionally list nearby matches within that scope.
- Existing local resolution, containment, type, permission, decoding, and section failures: report the local error and do not fall back.
- Missing section: identify the section and list available headings.
- Duplicate section: fail instead of choosing silently.
- Invalid UTF-8, unreadable file, or filesystem error: preserve the cause and affected path.
- Invalid name or root escape: reject before content loading.

## Validation Contract

- Run standard-library unit tests for the scope truth table, loader behavior, CLI diagnostics, and compatibility.
- Run `tools/validate-skills.ps1 -Skill m-context`.
- Run `tools/validate-skills.ps1 -Skill m-docs` when its context-directory governance changes.
- Run `tools/validate-skills.ps1 -Skill m-autoflow` after umbrella integration changes.
- Run `tools/sync-skills.ps1 -Skill m-context` only after validation succeeds.
- Check source/install parity after sync, excluding generated `.build-info.json` and accounting for Windows line endings during pre-sync drift checks.
- Run `git diff --check` before acceptance.

## Performance Constraints

- Auto `load` reads only the selected context file; local fallback probing uses path metadata, not body reads.
- `list` and `find` inspect filenames in at most two roots without reading file bodies.
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
- [2026-07-15_m-context-scopes.md](../change/2026-07-15_m-context-scopes.md)

## Related Intake

- [2026-07-13_m-context.md](../intake/2026-07-13_m-context.md)
- [2026-07-15_m-context-scopes.md](../intake/2026-07-15_m-context-scopes.md)
