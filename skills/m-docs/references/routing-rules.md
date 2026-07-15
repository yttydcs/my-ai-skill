# Routing Rules

Use this file when deciding where a document should live.

## Docs Root Decision

1. If the user explicitly names a `docs_root`, use it.
2. If the project has a private docs root, use that root for governed docs.
3. If the current path is a code repository and the user has said docs should not be pushed with code, do not write governed docs there.
4. If several candidate docs roots exist, ask or record a blocker instead of guessing.
5. If no docs root exists and the task requires stable docs, bootstrap a docs root only when the target root is confirmed.

## Category Decision Tree

Before classifying content, check whether it is reusable Agent context explicitly intended for `$m-context`. If so, route it to `<docs_root>/context` only when the user selected local scope; do not treat it as intake, feature, requirement, spec, decision, plan, change, lesson, or index content.

1. Ask whether the content is original request evidence, current feature truth, durable requirement, technical contract, architecture decision, workflow history, or troubleshooting lookup.
2. If it is original request evidence:
   - route to `intake`
3. If it is current user-visible feature behavior:
   - route to `features`
4. If it is durable capability intent, scope, actor, boundary, or non-feature acceptance:
   - route to `requirements`
5. If it is a technical contract, protocol, API, schema, architecture constraint, or generated-doc rule:
   - route to `specs`
6. If it records an architecturally significant choice and alternatives:
   - route to `decisions`
7. If it is troubleshooting lookup:
   - start with `lessons`
8. If it is workflow history:
   - planned work before or during execution -> `plan`
   - completed result and verification -> `change`
   - reusable incident knowledge or pitfall pattern -> `lessons`
9. If it is only navigation:
   - update the nearest `README.md`

## Typical Mappings

- "Where do I store the original request?"
  - `docs/intake/YYYY-MM-DD_topic.md`
- "Where does personnel management CRUD, buttons, layout, permissions, and acceptance go?"
  - `docs/features/personnel-management.md`
- "Where does a module's broad acceptance criteria go?"
  - `docs/requirements/<module>/...`
- "Where does a protocol action table go?"
  - `docs/specs/<domain>/...`
- "Where do I record why we chose event sync over polling?"
  - `docs/decisions/YYYY-MM-DD_event-sync.md`
- "Where do I archive this implementation breakdown?"
  - `docs/plan/YYYY-MM-DD_topic.md`
- "Where do I record what shipped?"
  - `docs/change/YYYY-MM-DD_topic.md`
- "Where do I store a root-cause analysis for a repeated outage?"
  - `docs/lessons/<domain>/...`
- "This error or symptom appeared again. Where should I look first?"
  - `docs/lessons/<domain>/...`

## Feature-first Rules

- For user-visible features, keep one complete feature dossier as the current truth.
- A feature dossier may link to several code repositories, but the feature truth should not be copied into every repo.
- Put screen layout, button placement, form states, validation states, permissions, CRUD workflows, and acceptance scenarios in `features`.
- Put the API, schema, event, job, or integration contract that supports the feature in `specs`.
- Put the rationale for a hard-to-reverse architectural choice in `decisions`.

## Multi-repo Rules

- Project-level or product-level behavior belongs in the private docs root.
- Code repositories are implementation carriers unless the user explicitly selects one as the docs root.
- For a cross-repo capability, create or update one private feature doc and link each participating repo or module from that doc.
- Repo-local docs may exist, but do not treat them as canonical when a private docs root is present.

## Troubleshooting Lookup

When the request is about a symptom, outage, debugging shortcut, or repeated confusion:

1. start with `docs/lessons/README.md`
2. match by symptom, module, trigger condition, and keywords or error text
3. read the matching lesson doc before scanning `docs/change/`
4. if no lesson matches, fall back to `change`, then confirm stable truth in `features`, `specs`, and `requirements`
5. after resolution, promote reusable knowledge into `lessons` instead of leaving it only in `change`

## Stable Naming Guidance

- `features`, `requirements`, `specs`, and `lessons`
  - prefer stable names without dates
- `intake`, `decisions`, `plan`, and `change`
  - prefer `YYYY-MM-DD_topic.md` when tied to a dated request, decision, or workflow

## When Multiple Categories Are Involved

If one request touches several categories:

1. create or update `intake` first when original request traceability matters
2. update `features` when user-visible behavior changed
3. update `requirements` when durable capability intent changed
4. update `specs` when the technical contract changed
5. update `decisions` when an architecturally significant choice was made or superseded
6. write or update `plan` for workflow execution
7. write `change` after implementation or analysis completes
8. add or update `lessons` only when there is reusable operational knowledge

## Publication Rules

- Do not add remotes, push docs, publish docs, or choose backup targets unless the user explicitly asks.
- If the docs root is a Git repository, local commits may be used only when requested or when project-local rules require them.
- Keep docs publication decisions separate from code repository branch, commit, and push decisions.
- Exclude `context/` from normal governed-doc indexing, archival, staging, and commit write sets. Do not modify ignore configuration for it unless the user explicitly requests that separate Git action.

## Anti-patterns

- Writing acceptance criteria only in `change`
- Treating `plan` as the permanent source of module behavior
- Treating `change` as the original request
- Splitting one feature's CRUD and UI behavior across unrelated specs without a feature dossier
- Storing protocol details in `lessons`
- Logging recurring failures only in `change` without a reusable `lessons` entry
- Starting every troubleshooting request from `change` when a reusable `lessons` entry already exists
- Writing private docs into a pushable code repo because it happens to be the current working directory
