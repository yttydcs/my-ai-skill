---
name: m-quick
description: Fast direct implementation for explicit, bounded, low-risk fixes or small requirements in one Git repository. Use when the user invokes $m-quick or explicitly asks for a minimal direct patch without the full staged workflow; first read governed project docs through $m-docs, then edit and run focused validation. Escalate ambiguous, cross-repo, architectural, contract, schema, security, migration, or otherwise high-risk work.
---

# m:quick

## Overview

Use this skill for small, uncontroversial changes whose expected result, write set, rollback, and focused validation are clear. It is a standalone fast path: the main agent may edit the selected repository's current checkout directly after the gate passes, without creating a workflow worktree or plan.

## Quick Start

- Read `references/quick.md` completely before deciding eligibility or editing.
- Read project-local instructions such as `AGENTS.md` and `guide.md`.
- Read `../m-autoflow/references/output-components.md` before presenting the quick-path result.
- Explicitly use `$m-docs` to locate `docs_root` and read the minimum relevant current docs before inspecting the implementation deeply.
- Treat explicit `$m-quick` invocation as authorization for direct edits only after the fast-path gate passes.

## Entry Gate

Proceed only when all are true:

- the requested result and acceptance check are clear
- exactly one target Git repository is selected
- the change is bounded to a small, understood module or behavior
- relevant governed docs have been read, or missing docs have been explicitly reported
- the request does not conflict with stable docs
- existing working-tree changes can be preserved safely
- rollback is local and straightforward
- focused validation can be run
- no prohibited risk category from `references/quick.md` applies

If any gate fails, do not broaden or partially implement the request. Route to `$m-discuss` when intent or options are unclear, or `$m-plan` when the requirement is clear but needs staged architecture and execution.

## Workflow

1. Identify `project_root`, `docs_root`, and the single target `code_repo`.
2. Use `$m-docs` to restore relevant feature, requirement, spec, decision, lesson, change, or intake context in the order defined by `references/quick.md`.
3. Inspect repository status and enough code to confirm the gate.
4. Report whether the fast path passed, escalated, or is blocked.
5. When passed, let the main agent apply the smallest safe edit directly in the selected current checkout.
6. Run the fastest relevant validation, including actual UI operation and screenshot evidence for UI-impacting changes.
7. Use `$m-docs` again only when stable behavior or a technical contract changed; update canonical stable docs without manufacturing workflow history.
8. Return the compact result table defined in `references/quick.md`.

## Guardrails

- Do not create a target-request branch, worktree, `plan.md`, `todo.md`, `docs/intake`, `docs/plan`, or `docs/change` by default.
- Do not dispatch implementation sub-agents; the fast path is intentionally a direct main-agent operation.
- Do not treat file count or changed-line count as a substitute for risk assessment.
- Do not overwrite, discard, or silently reformat pre-existing user changes.
- Do not call a missing, skipped, blocked, or failing validation check passed.
- Do not commit or push by default. Honor stricter project-local commit rules and require explicit permission for push or publication.
- Do not archive, merge, clean worktrees, or claim completion of a staged workflow from this skill.

## Exit Gate

End with:

| Item | Result |
| --- | --- |
| Docs Context | Paths read, or an explicit missing-context note |
| Fast-path Gate | Passed / Escalated / Blocked |
| Changes | Target repo and changed files, or none |
| Validation | Checks and evidence with honest status |
| Docs Impact | None or updated stable-doc paths |
| Residual Risk | None or a concise remaining risk |

Make docs and changed-file values clickable. For UI work, embed one or two representative acceptance screenshots and link any additional evidence. Emit Git components only when project-local instructions or the user authorized the corresponding successful action.

When escalation is required, include the concrete failed gate and the recommended next command.
