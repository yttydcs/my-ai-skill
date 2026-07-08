# m:docs Skill Spec

## Architecture Overview

The skill is packaged as `skills/m-docs` and keeps the routing logic in small reference files so the main `SKILL.md` stays concise while the docs system remains governed, private-docs aware, and queryable.

## Package Contract

- Source package: `skills/m-docs`
- UI metadata: `skills/m-docs/agents/openai.yaml`
- Install metadata: `manifests/m-docs.json`
- Install flow:
  - source -> `dist/codex/m-docs` -> `C:\Users\HelloWorld\.codex\skills\m-docs`

## Workflow Contract

- The skill must classify the request before writing docs.
- The skill must identify the active `docs_root` before writing governed docs.
- The skill must read `docs/README.md` and the nearest category README before editing leaf docs when those indexes exist.
- The skill must treat `intake`, `features`, `requirements`, `specs`, and `decisions` as evidence-bearing or stable-truth layers.
- The skill must treat `plan`, `change`, and `lessons` as workflow, archive, and learning layers.
- The skill must run feature/requirement/spec/decision impact checks before editing `plan` or `change`.
- The skill must update the minimum consistent set of leaf docs and indexes for each change.
- The skill must not infer remotes, push targets, or backup destinations for docs roots.

## Private Docs Root Contract

- A project may have a private docs root that is separate from every code repository.
- The private docs root is the canonical location for feature dossiers, intake records, decisions, plans, changes, and lessons when the user wants to keep docs out of pushable code repos.
- A private docs root may be:
  - a plain local folder
  - a separate local/private Git repository
  - a docs folder under a project root that is not itself a pushable code repo
- The skill may read and write local docs in the selected docs root.
- The skill must not add Git remotes, change remote URLs, push, publish, or choose backup strategy unless the user explicitly asks.
- If multiple candidate docs roots exist, stop and ask or record a blocker instead of guessing.

## Category Responsibility Contract

- `intake` owns original request evidence:
  - raw request text or source-preserving summaries
  - request source, date, requester when known
  - unresolved questions and routing links
- `features` own current user-visible feature truth:
  - end-to-end behavior
  - entry points, layout, controls, states, permissions, and CRUD workflows
  - acceptance scenarios and cross-repo ownership
- `requirements` own long-lived capability intent:
  - why the capability exists
  - what behavior is required
  - who or what it serves
  - what is in scope or out of scope
  - what acceptance criteria define success when no feature dossier owns the behavior
- `specs` own long-lived technical truth:
  - package or module structure
  - interfaces, routing rules, and integration contracts
  - technical constraints, workflow-control exceptions, and guardrails
  - validation, sync, and bootstrap behavior
- `decisions` own append-only architecture decision records:
  - context, options, decision, consequences, and supersession links
- `plan`, `change`, and `lessons` may reference stable truth but must not replace it.
- If a workflow changes feature behavior and technical contracts, update `features` first, then requirements, specs, or decisions as needed, then write `plan` and `change`.

## Self-Explanation Contract

- The stable docs must be detailed enough that a future editor can classify new content without relying on chat history.
- Category README files may summarize the boundary, but stable requirement/spec docs and skill references must carry the durable rule set.
- The boundary must remain explicit when lessons, change archives, or workflow plans are updated.

## Lessons Lookup Contract

- Troubleshooting or "have we seen this before?" requests start from `docs/lessons/README.md` and matching lesson docs when available.
- Lesson docs must include lookup hints such as symptoms, keywords or error text, trigger conditions, and quick checks.
- `docs/lessons/README.md` should expose short symptom or keyword clues for later lookup.
- If no lesson matches, the skill falls back to `docs/change/`, then confirms stable truth in `docs/features/`, `docs/specs/`, and `docs/requirements/`.
- Reusable troubleshooting knowledge must be promoted into `lessons` instead of being left only in `change`.

## Bootstrap Contract

- `skills/m-docs/scripts/bootstrap_docs_tree.py` must create the core docs categories plus `docs/README.md`.
- The generated root README must include reading order, troubleshooting order, and private docs root guidance.
- The generated `docs/intake/README.md` must explain source evidence handling.
- The generated `docs/features/README.md` must explain feature dossier maintenance.
- The generated `docs/decisions/README.md` must explain append-only decision records.
- The generated `docs/change/README.md` must remind users to promote reusable troubleshooting knowledge into `lessons`.
- The generated `docs/lessons/README.md` must require lookup hints.

## Validation Contract

- The skill must pass `tools/validate-skills.ps1 -Skill m-docs`.
- The skill must sync through `tools/sync-skills.ps1 -Skill m-docs`.

## Safety and Stability

- Do not duplicate stable truth across categories.
- Do not hand-edit protected generated sections unless the target repo explicitly allows it.
- Do not use `lessons` as the only home for feature, requirement, spec, or decision corrections.
- Do not let `change` or `plan` become the only place where category boundaries are explained.
- Do not write private docs into pushable code repos unless the user has explicitly selected that repo as the docs root.
- Do not infer docs remote, push, or backup behavior.

## Performance Considerations

- Keep the main skill and references concise enough for selective loading.
- Prefer updating the minimum consistent set of indexes instead of broad doc rewrites.

## Related Requirements

- [../requirements/m-docs-skill.md](../requirements/m-docs-skill.md)

## Related Changes

- [../change/2026-03-22_docs-governor-skill.md](../change/2026-03-22_docs-governor-skill.md)
- [../change/2026-03-23_lessons-archive-lookup.md](../change/2026-03-23_lessons-archive-lookup.md)
- [../change/2026-03-24_requirements-specs-responsibility-clarity.md](../change/2026-03-24_requirements-specs-responsibility-clarity.md)
- [../change/2026-03-24_skill-prefix-rename.md](../change/2026-03-24_skill-prefix-rename.md)
