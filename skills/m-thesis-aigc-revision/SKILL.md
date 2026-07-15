---
name: m-thesis-aigc-revision
description: Revise thesis passages that read overly generic, repetitive, or template-like, especially when an AIGC report highlights suspicious sections. Use this skill to map flagged report segments back to the source draft, ground claims in real project evidence, replace summary-style boilerplate with concrete implementation detail, vary sentence rhythm, and preserve undergraduate academic accuracy without fabricating facts, data, or references.
---

# m:thesis-aigc-revision

## Overview

Use this skill when a Chinese undergraduate thesis has been flagged by an AIGC report, or when the prose clearly reads like generic template text. The goal is not to conceal fabrication. The goal is to revise high-risk passages so they are more specific, evidence-backed, and stylistically natural while keeping the facts true to the actual project.

## Quick Start

- If the user provides an AIGC report HTML, run `scripts/extract_report_segments.py` first to pull the flagged segment list.
- Read the thesis source file and locate the matching paragraphs before rewriting.
- Read `references/revision-patterns.md` before editing high-risk sections such as the abstract, system overview, architecture summary, security summary, deployment summary, and conclusion.
- Prioritize the highest-ratio or highest-word-count segments first.

## Workflow

1. Collect the three inputs:
   - thesis source draft
   - AIGC report or other flagged-segment report if available
   - project evidence such as repo docs, implemented pages, screenshots, module names, or proposal constraints
2. Extract the suspicious segments:
   - if the report is structured, use the script
   - otherwise read the report manually and note segment text, word count, and ratio
3. Map each flagged segment back to the thesis source:
   - match by unique wording
   - when the report is truncated, match by topic, paragraph rhythm, and nearby nouns
4. Diagnose why the paragraph is high risk:
   - too generic or symmetrical
   - too many summary sentences in a row
   - not enough project anchors
   - repeated transition phrases
   - lecture-note cadence instead of thesis narration
5. Rewrite one paragraph at a time:
   - keep the factual claim
   - replace generic overview language with concrete project objects, modules, pages, or observed behavior
   - vary long and short sentences without becoming colloquial
   - keep terminology consistent with the thesis
6. Re-check boundary claims:
   - do not overclaim features that are only partial, planned, or documented
   - do not invent experiments, metrics, references, or implementation details
7. Review the surrounding section:
   - ensure the revised paragraph still fits the chapter tone
   - smooth neighboring paragraphs if the style now breaks abruptly
8. Before finishing, confirm:
   - the highest-risk segments were revised first
   - the revised text is more grounded and less boilerplate
   - the meaning still matches the project evidence

## Rewrite Rules

- Prefer concrete nouns over abstract bundles. Name the actual page, module layer, runtime role, or interaction path when the thesis already established them.
- Replace broad evaluative claims with bounded observations. Use "from the current implementation," "in the present deployment form," or similar scope markers when needed.
- Break up overly balanced triple summaries. If three sentences all follow the same rhythm, merge one, split one, and anchor one in a concrete object.
- Avoid code-level trivia unless the thesis is explicitly discussing implementation internals. Keep the description at the system or module level.
- Preserve academic tone. The result should read like a careful undergraduate engineering thesis, not like marketing copy or casual speech.
- When revising English abstracts, keep the same factual scope as the Chinese version instead of translating old generic wording literally.

## Guardrails

- Do not use this skill to hide fabricated data, fake references, or non-existent features.
- Do not rewrite away a real mismatch between the thesis and the implementation. Flag it and narrow the claim instead.
- Do not inflate RBAC-style implementations into ABAC or other stronger claims without evidence.
- Do not add quantitative results that were never measured.
- Do not turn every paragraph into short punchy sentences. Rhythm variation is useful only when it still reads like formal academic prose.

## References

- `references/revision-patterns.md`
  - common high-risk signals, rewrite moves, and section-specific heuristics

## Scripts

- `scripts/extract_report_segments.py`
  - extract the suspicious-segment summary table from a report HTML and print the high-risk segment list

## Exit Criteria

Before finishing a revision task with this skill, confirm:

- the flagged segments were mapped to the real source paragraphs
- the revised paragraphs are more specific and less template-like
- unsupported claims were narrowed instead of hidden
- terminology remains consistent across the chapter
- the revision preserves factual accuracy

## Output

- Lead with the revision outcome and the highest-priority remaining issue, if any.
- When several segments were handled, use a compact table with segment or source location, risk signal, revision status, and evidence used.
- Link the source draft, report, and revised artifact with absolute clickable paths when local files are available.
- Keep full before/after passages in the edited document or a focused revision section; do not force long prose into table cells.
- Use a compact priority table or Mermaid only when segment ordering or chapter dependencies are genuinely difficult to follow. Do not add a decorative visualization to a straightforward paragraph revision.
