# m:docs Skill Spec

## Architecture Overview

The skill is packaged as `skills/m-docs` and keeps the routing logic in small reference files so the main `SKILL.md` stays concise while the docs system remains governed and queryable.

## Package Contract

- Source package: `skills/m-docs`
- UI metadata: `skills/m-docs/agents/openai.yaml`
- Install metadata: `manifests/m-docs.json`
- Install flow:
  - source -> `dist/codex/m-docs` -> `C:\Users\HelloWorld\.codex\skills\m-docs`

## Workflow Contract

- The skill must classify the request before writing docs.
- The skill must read `docs/README.md` and the nearest category README before editing leaf docs when those indexes exist.
- The skill must treat `requirements` and `specs` as stable truth.
- The skill must treat `plan`, `change`, and `lessons` as archival layers.
- The skill must run requirement/spec impact checks before editing `plan` or `change`.
- The skill must update the minimum consistent set of leaf docs and indexes for each change.

## Requirements And Specs Responsibility Contract

- `requirements` own long-lived capability intent:
  - why the capability exists
  - what behavior is required
  - who or what it serves
  - what is in scope or out of scope
  - what acceptance criteria define success
- `specs` own long-lived technical truth:
  - package or module structure
  - interfaces, routing rules, and integration contracts
  - technical constraints, workflow-control exceptions, and guardrails
  - validation, sync, and bootstrap behavior
- `plan`, `change`, and `lessons` may reference the boundary but must not replace it.
- If a workflow changes both intent and implementation contract, update `requirements` first, then `specs`, then write `plan` and `change`.

## Self-Explanation Contract

- The stable requirement and spec docs must be detailed enough that a future editor can classify new content without relying on chat history.
- Category README files may summarize the boundary, but the stable requirement/spec docs must carry the durable rule set.
- The boundary must remain explicit when lessons, change archives, or workflow plans are updated.

## Lessons Lookup Contract

- Troubleshooting or "have we seen this before?" requests start from `docs/lessons/README.md` and matching lesson docs when available.
- Lesson docs must include lookup hints such as symptoms, keywords or error text, trigger conditions, and quick checks.
- `docs/lessons/README.md` should expose short symptom or keyword clues for later lookup.
- If no lesson matches, the skill falls back to `docs/change/`, then confirms stable truth in `docs/specs/` and `docs/requirements/`.
- Reusable troubleshooting knowledge must be promoted into `lessons` instead of being left only in `change`.

## Bootstrap Contract

- `skills/m-docs/scripts/bootstrap_docs_tree.py` must create the five core docs categories plus `docs/README.md`.
- The generated root README must include both reading order and troubleshooting order guidance.
- The generated `docs/change/README.md` must remind users to promote reusable troubleshooting knowledge into `lessons`.
- The generated `docs/lessons/README.md` must require lookup hints.

## Validation Contract

- The skill must pass `tools/validate-skills.ps1 -Skill m-docs`.
- The skill must sync through `tools/sync-skills.ps1 -Skill m-docs`.

## Safety and Stability

- Do not duplicate stable truth across categories.
- Do not hand-edit protected generated sections unless the target repo explicitly allows it.
- Do not use `lessons` as the only home for requirement or spec corrections.
- Do not let `change` or `plan` become the only place where the `requirements` versus `specs` split is explained.

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
