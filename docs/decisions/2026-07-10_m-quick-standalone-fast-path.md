# 2026-07-10 m-quick Standalone Fast Path

## Status

Accepted.

## Context

The existing staged commands deliberately require discussion, planning, worktree isolation, validation, and archive controls. Those guarantees are valuable for meaningful engineering work but create disproportionate overhead for localized, obvious, low-risk fixes.

The fast path must still read governed docs so that reducing workflow artifacts does not reduce understanding of current behavior or constraints.

## Options Considered

1. Add standalone `$m-quick` with its own guarded direct-edit contract.
2. Add a bypass or quick mode to `$m-execute`.
3. Let `$m-autoflow` select a shorter route implicitly.
4. Use `$m-fix`, `$m-patch`, or `$m-direct` as the command name.

## Decision

Add `$m-quick` as a standalone command and alternate route in the `m-*` collection.

- It is not a staged workflow phase.
- It explicitly uses `$m-docs` before eligibility or edits.
- It operates directly in one selected repository's current checkout after a risk gate passes.
- It does not create a worktree, plan, archive, commit, or push by default.
- It requires focused validation and UI evidence when applicable.
- It escalates unsuitable work to `$m-discuss` or `$m-plan`.
- It keeps complete current behavior in a dedicated feature dossier and references `$m-docs` instead of duplicating taxonomy rules.

Do not weaken `$m-execute` entry gates. Use the name `$m-quick` because it covers both fixes and small requirements while signaling bounded scope better than mechanism-oriented alternatives.

## Consequences

Positive:

- Small work can be completed with much less setup and archive overhead.
- Relevant project context remains mandatory.
- Staged commands retain their strict and auditable semantics.
- Risky requests have an explicit escalation path.

Negative:

- Quick runs have less historical workflow traceability than archived runs.
- Eligibility depends on engineering judgment and requires careful fail-closed wording.
- Installed umbrella and quick skill copies must be kept synchronized.

## Confidence

High. The boundary is explicit, and the existing `$m-docs` skill already provides the required context and stable-doc routing behavior.

## Supersedes / Superseded By

- Supersedes: none.
- Superseded by: none.

## Related Features

- [m-quick-fast-path.md](../features/m-quick-fast-path.md)
- [m-autoflow-workflow.md](../features/m-autoflow-workflow.md)

## Related Specs

- [m-quick-skill.md](../specs/m-quick-skill.md)
- [m-autoflow-skill.md](../specs/m-autoflow-skill.md)

## Related Changes

- [2026-07-10_m-quick-fast-path.md](../change/2026-07-10_m-quick-fast-path.md)
