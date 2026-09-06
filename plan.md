# Plan - Acceptance and review handoffs

## Workflow Information
- Repo / Project Root: D:/project/my-ai-skills
- Branch: codex/acceptance-review
- Base: main at eceea63
- Worktree: D:/project/my-ai-skills/worktrees/acceptance-review
- Docs Root: D:/project/my-ai-skills/worktrees/acceptance-review/docs (retained in the repository docs tree after closeout)
- Code Repos: this repository only
- Current Stage: plan confirmed; ready for execute
- Authority: the user approved the concrete proposal with "好的请继续" on 2026-09-06. No repeated implementation approval is needed within this scope.
- Discussion: completed in the current conversation; repository and upstream skill review established the proposal.

## Goal and Scope
Keep the existing discuss -> plan -> execute -> optional heavy test -> archive entries. Make confirmed requirements traceable to acceptance and evidence, favor independently verifiable task slices, and keep a lightweight requirements/standards review even when heavy testing is skipped.

Preserve explicit one-question Grill Mode, plan approval, private docs, existing execution authority, and archive closeout. Do not add a glossary system, change stage names, refactor m-pipeline, mandate TDD for every change, force commits for review, or add an outer scheduling loop.

## Acceptance
| ID | Confirmed requirement / source | Tasks | Evidence | Status |
| --- | --- | --- | --- | --- |
| AC-01 | Approved proposal: preserve confirmed, rejected, deferred and open decisions; carry negative, numeric, default and ordering constraints into acceptance | T1 | pending scenario evaluation | pending |
| AC-02 | Approved proposal: each task declares a deliverable, genuine blockers and independent verification; allow compatibility/migration exceptions | T1 | pending scenario evaluation | pending |
| AC-03 | Approved proposal: separate requirements and standards review from optional heavy testing; explicit waivers are not passes | T2 | pending contract and scenario evaluation | pending |
| AC-04 | Approved proposal: review committed, staged, unstaged and untracked workflow-owned changes without altering unrelated work | T2 | pending isolated Git scenario | pending |
| AC-05 | Approved proposal: bind review/evidence to plan and candidate state; changes invalidate affected evidence and archive reuses valid results | T1, T2 | pending scenario evaluation | pending |
| AC-06 | Approved proposal: discover facts; decide reversible in-scope choices; block only material unknowns or missing execution prerequisites; preserve all existing entry gates | T1, T2 | pending compatibility tests | pending |
| AC-07 | Approved proposal and repository packaging contract: update stable docs, package references, validate, sync installed copies and archive | T3, T4, T5 | pending full tests, skill validation and parity | pending |

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
- Lessons impact: assess at archive; known unittest discovery lesson reused.
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
