# m:autoflow Skill Spec

## Architecture Overview

The skill is packaged as `skills/m-autoflow` and kept intentionally small. Detailed operational rules live in `references/` so the main `SKILL.md` remains trigger-friendly and efficient.

## Package Contract

- Source package: `skills/m-autoflow`
- UI metadata: `skills/m-autoflow/agents/openai.yaml`
- Install metadata: `manifests/m-autoflow.json`
- Companion source packages:
  - `skills/m-autoflow-plan`
  - `skills/m-autoflow-execute`
  - `skills/m-autoflow-test`
  - `skills/m-autoflow-archive`
  - `skills/m-autoflow-research`
- Companion install metadata:
  - `manifests/m-autoflow-plan.json`
  - `manifests/m-autoflow-execute.json`
  - `manifests/m-autoflow-test.json`
  - `manifests/m-autoflow-archive.json`
  - `manifests/m-autoflow-research.json`
- Install flow:
  - source -> `dist/codex/<skill-name>` -> `C:\Users\HelloWorld\.codex\skills\<skill-name>`

## Trigger Contract

The skill supports explicit invocation and does not forbid host-side implicit selection in its metadata.

- Invoke it explicitly as `$m-autoflow` when deterministic routing matters.
- Use `$m-autoflow` as the umbrella entry point when the whole workflow is requested.
- Use companion entries for split-phase work:
  - `$m-autoflow-research` for optional explicit-request online research
  - `$m-autoflow-plan` for initialization, requirements, architecture, and `plan.md` / `todo.md`
  - `$m-autoflow-execute` for confirmed Task ID implementation plus lightweight validation
  - `$m-autoflow-test` for optional heavy validation and review
  - `$m-autoflow-archive` for change archive, lessons, and workflow closeout
- `$m-autoflow-research` must not run by default during normal planning; it requires an explicit user request for web research, current external facts, or source-backed investigation.
- `skills/m-autoflow/agents/openai.yaml` must not set:
  - `policy.allow_implicit_invocation: false`
- `manifests/m-autoflow.json` must not declare:
  - `manual_invocation_only: true`

## Workflow Contract

- Initialization precedes stage `1`.
- Stage order is fixed:
  - optional explicit-request research before or during planning
  - `1. requirements`
  - `2. architecture`
  - `3.1 plan`
  - `3.2 implementation`
  - `3.3 review`
  - `4. archive`
- Only one stage may be active at a time.
- Any rollback must state the reason and update the affected documents.
- Stage `1` prioritizes relevant docs under `docs/requirements` when they exist.
- Stage `2` prioritizes relevant docs under `docs/specs` when they exist.
- Optional research is read-only and may feed only verified, cited findings into requirements, architecture, `plan.md`, or stable docs.
- Active workflow control stays in the worktree root as `plan.md` or `todo.md`.
- Stage `3.1` plan artifacts must include an execution scope split with `Will Execute` and `Will Not Execute Now` groups. Every known Task ID must appear in exactly one group, and non-executed tasks must include the reason.
- Stage `3.2` owns lightweight local validation such as syntax checks, type checks, focused lint, touched-file formatting checks, focused unit tests, and `git diff --check`.
- Stage `3.3` is optional heavy validation. It may be skipped for low-risk small changes when execution-stage validation is sufficient and the skip reason plus residual risk are recorded.
- When stage `3.3` runs, it must cover integration or end-to-end flow, usability, security boundaries, and performance indicators when applicable.
- `docs/change/YYYY-MM-DD_topic.md` is required before a workflow counts as complete.
- Stage `4` must record `Lessons impact`, `Related lessons`, and searchable lesson cues in the archive.
- Stage `4` must create or update `docs/lessons` when the workflow exposed reusable troubleshooting knowledge.
- After stage `4`, the workflow must ask whether to end.
- If the user confirms workflow end, merge and worktree cleanup happen from the repo control-plane only.
- If stage `4` produced lessons docs or lesson-index updates, workflow end must carry them back into the global docs tree.
- Merge and worktree cleanup are forbidden until the user confirms workflow end.

## Docs Integration Contract

- Stage `3.1` must explicitly use `$m-docs`.
- Stage `4` must explicitly use `$m-docs`.
- `$m-autoflow-research` must explicitly use `$m-docs` when external research changes stable project truth.
- Requirement/spec impact must be recorded in planning and archive artifacts.
- Lesson impact and related lesson paths must be recorded in archive artifacts.
- The root-level active `plan.md` is a workflow-control exception and does not replace `docs/plan/` as an archive category.

## Sub-agent Contract

- Sub-agents are allowed only in `3.2` and `3.3`.
- Exception: `$m-autoflow-research` may use read-only research sub-agents before or during planning when the user explicitly asks for web research and host policy permits delegation.
- The research exception does not allow code edits, worktree changes, plan confirmation, implementation, validation, archive, merge, or cleanup delegation.
- A parallelism assessment is required on entry to `3.2` and `3.3`.
- When host policy permits and the split is safe, sub-agents should be created for qualifying parallel work.
- Delegation requires a confirmed plan and a complete context package.
- Research-only delegation requires an explicit web-research request, bounded read-only lanes, source quality expectations, and main-agent synthesis of source trust.
- Worktree creation, plan confirmation, requirements decisions, architecture decisions, conflict handling, integration, and final acceptance remain with the main agent.
- Research synthesis and final source trust decisions remain with the main agent.
- Host platform policy still applies; if the platform requires explicit user authorization for sub-agents, the skill must honor it.

## Validation Contract

- The skill must pass `tools/validate-skills.ps1 -Skill m-autoflow`.
- Each companion skill must pass `tools/validate-skills.ps1 -Skill <companion-skill>`.
- The skill must sync through `tools/sync-skills.ps1 -Skill m-autoflow`.
- Each companion skill must sync through `tools/sync-skills.ps1 -Skill <companion-skill>`.
- Validation must happen after the final skill content is written.

## Safety and Stability

- Do not implement in the main repo path.
- Do not proceed past a blocked stage.
- Do not perform web research by default during ordinary planning.
- Do not allow plan-external code changes without returning to `3.1`.
- Do not treat change docs as stable truth for requirements or specs.
- Do not silently choose among uncertain best-practice options.

## Performance Considerations

- Keep `SKILL.md` concise.
- Load references selectively.
- Avoid redundant scans when repository state is already known.

## Extension Points

- Add new references for lighter or heavier workflow variants without rewriting the main skill.
- Add future platform wrappers without changing the core references model.
- Add future companion phase skills when a workflow stage needs a separately invokable surface.

## Related Requirements

- [../requirements/m-autoflow-skill.md](../requirements/m-autoflow-skill.md)

## Related Changes

- [../change/2026-03-23_rigorous-execution-skill.md](../change/2026-03-23_rigorous-execution-skill.md)
- [../change/2026-03-23_rigorous-execution-alignment.md](../change/2026-03-23_rigorous-execution-alignment.md)
- [../change/2026-03-23_rigorous-execution-doc-priority.md](../change/2026-03-23_rigorous-execution-doc-priority.md)
- [../change/2026-03-23_rigorous-execution-invocation-policy.md](../change/2026-03-23_rigorous-execution-invocation-policy.md)
- [../change/2026-03-23_lessons-archive-lookup.md](../change/2026-03-23_lessons-archive-lookup.md)
- [../change/2026-03-24_skill-prefix-rename.md](../change/2026-03-24_skill-prefix-rename.md)
- [../change/2026-06-22_autoflow-phase-split-research.md](../change/2026-06-22_autoflow-phase-split-research.md)
- [../change/2026-06-23_autoflow-plan-execution-scope.md](../change/2026-06-23_autoflow-plan-execution-scope.md)
