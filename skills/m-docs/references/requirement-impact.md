# Stable Docs Impact Checks

Use this file before editing `plan` or `change`.

## Mandatory Check Sequence

1. Identify the affected capability, feature, module, and participating repos.
2. Identify the active `docs_root`.
3. Read relevant docs when they exist:
   - `docs/intake` for original request evidence
   - `docs/features` for current user-visible behavior
   - `docs/requirements` for durable capability intent
   - `docs/specs` for technical contracts
   - `docs/decisions` for architecture decisions
   - `docs/lessons` for known recurring pitfalls
4. Decide whether the work:
   - implements existing stable docs without changing them
   - clarifies an existing stable doc
   - adds a new stable doc
   - deprecates or supersedes existing stable docs
5. Decide whether the work should create or update reusable `lessons`.
6. Record the conclusion explicitly in `plan` and `change`.

## Required Rules

- Do not write `change` first if the underlying feature behavior, requirement, spec, or decision changed.
- Do not treat code as the only source of truth when stable docs should change.
- If original request traceability matters, create or update `intake`.
- If user-visible behavior changed, update `features`.
- If durable capability intent changed, update `requirements`.
- If the technical contract changed, update `specs`.
- If a significant architecture choice was made or superseded, update `decisions`.
- If reusable troubleshooting knowledge emerged, record whether `lessons` changed and where it lives.
- Do not add docs remotes, push docs, publish docs, or choose backup targets as part of impact handling.

## Suggested Recording Language

### In plan

- `Intake impact: none | add | clarify`
- `Feature impact: none | clarify | add | deprecate`
- `Requirements impact: none | clarify | add | deprecate`
- `Specs impact: none | clarify | add | deprecate`
- `Decision impact: none | add | supersede`
- `Related intake: ...`
- `Related features: ...`
- `Related requirements: ...`
- `Related specs: ...`
- `Related decisions: ...`
- `Related lessons: ...` when already known

### In change

- `Intake impact: none | updated`
- `Feature impact: none | updated`
- `Requirements impact: none | updated`
- `Specs impact: none | updated`
- `Decision impact: none | updated`
- `Lessons impact: none | updated`
- `Related intake: ...`
- `Related features: ...`
- `Related requirements: ...`
- `Related specs: ...`
- `Related decisions: ...`
- `Related lessons: ...`

## Escalation Conditions

Stop and ask for clarification if:

- no docs root can be identified for governed docs and the task needs stable docs
- no stable feature, requirement, or spec can be found for a behavior-changing request
- multiple docs appear to be competing sources of truth
- the user request conflicts with written stable docs
- the only apparent docs location is inside a pushable code repo while the user expects private docs
