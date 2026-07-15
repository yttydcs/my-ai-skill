# m:autoflow Workflow Skill Spec

## Architecture Overview

`m-autoflow` is the umbrella entry point and shared reference host for a focused workflow skill family. Phase-specific behavior lives in short, separately invokable skills, while `$m-quick` provides a guarded standalone fast path outside the stage chain.

## Package Contract

- Umbrella source package: `skills/m-autoflow`
- Context companion package: `skills/m-context`
- Umbrella UI metadata: `skills/m-autoflow/agents/openai.yaml`
- Umbrella install metadata: `manifests/m-autoflow.json`
- Canonical phase source packages:
  - `skills/m-discuss`
  - `skills/m-plan`
  - `skills/m-execute`
  - `skills/m-go`
  - `skills/m-test`
  - `skills/m-archive`
- Canonical phase install metadata:
  - `manifests/m-discuss.json`
  - `manifests/m-plan.json`
  - `manifests/m-execute.json`
  - `manifests/m-go.json`
  - `manifests/m-test.json`
  - `manifests/m-archive.json`
- Canonical standalone fast-path source package:
  - `skills/m-quick`
- Canonical standalone fast-path install metadata:
  - `manifests/m-quick.json`
- Install flow:
  - source -> `dist/codex/<skill-name>` -> `C:\Users\HelloWorld\.codex\skills\<skill-name>`
- Historical archives may mention older phase names as source evidence, but current source packages, manifests, and stable contracts must use the canonical phase names above.

## Trigger Contract

The skill family supports explicit invocation and does not forbid host-side implicit selection in metadata.

- Invoke `$m-autoflow` when the user wants the full workflow or wants the umbrella to choose the next phase.
- Invoke `$m-quick` for an explicit bounded low-risk direct change in one repository after mandatory `$m-docs` context reading.
- Invoke `$m-discuss` for discovery, requirement shaping, brainstorming, optional research, and early worktree setup.
- Invoke `$m-plan` for architecture, executable planning, direct task summary, and approval gating.
- Invoke `$m-execute` for confirmed Task ID implementation plus lightweight validation.
- Invoke `$m-go` for confirmed Task ID implementation through worker sub-agents plus an automatic `$m-test` loop.
- Invoke `$m-test` for optional heavy validation and review, including UI operation evidence when UI changes are tested.
- Invoke `$m-archive` for change archive, lessons, and workflow closeout.
- Web research must be initiated from `$m-discuss` only when current external facts, best-practice comparison, explicit user request, or source-backed investigation is needed.
- `skills/m-autoflow/agents/openai.yaml` must not set:
  - `policy.allow_implicit_invocation: false`
- `manifests/m-autoflow.json` must not declare:
  - `manual_invocation_only: true`

## Workflow Contract

- `$m-context` is a companion loader outside the staged phase chain and outside the `$m-quick` fast path.
- Co-invocation loads every requested context before the consuming skill performs task actions.
- Loaded plaintext context remains task-local and is not copied into workflow artifacts unless explicitly required.
- `$m-quick` is an alternate standalone route and is not part of the default phase order.
- Default phase order:
  - `discuss`
  - `plan`
  - `execute` or `go`
  - optional `test`
  - `archive`
- Direct plan invocation is allowed only when the plan records why discussion was skipped or already satisfied.
- `$m-quick` must apply its own docs-first eligibility gate before direct edits and must escalate unsuitable work before scope expands.
- Only one phase may be active at a time.
- Any rollback must state the reason and update the affected documents.
- Discussion prioritizes relevant private-docs-root intake, feature, and requirement docs when they exist.
- Discussion may create or confirm the dedicated worktree once project boundaries are clear.
- Planning prioritizes relevant private-docs-root specs and decisions when they exist.
- Planning rejects unreasonable, unsafe, contradictory, or under-specified requirements and returns to discussion with alternatives.
- Optional research is read-only and may feed only verified, cited findings into requirements, architecture, `plan.md`, or stable docs.
- Planning must distinguish:
  - `project_root`: umbrella project directory
  - `docs_root`: private governed docs root
  - `code_repos`: one or more implementation repositories
  - `active_worktree`: the current implementation worktree
- When the user keeps docs private, stable docs must be read from and written to `docs_root`, not inferred from code repo `docs/` directories.
- Active workflow control stays in the worktree root as `plan.md` or `todo.md`.
- The active workflow-control rule applies to staged execution. Eligible `$m-quick` requests do not create a root plan or dedicated worktree by default.
- Planning artifacts must include an execution-scope split with `Will Execute` and `Will Not Execute Now` groups. Every known Task ID must appear in exactly one group, and non-executed tasks must include the reason.
- After `$m-plan` creates or confirms the active `plan.md` / `todo.md`, the direct response must include a task summary table.
- The task summary table must include `Task ID`, `Title`, `Scope`, `Files / Modules`, `Acceptance / Tests`, and `Risk / Notes`.
- The task summary table must summarize the active plan artifact and preserve the `Will Execute` / `Will Not Execute Now` split.
- Execution owns lightweight local validation such as syntax checks, type checks, focused lint, touched-file formatting checks, focused unit tests, and `git diff --check`.
- `$m-go` is an alternate execution entry after planning. It requires a confirmed plan, delegates all implementation edits to worker sub-agents, runs safe parallel lanes when write sets allow it, and automatically invokes `$m-test` behavior after delegated execution.
- During `$m-go`, the main agent owns scheduling, context packaging, conflict handling, diff review, command execution, validation synthesis, external status reporting, and final acceptance. The main agent must not directly edit implementation files.
- If `$m-go` validation fails, the main agent must delegate bounded fixes and repeat the test loop until acceptance passes or a blocker is explicit.
- `$m-go` stops before archive, merge, cleanup, and push.
- Heavy validation is optional. It may be skipped for low-risk small changes when execution-stage validation is sufficient and the skip reason plus residual risk are recorded.
- The user may explicitly skip `$m-test` and proceed directly to `$m-archive`; the archive must record skipped validation, missing evidence, and residual risk.
- When heavy validation runs, it must cover integration or end-to-end flow, usability, security boundaries, and performance indicators when applicable.
- When heavy validation runs for UI-impacting changes, it must open the actual UI, operate the affected user path, and capture screenshot evidence.
- If UI evidence cannot be gathered during a run `$m-test`, the result must be `不通过` or `阻塞`.
- `$m-test` must output a concise direct result table with `Area`, `Check`, `Status`, `Evidence`, and `Notes` columns.
- `docs/change/YYYY-MM-DD_topic.md` is required before a workflow counts as complete.
- The change archive belongs in the selected governed docs root when a private docs root exists.
- Archive must record `Lessons impact`, `Related lessons`, and searchable lesson cues.
- Archive must create or update `docs/lessons` when the workflow exposed reusable troubleshooting knowledge.
- After archive, the workflow must close by default through repo control-plane merge and worktree cleanup.
- If the user explicitly requests archive-only handling, no merge, no cleanup, or an equivalent pause, the workflow must stop after archive readiness and report retained branch/worktree state.
- If archive produced lessons docs or lesson-index updates, workflow end must carry them back into the global docs tree.
- Merge and worktree cleanup are forbidden until archive completion, status verification, and unrelated-dirt preservation checks pass.
- `$m-quick` ends after focused validation and direct reporting; it does not create an archive, merge, clean, or push automatically.

## Docs Integration Contract

- `$m-discuss`, `$m-plan`, and `$m-archive` must explicitly use `$m-docs` when they decide docs root, route stable docs, or change governed docs.
- `$m-quick` must explicitly use `$m-docs` to read minimum relevant current context before eligibility or editing, and again only when stable-doc impact requires a write.
- `$m-quick` must not create `intake`, `plan`, or `change` merely because it ran; it updates canonical feature, requirement, or spec docs only when stable truth changed.
- Intake, feature, requirement, spec, and decision impact must be recorded in planning and archive artifacts when relevant.
- Lesson impact and related lesson paths must be recorded in archive artifacts.
- Feature docs are the home for current user-visible behavior and full workflow descriptions; change archives are historical evidence, not the only source of current truth.
- The root-level active `plan.md` is a workflow-control exception and does not replace `docs/plan/` as an archive category.
- Docs remote configuration, push target, publication, and backup strategy are user-owned and must not be inferred by the workflow.

## Visual Output Contract

- `skills/m-autoflow/references/output-components.md` is the shared component-selection contract for the `m-autoflow` workflow family and companion utilities listed in that reference.
- `skills/m-autoflow/references/interactive-output-patterns.md` owns workflow-specific rules for official inline interaction. It links conceptually to the official `$visualize:visualize` capability but does not copy its complete HTML, design-system, or rendering instructions.
- Every covered workflow-family or companion-utility `SKILL.md` must route to that reference before composing a user-facing result. Domain-specific skills such as `m-thesis-aigc-revision` may keep a standalone output contract.
- Responses must lead with the outcome and retain a readable plain-Markdown summary.
- Tables are preferred for repeated exact mappings; Mermaid is limited to relationships whose meaning is materially clearer as a diagram.
- Inline interaction is selected only when at least one meaningful local selection, drill-down, evidence-navigation, or next-phase action would be less convenient in static output.
- `$m-discuss`, `$m-plan`, `$m-test`, and `$m-archive` are the initial explicit consumers of the interactive-output pattern reference.
- A covered phase that selects inline interaction must invoke and obey the current official `$visualize:visualize` skill by name. Distributed files must not reference a versioned plugin-cache path.
- The official thread-scoped visualization directory and inline directive contract remain runtime concerns; generated fragments are ephemeral and must not be committed to this repository.
- Local selection and presentation state remain inside the inline result. A Codex action uses `window.openai.sendFollowUpMessage` with the selected values and requested operation.
- A follow-up action is a request, not proof of approval or completion. The receiving phase must re-check its entry gate and authorization.
- Buttons use native controls and official utility classes; icons use the sandbox-provided Lucide integration and inherit accessible labels from visible text or `aria-label`.
- If `$visualize:visualize`, the host bridge, or required runtime support is unavailable, the phase emits the full Markdown result and next command without `::codex-inline-vis`.
- Inline data must exclude secrets and unrelated personal data, stay within the official size and network restrictions, and preserve a useful first render before interaction.
- Local artifact and evidence links must use absolute paths; paths with spaces must use renderer-safe link syntax.
- UI and rendered-document validation must embed one or two representative images and link additional evidence when safe.
- Line-specific code review findings may emit `::code-comment`; non-actionable or non-line-specific findings remain prose.
- Git directives may be emitted only after the corresponding action succeeds and only when the active host supports them.
- No response may duplicate the same facts across prose, table, and diagram merely for decoration.

## Sub-agent Contract

- Implementation sub-agents are allowed only in execution and heavy review phases.
- `$m-quick` uses direct main-agent implementation and does not dispatch implementation sub-agents.
- `$m-go` requires implementation sub-agents for all file edits in its approved execution scope.
- Research lanes may be used from discussion only when the user requested or the workflow needs source-backed current research and host policy permits delegation.
- Research lanes are read-only: they cannot edit code, create plans, confirm requirements, validate implementation, archive changes, merge, or clean up.
- A parallelism assessment is required on entry to execution and heavy review.
- `$m-go` must perform the parallelism assessment before dispatch and must use parallel workers for independent non-conflicting write sets when host policy permits it.
- When host policy permits and the split is safe, sub-agents should be created for qualifying parallel work.
- Delegation requires a confirmed plan and a complete context package.
- Research-only delegation requires bounded lanes, source quality expectations, and main-agent synthesis of source trust.
- Worktree creation, plan confirmation, requirements decisions, architecture decisions, conflict handling, integration, and final acceptance remain with the main agent.
- For `$m-go`, integration edits required after worker completion must also be delegated to a worker with a bounded write set.
- Research synthesis and final source trust decisions remain with the main agent.
- Host platform policy still applies; if the platform requires explicit user authorization for sub-agents, the skill must honor it.

## Validation Contract

- The `$m-context` skill must pass `tools/validate-skills.ps1 -Skill m-context` and its focused standard-library loader tests.
- The `$m-context` skill must sync through `tools/sync-skills.ps1 -Skill m-context` after validation.
- The umbrella skill must pass `tools/validate-skills.ps1 -Skill m-autoflow`.
- Each canonical phase skill must pass `tools/validate-skills.ps1 -Skill <skill-name>`.
- The `$m-go` skill must pass `tools/validate-skills.ps1 -Skill m-go`.
- The `$m-quick` skill must pass `tools/validate-skills.ps1 -Skill m-quick`.
- `tests/test_visual_output_contract.py` must verify shared-reference routing, supported component coverage, success guards, and the standalone thesis output contract.
- The same test module must verify interactive-reference routing for the four initial phases, Markdown fallback, follow-up-only action boundaries, secret protection, and the absence of versioned plugin-cache paths.
- Heavy `$m-test` must render a representative inline result, inspect desktop and narrow layouts, operate the primary selection and follow-up controls, and report screenshot evidence.
- The umbrella skill must sync through `tools/sync-skills.ps1 -Skill m-autoflow`.
- Each canonical phase skill must sync through `tools/sync-skills.ps1 -Skill <skill-name>`.
- The `$m-go` skill must sync through `tools/sync-skills.ps1 -Skill m-go`.
- The `$m-quick` skill must sync through `tools/sync-skills.ps1 -Skill m-quick`.
- Validation must happen after final source content is written.
- Stale installed copies of superseded phase names should be removed after the canonical skills sync, unless a future compatibility decision reintroduces aliases.

## Safety and Stability

- Do not implement in the main repo path when a dedicated worktree is required.
- Treat `$m-quick` as the sole explicit bounded direct-edit exception; its gate must reject multi-repo, architecture, public-contract, schema/migration, security, destructive-data, infrastructure, broad dependency, conflicting-doc, and broad-validation work.
- Do not proceed past a blocked phase.
- Do not perform web research by default during ordinary planning.
- Do not allow plan-external code changes without returning to planning.
- Do not treat change docs as stable truth for intake, features, requirements, specs, or decisions.
- Do not write governed private docs into pushable code repos unless the user selected that repo as the docs root.
- Do not add remotes, push, or choose docs backup locations without explicit user instruction.
- Do not silently choose among uncertain best-practice options.

## Performance Considerations

- Keep `SKILL.md` concise.
- Load references selectively.
- Avoid redundant scans when repository state is already known.

## Extension Points

- Add new references for lighter or heavier workflow variants without rewriting the main skill.
- Refine fast-path eligibility in `skills/m-quick/references/quick.md` without copying it into staged phase skills.
- Add future platform wrappers without changing the phase contract.
- Add future compatibility aliases only by explicit decision.

## Related Features

- [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)
- [../features/m-quick-fast-path.md](../features/m-quick-fast-path.md)

## Related Requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)
- [../requirements/m-quick-fast-path.md](../requirements/m-quick-fast-path.md)

## Related Decisions

- [../decisions/2026-07-08_m-skill-phase-naming.md](../decisions/2026-07-08_m-skill-phase-naming.md)
- [../decisions/2026-07-09_m-go-automated-execution.md](../decisions/2026-07-09_m-go-automated-execution.md)
- [../decisions/2026-07-10_m-quick-standalone-fast-path.md](../decisions/2026-07-10_m-quick-standalone-fast-path.md)

## Related Changes

- [../change/2026-07-15_interactive-skill-outputs.md](../change/2026-07-15_interactive-skill-outputs.md)
- [../change/2026-07-15_visual-output-components.md](../change/2026-07-15_visual-output-components.md)
- [../change/2026-07-13_m-context.md](../change/2026-07-13_m-context.md)
- [../change/2026-07-08_m-plan-task-table.md](../change/2026-07-08_m-plan-task-table.md)
- [../change/2026-07-08_m-test-ui-evidence.md](../change/2026-07-08_m-test-ui-evidence.md)
- [../change/2026-07-08_m-archive-default-closeout.md](../change/2026-07-08_m-archive-default-closeout.md)
- [../change/2026-07-08_m-skill-phase-rename.md](../change/2026-07-08_m-skill-phase-rename.md)
- [../change/2026-03-23_rigorous-execution-skill.md](../change/2026-03-23_rigorous-execution-skill.md)
- [../change/2026-03-23_rigorous-execution-alignment.md](../change/2026-03-23_rigorous-execution-alignment.md)
- [../change/2026-03-23_rigorous-execution-doc-priority.md](../change/2026-03-23_rigorous-execution-doc-priority.md)
- [../change/2026-03-23_rigorous-execution-invocation-policy.md](../change/2026-03-23_rigorous-execution-invocation-policy.md)
- [../change/2026-03-23_lessons-archive-lookup.md](../change/2026-03-23_lessons-archive-lookup.md)
- [../change/2026-03-24_skill-prefix-rename.md](../change/2026-03-24_skill-prefix-rename.md)
- [../change/2026-06-22_autoflow-phase-split-research.md](../change/2026-06-22_autoflow-phase-split-research.md)
- [../change/2026-06-23_autoflow-plan-execution-scope.md](../change/2026-06-23_autoflow-plan-execution-scope.md)
