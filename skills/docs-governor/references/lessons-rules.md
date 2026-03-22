# Lessons Rules

Use this file when deciding whether to create or update a `lessons` document.

## When to Create a Lesson

Create or update a lesson when at least one of these is true:

- the issue is likely to recur
- the debugging path was expensive or non-obvious
- the root cause came from a structural weakness, not a one-off typo
- the incident reveals a rule the team should remember

## What a Lesson Should Answer

- What happened?
- How did it present?
- Why did it happen?
- How was it diagnosed?
- What fixed it?
- What should be checked next time before this happens again?

## Required Sections

- Summary
- Symptoms
- Impact
- Trigger Conditions
- Root Cause
- Investigation Trail
- Resolution
- Prevention / Guardrails
- Related Requirements / Specs / Changes

## Relationship to Other Docs

- If the incident revealed a missing or wrong requirement, update `requirements`.
- If the incident revealed a wrong technical contract, update `specs`.
- If the incident came from a concrete workflow, link the relevant `change`.
- Do not store the only copy of a technical rule inside `lessons`.
