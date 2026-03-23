# Lessons Rules

Use this file when deciding whether to create or update a `lessons` document.

## When to Create a Lesson

Create or update a lesson when at least one of these is true:

- the issue is likely to recur
- the debugging path was expensive or non-obvious
- the root cause came from a structural weakness, not a one-off typo
- the incident reveals a rule the team should remember
- the same question would otherwise require re-reading `change` logs or chat history

## Troubleshooting-first Lookup

When the user asks how to debug a symptom, whether a problem has happened before, or what should be checked first:

1. search `docs/lessons` first by symptom, module, trigger condition, and keywords or error text
2. use `docs/change` only when the lesson doc is missing or insufficient
3. after resolution, decide whether the new investigation should update or create a reusable lesson

## What a Lesson Should Answer

- What happened?
- How did it present?
- Why did it happen?
- How was it diagnosed?
- What fixed it?
- What should be checked next time before this happens again?
- How can someone recognize it quickly next time?

## Required Sections

- Summary
- Lookup Hints
- Symptoms
- Impact
- Trigger Conditions
- Root Cause
- Investigation Trail
- Resolution
- Prevention / Guardrails
- Related Requirements / Specs / Changes

## Lookup Hints Checklist

Each lesson should make future lookup easier. Capture at least:

- likely symptoms or user-facing signals
- keywords, error text, or aliases someone may search for
- trigger conditions or environment cues
- quick checks to run before repeating the full investigation

## Relationship to Other Docs

- If the incident revealed a missing or wrong requirement, update `requirements`.
- If the incident revealed a wrong technical contract, update `specs`.
- If the incident came from a concrete workflow, link the relevant `change`.
- Update the nearest `docs/lessons/README.md` so the lesson remains discoverable from the index.
- Do not store the only copy of a technical rule inside `lessons`.
