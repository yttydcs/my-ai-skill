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
- `$m-go` worker sub-agents: perform all implementation edits for `$m-go` runs while the main Codex agent schedules, audits, validates, and accepts results.

## Entry Points

- `$m-autoflow`: umbrella entry for the whole workflow or next-phase routing.
- `$m-context`: companion loader for reusable user-local plaintext context; it may be combined with any phase or fast path and loads before task actions.
- `$m-quick`: standalone guarded direct-edit path for explicit low-risk work in one repository after mandatory `$m-docs` context reading.
- `$m-discuss`: discovery, brainstorming, current-practice research when useful, requirement shaping, and early worktree setup.
- `$m-plan`: architecture and execution planning.
- `$m-execute`: confirmed Task ID implementation and lightweight validation.
- `$m-go`: high-automation delegated execution and automatic `$m-test` loop for confirmed plans.
- `$m-test`: optional heavy validation and review.
- `$m-archive`: change archive, lessons, default workflow closeout, merge decision, and cleanup routing.

## User Workflow

1. The user starts with `$m-autoflow` or a specific phase command, optionally adding `$m-context <name>` to load saved context first.
2. Discussion clarifies the request, records open questions, compares options, rejects weak directions, and recommends a path.
3. Discussion creates or confirms the dedicated worktree when project, docs, and code-repo boundaries are clear enough.
4. Planning turns the discussion brief into requirements, architecture, and a handoff-ready `plan.md` / `todo.md`.
5. `$m-plan` shows a concise task summary table directly in the user response.
6. The user approves execution scope.
7. Execution implements only approved Task IDs and runs lightweight checks through `$m-execute`, or the user invokes `$m-go` for delegated implementation and an automatic `$m-test` loop.
8. `$m-go` dispatches implementation edits to worker sub-agents, reviews their results, runs validation, and delegates bounded fixes until acceptance passes or a blocker is explicit.
9. Heavy testing runs when risk justifies it, when `$m-go` automatically invokes it, or when the user requests it; the user may explicitly skip `$m-test` only outside the normal `$m-go` path and proceed to archive with residual risk recorded.
10. When heavy testing runs for UI changes, Codex opens and operates the affected interface and provides screenshot evidence.
11. `$m-test` reports a concise pass/fail table directly in the user response.
12. Archive records the change, stable-doc impact, lessons impact, validation, rollback, and sub-agent trace.
13. Archive closes the workflow by default through verified control-plane merge and worktree cleanup.
14. The workflow stops after archive only when the user explicitly asks for archive-only handling, no merge, or no cleanup.

## Standalone Quick Path

`$m-quick` sits beside the staged workflow rather than inside it. The user explicitly selects it for a bounded small requirement or bug fix.

1. The main agent reads project-local instructions and identifies the governed docs root plus one target code repository.
2. The agent explicitly uses `$m-docs` to read the minimum relevant indexes and stable leaf docs before accepting fast-path eligibility.
3. The agent checks risk, Git status, existing changes, rollback, and focused validation.
4. Eligible work is edited directly in the selected current checkout without a quick-request worktree or plan.
5. Ineligible work is routed to `$m-discuss` or `$m-plan` before scope expands.
6. Focused validation runs; UI-impacting changes require actual operation and screenshot evidence.
7. Stable docs are updated through `$m-docs` only when stable truth changed.
8. The command returns a compact context/gate/change/validation/docs/risk table and stops without automatic archive, merge, cleanup, or push.

The complete current behavior is maintained in [m-quick-fast-path.md](m-quick-fast-path.md).

## Artifacts And Layout

- Active workflow control:
  - root-level `plan.md` or `todo.md` in the active worktree
- Standalone quick requests:
  - no root plan or workflow archive by default
  - update only affected stable docs when current truth changes
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

- `$m-context` is not a workflow phase and does not change the active phase; a failed required context load blocks dependent actions.
- A phase is blocked when unresolved questions remain or a required artifact is missing.
- Blocked output uses `问题清单` and `阻塞：是`.
- Planning must include a direct task summary table that reflects the active `plan.md` / `todo.md`.
- Execution must report lightweight validation.
- `$m-go` must require a confirmed plan, delegate implementation edits to sub-agents, run safe parallel task execution when write sets allow it, and automatically run `$m-test` behavior after delegated execution.
- `$m-go` must return failing validation to delegated fixes until acceptance passes or the blocker is explicit.
- `$m-quick` must read governed docs before eligibility, operate on one selected repository, reject prohibited risk, preserve existing changes, run focused validation, and report a concise direct result table.
- `$m-quick` is the sole explicit direct-edit exception to staged worktree and confirmed-plan gates; it must not weaken those gates for other commands.
- Heavy validation must report either passed checks or skip rationale with residual risk.
- UI-impacting changes tested through `$m-test` must include actual UI operation evidence and screenshot paths.
- `$m-test` must include a concise direct pass/fail table so the user can understand results without opening archive markdown.
- Archive must link related intake, feature, requirement, spec, decision, lessons, and plan artifacts.

## User-facing Output Experience

- Every workflow-family or companion-utility result leads with the outcome, decision, or blocker.
- Repeated fields and status mappings use compact tables; simple one-off results remain prose.
- Mermaid is reserved for dependencies, branches, ownership, or state flows that are materially harder to understand linearly.
- Local plans, changed files, docs, and evidence use absolute clickable links.
- UI or rendered-document acceptance embeds representative visual evidence and links additional artifacts.
- Actionable line-specific review findings may use code-comment components with tight source ranges.
- Git components appear only after the matching branch, stage, commit, push, or pull-request action succeeds.
- Plain Markdown continues to carry the result so the response remains readable when a component is unavailable.

## Acceptance Scenarios

### Load Reusable Context Before A Phase

Given a user-local `nas配置.md` exists, when the user invokes `$m-test $m-context nas配置`, then the context is loaded before `$m-test` performs validation actions and its plaintext contents are available to the Agent.

### Start From Discussion

Given the user invokes `$m-discuss`, when the request is still broad, then Codex records options, assumptions, open questions, rejected directions, recommended direction, and worktree/docs-root status before planning.

### Reject Weak Requirements

Given a requested requirement is unsafe, contradictory, or not implementable, when `$m-plan` evaluates it, then Codex blocks planning or returns to discussion with a better alternative instead of silently accepting it.

### Plan Task Summary

Given `$m-plan` creates or confirms a plan, when the user reviews the planning response, then Codex shows a concise task table with Task ID, scope, files/modules, acceptance/tests, and risk notes.

### Keep Docs Private

Given the user chooses a private docs root outside code repos, when a workflow updates docs, then Codex writes governed docs into that docs root and does not push or publish them without explicit instruction.

### Multi-repo Capability

Given one user capability is implemented by several repos, when the workflow documents current behavior, then Codex updates one feature dossier with repo ownership mapping and links separate technical specs where needed.

### Lightweight Change

Given a low-risk small change passes execution checks, when heavy testing is unnecessary, then Codex records the skip reason and residual risk before archive.

### Standalone Quick Change

Given the user explicitly invokes `$m-quick` for a bounded low-risk request in one repository, when relevant docs support the request and focused validation is available, then Codex reads those docs, edits the current checkout directly, validates the affected behavior, updates stable docs only when needed, and returns the compact result table without starting a staged workflow.

### Quick Change Escalation

Given a quick request conflicts with docs or touches multiple repos, architecture, a public contract, schema, migration, security boundary, destructive data, production infrastructure, or broad validation, when eligibility is evaluated, then Codex performs no expanding implementation and recommends `$m-discuss` or `$m-plan` with the failed gate.

### Automated Delegated Execution

Given the user invokes `$m-go` after a confirmed plan, when executable Task IDs have bounded write sets, then Codex delegates implementation edits to worker sub-agents, runs safe parallel lanes where possible, automatically runs `$m-test`, and loops delegated fixes until the acceptance checks pass or a blocker is explicit.

### UI Change Validation

Given a workflow changes UI, when `$m-test` runs, then Codex opens the affected interface, operates the affected user path, captures screenshot evidence, and summarizes pass/fail status in a direct table.

### Complex Plan Visualization

Given a plan has meaningful task dependencies or branching system flow, when `$m-plan` presents the result, then Codex links the plan artifact, shows the exact task table, and may add a focused Mermaid diagram without duplicating flat checklist content.

### Successful Git Action

Given an authorized Git action succeeds, when the phase returns its final result in a supporting Codex host, then Codex emits the matching Git component and an ordinary text status. Failed or unperformed actions emit no component.

### User Skips Heavy Testing

Given the user explicitly chooses to skip `$m-test`, when the workflow proceeds to `$m-archive`, then Codex records the skipped testing, missing evidence, and residual risk instead of fabricating validation.

## Related Requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)
- [../requirements/m-quick-fast-path.md](../requirements/m-quick-fast-path.md)

## Related Specs

- [../specs/m-autoflow-skill.md](../specs/m-autoflow-skill.md)
- [../specs/m-quick-skill.md](../specs/m-quick-skill.md)

## Related Decisions

- [../decisions/2026-07-08_m-skill-phase-naming.md](../decisions/2026-07-08_m-skill-phase-naming.md)
- [../decisions/2026-07-09_m-go-automated-execution.md](../decisions/2026-07-09_m-go-automated-execution.md)
- [../decisions/2026-07-10_m-quick-standalone-fast-path.md](../decisions/2026-07-10_m-quick-standalone-fast-path.md)

## Related Changes

- [../change/2026-07-15_visual-output-components.md](../change/2026-07-15_visual-output-components.md)
- [../change/2026-07-13_m-context.md](../change/2026-07-13_m-context.md)
- [../change/2026-07-08_m-plan-task-table.md](../change/2026-07-08_m-plan-task-table.md)
- [../change/2026-07-08_m-test-ui-evidence.md](../change/2026-07-08_m-test-ui-evidence.md)
- [../change/2026-07-08_m-archive-default-closeout.md](../change/2026-07-08_m-archive-default-closeout.md)
- [../change/2026-07-08_m-skill-phase-rename.md](../change/2026-07-08_m-skill-phase-rename.md)

## Related Lessons

- [../lessons/skill-frontmatter-yaml-colon.md](../lessons/skill-frontmatter-yaml-colon.md)
