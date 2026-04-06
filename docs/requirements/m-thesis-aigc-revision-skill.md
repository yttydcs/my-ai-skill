# m:thesis-aigc-revision Skill

## Background

This repository needs a reusable skill for thesis revision when a Chinese undergraduate draft is flagged as overly generic, repetitive, or template-like by an AIGC report. The current gap is not first-pass drafting. The gap is targeted revision after suspicious segments have already been identified.

## Goal

Provide a reusable skill that helps Codex revise flagged thesis passages into more specific, evidence-backed, and academically natural prose without fabricating content or overstating implementation maturity.

## Scope

### Must

- support Chinese undergraduate engineering theses and similar project-backed papers
- accept a thesis draft plus an AIGC report when available
- help map suspicious report segments back to the real source paragraphs
- prioritize the highest-risk or highest-volume suspicious segments first
- revise paragraphs by grounding them in real project evidence
- preserve factual accuracy and current implementation boundaries
- reduce boilerplate summary tone, repetitive cadence, and generic wording
- explicitly forbid fabricated data, fake references, and hidden overclaims

### Should

- work even when the report is HTML with a structured suspicious-segment table
- support aligned revision of Chinese and English abstracts
- give section-specific guidance for abstracts, architecture summaries, security summaries, deployment paths, and conclusions

### Out of Scope

- inventing experiments, evaluation metrics, or references
- hiding known implementation gaps instead of narrowing the claim
- guaranteeing any specific detector score
- rewriting a thesis from zero when the task is really full draft generation

## Primary Scenarios

1. A user provides a suspicious-segment report plus the thesis draft and asks for targeted revision.
2. A user has no report but wants help revising paragraphs that feel too “AI-like” or templated.
3. A user needs the English abstract revised to match a newly narrowed Chinese abstract.

## Acceptance Criteria

- The skill exists as a valid package in this repository.
- The skill can explain a deterministic revision workflow from report parsing through paragraph rewriting.
- The skill includes durable rewrite guidance that emphasizes specificity, scope control, and factual grounding.
- The skill includes a script that extracts suspicious segment summaries from a report HTML without extra dependencies.
- The repository requirements and specs indexes include this capability.

## Related Specs

- [../specs/m-thesis-aigc-revision-skill.md](../specs/m-thesis-aigc-revision-skill.md)
