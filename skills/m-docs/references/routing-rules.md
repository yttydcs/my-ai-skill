# Routing Rules

Use this file when deciding where a document should live.

## Decision Tree

1. Ask whether the content is long-lived truth, workflow-specific history, or troubleshooting lookup.
2. If it is troubleshooting lookup:
   - start with `lessons`
3. If it is long-lived truth:
   - user need, scope, acceptance -> `requirements`
   - technical contract, protocol, architecture, schema -> `specs`
4. If it is workflow history:
   - planned work before or during execution -> `plan`
   - completed result and verification -> `change`
   - reusable incident knowledge or pitfall pattern -> `lessons`
5. If it is only navigation:
   - update the nearest `README.md`

## Typical Mappings

- "Where does a module's acceptance criteria go?"
  - `docs/requirements/<module>/...`
- "Where does a protocol action table go?"
  - `docs/specs/<domain>/...`
- "Where do I archive this implementation breakdown?"
  - `docs/plan/YYYY-MM-DD_topic.md`
- "Where do I record what shipped?"
  - `docs/change/YYYY-MM-DD_topic.md`
- "Where do I store a root-cause analysis for a repeated outage?"
  - `docs/lessons/<domain>/...`
- "This error or symptom appeared again. Where should I look first?"
  - `docs/lessons/<domain>/...`

## Troubleshooting Lookup

When the request is about a symptom, outage, debugging shortcut, or repeated confusion:

1. start with `docs/lessons/README.md`
2. match by symptom, module, trigger condition, and keywords or error text
3. read the matching lesson doc before scanning `docs/change/`
4. if no lesson matches, fall back to `change`, then confirm stable truth in `specs` and `requirements`
5. after resolution, promote reusable knowledge into `lessons` instead of leaving it only in `change`

## Stable Naming Guidance

- `requirements`, `specs`, and `lessons`
  - prefer stable names without dates
- `plan` and `change`
  - prefer `YYYY-MM-DD_topic.md`

## When Multiple Categories Are Involved

If one request touches several categories:

1. update `requirements` first if the need changed
2. update `specs` next if the technical contract changed
3. write or update `plan` for workflow execution
4. write `change` after implementation or analysis completes
5. add or update `lessons` only when there is reusable operational knowledge

## Anti-patterns

- Writing acceptance criteria only in `change`
- Treating `plan` as the permanent source of module behavior
- Storing protocol details in `lessons`
- Logging recurring failures only in `change` without a reusable `lessons` entry
- Starting every troubleshooting request from `change` when a reusable `lessons` entry already exists
