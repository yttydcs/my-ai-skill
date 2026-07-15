# Context Format

## Storage Roots

The loader supports two plaintext scopes:

- Local: `<docs_root>/context`
- Global:
  1. `M_CONTEXT_HOME`
  2. `$CODEX_HOME/m-contexts`
  3. `~/.codex/m-contexts`

`docs_root` must be resolved explicitly from the active project or workflow. The loader does not search parent directories for it. Set `M_CONTEXT_HOME` when a different global directory is needed. Context data does not belong inside the installed skill package.

An unqualified name checks local first and checks global only when the local root or exact file is absent. An existing local file that fails validation, reading, UTF-8 decoding, or section lookup blocks global fallback.

## Files

- Store one context in one UTF-8 Markdown file.
- Use the exact filename stem as the context name: `nas配置.md` becomes `nas配置`.
- Unicode characters and spaces are allowed.
- Do not pass `.md` in `$m-context` load syntax.
- Plaintext passwords, tokens, private keys, connection strings, and other sensitive values are allowed.
- No YAML frontmatter is required.
- Context files are ordinary user-controlled files. The skill does not add ignore rules or change Git state for them.

Example:

```markdown
# NAS 配置

## 连接信息

- Host: 192.168.1.10
- SSH Port: 2222
- Username: admin
- Password: plaintext-password
- Private Key: C:\Users\HelloWorld\.ssh\nas_ed25519

## 测试方式

- Workdir: /volume1/test
- Command: npm run test:nas

### 清理

- Remove temporary containers after testing.

## 约束

- Do not modify /volume1/production.
```

## Section Loading

Use an exact ATX heading name:

```text
$m-context nas配置#测试方式
$m-context local:nas配置#测试方式
```

The loader returns the matched heading, its body, and nested headings. It stops at the next heading of the same or higher level. Duplicate exact heading names are ambiguous and fail explicitly.

## Authoring Guidance

- Use stable headings such as `连接信息`, `测试方式`, `部署方式`, and `约束` so a caller can load only what it needs.
- Put multiline private keys in fenced code blocks.
- Keep environment-specific facts in contexts rather than copying them into reusable skill instructions.
- Treat the directory as trusted local Agent memory. Files copied from untrusted sources should be reviewed before loading.
- Use `local:` or `global:` when creating a new context. Unqualified updates are allowed only when exact auto resolution already selects an existing file.
- Do not assume local context files are ignored or private from Git merely because they live under `docs_root/context`.
