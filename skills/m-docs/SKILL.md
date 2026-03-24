---
name: m-docs
description: Govern project documentation structure, routing, indexing, and archival. Use when Codex must decide where documentation belongs, create or repair a docs tree, route content between requirements, specs, plan, change, and lessons, check whether requirements or specs changed before updating plans or change logs, or maintain indexes and protected generated sections.
---

# m:docs

## Overview

Use this skill to treat project documentation as a governed system with stable truth, archival layers, explicit indexes, and reusable troubleshooting knowledge. Classify the request first, then read the minimum required entry docs, determine the canonical destination, run requirement/spec impact checks, and update the target doc plus any required indexes.

## Quick Start

- For docs tree creation or repair, run `scripts/bootstrap_docs_tree.py` and review the generated `README.md` files.
- For "where should this doc go?" questions, read `references/taxonomy.md` and `references/routing-rules.md`.
- For plan or change work, read `references/requirement-impact.md` before editing.
- For index maintenance, read `references/indexing-rules.md`.
- For postmortems, pitfalls, and recurring failure patterns, read `references/lessons-rules.md`.
- For troubleshooting, "have we seen this before?", or direct problem lookup, start from `references/lessons-rules.md` and the relevant `docs/lessons` entry before scanning `change` logs.
- For standard section layouts, read `references/templates.md`.

## Workflow

1. Classify the work into one of these categories:
   - `requirements`
   - `specs`
   - `plan`
   - `change`
   - `lessons` / troubleshooting lookup
   - index / entry maintenance
   - docs tree bootstrap
2. Read the current entry docs:
   - start with `docs/README.md` if it exists
   - then read the nearest category `README.md`
   - for troubleshooting lookup, prefer `docs/lessons/README.md` and matching lesson docs before `docs/change/`
   - then read only the affected leaf docs
3. Determine the canonical destination:
   - stable truth belongs in `requirements` or `specs`
   - workflow execution belongs in `plan`
   - completed results belong in `change`
   - reusable incident knowledge and lookup guidance belong in `lessons`
4. Run requirement and spec impact checks before editing `plan` or `change`.
5. Write the minimum consistent set of files:
   - target leaf doc
   - affected category index
   - root `docs/README.md` only if entry topology changes or a new global troubleshooting path must be exposed
6. Preserve protected content:
   - do not hand-edit generated regions unless the manual section explicitly allows it
   - do not turn archive docs into new sources of truth
7. Cross-link related artifacts so the docs chain and troubleshooting lookup path remain navigable.

## Guardrails

- Do not duplicate the same truth across categories.
- `plan`, `change`, and `lessons` are archival layers, not long-lived requirements/specs.
- If the project lacks a docs structure, bootstrap it before inventing ad hoc paths.
- If a request changes behavior, check whether `requirements` and `specs` must change before writing `change`.
- Do not leave reusable troubleshooting guidance only in `change`; promote it into `lessons`.
- If generated docs contain protected regions, edit only permitted manual sections.

## References

- `references/taxonomy.md`
  - category definitions, canonical intent, and source-of-truth boundaries
- `references/routing-rules.md`
  - decision tree for document placement and examples
- `references/indexing-rules.md`
  - root and category index obligations, naming, and maintenance
- `references/requirement-impact.md`
  - mandatory requirement/spec impact checks and record rules
- `references/lessons-rules.md`
  - when to create lessons and how to structure them
- `references/templates.md`
  - concise templates for docs categories and indexes

## Scripts

- `scripts/bootstrap_docs_tree.py`
  - create the recommended `docs/` tree with category indexes and optional module buckets

## Exit Criteria

Before finishing a docs task with this skill, confirm:

- the target doc is in the correct category
- requirement/spec impact is explicitly recorded when needed
- all required indexes were updated
- protected or generated content was not edited unsafely
