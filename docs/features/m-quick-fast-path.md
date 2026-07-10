# m:quick Fast Path

## Status

Current.

## Goal

Resolve explicit, bounded, low-risk fixes and small requirements in one Git repository without paying the setup and archive cost of the full staged workflow, while restoring relevant project context from governed docs before editing.

## Non-goals

- Replace `$m-autoflow` for ambiguous, architectural, cross-repo, security-sensitive, contract-changing, or otherwise high-risk work.
- Skip focused validation or conceal missing evidence.
- Create worktrees, plans, intake records, change archives, commits, or pushes for every quick request.
- Duplicate the `$m-docs` taxonomy inside the command.

## Actors

- User: explicitly selects the fast path and owns push, publication, deployment, and backup decisions.
- Main Codex agent: restores docs context, evaluates eligibility, edits the selected repo, validates the result, and reports residual risk.
- `$m-docs`: locates the governed docs root, routes contextual reading, and governs stable-doc updates when current truth changes.

## Entry Point

Invoke `$m-quick` with a concrete small change, for example a localized bug fix, explicit validation adjustment, copy correction, or bounded UI behavior change.

The invocation authorizes direct edits only after the fast-path gate passes. It does not authorize push, publication, deployment, destructive data work, or an automatic staged workflow.

## Context Restoration

Before deciding that the work is quick, the agent:

1. reads project-local instructions
2. identifies `project_root`, `docs_root`, and one target code repository
3. explicitly uses `$m-docs`
4. reads `docs/README.md`, the nearest category index, and only relevant leaf docs
5. prioritizes `features`, `requirements`, `specs`, and constraining `decisions`
6. starts bug and recurring-symptom lookup from `lessons`, then uses `change` only when needed
7. reads `intake` only when original intent is unclear

The command reports missing docs. It may continue without a docs root or matching leaf only when local evidence keeps the request self-contained and unambiguous. Conflicting docs force escalation to `$m-discuss`.

## Eligibility

The fast path requires:

- one unambiguous target Git repository
- a clear expected result and focused acceptance check
- a bounded, understood module and write set
- safe preservation of current working-tree changes
- local, straightforward rollback
- available focused validation
- no conflict with stable docs

It rejects:

- multi-repo coordination
- unresolved product or root-cause questions
- architecture or dependency-direction changes
- public API, protocol, schema, migration, or compatibility changes
- authentication, authorization, secrets, privacy, or other security boundaries
- destructive data handling, production infrastructure, deployment policy, or broad dependency upgrades
- work requiring a new architecture decision
- work needing broad integration, performance, or security review

File and line counts are warning signals rather than hard thresholds.

## Direct Change Workflow

1. Inspect the selected repo's branch, Git status, relevant code, tests, and pre-existing diffs.
2. Report whether the gate passed, escalated, or is blocked.
3. When passed, edit the current checkout directly; do not create a quick-request branch, worktree, or root plan.
4. Apply the smallest safe change and preserve unrelated work.
5. Stop expanding if implementation reveals a prohibited risk or wider ownership boundary.
6. Run focused validation.
7. Check stable-doc impact through `$m-docs`.
8. Return the direct result table.

The main agent performs the edit without implementation sub-agents. This keeps the quick path low overhead and distinguishes it from `$m-go`.

## Validation

Run the fastest checks that directly exercise the change, such as focused tests, syntax/type/lint checks, a narrow runtime smoke test, and `git diff --check`.

For UI-impacting changes, open the actual UI, operate the affected path, capture screenshot evidence, and report the evidence path. If the UI cannot be operated within the bounded fast path, the result is blocked or escalated rather than passed.

Pre-existing validation failures must be separated from failures introduced by the patch. Skipped or unavailable checks are never reported as passed.

## Docs Impact

- Restoring behavior already described correctly: normally no stable-doc edit.
- Intentional user-visible behavior change: update the canonical feature dossier.
- Durable scope or boundary change: update requirements.
- Technical contract clarification: update specs.
- Need for a new architecture decision: leave the fast path and use the staged workflow.

`$m-quick` does not create `intake`, `plan`, or `change` merely because it ran. New or renamed stable-doc leaves still require their nearest index to be updated through `$m-docs`.

## Commit And Closeout

The command does not commit or push by default. Project-local rules may require a commit; push, publication, deployment, merge, and backup destinations always require explicit authorization.

The command does not call `$m-archive`, merge branches, or clean worktrees. It ends after direct validation and reporting.

## Result Table

The direct response contains:

| Item | Meaning |
| --- | --- |
| Docs Context | Relevant paths read or an explicit missing-context note |
| Fast-path Gate | Passed, Escalated, or Blocked |
| Changes | Target repo and files, or none |
| Validation | Checks, status, and evidence |
| Docs Impact | None or updated stable-doc paths |
| Residual Risk | Remaining risk or none |

## Acceptance Scenarios

### Restore Documented Behavior

Given one repo contains a localized bug and the feature docs already describe the intended behavior, when `$m-quick` runs, then it reads those docs, fixes the current checkout, runs focused validation, and reports no stable-doc update.

### Small Intentional Behavior Change

Given a bounded behavior change has clear acceptance and no prohibited risk, when `$m-quick` runs, then it edits directly, validates the result, and updates the canonical stable doc through `$m-docs`.

### Docs Conflict

Given stable docs conflict with the request or each other, when `$m-quick` evaluates eligibility, then it performs no expanding implementation and routes to `$m-discuss` with the conflict.

### High-risk Request

Given a request touches several repos, a schema, security boundary, public contract, architecture decision, or broad integration path, when `$m-quick` evaluates eligibility, then it routes to `$m-plan` before implementation.

### Missing Docs

Given no governed docs or matching leaf exists, when the change is still unambiguous and self-contained from local evidence, then `$m-quick` may continue while reporting the gap; otherwise it escalates.

### Existing User Changes

Given the target working tree is dirty, when unrelated changes can be preserved safely, then `$m-quick` works around them; when ownership or overlap is ambiguous, it blocks instead of overwriting them.

### UI Change

Given an eligible bounded UI change, when validation runs, then the actual UI path is opened and operated and screenshot evidence is included; unavailable evidence cannot produce a pass.

## Cross-repo Ownership

- Skill source and stable docs: `D:\project\my-ai-skills`
- Installed local copy: `C:\Users\HelloWorld\.codex\skills\m-quick`
- Target project repositories: selected at invocation; only one may be modified by a single fast-path run.

## Related Intake

- [2026-07-10_m-quick-fast-path.md](../intake/2026-07-10_m-quick-fast-path.md)

## Related Requirements

- [m-quick-fast-path.md](../requirements/m-quick-fast-path.md)

## Related Specs

- [m-quick-skill.md](../specs/m-quick-skill.md)

## Related Decisions

- [2026-07-10_m-quick-standalone-fast-path.md](../decisions/2026-07-10_m-quick-standalone-fast-path.md)

## Related Changes

- To be added during archive.

## Related Lessons

- [skill-frontmatter-yaml-colon.md](../lessons/skill-frontmatter-yaml-colon.md)
