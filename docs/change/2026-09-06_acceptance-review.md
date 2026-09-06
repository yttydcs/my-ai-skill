# Acceptance And Review Handoffs

## 变更背景 / 目标

The user approved the first round of improvements after comparing Matt Pocock's grill-with-docs -> to-spec -> to-tickets -> implement -> code-review chain with the local staged workflow. Preserve the existing entry commands while improving requirement retention, task verification, review coverage and evidence reuse.

## 具体变更内容

- Discussion retains confirmed, rejected, deferred and open decisions with exact source constraints. Planning maps source -> AC ID -> Task ID -> evidence and prefers independently verifiable behavior slices.
- Execution performs separate lightweight requirements and standards review. Heavy-test skips do not implicitly skip review or waive required behavior.
- The shared review covers committed, staged, unstaged and untracked owned changes, records candidate/plan identity, and refreshes only affected stale evidence during test, continuation and archive.
- Discoverable facts and reversible in-scope choices no longer trigger generic approval loops. Existing plan approval, explicit Grill Mode, private docs and archive closeout rules remain intact.
- Updated eight packages: m-autoflow, m-plan, m-execute, m-test, m-archive, m-go and m-continue are version 0.2.0; m-discuss is version 0.3.0. This implementation does not edit the m-pipeline runtime; an unrelated control-branch fix was preserved during integration as recorded below.

## Docs Governance

- Docs root: `D:/project/my-ai-skills/docs`; authored in the dedicated worktree's docs tree and retained in this repository.
- Intake impact: updated. [Original request and approved scope](../intake/2026-09-06_acceptance-review.md).
- Feature impact: updated. [Workflow behavior](../features/m-autoflow-workflow.md).
- Requirements impact: updated. [Capability requirements](../requirements/m-autoflow-skill.md).
- Specs impact: updated. [Technical contract](../specs/m-autoflow-skill.md).
- Decision impact: none. Existing [explicit Grill Mode decision](../decisions/2026-07-20_m-discuss-grill-mode.md) remains applicable.
- Lessons impact: updated. [Dirty worktree review](../lessons/dirty-worktree-review.md).
- Related plan: [Retained approved plan and results](../plan/2026-09-06_acceptance-review.md).
- Existing lessons reused: [unittest discovery](../lessons/python-unittest-discovery-nonpackage-tests.md), [Windows parity](../lessons/windows-skill-parity-line-endings.md), [symlink privilege](../lessons/windows-symlink-test-privilege.md).
- Category indexes updated; documentation topology and publication boundary unchanged. No remote publication or push.

## 对应任务 / 验收项 / 证据与未验证事项

| Acceptance | Tasks | Evidence / outcome |
| --- | --- | --- |
| AC-01: retain exact decisions | T1, T4 | Source review and independent save-dialog-plan output preserve failure negation, 3 seconds, no retry default and event ordering |
| AC-02: verifiable slices and blockers | T1, T3, T4 | Scenario produced two complete behavior tasks; source and stable docs agree on isolated migration batches and explicit final integration |
| AC-03: separate review and skips | T2, T4 | Five consumers route to shared review; heavy-skip scenario blocks archive pending lightweight review; continuation exit wording corrected |
| AC-04: full owned candidate | T2, T4 | Documented Git commands exercised against all change surfaces, including overlapping index/worktree edits; review does not mutate state |
| AC-05: fresh evidence | T1, T2, T4 | Changed-limit scenario invalidates 10 MiB evidence for the approved 8 MiB revision and reuses independent T2 evidence with its supplied impact proof |
| AC-06: bounded uncertainty | T1, T2, T4 | Private helper naming resolved from convention without another question; existing Grill Mode and continuation contracts pass |
| AC-07: docs, packaging, installation and closeout | T3, T4, T5 | Stable docs, validation and exact installed parity complete; final local closeout status recorded below |

## 测试与验证方式 / 结果

| Check | Result | Evidence and limits |
| --- | --- | --- |
| Full repository regression | 69 passed, 2 skipped (71 total) | `python -B -m unittest discover -s tests -v`; 118.765 seconds |
| Focused final checks | 9 passed | Continuation contract 6 and acceptance/review contract 3 rerun after the final continuation wording correction; no runtime/test implementation changed after full regression |
| Integration after control-branch advance | 31 passed, 1 skipped (32 total) | `python -B -m unittest discover -s tests -p 'test_m_pipeline_*.py' -v`; 95.374 seconds; includes the concurrent project-creation fix; same symlink-fixture limitation |
| New review checks | 3 passed | Shared-reference packaging, executable Git coverage, and unchanged HEAD/index/worktree; included in the full-suite count |
| Package validation | 8 passed | Existing `tools/validate-skills.ps1 -Skill <name>` run for each changed package, including after final wording fixes |
| Independent decision scenarios | 4 satisfactory outputs | Fresh evaluator received only raw packets and relevant skills; main assessed actual outputs; these are not live product end-to-end runs |
| Installation | Exact parity passed | Before sync, 32 prior source files matched installed text apart from line endings. After sync, all 33 source files matched distribution and installation SHA-256 bytes; build versions checked separately |
| Whitespace / scope review | Passed | `git diff --check`; source changes restricted to approved eight packages, manifests, tests and stable docs |

The skipped tests are `test_rejects_symlink_escape_when_supported` in m-context and `test_candidate_dirty_wrong_repository_and_symlink_escape` in m-pipeline config. Windows rejected fixture creation with WinError 1314. Those symlink branches have no new runtime evidence here; the affected runtime files were not changed. No waiver or skipped check is labeled passed. Product UI, security/performance load tests and real application end-to-end runs are not applicable to these instruction/document changes; no such execution is claimed.

### Independent scenario outputs

Source packets: [scenarios.json](../../tests/fixtures/acceptance-review/scenarios.json). The evaluator read the packets, named skill entries and required references without expected answers or parent conversation, made no product edits and ran no product checks.

1. **save-dialog-plan**: T1 preserves all inputs and keeps the dialog open on failure, uses a 3-second timeout and no automatic retry; T2 updates the list before closing on success. Verification observes the public dialog/save interface, requests and event order. Silent retry remains rejected; offline editing becomes explicitly deferred T3. T1/T2 have no real dependency but may edit shared files serially. Criteria remain pending. Actual filenames were absent, so output used module scope and did not create a real plan. Its implementation block reflected missing implementation approval, not unclear requirements.
2. **heavy-skip-dirty-review**: honors the requested heavy-test skip, returns to m-execute for requirements/standards review and keeps archive blocked. It does not treat supplied focused-test/typecheck claims as newly verified results. Review includes modified save.py and untracked test_save.py without forced staging/commit/cleanup; no defect or waiver is invented.
3. **changed-limit-resume**: continues the already approved 8 MiB revision without another approval. Old 10 MiB/T1 evidence is historical; candidate B needs affected validation and review. T2 evidence can be reused because unchanged inputs/dependencies and a verified impact note are supplied facts. No full heavy rerun is inferred from missing lightweight review, and no archive is invoked. Actual loop count is zero.
4. **approved-reversible-choice**: selects matchesFilter from local convention without a question. Proposes verification through the public list interface, followed by focused checks and both review axes. Implementation and evidence remain pending; no edits or passes are claimed.

These samples demonstrate the evaluated decisions only. They do not establish universal model compliance or a complete discuss-to-archive product run.

## Requirements / Standards 审查结论与有效性

- Requirements: passed for the implemented approved behavior and package/document obligations. AC-07 closeout is tracked separately until actual integration and cleanup finish.
- Standards: passed. Shared rules have one reference owner and five phase consumers; source/package routing is valid; tests execute the documented Git commands and observe state independently. No outstanding in-scope finding remains.
- Findings fixed: migration documentation initially implied every intermediate batch must pass independently; corrected to allow isolated batches with an explicit final integration gate. Fixed a nested-list indentation error. Replaced the legacy continuation termination sentence that could confuse a heavy-test skip with AC disposition.
- Review base: `eceea63df4507b65f5bb18fc606ee42c62f49d1a`. Review-time HEAD: `d61dbc4d2e75c9bf9d63e3e96125e333ab674911`. At review, 30 tracked files were modified and 3 new files were untracked. No source deletion, mode change or symlink was involved; base-to-worktree, staged/unstaged views and new-file contents were inspected.
- Reviewed 33-file content SHA-256: `c1de2e47e7082695b726a02b3791a773e764ca4514e0fe7f569f734e83d27c61`. For each lexically sorted implementation path, hash bytes after CRLF-to-LF conversion; concatenate `path + NUL + file_sha256 + newline` and SHA-256 that UTF-8 sequence. Paths are exactly the files in implementation commit `636e8b7cfb1f9b7d9e52a399e612c8070bfeabcb` relative to its parent. All are regular text files with mode 100644. This normalization is explicit; installed-copy parity uses exact bytes instead.
- The implementation commit was created only after review and was verified content-equivalent to that dirty candidate. Its commit is the durable candidate reference. Subsequent archive/progress files are outside measured product inputs; a commit alone is not new test evidence.
- Plan source: `d61dbc4d2e75c9bf9d63e3e96125e333ab674911:plan.md`, blob `d61d16a548b5982163a5bfe36f220730c1ff4f53`. Definition SHA-256: `7dbf34ce11508e9910912b1c6cf62379e1388b34251f34ed10f33a447ff1151b`. Projection contains goal/scope, AC ID/source/Task columns, execution scope, task details and risks/parallelism; excludes workflow progress, evidence/status cells and later execution-result annotations. Task and acceptance definitions remain unchanged.
- Freshness at archive: source hashes still match after validation, sync and commit. The final small wording correction received focused checks and semantic review; existing unrelated regression evidence remains applicable. Integration must preserve the reviewed contents before cleanup.

## 经验 / 教训摘要与可复用排查线索

An empty committed diff can hide dirty implementation; even the final worktree may hide index-only edits. Search the new [dirty-worktree lesson](../lessons/dirty-worktree-review.md) for symptoms and the reproducible test. Existing Windows lessons cover line-ending-only pre-sync differences and symlink-fixture privilege skips.

## 关键设计决策与权衡

Keep the five-stage workflow and add shared review within existing phases. Favor one compact acceptance map and selective evidence refresh; do not require extra checkpoint commits, duplicate review at archive, mandatory TDD or a new pipeline. Migration batches are allowed only with their integration dependency made explicit. Instruction behavior remains model-dependent, so semantic scenario evidence is reported separately from deterministic tests.

## 潜在影响与回滚方案

Eight installed packages now enforce the revised handoffs. Existing explicit approvals, single-question Grill Mode and private-doc boundaries remain intact. If rollback is requested, revert implementation commit `636e8b7` on the control branch, validate the prior packages, then resync the same eight named skills with the existing tool. Preserve user changes and historical intake/change records; do not reset the repository or installed skill root wholesale.

## 子Agent执行轨迹

- Main agent: approved-plan control, T1/T2 source and package changes, deterministic validation, integration review, source/install checks and T5 closeout.
- stable_docs: bounded T3 write set of three stable leaves, followed by read-only consistency review; identified the migration wording issue, which main reconciled. No commit, merge, cleanup or install was delegated.
- behavior_eval: independent read-only T4 evaluation with four raw packets; no expected output or parent conversation supplied. Returned actual decisions and execution limits. Main owns the acceptance conclusion and retained summary.

## Local Closeout

- Archive and retained plan: prepared; local merge and cleanup pending.
- Implementation commit: `636e8b7cfb1f9b7d9e52a399e612c8070bfeabcb`.
- The control branch advanced to `c6805329960d29c9e4aff574aa4826586dcec251` while this work ran. Its unrelated m-pipeline project-creation fix was merged into the worktree for validation. Only docs/change/README.md conflicted; both index entries were retained. All 33 reviewed implementation files remain unchanged, and all 15 imported non-index files match the control commit; the two shared indexes combine both changes.
- Installation is current with the worktree source. After merge, rebuild from the persistent control source and check exact source/distribution/install parity before worktree removal.
- Remote state: local-only; no push requested or performed.
