# m:autoflow Workflow Skill Spec

## Architecture Overview

`m-autoflow` is the umbrella entry point and shared reference host for a focused workflow skill family. Phase-specific behavior lives in short, separately invokable skills so the user can call only the stage they need.

## Package Contract

- Umbrella source package: `skills/m-autoflow`
- Umbrella UI metadata: `skills/m-autoflow/agents/openai.yaml`
- Umbrella install metadata: `manifests/m-autoflow.json`
- Canonical phase source packages:
  - `skills/m-discuss`
  - `skills/m-plan`
  - `skills/m-execute`
  - `skills/m-test`
  - `skills/m-archive`
- Canonical phase install metadata:
  - `manifests/m-discuss.json`
  - `manifests/m-plan.json`
  - `manifests/m-execute.json`
  - `manifests/m-test.json`
  - `manifests/m-archive.json`
- Install flow:
  - source -> `dist/codex/<skill-name>` -> `C:\Users\HelloWorld\.codex\skills\<skill-name>`
- Historical archives may mention older phase names as source evidence, but current source packages, manifests, and stable contracts must use the canonical phase names above.

## Trigger Contract

The skill family supports explicit invocation and does not forbid host-side implicit selection in metadata.

- Invoke `$m-autoflow` when the user wants the full workflow or wants the umbrella to choose the next phase.
- Invoke `$m-discuss` for discovery, requirement shaping, brainstorming, optional research, and early worktree setup.
- Invoke `$m-plan` for architecture, executable planning, and approval gating.
- Invoke `$m-execute` for confirmed Task ID implementation plus lightweight validation.
- Invoke `$m-test` for optional heavy validation and review.
- Invoke `$m-archive` for change archive, lessons, and workflow closeout.
- Web research must be initiated from `$m-discuss` only when current external facts, best-practice comparison, explicit user request, or source-backed investigation is needed.
- `skills/m-autoflow/agents/openai.yaml` must not set:
  - `policy.allow_implicit_invocation: false`
- `manifests/m-autoflow.json` must not declare:
  - `manual_invocation_only: true`

## Workflow Contract

- Default phase order:
  - `discuss`
  - `plan`
  - `execute`
  - optional `test`
  - `archive`
- Direct plan invocation is allowed only when the plan records why discussion was skipped or already satisfied.
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
- Planning artifacts must include an execution-scope split with `Will Execute` and `Will Not Execute Now` groups. Every known Task ID must appear in exactly one group, and non-executed tasks must include the reason.
- Execution owns lightweight local validation such as syntax checks, type checks, focused lint, touched-file formatting checks, focused unit tests, and `git diff --check`.
- Heavy validation is optional. It may be skipped for low-risk small changes when execution-stage validation is sufficient and the skip reason plus residual risk are recorded.
- When heavy validation runs, it must cover integration or end-to-end flow, usability, security boundaries, and performance indicators when applicable.
- `docs/change/YYYY-MM-DD_topic.md` is required before a workflow counts as complete.
- The change archive belongs in the selected governed docs root when a private docs root exists.
- Archive must record `Lessons impact`, `Related lessons`, and searchable lesson cues.
- Archive must create or update `docs/lessons` when the workflow exposed reusable troubleshooting knowledge.
- After archive, the workflow must close by default through repo control-plane merge and worktree cleanup.
- If the user explicitly requests archive-only handling, no merge, no cleanup, or an equivalent pause, the workflow must stop after archive readiness and report retained branch/worktree state.
- If archive produced lessons docs or lesson-index updates, workflow end must carry them back into the global docs tree.
- Merge and worktree cleanup are forbidden until archive completion, status verification, and unrelated-dirt preservation checks pass.

## Docs Integration Contract

- `$m-discuss`, `$m-plan`, and `$m-archive` must explicitly use `$m-docs` when they decide docs root, route stable docs, or change governed docs.
- Intake, feature, requirement, spec, and decision impact must be recorded in planning and archive artifacts when relevant.
- Lesson impact and related lesson paths must be recorded in archive artifacts.
- Feature docs are the home for current user-visible behavior and full workflow descriptions; change archives are historical evidence, not the only source of current truth.
- The root-level active `plan.md` is a workflow-control exception and does not replace `docs/plan/` as an archive category.
- Docs remote configuration, push target, publication, and backup strategy are user-owned and must not be inferred by the workflow.

## Sub-agent Contract

- Implementation sub-agents are allowed only in execution and heavy review phases.
- Research lanes may be used from discussion only when the user requested or the workflow needs source-backed current research and host policy permits delegation.
- Research lanes are read-only: they cannot edit code, create plans, confirm requirements, validate implementation, archive changes, merge, or clean up.
- A parallelism assessment is required on entry to execution and heavy review.
- When host policy permits and the split is safe, sub-agents should be created for qualifying parallel work.
- Delegation requires a confirmed plan and a complete context package.
- Research-only delegation requires bounded lanes, source quality expectations, and main-agent synthesis of source trust.
- Worktree creation, plan confirmation, requirements decisions, architecture decisions, conflict handling, integration, and final acceptance remain with the main agent.
- Research synthesis and final source trust decisions remain with the main agent.
- Host platform policy still applies; if the platform requires explicit user authorization for sub-agents, the skill must honor it.

## Validation Contract

- The umbrella skill must pass `tools/validate-skills.ps1 -Skill m-autoflow`.
- Each canonical phase skill must pass `tools/validate-skills.ps1 -Skill <skill-name>`.
- The umbrella skill must sync through `tools/sync-skills.ps1 -Skill m-autoflow`.
- Each canonical phase skill must sync through `tools/sync-skills.ps1 -Skill <skill-name>`.
- Validation must happen after final source content is written.
- Stale installed copies of superseded phase names should be removed after the canonical skills sync, unless a future compatibility decision reintroduces aliases.

## Safety and Stability

- Do not implement in the main repo path when a dedicated worktree is required.
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
- Add future platform wrappers without changing the phase contract.
- Add future compatibility aliases only by explicit decision.

## Related Features

- [../features/m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related Decisions

- [../decisions/2026-07-08_m-skill-phase-naming.md](../decisions/2026-07-08_m-skill-phase-naming.md)

## Related Changes

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
