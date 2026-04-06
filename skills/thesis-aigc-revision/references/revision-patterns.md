# Revision Patterns

Use this file when the thesis text has already been drafted and the task is targeted revision rather than first-pass writing.

## 1. Common High-Risk Signals

The following patterns often trigger “AI-written” suspicion even when the content is factually correct:

- the paragraph is all overview and no object
- three or more sentences use the same explanatory rhythm
- abstract nouns dominate concrete nouns
- repeated transitions such as “from this perspective,” “furthermore,” “therefore,” “in addition,” or their Chinese equivalents
- broad capability summaries with no scope marker
- architecture paragraphs that sound like product introductions
- security paragraphs that list ideals rather than current implemented rules
- conclusion paragraphs that restate the whole paper in compressed lecture-note form

## 2. Core Rewrite Moves

### 2.1 Anchor the paragraph

Before:
- a system-level summary with no concrete object

After:
- identify the actual host, page, module, protocol layer, or user path that carries the claim

Examples of anchors:
- a local host page
- an independent service process
- a protocol layer split
- a specific user operation chain
- the current implementation boundary

### 2.2 Narrow the claim

Replace:
- “the system fully realizes...”
- “the platform comprehensively supports...”

With:
- “the current implementation supports...”
- “in the present deployment form...”
- “the project currently provides...”

This keeps the prose honest and usually makes it sound less templated.

### 2.3 Break symmetric summaries

If three consecutive sentences all follow the same pattern, revise them into different roles:

- one sentence names the concrete object
- one sentence explains the design intent
- one sentence states the current boundary or observed effect

### 2.4 Prefer system-level detail over code trivia

For thesis prose, avoid raw function names, raw code expressions, or tiny execution details unless the chapter explicitly analyzes implementation internals. Replace code details with:

- continuous byte-stream reading
- frame parsing
- worker-based dispatch
- connection-order write-out
- parent-child routing

## 3. Section-Specific Heuristics

## Abstract

- Avoid sweeping value judgments.
- Mention the concrete deployment form, host, or topology.
- Keep Chinese and English abstracts aligned in scope.
- If the abstract sounds like a product brochure, reduce evaluation and increase structure.

## Architecture Summary

- Name the actual layers once.
- Then explain why the layers are separated.
- Avoid repeating “responsible for” in every clause if the sentence becomes mechanical.

## Security / Permission Summary

- Describe implemented rules, not ideal security doctrine.
- Prefer concrete boundaries such as source validation, explicit failure, approval flow, or permission-node checks.
- Narrow anything that sounds stronger than the current implementation.

## Deployment / Demo Chain

- Use the actual user path in the current host or runtime.
- Mention what the host does versus what the independent service process does.
- A short sequence is usually better than a grand platform summary.

## Conclusion

- Do not re-summarize every chapter in the same cadence.
- Emphasize the actual engineering value and the current maturity boundary.
- Keep future work specific and scoped.

## 4. Safe Style Checklist

- factual scope is narrower, not broader
- paragraph has at least one concrete anchor
- sentence lengths are varied but still formal
- repeated transition phrases were reduced
- no fabricated data, references, or implementation claims were introduced
