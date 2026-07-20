# Archived Plan - m-discuss Grill Mode

## Goal

Add an explicitly triggered Grill Mode to `$m-discuss` that pressure-tests decisions one question at a time while preserving normal discussion behavior, the standard brief, and downstream authorization gates.

## Workflow Information

- Repository: `D:\project\my-ai-skills`
- Branch: `feat/m-discuss-grill-mode`
- Base: `main` at `b75bab8c8b325cd91e6d2146d69caa49836dc28b`
- Worktree: `D:\project\my-ai-skills\worktrees\m-discuss-grill-mode`
- Docs root: repository `docs` tree
- Planning commit: `a9d7a98`

## Discussion Summary

Research confirmed that current upstream `grill-me` is a small wrapper around a reusable `grilling` primitive. The useful behavior is the interview discipline: resolve dependent decisions depth-first, ask one judgment question at a time with a recommendation, research discoverable facts, wait for the user, and stop before action without explicit confirmation.

The chosen design adapted that discipline as a conditional local reference instead of adding upstream dependencies, forcing every discussion into a long interview, or creating a second public discovery skill.

## Accepted Requirements

- Explicit-only activation; ambiguity alone does not trigger Grill Mode.
- Discoverable facts are researched before asking the user.
- Exactly one judgment question per turn, with a recommendation and rationale.
- Parent decisions precede child branches.
- Confirmed, rejected, deferred, and open decisions remain distinguishable.
- The user may stop or request a summary without a fixed question count.
- Shared understanding requires explicit user confirmation.
- The standard discussion brief remains authoritative.
- No automatic `$m-plan`, implementation, archive, merge, push, publication, or cleanup.
- No external skill or runtime dependency.

## Architecture

- `skills/m-discuss/SKILL.md`: explicit trigger detection and conditional routing.
- `skills/m-discuss/references/grilling.md`: decision snapshot and interview loop.
- `skills/m-discuss/references/discussion.md`: brief, blockers, worktree status, and handoff authority.
- `manifests/m-discuss.json`: version `0.2.0` and reference packaging.
- `tests/test_m_discuss_grill_contract.py`: deterministic source, package, gate, and stable-doc assertions.
- Stable docs: workflow feature, durable requirements, and technical spec.
- Generated copies: source -> ignored dist -> installed `m-discuss`.

## Tasks And Results

| Task ID | Result | Commits / Evidence |
| --- | --- | --- |
| GM-1 | Completed | `ee906f6` - conditional routing and local interview reference |
| GM-2 | Completed | `6698149` - manifest/version and eight focused contract tests |
| GM-3 | Completed | `2174254` - feature, requirements, spec, and plan command correction |
| GM-4 | Completed | source/installed validation, full tests, sync, and hash parity; execution record `07258e9` |
| GM-5 | Completed by archive | change record, archived plan, control-plane closeout |

## Stable Docs Impact

- Intake impact: added.
- Feature impact: clarified.
- Requirements impact: clarified.
- Specs impact: clarified.
- Decision impact: added and accepted.
- Lessons impact: none; reused the existing non-package unittest discovery lesson.

## Validation

- 8 focused tests passed.
- 40 full repository tests passed; 1 existing conditional test skipped.
- Source and installed skill validators passed.
- `git diff --check` passed.
- Source, dist, and installed copies matched by SHA-256 for 5 package files, excluding generated build metadata.
- Package metadata version was `0.2.0` in dist and installed copies.

## Residual Risk

- Live model adherence can vary even when the instruction contract is complete.
- An optional real conversational trial can provide behavioral evidence, but no heavy test was required for this prompt/package/documentation-only change.

## Rollback

- Revert the workflow commits and resync `m-discuss` from the restored source.
- Revalidate the source and installed copies and rerun unittest discovery.

## Related Docs

- [Intake](../intake/2026-07-20_m-discuss-grill-mode.md)
- [Decision](../decisions/2026-07-20_m-discuss-grill-mode.md)
- [Feature](../features/m-autoflow-workflow.md)
- [Requirements](../requirements/m-autoflow-skill.md)
- [Spec](../specs/m-autoflow-skill.md)
- [Change archive](../change/2026-07-20_m-discuss-grill-mode.md)
- [Related existing lesson](../lessons/python-unittest-discovery-nonpackage-tests.md)
