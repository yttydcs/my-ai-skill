# Repair Loop Progress

Shared by m-continue and m-go. Apply after a complete repair/test cycle; this does not change either entry point's authorization or delegation rules. An initial validation-only pass establishes the baseline and does not consume a repair cycle.

## Failure Signature

Normalize the unresolved result using stable identifiers where available:

- failing Task IDs and acceptance-criterion IDs
- failing test/check names and command names
- blocker category and relevant error class
- missing evidence category, such as UI operation or screenshot evidence

Ignore volatile timestamps, temporary paths, random IDs, and harmless output ordering. Preserve enough detail to distinguish a changed failure from the same failure recurring.

## Progress Evidence

Compare at least:

- newly completed approved Task IDs or acceptance criteria
- a confirmed repair whose resulting check demonstrates improvement; an attempted diff alone is not progress
- fewer failing checks or a lower-severity failure under comparable check coverage, without trading away already-satisfied acceptance
- new valid validation or UI evidence
- removal of a blocker prerequisite within existing authority

Reset the consecutive non-progress count only for new, durable progress supported by comparable evidence: an acceptance improvement, newly valid required evidence, removal of a prerequisite, or a test that rules out a specific causal hypothesis and changes the next repair decision. Count a ruled-out hypothesis once. A changed failure signature, new diff, repeated green evidence or different error wording alone does not reset the count. Regressions that merely exchange one failed criterion for another are not net progress.

Keep a compact cycle history in the existing result record: normalized signature, affected ACs, attempted repair/hypothesis, comparable evidence delta and non-progress count. Compare against prior best verified acceptance as well as the previous cycle. Detect A -> B -> A and longer recurring states; restoring a previously reached state is not new progress unless independent evidence establishes a durable gain.

## Non-progress Rule

Increment the consecutive non-progress count when a complete repair/test cycle yields no new durable progress under the evidence rule above, whether its failure signature stays the same, changes or oscillates.

Stop as a non-progress loop after **three consecutive complete cycles** lack such progress. Do not impose a separate small total-iteration limit while verifiable progress continues. Report the signature history, three attempted cycles, evidence deltas and the exact decision or external change needed to resume. Do not repeat the same repair/check without a new hypothesis or changed input. A hard blocker may stop earlier.

Do not run empty or cosmetic edits merely to reset the counter. They are not progress.

