# Indexing Rules

Use this file when creating or updating `README.md` entry files.

## Index Layers

- Root index:
  - `docs/README.md`
- Category indexes:
  - `docs/intake/README.md`
  - `docs/features/README.md`
  - `docs/requirements/README.md`
  - `docs/specs/README.md`
  - `docs/decisions/README.md`
  - `docs/plan/README.md`
  - `docs/change/README.md`
  - `docs/lessons/README.md`
- Module indexes when needed:
  - `docs/features/<module>/README.md`
  - `docs/requirements/<module>/README.md`
  - `docs/specs/<module>/README.md`
  - `docs/lessons/<module>/README.md`

## Responsibilities

### docs/README.md

- describe the documentation system at a high level
- explain reading order
- explain the private docs root / publication boundary when relevant
- link to each category index
- avoid duplicating leaf document content

### category README.md

- explain what belongs in the category
- link to leaf docs or module indexes
- state naming and maintenance rules for the category
- for `docs/lessons/README.md`, add a short symptom or keyword clue for each lesson when practical
- for `docs/features/README.md`, expose feature names and cross-repo ownership cues when practical
- for `docs/intake/README.md`, expose source/date cues when practical

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
- change the discoverability cues for an existing lesson, feature, intake record, or decision

Update root `docs/README.md` only when:

- a top-level category changes
- the reading order changes
- a new navigation path must be exposed globally
- the docs-root or publication boundary changes

## Ordering Rules

- `intake`, `decisions`, `plan`, and `change`
  - prefer reverse chronological order
- `features`, `requirements`, `specs`, and `lessons`
  - prefer logical grouping by module or domain, then stable alphabetical ordering

## Minimal README Sections

- Purpose
- How to enter this section
- What belongs here
- Naming / maintenance rules
- Links to current leaf docs or module indexes
