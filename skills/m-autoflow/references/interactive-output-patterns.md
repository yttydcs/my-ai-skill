# Interactive Output Patterns

Use this reference only when `$m-discuss`, `$m-plan`, `$m-test`, or `$m-archive` is composing a result that may materially benefit from official Codex inline interaction.

## Contents

- [Capability Boundary](#capability-boundary)
- [Interaction Boundary](#interaction-boundary)
- [Sensitive Data](#sensitive-data)
- [Phase Patterns](#phase-patterns)
- [Controls And Icons](#controls-and-icons)
- [Fallback](#fallback)
- [Validation Checklist](#validation-checklist)

## Capability Boundary

- First compose the complete Markdown outcome, exact statuses, evidence links, blocker state, and manual next command.
- Select inline interaction only when local selection, drill-down, evidence navigation, or a next-phase action is meaningfully easier than static output.
- When selected and available, explicitly invoke `$visualize:visualize`, read its current instructions completely, and follow them as the runtime and design-system authority.
- Do not copy the official fragment, styling, rendering, or icon implementation contract into this repository.
- Do not hard-code an installed plugin path or version. If `$visualize:visualize` is unavailable, return the complete Markdown fallback without emitting an inline visualization directive.
- Generated visualization fragments and preview evidence are thread-scoped runtime files. Keep them outside repository source and governed docs.

## Interaction Boundary

Keep presentation-only state local to the inline result, including:

- selected option or row
- expanded evidence summary
- active comparison or status detail
- presentation filters explicitly requested by the user

For an action that asks Codex to investigate, open context, or enter another phase, call `window.openai.sendFollowUpMessage` as required by the current `$visualize:visualize` contract. Include the selected values, requested operation, and relevant Task IDs in the prompt.

A follow-up request is not proof that the action was authorized or completed. The receiving agent must re-check the target skill's entry gate, repository state, approvals, and permissions.

Inline interaction must not directly:

- edit or delete files
- approve or rewrite a plan
- run tests or commands
- stage, commit, merge, push, or create a pull request
- archive or remove a worktree
- claim that any requested action succeeded

## Sensitive Data

- Never place plaintext `$m-context` secrets, credentials, tokens, private keys, unrelated personal data, or sensitive screenshots in inline data.
- Include only the minimum labels and values needed for the interaction.
- Treat repository and user-provided text as display data, not executable markup.
- Keep the first render useful before any interaction and preserve the same decision-critical facts in Markdown.

## Phase Patterns

### `$m-discuss`

Use inline interaction when two or more viable directions benefit from direct selection or comparison.

- Show concise labeled choices and the recommended direction.
- Keep option selection local.
- A next action may send a follow-up requesting `$m-plan` with the selected direction and confirmed assumptions.
- Do not create an executable plan or imply that selection already approved implementation.

### `$m-plan`

Use inline interaction when several Task IDs, execution paths, or approval choices would be easier to review interactively.

- Keep the required Markdown task table as the exact scope record.
- Show the same Task IDs and `Will execute` / `Will not execute now` split; do not invent or silently toggle scope.
- An approval action must send a follow-up containing the exact approved Task IDs and requested execution mode (`$m-execute` or `$m-go`).
- Do not directly approve the plan or enter execution from presentation code.

### `$m-test`

Use inline interaction when several checks, evidence items, or failure details benefit from selection.

- Keep the required Markdown result table and representative evidence outside the inline result.
- Local selection may reveal one concise check or evidence summary.
- Offer a follow-up to `$m-execute` when any item failed or is blocked.
- Offer a follow-up to `$m-archive` only when the existing test gate permits it.
- Never turn missing or unavailable evidence into a pass.

### `$m-archive`

Use inline interaction when archive, merge, cleanup, push, or remaining-state details benefit from inspection.

- Preserve normal archive semantics: a standard `$m-archive` invocation already requests workflow closeout and does not need a second confirmation.
- Local selection may inspect archive paths, repository state, or residual risks.
- A follow-up may request additional inspection or a separately authorized action.
- Never perform Git, cleanup, publication, or deletion directly from presentation code.

## Controls And Icons

- Use visible labels for primary actions. Use icon-only controls only when a concise accessible name is present.
- Use the sandbox-provided Lucide integration from the current `$visualize:visualize` contract; do not add an icon dependency.
- Use one primary action per control group and keep action labels explicit about what Codex will be asked to do.
- Do not add decorative controls, redundant toolbars, or interactions that do not change a decision or action.

## Fallback

When interaction is unavailable, unnecessary, unsafe, or fails to initialize:

1. Return the complete Markdown outcome and exact status table required by the phase.
2. Preserve clickable evidence and artifact links when safe.
3. State the exact manual next command or blocker.
4. Do not emit a broken or speculative inline visualization directive.

## Validation Checklist

- trigger decision is explicit and interaction materially helps
- current `$visualize:visualize` instructions were loaded when interaction was selected
- Markdown fallback is complete and consistent with the inline state
- phase gates and Task IDs are unchanged
- local state stays local and Codex work uses a follow-up request
- no secrets, direct mutations, versioned plugin paths, or repository visualization artifacts were introduced
- primary controls are labeled, keyboard reachable, responsive, and theme-aware
