# m:quick Rules

Use this reference to classify and execute the standalone `$m-quick` fast path.

## Context Lookup

Read project truth before deciding that a request is small:

1. Read project-local instructions such as `AGENTS.md` and `guide.md`.
2. Identify `project_root`, the governed `docs_root`, candidate code repositories, and the single selected target repository.
3. Explicitly use `$m-docs` in read/context mode.
4. Start with `docs/README.md`, then the nearest category `README.md`, then only matching leaf docs.
5. Route the lookup by request type:
   - user-visible behavior -> `features`
   - durable scope or boundary -> `requirements`
   - interface, schema, protocol, or implementation constraint -> `specs`
   - constraining architecture rationale -> `decisions`
   - bug, symptom, or recurring failure -> `lessons` before `change`
   - unclear original intent -> relevant `intake`
6. Summarize the constraints internally before applying the fast-path gate.

Do not scan the entire docs tree by default. Read the minimum set that can establish current behavior, constraints, ownership, known pitfalls, and acceptance.

If a docs root exists but no matching leaf doc is found, report the gap. Continue only when the request remains self-contained and unambiguous from project-local evidence. If no docs root exists, follow the same rule and do not bootstrap a docs system from `$m-quick`.

If docs conflict with each other, the request, or the implementation, fail the fast-path gate and use `$m-discuss` to resolve current truth.

## Eligibility Gate

All of these must be true:

- The user explicitly invoked `$m-quick` or clearly requested a fast direct patch.
- One target Git repository is unambiguous.
- The expected result can be stated as a small set of concrete assertions.
- The affected behavior and likely implementation location are understood after bounded inspection.
- The write set is local and does not require coordinated cross-repo changes.
- Existing uncommitted work can be preserved without guessing ownership.
- Failure and rollback are local, visible, and straightforward.
- A focused validation path exists and can finish without broad integration setup.
- Stable docs either support the request or are absent without making intent ambiguous.

File count, line count, and estimated effort are useful warning signals, not eligibility rules. A one-line authorization change can be high risk; a several-file typo correction can still be low risk.

## Automatic Escalation

Do not use the fast path when the request involves any of these:

- more than one implementation repository
- unresolved product choices or competing valid behaviors
- unclear root cause requiring open-ended investigation
- architecture or dependency-direction changes
- a new or changed public API, event, protocol, or compatibility contract
- database schema changes, migrations, backfills, or destructive data handling
- authentication, authorization, secrets, privacy, or other security boundaries
- production infrastructure, deployment, release, or environment policy
- broad dependency upgrades, lockfile churn, or platform/runtime migrations
- generated artifacts whose source or regeneration path is unclear
- changes that require a new architecture decision record
- validation that requires broad integration, security, performance, or multi-system review
- a working-tree overlap that cannot be attributed and preserved safely

Use `$m-discuss` for unclear goals, conflicting docs, product decisions, or root-cause exploration. Use `$m-plan` when the goal is clear but needs coordinated architecture, multiple tasks, a dedicated worktree, or auditable execution.

## Direct Repository Safety

Before editing:

- resolve and report the absolute target repository path
- inspect the current branch and `git status`
- inspect diffs for files already modified before touching them
- read nearby tests and local style before selecting the patch
- confirm that generated files have an understood source and regeneration command

During editing:

- modify the current checkout directly; do not create a new branch or worktree for the quick request
- use the smallest write set that meets acceptance
- preserve unrelated changes and avoid broad formatting
- validate external inputs and fail explicitly on invalid states when applicable
- stop if implementation reveals a prohibited category or expands beyond one bounded module

If eligibility changes after editing begins, stop expanding the patch. Report changed files, current validation state, the newly discovered risk, and the required staged follow-up. Revert only the agent's own isolated edits when doing so cannot affect user work.

## Validation

Run the fastest checks that directly exercise the change:

- focused unit or component tests
- syntax, type, or focused lint checks
- touched-file formatting checks
- a narrow runtime smoke test
- `git diff --check` when Git is available

For UI-impacting changes:

- start or open the actual affected application, page, preview, or story
- operate the affected user path rather than checking only initial render
- capture screenshot evidence for the acceptance state
- include the screenshot path or rendered evidence in the result
- escalate or report `Blocked` when the UI cannot be started, authenticated, or operated within the bounded quick path

Separate pre-existing failures from failures introduced by the patch. Never report skipped or unavailable checks as passed.

## Stable Docs Impact

After validation, use `$m-docs` to decide write impact:

- A bug that restores behavior already documented correctly usually has no stable-doc update.
- An intentional user-visible behavior change updates the canonical `features` doc.
- A durable scope or boundary change updates `requirements`.
- A technical contract clarification updates `specs`.
- A change requiring a new architecture decision is not eligible for `$m-quick`; escalate it.

Do not create `intake`, `plan`, or `change` records merely because `$m-quick` ran. When a stable-doc leaf is added or renamed because the canonical destination is clear, update its nearest index through `$m-docs`.

## Commit And Publication

- Do not commit by default.
- Commit only when the user requested it or project-local instructions require it.
- Do not push, publish, deploy, merge, or choose a remote/backup destination without explicit user authorization.

## Result Table

Return this table directly to the user:

```md
| Item | Result |
| --- | --- |
| Docs Context | `<paths read>` or `No governed docs found; local evidence used` |
| Fast-path Gate | Passed / Escalated / Blocked |
| Changes | `<repo and files>` or `None` |
| Validation | `<check: status; evidence>` |
| Docs Impact | None / `<updated stable-doc paths>` |
| Residual Risk | None / `<concise risk>` |
```

For escalation, add the failed gate and recommend `$m-discuss` or `$m-plan`. Do not create a staged workflow automatically unless the user asks to continue with it.
