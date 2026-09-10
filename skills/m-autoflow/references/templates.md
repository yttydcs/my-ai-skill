# Templates

Use these templates as concise defaults.

## Blocking Output

```md
问题清单
- <issue 1>
- <issue 2>

阻塞：是
禁止进入下一阶段或写代码
```

## plan.md Skeleton

Use this compact default for bounded work. Fill the information required by `../../m-plan/references/planning.md`, not empty headings. Add architecture, alternative analysis, cross-repo ordering or per-task rollback details where the work needs them. Existing project formats and pipeline admission/identity fields take precedence.

```md
# Plan - <workflow-name>

## Context
- Goal / existing capability / gap / scope:
- Repo(s), branch, base, worktree, project root, docs root, phase:
- guide.md and discussion/source links (or discussion skipped with reason):
- Confirmed, rejected, deferred and open decisions:
- Approach, affected interfaces and material constraints:

## Tasks and Acceptance
| Task ID | Deliverable | Scope / reason if deferred | Files / write set | Blocked by | AC IDs / verification |
| --- | --- | --- | --- | --- | --- |
| T1 | <observable outcome> | Will execute | <paths> | none | AC-01 / <check> |

| AC ID | Source / exact requirement | Task IDs | Verification / evidence | Status |
| --- | --- | --- | --- | --- |
| AC-01 | <preserve negation, values, defaults, order, permissions> | T1 | <boundary, independent expected result> | pending |

## Shared Controls
- Risks, rollback and task-specific exceptions:
- Parallelism assessment; context package only if delegating:
- Stable-doc impact and related paths; explicitly group unaffected categories:
- Approval status / executable Task IDs / blockers:
```

Task rows are the executable checklist; update their state rather than maintaining a second list. Shared fields need not be repeated in each Task Block. Keep acceptance definitions here and reference their IDs elsewhere.

## Task Block

```md
##### <Task ID> - <Title>
- Owner:
- Worktree:
- Plan Path:
- Goal:
- Deliverable:
- Blocked by: <Task IDs or none; genuine prerequisites only>
- Files / Modules:
- Write Set:
- Acceptance: <AC IDs; definitions live in the acceptance map>
- Verification: <independently observable behavior and how to check it>
- Test Points: <existing interface/boundary, independent expected outcome>
- Rollback:
```

## Plan Task Summary Table

Use this table in the direct `$m-plan` response after creating or confirming the active `plan.md` / `todo.md`.

```md
| Task ID | Title | Scope | Files / Modules | Acceptance / Tests | Risk / Notes |
| --- | --- | --- | --- | --- | --- |
| <Task ID> | <short title> | Will execute / Will not execute now | <paths or modules> | <short acceptance or test cue> | <risk, blocker, or deferral reason> |
```

## docs/change Skeleton

Cover `../../m-archive/references/archive.md` using these compact sections. Link the durable authoritative acceptance record; do not copy its complete map/logs. Omit sub-agent details when no delegation occurred. Create a lesson only when reusable knowledge warrants one.

```md
# YYYY-MM-DD_<topic>

## Result
- Goal, completed Task IDs, behavior changes and deviations from plan:
- Durable plan link / docs root:
- Material decisions, impact and rollback:

## Evidence
- Durable authoritative acceptance/review record:
- Validation summary, Requirements / Standards verdicts, candidate/plan identity reference:
- Unverified or waived items, authority and residual risks:

## Documentation
- Changed categories and related paths / index updates:
- Unaffected categories: <explicit category names>: none
- Lessons: <link, or none with reason>
- Sub-agent trace: <only if delegated; durable trace link is sufficient>

## Closeout
- Per-repo commit / merge / cleanup status:
- Remaining local state, unpushed changes and unresolved items:
```

## docs/lessons Skeleton

```md
# <lesson-topic>

## Summary
## Lookup Hints
## Symptoms
## Impact
## Trigger Conditions
## Root Cause
## Investigation Trail
## Resolution
## Prevention / Guardrails
## Related Docs
```
