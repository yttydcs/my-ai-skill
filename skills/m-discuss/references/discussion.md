# Discussion Rules

Use this reference for the discovery and discussion phase before `$m-plan`.

## Phase Boundary

- Owns problem framing, requirement shaping, option discovery, feasibility discussion, and early workflow initialization.
- May create or confirm the dedicated branch and worktree when discussion starts the full workflow.
- May update intake, feature, requirement, spec, or decision docs through `$m-docs` when stable truth changes.
- Does not own architecture decomposition, executable Task IDs, implementation, validation, archive, merge, or cleanup.

## Required Discussion Brief

Capture:

- original request and source
- problem / opportunity
- goals and non-goals
- assumptions
- open questions
- constraints and risks
- viable options
- rejected options and reasons
- recommended direction
- research summary with citations when research was used
- docs root, code repo, branch, and worktree status
- handoff criteria for `$m-plan`

## Product And Technical Judgment

- Prefer clarifying the right problem over rushing to implementation.
- Brainstorm several feasible options when the solution space is still open.
- Challenge requests that are unsafe, internally inconsistent, not worth the complexity, or likely to fail the user's real goal.
- When rejecting a requirement, explain the reason and offer a safer or simpler alternative.
- Mark assumptions clearly and avoid turning guesses into requirements.

## Worktree Rule

- If this discussion starts a full workflow, create or confirm the dedicated worktree before handing off to `$m-plan`.
- If the discussion is exploratory only, record that no worktree was created and why.
- If a worktree cannot be created or identified, stop with a blocker before planning.

## Handoff To Plan

Proceed to `$m-plan` only when:

- the goal is coherent
- the recommended direction is explicit
- blocking questions are resolved or clearly deferred
- docs root and code repo boundaries are known
- worktree status is known

If these are not true, continue discussion or ask the user for clarification.

## User-facing Output

- Lead with the recommended direction or the unresolved blocker.
- Compare three or more viable options in a compact criteria / tradeoff / decision table.
- Use Mermaid only when branches, dependencies, or ownership boundaries are materially clearer as a diagram.
- Link created briefs, governed docs, and worktree artifacts using absolute clickable paths.
