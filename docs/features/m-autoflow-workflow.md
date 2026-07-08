# m:autoflow Workflow

## Feature Goal

Give the user one disciplined workflow family for turning an idea into discussion, architecture, implementation, validation, and archive without scattering current truth across chat history or dated change notes.

## Non-goals

- Replace project-specific product specs.
- Publish private docs or choose backup targets.
- Keep compatibility aliases without an explicit future decision.

## Actors

- User: owns goals, priorities, docs publication choices, and explicit archive-only pauses when they do not want default workflow closeout.
- Main Codex agent: owns phase orchestration, requirements decisions, architecture decisions, integration, validation summary, and final acceptance.
- Optional sub-agents: may perform bounded read-only research, implementation, or review work only when the active phase permits delegation.

## Entry Points

- `$m-autoflow`: umbrella entry for the whole workflow or next-phase routing.
- `$m-discuss`: discovery, brainstorming, current-practice research when useful, requirement shaping, and early worktree setup.
- `$m-plan`: architecture and execution planning.
- `$m-execute`: confirmed Task ID implementation and lightweight validation.
- `$m-test`: optional heavy validation and review.
- `$m-archive`: change archive, lessons, default workflow closeout, merge decision, and cleanup routing.

## User Workflow

1. The user starts with `$m-autoflow` or a specific phase command.
2. Discussion clarifies the request, records open questions, compares options, rejects weak directions, and recommends a path.
3. Discussion creates or confirms the dedicated worktree when project, docs, and code-repo boundaries are clear enough.
4. Planning turns the discussion brief into requirements, architecture, and a handoff-ready `plan.md` / `todo.md`.
5. The user approves execution scope.
6. Execution implements only approved Task IDs and runs lightweight checks.
7. Heavy testing runs when risk justifies it, or the user may explicitly skip it and proceed to archive with residual risk recorded.
8. When heavy testing runs for UI changes, Codex opens and operates the affected interface and provides screenshot evidence.
9. `$m-test` reports a concise pass/fail table directly in the user response.
10. Archive records the change, stable-doc impact, lessons impact, validation, rollback, and sub-agent trace.
11. Archive closes the workflow by default through verified control-plane merge and worktree cleanup.
12. The workflow stops after archive only when the user explicitly asks for archive-only handling, no merge, or no cleanup.

## Artifacts And Layout

- Active workflow control:
  - root-level `plan.md` or `todo.md` in the active worktree
- Current feature truth:
  - `docs/features/<feature>.md`
- Current requirement truth:
  - `docs/requirements/<topic>.md`
- Current technical contract:
  - `docs/specs/<topic>.md`
- Architecture decisions:
  - `docs/decisions/YYYY-MM-DD_<topic>.md`
- Historical archive:
  - `docs/change/YYYY-MM-DD_<topic>.md`
- Reusable troubleshooting knowledge:
  - `docs/lessons/<topic>.md`

## Multi-repo Behavior

- `project_root` is the user-facing project boundary.
- `docs_root` is the governed documentation root and may be outside every code repo.
- `code_repos` lists every implementation repository participating in the capability.
- `active_worktree` records the current worktree for each repo being changed.
- A capability spanning multiple repos still has one feature dossier unless the user intentionally splits the product surface.

## State And Validation

- A phase is blocked when unresolved questions remain or a required artifact is missing.
- Blocked output uses `问题清单` and `阻塞：是`.
- Execution must report lightweight validation.
- Heavy validation must report either passed checks or skip rationale with residual risk.
- UI-impacting changes tested through `$m-test` must include actual UI operation evidence and screenshot paths.
- `$m-test` must include a concise direct pass/fail table so the user can understand results without opening archive markdown.
- Archive must link related intake, feature, requirement, spec, decision, lessons, and plan artifacts.

## Acceptance Scenarios

### Start From Discussion

Given the user invokes `$m-discuss`, when the request is still broad, then Codex records options, assumptions, open questions, rejected directions, recommended direction, and worktree/docs-root status before planning.

### Reject Weak Requirements

Given a requested requirement is unsafe, contradictory, or not implementable, when `$m-plan` evaluates it, then Codex blocks planning or returns to discussion with a better alternative instead of silently accepting it.

### Keep Docs Private

Given the user chooses a private docs root outside code repos, when a workflow updates docs, then Codex writes governed docs into that docs root and does not push or publish them without explicit instruction.

### Multi-repo Capability

Given one user capability is implemented by several repos, when the workflow documents current behavior, then Codex updates one feature dossier with repo ownership mapping and links separate technical specs where needed.

### Lightweight Change

Given a low-risk small change passes execution checks, when heavy testing is unnecessary, then Codex records the skip reason and residual risk before archive.

### UI Change Validation

Given a workflow changes UI, when `$m-test` runs, then Codex opens the affected interface, operates the affected user path, captures screenshot evidence, and summarizes pass/fail status in a direct table.

### User Skips Heavy Testing

Given the user explicitly chooses to skip `$m-test`, when the workflow proceeds to `$m-archive`, then Codex records the skipped testing, missing evidence, and residual risk instead of fabricating validation.

## Related Requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related Specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related Decisions

- [../decisions/2026-07-08_m-skill-phase-naming.md](../decisions/2026-07-08_m-skill-phase-naming.md)

## Related Changes

- [../change/2026-07-08_m-archive-default-closeout.md](../change/2026-07-08_m-archive-default-closeout.md)
- [../change/2026-07-08_m-skill-phase-rename.md](../change/2026-07-08_m-skill-phase-rename.md)

## Related Lessons

- [../lessons/skill-frontmatter-yaml-colon.md](../lessons/skill-frontmatter-yaml-colon.md)
