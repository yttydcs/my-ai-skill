# Visual Output Components

Use this reference before composing a user-facing result from an `m-autoflow` workflow skill or companion utility listed in the phase recipes below. Prefer the smallest component that makes the result easier to scan, verify, or act on. Keep a plain-Markdown summary so the response remains useful when an app-specific component is unavailable.

## Contents

- [Default Composition](#default-composition)
- [Component Selection](#component-selection)
- [Official Inline Interaction](#official-inline-interaction)
- [Tables And Status](#tables-and-status)
- [Mermaid](#mermaid)
- [Local Files And Media](#local-files-and-media)
- [Code Review Comments](#code-review-comments)
- [Git Components](#git-components)
- [Phase Recipes](#phase-recipes)
- [Final Check](#final-check)

## Default Composition

1. Lead with the outcome, decision, or blocker in one sentence.
2. Add one primary component that exposes the important structure.
3. Link or embed the evidence the user is most likely to open.
4. End with the next action only when one is required.

Do not repeat the same facts in prose, a table, and a diagram. Do not add a visual solely for decoration.

## Component Selection

| Information shape | Preferred component | Use it when |
| --- | --- | --- |
| Repeated fields, status, options, task mappings | Markdown table | Three or more items benefit from exact side-by-side comparison |
| Dependencies, branches, ownership, or a multi-step state flow | Mermaid flowchart | The relationship is materially harder to understand in prose |
| Selection, drill-down, evidence navigation, or next-phase request | Official `$visualize:visualize` inline interaction | A meaningful interaction is materially easier than static output |
| Created or changed local artifacts | Clickable file links | The user may need to open or inspect the artifact |
| UI or rendered-document evidence | Embedded image or video | Visual state is part of acceptance or diagnosis |
| Actionable line-specific review finding | `::code-comment` | The finding maps to a tight source range |
| Successful Git action | Git directive | The host supports the directive and the corresponding action actually succeeded |

Use short prose for a single fact, one-step action, or simple edit.

## Official Inline Interaction

- For `$m-discuss`, `$m-plan`, `$m-test`, or `$m-archive`, read `interactive-output-patterns.md` when the result may benefit from interaction.
- Keep the complete phase outcome and exact status in Markdown before adding an inline result.
- Invoke `$visualize:visualize` only after the shared interaction trigger passes; let its current instructions own fragment implementation and presentation details.
- Use inline interaction as a supplement, not a replacement for required task tables, test tables, evidence, blocker wording, or manual next commands.
- If the capability is unavailable or unnecessary, keep the static result and emit no inline directive.

## Tables And Status

- Keep tables to the few columns needed for the decision; prefer five or fewer columns when practical.
- Put long reasoning below the table instead of creating unreadable cells.
- Use explicit text statuses: `Passed`, `Failed`, `Blocked`, `Skipped`, `Changed`, or `Unchanged`. Do not rely on color or emoji alone.
- Link file values instead of showing bare local paths.
- When a table has only one row and no comparison value, use a sentence or short list instead, unless the active skill requires a fixed result-table schema.

## Mermaid

- Use `flowchart LR` for short pipelines and dependency chains; use `flowchart TD` for branching or hierarchical flows.
- Quote node labels that contain spaces or punctuation.
- Keep the diagram focused, normally at twelve nodes or fewer. Split or omit it when it becomes a wall of boxes.
- Follow the diagram with the decision or implication in text so it remains accessible.
- Do not use Mermaid for a flat checklist, a one-path sequence, or information already clear in a compact table.

## Local Files And Media

Use absolute paths in user-facing links:

```md
[plan.md](/absolute/worktree/plan.md)
[implementation](/absolute/repo/src/module.ts:42)
[file with spaces](</absolute/repo/My File.md:12>)
```

Embed representative visual evidence instead of returning only a screenshot path:

```md
![Settings page after save](/absolute/evidence/settings-saved.png)
```

- Use concise, meaningful alt text.
- Show one or two representative images inline, then link additional evidence in a compact table.
- Never embed or link a screenshot that exposes secrets or unrelated personal data.

## Code Review Comments

For actionable line-specific findings, emit one directive per finding with the tightest useful range:

```text
::code-comment{title="[P1] Validate the decoded path" body="Reject paths outside the configured root before opening the file." file="/absolute/repo/src/loader.ts" start=42 end=44 priority=1}
```

Use priorities `0` through `3`, where `0` is highest. Keep the normal response as a short findings summary. Emit no code-comment directive when there are no actionable findings or the issue is not line-specific.

## Git Components

After an action succeeds, emit the matching directive on its own line in the final response:

```text
::git-create-branch{cwd="/absolute/repo" branch="codex/topic"}
::git-stage{cwd="/absolute/repo"}
::git-commit{cwd="/absolute/repo"}
::git-push{cwd="/absolute/repo" branch="codex/topic"}
::git-create-pr{cwd="/absolute/repo" branch="codex/topic" url="https://example.com/pr/1" isDraft=false}
```

- Emit only directives supported by the active host.
- Never emit a directive for an attempted, skipped, failed, or merely recommended action.
- Keep an ordinary text status beside the directives so the result remains understandable outside the component renderer.

## Phase Recipes

- `$m-autoflow`: show the selected route and next gate; use Mermaid only when several valid workflow branches or phase transitions need comparison.
- `$m-orchestrator`: show project and Task state, Worker identity, pool status, and next transition in a compact table; never expose loaded context bodies or credentials.
- `$m-context`: show loaded context names and sections in a compact table only when several were requested; never echo secret values.
- `$m-discuss`: use an option comparison table; add Mermaid only for a real branch, dependency, or ownership model; consider the shared interactive pattern when direct option selection helps.
- `$m-plan`: link the active `plan.md` / `todo.md`, show the task table, and add Mermaid only when task dependencies or system flow need it; consider the shared interactive pattern for bounded approval follow-up.
- `$m-execute` and `$m-go`: map Task IDs to clickable changed files and validation status; visualize dependencies only when they affect sequencing.
- `$m-continue`: summarize iterations, Task IDs, validation changes, and the terminal reason in a compact table; link changed files and show whether the result is archive-ready or blocked by a repeated signature or hard dependency.
- `$m-quick`: keep the compact result table, link changed files, and embed representative UI evidence when UI acceptance was exercised.
- `$m-test`: show the result table, embed representative screenshots or rendered pages, use code comments only for actionable line findings, and consider the shared interactive pattern for multi-item evidence navigation.
- `$m-docs`: link created or updated docs and summarize category / impact / index status in one table when several artifacts changed.
- `$m-archive`: summarize archive, merge, cleanup, and remaining-state status; emit Git components only for successful actions; consider the shared interactive pattern for state inspection without adding a second closeout confirmation.
- `$m-gitpush`: show remote, branch, pushed range, and final status; emit `::git-push` only after the push succeeds.

## Final Check

Before sending the response, confirm that:

- the first sentence states the outcome
- every visual component has a decision or verification purpose
- local artifacts use clickable absolute links
- representative visual evidence is embedded when appearance is part of acceptance
- status is understandable without color or component rendering
- app directives correspond to actions that actually succeeded
