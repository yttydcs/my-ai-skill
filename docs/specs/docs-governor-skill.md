# Docs Governor Skill Spec

## Architecture Overview

The skill is packaged as `skills/docs-governor` and keeps the routing logic in small reference files so the main `SKILL.md` stays concise while the docs system remains governed and queryable.

## Package Contract

- Source package: `skills/docs-governor`
- UI metadata: `skills/docs-governor/agents/openai.yaml`
- Install metadata: `manifests/docs-governor.json`
- Install flow:
  - source -> `dist/codex/docs-governor` -> `C:\Users\HelloWorld\.codex\skills\docs-governor`

## Workflow Contract

- The skill must classify the request before writing docs.
- The skill must read `docs/README.md` and the nearest category README before editing leaf docs when those indexes exist.
- The skill must treat `requirements` and `specs` as stable truth.
- The skill must treat `plan`, `change`, and `lessons` as archival layers.
- The skill must run requirement/spec impact checks before editing `plan` or `change`.
- The skill must update the minimum consistent set of leaf docs and indexes for each change.

## Lessons Lookup Contract

- Troubleshooting or "have we seen this before?" requests start from `docs/lessons/README.md` and matching lesson docs when available.
- Lesson docs must include lookup hints such as symptoms, keywords or error text, trigger conditions, and quick checks.
- `docs/lessons/README.md` should expose short symptom or keyword clues for later lookup.
- If no lesson matches, the skill falls back to `docs/change/`, then confirms stable truth in `docs/specs/` and `docs/requirements/`.
- Reusable troubleshooting knowledge must be promoted into `lessons` instead of being left only in `change`.

## Bootstrap Contract

- `skills/docs-governor/scripts/bootstrap_docs_tree.py` must create the five core docs categories plus `docs/README.md`.
- The generated root README must include both reading order and troubleshooting order guidance.
- The generated `docs/change/README.md` must remind users to promote reusable troubleshooting knowledge into `lessons`.
- The generated `docs/lessons/README.md` must require lookup hints.

## Validation Contract

- The skill must pass `tools/validate-skills.ps1 -Skill docs-governor`.
- The skill must sync through `tools/sync-skills.ps1 -Skill docs-governor`.

## Safety and Stability

- Do not duplicate stable truth across categories.
- Do not hand-edit protected generated sections unless the target repo explicitly allows it.
- Do not use `lessons` as the only home for requirement or spec corrections.

## Performance Considerations

- Keep the main skill and references concise enough for selective loading.
- Prefer updating the minimum consistent set of indexes instead of broad doc rewrites.

## Related Requirements

- [../requirements/docs-governor-skill.md](../requirements/docs-governor-skill.md)

## Related Changes

- [../change/2026-03-22_docs-governor-skill.md](../change/2026-03-22_docs-governor-skill.md)
- [../change/2026-03-23_lessons-archive-lookup.md](../change/2026-03-23_lessons-archive-lookup.md)
