# Requirement and Spec Impact Checks

Use this file before editing `plan` or `change`.

## Mandatory Check Sequence

1. Identify the affected capability or module.
2. Read the relevant `requirements` docs.
3. Read the relevant `specs` docs.
4. Decide whether the work:
   - implements existing requirements/specs without changing them
   - clarifies an existing requirement or spec
   - adds a new requirement or spec
   - deprecates or removes an existing requirement or spec
5. Record the conclusion explicitly in `plan` and `change`.

## Required Rules

- Do not write `change` first if the underlying requirement changed.
- Do not treat code as the only source of truth when stable docs should change.
- If the requirement changed, update `requirements` before or alongside `change`.
- If the technical contract changed, update `specs` before or alongside `change`.

## Suggested Recording Language

### In plan

- `Requirements impact: none | clarify | add | deprecate`
- `Specs impact: none | clarify | add | deprecate`
- `Related requirements: ...`
- `Related specs: ...`

### In change

- `Requirements impact: none | updated`
- `Specs impact: none | updated`
- `Related requirements: ...`
- `Related specs: ...`

## Escalation Conditions

Stop and ask for clarification if:

- no stable requirement or spec can be found for a behavior-changing request
- multiple docs appear to be competing sources of truth
- the user request conflicts with the written requirement or spec
