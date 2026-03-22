# Indexing Rules

Use this file when creating or updating `README.md` entry files.

## Index Layers

- Root index:
  - `docs/README.md`
- Category indexes:
  - `docs/requirements/README.md`
  - `docs/specs/README.md`
  - `docs/plan/README.md`
  - `docs/change/README.md`
  - `docs/lessons/README.md`
- Module indexes when needed:
  - `docs/requirements/<module>/README.md`
  - `docs/specs/<module>/README.md`
  - `docs/lessons/<module>/README.md`

## Responsibilities

### docs/README.md

- describe the documentation system at a high level
- explain reading order
- link to each category index
- avoid duplicating leaf document content

### category README.md

- explain what belongs in the category
- link to leaf docs or module indexes
- state naming and maintenance rules for the category

### module README.md

- link to the module's leaf docs
- summarize module scope in one short paragraph

## Update Obligations

Update the nearest index whenever you:

- create a new leaf doc
- rename a leaf doc
- move a leaf doc across modules or categories
- add a new module bucket
- change the docs topology itself

Update root `docs/README.md` only when:

- a top-level category changes
- the reading order changes
- a new navigation path must be exposed globally

## Ordering Rules

- `plan` and `change`
  - prefer reverse chronological order
- `requirements`, `specs`, and `lessons`
  - prefer logical grouping by module or domain, then stable alphabetical ordering

## Minimal README Sections

- Purpose
- How to enter this section
- What belongs here
- Naming / maintenance rules
- Links to current leaf docs or module indexes
