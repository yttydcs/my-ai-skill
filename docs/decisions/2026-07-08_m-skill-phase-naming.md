# 2026-07-08 M Skill Phase Naming

## Status

Accepted

## Context

The workflow had grown from one umbrella skill into several separately invokable phase skills. The long phase names were accurate but noisy in daily use, and research was modeled as a separate optional phase rather than a fuller discussion phase.

The user wants:

- short phase commands
- `m-autoflow` to remain the collection entry point
- less duplicated instruction text
- a first-class discussion phase that can research current best practices when useful
- planning to behave like senior architecture review, including rejecting bad requirements

## Options Considered

- Keep long phase names.
  - Rejected because they make frequent manual invocation harder.
- Rename canonical phase skills to short `m-*` names.
  - Accepted because it keeps daily usage concise while preserving clear phase boundaries.
- Keep compatibility aliases immediately.
  - Deferred because aliases would add extra packages, validation surface, sync behavior, and stale-instruction risk.
- Move shared references into a separate core package now.
  - Deferred because `m-autoflow` can act as umbrella plus shared reference host without another package boundary.

## Decision

Use these canonical phase names:

- `$m-discuss`
- `$m-plan`
- `$m-execute`
- `$m-test`
- `$m-archive`

Keep `$m-autoflow` as the umbrella entry point and shared reference host for this workflow family.

Discussion owns discovery, brainstorming, current-practice research when needed, requirement shaping, and early worktree setup. Planning owns architecture, executable planning, approval gating, and rejection of unreasonable requirements.

## Consequences

- Current source packages, manifests, and stable docs use the short names.
- Historical `docs/change` records may keep older names as append-only evidence.
- Installed stale copies of superseded phase packages should be removed after sync unless aliases are explicitly reintroduced later.
- A future separate reference/core package remains possible if `m-autoflow` becomes too large as a shared host.

## Related Feature

- [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related Specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)
