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

Preserve confirmed, rejected, deferred, and open decisions in the durable brief after either standard discussion or Grill Mode. Keep a source reference or source-preserving statement for each material constraint, especially prohibitions, quantities, units, defaults, ordering and permissions. Do not replace a precise answer with a weaker summary. Record what a deferred decision blocks; deferral alone does not resolve that dependency. Persist the brief through `$m-docs` before a session handoff, using the existing intake/plan routing rather than a new document category.

## Product And Technical Judgment

- Prefer clarifying the right problem over rushing to implementation.
- Brainstorm several feasible options when the solution space is still open.
- Challenge requests that are unsafe, internally inconsistent, not worth the complexity, or likely to fail the user's real goal.
- When rejecting a requirement, explain the reason and offer a safer or simpler alternative.
- Mark assumptions clearly and avoid turning guesses into requirements.
- Resolve discoverable facts from relevant docs, code and authorized tools. Choose reversible implementation details inside the agreed scope using project conventions, and record a material assumption. Ask when an unresolved decision affects behavior, compatibility, architecture, permissions, data, scope or acceptance, or when a required prerequisite cannot be established. Do not repeat an approval already given for the same scope.

## Grill Mode Compatibility

- Use `grilling.md` only after an explicit request to be grilled, pressure-test thinking through hard questions, or resolve decisions one at a time.
- Do not infer Grill Mode from ambiguity alone; ordinary `$m-discuss` keeps its existing discovery and option-comparison behavior.
- The interview feeds this reference's required discussion brief rather than replacing it.
- If the user requests an early wrap-up, preserve unresolved and deferred decisions in the brief instead of inventing agreement.
- Blocking open decisions prevent the `$m-plan` handoff. Confirmed shared understanding permits the normal handoff check but never authorizes planning or implementation automatically.

## Worktree Rule

- If this discussion starts a full workflow, create or confirm the dedicated worktree before handing off to `$m-plan`.
- If the discussion is exploratory only, record that no worktree was created and why.
- If a worktree cannot be created or identified, stop with a blocker before planning.

## Handoff To Plan

Proceed to `$m-plan` only when:

- the goal is coherent
- the recommended direction is explicit
- blocking questions are resolved, or their dependent work is explicitly excluded/deferred from the next plan
- docs root and code repo boundaries are known
- worktree status is known

If these are not true, continue discussion or ask the user for clarification.

## User-facing Output

- Lead with the recommended direction or the unresolved blocker.
- Compare three or more viable options in a compact criteria / tradeoff / decision table.
- Use Mermaid only when branches, dependencies, or ownership boundaries are materially clearer as a diagram.
- Link created briefs, governed docs, and worktree artifacts using absolute clickable paths.
