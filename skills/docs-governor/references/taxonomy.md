# Documentation Taxonomy

Use this file when you need to classify documentation before reading or writing it.

## Core Model

The recommended docs tree is:

```text
docs/
├── README.md
├── requirements/
├── specs/
├── plan/
├── change/
└── lessons/
```

## Canonical Question by Category

- `requirements`
  - Why does this capability exist, what must it do, what is in scope, and how is it accepted?
- `specs`
  - How is the capability constrained or structured technically?
- `plan`
  - How will a specific workflow implement or investigate the work?
- `change`
  - What did a specific workflow actually change, how was it verified, and how can it be rolled back?
- `lessons`
  - What recurring problem or failure pattern did we learn from, and how should we avoid it next time?

## Source-of-Truth Boundaries

- `requirements` and `specs` are long-lived truth.
- `plan`, `change`, and `lessons` are archival and explanatory.
- Root and category `README.md` files are navigation layers, not truth layers.

## Category Rules

### requirements

Put long-lived needs, boundaries, actors, scenarios, and acceptance criteria here.

Do not put:

- implementation history
- sprint-by-sprint planning
- final change summaries
- incident retrospectives

### specs

Put interfaces, protocol rules, architecture constraints, generated-doc rules, and technical contracts here.

Do not put:

- why the feature exists at a business level unless needed as short context
- change chronology
- postmortem content

### plan

Put one workflow's planning, task IDs, dependencies, acceptance points, test points, and rollback points here.

Do not treat `plan` as a stable source of truth once the work is complete.

### change

Put one workflow's result summary, verification, impact, and rollback here.

Always record whether `requirements` or `specs` changed.

### lessons

Put recurring issue patterns, root causes, debugging trails, and prevention guidance here.

Do not use lessons as a substitute for updating a broken requirement or spec.

## Category Relationships

- `plan` must reference the relevant `requirements` and `specs`.
- `change` must reference the relevant `plan` and stable docs.
- `lessons` should link back to the relevant `change` and any corrected `requirements` or `specs`.
