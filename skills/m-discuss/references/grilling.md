# Grill Mode

Use this reference only when the user explicitly asks to be grilled, pressure-test a plan through hard questions, or resolve decisions one at a time. Do not enter Grill Mode merely because the request is vague or incomplete.

## Purpose

Grill Mode is an opt-in interview inside `$m-discuss`. It exposes hidden judgment calls, resolves decision dependencies, and then returns to the standard discussion brief. It does not own planning or implementation.

## Decision Snapshot

Maintain a task-local snapshot with:

- confirmed decisions
- rejected alternatives
- deferred decisions and their consequences
- open decisions
- discoverable facts and evidence gaps
- dependencies between parent and child decisions

Update the snapshot after every answer. Never turn a recommendation, silence, ambiguity, or an inferred preference into a confirmed decision. When a parent decision changes, invalidate only the dependent child decisions and revisit them as needed.

## Fact And Decision Boundary

- Look up discoverable facts from the filesystem, repository, available tools, or authorized external research before asking the user.
- Ask the user only for judgment calls, priorities, trade-offs, risk acceptance, or information that cannot be discovered safely.
- If a fact cannot be verified, record an evidence gap. Do not disguise the gap as a decision or ask the user to restate information the environment can provide.

## Interview Loop

1. Select the highest-risk unresolved parent decision. Resolve parent decisions before dependent child branches.
2. Ask exactly one judgment question per turn.
3. Include one recommended answer and a concise rationale with the question. Make clear that the recommendation is not a confirmed decision.
4. Wait for the user's answer before asking another question. Do not bundle related questions, alternatives, or follow-ups into the same turn.
5. Record a concrete answer in the decision snapshot.
6. If the answer is too vague to support planning, narrow or re-ask the same branch instead of silently assuming agreement or moving on.
7. Continue depth-first until the current branch is resolved or explicitly deferred, then select the next highest-risk unresolved branch.

Avoid redundant questions. Do not impose a fixed numeric question limit: the user may stop at any time or ask to wrap up and summarize.

## Completion And Early Wrap-up

- When no blocking decision remains, ask the user to confirm explicitly that shared understanding has been reached.
- Do not treat the absence of more questions as confirmation.
- If the user confirms, return to `discussion.md` and produce the complete standard discussion brief.
- If the user asks to stop or wrap up early, return to the brief immediately, distinguish confirmed, rejected, deferred, and open decisions, and state whether the open items block `$m-plan`.
- If blocking decisions remain, do not claim the workflow is ready for `$m-plan`.
- If the normal discussion exit gate passes, report readiness for `$m-plan` but wait for the user to invoke or approve the next phase.

Do not enter `$m-plan`, implement code, create `docs/change`, archive, merge, push, publish, or clean worktrees automatically.

## Attribution

This local protocol is an independent adaptation of the interview pattern in Matt Pocock's [`grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) skill. The upstream repository uses the [MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE). This reference has no runtime dependency on the upstream skill or repository.
