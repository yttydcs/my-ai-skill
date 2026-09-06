# Plan - Acceptance and review handoffs

## Workflow Information
- Repo / Project Root: D:/project/my-ai-skills
- Branch: codex/acceptance-review
- Base: main at eceea63
- Worktree: D:/project/my-ai-skills/worktrees/acceptance-review
- Docs Root: D:/project/my-ai-skills/worktrees/acceptance-review/docs (retained in the repository docs tree after closeout)
- Code Repos: this repository only
- Current Stage: implementation and validation complete; archive and local closeout in progress
- Authority: the user approved the concrete proposal with "好的请继续" on 2026-09-06. No repeated implementation approval is needed within this scope.
- Discussion: completed in the current conversation; repository and upstream skill review established the proposal.

## Goal and Scope
Keep the existing discuss -> plan -> execute -> optional heavy test -> archive entries. Make confirmed requirements traceable to acceptance and evidence, favor independently verifiable task slices, and keep a lightweight requirements/standards review even when heavy testing is skipped.

Preserve explicit one-question Grill Mode, plan approval, private docs, existing execution authority, and archive closeout. Do not add a glossary system, change stage names, refactor m-pipeline, mandate TDD for every change, force commits for review, or add an outer scheduling loop.

## Acceptance
| ID | Confirmed requirement / source | Tasks | Evidence | Status |
| --- | --- | --- | --- | --- |
| AC-01 | Approved proposal: preserve confirmed, rejected, deferred and open decisions; carry negative, numeric, default and ordering constraints into acceptance | T1 | Independent save-dialog-plan evaluation; source review | passed |
| AC-02 | Approved proposal: each task declares a deliverable, genuine blockers and independent verification; allow compatibility/migration exceptions | T1 | save-dialog-plan evaluation; migration wording reconciled across source and stable docs | passed |
| AC-03 | Approved proposal: separate requirements and standards review from optional heavy testing; explicit waivers are not passes | T2 | heavy-skip-dirty-review evaluation; package routing tests; continuation exit-rule review | passed |
| AC-04 | Approved proposal: review committed, staged, unstaged and untracked workflow-owned changes without altering unrelated work | T2 | Documented Git recipe executed in temporary repositories; coverage and unchanged-state tests passed | passed |
| AC-05 | Approved proposal: bind review/evidence to plan and candidate state; changes invalidate affected evidence and archive reuses valid results | T1, T2 | changed-limit-resume evaluation; candidate/plan identities retained in change record | passed |
| AC-06 | Approved proposal: discover facts; decide reversible in-scope choices; block only material unknowns or missing execution prerequisites; preserve all existing entry gates | T1, T2 | approved-reversible-choice evaluation; existing Grill Mode and continuation contract tests | passed |
| AC-07 | Approved proposal and repository packaging contract: update stable docs, package references, validate, sync installed copies and archive | T3, T4, T5 | 69 tests passed, 2 environment skips; 8 valid packages / 33 matching source-dist-install files; local closeout pending | pending |

## Execution Scope After Approval
- Will Execute: T1, T2, T3, T4, T5.
- Will Not Execute Now: none. Exclusions are recorded in Goal and Scope, not silently scheduled.

## Task Details
### T1 - Preserve requirements through independently verifiable tasks
- Owner: main agent.
- Deliverable: discuss/plan handoffs retain exact constraints and AC identifiers with bounded behavior slices.
- Files / Write Set: skills/m-discuss; skills/m-plan; skills/m-autoflow/SKILL.md and references/stages.md, templates.md, subagents.md; manifests for these changed packages.
- Blocked by: none.
- Acceptance: AC-01, AC-02, AC-05, AC-06.
- Test Points: static routing/package checks plus independent raw-input scenario evaluations; no implementation-mirroring assertions.
- Rollback: revert this task's commit and resync the affected packages.

### T2 - Review actual candidate changes and reuse current evidence
- Owner: main agent.
- Deliverable: execute produces separate requirements/standards results; test and archive check freshness and explicit skips.
- Files / Write Set: new skills/m-autoflow/references/review.md; skills/m-execute, m-test, m-archive, m-go, m-continue; their changed manifests. Coordinate shared template/umbrella edits with T1 in the main agent.
- Blocked by: T1 acceptance contract.
- Acceptance: AC-03, AC-04, AC-05, AC-06.
- Test Points: temporary Git repo with committed/staged/unstaged/untracked changes; dirty evidence and plan changes; heavy-test skip case.
- Rollback: revert this task's commit and resync affected packages.

### T3 - Align stable documentation
- Owner: bounded documentation worker after execution admission.
- Deliverable: current feature, requirements and spec docs explain the approved behavior consistently.
- Files / Write Set: docs/features/m-autoflow-workflow.md; docs/requirements/m-autoflow-skill.md; docs/specs/m-autoflow-skill.md.
- Blocked by: confirmed proposal; reconcile against final T1/T2 output before acceptance.
- Acceptance: AC-07 plus accurate descriptions of AC-01 through AC-06.
- Test Points: main-agent semantic review and existing documentation tests.
- Rollback: revert this task's commit.

### T4 - Verify behavior and synchronize packages
- Owner: main agent, with an independent read-only evaluator after implementation.
- Deliverable: focused meaningful packaging checks, reusable behavior fixtures and actual evaluation evidence; installed skills match validated source.
- Files / Write Set: tests/test_m_acceptance_review_contract.py; tests/fixtures/acceptance-review/; necessary updates to existing contract tests; ignored dist and installed affected skill directories.
- Blocked by: T1, T2, T3.
- Acceptance: AC-01 through AC-07.
- Test Points: full unittest discovery; skill validation; isolated Git checks; independent evaluation; source/dist/install parity.
- Rollback: revert test changes; restore and resync prior skill source.

### T5 - Archive and close out
- Owner: main agent only.
- Deliverable: intake, retained plan and change archive with actual checks; local commits merged and dedicated worktree cleaned.
- Files / Write Set: docs/intake/2026-09-06_acceptance-review.md and index; docs/plan/2026-09-06_acceptance-review.md and index; docs/change/2026-09-06_acceptance-review.md and index; lessons only if new reusable evidence warrants one.
- Blocked by: T4 passing or explicit residual-risk disposition.
- Acceptance: AC-07.
- Test Points: archive link/status review, clean local main and installed parity; no push.
- Rollback: preserve worktree on closeout failure; revert workflow-owned commits when requested.

## Docs Governance
- Intake impact: add.
- Feature / Requirements / Specs impact: clarify and add the approved handoff/review behavior in existing stable leaves.
- Decision impact: none; preserve established phase and Grill Mode decisions. Operational rationale belongs in this plan/change record.
- Lessons impact: add dirty-worktree-review.md from the executable Git reproduction; existing unittest discovery, Windows parity and symlink privilege lessons reused.
- Related intake: docs/intake/2026-09-06_acceptance-review.md.
- Related stable docs: docs/features/m-autoflow-workflow.md; docs/requirements/m-autoflow-skill.md; docs/specs/m-autoflow-skill.md.
- Related decision: docs/decisions/2026-07-20_m-discuss-grill-mode.md.

## Risks and Parallelism
- Main owns coupled phase/reference contracts. A documentation worker can independently update the three stable leaves under the fixed approved proposal, then main reconciles them against final source.
- Independent evaluation runs only after implementation, with raw fixtures and no expected answers in the evaluator prompt.
- Host and m-autoflow stage 3.2/3.3 rules permit these bounded delegations; no planning, decisions, archive or cleanup are delegated.
- Prompt behavior remains model-dependent: text checks cannot prove compliance; record actual scenario evidence and limits.
- Git review must distinguish workflow changes from pre-existing dirt. Snapshot metadata must not copy secret context or unrelated file bodies.
- Do not broaden this task into a runtime validator or pipeline migration.

## Execution Results

| Task | Status | Result |
| --- | --- | --- |
| T1 | complete | Exact source constraints, acceptance mapping and independently verifiable slices implemented |
| T2 | complete | Shared lightweight review and freshness rules routed through all five consumers |
| T3 | complete | Feature, requirements and spec leaves updated; migration exception reconciled by main |
| T4 | complete | Full suite 69 passed / 2 skipped; final affected checks 9 passed; 4 independent decision scenarios; 8 packages validated and installed with exact 33-file parity |
| T5 | in progress | Intake and retained evidence prepared; archive, merge and cleanup status tracked below |

Requirements review: passed for AC-01 through AC-06 and the completed portions of AC-07. Standards review: passed; no open in-scope findings. The final review corrected an overstrict migration statement, a list indentation issue, and the legacy continuation rule that could confuse a heavy-test skip with acceptance disposition.

Implementation commit: `636e8b7cfb1f9b7d9e52a399e612c8070bfeabcb`. It has the same 33-file content identity as the dirty candidate reviewed before commit. Original approved plan: `d61dbc4d2e75c9bf9d63e3e96125e333ab674911:plan.md`. Goal, acceptance definitions, execution scope and Task definitions remain unchanged; status/evidence and the planned lessons decision were updated.

The independent evaluator received raw scenario packets and current skills without expected answers or parent conversation. Its outputs are decision/plan evaluations, not live product end-to-end tests. Windows symlink tests remain visibly skipped; no skip or waiver was reported as passed. See the [change record](../change/2026-09-06_acceptance-review.md) for detailed evidence, identities, limits and final closeout status after this plan is retained in docs/plan.
