# Documentation Taxonomy

Use this file when you need to classify documentation before reading or writing it.

## Core Model

The recommended private docs tree is:

```text
docs/
├── README.md
├── context/        # optional non-governed m-context data
├── intake/
├── features/
├── requirements/
├── specs/
├── decisions/
├── plan/
├── change/
└── lessons/
```

`context/` is an optional reserved companion directory, not a governed documentation category. Do not create, index, summarize, archive, stage, commit, publish, or copy its contents as part of normal `$m-docs` work. `$m-context` owns access to it, and it may contain plaintext secrets.

## Docs Root Model

- `project_root`
  - local umbrella project directory; it may contain one or more code repositories
- `docs_root`
  - governed documentation root; it can be a local folder or a separate local/private Git repository
- `code_repos`
  - implementation repositories; they are not the default home for private governed docs
- `active_worktree`
  - the dedicated worktree where implementation happens

When the user wants docs kept private, treat `docs_root` as the canonical source for governed docs and treat code repos as implementation carriers.

## Canonical Question by Category

- `intake`
  - What did the user originally ask for, from what source, and what was still unclear?
- `features`
  - What does this user-visible feature currently do end to end, including UI, workflow, permissions, states, and acceptance?
- `requirements`
  - Why does this capability exist, what durable outcomes or boundaries must hold, and what non-feature acceptance criteria apply?
- `specs`
  - How is the capability constrained or structured technically?
- `decisions`
  - What architecturally significant choice was made, why, and what alternatives were considered?
- `plan`
  - How will a specific workflow implement or investigate the work?
- `change`
  - What did a specific workflow actually change, how was it verified, and how can it be rolled back?
- `lessons`
  - What recurring problem or failure pattern did we learn from, how can we look it up by symptom, and how should we avoid it next time?

## Source-of-Truth Boundaries

- `intake` is source evidence, not current truth.
- `features`, `requirements`, `specs`, and `decisions` are long-lived truth layers.
- `plan`, `change`, and `lessons` are workflow, archive, and explanatory layers.
- Root and category `README.md` files are navigation layers, not truth layers.
- `context` is user-controlled runtime context data, not a truth, workflow, archive, or navigation layer.

## Category Rules

### intake

Put original request evidence here.

Include:

- source, date, requester when known
- raw request text or source-preserving summary
- context and unresolved questions
- routing links to features, requirements, specs, decisions, plans, and changes

Do not put:

- current feature truth
- rewritten requirements without source context
- implementation history

### features

Put current user-visible feature behavior here.

Include:

- goal and non-goals
- actors, permissions, entry points, layout, navigation, and UI states
- CRUD workflows and validation rules
- acceptance scenarios
- cross-repo ownership and links to technical specs

Do not put:

- full API specs or protocol tables
- append-only decision records
- one-off implementation history

### requirements

Put durable capability intent, boundaries, actors, scenarios, and non-feature acceptance criteria here.

Do not put:

- detailed screen layouts or button placement when a feature doc owns them
- implementation history
- sprint-by-sprint planning
- final change summaries
- incident retrospectives

### specs

Put interfaces, protocol rules, architecture constraints, generated-doc rules, and technical contracts here.

Do not put:

- current product behavior unless needed as short context
- change chronology
- postmortem content
- ADR rationale that belongs in `decisions`

### decisions

Put append-only architecture decision records here.

Include:

- status
- context
- options considered
- decision
- consequences
- supersedes / superseded-by links

Do not put:

- complete feature behavior
- full technical reference
- change summaries

### plan

Put one workflow's planning, task IDs, dependencies, acceptance points, test points, and rollback points here.

Do not treat `plan` as a stable source of truth once the work is complete.

### change

Put one workflow's result summary, verification, impact, and rollback here.

Always record whether intake, features, requirements, specs, decisions, or lessons changed.

### lessons

Put recurring issue patterns, lookup hints, root causes, debugging trails, and prevention guidance here.

Do not use lessons as a substitute for updating broken feature, requirement, spec, or decision docs.

## Category Relationships

- `intake` should link to the feature, requirement, spec, decision, plan, or change that interpreted it.
- `features` should link to related intake, specs, decisions, changes, and lessons.
- `requirements` should link to related features, specs, and changes.
- `specs` should link to related features, requirements, decisions, and changes.
- `decisions` should link to related features, specs, and superseded decisions.
- `plan` must reference the relevant stable docs.
- `change` must reference the relevant plan and stable docs.
- `lessons` should link back to the relevant change and any corrected stable docs.
- `lessons` indexes should expose enough symptom or keyword context for later lookup.

## Publication Boundary

- A docs root may be versioned with Git.
- Do not add remotes, change remotes, push, publish, or choose a backup destination unless the user explicitly asks.
- `.gitignore` is a useful backup guard, but the safer default is to keep private docs physically outside pushable code repositories.
- The presence of `context/` does not authorize automatic `.gitignore`, `.git/info/exclude`, Git configuration, staging, commit, or push changes. Any Git treatment of context data requires an explicit user request.
