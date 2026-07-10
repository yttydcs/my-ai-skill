# m:quick Skill Specification

## Scope

Define the package, invocation, docs-context, eligibility, direct-edit, validation, escalation, and installation contracts for the standalone `$m-quick` fast path.

## Package Contract

- Source package: `skills/m-quick`
- Skill entry: `skills/m-quick/SKILL.md`
- Detailed rules: `skills/m-quick/references/quick.md`
- UI metadata: `skills/m-quick/agents/openai.yaml`
- Install metadata: `manifests/m-quick.json`
- Install flow: source -> `dist/codex/m-quick` -> `C:\Users\HelloWorld\.codex\skills\m-quick`
- Dependencies: `m-autoflow` collection and `m-docs`
- No scripts, assets, examples, or package README are required.

## Trigger Contract

- Trigger on explicit `$m-quick` invocation or an explicit request for a minimal direct patch without the full staged workflow.
- Metadata must describe both eligible low-risk work and the major escalation categories.
- Do not position `$m-quick` as a general default for all small-looking requests.

## Docs Context Contract

Before eligibility or implementation:

1. Read project-local instructions.
2. Resolve `project_root`, governed `docs_root`, and one target `code_repo`.
3. Explicitly invoke `$m-docs` in read/context mode.
4. Read `docs/README.md`, the nearest category index, and only matching leaf docs.
5. Route behavior to `features`, boundaries to `requirements`, contracts to `specs`, constraints to `decisions`, symptoms to `lessons` before `change`, and unclear source intent to `intake`.

Missing docs must be reported. Conflicting docs fail the gate. `$m-quick` must not bootstrap a docs tree.

## Eligibility Contract

The command requires:

- one target Git repository
- clear acceptance assertions
- bounded, understood ownership and write set
- safely preservable working-tree state
- local rollback
- focused validation
- no stable-doc conflict

Automatic escalation includes multi-repo, ambiguous root cause, architecture, dependency direction, public interfaces/protocols, schema/migration/backfill, authentication/authorization/security, destructive data, production infrastructure/deployment, broad dependency/runtime migration, unclear generated sources, new ADR needs, and broad integration/security/performance validation.

Counts of files, lines, or estimated duration are advisory signals only.

## Direct Edit Contract

- The main agent performs implementation directly in the selected current checkout.
- Do not create a branch, worktree, plan, or workflow archive for the target request by default.
- Inspect branch, Git status, target-file diffs, nearby tests, and generation ownership before editing.
- Preserve unrelated work and avoid broad formatting.
- Stop expansion when implementation invalidates eligibility.
- Do not dispatch implementation sub-agents.

## Validation Contract

- Run the fastest checks that directly exercise the change.
- Include `git diff --check` when Git is available.
- Separate pre-existing failures from introduced failures.
- For UI-impacting changes, open the actual UI, operate the affected path, and capture screenshot evidence.
- Missing required UI evidence yields `Blocked` or escalation, never pass.

## Stable Docs Write Contract

- Use `$m-docs` after validation only when current stable truth changed.
- Restore documented behavior without unnecessary stable-doc edits.
- Update feature behavior, durable requirements, or technical specs at their canonical locations when intentionally changed.
- Escalate changes that require a new architecture decision.
- Do not create `intake`, `plan`, or `change` solely because `$m-quick` ran.
- Update the nearest index when a stable leaf is added, renamed, or moved.

## Result Contract

The direct response must contain rows for:

- Docs Context
- Fast-path Gate
- Changes
- Validation
- Docs Impact
- Residual Risk

Escalated or blocked results must identify the failed gate and recommend `$m-discuss` or `$m-plan`.

## m-autoflow Integration Contract

- `$m-quick` is an alternate standalone route, not a discuss/plan/execute/test/archive phase.
- The default staged order is unchanged.
- Staged worktree, plan, mandatory archive, merge, and cleanup rules remain strict.
- Umbrella documentation and guardrails must identify `$m-quick` as the sole bounded direct-edit exception.
- `$m-quick` ends after validation and reporting; it does not enter archive automatically.

## Commit And Publication Contract

- Do not commit by default unless project-local instructions require it or the user asks.
- Never infer authorization to push, publish, deploy, merge, or select backup/remotes.

## Validation And Installation Contract

- `tools/validate-skills.ps1 -Skill m-quick` must pass.
- `manifests/m-quick.json` must parse as JSON.
- `tools/sync-skills.ps1 -Skill m-quick` must succeed.
- Installed source files must match repository source files, excluding generated `.build-info.json`.
- Changed umbrella packages must also validate and sync.

## Error Handling

- Fail closed on ambiguous repository selection, conflicting docs, prohibited risk, unsafe overlap, or unavailable required evidence.
- Report missing context rather than inventing requirements.
- Report skipped, blocked, and failing checks honestly.
- Do not revert user work when eligibility changes after editing begins.

## Performance Constraints

- Read indexes and matching leaves rather than the entire docs tree.
- Keep `SKILL.md` concise and detailed rules in one reference.
- Avoid deterministic eligibility scripts because engineering risk classification is contextual.

## Related Features

- [m-quick-fast-path.md](../features/m-quick-fast-path.md)

## Related Requirements

- [m-quick-fast-path.md](../requirements/m-quick-fast-path.md)

## Related Decisions

- [2026-07-10_m-quick-standalone-fast-path.md](../decisions/2026-07-10_m-quick-standalone-fast-path.md)

## Related Changes

- [2026-07-10_m-quick-fast-path.md](../change/2026-07-10_m-quick-fast-path.md)

## Related Lessons

- [windows-skill-parity-line-endings.md](../lessons/windows-skill-parity-line-endings.md)
